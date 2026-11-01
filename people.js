'use strict';
/* Find People is an independent, optional tracking pass over a PREPARED
 * Openjutsu job. No automatic POST, no paid API, no render, no auto-approval.
 */
const pEl = id => document.getElementById(id);
let pStatus='IDLE', pPrepared=false, pAuthorized=false;
async function pAPI(resource, options={}){
 const r=await fetch('/api/comfy/people/'+resource,{cache:'no-store',...options});
 let obj;
 try{obj=await r.json()}catch{throw new Error('Gateway local não conectado.')}
 if(!r.ok)throw new Error(obj.error||('HTTP '+r.status));
 return obj;
}
function pMessage(text){pEl('peopleStatus').textContent=text}
function pControls(){
 const canStart=pStatus==='IDLE'||pStatus==='FAILED'||pStatus==='TRACKS_READY_UNREVIEWED';
 pEl('peopleStart').disabled=!(pPrepared&&pAuthorized&&canStart);
 pEl('peopleResume').disabled=!['SUBMITTED','PENDING'].includes(pStatus);
}
async function pRefresh(){
 try{
  const [parent,job]=await Promise.all([
   fetch('/api/comfy/status',{cache:'no-store'}).then(r=>r.json()),
   pAPI('status')
  ]);
  pPrepared=parent.status==='PREPARED'&&Boolean(parent.configured);
  pAuthorized=Boolean(pEl('comfyAuthorize').checked);
  pStatus=job.status;
  const status=job.status==='TRACKS_READY_UNREVIEWED'
   ? 'Rastreamento recebido: '+job.appearances+' aparições em '+job.frames+' quadros. Revise cuidadosamente. Ainda não aplicado ao render.'
   : job.status==='SUBMISSION_UNCERTAIN'
    ? 'Envio incerto: consulte a fila ComfyUI manualmente. Não reenviar.'
    : job.status==='SUBMITTED'||job.status==='PENDING'
     ? 'Buscando pessoas… prompt '+(job.prompt_id||'não recebido')+'. Atualização somente de leitura.'
     : job.status==='IDLE'
      ? 'Nenhum rastreamento iniciado. Prepare a geração Openjutsu primeiro.'
      : 'Find People: '+job.status+(job.error?' — '+job.error:'');
  pMessage(status);
  pEl('peopleResults').hidden=job.status!=='TRACKS_READY_UNREVIEWED';
  if(job.status==='TRACKS_READY_UNREVIEWED')await pShowReview();
 }catch(error){
  pPrepared=false;
  pMessage('Find People exige o gateway local Furuya: '+error.message);
 }finally{pControls()}
}
async function pShowReview(){
 const data=await pAPI('review');
 const gallery=pEl('peopleGallery');
 gallery.replaceChildren();
 const rows=(data.people||[]).slice(0,40);
 pEl('peopleSummary').textContent=
  (data.people||[]).length+' aparições detectadas ('+data.frames+' quadros). '+
  'Exibindo até 40. Papéis são sugestões, não seleção confirmada; rastreamento ainda não vinculado ao render.';
 for(const person of rows){
  const card=document.createElement('div');
  card.style.cssText='background:#1c2c43;border:1px solid #45556f;border-radius:9px;padding:8px;font-size:12px';
  if(person.image&&person.image.startsWith('data:image/jpeg;base64,')&&person.image.length<180000){
   const img=document.createElement('img');
   img.alt='Recorte da pessoa rastreada '+person.track;
   img.src=person.image;
   img.loading='lazy';img.style.cssText='width:100%;max-height:160px;object-fit:contain';
   card.append(img);
  }
  const text=document.createElement('p');
  text.textContent='Pessoa/track '+person.track+' · quadros '+person.start+'–'+person.end+
   ' · papel previsto '+person.role+' · referência sugerida '+person.pick;
  card.append(text);gallery.append(card);
 }
}
async function pStart(){
 if(!pEl('comfyAuthorize').checked){pMessage('Autorize o uso da GPU local no painel Openjutsu.');return}
 if(!window.confirm('Executar uma única análise SAM 3.1 + Qwen na GPU local já configurada e sem cobrança? A operação NÃO gera vídeo.'))return;
 try{
  pEl('peopleStart').disabled=true;
  const job=await pAPI('start',{method:'POST',headers:{
   'X-Furuya-Intent':'local-explicit-user-action',
   'X-Furuya-Confirm':'AUTHORIZE_LOCAL_GPU'
  }});
  pStatus=job.status;
  pMessage('Rastreamento solicitado; sem render de vídeo. Consulte o status.');
 }catch(error){pMessage('Rastreamento não iniciado: '+error.message)}
 finally{pRefresh()}
}
async function pResume(){
 try{
  const job=await pAPI('resume',{method:'POST',
   headers:{'X-Furuya-Intent':'local-explicit-user-action'}});
  pStatus=job.status;pMessage('Reconsulta do trabalho existente iniciada, sem novo envio.');
 }catch(error){pMessage('Retomada indisponível: '+error.message)}
 finally{pControls()}
}
pEl('peopleStart').addEventListener('click',pStart);
pEl('peopleResume').addEventListener('click',pResume);
pEl('peopleRefresh').addEventListener('click',pRefresh);
pEl('comfyAuthorize').addEventListener('change',()=>{pAuthorized=pEl('comfyAuthorize').checked;pControls()});
pRefresh();
setInterval(()=>{if(['PENDING','SUBMITTED'].includes(pStatus))pRefresh()},6000);
