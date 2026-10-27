'use strict';
const $=id=>document.getElementById(id);
const video=$('source'),screen=$('screen'),ctx=screen.getContext('2d');
const ui={videoFile:$('videoFile'),jsonFile:$('jsonFile'),sourceInfo:$('sourceInfo'),status:$('status'),layers:$('layers'),addLayer:$('addLayer'),scrub:$('scrub'),time:$('time'),length:$('length'),play:$('play'),pause:$('pause'),snapshot:$('snapshot'),coverage:$('coverage'),exportVideo:$('exportVideo'),stopExport:$('stopExport'),progress:$('progress'),exportInfo:$('exportInfo')};
let motion=null,frames=[],duration=0,videoURL=null,layers=[],serial=0,raf=0,exporting=false,recorder=null,recordChunks=[],mediaType='',exportStopped=false,recordStream=null;
const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
const format=x=>{const t=Number.isFinite(x)?Math.max(0,x):0;return String(Math.floor(t/60)).padStart(2,'0')+':'+(t%60).toFixed(2).padStart(5,'0')};
const ready=()=>Boolean(motion&&video.readyState>=2);
function status(message,error=false){ui.status.textContent=message;ui.status.className='status'+(error?' error':'')}
function updateUI(){
 const can=ready(),idle=!exporting;
 ui.addLayer.disabled=!motion||!idle;ui.scrub.disabled=!can||!idle;
 ui.play.disabled=!can||!idle;ui.pause.disabled=!can||!idle;
 ui.snapshot.disabled=!can||!idle;ui.exportVideo.disabled=!can||!layers.some(l=>l.image)||!idle;
 ui.stopExport.disabled=!exporting;
 ui.time.textContent=format(video.currentTime);ui.length.textContent=format(duration);
}
function resized(){
 if(!video.videoWidth||!video.videoHeight)return;
 const ratio=Math.min(1,1280/Math.max(video.videoWidth,video.videoHeight));
 screen.width=Math.max(2,Math.round(video.videoWidth*ratio/2)*2);
 screen.height=Math.max(2,Math.round(video.videoHeight*ratio/2)*2);
}
ui.videoFile.addEventListener('change',()=>{
 const file=ui.videoFile.files?.[0];if(!file)return;
 video.pause();stopLoop();if(videoURL)URL.revokeObjectURL(videoURL);
 videoURL=URL.createObjectURL(file);video.src=videoURL;video.load();
 ui.sourceInfo.textContent='Vídeo: '+file.name+' · carregando…';updateUI();
});
video.addEventListener('loadeddata',()=>{
 duration=video.duration;resized();
 ui.sourceInfo.textContent='Vídeo: '+(ui.videoFile.files?.[0]?.name||'')+' · '+video.videoWidth+'×'+video.videoHeight+' · '+format(duration)+' · saída: '+screen.width+'×'+screen.height;
 if(motion&&motion.dimensions&&Math.abs(motion.dimensions[0]/motion.dimensions[1]-video.videoWidth/video.videoHeight)>.03){
  status('A proporção do vídeo é diferente do JSON! Os personagens podem ficar desalinhados.',true);
 }else if(motion&&Math.abs(motion.sourceDuration-duration)>.5){
  status('A duração do vídeo é diferente do JSON. Escolha o mesmo arquivo da captura.',true);
 }else status('Vídeo carregado. A composição usa somente dados locais.');
 draw();updateUI();
});
video.addEventListener('error',()=>status('Erro de vídeo: tente MP4/H.264 no Chrome Android.',true));
async function loadMotion(file){
 if(!file)return;
 try{
  if(file.size>60e6)throw Error('O limite experimental de JSON é 60 MB.');
  const data=JSON.parse(await file.text());
  if(data.app!=='Furuya Motion Studio'||!Array.isArray(data.frames)||!data.frames.length)throw Error('JSON não pertence ao Furuya Motion Studio.');
  if(!data.frames.every(f=>Number.isFinite(f.t)&&Array.isArray(f.people)))throw Error('Quadros inválidos.');
  motion=data;
  frames=data.frames.map(f=>({...f,people:f.people.filter(p=>Array.isArray(p.landmarks)&&p.landmarks.length>=33)})).sort((a,b)=>a.t-b.t);
  layers.forEach(l=>{if(l.image?.close)l.image.close()});layers=[];serial=0;ui.layers.replaceChildren();
  status('JSON v'+data.version+' carregado: '+frames.length+' quadros. Identidades ainda são estimadas.');
  addLayer();updateCoverage();updateUI();draw();
 }catch(e){status('Erro no JSON: '+e.message,true)}
}
ui.jsonFile.addEventListener('change',()=>loadMotion(ui.jsonFile.files?.[0]));
function trackOptions(){
 const stats=new Map();
 for(const f of frames)for(const p of f.people)if(Number.isInteger(Number(p.id)))stats.set(Number(p.id),(stats.get(Number(p.id))||0)+1);
 const entries=[...stats].sort((a,b)=>b[1]-a[1]);
 return [{v:'selected',label:'★ Alvo escolhido na captura'},...entries.map(([id,n])=>({v:String(id),label:'Trilha '+id+' ('+n+' quadros)'}))];
}
function element(tag,props={},txt){
 const n=document.createElement(tag);
 for(const [k,v]of Object.entries(props)){
  if(k==='className')n.className=v;else if(k==='type'||k==='accept'||k==='min'||k==='max'||k==='step'||k==='value'||k==='title')n.setAttribute(k,v);
  else n[k]=v;
 }
 if(txt!==undefined)n.textContent=txt;
 return n;
}
function field(name,control){const node=element('div');node.append(element('label',{},name),control);return node}
function select(options,value){
 const n=element('select');options.forEach(o=>n.append(element('option',{value:o.v},o.label)));n.value=value;return n;
}
function slider(label,min,max,step,val,callback){
 const n=element('input',{type:'range',min,max,step,value:val}),amount=element('span',{className:'num'},String(val));
 const wrap=element('div'),heading=element('label');
 heading.append(document.createTextNode(label+' '),amount);wrap.append(heading,n);
 n.addEventListener('input',()=>{amount.textContent=n.value;callback(Number(n.value));draw()});
 return wrap;
}
function addLayer(){
 if(!motion)return;
 const selectedExists=frames.some(f=>f.people.some(p=>p.selected));
 const defaultTrack=selectedExists?'selected':(trackOptions()[1]?.v||'selected');
 const layer={id:++serial,mode:'head',track:defaultTrack,scale:1,offsetX:0,offsetY:0,alpha:1,image:null,fileName:'',hasTransparency:false};
 layers.push(layer);
 const box=element('section',{className:'layer'});
 const heading=element('div',{className:'layerHead'}),remove=element('button',{className:'danger',type:'button'},'Remover');
 heading.append(element('strong',{},'Personagem '+layer.id),remove);box.append(heading);
 const upload=element('input',{type:'file',accept:'image/png,image/webp,image/*'}),thumb=element('img',{className:'thumb',alt:'Miniatura'});
 const uploader=element('div',{className:'row'});uploader.append(upload,thumb);box.append(uploader);
 const controls=element('div',{className:'controlgrid'});
 const track=select(trackOptions(),layer.track),mode=select([{v:'head',label:'Cabeça / rosto'},{v:'body',label:'Corpo rígido'}],layer.mode);
 controls.append(field('Vincular à trilha',track),field('Posicionamento',mode));box.append(controls);
 const tuning=element('div',{className:'controlgrid'});
 tuning.append(slider('Escala',.3,3,.05,1,v=>layer.scale=v),slider('Opacidade',.25,1,.05,1,v=>layer.alpha=v),slider('Deslocamento X',-60,60,1,0,v=>layer.offsetX=v/100),slider('Deslocamento Y',-60,60,1,0,v=>layer.offsetY=v/100));
 box.append(tuning);
 const note=element('p',{className:'caption'},'Escolha um PNG com fundo transparente para evitar um retângulo ao redor do personagem.');
 box.append(note);ui.layers.append(box);
 track.addEventListener('change',()=>{layer.track=track.value;draw();updateCoverage()});
 mode.addEventListener('change',()=>{layer.mode=mode.value;draw()});
 remove.addEventListener('click',()=>{
  if(exporting)return;
  if(layer.image?.close)layer.image.close();layers=layers.filter(l=>l!==layer);box.remove();draw();updateUI();updateCoverage();
 });
 upload.addEventListener('change',async()=>{
  const file=upload.files?.[0];if(!file)return;
  try{
   const bitmap=await createImageBitmap(file);
   if(layer.image?.close)layer.image.close();layer.image=bitmap;layer.fileName=file.name;
   const cv=document.createElement('canvas');cv.width=16;cv.height=16;
   const c=cv.getContext('2d',{willReadFrequently:true});c.drawImage(bitmap,0,0,16,16);
   const d=c.getImageData(0,0,16,16).data;
   layer.hasTransparency=false;for(let i=3;i<d.length;i+=4)if(d[i]<240){layer.hasTransparency=true;break}
   const url=URL.createObjectURL(file);thumb.src=url;thumb.onload=()=>URL.revokeObjectURL(url);
   note.textContent=file.name+' · '+bitmap.width+'×'+bitmap.height+(layer.hasTransparency?' · com transparência':' · imagem opaca: pode cobrir o vídeo');
   draw();updateUI();
  }catch(e){status('Não foi possível importar a imagem: '+e.message,true)}
 });
 updateCoverage();updateUI();draw();
}
ui.addLayer.addEventListener('click',addLayer);
function eligible(frame,track){return frame.people.filter(p=>track==='selected'?p.selected===true:String(p.id)===track)}
// Nearest known pose: do not invent movement during long gaps or interpolate across changing IDs.
function atTime(t,track){
 if(!frames.length)return null;
 let lo=0,hi=frames.length-1;
 while(lo<hi){const m=(lo+hi+1)>>1;if(frames[m].t<=t)lo=m;else hi=m-1}
 const a=frames[lo],b=frames[Math.min(lo+1,frames.length-1)];
 const pa=eligible(a,track)[0],pb=eligible(b,track)[0];
 const maxGap=.38;
 if(pa&&Math.abs(t-a.t)<=maxGap){
  if(pb&&b!==a&&b.t-a.t<=.45&&(track!=='selected'||pa.id===pb.id)){
   const f=clamp((t-a.t)/(b.t-a.t),0,1);
   return {p:interpolate(pa,pb,f),kind:'interpolado'};
  }
  return {p:pa,kind:'medido'};
 }
 if(pb&&Math.abs(b.t-t)<=maxGap)return {p:pb,kind:'medido'};
 // Hold a preceding pose only for a very short missing sample, without bridging long occlusions.
 for(let i=lo-1;i>=Math.max(0,lo-2);i--){
  const prev=eligible(frames[i],track)[0];
  if(prev&&t-frames[i].t<=.30)return {p:prev,kind:'retenção breve'};
 }
 return null;
}
function interpolate(a,b,f){
 const landmarks=a.landmarks.map((p,i)=>p.map((v,k)=>v*(1-f)+(b.landmarks[i]?.[k]??v)*f));
 return {...a,landmarks};
}
function point(p,i,min=.48){
 const a=p?.landmarks?.[i];
 return a&&a[3]>=min&&a[0]>=0&&a[0]<=1&&a[1]>=0&&a[1]<=1?{x:a[0],y:a[1]}:null;
}
function geometry(p,mode,image){
 const l=point(p,11),r=point(p,12);if(!l||!r)return null;
 const sw=screen.width,sh=screen.height;
 const shoulderDist=Math.hypot((l.x-r.x)*sw,(l.y-r.y)*sh);
 if(shoulderDist<8)return null;
 const middle={x:(l.x+r.x)/2,y:(l.y+r.y)/2};
 const angle=Math.atan2((r.y-l.y)*sh,(r.x-l.x)*sw);
 const earL=point(p,7,.35),earR=point(p,8,.35),nose=point(p,0,.35);
 if(mode==='head'){
  const center=earL&&earR?{x:(earL.x+earR.x)/2,y:(earL.y+earR.y)/2}:nose;
  if(!center)return null;
  const w=shoulderDist*.95;
  return {x:center.x*sw,y:center.y*sh,w,h:w*image.height/image.width,angle:angle*.25};
 }
 const hipL=point(p,23),hipR=point(p,24);
 const hip=hipL&&hipR?{x:(hipL.x+hipR.x)/2,y:(hipL.y+hipR.y)/2}:null;
 const torso=hip?Math.hypot((middle.x-hip.x)*sw,(middle.y-hip.y)*sh):shoulderDist*.8;
 const w=Math.max(shoulderDist*1.15,torso*.85);
 return {x:middle.x*sw,y:middle.y*sh+torso*.4,w,h:w*image.height/image.width,angle:angle*.2};
}
function renderFrame(t){
 ctx.clearRect(0,0,screen.width,screen.height);
 if(video.readyState>=2){try{ctx.drawImage(video,0,0,screen.width,screen.height)}catch{}}
 else{ctx.fillStyle='#090f1e';ctx.fillRect(0,0,screen.width,screen.height)}
 let visible=0;
 for(const layer of layers){
  if(!layer.image)continue;
  const data=atTime(t,layer.track);if(!data)continue;
  const g=geometry(data.p,layer.mode,layer.image);if(!g)continue;
  visible++;
  ctx.save();ctx.globalAlpha=layer.alpha;
  ctx.translate(g.x+layer.offsetX*screen.width,g.y+layer.offsetY*screen.height);
  ctx.rotate(g.angle);
  const w=g.w*layer.scale,h=g.h*layer.scale;
  if(layer.mode==='head')ctx.drawImage(layer.image,-w/2,-h*.52,w,h);
  else ctx.drawImage(layer.image,-w/2,-h*.24,w,h);
  ctx.restore();
 }
 return visible;
}
function draw(){
 renderFrame(video.currentTime||0);
 if(!exporting){ui.scrub.value=duration?Math.round(clamp(video.currentTime/duration,0,1)*1000):0;ui.time.textContent=format(video.currentTime)}
}
function stopLoop(){if(raf)cancelAnimationFrame(raf);raf=0}
function tick(){draw();if(!video.paused&&!exporting)raf=requestAnimationFrame(tick)}
function playback(){if(!ready())return;stopLoop();video.play().then(tick).catch(e=>status('Reprodução não iniciada: '+e.message,true))}
ui.play.addEventListener('click',playback);
ui.pause.addEventListener('click',()=>{video.pause();stopLoop();draw()});
ui.scrub.addEventListener('input',()=>{
 if(!duration||exporting)return;video.pause();stopLoop();
 video.currentTime=duration*Number(ui.scrub.value)/1000;ui.time.textContent=format(video.currentTime);
});
video.addEventListener('seeked',()=>{if(!exporting)draw()});
video.addEventListener('ended',()=>{stopLoop();draw();if(exporting)finishRecord()});
function updateCoverage(){
 if(!frames.length){ui.coverage.textContent='Importe os movimentos para calcular a cobertura.';return}
 const tracks=[...new Set(layers.map(l=>l.track))];
 ui.coverage.textContent=tracks.map(track=>{
  const n=frames.filter(f=>eligible(f,track).length).length;
  return (track==='selected'?'Alvo selecionado':'Trilha '+track)+': '+n+'/'+frames.length+' quadros ('+Math.round(n/frames.length*100)+'%)';
 }).join(' · ')+' · nenhuma lacuna é reconstruída automaticamente.';
}
function saveBlob(blob,name){
 const url=URL.createObjectURL(blob),a=element('a',{href:url,download:name});
 document.body.append(a);a.click();setTimeout(()=>{URL.revokeObjectURL(url);a.remove()},5000);
}
ui.snapshot.addEventListener('click',()=>{
 if(!ready())return;draw();
 screen.toBlob(b=>{if(b)saveBlob(b,'furuya-composicao-'+Math.round(video.currentTime*1000)+'.png')},'image/png');
});
function supportedMedia(){
 if(!window.MediaRecorder||!screen.captureStream)return null;
 return ['video/webm;codecs=vp9','video/webm;codecs=vp8','video/webm','video/mp4'].find(x=>MediaRecorder.isTypeSupported(x))||null;
}
function seek(t){
 return new Promise((resolve,reject)=>{
  if(Math.abs(video.currentTime-t)<.02){resolve();return}
  const timeout=setTimeout(()=>{video.removeEventListener('seeked',done);reject(Error('O vídeo não respondeu à busca de quadro'))},10000);
  function done(){clearTimeout(timeout);resolve()}
  video.addEventListener('seeked',done,{once:true});video.currentTime=t;
 });
}
async function beginRecord(){
 if(exporting||!ready()||!layers.some(l=>l.image))return;
 const type=supportedMedia();
 if(!type){status('Este navegador não oferece MediaRecorder com saída de vídeo. Experimente Chrome atualizado ou PNG.',true);return}
 try{
  video.pause();stopLoop();exporting=true;exportStopped=false;recordChunks=[];updateUI();
  await seek(0);renderFrame(0);
  recordStream=screen.captureStream(24);mediaType=type;
  recorder=new MediaRecorder(recordStream,{mimeType:type,videoBitsPerSecond:3000000});
  recorder.ondataavailable=e=>{if(e.data?.size)recordChunks.push(e.data)};
  recorder.onerror=e=>status('Erro do MediaRecorder: '+(e.error?.message||'não especificado'),true);
  recorder.onstop=()=>{
   recordStream?.getTracks().forEach(x=>x.stop());recordStream=null;
   if(recordChunks.length&&!exportStopped){
    const ext=mediaType.includes('mp4')?'mp4':'webm';
    saveBlob(new Blob(recordChunks,{type:mediaType}),'furuya-motion-composicao.'+ext);
   }
   exporting=false;recorder=null;
   ui.progress.style.width=exportStopped?'0%':'100%';
   ui.exportInfo.textContent=exportStopped?'Exportação interrompida.':'Exportação finalizada.';
   updateUI();draw();
  };
  recorder.start(250);
  ui.exportInfo.textContent='Gravando sem áudio em tempo real…';
  await video.play();
  function step(){
   renderFrame(video.currentTime);
   ui.progress.style.width=Math.round(clamp(video.currentTime/Math.max(duration,.001),0,1)*100)+'%';
   ui.exportInfo.textContent='Gravando '+format(video.currentTime)+' de '+format(duration)+' · sem áudio';
   if(exporting&&!video.paused&&!video.ended)raf=requestAnimationFrame(step);
   else if(exporting&&video.ended)finishRecord();
  }
  step();
 }catch(e){
  status('Erro ao iniciar exportação: '+e.message,true);
  if(recorder&&recorder.state!=='inactive'){exportStopped=true;recorder.stop()}
  else{recordStream?.getTracks().forEach(x=>x.stop());recordStream=null;exporting=false;updateUI()}
 }
}
function finishRecord(){
 if(!exporting)return;video.pause();stopLoop();
 if(recorder&&recorder.state!=='inactive'){try{recorder.requestData()}catch{}recorder.stop()}
 else{exporting=false;updateUI()}
}
ui.exportVideo.addEventListener('click',beginRecord);
ui.stopExport.addEventListener('click',()=>{exportStopped=true;finishRecord()});
draw();updateUI();
