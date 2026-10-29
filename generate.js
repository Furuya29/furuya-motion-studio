'use strict';
const $ = id => document.getElementById(id);
let connected=false, prepared=false, available=null, requiredCredits=null, jobStatus='IDLE', refreshing=false;
let engineCatalog=null, routePolicy=null;
const button=(id,enable)=>{$(id).disabled=!enable};
function notice(msg,bad=false){$('state').textContent=msg;$('state').className=bad?'note error':'note'}
async function request(route,options){
 const response=await fetch('/api/'+route,{cache:'no-store',...options});
 let data;
 try{data=await response.json()}catch{throw new Error('Gateway não encontrado ou retornou resposta inválida. Execute o servidor Python local.')}
 if(!response.ok)throw new Error(data.error||'Erro HTTP '+response.status);
 return data;
}
function currentEngine(){return $('engine').value}
function automaticTask(){
 const count=Number($('targetCount').value||1);
 return count>1?'multi_scene_replacement':$('preserveScene').value==='true'?'scene_replacement':'motion_transfer';
}
function recommendFromPolicy(){
 const task=automaticTask();
 const ids=routePolicy?.priorities?.[task]||[];
 const engines=engineCatalog?.[task]||[];
 const found=ids.map(id=>engines.find(e=>e.id===id)).find(Boolean)||engines[0];
 return found?{task,engine:found}:null;
}
function applyMode(){
 const automatic=$('selectionMode').value==='auto';
 $('advancedEngineControls').hidden=automatic;
 if(automatic){
  const suggestion=recommendFromPolicy();
  if(suggestion){
   $('task').value=suggestion.task;
   renderEngines();
   $('engine').value=suggestion.engine.id;
   describeEngine();
   $('autoRecommendation').textContent=
    'Furuya recomenda: '+suggestion.engine.name+' · '+(routePolicy?.explanation?.[suggestion.task]||'')+
    ' · Situação: '+suggestion.engine.state+
    '. Isto é uma recomendação por regras; GPU, créditos e geração NÃO foram validados.';
  }else{
   $('autoRecommendation').textContent='O catálogo ainda não está disponível. Nenhuma geração será iniciada.';
  }
 }else{
  $('autoRecommendation').textContent='Modo avançado: escolha manualmente a categoria e o motor. As mesmas verificações de recursos e custos continuam obrigatórias.';
  renderEngines();
 }
 refreshControls();
}
async function loadPolicy(){
 try{
  const response=await fetch('./routing-policy.json',{cache:'no-store'});
  if(!response.ok)throw new Error('Regras não disponíveis.');
  const policy=await response.json();
  if(policy.schema!=='furuya-routing-policy/1')throw new Error('Versão de regras incompatível.');
  routePolicy=policy;
 }catch(e){routePolicy=null;$('autoRecommendation').textContent='Não foi possível carregar a política de seleção automática: '+e.message}
}

