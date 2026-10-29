# P0: conectores reais de execução e máscaras temporais

Data: 29/10/2026. Status: **ponte ComfyUI com protocolo HTTP implementado; nenhuma inferência de vídeo real validada**.

## O que é novo

1. **cloud/comfyui_local_bridge.py** conecta a instância ComfyUI local existente usando os endpoints oficiais **GET /object_info**, **POST /prompt**, **GET /history/{prompt_id}** e **GET /view**. Ele valida nós, associa arquivo de personagem e vídeo de entrada a IDs de nós fornecidos no workflow, executa uma única submissão autorizada, acompanha o resultado e salva o MP4 obtido. Não usa API comercial.
2. **tools/export_temporal_boxes.py** transforma um `furuya-multicast-plan/1` exportado pelo planejador de até quatro pessoas em sequências PNG monocromáticas indexadas por personagem e por frame. Os retângulos são **propostas espaciais interpoladas, não máscaras SAM**. Só interpola entre âncoras explicitamente marcadas; fora delas grava imagens pretas. Uma única âncora gera caixa apenas no frame correspondente.
3. Testes usam um **servidor ComfyUI sintético** na interface 127.0.0.1, sem modelos ou GPU, para comprovar a comunicação e o bloqueio contra envios duplicados. Um MP4 sintético válido apenas pela assinatura do contêiner não comprova vídeo gerado por IA.

## Protocolo e restrições

A ponte de geração **não fornece nem instala um workflow de qualquer modelo**. É necessário um ComfyUI já instalado com as dependências, os pesos do motor e um fluxo de vídeo compatível exportado em formato **API**. A ferramenta não pode criar esse grafo do zero porque cada motor usa nós, checkpoints, LoRAs e entradas distintos.

**Não considera 'ComfyUI conectado' como garantia de geração.** Os nós presentes e os requisitos de hardware podem ser insuficientes; também é necessário testar o processamento do vídeo e auditar o resultado.

**Segurança:** aceita somente `http://127.0.0.1:PORT` ou `http://localhost:PORT`; no momento não controla ComfyUI hospedado em outras máquinas. Não abre a porta para a internet. Sem instalações automáticas, sem gastos ou chamadas para provedores externos. O código não guarda segredos. Só envia um `POST /prompt` após `--execute --confirm-free-gpu`; cria recibo antes do POST, recusando uma segunda execução se houver incerteza.

## Como executar um workflow previamente instalado no PC ou ambiente GPU gratuito

Requer Python 3.10+ e o checkout atualizado do Furuya. ComfyUI deve estar executando em 127.0.0.1:8188, usando um workflow de vídeo exportado em API Format com nó capaz de **carregar um MP4** e outro de **carregar a imagem da personagem**. Para localizar os IDs, examine as chaves numéricas e o campo `class_type` do JSON exportado.

Exemplo ilustrativo de linha de comando (os IDs e caminhos **não são universais**, substitua pelos reais do workflow):

```powershell
python cloud/comfyui_local_bridge.py `
  --workflow 'E:\ComfyUI\workflows\viral-api.json' `
  --server 'http://127.0.0.1:8188' `
  --input-dir 'E:\ComfyUI\input' `
  --video 'E:\Furuya\driving.mp4' `
  --image 'E:\Furuya\Albedo_original.png' `
  --video-node 11 --video-field video `
  --image-node 12 --image-field image `
  --output 'E:\Furuya\albedo_rio_generated.mp4'
```

O comando acima é **dry-run**: não envia nem gera nada, apenas valida a forma do workflow, arquivos e destino. No momento de execução, usar `--execute --confirm-free-gpu` **somente** depois de verificar que a instância realmente possui GPU gratuita apropriada e todos os pesos. ComfyUI aceita a tarefa uma vez; o recibo impede repetir submissões após timeout. A ferramenta não pode recuperar automaticamente jobs com recibo incerto; a recuperação do `prompt_id` precisa ser verificada no ComfyUI. 

A ponte registra o arquivo recebido do ComfyUI como `RENDERED_UNREVIEWED` (necessário executar `ffprobe` e auditoria visual antes de tratar como vídeo válido). A aprovação final deve ser feita com `tools/audit_generated_video.py` e inspeção humana da personagem, multidão, oclusões e 72 frames.

## Máscaras temporais: exportar rascunhos, não dados definitivos

O módulo `multicast.html` exporta `furuya-multicast-plan.json` depois de selecionar até 4 pessoas, carregar referências e marcar caixas em alguns momentos. Exporte as propostas:

```powershell
python tools/export_temporal_boxes.py --plan .\furuya-multicast-plan.json --output-dir .\furuya-temporal-boxes --fps 24
```

A ferramenta cria `furuya-temporal-boxes/<target_id>/frame_00000.png` etc. e `proposals-index.json`. Corrija manualmente as regiões e use as caixas para iniciar o rastreamento no SAM3/SAM2. **NÃO use retângulos como máscaras finais de cabelo, asas, corpo ou cenário**, nem suponha identidade preservada nos cruzamentos de pessoas. O exportador não extrapola caixas para frames sem evidência para evitar criar falsa precisão.

## Próxima tarefa indispensável para o vídeo da festa no Rio

- Disponibilizar um workflow **real** de Openjutsu/Henge ou Wan VACE (com os nós e pesos corretamente instalados) em GPU gratuita validada.
- Importar o plano de elenco, produzir tracking multi-ID e máscaras segmentadas por frame. Corrigir manualmente o risco de troca de IDs da multidão.
- Configurar o mapeamento de entradas no ComfyUI; aplicar modelos e gerar um MP4 genuíno; comparar cada quadro.
- Só então anunciar "geração dentro do Furuya" concluída.

Referência oficial da API ComfyUI: https://docs.comfy.org/development/comfyui-server/comms_routes
Referência oficial SAM 3.1: https://ai.meta.com/blog/segment-anything-model-3/
