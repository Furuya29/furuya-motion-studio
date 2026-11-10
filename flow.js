"use strict";
/* Google Flow free-tier helper. No provider API or charge. */
const $ = id => document.getElementById(id);
const names=["Albedo","Shalltear Bloodfallen","Solution Epsilon","Lupusregina Beta","Narberal Gamma (Nabe)"];
const targets=[
 "foreground center dancer wearing a blue denim shirt",
 "explicitly selected dancer in the left-side crowd",
 "explicitly selected dancer behind-left of the main foreground person",
 "dancer in grey shirt and dark cap on the right when visible",
 "dancer with sunglasses behind-right of the foreground person"
];
const identity=[
 "long black hair, curved white horns, large black feathered wings, gold eyes, ornate white-and-gold dress",
 "silver hair, red eyes, dark burgundy-and-black gothic aristocratic gown",
 "long green hair, gold eyes, fitted black-and-white battle-maid attire",
 "long red braided hair, mischievous smile, black-and-white battle-maid attire",
 "long straight black hair, composed face, elegant black-and-white battle-maid uniform"
];
let latestJob=null;
function state(str){$("status").textContent=str}
function getBudget(){
 const seconds=Number($("seconds").value);
 const res=Number($("resolution").value);
 const balance=Number($("balance").value);
 if(!Number.isFinite(seconds)||seconds<.5||seconds>10)throw Error("O Flow gratuito só permite escolher trechos de 0,5 a 10 segundos.");
 if(![360,720].includes(res))throw Error("Resolução não reconhecida.");
 if(!Number.isInteger(balance)||balance<0)throw Error("Informe a cota gratuita real da conta.");
 const cost=Math.ceil(seconds*(res===360?1:3));
 return {seconds,res,balance,cost};
}
function updateCost(){
 try{
  const b=getBudget();
  $("cost").textContent="Estimativa: "+b.cost+" crédito(s) para "+b.seconds+"s a "+b.res+"p; cota informada: "+b.balance+"."+
    (b.cost>b.balance?" Sem saldo gratuito: geração deve permanecer bloqueada.":"");
 }catch(e){$("cost").textContent=e.message}
}
function makePrompt(n){
 const lines=[
 "Edit the UPLOADED original street-party video, not a new imaginary dance.",
 "Full body 3D-anime character replacement. Keep the exact choreography,",
 "handheld camera motion, audio, lights, crowd, buildings and all unselected",
 "people unchanged. Never produce simple static stickers or a face-only swap.",
 "Reference mappings; do not exchange identities:",
 ];
 for(let i=0;i<n;i++)lines.push(
  (i+1)+". "+names[i]+": replace the "+targets[i]+"; appearance: "+identity[i]+"."
 );
 lines.push(
  "All replacements should share semi-realistic 3D visual quality consistent",
  "with real street-light illumination, physically plausible hair/clothing,",
  "and correct occlusion when spectators pass in front of the characters.",
  "When a target leaves the frame, do not invent another body. Never create",
  "additional copies or alter non-selected dancers. Preserve background.",
  "Prioritize Albedo if the model cannot reliably track every chosen person.",
  "Keep vertical 9:16 framing and exactly the uploaded excerpt duration."
 );
 return lines.join("\n");
}
function prepare(){
 try{
  const budget=getBudget();
  if(budget.cost>budget.balance)throw Error("Saldo informado insuficiente. O Furuya nunca compra créditos.");
  const n=Number($("targets").value);
  const source=$("source").files[0];
  if(!source||!(/\.(mp4|mov)$/i.test(source.name)))throw Error("Selecione o vídeo MP4/MOV original.");
  const refs=[];
  for(let i=1;i<=n;i++){
   const file=$("ref"+i).files[0];
   if(!file||!(/^image\//.test(file.type)))throw Error("Falta imagem da personagem "+i+": "+names[i-1]);
   refs.push({character:names[i-1],reference_file:file.name,target:targets[i-1]});
  }
  const prompt=makePrompt(n);
  $("prompt").value=prompt;
  latestJob={
   schema:"furuya-flow-free-job/1",source_video:source.name,
   reference_images:refs,target_count:n,style:"semi_real_3d",
   task:"video_to_video_character_replacement",
   engine:"flow_omni_flash_1_2",source_preservation_required:true,
   clip_seconds:budget.seconds,resolution:budget.res,
   expected_credits:budget.cost,claimed_free_balance:budget.balance,
   credits_checked_live:false,actual_free_cost_verified:false,
   upload_status:"NOT_UPLOADED",render_status:"NOT_RENDERED",
   manual_upload_required:true,
   never_auto_purchase:true,prompt,
  };
  $("copy").disabled=false;$("export").disabled=false;
  state("Prompt e manifesto preparados, sem consumo. Abra Flow, confira sua cota GRATUITA, envie o vídeo e as imagens correspondentes, cole o prompt e inicie UMA geração. Não há envio automático pela página.");
 }catch(e){latestJob=null;$("copy").disabled=true;$("export").disabled=true;state("Preparação bloqueada: "+e.message)}
}
async function copyPrompt(){
 const text=$("prompt").value;
 try{await navigator.clipboard.writeText(text);state("Prompt copiado. Nenhuma geração iniciada.")}
 catch{ $("prompt").select();document.execCommand("copy");state("Prompt selecionado para cópia.")}
}
function downloadJob(){
 if(!latestJob)return;
 const blob=new Blob([JSON.stringify(latestJob,null,2)],{type:"application/json"});
 const url=URL.createObjectURL(blob);
 const anchor=document.createElement("a");
 anchor.href=url;anchor.download="flow_job.json";document.body.append(anchor);anchor.click();anchor.remove();
 URL.revokeObjectURL(url);
}
for(const name of ["seconds","resolution","balance"])$(name).addEventListener("input",updateCost);
$("prepare").addEventListener("click",prepare);
$("copy").addEventListener("click",copyPrompt);
$("export").addEventListener("click",downloadJob);
updateCost();
