# Furuya Motion Studio — Multipersonagem: demonstração e plano técnico

Data: 29/10/2026. Objetivo: **substituição integral de uma ou várias pessoas do mesmo vídeo**, mantendo referências individuais, coreografia, câmera, trilha e preservação das pessoas não selecionadas.

## Evidência fornecida pelo usuário (arquivo privado; não comitar no GitHub)

Vídeo demonstrativo com personagens representando figuras cinematográficas e vários dançarinos no mesmo ambiente noturno: MP4 H.264, **720 × 1280**, **30 FPS**, **24,133 s**, **724 frames** e áudio AAC. Foram amostrados quadros em 0,5–23 s e verificados vários personagens destacados participando da mesma sequência de rua, com oclusões e movimentação. O ambiente de festa apresenta construções, tenda, iluminação e multidão. Uma marca gráfica aparece na área central do vídeo.

**A demonstração não revela o workflow de geração:** não é prova de que as pessoas foram substituídas por um único modelo ou em um único passo; pode envolver múltiplas máscaras, rastreamento, fluxos regionais, edição temporal ou reconstrução de cena. O usuário enviou o vídeo para demonstrar a META de qualidade, não para afirmar a tecnologia usada.

## Referências tecnológicas atuais pesquisadas

1. [Openjutsu](https://github.com/D3voz/openjutsu), MIT (código, não necessariamente pesos): seu modo Advanced Motion Transfer documenta **1 a 4 personagens**, correspondência de identidades ao longo dos planos, tratamento de pessoas sem referência como intocadas e máscaras com SAM 3.1. Usa ComfyUI + MiniMax H3. O autor descreve teste em RTX 4060 Ti de 16 GB com 64 GB RAM. Não há comprovação de execução gratuita na nossa conta; integração ainda é candidata.
2. [Henge](https://github.com/alisson-anjos/Henge): relata demo de **dois personagens transformados simultaneamente** em cortes de câmera com SAM 3.1 e LoRAs próprios TARA/Guide Latents em MiniMax H3. Fluxo de região mascarada disponível, mas sem máscara o fundo original não é garantido. O autor usou RunPod Serverless; esse exemplo **não é gratuito**.
3. [SAM 3.1](https://ai.meta.com/blog/segment-anything-model-3/), atualização publicada pela Meta em 27/03/2026: suporta rastrear **até 16 objetos em uma passagem** por multiplexação. É **segmentação**, não geração temporal do personagem. Exige GPU/ambiente para inferência; não significa rastreamento instalado no Furuya.
4. [Wan2.1 VACE](https://comfy.org/workflows/video_wan_vace_inpainting-a1bb55d904c9/): pipeline regional de edição de vídeo com máscaras. É candidato para **múltiplas passagens controladas** e preservação do fundo; não comprovado como troca multipersonagem em um único render.
5. [Higgsfield Genjutsu](https://higgsfield.ai/creator-hub/help-center/tools/how-do-i-use-genjutsu): diferencia Motion Transfer (reconstrói a cena) de Objects Swap (edita elemento específico), suporta vídeo 4–30s, até 30 imagens de referência. **Serviço proprietário**: API/MCP/CLI usam créditos. Referência para design e benchmarking, não backend gratuito implícito.

## Arquitetura de processamento multipersonagem a construir

1. **Elenco e identidade:** usuários atribuem explicitamente uma referência canônica de personagem a cada pessoa selecionada no vídeo; pessoas não selecionadas devem permanecer originais.
2. **Anotações espaciais:** salvar bboxes normalizadas em vários timestamps (implementado em `multicast.html`). São âncoras, não máscaras inferidas e não garantem identidade.
3. **Segmentação temporária:** SAM3/3.1 ou SAM2 com IDs estáveis, prompts positivos/negativos, reidentificação após oclusão, correção de erros ao cruzar pessoas e verificação por quadros.
4. **Render por motor:** usar backend multipersonagem validado quando disponível (Openjutsu/Henge candidatos) ou composição de renderizações regionais com máscaras independentes; documentar estratégia e custo.
5. **Pós-processamento:** preservar fundo, trilha, contexto, sombras, oclusões e fidelidade visual de cada personagem, inclusive chifres, asas e roupas; não pintar o mesmo pixel de duas identidades simultaneamente sem regra de prioridade.
6. **Auditoria:** comparação com fonte/quadros, identidade por personagem e coerência temporal, largura do vídeo, duração, áudio, composição da multidão e deformações.

## Implementação desta etapa

- `cloud/engine_registry.py`: categoria `multi_scene_replacement` e candidatos **Openjutsu Advanced**, **Henge TARA** e **Wan VACE Masked**. Todos marcados `RESEARCH_ONLY`, sem submissão automática de GPU.
- `multicast.html` + `multicast.js`: módulo separado de planejamento com até **quatro personagens**, importação de vídeo e imagens locais, caixas por momento, exportação JSON; **zero rede**.
- `tools/validate_multicast_plan.py`: auditoria rigorosa de IDs, timestamps, caixas, nomes de referência e limites, mantendo `tracking_state=NOT_RUN`.
- `cloud/local_render_gateway.py`: lista motores multipersonagem via `GET /api/engines` e oferece visualizador offline; **não aceita render multipersonagem antes de existir backend validado**.
- Testes offline JavaScript/Python incluídos no CI, sem baixar pesos nem chamar serviços pagos.

## Critério de aceitação real

A interface não pode anunciar sucesso até possuir **MP4 realmente gerado** com N substituições corretas e estáveis, pessoas intactas, áudio/câmera preservados e rastreamento validado. Prioridade imediata: primeiro clipe de 3 segundos da Albedo no centro da festa; próximo passo: **dois personagens** no mesmo vídeo; depois três ou quatro. Orçamento adicional R$ 0 continua obrigatório; não utilizar RunPod pago.

Nota de licenciamento: código MIT dos projetos pesquisados não altera direitos autorais de pesos, LoRAs, materiais de cinema ou gravações de pessoas reais. Verificar condições antes de publicar/monetizar.
