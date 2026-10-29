'use strict';
const $ = id => document.getElementById(id);
let connected=false, prepared=false, available=null, jobStatus='IDLE', refreshing=false;
const button=(id,enable)=>{$(id).disabled=!enable};
function notice(msg,bad=false){$('state').textContent=msg;$('state').className=bad?'note error':'note'}
async function request(route,options){
 const response=await fetch('/api/'+route,{cache:'no-store',...options});
 let data;
 try{data=await response.json()}catch{throw new Error('Gateway não encontrado ou retornou resposta inválida. Execute o servidor Python local.')}
 if(!response.ok)throw new Error(data.error||'Erro HTTP '+response.status);
 return data;
}
function refreshControls(){
 button('credits',connected);
 button('prepare',connected);
 button('generate',connected&&prepared&&available!==null&&available>=0&&jobStatus==='PREPARED'&&$('confirm').checked);
 button('resume',connected&&['PENDING','SUBMITTED'].includes(jobStatus));
}
async function connect(){
 try{
  const status=await request('status');
  connected=status.gateway==='LOCAL_ONLY';
  jobStatus=status.status;
  $('connection').textContent=connected
   ? 'Gateway local conectado. Chave da API '+(status.api_key_configured?'configurada.':'não configurada — sem submissões.')
   : 'Gateway não disponível.';
  if(connected&&status.status==='PREPARED'){prepared=true;$('prepared').textContent='Pacote preparado neste servidor. Consulte os créditos antes de gerar.'}
  refreshControls();
  await showStatus(status);
 }catch(e){connected=false;$('connection').textContent='Servidor local indisponível. Esta página pode mostrar os controles no GitHub Pages, mas precisa do gateway para gerar: '+e.message;refreshControls()}
}
async function credits(){
 try{
  const r=await request('credits');
  available=r.available;
  $('connection').textContent=r.status==='OK'
   ?'Conectado. Saldo: '+r.available+' crédito(s) disponíveis. A origem gratuita dos créditos não é identificável.'
   :'Chave Viggle ausente no ambiente local. Não é possível executar.';
  refreshControls();
 }catch(e){available=null;$('connection').textContent='Falha na verificação de créditos: '+e.message;refreshControls()}
}
async function showStatus(s){
 jobStatus=s.status;
 if(s.status==='RENDERED_UNREVIEWED'){
  $('resultPanel').hidden=false;
  $('resultVideo').src='/api/result';
  $('download').href='/api/result';
  notice('MP4 generativo renderizado e recebido. A identidade da Albedo, a coreografia e a multidão ainda precisam de auditoria visual. Arquivo: '+s.output_bytes+' bytes.');
 }else if(s.status==='PREPARED'){
  notice('Arquivos preparados: '+s.duration_seconds+' s; custo estimado '+s.credit_estimate+' crédito(s). Aguardando autorização explícita.');
 }else if(s.status==='SUBMISSION_UNCERTAIN'){
  notice('SUBMISSÃO INCERTA. Não envie de novo: uma cobrança pode ter ocorrido. Confira seu painel Viggle e recupere o render_id, se existir. '+(s.error||''),true);
 }else if(s.status==='FAILED'){
  notice('O provedor retornou falha: '+(s.error||'erro não especificado'),true);
 }else if(['SUBMITTED','PENDING'].includes(s.status)){
  notice('Render '+(s.render_id||'')+' — '+(s.stage||s.status)+'. Não reenvie. Use a consulta do job existente.');
 }else if(s.status!=='IDLE'){
  notice('Estado: '+s.status+'.');
 }
 refreshControls();
}
async function prepare(){
 const image=$('image').files[0],motion=$('motion').files[0];
 if(!image||!motion){notice('Selecione a PNG original da Albedo e o driving.mp4.',true);return}
 const form=new FormData();
 form.append('image',image);form.append('motion_video',motion);
 const repaint=$('repaint').files[0];if(repaint)form.append('repaint',repaint);
 try{
  button('prepare',false);notice('Validando arquivos localmente, sem gerar vídeo…');
  const job=await request('prepare',{method:'POST',headers:{'X-Furuya-Intent':'local-explicit-user-action'},body:form});
  prepared=true;available=null;
  $('prepared').textContent='Vídeo: '+job.duration_seconds+'s · Custo estimado: '+job.credit_estimate+' crédito(s). Quadro retocado é arquivado, não usado no Remix.';
  await showStatus(job);
 }catch(e){notice('Falha na preparação: '+e.message,true)}
 finally{refreshControls()}
}
async function generate(){
 if(!$('confirm').checked){notice('A autorização explícita é obrigatória.',true);return}
 if(available===null){notice('Consulte o saldo primeiro.',true);return}
 if(!window.confirm('Confirma enviar imagem e vídeo ao Viggle e usar até os créditos disponíveis para este teste? Não haverá compra automática.'))return;
 try{
  button('generate',false);
  const job=await request('start',{method:'POST',headers:{'X-Furuya-Intent':'local-explicit-user-action','X-Furuya-Confirm':'AUTHORIZE_EXISTING_CREDITS'}});
  await showStatus(job);
 }catch(e){notice('Não foi possível iniciar: '+e.message,true)}
}
async function refresh(){
 if(refreshing||!connected)return;
 refreshing=true;
 try{await showStatus(await request('status'))}catch(e){notice('Erro ao consultar: '+e.message,true)}
 finally{refreshing=false}
}
async function resume(){
 try{
  const job=await request('resume',{method:'POST',headers:{'X-Furuya-Intent':'local-explicit-user-action'}});
  await showStatus(job);
 }catch(e){notice('Falha na recuperação: '+e.message,true)}
}
$('connect').addEventListener('click',connect);
$('credits').addEventListener('click',credits);
$('prepare').addEventListener('click',prepare);
$('generate').addEventListener('click',generate);
$('refresh').addEventListener('click',refresh);
$('resume').addEventListener('click',resume);
$('confirm').addEventListener('change',refreshControls);
connect();
// Polling only queries local status. It never submits a render.
setInterval(()=>{if(connected&&['SUBMISSION_UNCERTAIN','SUBMITTED','PENDING'].includes(jobStatus))refresh()},5000);