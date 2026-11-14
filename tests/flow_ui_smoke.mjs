import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const page=readFileSync(new URL('../flow.html',import.meta.url),'utf8');
const code=readFileSync(new URL('../flow.js',import.meta.url),'utf8');
const catalog=JSON.parse(readFileSync(new URL('../engine-catalog.json',import.meta.url),'utf8'));
for(const id of ['source','ref1','ref2','ref3','ref4','ref5','targets','seconds','balance','resolution','prepare','copy','export','prompt','cost','status']) {
 assert.match(page, new RegExp('id="'+id+'"'));
}
assert.match(page,/flow\.google/);
assert.match(page,/src="\.\/flow\.js"/);
assert.match(code,/credits_checked_live:false/);
assert.match(code,/never_auto_purchase:true/);
assert.match(code,/NOT_RENDERED/);
assert.match(code,/upload_status:"NOT_UPLOADED"/);
assert.doesNotMatch(code,/fetch\(|XMLHttpRequest|\.send\(|VIGGLE_API_KEY/);
for(const name of ['Albedo','Shalltear','Solution','Lupusregina','Narberal']) {
 assert.match(code,new RegExp(name));
}
assert.ok(catalog.scene_replacement.some(e=>e.id==='flow_omni_edit'));
assert.equal(catalog.scene_replacement[0].id,'openjutsu_advanced');
new Function(code);
console.log('PASS: five-character Flow UI is local-only, transparent and no payment.');
