import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const html=readFileSync(new URL('../generate.html',import.meta.url),'utf8');
const js=readFileSync(new URL('../comfy.js',import.meta.url),'utf8');
const workflow=JSON.parse(readFileSync(new URL('../workflows/openjutsu_advanced.api.json',import.meta.url),'utf8'));
const ids=['comfyPanel','comfyWorkflow','comfyCheck','comfyPrepare','comfyAuthorize','comfyStart','comfyRefresh','comfyResume','comfyStatus','comfyResultVideo','comfyDownload'];
for(const id of ids) assert.ok(html.includes('id="'+id+'"'),'Missing ComfyUI control '+id);
assert.ok(html.includes('src="./comfy.js'));
for(const id of [2,3,4]) {
 assert.ok(html.includes('id="comfyImage'+id+'"'));
 assert.ok(html.includes('id="comfyRole'+id+'"'));
}
assert.match(js,/\/api\/comfy\//);
assert.match(js,/AUTHORIZE_LOCAL_GPU/);
assert.match(js,/openjutsu_advanced\.api\.json/);
assert.match(js,/comfyTargetCount/);
assert.match(js,/can_attempt_render/);
assert.match(js,/missing_node_classes/);
assert.match(js,/missing_models/);
assert.match(js,/ram_total_gib/);
assert.match(js,/RENDERED_UNREVIEWED/);
assert.match(js,/PREPARED/);
assert.doesNotMatch(js,/localStorage\.(setItem|removeItem)/);
assert.doesNotMatch(js,/VIGGLE_API_KEY/);
new Function(js);
assert.equal(workflow['14'].class_type,'VHS_LoadVideo');
assert.equal(workflow['20'].class_type,'H3AdvancedSwapPlan');
for(const id of ['2','5','8','11'])assert.equal(workflow[id].class_type,'LoadImage');
console.log('PASS: Furuya ComfyUI UI binds controls and vendored four-reference Openjutsu workflow.');
