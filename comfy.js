'use strict';
/* Furuya local-only ComfyUI/Openjutsu generation. Separate from optional Viggle.
 * No network upload or render without a real local gateway and explicit click.
 */
const cEl = name => document.getElementById(name);
let comfyGateway = false, comfyConnectionOk = false, comfyPrepared = false;
let comfyState = 'IDLE', comfyCurrentJob = null;
const comfyEnable = (id, active) => {cEl(id).disabled = !active};
const comfyMessage = (message, error=false) => {
 cEl('comfyStatus').textContent = message;
 cEl('comfyStatus').className = error ? 'note error' : 'note';
};
async function comfyRequest(route, options={}) {
 const response = await fetch('/api/comfy/'+route, {cache:'no-store', ...options});
 let data;
 try{data = await response.json()}catch{throw new Error('Não há gateway Furuya local com suporte a ComfyUI.')}
 if(!response.ok) throw new Error(data.error || 'HTTP '+response.status);
 return data;
}
function comfyTargetCount(){return Number(cEl('targetCount').value||1)}
function comfyUpdateInputs(){
 const count = comfyTargetCount();
 for(let i=2;i<=4;i++){
  cEl('comfyExtra'+i).hidden = i>count;
  cEl('comfyRoleWrap'+i).hidden = i>count;
 }
 comfyRefreshButtons();
}
function comfyRefreshButtons(){
 comfyEnable('comfyCheck',comfyGateway);
 comfyEnable('comfyPrepare',comfyGateway&&comfyState!=='SUBMITTED'
  &&comfyState!=='PENDING'&&comfyState!=='SUBMISSION_UNCERTAIN');
 comfyEnable('comfyStart',comfyGateway&&comfyConnectionOk&&comfyPrepared
  &&comfyState==='PREPARED'&&cEl('comfyAuthorize').checked);
 comfyEnable('comfyResume',comfyGateway&&['SUBMITTED','PENDING'].includes(comfyState));
 comfyEnable('comfyRefresh',comfyGateway);
}
function comfyShowJob(job){
 comfyCurrentJob = job;
 comfyState = job.status || 'IDLE';
 comfyPrepared = comfyState==='PREPARED';
 if(comfyState==='PREPARED'){
  comfyMessage('Workflow Openjutsu preparado para '+job.characters+
   ' personagem(ns); vídeo '+job.seconds+'s. Arquivos não foram enviados ao ComfyUI. '+
   'Verifique a instância e confirme somente se os modelos e a GPU estiverem realmente disponíveis.');
 }else if(comfyState==='SUBMISSION_UNCERTAIN'){
  comfyMessage('SUBMISSÃO INCERTA: não clique em gerar novamente. Confira a fila/console do ComfyUI.'+
  (job.error?' Detalhe: '+job.error:''),true);
 }else if(comfyState==='SUBMITTED'||comfyState==='PENDING'){
  comfyMessage('Processamento do prompt '+(job.prompt_id||'(não recebido)')+
   ' · '+(job.stage||comfyState)+'. Consultas não reenviam o trabalho.');
 }else if(comfyState==='RENDERED_UNREVIEWED'){
  cEl('comfyResultPanel').hidden = false;
  cEl('comfyResultVideo').src='/api/comfy/result';
  cEl('comfyDownload').href='/api/comfy/result';
  comfyMessage('Vídeo recebido do ComfyUI ('+job.output_bytes+' bytes). Ainda exige revisão de identidade, '+
   'corpo, roupas, multidão, oclusões e duração antes de aprovar.');
 }else if(comfyState==='FAILED'){
  comfyMessage('O workflow terminou sem MP4 disponível. Inspecione o workflow do ComfyUI. '+
  (job.error||''),true);
 }else if(comfyState==='IDLE'){
  comfyMessage('Nenhum processamento ComfyUI iniciado.');
 }
 comfyRefreshButtons();
}
async function comfyRefresh(){
 try{
  const job=await comfyRequest('status');
  comfyGateway=job.mode==='COMFYUI_LOCAL_ONLY';
  comfyShowJob(job);
  cEl('comfyConnection').textContent=comfyGateway
   ? 'Gateway Furuya local detectado. '+(job.configured?'Diretório ComfyUI configurado.':'Configure --comfy-input-dir no gateway para habilitar execução.')
   : 'Gateway ComfyUI indisponível.';
 }catch(error){
  comfyGateway=false; comfyConnectionOk=false; comfyPrepared=false;
  cEl('comfyConnection').textContent='Esta página só prepara/gera pelo gateway local, não pelo GitHub Pages. '+error.message;
  comfyRefreshButtons();
 }
}
async function comfyCheck(){
 try{
  comfyEnable('comfyCheck',false);
  const result=await comfyRequest('check');
  comfyConnectionOk=Boolean(result.connected&&result.openjutsu_present);
  const devices=(result.devices||[]).map(x=>x.name).filter(Boolean);
  cEl('comfyConnection').textContent=result.connected
   ? 'ComfyUI detectado. Nós essenciais Openjutsu: '+(result.openjutsu_present?'presentes':'ausentes')+
     '. Dispositivos: '+(devices.join(', ')||'não informados')+
     '. Atenção: pesos/VRAM e inferência ainda NÃO validados.'
   : (result.message||'ComfyUI não conectado.');
  if(!comfyConnectionOk)comfyMessage('Instância ComfyUI indisponível/incompleta. Nenhum trabalho foi submetido.',true);
 }catch(e){comfyConnectionOk=false;comfyMessage('Falha ao verificar ComfyUI: '+e.message,true)}
 finally{comfyRefreshButtons()}
}
async function comfyWorkflowBlob(){
 const selected=cEl('comfyWorkflow').files[0];
 if(selected) return selected;
 const result=await fetch('./workflows/openjutsu_advanced.api.json',{cache:'no-store'});
 if(!result.ok) throw new Error('Workflow padrão não disponível. Importe um workflow Openjutsu Advanced em formato API.');
 const blob=await result.blob();
 if(blob.size>2*1024*1024)throw new Error('Workflow padrão excede o limite de tamanho.');
 return new File([blob],'openjutsu_advanced.api.json',{type:'application/json'});
}
async function comfyPrepare(){
 const video=cEl('motion').files[0], first=cEl('image').files[0];
 if(!video||!first){comfyMessage('Selecione o vídeo e a primeira personagem no formulário principal.',true);return}
 const count=comfyTargetCount();
 const data=new FormData();
 data.append('motion_video',video);
 data.append('image_1',first);
 for(let i=2;i<=count;i++){
  const file=cEl('comfyImage'+i).files[0];
  if(!file){comfyMessage('Escolha a imagem da personagem '+i+'.',true);return}
  data.append('image_'+i,file);
 }
 for(let i=1;i<=count;i++){
  const role=cEl('comfyRole'+i).value.trim();
  if(!role){comfyMessage('Descreva a pessoa original '+i+' para evitar trocas de identidade.',true);return}
  data.append('role_'+i,role);
 }
 try{
  comfyEnable('comfyPrepare',false);
  comfyMessage('Validando o vídeo e preparando o workflow no computador; não há inferência nesta etapa.');
  data.append('workflow',await comfyWorkflowBlob());
  const job=await comfyRequest('prepare',{
   method:'POST',headers:{'X-Furuya-Intent':'local-explicit-user-action'},body:data
  });
  comfyShowJob(job);
 }catch(e){comfyMessage('Não foi possível preparar: '+e.message,true)}
 finally{comfyRefreshButtons()}
}
async function comfyStart(){
 if(!comfyConnectionOk||!comfyPrepared||!cEl('comfyAuthorize').checked){
  comfyMessage('Verifique o ComfyUI, prepare o trabalho e autorize a GPU local.',true);return
 }
 if(!window.confirm('Confirma executar UM workflow Openjutsu na sua instância ComfyUI local? '+
   'Confirme que os pesos estão instalados e que a GPU/infraestrutura não tem cobrança.'))return;
 try{
  comfyEnable('comfyStart',false);
  comfyMessage('Iniciando um único processamento local no ComfyUI…');
  const job=await comfyRequest('start',{
   method:'POST',
   headers:{'X-Furuya-Intent':'local-explicit-user-action',
    'X-Furuya-Confirm':'AUTHORIZE_LOCAL_GPU'}
  });
  comfyShowJob(job);
 }catch(e){comfyMessage('Falha ao iniciar: '+e.message,true)}
 finally{comfyRefreshButtons()}
}
async function comfyResume(){
 try{
  comfyEnable('comfyResume',false);
  const job=await comfyRequest('resume',{
   method:'POST',headers:{'X-Furuya-Intent':'local-explicit-user-action'}
  });
  comfyShowJob(job);
 }catch(e){comfyMessage('Não foi possível retomar consulta: '+e.message,true)}
 finally{comfyRefreshButtons()}
}
cEl('targetCount').addEventListener('change',comfyUpdateInputs);
cEl('comfyAuthorize').addEventListener('change',comfyRefreshButtons);
cEl('comfyCheck').addEventListener('click',comfyCheck);
cEl('comfyPrepare').addEventListener('click',comfyPrepare);
cEl('comfyStart').addEventListener('click',comfyStart);
cEl('comfyResume').addEventListener('click',comfyResume);
cEl('comfyRefresh').addEventListener('click',comfyRefresh);
comfyUpdateInputs();
comfyRefresh();
// Polling uses GET only. It NEVER retries /prompt or sends another render.
setInterval(()=>{
 if(comfyGateway&&['SUBMITTED','PENDING','SUBMISSION_UNCERTAIN'].includes(comfyState))comfyRefresh();
},5000);
