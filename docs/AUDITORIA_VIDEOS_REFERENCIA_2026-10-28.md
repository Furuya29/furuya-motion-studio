# Auditoria comparativa dos seis vídeos enviados — Furuya Motion Studio
Data: 2026-10-28 · Evidência: inspeção de amostras visuais dos arquivos enviados pelo proprietário, metadados via ffprobe e pesquisa pública das interfaces observadas.

## Conclusão de projeto
**NÃO** insistir em ajustes incrementais no JSON MediaPipe v0.5 para reproduzir AI video recasting. O projeto precisa de uma rota primária VIDEO-FIRST, caracterizada por edição de vídeo condicionada por identidade visual (imagem de referência, keyframe editado, máscara e propagação temporal) e uma rota secundária MOTION-FIRST para rigs 2D controláveis. O compositor v0.6.1 é só um sprite overlay rígido, não a tecnologia vista nos exemplos.

## Evidência individual (material do usuário, não inferir ferramenta somente pelo resultado)
1. `1000585222.webm` — ~29,586 s, VP9 720×1280, exportação do próprio compositor v0.6.1. A personagem aparece sobre o vídeo original em alguns trechos iniciais, reduzida e reposicionada, sem articulação própria; por volta de 10–12 s deixa de aparecer na amostragem analisada, enquanto o dançarino real permanece e a câmera continua. O arquivo WebM de origem não anunciava duration em metadata e precisou ser decodificado/remuxado para obter 29,586 s: este é um problema de compatibilidade de contêiner separado. O algoritmo usa poses e IDs instáveis de JSON v0.5; vídeo não contém informação sobre a pessoa de origem nos trechos em que a pose foi perdida.
2. `1000585215.mp4` — 19,18 s, 576×1022, anime 2D com personagens em ambiente de festa, close-ups, corte de câmera e aproximadamente 3 s de tela final TikTok. Não é evidência de substituição rastreada de multidão real; é um clipe de sequência animada em múltiplas tomadas, marcado AI-generated.
3. `1000585214.mp4` — 205,125 s, 576×1024, longa narrativa/paródia cinematográfica com cenas, diálogos e diferentes planos; personagens de aparência de ícones de filmes de ação. Não é uma tomada contínua de 205 s nem prova tracking multi-pessoa por 205 s; pode ser editada/composta de muitos trechos curtos.
4. `1000585213.mp4` — 18,738 s, 576×1024, cena dentro de carro com duas pessoas em performances e movimentos de braços e objetos, cortes de câmera. É compatível com geração/edição visual ou troca de rostos, mas o vídeo sozinho não identifica qual ferramenta criou o efeito. Não é referência a uma multidão dançando.
5. `908fa2096fe2ae8d0d5dbed5d2679fb2.mp4` — 25,8 s, 576×1024, início mostra versões de dança em multidão; a partir de ~9 s mostra tutorial de smartphone, abrindo um template que se lê **THE WALKING STEP**, com botão textual **Usar o modelo no CapCut** e escolha de fotografia/referência. Isso prova fluxo de uso via MODELO, sem que o usuário exporte JSON de esqueleto. NÃO comprova que o algoritmo interno não use pose/face detection.
6. `b706d31a1ab274675f8619b04b229a44.mp4` — 26,567 s, 576×1024, primeiros ~10 s apresentam duas versões da mesma situação de multidão na tela dividida (recasting/comparação visual); depois mostra iPhone e tela de aplicativo **PixVerse Lite**, inclusive permissão de colar de TikTok, navegação de modelos, prévia de template, escolha de fotografia para criar e preço de **135 créditos na tela do botão Criar**. É demonstração de fluxo baseado em **template + foto**; não fornece algoritmo interno nem evidência de operação gratuita ilimitada.

### Fontes públicas consultadas para validação das interfaces
- Página App Store PixVerse Lite, capacidades: templates de dança, imagens/refs, image-to-video, motion control: https://apps.apple.com/br/app/pixverse-lite/id6767802142
- Documentação PixVerse Motion Control/Mimic: https://docs.platform.pixverse.ai/how-to-use-mimic-1982936m0 ; sua API requer assinatura/créditos, portanto NÃO considerar caminho livre na arquitetura.
- Funcionalidades PixVerse Swap/Modify/Restyle: https://docs.platform.pixverse.ai/model-overview-2140345m0
- Runway Aleph 2.0, fluxo vídeo+keyframe editado com máscara: https://dev.runway.com/learn/edit-and-finish-video-api

## Decisão arquitetural
### A. VIDEO-FIRST (rota principal de substituição visual)
- Arquivo de vídeo base + imagens canônicas dos personagens + frames-chave selecionáveis + máscaras por personagem.
- Modo de autoria de frames: substituir visualmente a pessoa escolhida no quadro-chave, sem alegar que isso por si só propaga a edição.
- Track de aparência/máscara e correções manuais para multidões; usar modelos de edição temporal em segmentos de 3–8 s quando houver GPU realmente disponível.
- Compor segmentos e verificar que rosto, roupas, acessórios, estilo e silhueta permanecem estáveis.
- Preservar original e exportar um relatório das áreas editadas e frames sem certeza.

### B. MOTION-FIRST (rota secundária)
- MediaPipe/RTMPose para controle de rigs e medidas auditáveis; skeleton JSON não é requisito para rota A.
- Para imagem 2D inteira, movimento de sprite rígido não é animação corporal; precisará de rig/articulação por camadas e reconstrução manual/IA das juntas ocultas.
- Trocas de IDs e oclusão não devem resultar em troca silenciosa de personagem.

## MVP v0.7 proposto
1. Painel vídeo-original + imagem original do personagem + escolha de pessoa no quadro.
2. A pessoa é marcada por máscara editável, não só por pose.
3. Compositor de **quadros-chave editados** (um ou múltiplos) e trilha de máscaras/identidade observável.
4. Exportar sequência de keyframes e instruções condicionantes para modelo de vídeo **externo opcional**; não prometer renderizar vídeo generativo com GPU do Redmi.
5. Módulo para encaixar modelos locais quando PC/GPU realmente suportar; PC Remote Agent ainda não validado.
6. Benchmark com a dança 29,58s e outros exemplos; diferença entre _medido_, _estimado_ e _gerado_ sempre registrada.

## Resultados reais vs hipótese
- **Observado diretamente:** PixVerse Lite, template CapCut, recortes e cortes de cenas, perda do personagem em nosso WebM.
- **Inferência plausível:** templates com image-to-video e video-to-video recasting, possível face swap, inpainting e propagação temporal. Não é possível atribuir arquiteturas, modelo específico ou qualidade perfeita somente pelas imagens.
- **Viabilidade:** modelos proprietários podem ser pagos; caminhos abertos exigem hardware ou otimizações ainda não demonstradas. Não dizer que substituição de múltiplos personagens 2D em multidão está pronta.
