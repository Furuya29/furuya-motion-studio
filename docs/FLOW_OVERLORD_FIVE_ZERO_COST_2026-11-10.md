# P0 — Google Flow gratuito: Albedo + Shalltear + Solution + Lupusregina + Narberal

**Data:** 10/11/2026. **Custo financeiro adicional:** R$ 0. **Estado:** pacote de mídia e código de preparação concluídos; geração generativa em Flow ainda **NÃO EXECUTADA**.

## Demanda concreta

Editar o vídeo vertical original da festa noturna (24,255 segundos, 720×1280, 30 FPS, áudio original) substituindo **até cinco dançarinos** por:
1. Albedo, referência 3D **já inserida na cena pelo usuário**, mantendo chifres brancos, asas negras, cabelo preto, olhos dourados e vestido branco/dourado;
2. Shalltear Bloodfallen, vestido gótico bordô/preto, cabelos prateados e olhos vermelhos;
3. Solution Epsilon, longos cabelos verdes e uniforme de empregada de batalha;
4. Lupusregina Beta, cabelos vermelhos, traje de empregada e expressão provocadora;
5. Narberal Gamma (Nabe), cabelos pretos e traje de empregada.

Estética: **3D semi-realista** integrada ao vídeo original. Não usar composição de PNG rígida. Alterar **somente dançarinos selecionados**, preservando espectadores, cenário, som e câmera. As identidades secundárias ficam como **propostas não verificadas** — o vídeo tem grande aglomeração e o rastreamento ainda não foi executado.

## Implementação no repositório

- `flow.html` + `flow.js`: novo modo no aplicativo para escolher vídeo e até cinco imagens, calcular custo de créditos gratuitos, gerar e copiar prompt, exportar `flow_job.json` e abrir o Google Flow. **Não tenta fazer upload nem gerar pela API**; não existe backend de execução Flow validado no Furuya.
- `cloud/flow_free_adapter.py`: preparador offline, com FFprobe/FFmpeg e arquivos locais. Não precisa de GPU. Segmenta o MP4 original em trechos menores que 10 segundos, preserva áudio e referências, cria `flow_prompt.txt` e `flow_job.json`, além de um piloto de três segundos. Impede sobrescrita, mostra orçamento e rejeita piloto acima do saldo gratuito informado.
- `routing-policy.json` e `cloud/auto_router.py`: Flow é a **primeira rota de avaliação** para edição preservando cena, especialmente **cinco personagens**, caso em que não oferece erroneamente Openjutsu de até quatro personagens.
- `cloud/engine_registry.py` e `engine-catalog.json`: o Flow entra como décimo primeiro motor catalogado, sem remover os dez anteriores.
- `generate.html`: oferece acesso evidente ao novo modo Flow.
- Testes Python reais de divisão FFmpeg e smoke de JavaScript: execução offline, nenhum crédito debitado.

## Arquivos reais já preparados

O pacote da sessão foi salvo em `Furuya_Flow_Overlord_5_Personagens_Inputs.zip` e contém:
- `01_piloto_3s.mp4` — teste original com áudio;
- `cena_01_00_08s.mp4`, `cena_02_08_16s.mp4` e `cena_03_16_24s.mp4` — cortes que cobrem o vídeo original (último segmento inclui fração de segundo final);
- cinco JPGs compactados com identidade visual individual;
- `personagens_5_referencias_visuais.jpg` — guia para conferência;
- `scene_original_frame_00.png` — referência do cenário original;
- `flow_prompt_5_personagens.txt` e `flow_job.json` — tarefa preparada.

**Esses arquivos NÃO são um MP4 generativo editado.** São entradas para a geração no Flow.

## Execução sem cobrar

O Google Flow documenta edições em vídeos enviados (modelo **Omni Flash 1.2**); na modalidade sem assinatura, no máximo **10 segundos por trecho**. Fontes oficiais:
- https://support.google.com/flow/answer/16935718
- https://support.google.com/flow/answer/16353334
- https://support.google.com/flow/answer/16526234

O custo documentado é de **1 crédito/segundo em 360p e 3 créditos/segundo em 720p** (sujeito a mudanças). O piloto de 3 segundos é estimado em 3 créditos em 360p; os trechos completos, aproximadamente 25 créditos em 360p adicionais ao piloto. A quantidade efetivamente gratuita disponível deve ser consultada **dentro da conta do Google Flow**, não presumida. O Furuya não tem API pública/autorizada para consultar saldo ou controlar render via site por esta integração.

**Para executar o vídeo generativo real** é preciso uma sessão autenticada do Google Flow com saldo gratuito elegível. Abrir `flow.html` e conferir os cinco insumos, então editar o vídeo pelo site Flow usando referências/ingredients e um prompt. Um clique em Gerar no próprio Google Flow poderá consumir créditos gratuitos da conta; se oferecer apenas créditos pagos, interromper.

## Bloqueios reais neste teste

- O canal anterior do navegador Opera GX via CDP (porta 55870) **não estava disponível** no PC autorizado na inspeção de 10/11/2026. A conexão PCRA exposta à conversa aceita apenas comandos sintéticos, não execução do navegador. Não foi possível enviar os arquivos para Flow nem recuperar um MP4 generativo.
- O Flow gratuito não garante manter cinco identidades separadas numa multidão; testar primeiro 3 s e revisar o resultado quadro a quadro.
- Quatro personagens secundárias podem estar parcialmente fora de quadro. Não inventar participantes novos para atingir cinco simultâneos. Para melhor qualidade, fazer edições por trechos e somente alvos presentes; caso falhe, preservar as pessoas originais e reduzir o número de alvos numa única geração.

## Próximo marco de produção

Restabelecer uma sessão Google Flow operacional autorizada e com créditos realmente gratuitos, transferir o pacote de insumos, gerar **uma tentativa de 3 s**, baixar o MP4 e avaliar corpo inteiro, cabelo, asas, roupas, dança, multidão e som. Depois avançar para 24,255 s divididos, sem gasto.
