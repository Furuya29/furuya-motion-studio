'use strict';
// Offline human-guided role assignments only. There is no AI tracking here.
const $=id=>document.getElementById(id);
const video=$('video'),canvas=$('overlay'),cx=canvas.getContext('2d');
const colors=['#68f1c7','#ffb468','#c6a9ff','#66bcff'];
let url='',filename='',roles=[],activeId=null,nextId=0,drag=null,ready=false;
const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
const active=()=>roles.find(r=>r.id===activeId)||null;
function setStatus(text,bad=false){$('status').textContent=text;$('status').style.color=bad?'#ffd1d9':''}
function updateButtons(){
 $('addRole').disabled=!ready||roles.length>=4;
 $('clearCurrent').disabled=!ready||!active()||!active().anchors.length;
 $('download').disabled=!ready||!roles.length;
 $('clear').disabled=!ready;
 $('counter').textContent=roles.length+' / 4 personagens · '+roles.reduce((n,r)=>n+r.anchors.length,0)+' marcações em quadros.';
}
function usableTime(){return Math.round((video.currentTime||0)*1000)/1000}
function normalizedPoint(event){
 const rect=canvas.getBoundingClientRect();
 return {x:clamp((event.clientX-rect.left)/rect.width,0,1),y:clamp((event.clientY-rect.top)/rect.height,0,1)};
}
function paint(){
 cx.clearRect(0,0,canvas.width,canvas.height);
 if(!ready)return;
 for(const [index,role] of roles.entries()){
  let best=null;
  for(const anchor of role.anchors){
   if(!best||Math.abs(anchor.time_seconds-usableTime())<Math.abs(best.time_seconds-usableTime()))best=anchor;
  }
  if(!best||Math.abs(best.time_seconds-usableTime())>0.7)continue;
  const [x,y,w,h]=best.box_xywh;
  cx.strokeStyle=colors[index];cx.lineWidth=Math.max(3,canvas.width/210);cx.strokeRect(x*canvas.width,y*canvas.height,w*canvas.width,h*canvas.height);
  cx.fillStyle=colors[index];cx.font='bold '+Math.round(canvas.width/29)+'px sans-serif';
  cx.fillText(role.name.slice(0,28),x*canvas.width+4,Math.max(24,y*canvas.height-7));
 }
 if(drag){
  const a=drag.a,b=drag.b;
  const x=Math.min(a.x,b.x),y=Math.min(a.y,b.y),w=Math.abs(a.x-b.x),h=Math.abs(a.y-b.y);
  cx.strokeStyle='#ffffff';cx.lineWidth=4;cx.setLineDash([10,5]);
  cx.strokeRect(x*canvas.width,y*canvas.height,w*canvas.width,h*canvas.height);cx.setLineDash([]);
 }
}
function repaintWhenPlaying(){paint();if(!video.paused&&!video.ended)requestAnimationFrame(repaintWhenPlaying)}
function make(tag,text){const e=document.createElement(tag);if(text!==undefined)e.textContent=text;return e}
function renderRoles(){
 $('roles').replaceChildren();
 for(const [index,r] of roles.entries()){
  const box=make('div');box.className='role'+(r.id===activeId?' selected':'');
  const top=make('div');top.className='roleHead';
  const select=make('button',r.id===activeId?'✓ Marcando':'Marcar esta pessoa');
  select.addEventListener('click',()=>{activeId=r.id;renderRoles();paint()});
  const del=make('button','Remover');
  del.addEventListener('click',()=>{roles=roles.filter(x=>x.id!==r.id);activeId=roles[0]?.id||null;renderRoles();paint()});
  top.append(select,del);box.append(top);
  const label=make('label','Nome da personagem');
  const input=make('input');input.type='text';input.value=r.name;input.maxLength=50;
  input.addEventListener('change',()=>{r.name=input.value.trim().slice(0,50)||('Personagem '+r.id);renderRoles();paint()});
  box.append(label,input);
  box.append(make('label','Imagem original (não será enviada nem copiada ao JSON)'));
  const ref=make('input');ref.type='file';ref.accept='image/png,image/jpeg,image/webp,.png,.jpg,.jpeg,.webp';
  ref.addEventListener('change',()=>{const f=ref.files?.[0];if(f){r.reference_filename=f.name;renderRoles();paint()}});
  box.append(ref);
  box.append(make('p','Referência: '+(r.reference_filename||'não selecionada')+' · Marcações: '+r.anchors.length));
  $('roles').append(box);
 }
 updateButtons();
}
function reset(){roles=[];activeId=null;nextId=0;drag=null;renderRoles();paint()}
function addRole(){
 if(!ready||roles.length>=4)return;
 const r={id:'target_'+(++nextId),name:'Personagem '+nextId,reference_filename:'',anchors:[]};
 roles.push(r);activeId=r.id;renderRoles();paint();
 setStatus('Alvo criado. Escolha a imagem e arraste uma caixa em torno da pessoa com o vídeo pausado.');
}
$('source').addEventListener('change',()=>{
 const f=$('source').files?.[0];if(!f)return;
 video.pause();if(url)URL.revokeObjectURL(url);
 url=URL.createObjectURL(f);filename=f.name;ready=false;reset();video.src=url;video.load();
 setStatus('Carregando vídeo local: '+f.name);
});
video.addEventListener('loadedmetadata',()=>{
 ready=video.videoWidth>0&&video.videoHeight>0&&Number.isFinite(video.duration)&&video.duration>0;
 if(!ready){setStatus('Não foi possível ler metadados do vídeo.',true);return}
 canvas.width=video.videoWidth;canvas.height=video.videoHeight;
 addRole();updateButtons();paint();
 setStatus('Vídeo carregado. Pause em um quadro, selecione uma referência e marque quem será substituído. O vídeo continua intacto.');
});
video.addEventListener('play',repaintWhenPlaying);
video.addEventListener('seeked',paint);
video.addEventListener('pause',paint);
canvas.addEventListener('pointerdown',e=>{
 if(!ready||!active()){setStatus('Adicione um personagem para marcar.',true);return}
 if(!video.paused){video.pause();setStatus('Vídeo pausado para marcar um quadro; selecione o corpo do alvo.')}
 const pt=normalizedPoint(e);drag={a:pt,b:pt,pointerId:e.pointerId};canvas.setPointerCapture(e.pointerId);paint();
});
canvas.addEventListener('pointermove',e=>{
 if(!drag||e.pointerId!==drag.pointerId)return;
 drag.b=normalizedPoint(e);paint();
});
canvas.addEventListener('pointerup',e=>{
 if(!drag||e.pointerId!==drag.pointerId)return;
 drag.b=normalizedPoint(e);
 const a=drag.a,b=drag.b;
 drag=null;
 const x=Math.min(a.x,b.x),y=Math.min(a.y,b.y),w=Math.abs(b.x-a.x),h=Math.abs(b.y-a.y);
 if(w<0.02||h<0.02){setStatus('Caixa pequena demais. Arraste ao redor de toda a pessoa.',true);paint();return}
 const r=active(),t=usableTime();
 const anchor={time_seconds:t,box_xywh:[x,y,w,h].map(v=>Math.round(v*10000)/10000)};
 const found=r.anchors.findIndex(item=>Math.abs(item.time_seconds-t)<0.06);
 if(found>=0)r.anchors[found]=anchor;else r.anchors.push(anchor);
 r.anchors.sort((a,b)=>a.time_seconds-b.time_seconds);
 renderRoles();paint();setStatus('Posição marcada para '+r.name+' aos '+t.toFixed(2)+' segundos. Isto é uma âncora, não rastreamento automático.');
});
$('addRole').addEventListener('click',addRole);
$('clearCurrent').addEventListener('click',()=>{const r=active();if(!r)return;r.anchors=[];renderRoles();paint();setStatus('Marcações removidas do alvo '+r.name+'.')});
$('clear').addEventListener('click',()=>{reset();if(ready)addRole();setStatus('Elenco reiniciado. O arquivo original não foi alterado.')});
function plan(){
 if(!ready||!roles.length)throw Error('Carregue o vídeo e defina pelo menos um alvo.');
 for(const r of roles){
  if(!r.reference_filename)throw Error('Escolha uma imagem para '+r.name+'.');
  if(!r.anchors.length)throw Error('Marque a pessoa correspondente a '+r.name+' em um quadro.');
 }
 return {
  schema:'furuya-multicast-plan/1',
  task:'multi_scene_replacement',
  source_immutable:true,
  tracking_state:'NOT_RUN',
  segmentation_state:'NOT_RUN',
  render_state:'NOT_STARTED',
  video:{filename,duration_seconds:Math.round(video.duration*1000)/1000,width:video.videoWidth,height:video.videoHeight},
  targets:roles.map(r=>({id:r.id,name:r.name,reference_filename:r.reference_filename,anchors:r.anchors.map(x=>({...x}))})),
  preservation:{original_camera:true,original_bystanders:true,original_audio:true,original_environment:true},
  caveat:'These are only annotated boxes at selected frames. No identity tracking, occlusion masks or generative render has occurred.'
 };
}
$('download').addEventListener('click',()=>{
 try{
  const data=JSON.stringify(plan(),null,2);
  const blob=new Blob([data],{type:'application/json'});
  const uri=URL.createObjectURL(blob);
  const link=make('a');link.href=uri;link.download='furuya-multicast-plan.json';
  document.body.append(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(uri),2000);
  setStatus('Plano salvo. Sem upload de vídeo/imagens e sem processamento generativo. Próxima etapa: segmentação multi-ID.');
 }catch(e){setStatus(e.message,true)}
});
renderRoles();