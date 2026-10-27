# Furuya Motion Studio — Pesquisa técnica e decisão arquitetural
Data: 2026-10-27 · Status: investigação e desenho de v0.6, não implementação

## Objetivo do produto
Animar personagens 2D/anime visualmente reconhecíveis a partir de vídeo real de dança, com múltiplos dançarinos, oclusões, corpos incompletos, câmera móvel, velocidade e fidelidade de identidade/proporções. Priorizar execução gratuita/local, Android Redmi K70 Ultra, PC legado; geração pesada deve ser opcional, não requisito.

## Evidência empírica v0.5 (arquivo fornecido pelo proprietário)
Fonte: `1000584780_motion (4).json`. Vídeo 29.583 s, 2160×3840, 4 amostras/s, modelo Lite, 119 quadros.
`targetStats`: found 31, missing 78, unassigned 82, fallbackFrames 81; 7 quadros repetidos; 27 poses boa e 97 parcial (essas contagens NÃO equivalem à quantidade de quadros).
Primeira referência manual: 2.447 s. Última associação ao alvo: 11.5 s. Entre 13–19.75 s houve 28/28 quadros com ao menos uma detecção bruta, MAS zero associações ao alvo; entre 20–29.5 s houve 34/39 quadros com detecções brutas e zero associações.
Conclusão: a recuperação full-frame da v0.5 impediu o desaparecimento das detecções, mas não resolveu identidade persistente. Oito IDs de trilha diferentes foram marcados `selected=true`. Uma associação provável não comprova que seja a pessoa correta. Não alegar rastreamento estável.

## Pesquisa primária (2026)

### Viggle JST-2 (proprietário)
Lançamento 2026-10-19: modelo espacial `physics-native` com representação 3D de elementos persistentes, características e dinâmicas aprendidas. O sistema de movimento infere partes invisíveis com aprendizado de dinâmica. **Importante**: isso é reconstrução plausível, não medição real do que está oculto. A própria equipe documenta erros em movimento rápido, contato com solo e proporções incomuns.
Fontes:
- https://viggle.ai/jst2
- https://viggle.ai/research/jst2-motion
- https://viggle.ai/research/jst2-character

### Viggle-Animate (pesos abertos, NÃO idêntico à tecnologia proprietária JST-2/V4)
Modelo de substituição de personagem no vídeo, lançado pela Viggle em 2026-09. Recebe um vídeo e UM quadro retirado desse vídeo, previamente repintado com o personagem desejado. A etapa de renderização temporal NÃO requer pose extractor, detector de máscara, face tracker ou texto. Codifica vídeo diretamente e condiciona na aparência alinhada ao mesmo quadro. Implementação publicada: finetune de 33.1 bilhões de parâmetros sobre MiniMax H3; LoRA distilada com DMD; 124 quadros 24 fps 480×832 em 26 s em uma NVIDIA B200 (benchmark dos próprios autores, não reproduzido aqui).
Atenção: pesos no Hugging Face ~69 GB. BF16 para 124 quadros 480×832 consome pico ~80.1 GiB; documentação exige ≥96 GB GPU para uso sem offload; modo quantizado RTX 5090 32 GB foi anunciado mas NÃO entregue no repositório. CPU offload possível com grande penalidade de tempo e RAM.
Limitações documentadas: múltiplos personagens, cortes e contato físico diminuem fidelidade; corpo com geometria incompatível tende a conservar a topologia do vídeo; detalhes não visíveis em frame-referência não são garantidos; lip-sync fraco. Licença dos pesos MiniMax-H3 Community; código Apache-2.0. Verificar licença antes de distribuir o aplicativo.
Fontes:
- https://viggle.ai/research/viggle-animate-character-replacement-from-a-repainted-frame
- https://huggingface.co/Viggle/Viggle-Animate
- https://viggle.ai/developers

### PixVerse Motion Control/Mimic (proprietário)
Documenta vídeo motor + imagem de personagem, preservação de ritmo e renderização consistente. Não publica arquitetura interna reproduzível. Recomenda indivíduo como foco claro; portanto não declara resolver multidões arbitrárias. Requer créditos para API. Não assumir que sua operação usa os mesmos módulos do Viggle.
Fonte:
- https://docs.platform.pixverse.ai/how-to-use-mimic-1982936m0

### Wan2.2 Animate 14B (pesos abertos, GPU pesada)
Pipeline explícito de pose, rosto, máscaras e fundo antes da geração; modo animação e substituição. Não cabe no orçamento local atual. Usar como opção futura de export/render na nuvem, somente se recurso livre estiver efetivamente disponível.
Fonte: https://github.com/Wan-Video/Wan2.2

