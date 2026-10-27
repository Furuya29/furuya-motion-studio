# Furuya Motion Studio — v0.5 (protótipo experimental)

## O que já está implementado

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