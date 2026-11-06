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
 pEl('peopleApprove').disabled=!(pPrepared&&pStatus==='TRACKS_READY_UNREVIEWED');
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
  const status=job.status==='TRACKS_REVIEWED_MONTAGE_PREPARED'
   ? 'Aparições revisadas e Montage preparado ('+job.selected_replacements+' substituições). Confirme o ComfyUI e clique Gerar no painel acima; nenhuma GPU foi acionada ainda.'
   : job.status==='TRACKS_READY_UNREVIEWED'
   ? 'Rastreamento recebido: '+job.appearances+' aparições em '+job.frames+' quadros. Revise cuidadosamente. Ainda não aplicado ao render.'
   : job.status==='SUBMISSION_UNCERTAIN'
    ? 'Envio incerto: consulte a fila ComfyUI manualmente. Não reenviar.'
    : job.status==='SUBMITTED'||job.status==='PENDING'
     ? 'Buscando pessoas… prompt '+(job.prompt_id||'não recebido')+'. Atualização somente de leitura.'
     : job.status==='IDLE'
      ? 'Nenhum rastreamento iniciado. Prepare a geração Openjutsu primeiro.'
      : 'Find People: '+job.status+(job.error?' — '+job.error:'');
  pMessage(status);
  pEl('peopleResults').hidden=!['TRACKS_READY_UNREVIEWED','TRACKS_REVIEWED_MONTAGE_PREPARED'].includes(job.status);
  if(['TRACKS_READY_UNREVIEWED','TRACKS_REVIEWED_MONTAGE_PREPARED'].includes(job.status))await pShowReview(parent);
 }catch(error){
  pPrepared=false;
  pMessage('Find People exige o gateway local Furuya: '+error.message);
 }finally{pControls()}
}
async function pShowReview(parent){
 const data=await pAPI('review');
 const gallery=pEl('peopleGallery');
 gallery.replaceChildren();
 const rows=(data.people||[]).slice(0,40);
 pEl('peopleSummary').textContent=
  (data.people||[]).length+' aparições detectadas ('+data.frames+' quadros). '+
  'Exibindo até 40. Selecione a personagem para cada aparição; todas as demais serão preservadas. '+
  'As sugestões do modelo não são aprovação de identidade.';
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
  card.append(text);
  const select=document.createElement('select');
  select.dataset.track=String(person.track);
  select.dataset.start=String(person.start);
  select.dataset.end=String(person.end);
  select.style.cssText='width:100%;background:#122039;color:white;padding:6px;border:1px solid #566882';
  for(let i=0;i<=Number(parent.characters||0);i++){
   const option=document.createElement('option');
   option.value=String(i);
   option.textContent=i===0?'Preservar original':'Substituir pela personagem '+i+
    ' ('+(parent.roles?.[i-1]||'referência '+i)+')';
   select.append(option);
  }
  // Fail-safe: unselected/hidden appearances are always preserved.
  select.value='0';
  select.disabled=pStatus!=='TRACKS_READY_UNREVIEWED';
  card.append(select);gallery.append(card);
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
async function pApprove(){
 const fields=[...document.querySelectorAll('#peopleGallery select[data-track]')];
 const selections=fields.map(el=>({
  track:Number(el.dataset.track),start:Number(el.dataset.start),
  end:Number(el.dataset.end),pick:Number(el.value)
 })).filter(el=>el.pick>0);
 if(!selections.length){pMessage('Selecione pelo menos uma aparição para substituir; ninguém será alterado automaticamente.');return}
 if(!window.confirm('Confirma '+selections.length+' substituição(ões) selecionadas? Todas as outras pessoas permanecerão originais. Isto só prepara o Montage; não utiliza GPU agora.'))return;
 try{
  pEl('peopleApprove').disabled=true;
  const result=await pAPI('approve',{method:'POST',
   headers:{'Content-Type':'application/json',
    'X-Furuya-Intent':'local-explicit-user-action'},
   body:JSON.stringify({selections})
  });
  pEl('comfyWorkflowMode').value='standard';
  if(typeof comfyUpdateInputs==='function')comfyUpdateInputs();
  pStatus='TRACKS_REVIEWED_MONTAGE_PREPARED';
  pMessage('Montage preparado para '+result.selected_replacements+
   ' aparição(ões), sem iniciar a GPU. Confira o pré-teste no painel acima.');
  if(typeof comfyRefresh==='function')await comfyRefresh();
  if(typeof comfyCheck==='function')await comfyCheck();
 }catch(error){pMessage('Montage não preparado: '+error.message)}
 finally{await pRefresh()}
}
pEl('peopleStart').addEventListener('click',pStart);
pEl('peopleApprove').addEventListener('click',pApprove);
pEl('peopleResume').addEventListener('click',pResume);
pEl('peopleRefresh').addEventListener('click',pRefresh);
pEl('comfyAuthorize').addEventListener('change',()=>{pAuthorized=pEl('comfyAuthorize').checked;pControls()});
pRefresh();
setInterval(()=>{if(['PENDING','SUBMITTED'].includes(pStatus))pRefresh()},6000);
