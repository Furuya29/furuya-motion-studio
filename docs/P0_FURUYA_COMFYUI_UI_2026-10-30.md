# Furuya Motion Studio — geração Openjutsu diretamente pelo aplicativo

Atualizado em 30/10/2026. Integração da PR #7.

## O que esta versão implementa

A página `generate.html` agora possui o módulo **Openjutsu / ComfyUI**, independente do serviço opcional Viggle. O usuário escolhe o vídeo viral, uma a quatro imagens originais e descrições das pessoas do vídeo que deseja substituir. O Furuya abre um workflow Openjutsu Advanced (copiado sob licença MIT), ajusta automaticamente os nós para 1–4 personagens, salva um job local e oferece botões de **Verificar, Preparar, Gerar, Atualizar e Retomar**.

O módulo trabalha diretamente com **ComfyUI instalado pelo usuário**, através do mesmo gateway local Furuya (não envia mídia ao GitHub). A geração **não exige uma chave Viggle**. Porém, os nós, modelos e GPU do Openjutsu precisam existir no ambiente ComfyUI; esta mudança NÃO instala pesos nem provisiona GPU gratuita.

### Arquivos integrados

- `cloud/comfyui_web_jobs.py`: sessões e recibos independentes dos jobs Viggle; preparo local, verificação de classes, envio único de `/prompt`, consulta de `/history`, recebimento de vídeo por `/view`, recuperação apenas via GET
- `workflows/openjutsu_advanced.api.json`: workflow original do Openjutsu Advanced obtido do projeto D3voz/openjutsu em 29/10/2026; `workflows/OPENJUTSU_LICENSE.txt` conserva a licença MIT (a licença do código **não** garante direitos sobre os pesos MiniMax H3/SAM)
- `comfy.js` e `generate.html`: fluxo na interface Furuya sem repetir comandos para cada render
- `cloud/local_render_gateway.py`: endpoints `/api/comfy/status`, `/api/comfy/check`, `/api/comfy/prepare`, `/api/comfy/start`, `/api/comfy/resume`, `/api/comfy/result`
- `tests/test_comfy_web_jobs.py`: testes com servidor HTTP simulado, **sem executar modelos**
- O gateway original Viggle e os outros motores permanecem disponíveis, mas não são usados nessa rota.

## Configuração inicial, necessária uma vez no PC

Exige Python 3.10+, `ffprobe` instalado, checkout atualizado e ComfyUI rodando localmente em `127.0.0.1:8188`, com a pasta `ComfyUI/input` do mesmo processo e os custom nodes/modelos Openjutsu. A GPU atual de 8 GB do usuário **não foi qualificada** para esse pipeline; usar outra GPU existente e gratuita compatível, se disponível.

No Windows PowerShell a partir da pasta Furuya:

```powershell
python cloud/local_render_gateway.py --port 8765 --comfy-server "http://127.0.0.1:8188" --comfy-input-dir "E:\\ComfyUI\\input" --workdir "local-render-jobs"
```

**Atenção:** `E:\ComfyUI\input` é exemplo, substitua pelo caminho existente. Não inventar que ComfyUI já está instalado. Não existe serviço de GPU gratuito configurado automaticamente.

Depois, abra no **mesmo PC**: http://127.0.0.1:8765/generate.html

Fluxo normal do aplicativo:

1. Escolher vídeo MP4 (nesta rota até 30 s, limitados às capacidades do workflow) e primeira personagem original.
2. Informar quantidade de pessoas (1 a 4), anexar imagens adicionais e escrever identificadores visuais das **pessoas originais**, por exemplo `the central dancer in a beige shirt` ou `the dancer on the left`. Isso ajuda o modelo a não substituir a pessoa errada, mas **não garante** o alvo.
3. O workflow Openjutsu Advanced é carregado automaticamente do código do projeto; outro JSON de formato API pode ser selecionado manualmente se necessário.
4. Verificar conexão ComfyUI e os nós essenciais. Pressionar **Preparar** não consome GPU nem créditos, apenas salva arquivos localmente.
5. Confirmar que o ComfyUI realmente possui os pesos e GPU gratuita antes de marcar a autorização e clicar em **Gerar**. O Furuya faz **uma** submissão.
6. Acompanhar a execução na página. Se houver `prompt_id`, poderá retomar consultas **sem reenviar** o processamento. Se o POST falhar sem ID, o estado é `SUBMISSION_UNCERTAIN` e **não pode ser enviado de novo automaticamente**.
7. Se o workflow devolver um MP4/WebM via histórico e o FFprobe confirmar contêiner/duração, a tela permitirá visualização e download. O status será `RENDERED_UNREVIEWED`, **não** qualidade aprovada.

## Limitações e segurança

- **O site GitHub Pages sozinho não gera vídeos.** O gateway roda em 127.0.0.1 e precisa de ComfyUI e GPU; celulares sem conexão autorizada a esse backend só poderão visualizar a interface estática.
- A verificação de `/object_info` identifica classes de nós, não comprova pesos, capacidade de VRAM ou sucesso de inferência. A tela informa isso.
- O workflow Openjutsu Advanced pode falhar ou usar várias etapas. Uma tentativa do usuário não deve ser confundida com geração aprovada.
- A interface não faz rastreamento multi-ID por conta própria, e não transforma caixas de bounding-box em máscaras SAM automaticamente. Isso depende do próprio workflow ou de um pipeline futuro.
- Um vídeo recebido pode representar exportação/cópia, sem substituição. É necessária auditoria visual e comparação com a fonte antes de afirmar sucesso.
- Segurança local: servidor e ComfyUI apenas em loopback, `X-Furuya-Intent` nas rotas de mudança de estado e confirmação explícita `X-Furuya-Confirm: AUTHORIZE_LOCAL_GPU` para submeter.
- Recibos ficam em `local-render-jobs/comfy-jobs/job-*/receipt.json`. A rota não usa créditos Viggle, não abre plano pago e não provisiona GPU.
- Restrição P0 de upload: 48 MB totais, vídeo até 25 MB, até quatro imagens de 12 MB cada e workflow de até 2 MB. O limite concreto do modelo pode ser menor.

## Próximo marco

Conectar uma instância ComfyUI real, verificar os nós MiniMax H3 / Openjutsu / SAM3.1, confrontar os recursos disponíveis e executar o primeiro vídeo Albedo/Rio. **Nenhum MP4 final de IA foi gerado nesta PR.** A preferência do projeto permanece orçamento R$0.
