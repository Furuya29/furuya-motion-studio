# Furuya Motion Studio — captura v0.5 + compositor 2D v0.6

## Diagnóstico de compatibilidade Openjutsu — 31/10/2026

A integração Furuya agora faz uma **pré-verificação somente de leitura**, inclusive do workflow realmente preparado. Antes de permitir geração Openjutsu, analisa todos os nós, nomes dos checkpoints listados pelo ComfyUI e GPU/RAM, confrontando-os com o ambiente testado pelo projeto upstream (16 GiB VRAM, 64 GiB RAM). **Não comprova pesos íntegros nem garante inferência.** A implementação e os limites de nuvens gratuitas estão em [docs/P0_FREE_GPU_OPENJUTSU_READINESS_2026-10-31.md](docs/P0_FREE_GPU_OPENJUTSU_READINESS_2026-10-31.md). Em caso de componentes ausentes ou recursos inferiores, o botão de geração é bloqueado para evitar execução incompatível.

---

## Atualização: botão Openjutsu/ComfyUI dentro do Furuya (30/10/2026)

A tela `generate.html` agora contém o fluxo de preparação, envio único, acompanhamento e download de vídeos para o motor aberto **Openjutsu Advanced via ComfyUI local**. Pode aceitar de 1 a 4 imagens originais e inclui uma cópia do workflow API oficial, respeitando sua licença MIT. A configuração inicial do backend está em [docs/P0_FURUYA_COMFYUI_UI_2026-10-30.md](docs/P0_FURUYA_COMFYUI_UI_2026-10-30.md).

**Ainda não é um render validado**: o ComfyUI deve estar instalado com os nós e pesos, e ter GPU adequada. O servidor local não provisiona GPU grátis nem torna o GitHub Pages um backend de IA. Os testes até agora só verificam o ciclo HTTP com servidor simulado. A compatibilidade real do modelo com a festa do Rio permanece pendente.

---

## Arquitetura principal multimotor — 29/10/2026

**Missão:** transformar o Furuya Motion Studio na plataforma de geração de vídeos com substituição de personagens inteiros. A plataforma controla preparação, seleção do alvo, motores, execução, download e auditoria; nenhum provedor (inclusive Viggle) deve ser obrigatório.

O novo núcleo `cloud/engine_registry.py` separa duas tarefas: **substituição na cena existente** (clipe da dança no Rio; preservar a multidão) e **transferência de movimento** (personagens de animes/cinema executando coreografias de vídeos virais). A interface `generate.html` oferece seleção de motor, mas **apenas o Viggle Remix possui submissão via API experimental**, exclusivamente para motion-transfer. Os motores abertos Wan2.2-Animate replacement, Viggle-Animate open e Wan-Animate-2 motion têm adaptadores CLI em dry-run, sem GPUs provisionadas. Motor Kling 3.0 está catalogado como candidato de pesquisa sujeito a cobrança e indisponível no orçamento zero até comprovar créditos gratuitos com controles de gasto.

Os critérios, fontes oficiais, comparação e plano de execução encontram-se em **[docs/MOTORES_MULTIMOTOR_P0_2026-10-29.md](docs/MOTORES_MULTIMOTOR_P0_2026-10-29.md)**. O comando `tools/audit_generated_video.py` também impede confundir cópias do vídeo original com resultados novos e exige revisão de identidade/oclusões antes de aprovar o primeiro MP4.

**Limite atual: nenhum motor pesado foi executado; o vídeo final da Albedo na festa do Rio ainda não existe.** Nenhuma contratação ou gasto adicional foi feito.

---

## Novo teste P0 de geração temporal (29/10/2026; experimental, ainda sem render real)

O módulo [generate.html](./generate.html) introduz a tela de geração de vídeo da Albedo com o backend [cloud/local_render_gateway.py](./cloud/local_render_gateway.py). Ele usa a API Viggle V1 Video Remix para **uma pessoa em um clipe de 3 segundos** e pode, após confirmação do usuário, enviar a PNG original e o MP4, consultar o estado da geração e baixar o vídeo resultante. Não depende da GPU do Redmi ou da RX580, mas exige créditos gratuitos existentes na conta do provedor. O backend protege a chave em uma variável de ambiente do Python. **No GitHub Pages a tela é demonstrativa e não pode gerar sozinha**, pois a chave não pode ficar num JavaScript público. Para a execução, siga [docs/P0_ALBEDO_GERACAO_REAL_2026-10-29.md](docs/P0_ALBEDO_GERACAO_REAL_2026-10-29.md) e abra a página servida pelo gateway local.

