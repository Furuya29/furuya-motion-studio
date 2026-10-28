import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {pathToFileURL} from 'node:url';

const script=readFileSync(new URL('../recast.js',import.meta.url),'utf8');
const html=readFileSync(new URL('../recast.html',import.meta.url),'utf8');
assert.match(html,/ALPHA 0\.7/);
assert.match(html,/recast\.js\?v=0\.7/);
new Function(script);

const nodes=new Map();
function createElement(tag='div'){
 const n={tag,style:{},value:'',textContent:'',disabled:false,hidden:false,files:[],width:384,height:672,readyState:0,currentTime:0,children:[],events:{},
  addEventListener(key,cb){this.events[key]=cb},
  setAttribute(key,value){this[key]=value},
  append(...x){this.children.push(...x)},
  replaceChildren(...x){this.children=x},
  getBoundingClientRect(){return {left:0,top:0,width:384,height:672}},
  setPointerCapture(){},
  pause(){this.paused=true},load(){},play(){this.paused=false;return Promise.resolve()},
  getContext(){return {clearRect(){},drawImage(){},fillRect(){},save(){},restore(){},translate(){},rotate(){},stroke(){},fill(){},beginPath(){},closePath(){},moveTo(){},lineTo(){},arc(){}}}};
 return n;
}
const document={
 getElementById(id){if(!nodes.has(id))nodes.set(id,createElement(id));return nodes.get(id)},
 createElement,
 createTextNode:v=>({textContent:String(v)}),
};
const video=document.getElementById('video');
video.readyState=2;video.duration=29.58;video.currentTime=2;
video.videoWidth=2160;video.videoHeight=3840;video.paused=true;
const app=new Function('document','window','requestAnimationFrame','cancelAnimationFrame',script+
 '\nreturn {slots,active,ui,stage,manifest};')(document,{},()=>0,()=>{});
video.events.loadeddata();
assert.equal(app.slots.length,1);
const stage=document.getElementById('stage');
assert.equal(stage.height,1024);assert.equal(stage.width,576);
app.ui.maskMode.events.click();
for(const [x,y] of [[100,100],[250,100],[250,350],[100,350]])
 stage.events.pointerdown({clientX:x,clientY:y});
assert.equal(app.active().polygon.length,4);
assert.equal(app.ui.saveMask.disabled,false);
app.ui.undoMask.events.click();
assert.equal(app.active().polygon.length,3);
stage.events.pointerdown({clientX:120,clientY:330});
assert.equal(app.active().polygon.length,4);
app.ui.dragMode.events.click();
stage.events.pointerdown({clientX:190,clientY:200,pointerId:1});
stage.events.pointermove({clientX:235,clientY:215});
stage.events.pointerup({});
assert.ok(app.active().x>0);
app.ui.rotation.value='120';app.ui.rotation.events.input();
assert.equal(app.active().rotation,120);
const project=app.manifest();
assert.equal(project.schema,'furuya-recast-project/0.7');
assert.equal(project.characters.length,1);
assert.equal(project.characters[0].polygon.length,4);
assert.equal(project.video.clipDuration,5);
assert.equal(project.pipeline.status,'PREPARATION_ONLY; NO AI VIDEO GENERATED');
app.ui.markClipStart.events.click();
assert.equal(Number(app.ui.clipStart.value),2);
app.ui.clipStart.value='28.9';
assert.ok(app.manifest().video.clipDuration<.71);
console.log('PASS: initial loading, 4-point silhouette, mask control, undo, drag, rotation, manifest, bounded clip and mobile start button');