function engineIsLive(){return currentEngine()==='viggle_video_remix'&&$('task').value==='motion_transfer'}
function renderEngines(){
 const task=$('task').value, list=engineCatalog?.[task]||[];
 const old=$('engine').value;
 $('engine').replaceChildren();
 for(const engine of list){
  const option=document.createElement('option');
  option.value=engine.id;
  option.textContent=engine.name+' · '+(engine.state==='INTEGRATED_API_UNVERIFIED'?'API experimental':'adaptador offline');
  $('engine').append(option);
 }
 if(list.some(e=>e.id===old))$('engine').value=old;
 describeEngine();
}
function describeEngine(){
 const engine=(engineCatalog?.[$('task').value]||[]).find(e=>e.id===currentEngine());
 if(!engine){$('engineInfo').textContent='Catálogo indisponível; nenhum motor será executado.';refreshControls();return}
 $('engineInfo').textContent=engine.strengths+' LIMITAÇÕES: '+engine.limitations+
  (engineIsLive()
   ? ' A execução exige chave Viggle e créditos verificados.'
   : ' Não existe backend de render ativo para este motor; é possível preparar os arquivos, mas não enviar GPU automaticamente.');
 prepared=false;available=null;requiredCredits=null;
 refreshControls();
}
async function loadEngines(){
 try{engineCatalog=await request('engines');await loadPolicy();applyMode()}
 catch(e){$('engineInfo').textContent='Catálogo local indisponível: '+e.message}
}
function refreshControls(){
 button('credits',connected&&engineIsLive());
 button('prepare',connected&&$('task').value!=='multi_scene_replacement');
 button('generate',connected&&engineIsLive()&&prepared&&available!==null&&requiredCredits!==null&&available>=requiredCredits&&jobStatus==='PREPARED'&&$('confirm').checked);
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
  if(connected){await loadEngines()}
  if(connected&&status.status==='PREPARED'){
   if(status.task&&['scene_replacement','motion_transfer','multi_scene_replacement'].includes(status.task))$('task').value=status.task;
   renderEngines();
   if(status.route&&[...($('engine').options||[])].some(e=>e.value===status.route))$('engine').value=status.route;
   // Restore only if the current selection matches the recovered job.
   prepared=Boolean(status.route===currentEngine()&&status.task===$('task').value);
   requiredCredits=prepared?status.required_balance:null;
   $('prepared').textContent='Pacote preparado neste servidor. '+(status.backend_ready_for_submission?'Consulte os créditos para gerar.':'Motor offline: nenhum render pode ser iniciado aqui.');
   refreshControls();
  }
  refreshControls();
  await showStatus(status);
 }catch(e){
  connected=false;
  $('connection').textContent='Servidor local indisponível: o catálogo pode ser consultado neste site, mas nenhum motor será executado no GitHub Pages.';
  try{
   const response=await fetch('./engine-catalog.json',{cache:'no-store'});
   if(response.ok){engineCatalog=await response.json();await loadPolicy();applyMode()}
  }catch{}
  refreshControls();
 }
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
  notice(s.backend_ready_for_submission
   ? 'Arquivos preparados: '+s.duration_seconds+' s; custo estimado '+s.credit_estimate+' crédito(s). Aguardando autorização explícita.'
   : 'Pacote '+s.duration_seconds+' s preparado para '+s.route+'. Este é um adaptador offline: sem GPU gratuita validada e sem MP4 gerado.');
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
 if(!image||!motion){notice('Selecione a imagem da personagem e o vídeo original.',true);return}
 if($('task').value==='multi_scene_replacement'){
  notice('Para duas a quatro pessoas, use o planejador multipersonagem. O backend de rastreamento/render ainda não está conectado.',true);
  return;
 }
 const form=new FormData();
 form.append('image',image);form.append('motion_video',motion);
 form.append('task',$('task').value);form.append('engine_id',currentEngine());
 const repaint=$('repaint').files[0];if(repaint)form.append('repaint',repaint);
 try{
  button('prepare',false);notice('Validando arquivos localmente, sem gerar vídeo…');
  const job=await request('prepare',{method:'POST',headers:{'X-Furuya-Intent':'local-explicit-user-action'},body:form});
  prepared=true;available=null;requiredCredits=job.required_balance;
  $('prepared').textContent='Vídeo: '+job.duration_seconds+'s · Motor: '+job.route+'. '+(job.backend_ready_for_submission?'Custo estimado: '+job.credit_estimate+' crédito(s).':'Somente preparação. Requer execução futura do adaptador no ambiente correto.');
  await showStatus(job);
 }catch(e){notice('Falha na preparação: '+e.message,true)}
 finally{refreshControls()}
}
async function generate(){
 if(!engineIsLive()){notice('Este motor está disponível apenas para preparação: inferência local pesada não configurada.',true);return}
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
$('task').addEventListener('change',renderEngines);
$('engine').addEventListener('change',describeEngine);
$('selectionMode').addEventListener('change',applyMode);
$('targetCount').addEventListener('change',applyMode);
$('preserveScene').addEventListener('change',applyMode);
connect();
// Polling only queries local status. It never submits a render.
setInterval(()=>{if(connected&&['SUBMISSION_UNCERTAIN','SUBMITTED','PENDING'].includes(jobStatus))refresh()},5000);