A v0.8.1 continua sendo exclusivamente um editor de preparação. **Nenhum vídeo final de Albedo animada por IA foi renderizado ou aprovado até esta atualização.** A documentação do serviço informa uma franquia inicial para contas novas, não créditos garantidos para uma conta específica.

---


## Correção de usabilidade v0.8.1 — por que a personagem desaparece ao reproduzir

A gravação real `1000585256.webm` de 5 segundos enviada pelo usuário mostrou apenas o **vídeo base** nas amostras examinadas. Isso é compatível com o funcionamento esperado do editor: a prévia com personagem é um **quadro-chave estático** (dentro de ~0,26 s do instante marcado); ao reproduzir, o original aparece, sem propagação de identidade. O botão **Vídeo ORIGINAL (sem IA)** exporta apenas o material de entrada para IA, sem alteração da pessoa. Isso não é bug de renderizador: a **geração temporal nunca foi implementada**.

Na v0.8.1 foram adicionados avisos permanentes junto ao canvas, rótulos explícitos no play e na exportação, mensagens dinâmicas ao sair do instante de edição, e documentação das limitações. Nenhum processamento por IA foi adicionado; é incorreto recomendar o play como validação de animação. O próximo teste relevante exige realmente executar um modelo generativo de recasting, com quadro integralmente retocado, condições gratuitas verificadas e respeito aos limites do provedor.

A avaliação de vídeo pelo usuário **não comprova que a pessoa foi substituída com fidelidade**. Não confundir preview de still, rascunho e vídeo final gerado.

---

## Editor v0.8 — Quadros-chave e preparação reproduzível (implantado)

**Abrir:** https://furuya29.github.io/furuya-motion-studio/recast.html?v=0.8.1

A v0.8 implementa quadros-chave independentes para cada personagem, máscaras por instante, restauração de quadros salvos, importação e exportação de projetos JSON. Os arquivos de imagem e vídeo não são embutidos no JSON: ao restaurar o projeto, reimporte os arquivos originais.

Uma sobreposição manual **só aparece perto do quadro em que foi editada**: não se apresenta como rastreamento contínuo. A referência retocada é vinculada ao tempo da tomada e o validador não aprova somente um nome de arquivo sem a imagem carregada no dispositivo. Dimensões do Canvas são alinhadas em múltiplos de 32 para compatibilidade com modelos de vídeo.

**Ferramenta CPU para preparação de clipe MP4:** `tools/prepare_clip.py` recebe o projeto e o vídeo e valida metadados, duração (até 5,2 s), dimensões e um quadro-chave do trecho. Por padrão só mostra os comandos; com `--execute` e FFmpeg previamente instalado gera `driving.mp4`, `source-ref.png` e, quando fornecido um quadro **inteiramente** retocado por imagem, `repainted-ref.png`. O resultado não é vídeo gerado por IA; sem GPU e sem upload. Não sobrescreve arquivos existentes.

**Adaptador de inferência oficial Viggle-Animate:** `cloud/viggle_inference.py` prepara uma chamada ao script original `inference/sample.py` com `--cond driving.mp4 --ref repainted-ref.png`. Só executa com `--execute`, checkpoint e instalação existentes. Não baixa modelos, não inicia máquinas remotas nem garante recursos ou franquia.

**Demonstração externa oficial:** https://huggingface.co/spaces/Viggle/viggle-animate . O Space aparece como ZeroGPU, mas dispõe de quota gratuita limitada; não houve geração real comprovada na conta do usuário. O envio de vídeo/imagem a essa página é uma ação externa e opcional.

O pipeline atual segue sendo **preparação + integração local opcional**; a geração de vídeo de personagem inteiro no aplicativo NÃO está operacional até que um backend passe no teste real de 3 segundos. Video-to-video multi-personagem, oclusões e preservação visual ainda não estão aprovados.

---

## Editor v0.7 — Recasting integral VIDEO-FIRST (novo)

