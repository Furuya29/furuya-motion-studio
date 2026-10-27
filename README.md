# Furuya Motion Studio — v0.1 (protótipo)

## O que já está implementado

- Importação local de arquivos MP4/WebM compatíveis com o Chrome Android.
- MediaPipe Pose Landmarker Lite ou Full, inicialização GPU com fallback automático para CPU.
- Configuração de até 6 **poses estimadas** por quadro (não garante detecção de seis pessoas em cenas complexas).
- Detecção de um quadro selecionado, visualização de esqueletos e varredura temporal ajustável (2, 4, 6 ou 8 amostras/s).
- Rastreamento **experimental** por proximidade, com IDs sujeitos a trocas quando há cruzamentos/oclusões.
- Exportação local em JSON (33 articulações, coordenadas normalizadas + coordenadas 3D aproximadas), CSV e quadro PNG.
- Sem upload de vídeo para nossos servidores. O motor JavaScript e o modelo são baixados de servidores públicos na primeira execução.

## Como abrir no Android

### Recomendado: publicar gratuitamente no GitHub Pages
1. Crie um repositório público `furuya-motion-studio` na sua conta GitHub.
2. Adicione `index.html` na raiz do repositório.
3. Vá a **Settings → Pages → Build and deployment** e selecione **Deploy from a branch**, branch `main`, pasta `/(root)`.
4. Abra o endereço HTTPS fornecido por GitHub Pages no Chrome do Redmi K70 Ultra.
5. Toque em **Selecionar vídeo do aparelho**, selecione um MP4 e em **Carregar IA no aparelho**.
6. Use **Detectar quadro** antes de iniciar **Capturar coreografia**; depois exporte JSON/CSV.

O GitHub Pages hospeda apenas o site estático. O vídeo escolhido e as inferências de pose são processados no navegador do celular. As bibliotecas e modelos externos ainda precisam ser baixados; não é totalmente offline.

### Alternativa experimental: abrir `index.html` diretamente
Pode funcionar em alguns navegadores Android, mas origens `file://` podem bloquear o carregamento de WebAssembly/modelos. Se falhar, use o método HTTPS acima. Não desative configurações de segurança do Chrome.

## Uso responsável e limitações

- Esta é uma **versão experimental não validada no Redmi K70 Ultra**; a velocidade depende do navegador e da complexidade do vídeo.
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

1. Validar importação e desempenho no Redmi.
2. Corrigir bugs e adicionar tracking mais robusto.
3. Criar rig 2D / importação de camadas e associar cada boneco ao movimento.
4. Ferramentas para rostos, mãos, montagem e exportação de vídeo.
5. Integração opcional de Wan2.2-Animate via GPU compatível, sem depender dele para o funcionamento básico.