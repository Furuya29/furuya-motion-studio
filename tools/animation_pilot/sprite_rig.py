#!/usr/bin/env python3
"""Layered 2D sprite rig v0.1: FK joints, keyframe curves and sprite swaps.

Original sprite PNG files remain unchanged. This is deterministic cutout animation,
not inbetween drawing, pose estimation, lip-sync, or an anime art generator.
Requires Pillow, and FFmpeg only for MP4 output.
"""
import argparse
import json
import math
import shutil
import subprocess
from pathlib import Path
from PIL import Image


def matmul(a,b):
    aa,ab,ac,ad,ae,af=a;ba,bb,bc,bd,be,bf=b
    return (aa*ba+ab*bd, aa*bb+ab*be, aa*bc+ab*bf+ac,
            ad*ba+ae*bd, ad*bb+ae*be, ad*bc+ae*bf+af)


def translate(x,y):return (1,0,x,0,1,y)
def rotate(degrees):
    a=math.radians(degrees);c=math.cos(a);s=math.sin(a)
    return (c,-s,0,s,c,0)
def scale(s):return (s,0,0,0,s,0)
def invert(a):
    x,y,u,z,w,v=a;det=x*w-y*z
    if abs(det)<1e-8:raise ValueError('non-invertible transform')
    return (w/det,-y/det,(y*v-w*u)/det,-z/det,x/det,(z*u-x*v)/det)


def sample(keys,frame,step=False):
    """Keys are sorted {frame,value}; numeric linear interpolation or stepped sprite."""
    if frame<=keys[0]['frame']:return keys[0]['value']
    for i in range(len(keys)-1):
        a,b=keys[i],keys[i+1]
        if frame<b['frame']:
            if step:return a['value']
            t=(frame-a['frame'])/(b['frame']-a['frame'])
            return a['value']+(b['value']-a['value'])*t
    return keys[-1]['value']


def validate(rig):
    errors=[]
    if rig.get('version')!='sprite-rig/0.1':errors.append('unsupported rig version')
    canvas=rig.get('canvas',[])
    if len(canvas)!=2 or any(not isinstance(x,int) or x<=0 or x%2 for x in canvas):errors.append('even canvas dimensions required')
    if not isinstance(rig.get('fps'),int) or rig['fps']<=0:errors.append('positive fps required')
    if not isinstance(rig.get('frames'),int) or rig['frames']<=0:errors.append('positive frame count required')
    parts=rig.get('parts',[])
    if not isinstance(parts,list) or not parts:return errors+['parts required']
    registry={p['id']:p for p in parts}
    if len(registry)!=len(parts):errors.append('duplicate part id')
    for p in parts:
        if p.get('parent') is not None and p['parent'] not in registry:errors.append('unknown parent for '+p['id'])
        if len(p.get('pivot',[]))!=2 or len(p.get('offset',[]))!=2:errors.append('pivot/offset must be 2D for '+p['id'])
        parent=p.get('parent');visited={p['id']}
        while parent is not None and parent in registry:
            if parent in visited:
                errors.append('parent cycle for '+p['id']);break
            visited.add(parent);parent=registry[parent].get('parent')
        path=Path(p.get('sprite',''))
        if path.is_absolute() or '..' in path.parts or not str(path).lower().endswith('.png'):
            errors.append('unsafe or non-PNG sprite path for '+p['id'])
    allowed={'rotation_deg','offset_x','offset_y','scale','sprite'}
    for track in rig.get('tracks',[]):
        label=f"{track.get('part')} / {track.get('property')}"
        if track.get('part') not in registry or track.get('property') not in allowed:errors.append('invalid track '+label)
        keys=track.get('keys',[])
        if not keys or any(not isinstance(k.get('frame'),int) for k in keys):errors.append('keys invalid '+label);continue
        numbers=[k['frame'] for k in keys]
        if numbers!=sorted(set(numbers)) or numbers[0]<0 or numbers[-1]>=rig['frames']:
            errors.append('keyframes out of order or range '+label)
        if track.get('property')=='sprite':
            for k in keys:
                sp=Path(k.get('value',''))
                if sp.is_absolute() or '..' in sp.parts or sp.suffix.lower()!='.png':errors.append('unsafe sprite switch '+label)
        elif any(not isinstance(k.get('value'),(int,float)) or not math.isfinite(k['value']) for k in keys):
            errors.append('non-numeric track '+label)
        elif track.get('property')=='scale' and any(k['value']<=0 for k in keys):
            errors.append('scale must be positive '+label)
    return errors


def render_frame(rig,base_dir,frame,cache=None):
    cache=cache if cache is not None else {}
    width,height=rig['canvas']
    frame=max(0,min(frame,rig['frames']-1))
    parts={p['id']:p for p in rig['parts']}
    tracks={(t['part'],t['property']):t['keys'] for t in rig.get('tracks',[])}
    world={}
    def world_matrix(part_id):
        if part_id in world:return world[part_id]
        p=parts[part_id]
        parent=world_matrix(p['parent']) if p.get('parent') else (1,0,0,0,1,0)
        def value(property_,default):
            k=tracks.get((part_id,property_))
            return sample(k,frame) if k else default
        offx,offy=p['offset']; angle=value('rotation_deg',0); factor=value('scale',1)
        m=matmul(parent,matmul(translate(offx+value('offset_x',0),offy+value('offset_y',0)),matmul(rotate(angle),scale(factor))))
        world[part_id]=m
        return m
    image=Image.new('RGBA',(width,height),(0,0,0,0))
    for p in sorted(rig['parts'],key=lambda item:(item.get('layer',0),item['id'])):
        key=tracks.get((p['id'],'sprite'))
        sprite=sample(key,frame,step=True) if key else p['sprite']
        if sprite not in cache:
            path=(base_dir/sprite).resolve()
            if not path.is_relative_to(base_dir.resolve()):raise ValueError('sprite outside rig directory')
            cache[sprite]=Image.open(path).convert('RGBA')
        local=matmul(world_matrix(p['id']),translate(-p['pivot'][0],-p['pivot'][1]))
        transformed=cache[sprite].transform((width,height),Image.Transform.AFFINE,invert(local),resample=Image.Resampling.BICUBIC)
        image.alpha_composite(transformed)
    return image


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rig',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args(argv)
    rig=json.loads(args.rig.read_text(encoding='utf-8'))
    errors=validate(rig)
    if errors:parser.error('; '.join(errors))
    if not shutil.which('ffmpeg'):parser.error('ffmpeg not installed')
    args.out.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-loglevel','error','-hide_banner','-y','-f','rawvideo','-pix_fmt','rgba',
         '-s',f'{rig["canvas"][0]}x{rig["canvas"][1]}','-r',str(rig['fps']),'-i','-',
         '-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p','-movflags','+faststart',str(args.out)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    cache={}
    try:
        for frame in range(rig['frames']):
            proc.stdin.write(render_frame(rig,args.rig.resolve().parent,frame,cache).tobytes())
        proc.stdin.close();err=proc.stderr.read().decode('utf-8','replace')
        if proc.wait()!=0:raise RuntimeError('ffmpeg: '+err[-1200:])
    except BaseException:
        if proc.poll() is None:proc.kill()
        proc.wait();args.out.unlink(missing_ok=True);raise
    print(f'SPRITE_RIG_RENDERED {args.out} ({rig["frames"]} frames)')

if __name__=='__main__':main()