Acesse: [Furuya Recasting v0.7](https://furuya29.github.io/furuya-motion-studio/recast.html?v=0.7)

O fluxo principal agora é **vídeo original → quadros do vídeo → referências de personagem inteiro (cabelo, rosto, corpo, roupas, acessórios) → silhueta/máscara por pessoa → quadro original retocado → assets preparados para IA de vídeo**. Não há dependência de JSON MediaPipe.

O editor implementado funciona inteiramente no Chrome Android/PC: linha do tempo do vídeo, recorte de trecho 3/5/8 s, múltiplas referências visuais, máscara manual por pontos, posicionamento de PNG com escala, giro e arraste, importação do quadro retocado final, exportação individual de PNG original, rascunho, máscara, quadro retocado, projeto JSON e tentativa de exportação do vídeo-base recortado em WebM/MP4 conforme navegador (sem áudio). Para selecionar o início do trecho, pressione **Usar o instante atual como início do trecho**.

**Transparência sobre o estágio atual:** o PNG provisoriamente sobreposto não é uma troca real de personagem. O quadro definitivo deve conter a substituição INTEGRAL da pessoa com cenário preservado; a propagação generativa para o vídeo ainda **não está implementada** e demandará um serviço/modelo de inferência adicional. O Wan2.2-Animate exige seu próprio pré-processamento, e a máscara desenhada no editor não equivale à saída desse pipeline.

Verificação gratuita de hardware: `python cloud/free_gpu_preflight.py --workdir . --project furuya-projeto-recasting.json`. Esse script apenas inspeciona CPU/RAM/disco/NVIDIA GPU, sem executar modelos, instalar bibliotecas ou consumir uma quota remota. Leia [os critérios GO/NO-GO para GPUs gratuitas](cloud/README.md) antes de tentar Hugging Face ZeroGPU, Colab ou Kaggle. **Nenhuma GPU foi conectada, nenhum modelo pesado foi executado e nenhuma cobrança foi gerada.**

---

## Novo módulo v0.6.1 — Compositor visual de personagens 2D

**Abrir:** [Compositor 2D](https://furuya29.github.io/furuya-motion-studio/compositor.html?v=0.6.1)

A página `compositor.html` e o motor `compositor.js` foram adicionados ao projeto sem modificar o algoritmo MediaPipe de captura v0.5.

### O que já foi implementado de fato

1. Importar no Chrome Android o **mesmo vídeo** MP4/WebM e o JSON previamente exportado pelo motor de captura.
2. Adicionar **múltiplas camadas de personagem**, cada uma com uma imagem PNG/WebP e associação ao **alvo marcado** ou a um **ID de trilha** extraído do JSON.
3. Posicionar a imagem pelos landmarks de ombros, cabeça/orelhas, quadris e rotação estimada; modos de imagem **cabeça/rosto** e **corpo rígido**, com controle de escala, opacidade e offsets X/Y.
4. Prévia local por Canvas, reprodução do vídeo, busca temporal e interpolação **somente entre amostras próximas** da mesma trilha. Breves retenções de pose são permitidas, sem fingir que se trata de nova medição.
5. Salvar um PNG do quadro ou tentar gravar vídeo local por `Canvas.captureStream()` + `MediaRecorder`; conforme o navegador, saída WebM ou MP4, **sem áudio**, em tempo real. Teto de dimensão de saída ~1280 pixels no maior lado.
6. Mensagens de cobertura da trilha no JSON, avisos para vídeos de proporções/durações diferentes, indicador de transparência da imagem importada.

### Correção da rotação — v0.6.1 (a partir de vídeo de teste real)

- Vídeo exportado pelo usuário: WebM VP9 720×1280, ~29,5 segundos de quadros; o contêiner WebM não possui duração explícita detectada pelo ffprobe. Isso será tratado separadamente.
- A pose 2D da personagem aparece inclinada entre aproximadamente 3 e 9 segundos, enquanto a pessoa de referência permanece predominantemente ereta. A imagem do personagem é um sprite rígido: ainda não há rigging, deformação de braços/pernas ou substituição generativa do corpo.
- Origem do bug: `atan2` entre os ombros podia resultar próximo de `±π` para um torso horizontal quando os índices dos ombros estavam invertidos. Multiplicar esse ângulo por 0,2–0,25 causava inclinação artificial de cerca de 36–45 graus.
- Alterações executadas: orientação dos ombros normalizada módulo π, inclinação limitada; por padrão, **automática desligada**. Em cada camada existe agora um controle **Giro manual −180° a +180°**, botões **−15°, 0°, +15°** e checkbox para permitir inclinação automática. O ajuste funciona na prévia e na exportação.
- O personagem desaparecer após ~12 segundos no teste é consequência de perda de associação do dançarino no JSON v0.5; **não corrigido pela rotação**. A correção requer rastreamento visual melhor, referências de novos trechos ou edição manual com keyframes.
- Executados testes sintáticos e testes simulados dos controles, rotação manual, opt-in de auto inclinação e anti-180°. É indispensável validar o layout e exportar novo clipe no Redmi.

### Primeiro teste recomendado

- Faça uma captura v0.5 e exporte o JSON; mantenha o arquivo de vídeo original.
- Abra o compositor v0.6; importe o mesmo vídeo e o arquivo JSON.
- Em **Personagem 1**, importe uma imagem PNG **com fundo transparente** (ex.: rosto/cabeça do personagem).
- Selecione `★ Alvo escolhido na captura`. Ajuste escala e posição na prévia de aproximadamente 2 a 8 segundos, pois o alvo esteve visível apenas num subconjunto da gravação de teste.
- Se desejar, adicione personagem 2, atribuindo um **ID de trilha diferente**.
- Salve um PNG, depois tente **Exportar vídeo** no Chrome Android. O formato de vídeo depende do suporte a `MediaRecorder`, e o browser pode limitar o FPS de saída.

**Limites honestos:** isso é composição 2D sobre vídeo, NÃO face swap por inteligência artificial, recasting generativo, remoção do corpo original, reconstrução de membros ocultos, rig 2D segmentado ou preservação por IA de cabelo/roupa quadro a quadro. A arte carregada não é gerada novamente; por isso mantém os pixels da imagem, mas é apenas deslocada, escalada e girada como sprite rígido. Oclusões, mudanças drásticas de ângulo, rotatividade e trocas de trilha ainda exigem tratamento especializado.

### Adaptador desktop FaceFusion (preparado, mas motor não instalado)

O arquivo `desktop/facefusion_adapter.py` contém um **adaptador funcional de CLI** para FaceFusion: verifica caminhos, prepara `headless-run` com fonte, vídeo-alvo e saída, seleciona modo de referência, valida sobreposição de saída e oferece CPU/DirectML/CUDA/ROCm. **Por padrão, não executa nada** (dry-run); somente `--execute` inicia um FaceFusion já instalado. Nenhum serviço externo é obrigatório.

Documentação oficial consultada em 2026-10-27: [FaceFusion CLI](https://docs.facefusion.io/usage/cli-commands/general), [Paths](https://docs.facefusion.io/usage/cli-arguments/paths), [Selector](https://docs.facefusion.io/usage/cli-arguments/face-selector), [Processors](https://docs.facefusion.io/usage/cli-arguments/processors), [Execution Providers](https://docs.facefusion.io/usage/cli-arguments/execution).

Exemplo de inspeção **no PC onde o FaceFusion já estiver instalado** (não há instalação automática neste repositório):

```powershell
python desktop/facefusion_adapter.py --facefusion-dir "C:\FaceFusion" --source "C:\imagens\rosto.png" --video "C:\videos\danca.mp4" --output "C:\videos\danca_fusion.mp4" --provider cpu --reference-frame 48
```

Se a prévia do comando estiver correta e **somente após verificar a instalação**, acrescente `--execute`. O modo de referência **não garante** associação correta de múltiplos rostos em multidões; esta primeira versão só prepara **uma substituição facial por trabalho**, sem recasting de corpo inteiro. Requisitos de hardware e aceleração AMD ainda não foram verificados.

O PC Remote Agent está em manutenção; **não houve execução remota nem instalação no PC nesta entrega**. Não publicar o material editado como gravação autêntica; sinalize conteúdo sintético quando apropriado.

---

## O que já está implementado no motor de captura

- Importação local de arquivos MP4/WebM compatíveis com o Chrome Android.
- MediaPipe Pose Landmarker Lite ou Full, inicialização GPU com fallback automático para CPU.
- Configuração de até 6 **poses estimadas** por quadro (não garante detecção de seis pessoas em cenas complexas).
- Detecção de um quadro selecionado, visualização de esqueletos e varredura temporal ajustável (2, 4, 6 ou 8 amostras/s).
- Rastreamento **experimental** por proximidade e predição curta; os rótulos agora mostram **trilhas**, não identidades pessoais confiáveis.
- Filtro heurístico para separar poses **úteis**, **parciais** e **descartadas**; juntas fora da imagem ou com baixa visibilidade não são desenhadas.
- Suavização temporal leve de pontos quando o rastreador consegue associar poses próximas; isso não resolve cruzamentos ou oclusões complexas.
- **Seleção manual opcional de um dançarino:** após Detectar quadro, toque em Escolher dançarino e marque o tronco da pessoa na imagem. Os dois ombros precisam estar visíveis. Isso gera uma referência inicial e sinaliza apenas correspondências prováveis, sem garantir identidade.
- **Análise focal da pessoa escolhida:** a partir do instante selecionado, o MediaPipe passa a analisar um recorte móvel da região ao redor dos ombros; pontos resultantes são remapeados às coordenadas do vídeo completo.
- **Âncora nos ombros:** a referência espacial ignora o centro estimado dos quadris, que é especialmente instável quando as pernas saem do vídeo.
- **Acompanhamento conservador do alvo:** valida proximidade e largura dos ombros; após uma oclusão longa, interrompe a associação do alvo em vez de atribuir automaticamente outra pessoa.
- **Recuperação do quadro inteiro (v0.5):** quando a associação se perde, o aplicativo deixa de restringir a IA ao recorte antigo e volta a detectar poses no vídeo inteiro; as poses não confirmadas aparecem como trilhas sem associação, não como o dançarino escolhido.
- **Múltiplas referências manuais (v0.5):** o mesmo dançarino pode ser marcado em diferentes instantes (por exemplo 2,5 s, 12 s e 20 s), permitindo reabrir segmentos de acompanhamento após interrupções. O usuário deve escolher sempre a mesma pessoa.
- **Diagnóstico de repetição de poses:** contabiliza resultados exatamente repetidos em amostras consecutivas, sem presumir que a causa seja o decodificador.
- **Alinhamento de sobreposição:** vídeo e canvas usam a mesma área visível, eliminando desalinhamento causado por altura máxima divergente.
- A prévia em tempo real **não** foi adicionada. A detecção de um quadro acontece somente ao pressionar Detectar quadro; a varredura completa acontece somente ao pressionar Capturar coreografia.
- Exportação local em JSON (33 articulações, coordenadas normalizadas + coordenadas 3D aproximadas), CSV e quadro PNG.
- Sem upload de vídeo para nossos servidores. O motor JavaScript e o modelo são baixados de servidores públicos na primeira execução.

## Como abrir no Android

### Recomendado: publicar gratuitamente no GitHub Pages
1. Crie um repositório público `furuya-motion-studio` na sua conta GitHub.
2. Adicione `index.html` na raiz do repositório.
3. Vá a **Settings → Pages → Build and deployment** e selecione **Deploy from a branch**, branch `main`, pasta `/(root)`.
4. Abra o endereço HTTPS fornecido por GitHub Pages no Chrome do Redmi K70 Ultra.
5. Toque em **Selecionar vídeo do aparelho**, selecione um MP4 e em **Carregar IA no aparelho**.
6. Para rastrear um dançarino específico, pause em um instante próximo do início com corpo claramente visível, pressione **Detectar quadro**, depois **Escolher dançarino** e toque no tronco da pessoa desenhada. Para adicionar mais referências temporais, vá ao segundo 12 e depois ao 20 (ou instantes em que o alvo esteja visível); repita **Detectar quadro → Escolher dançarino → tocar na mesma pessoa**. Esse passo é opcional.
7. Pressione **Capturar coreografia** para analisar os instantes amostrados. Acompanhe as contagens de alta visibilidade/parciais/descartadas e as possíveis repetições.
8. Exporte JSON para auditar o atributo `selected` em cada pose, `targetStats` e `repeatedFrames` (o CSV também possui a coluna `possible_target`).
9. A captura é exploratória: se as poses estiverem fora do corpo ou forem majoritariamente parciais, não reutilize os dados na animação final.

### Teste de qualidade no Redmi (v0.5)
- Atualize a página (se necessário, recarregue sem cache) e confirme o selo **ALPHA 0.5**.
- Use inicialmente **Lite / 3 pessoas / 4 amostras/s**; para melhorar a frequência temporal, experimente 8 amostras/s após o teste inicial.
- Carregue o modelo, selecione o mesmo vídeo, detecte um quadro e capture a coreografia.
- Confira os números de poses úteis, parciais e descartadas. Numa multidão, ter muitas trilhas criadas não prova que a IA acompanhou muitas pessoas reais; geralmente reflete entradas/saídas e trocas.
- Envie o JSON exportado para inspeção da estabilidade, porcentagem de detecções válidas e taxa de trocas de trilha.


O GitHub Pages hospeda apenas o site estático. O vídeo escolhido e as inferências de pose são processados no navegador do celular. As bibliotecas e modelos externos ainda precisam ser baixados; não é totalmente offline.

### Observações sobre o alvo
- O campo `targetSelection` documenta apenas a referência indicada com o toque. `selected: true` significa **provável continuidade**, não uma identidade biométrica comprovada.
- A partir de oclusões longas, o sistema pode deixar de marcar o alvo até a próxima referência temporal. Os quadros seguintes continuam sendo analisados na imagem completa e guardados como **não associados**, evitando um apagão de detecções. O próximo marco manual reacende uma nova tentativa de rastreamento.
- Mesmo várias referências não garantem que as poses intermediárias pertençam ao mesmo indivíduo. As detecções não associadas são mantidas separadas do alvo e **não devem** ser usadas automaticamente para animá-lo.
- No modo focal são exportadas apenas as poses associadas ao alvo. Durante recuperação pela imagem inteira, outras poses aparecem e são exportadas com `selected: false` e `detectionMode: 'full-frame-unassigned'`, para posterior auditoria.
- O recorte é um auxílio de reconhecimento, **não uma garantia de identidade**. Coordenadas 3D obtidas do recorte são aproximações; o arquivo JSON inclui `targetReferences`, `targetSelection.mode` e `detectionMode` por quadro para auditoria.
- Na gravação lotada de referência, pernas e pés frequentemente ficam fora do enquadramento; não há informação suficiente para uma coreografia corporal completa.

### Alternativa experimental: abrir `index.html` diretamente
Pode funcionar em alguns navegadores Android, mas origens `file://` podem bloquear o carregamento de WebAssembly/modelos. Se falhar, use o método HTTPS acima. Não desative configurações de segurança do Chrome.

## Uso responsável e limitações

- As versões **v0.1** e **v0.2** foram executadas no Redmi K70 Ultra. A v0.2 cobriu o vídeo inteiro, mas continuou apresentando poses parciais, rastros interrompidos e pontos fora da imagem. Na v0.3, o alvo apareceu em **3 dos 113 quadros elegíveis** e os 25 rastros distintos mostraram fragmentação. Na **v0.4**, uma seleção inicial em 2,42 s perdeu o alvo após 8,25 s e permaneceu sem poses associadas até o final; o MediaPipe ainda reportou detecções após 13 s, mas o algoritmo não as vinculou. A **v0.5 ainda depende de validação no Redmi**.
- O MediaPipe identifica pontos do corpo (pose landmarks) e não garante IDs persistentes em multidões.
- Ainda **não** gera vídeos com personagens de anime, não faz substituição de seis atores, não gera rig 2D e não integra Wan2.2-Animate. Essas são fases seguintes.
- Os dados 3D (`world`) são aproximações inferidas de câmera monocular, e não captura 3D calibrada profissionalmente.
- Para maior precisão em vídeos com muita gente, na próxima fase avaliaremos detector multi-pessoa especializado e reidentificação temporal.
- O processamento ocorre no aparelho; no entanto a biblioteca MediaPipe pode emitir métricas de uso conforme seu aviso de privacidade. Consulte https://developers.google.com/edge/mediapipe/solutions/vision/pose_landmarker/web_js.

## Tecnologias

- HTML / CSS / JavaScript moderno
- `@mediapipe/tasks-vision@0.10.34` (versão fixada para manter estabilidade)
- Modelos públicos Pose Landmarker Lite e Full (arquivos `.task`)

## Próximas fases

1. Validar a v0.5 no Redmi: confirmar detecções de quadro inteiro depois das perdas, referências adicionais, quadro `detectionMode`, `targetFound` e continuidade por segmentos.
2. Aprimorar o rastreamento multi-pessoa com reidentificação de aparência, interface de correção de correspondências e avaliação de consistência.
3. Criar rig 2D / importação de camadas e associar cada boneco ao movimento.
4. Ferramentas para rostos, mãos, montagem e exportação de vídeo.
5. Integração opcional de Wan2.2-Animate via GPU compatível, sem depender dele para o funcionamento básico.