### SAM 2.1 (máscaras com memória temporal)
Modelo Meta para segmentar e seguir um objeto selecionado ao longo do vídeo com memória de aparências e prompts/correções. Tamanho tiny 38.9M parâmetros, versão Python/PyTorch (não equivale a solução pronta em navegador Android). Permite associação por máscara e contexto visual, muito mais informativa do que centro dos ombros; usar como referência para a arquitetura de tracking. Não prometer que resolve todas as oclusões.
Fonte: https://github.com/facebookresearch/sam2

### RTMPose / RTMW (multi-person)
Detectar pessoas antes de estimar keypoints por recorte individual é uma arquitetura top-down. RTMPose tem ONNX/ncnn publicados, RTMW estende para face/mãos/corpo. Requer protótipo de compatibilidade WebGPU/ONNX Runtime Web ou motor Android nativo; desempenho no Redmi desconhecido.
Fontes:
- https://github.com/open-mmlab/mmpose
- https://arxiv.org/abs/2407.08634

### Rastreadores multi-objeto
ByteTrack, DeepSORT e BoT-SORT aplicam associação de bounding boxes e/ou características visuais. Adicionar trilhas temporais com custo de associação e um estado `unassigned` honesto; avaliar reversão temporal e correções pontuais. Material de referência:
- https://github.com/open-mmlab/mmtracking

### MimicMotion (video diffusion com sinal de pose)
Referência histórica útil do mecanismo de pose guiada e confiança: mínimo 8 GB VRAM modelo 16 quadros, mas VAE tipicamente 16 GB; execução completa não é realista no celular atual.
Fonte: https://github.com/Tencent/MimicMotion

## Decisão para Furuya Motion Studio
**Não continuar tratando esqueleto MediaPipe de quadro isolado como motor completo da animação.** Separar percepção (quem é quem), recuperação de movimento (visível/inferido), identidade do personagem (canônico), e síntese (determinística leve vs IA generativa pesada).

Duas rotas complementares:
A. LOCAL/LIVRE: decodificação em resolução de análise; detector de pessoas; trilhas com caixas+recortes+aparência/máscara; pose por indivíduo; correção temporal bidirecional; articulações ocultas marcadas como `inferred` com incerteza; retarget para rig 2D com proporções fixas; WebGL/WebGPU/Canvas; exportar a 24/30 fps a partir de keyframes e interpolação.
B. OPCIONAL GPU: recriar um quadro do vídeo com o personagem anime (preservar pose, cenário, luz, enquadramento), e propagar a edição ao vídeo com modelo image/video-conditioned (p.ex. Viggle-Animate aberto ou Wan Animate); render em tomadas menores; não confundir com a rota offline e não depender de GPU ilimitada grátis.

## Projeto v0.6 — trabalho proposto, ainda não implementado
1. Criar `TrackId` separado de `PoseId`: objetivo reconhecível por área de roupa, aparência e máscara, não pelo ID de MediaPipe. Incluir estado `tracked`, `occluded`, `lost`, `reidentified` e `unassigned`.
2. Implementar memória temporal: preservar keyframes de recortes visuais, aparência histograma/embedding leve; associação com deslocamento, IoU e coerência do corpo; busca full-frame se perdido.
3. Análise não-causal em duas passagens (frente e trás); propagar marcações de múltiplas referências manuais para preencher lacunas, preservando incerteza.
4. Separar `visible_pose` de `inferred_pose`; não preencher pernas ocultas como se fossem medições. Regras anatômicas e biblioteca de danças opcionais para movimento plausível, auditável.
5. Novo modo `image-first`: editar frame da gravação e aplicar a mesma substituição visual em segmento, inicialmente criar storyboard sem prometer render local generativo.
6. Definir testes com vídeos desafiadores e vídeos controlados com pessoa visível; medir `target_coverage`, `identity_switches`, `keypoint_jitter`, % `inferred`, continuidade e fidelidade visual. Validar em Android e registrar consumo de RAM/energia/tempo.

## Métricas e critérios de saída
- Cobertura do alvo = quadros corretamente atribuídos ao mesmo indivíduo/quadros avaliáveis (exige inspeção, não é apenas `targetFound`).
- Trocas de identidade auditadas visualmente por clipe.
- Movimento visível e inferido rotulado distintamente.
- Fidelidade do personagem: face, cores, roupas, cabelo, proporções, acessórios e silhueta quadro a quadro.
- Progresso não medido por quantidade de IDs nem número de articulações previstas fora da tela.

## Restrições permanentes
Sem assinaturas pagas, sem dependência obrigatória de API, sem prometer execução de 33B na GPU do Redmi, sem prometer equivalência do modelo aberto ao JST-2/V4 proprietário. Dados de vídeo locais na rota A; qualquer futura rota remota deve informar o envio. Respeitar permissões e licenças das fontes e do vídeo.
