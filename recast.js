'use strict';
const $=id=>document.getElementById(id),video=$('video'),stage=$('stage'),cx=stage.getContext('2d');
const ui={videoFile:$('videoFile'),clipStart:$('clipStart'),clipLength:$('clipLength'),markClipStart:$('markClipStart'),newKeyframe:$('newKeyframe'),saveKeyframe:$('saveKeyframe'),keyframeList:$('keyframeList'),projectFile:$('projectFile'),projectInfo:$('projectInfo'),checkPackage:$('checkPackage'),packageStatus:$('packageStatus'),videoInfo:$('videoInfo'),status:$('status'),timeline:$('timeline'),now:$('now'),end:$('end'),play:$('play'),pause:$('pause'),maskMode:$('maskMode'),dragMode:$('dragMode'),undoMask:$('undoMask'),clearMask:$('clearMask'),clearOverlay:$('clearOverlay'),slots:$('slots'),addSlot:$('addSlot'),controls:$('controls'),scale:$('scale'),rotation:$('rotation'),offsetX:$('offsetX'),offsetY:$('offsetY'),scaleValue:$('scaleValue'),rotationValue:$('rotationValue'),xValue:$('xValue'),yValue:$('yValue'),repaintFile:$('repaintFile'),repaintInfo:$('repaintInfo'),repaintView:$('repaintView'),sourceView:$('sourceView'),saveSource:$('saveSource'),saveDraft:$('saveDraft'),saveMask:$('saveMask'),saveProject:$('saveProject'),saveRepaint:$('saveRepaint'),saveSegment:$('saveSegment'),exportInfo:$('exportInfo')};
let duration=0,videoUrl='',slots=[],activeId=null,nextId=0,mode='drag',showOverlay=true,showRepaint=false,repaint=null,repaintName='',raf=0,dragging=null,exporting=false,record=null,clipStream=null,clipChunks=[],clipCanceled=false,clipType='',clipCanvas=null,clipContext=null,keyframes=[],workingTime=0,repaintTime=null;
const clamp=(v,min,max)=>Math.max(min,Math.min(max,v));
const clock=t=>{t=Number.isFinite(t)?Math.max(0,t):0;return String(Math.floor(t/60)).padStart(2,'0')+':'+(t%60).toFixed(2).padStart(5,'0')};
const ready=()=>video.readyState>=2&&Number.isFinite(video.duration)&&video.duration>0;
const active=()=>slots.find(s=>s.id===activeId)||null;
function status(t,bad=false){ui.status.textContent=t;ui.status.className='message'+(bad?' error':'')}
function make(tag,props={},label){const n=document.createElement(tag);for(const [k,v]of Object.entries(props)){if(['type','accept','value','title','min','max','step'].includes(k))n.setAttribute(k,v);else n[k]=v}if(label!==undefined)n.textContent=label;return n}
function toPixel(point){return [point.x*stage.width,point.y*stage.height]}
function widthHeight(){
 const targetLong=1024,scale=Math.min(1,targetLong/Math.max(video.videoWidth,video.videoHeight));
 // Latent video models commonly require dimensions divisible by 32.
 stage.width=Math.max(32,Math.round(video.videoWidth*scale/32)*32);
 stage.height=Math.max(32,Math.round(video.videoHeight*scale/32)*32);
}
function canSave(){return ready()&&!exporting}
function update(){
 const ok=canSave(),slot=active();
 ui.timeline.disabled=!ok;ui.play.disabled=!ok;ui.pause.disabled=!ok;
 ui.maskMode.disabled=!ok||!slot;ui.dragMode.disabled=!ok||!slot;
 ui.undoMask.disabled=!ok||!slot||!slot.polygon.length;
 ui.clearMask.disabled=!ok||!slot||!slot.polygon.length;
 ui.clearOverlay.disabled=!ok||!slot;ui.addSlot.disabled=!ok;ui.markClipStart.disabled=!ok;
 ui.saveSource.disabled=!ok;ui.saveDraft.disabled=!ok;ui.saveMask.disabled=!ok||!slot||slot.polygon.length<3;
 ui.saveProject.disabled=!ok;ui.saveRepaint.disabled=!ok||!repaint;
 ui.saveSegment.disabled=!ok&&!exporting;
 ui.repaintView.disabled=!ok||!repaint;ui.sourceView.disabled=!ok;
 ui.controls.hidden=!slot;ui.newKeyframe.disabled=!ok||!slot;ui.saveKeyframe.disabled=!ok||!slot;ui.checkPackage.disabled=!ok;
 ui.now.textContent=clock(video.currentTime);ui.end.textContent=clock(duration);
}
function drawImageCanvas(img,c,fit=true){
 if(!fit){c.drawImage(img,0,0,stage.width,stage.height);return}
 c.drawImage(img,0,0,stage.width,stage.height);
}
function paintSlot(c,slot){
 if(!slot.image)return;
 c.save();
 c.globalAlpha=.9;
 c.translate((.5+slot.x)*stage.width,(.5+slot.y)*stage.height);
 c.rotate(slot.rotation*Math.PI/180);
 const height=stage.height*.58*slot.scale;
 const width=height*slot.image.width/slot.image.height;
 c.drawImage(slot.image,-width/2,-height/2,width,height);
 c.restore();
}
function drawPolygon(c,slot){
 const arr=slot.polygon;if(!arr.length)return;
 c.save();c.strokeStyle=slot.id===activeId?'#82ffe2':'#b9a2fa';c.lineWidth=Math.max(2,stage.width/300);
 c.fillStyle='rgba(70,250,190,.14)';c.beginPath();arr.forEach((p,i)=>{const [x,y]=toPixel(p);if(i===0)c.moveTo(x,y);else c.lineTo(x,y)});
 if(arr.length>=3){c.closePath();c.fill()}c.stroke();
 for(const p of arr){const [x,y]=toPixel(p);c.beginPath();c.arc(x,y,Math.max(4,stage.width/160),0,Math.PI*2);c.fillStyle='#d3fff5';c.fill()}
 c.restore();
}
function render(t=video.currentTime,options={}){
 const c=options.ctx||cx,w=stage.width,h=stage.height;
 c.clearRect(0,0,w,h);
 if(ready()){try{c.drawImage(video,0,0,w,h)}catch{}}
 else{c.fillStyle='#0a1020';c.fillRect(0,0,w,h)}
 if(options.raw)return;
 if(showRepaint&&repaint&&!options.forceDraft&&repaintTime!==null&&Math.abs(t-repaintTime)<=.25){c.drawImage(repaint,0,0,w,h);return}
 // Do not pretend to track people across video time: a manual edit applies ONLY to its own frame.
 const onEditedFrame=Math.abs(t-workingTime)<=.26;
 if((showOverlay&&onEditedFrame)||options.forceDraft)for(const s of slots)paintSlot(c,s);
 if(onEditedFrame&&!options.noGuides&&!options.forceDraft)for(const s of slots)drawPolygon(c,s);
}
function draw(){render();if(!exporting){ui.timeline.value=duration?Math.round(clamp(video.currentTime/duration,0,1)*1000):0;ui.now.textContent=clock(video.currentTime)}}
function stopLoop(){if(raf)cancelAnimationFrame(raf);raf=0}
function animate(){draw();if(!video.paused&&!exporting)raf=requestAnimationFrame(animate)}
ui.markClipStart.addEventListener('click',()=>{if(!canSave())return;ui.clipStart.value=String(Math.round(video.currentTime*100)/100);status('Início do trecho definido em '+clock(video.currentTime)+'. Escolha um quadro pertencente a esse trecho para retocá-lo.');});
ui.videoFile.addEventListener('change',()=>{
 const file=ui.videoFile.files?.[0];if(!file)return;
 video.pause();stopLoop();if(videoUrl)URL.revokeObjectURL(videoUrl);
 // A new video invalidates image alignment and the timeline of saved reference frames.
 keyframes=[];workingTime=0;repaintTime=null;showRepaint=false;
 if(repaint?.close)repaint.close();repaint=null;repaintName='';
 for(const slot of slots)if(slot.image?.close)slot.image.close();
 slots=[];activeId=null;nextId=0;ui.slots.replaceChildren();renderKeyframeList();
 videoUrl=URL.createObjectURL(file);video.src=videoUrl;video.load();status('Carregando vídeo local: '+file.name);update();
});
video.addEventListener('loadeddata',()=>{
 duration=video.duration;widthHeight();workingTime=video.currentTime||0;
 ui.videoInfo.textContent=(ui.videoFile.files?.[0]?.name||'')+' · '+video.videoWidth+'×'+video.videoHeight+' · '+clock(duration)+' · quadros exportados a '+stage.width+'×'+stage.height+'.';
 ui.clipStart.value='0';
 if(!slots.length)addSlot();
 status('Vídeo pronto. Marque um quadro-chave, selecione uma silhueta e importe a referência do personagem.');
 draw();update();
});
video.addEventListener('error',()=>status('Não foi possível decodificar esse vídeo. Tente MP4 H.264.',true));
ui.timeline.addEventListener('input',()=>{if(!canSave())return;video.pause();stopLoop();video.currentTime=duration*Number(ui.timeline.value)/1000});
video.addEventListener('seeked',()=>{if(!exporting)draw()});
video.addEventListener('timeupdate',()=>{if(!exporting)ui.now.textContent=clock(video.currentTime)});
video.addEventListener('ended',()=>{stopLoop();if(!exporting)draw()});
ui.play.addEventListener('click',()=>{if(!canSave())return;video.play().then(()=>{stopLoop();animate()}).catch(e=>status(e.message,true))});
ui.pause.addEventListener('click',()=>{video.pause();stopLoop();draw()});
function addSlot(){
 if(!ready()||exporting)return;
 const slot={id:++nextId,name:'Personagem '+nextId,referenceFile:'',image:null,x:0,y:0,rotation:0,scale:1,polygon:[],anchorTime:video.currentTime};
 slots.push(slot);activeId=slot.id;
 buildSlots();fillControls();update();draw();
}
function buildSlots(){
 ui.slots.replaceChildren();
 for(const s of slots){
  const section=make('div',{className:'slot'+(s.id===activeId?' selected':'')});
  const head=make('div',{className:'slot-head'});head.append(make('strong',{},s.name),make('span',{className:'status-tag'},s.polygon.length>=3?'Contorno registrado':'Sem máscara'));section.append(head);
  const upper=make('div',{className:'row'});
  const pick=make('button',{type:'button'},s.id===activeId?'✓ Editando':'Editar este personagem');
  pick.addEventListener('click',()=>{activeId=s.id;buildSlots();fillControls();update();draw()});
  const remove=make('button',{type:'button',className:'warning'},'Remover');
  remove.addEventListener('click',()=>{if(exporting)return;if(s.image?.close)s.image.close();slots=slots.filter(a=>a.id!==s.id);activeId=slots[0]?.id||null;buildSlots();fillControls();update();draw()});
  upper.append(pick,remove);section.append(upper);
  const title=make('input',{type:'text',value:s.name});title.setAttribute('aria-label','Nome do personagem');
  title.addEventListener('change',()=>{s.name=title.value.trim().slice(0,75)||'Personagem '+s.id;buildSlots()});
  const label=make('label',{},'Nome da personagem');section.append(label,title);
  const upload=make('input',{type:'file',accept:'image/png,image/webp,image/jpeg'});upload.setAttribute('aria-label','Referência visual de '+s.name);
  upload.addEventListener('change',async()=>{
   const f=upload.files?.[0];if(!f)return;
   try{const img=await createImageBitmap(f);if(s.image?.close)s.image.close();s.image=img;s.referenceFile=f.name;activeId=s.id;buildSlots();fillControls();update();draw();status('Referência carregada para '+s.name+'. Posicione no quadro, depois exporte o rascunho.')}
   catch(e){status('Falha na imagem de referência: '+e.message,true)}
  });
  section.append(make('label',{},'Imagem de referência do personagem inteiro'),upload);
  section.append(make('p',{className:'sub'},'Imagem: '+(s.referenceFile||'nenhuma')+' · Máscara: '+s.polygon.length+' pontos'));
  ui.slots.append(section);
 }
}
ui.addSlot.addEventListener('click',addSlot);
function fillControls(){
 const s=active();ui.controls.hidden=!s;if(!s)return;
 ui.scale.value=String(Math.round(s.scale*100));
 ui.rotation.value=String(s.rotation);
 ui.offsetX.value=String(Math.round(s.x*100));ui.offsetY.value=String(Math.round(s.y*100));
 ui.scaleValue.textContent=Math.round(s.scale*100)+'%';
 ui.rotationValue.textContent=s.rotation+'°';
 ui.xValue.textContent=Math.round(s.x*100)+'%';
 ui.yValue.textContent=Math.round(s.y*100)+'%';
}
for(const [id,field,format] of [['scale','scale',v=>Math.round(v*100)+'%'],['rotation','rotation',v=>v+'°'],['offsetX','x',v=>Math.round(v*100)+'%'],['offsetY','y',v=>Math.round(v*100)+'%']]){
 ui[id].addEventListener('input',()=>{
  const s=active();if(!s)return;
  s[field]=id==='scale'?Number(ui[id].value)/100:id==='offsetX'||id==='offsetY'?Number(ui[id].value)/100:Number(ui[id].value);
  const value=id==='offsetX'?'xValue':id==='offsetY'?'yValue':id==='scale'?'scaleValue':'rotationValue';
  ui[value].textContent=format(s[field]);s.anchorTime=video.currentTime;draw();
 });
}
function setMode(next){
 mode=next;
 ui.maskMode.textContent=mode==='mask'?'✓ Marcar silhueta':'✎ Marcar silhueta';
 ui.dragMode.textContent=mode==='drag'?'✓ Mover referência':'✥ Mover referência';
 stage.style.cursor=mode==='mask'?'crosshair':'grab';
}
ui.maskMode.addEventListener('click',()=>setMode('mask'));
ui.dragMode.addEventListener('click',()=>setMode('drag'));
function pointer(ev){
 const rect=stage.getBoundingClientRect();
 return {x:clamp((ev.clientX-rect.left)/rect.width,0,1),y:clamp((ev.clientY-rect.top)/rect.height,0,1)};
}
stage.addEventListener('pointerdown',ev=>{
 const s=active();if(!canSave()||!s||showRepaint)return;
 const p=pointer(ev);
 if(mode==='mask'){if(s.polygon.length>=90){status('Limite de 90 pontos por máscara. Exporte ou limpe a máscara.',true);return}
  s.polygon.push(p);s.anchorTime=video.currentTime;buildSlots();update();draw();return}
 dragging={id:s.id,x:p.x,y:p.y,startX:s.x,startY:s.y};
 if(stage.setPointerCapture)stage.setPointerCapture(ev.pointerId);
});
stage.addEventListener('pointermove',ev=>{
 if(!dragging||mode!=='drag'||!canSave())return;
 const s=active();if(!s||s.id!==dragging.id)return;
 const p=pointer(ev);
 s.x=clamp(dragging.startX+p.x-dragging.x,-1,1);
 s.y=clamp(dragging.startY+p.y-dragging.y,-1,1);
 s.anchorTime=video.currentTime;fillControls();draw();
});
function endDrag(){dragging=null}
stage.addEventListener('pointerup',endDrag);stage.addEventListener('pointercancel',endDrag);
ui.undoMask.addEventListener('click',()=>{active()?.polygon.pop();buildSlots();update();draw()});
ui.clearMask.addEventListener('click',()=>{const s=active();if(s)s.polygon=[];buildSlots();update();draw()});
ui.clearOverlay.addEventListener('click',()=>{showOverlay=!showOverlay;ui.clearOverlay.textContent=showOverlay?'◎ Ocultar sobreposição':'◎ Mostrar sobreposição';draw()});
ui.repaintFile.addEventListener('change',async()=>{
 const file=ui.repaintFile.files?.[0];if(!file)return;
 try{
  const img=await createImageBitmap(file);
  const diff=Math.abs(img.width/img.height-stage.width/stage.height);
  if(repaint?.close)repaint.close();repaint=img;repaintName=file.name;repaintTime=video.currentTime;workingTime=video.currentTime;
  ui.repaintInfo.textContent=file.name+' · '+img.width+'×'+img.height+(diff>.025?' · ATENÇÃO: proporções divergentes; pode distorcer.':' · enquadramento compatível. O conteúdo deve corresponder a um quadro original.');
  showRepaint=true;update();draw();status('Quadro retocado carregado. Confira se ele representa a pessoa inteira e se preserva o cenário.');
 }catch(e){status('Não foi possível abrir o quadro retocado: '+e.message,true)}
});
ui.repaintView.addEventListener('click',()=>{showRepaint=true;draw()});
ui.sourceView.addEventListener('click',()=>{showRepaint=false;draw()});
function slotSnapshot(s){
 return {slot:s.id,name:s.name,referenceFilename:s.referenceFile,x:s.x,y:s.y,rotationDegrees:s.rotation,scale:s.scale,markedAtTime:workingTime,
   polygon:s.polygon.map(p=>({x:p.x,y:p.y}))};
}
function snapshotFrame(){
 const time=Number(video.currentTime.toFixed(3));
 return {time,characters:slots.map(slotSnapshot),
   fullRepaintFilename:repaint&&repaintTime!==null&&Math.abs(time-repaintTime)<=.26?repaintName:null};
}
function validPoint(p){return !!p&&Number.isFinite(p.x)&&Number.isFinite(p.y)&&p.x>=0&&p.x<=1&&p.y>=0&&p.y<=1}
function safeSnapshot(k){
 if(!k||!Number.isFinite(k.time)||k.time<0||k.time>duration+.2||!Array.isArray(k.characters)||k.characters.length>30)throw Error('Quadro-chave fora do intervalo ou inválido');
 return {time:Number(k.time.toFixed(3)),
  fullRepaintFilename:typeof k.fullRepaintFilename==='string'?k.fullRepaintFilename.slice(0,200):null,
  characters:k.characters.map(a=>{
   if(!Number.isInteger(a.slot)||a.slot<1||a.slot>9999||!Array.isArray(a.polygon)||a.polygon.length>90||!a.polygon.every(validPoint))throw Error('Máscara ou personagem inválido');
   for(const v of [a.x,a.y,a.scale,a.rotationDegrees])if(!Number.isFinite(v))throw Error('Transformações inválidas');
   return {slot:a.slot,name:String(a.name||'Personagem').slice(0,75),referenceFilename:String(a.referenceFilename||'').slice(0,200),
     x:clamp(a.x,-1,1),y:clamp(a.y,-1,1),scale:clamp(a.scale,.2,3),rotationDegrees:clamp(a.rotationDegrees,-180,180),
     markedAtTime:Number.isFinite(a.markedAtTime)?a.markedAtTime:k.time,polygon:a.polygon.map(p=>({x:p.x,y:p.y}))};
  })};
}
function renderKeyframeList(){
 ui.keyframeList.replaceChildren();
 if(!keyframes.length){ui.keyframeList.append(make('p',{className:'sub'},'Nenhum quadro-chave salvo. Eles serão preservados no JSON do projeto.'));return}
 for(let i=0;i<keyframes.length;i++){
  const k=keyframes[i],wrapper=make('div',{className:'slot'});
  const row=make('div',{className:'row'}),select=make('button',{type:'button'},'Ir para '+clock(k.time));
  const deleteButton=make('button',{type:'button',className:'warning'},'Excluir');
  select.addEventListener('click',()=>restoreKeyframe(i));
  deleteButton.addEventListener('click',()=>{
   if(exporting)return;keyframes.splice(i,1);renderKeyframeList();update();status('Quadro-chave excluído.');});
  row.append(select,deleteButton);wrapper.append(row);
  wrapper.append(make('div',{className:'sub'},
   k.characters.length+' personagem(ns) · '+k.characters.filter(x=>x.polygon.length>=3).length+' máscara(s)'
   +(k.fullRepaintFilename?' · quadro retocado referenciado':' · sem quadro retocado')));
  ui.keyframeList.append(wrapper);
 }
}
function saveCurrentKeyframe(){
 if(!canSave())return;
 if(Math.abs(video.currentTime-workingTime)>.26){status('A edição pertence a outro instante. Toque em Preparar outro quadro para marcar o momento atual.',true);return}
 try{
  const snap=safeSnapshot(snapshotFrame());
  const at=keyframes.findIndex(k=>Math.abs(k.time-snap.time)<=.07);
  if(at>=0)keyframes[at]=snap;else keyframes.push(snap);
  keyframes.sort((a,b)=>a.time-b.time);
  renderKeyframeList();update();
  status('Quadro-chave salvo em '+clock(snap.time)+'. O movimento ENTRE quadros ainda não foi gerado.');
 }catch(e){status('Falha ao salvar quadro-chave: '+e.message,true)}
}
function prepareNewKeyframe(){
 if(!canSave()||!active())return;
 workingTime=video.currentTime;showRepaint=false;
 for(const s of slots){s.polygon=[];s.anchorTime=workingTime}
 ui.repaintInfo.textContent='Novo instante de edição: '+clock(workingTime)+'. Importe outro quadro retocado quando necessário.';
 buildSlots();update();draw();status('Novo quadro em '+clock(workingTime)+'. Posicione personagens e marque as silhuetas antes de salvar.');
}
function restoreKeyframe(index){
 if(!canSave()||!keyframes[index])return;
 const k=keyframes[index],previous=new Map(slots.map(s=>[s.id,s]));
 slots=k.characters.map(a=>({
  id:a.slot,name:a.name,referenceFile:a.referenceFilename,
  image:previous.get(a.slot)?.image||null,x:a.x,y:a.y,rotation:a.rotationDegrees,
  scale:a.scale,polygon:a.polygon.map(p=>({...p})),anchorTime:k.time
 }));
 nextId=Math.max(nextId,...slots.map(s=>s.id),0);
 activeId=slots[0]?.id||null;workingTime=k.time;
 showRepaint=false;
 const sameRepaint=!!repaint&&repaintName===k.fullRepaintFilename;
 repaintTime=sameRepaint?k.time:null;
 ui.repaintInfo.textContent=k.fullRepaintFilename?
   'Quadro retocado registrado: '+k.fullRepaintFilename+(sameRepaint?' · imagem disponível':' · reimporte esta imagem para visualizá-la'):
   'Nenhum quadro retocado anexado a este instante.';
 video.pause();stopLoop();video.currentTime=k.time;
 buildSlots();fillControls();update();draw();
 status('Quadro-chave '+clock(k.time)+' recuperado. Referências não incluídas no JSON precisam ser importadas novamente.');
}
ui.newKeyframe.addEventListener('click',prepareNewKeyframe);
ui.saveKeyframe.addEventListener('click',saveCurrentKeyframe);
function packageCheck(){
 const m=manifest(),issues=[],notes=[];
 if(!ready()){issues.push('Vídeo original não carregado');return {ready:false,issues,notes}}
 if(!m.video.clipDuration||m.video.clipDuration<1||m.video.clipDuration>5.2)issues.push('Trecho deve durar entre 1 e 5,2 segundos para teste do Viggle-Animate');
 if(m.video.width%1!==0||m.video.height%1!==0)issues.push('Metadados de vídeo inválidos');
 if(stage.width%32||stage.height%32)issues.push('A saída do quadro não está alinhada em múltiplos de 32 pixels');
 const start=m.video.clipStart,end=start+m.video.clipDuration;
 const candidates=[...keyframes,snapshotFrame()].filter(k=>k.time>=start-.001&&k.time<=end+.001);
 if(!candidates.length)issues.push('Nenhum quadro-chave pertencente ao trecho');
 if(!candidates.some(k=>k.characters.some(c=>c.polygon.length>=3)))notes.push('Máscara do personagem ainda não delimitada; útil para edição manual, mas Viggle-Animate não a exige');
 const editedHere=!!repaint&&repaintTime!==null&&candidates.some(k=>!!k.fullRepaintFilename&&k.fullRepaintFilename===repaintName&&Math.abs(k.time-repaintTime)<=.26);
 if(!editedHere)issues.push('Falta importar neste aparelho o quadro FINAL retocado correspondente a um quadro-chave do trecho');
 if(repaint&&repaintTime!==null&&Math.abs(repaint.width/repaint.height-stage.width/stage.height)>0.025)notes.push('Proporção do quadro retocado pode não coincidir');
 if(m.characters.length>1)notes.push('Várias pessoas podem exigir testes em tomadas separadas: o modelo não garante multi-personagem');
 notes.push('Ainda é necessário importar o vídeo recortado e o quadro editado em um motor generativo compatível e disponível');
 return {ready:issues.length===0,issues,notes,clip:{start,duration:m.video.clipDuration},keyframes:candidates.length};
}
ui.checkPackage.addEventListener('click',()=>{
 const check=packageCheck();
 ui.packageStatus.textContent=(check.ready?'Pré-preparação válida para um TESTE, não para geração local.':'Pacote incompleto:')
   +' '+(check.issues.length?check.issues.join(' · '):'Trecho e referência temporal identificados.')
   +' '+check.notes.join(' · ');
 status(check.ready?'Pré-requisitos de preparação identificados. O render por IA ainda não está conectado.':
  'Confira os itens do painel de validação. Nenhuma GPU foi utilizada.',!check.ready);
});
ui.projectFile.addEventListener('change',async()=>{
 const file=ui.projectFile.files?.[0];if(!file)return;
 if(!ready()){status('Carregue primeiro o vídeo original e depois importe o JSON do projeto.',true);return}
 try{
  if(file.size>5e6)throw Error('O JSON do projeto deve ter até 5 MB');
  const data=JSON.parse(await file.text());
  if(!['furuya-recast-project/0.7','furuya-recast-project/0.8'].includes(data?.schema))throw Error('Formato de projeto não reconhecido');
  if(data.video?.width!==video.videoWidth||data.video?.height!==video.videoHeight||Math.abs((data.video?.duration||0)-duration)>.8)
   throw Error('O projeto não corresponde à resolução ou duração do vídeo carregado');
  if(!Array.isArray(data.characters)||data.characters.length>30)throw Error('Lista de personagens inválida');
  const imported=(data.keyframes?.length?data.keyframes:[{time:data.keyframe?.sourceTime||0,characters:data.characters,fullRepaintFilename:data.keyframe?.referenceFilename||null}]);
  if(imported.length>200)throw Error('Máximo de 200 quadros-chave');
  const validated=imported.map(safeSnapshot).sort((a,b)=>a.time-b.time);
  const oldImages=new Map(slots.map(s=>[s.id,s.image]));
  const head=validated[0]||{time:0,characters:[]};
  keyframes=validated;
  slots=head.characters.map(a=>({id:a.slot,name:a.name,referenceFile:a.referenceFilename,
   image:oldImages.get(a.slot)||null,x:a.x,y:a.y,rotation:a.rotationDegrees,scale:a.scale,
   polygon:a.polygon.map(p=>({...p})),anchorTime:head.time}));
  activeId=slots[0]?.id||null;nextId=Math.max(...slots.map(s=>s.id),0);
  workingTime=head.time;showRepaint=false;repaintTime=null;
  ui.clipStart.value=String(clamp(Number(data.video?.clipStart)||0,0,duration));
  const requested=Number(data.video?.clipDuration)||5;
  ui.clipLength.value=[3,5,8].includes(requested)?String(requested):'5';
  video.pause();stopLoop();video.currentTime=head.time;
  buildSlots();fillControls();renderKeyframeList();update();draw();
  ui.projectInfo.textContent='Projeto restaurado: '+keyframes.length+' quadros-chave. Reimporte imagens do(s) personagem(ns) e quadros retocados; o JSON não contém esses arquivos.';
  status('Projeto v0.8 carregado em memória. Não houve envio à nuvem.');
 }catch(e){status('Não foi possível reabrir o projeto: '+e.message,true)}
});

