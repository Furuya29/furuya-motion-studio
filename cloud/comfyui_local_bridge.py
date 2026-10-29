#!/usr/bin/env python3
"""ComfyUI LOCAL execution bridge for an existing, user-supplied API workflow.

This is a real /prompt -> /history -> /view bridge, not a model implementation.
Runs only against 127.0.0.1 / localhost, with an already-installed ComfyUI,
appropriate models, exported API-format workflow and its required custom nodes.
Dry-run is default; --execute --confirm-free-gpu explicitly opts in to ONE
submission. After uncertain submission, never resend automatically.
Python stdlib only. No paid endpoints, shell commands or automatic downloads.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import time
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen
from uuid import uuid4

SAFE_FILE = re.compile(r"^[^/\\]+$")
VIDEO_SUFFIXES = {".mp4", ".webm", ".mov"}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}


def local_base(value: str) -> str:
    url = urlsplit(value)
    if (url.scheme != "http" or url.hostname not in ("127.0.0.1", "localhost")
            or not url.port or url.username or url.password
            or url.path not in ("", "/") or url.query or url.fragment):
        raise ValueError("Only an explicit local HTTP ComfyUI server is supported (e.g. http://127.0.0.1:8188).")
    return f"http://127.0.0.1:{url.port}"


def api_json(base: str, path: str, payload: dict | None = None) -> dict:
    raw = None if payload is None else json.dumps(payload).encode("utf-8")
    request = Request(base + path, data=raw,
                      headers={"Content-Type": "application/json"} if raw is not None else {},
                      method="POST" if raw is not None else "GET")
    with urlopen(request, timeout=18) as response:
        result = json.load(response)
    if not isinstance(result, dict):
        raise ValueError("ComfyUI returned a non-object response")
    return result


def workflow_api(workflow_path: Path) -> dict:
    data = json.loads(workflow_path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and isinstance(data.get("prompt"), dict):
        data = data["prompt"]
    if not isinstance(data, dict) or not data:
        raise ValueError("Expected nonempty ComfyUI workflow in API format")
    if "nodes" in data and "links" in data:
        raise ValueError("UI graph JSON detected. Export 'Save (API Format)' from ComfyUI.")
    for node_id, node in data.items():
        if (not str(node_id).isdigit() or not isinstance(node, dict)
                or not isinstance(node.get("class_type"), str)
                or not isinstance(node.get("inputs"), dict)):
            raise ValueError(f"Invalid API-format node: {node_id}")
    return data


def verify_media(path: Path, formats: set[str]) -> Path:
    resolved = path.expanduser().resolve()
    if not resolved.is_file() or resolved.stat().st_size < 1024 or resolved.suffix.lower() not in formats:
        raise ValueError("Missing or unsupported media: " + str(path))
    return resolved


def bind(workflow: dict, *, video_id: str, video_field: str, image_id: str,
         image_field: str, video_file: str, image_file: str) -> dict:
    # Copy every node input structure: never edit the source workflow in-place.
    nodes = json.loads(json.dumps(workflow))
    for node_id, name, value in (
        (video_id, video_field, video_file), (image_id, image_field, image_file)
    ):
        if node_id not in nodes or name not in nodes[node_id]["inputs"]:
            raise ValueError("ComfyUI workflow node/field not found: " + str(node_id) + "." + name)
        if not isinstance(nodes[node_id]["inputs"][name], str):
            raise ValueError("Expected a filename string field in node " + str(node_id))
        nodes[node_id]["inputs"][name] = value
    return nodes


def stage(source: Path, dest: Path) -> str:
    # Copy only media; use deterministic content-addressed names and no replacement.
    digest = hashlib.sha256()
    with source.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(block)
    name = "furuya_" + digest.hexdigest()[:20] + source.suffix.lower()
    target = dest / name
    if target.exists():
        if target.stat().st_size != source.stat().st_size:
            raise ValueError("Staged file collision: " + name)
    else:
        # Atomic rename prevents a partial file from looking ready.
        tmp = dest / ("." + name + "." + uuid4().hex + ".partial")
        try:
            shutil.copyfile(source, tmp)
            tmp.replace(target)
        finally:
            tmp.unlink(missing_ok=True)
    return name


def video_outputs(history: dict, prompt_id: str) -> list[dict]:
    entry = history.get(prompt_id, {})
    outputs = entry.get("outputs", {}) if isinstance(entry, dict) else {}
    files = []
    for node in outputs.values():
        if not isinstance(node, dict):
            continue
        for key in ("gifs", "videos", "files"):
            for file in node.get(key, []) or []:
                if not isinstance(file, dict):
                    continue
                filename = file.get("filename")
                subfolder = file.get("subfolder", "")
                ftype = file.get("type", "output")
                if (isinstance(filename, str) and SAFE_FILE.fullmatch(filename)
                        and Path(filename).suffix.lower() in (".mp4", ".webm")
                        and isinstance(subfolder, str)
                        and not (Path(subfolder).is_absolute() or ".." in Path(subfolder).parts or "\\" in subfolder)
                        and ftype in ("output", "temp")):
                    files.append({"filename": filename, "subfolder": subfolder, "type": ftype})
    return files


def download(base: str, file: dict, output: Path) -> int:
    query = urlencode(file)
    with urlopen(base + "/view?" + query, timeout=120) as response:
        mime = response.headers.get("Content-Type", "").split(";", 1)[0]
        if mime not in ("video/mp4", "video/webm", "application/octet-stream"):
            raise ValueError("ComfyUI /view returned unexpected media type: " + mime)
        tmp = output.with_name("." + output.name + "." + uuid4().hex + ".partial")
        size = 0
        try:
            with tmp.open("wb") as dest:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    size += len(chunk)
                    if size > 1000 * 1024 * 1024:
                        raise ValueError("Output exceeds 1GB limit")
                    dest.write(chunk)
            if size < 1024:
                raise ValueError("ComfyUI output video too small")
            with tmp.open("rb") as check:
                signature = check.read(32)
            suffix = output.suffix.lower()
            if suffix == ".mp4" and b"ftyp" not in signature:
                raise ValueError("ComfyUI output is not a valid MP4 container header")
            if suffix == ".webm" and not signature.startswith(b"\x1a\x45\xdf\xa3"):
                raise ValueError("ComfyUI output is not a valid WebM container header")
            if output.exists():
                raise ValueError("Refusing to overwrite existing output")
            tmp.replace(output)
            return size
        finally:
            tmp.unlink(missing_ok=True)


def job_plan(args) -> dict:
    base = local_base(args.server)
    wf = workflow_api(args.workflow.expanduser().resolve())
    video = verify_media(args.video, VIDEO_SUFFIXES)
    image = verify_media(args.image, IMAGE_SUFFIXES)
    input_dir = args.input_dir.expanduser().resolve()
    if not input_dir.is_dir():
        raise ValueError("Existing ComfyUI input directory required; no installation is performed.")
    if not args.output.parent.expanduser().resolve().is_dir():
        raise ValueError("Output parent directory does not exist")
    if args.output.exists():
        raise ValueError("Refusing to overwrite an existing video")
    bind(wf, video_id=args.video_node, video_field=args.video_field,
         image_id=args.image_node, image_field=args.image_field,
         video_file=video.name, image_file=image.name)
    return {
        "schema": "furuya-comfyui-bridge/1",
        "server": base,
        "workflow_nodes": len(wf),
        "mode": "DRY_RUN" if not args.execute else "EXPLICIT_SUBMISSION",
        "media": {"video": video.name, "image": image.name},
        "output": str(args.output),
        "model_inference_verified": False,
        "free_gpu_verified": False,
        "notice": "Source workflow must already contain valid model/VideoHelperSuite/custom nodes. No integration claims until actual MP4 is returned."
    }


def run(args) -> int:
    if not isinstance(args.max_wait, int) or not 1 <= args.max_wait <= 3600:
        raise ValueError("--max-wait must be between 1 and 3600 seconds")
    if args.output.suffix.lower() not in (".mp4", ".webm"):
        raise ValueError("Output path must end with .mp4 or .webm")
    if args.execute and args.receipt.expanduser().resolve().exists():
        raise ValueError("A previous job receipt exists. Refusing to resubmit; inspect status and recover manually.")
    result = job_plan(args)
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)
    if not args.execute:
        return 0
    if not args.confirm_free_gpu:
        raise ValueError("Execution requires --confirm-free-gpu, with a known free self-hosted ComfyUI GPU.")
    receipt = args.receipt.expanduser().resolve()
    if receipt.exists():
        raise ValueError("A previous job receipt exists. Refusing to resubmit; inspect status and recover manually.")
    if not receipt.parent.is_dir():
        raise ValueError("Receipt parent directory does not exist")
    base = result["server"]
    object_info = api_json(base, "/object_info")
    nodes = workflow_api(args.workflow.expanduser().resolve())
    missing = sorted({n["class_type"] for n in nodes.values()} - set(object_info))
    if missing:
        raise ValueError("Required ComfyUI nodes not installed: " + ", ".join(missing))
    # Check the existing model graph BEFORE staging; staging is the only local side effect pre-submission.
    video_file = stage(verify_media(args.video, VIDEO_SUFFIXES), args.input_dir.expanduser().resolve())
    image_file = stage(verify_media(args.image, IMAGE_SUFFIXES), args.input_dir.expanduser().resolve())
    prompt = bind(nodes, video_id=args.video_node, video_field=args.video_field,
                  image_id=args.image_node, image_field=args.image_field,
                  video_file=video_file, image_file=image_file)
    receipt.write_text(json.dumps({"status": "SUBMISSION_UNCERTAIN",
                                   "server": base, "reason": "POST /prompt initiated, no id yet"},
                                  indent=2) + "\n", encoding="utf-8")
    # Do not repeat a POST after any error. A timeout may still have queued the job.
    created = api_json(base, "/prompt", {"prompt": prompt, "client_id": uuid4().hex})
    prompt_id = created.get("prompt_id")
    if not isinstance(prompt_id, str) or not re.fullmatch(r"[0-9a-fA-F-]{36}", prompt_id):
        raise ValueError("ComfyUI submission returned no valid prompt_id: " + str(created)[:300])
    receipt.write_text(json.dumps({"status": "SUBMITTED", "server": base,
                                   "prompt_id": prompt_id}, indent=2) + "\n", encoding="utf-8")
    stop = time.monotonic() + args.max_wait
    while time.monotonic() < stop:
        history = api_json(base, "/history/" + prompt_id)
        entry = history.get(prompt_id)
        if entry:
            outputs = video_outputs(history, prompt_id)
            if outputs:
                size = download(base, outputs[0], args.output)
                receipt.write_text(json.dumps({"status": "RENDERED_UNREVIEWED",
                                               "prompt_id": prompt_id,
                                               "output": str(args.output),
                                               "bytes": size}, indent=2) + "\n", encoding="utf-8")
                print(json.dumps({"status": "RENDERED_UNREVIEWED", "bytes": size,
                                  "output": str(args.output)}))
                return 0
            if entry.get("status", {}).get("completed"):
                raise ValueError("ComfyUI finished, but no .mp4/.webm appeared in history. Inspect SaveVideo nodes.")
        time.sleep(3)
    receipt.write_text(json.dumps({"status": "PENDING", "prompt_id": prompt_id},
                                  indent=2) + "\n", encoding="utf-8")
    print("ComfyUI job still pending: " + prompt_id + "; no automatic retry.")
    return 3


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workflow", type=Path, required=True, help="ComfyUI exported API-format workflow JSON")
    parser.add_argument("--server", default="http://127.0.0.1:8188")
    parser.add_argument("--input-dir", type=Path, required=True, help="Existing local ComfyUI/input directory")
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--image", type=Path, required=True)
    parser.add_argument("--video-node", required=True, help="API workflow node ID that loads video")
    parser.add_argument("--video-field", default="video")
    parser.add_argument("--image-node", required=True, help="API workflow node ID that loads image")
    parser.add_argument("--image-field", default="image")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, default=Path("comfy-furuya-job.json"))
    parser.add_argument("--max-wait", type=int, default=600)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--confirm-free-gpu", action="store_true")
    args = parser.parse_args(argv)
    try:
        return run(args)
    except (OSError, ValueError, URLError, HTTPError, KeyError, TimeoutError) as exc:
        print(json.dumps({"status": "NO_GO_OR_UNCERTAIN", "reason": str(exc)},
                         ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