function saveBlob(data,name){
 const u=URL.createObjectURL(data),a=make('a',{href:u,download:name});document.body.append(a);a.click();setTimeout(()=>{URL.revokeObjectURL(u);a.remove()},8000);
}
function saveCanvas(name,kind){
 if(!canSave())return;
 if((kind==='mask'||kind==='draft')&&Math.abs(video.currentTime-workingTime)>.26){
  status('O instante da prévia não corresponde ao quadro em edição. Prepare ou recupere um quadro-chave antes de exportar a máscara/rascunho.',true);return;
 }
 const canvas=document.createElement('canvas');canvas.width=stage.width;canvas.height=stage.height;
 const c=canvas.getContext('2d');
 if(kind==='mask'){
  const s=active();if(!s||s.polygon.length<3)return;
  c.fillStyle='#000';c.fillRect(0,0,canvas.width,canvas.height);c.fillStyle='#fff';c.beginPath();
  s.polygon.forEach((p,i)=>{const [x,y]=toPixel(p);if(i)c.lineTo(x,y);else c.moveTo(x,y)});
  c.closePath();c.fill();
 }else if(kind==='repaint'){
  if(!repaint)return;c.drawImage(repaint,0,0,canvas.width,canvas.height);
 }else render(video.currentTime,{ctx:c,raw:kind==='source',forceDraft:kind==='draft',noGuides:true});
 canvas.toBlob(blob=>{if(blob)saveBlob(blob,name)},'image/png');
}
ui.saveSource.addEventListener('click',()=>saveCanvas('furuya-quadro-original.png','source'));
ui.saveDraft.addEventListener('click',()=>saveCanvas('furuya-rascunho-personagens.png','draft'));
ui.saveMask.addEventListener('click',()=>saveCanvas('furuya-mascara-pessoa-'+activeId+'.png','mask'));
ui.saveRepaint.addEventListener('click',()=>saveCanvas('furuya-quadro-retocado.png','repaint'));
function manifest(){
 const start=clamp(Number(ui.clipStart.value)||0,0,Math.max(0,duration-.1));
 const len=Math.min(Number(ui.clipLength.value)||5,duration-start);
 return {schema:'furuya-recast-project/0.8',created:new Date().toISOString(),video:{filename:ui.videoFile.files?.[0]?.name||null,width:video.videoWidth,height:video.videoHeight,duration,clipStart:start,clipDuration:len},keyframe:{sourceTime:workingTime,relativeToClip:workingTime-start,referenceFilename:repaint&&repaintTime!==null&&Math.abs(workingTime-repaintTime)<=.26?repaintName:null,frameCanvasWidth:stage.width,frameCanvasHeight:stage.height,hasFullRepaint:!!repaint&&repaintTime!==null&&Math.abs(workingTime-repaintTime)<=.26},keyframes:keyframes.map(k=>({time:k.time,characters:k.characters.map(a=>({...a,polygon:a.polygon.map(p=>({...p}))})),fullRepaintFilename:k.fullRepaintFilename})),characters:slots.map(slotSnapshot),paths:{originalFrame:'furuya-quadro-original.png',draft:'furuya-rascunho-personagens.png',mask:'furuya-mascara-pessoa-[slot].png',repaintedFrame:'furuya-quadro-retocado.png',drivingClip:'furuya-trecho-video.webm'},pipeline:{recommended:'video-conditioned whole-character replacement',viggleAnimate:'Requires driving clip plus fully repainted frame FROM THAT CLIP; no pose JSON needed.',wan22Animate:'Requires official pose/face/mask/background preprocess; manually drawn mask here does not replace it.',status:'PREPARATION_ONLY; NO AI VIDEO GENERATED'},privacy:'Files local. No remote upload performed.'};
}
ui.saveProject.addEventListener('click',()=>{if(!canSave())return;saveBlob(new Blob([JSON.stringify(manifest(),null,2)],{type:'application/json'}),'furuya-projeto-recasting.json')});
function mediaType(){
 if(!window.MediaRecorder||typeof stage.captureStream!=='function')return null;
 return ['video/webm;codecs=vp8','video/webm','video/mp4'].find(t=>MediaRecorder.isTypeSupported(t))||null;
}
function seek(t){
 return new Promise((resolve,reject)=>{
  if(Math.abs(video.currentTime-t)<.02&&video.readyState>=2)return resolve();
  const timer=setTimeout(()=>{video.removeEventListener('seeked',done);reject(new Error('Falha ao buscar o instante desejado.'))},12000);
  function done(){clearTimeout(timer);resolve()}
  video.addEventListener('seeked',done,{once:true});video.currentTime=t;
 });
}
function stopRecord(cancel=false){
 if(!exporting)return;clipCanceled=cancel;video.pause();
 if(raf)cancelAnimationFrame(raf);raf=0;
 if(record&&record.state!=='inactive'){try{record.requestData()}catch{}record.stop()}
 else{exporting=false;update()}
}
async function saveVideoSegment(){
 if(exporting){stopRecord(true);return}
 if(!canSave())return;
 const type=mediaType();if(!type){ui.exportInfo.textContent='O navegador não suporta MediaRecorder para esta exportação. Use a linha do tempo e o projeto JSON.';return}
 const m=manifest(),start=m.video.clipStart,length=m.video.clipDuration;
 if(length<.5){status('O trecho precisa ter pelo menos meio segundo.',true);return}
 if(Math.abs(video.currentTime-start)>1&&repaint)status('Atenção: o quadro retocado deve pertencer ao mesmo trecho selecionado.');
 try{
  video.pause();stopLoop();exporting=true;clipCanceled=false;clipChunks=[];update();
  ui.saveSegment.disabled=false;ui.saveSegment.textContent='■ Cancelar gravação';
  await seek(start);
  clipCanvas=document.createElement('canvas');clipCanvas.width=stage.width;clipCanvas.height=stage.height;
  clipContext=clipCanvas.getContext('2d');clipContext.drawImage(video,0,0,clipCanvas.width,clipCanvas.height);
  clipStream=clipCanvas.captureStream(24);
  clipType=type;record=new MediaRecorder(clipStream,{mimeType:type,videoBitsPerSecond:2500000});
  record.ondataavailable=e=>{if(e.data?.size)clipChunks.push(e.data)};
  record.onerror=e=>status('Falha do MediaRecorder: '+(e.error?.message||'erro'),true);
  record.onstop=()=>{
   clipStream?.getTracks().forEach(t=>t.stop());clipStream=null;
   if(!clipCanceled&&clipChunks.length)saveBlob(new Blob(clipChunks,{type:clipType}),'furuya-trecho-video.'+(clipType.includes('mp4')?'mp4':'webm'));
   ui.exportInfo.textContent=clipCanceled?'Gravação cancelada.':'Trecho exportado no navegador. Confira a reprodução e duração antes de usar na IA.';
   exporting=false;record=null;ui.saveSegment.textContent='↓ Trecho de vídeo';update();draw();
  };
  record.start(300);
  await video.play();
  const target=start+length;
  function step(){
   if(!exporting)return;
   clipContext.drawImage(video,0,0,clipCanvas.width,clipCanvas.height);
   ui.exportInfo.textContent='Exportando vídeo original: '+clock(Math.max(0,video.currentTime-start))+' / '+clock(length)+' (sem áudio)';
   if(video.currentTime>=target-.025||video.ended){stopRecord(false);return}
   if(video.paused){stopRecord(true);return}
   raf=requestAnimationFrame(step);
  }
  step();
 }catch(e){
  status('Exportação não iniciada: '+e.message,true);
  if(record&&record.state!=='inactive')stopRecord(true);
  else{clipStream?.getTracks().forEach(t=>t.stop());exporting=false;ui.saveSegment.textContent='↓ Trecho de vídeo';update()}
 }
}
ui.saveSegment.addEventListener('click',saveVideoSegment);
setMode('drag');renderKeyframeList();draw();update();
