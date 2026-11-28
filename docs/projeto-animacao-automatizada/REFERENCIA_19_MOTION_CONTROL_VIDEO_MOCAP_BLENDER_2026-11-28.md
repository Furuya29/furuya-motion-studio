# Referência 19 — Motion Control por vídeo e transferência de movimento ao Blender

Data: 28/11/2026. Fonte exata enviada: https://youtu.be/vFH9Dk9HzSI?is=iEhFX1HMGGO6GiBC. Título: “CLONE OS MOVIMENTOS DE QUALQUER PESSOA NO GOOGLE FLOW (DE GRAÇA E ILIMITADO)”. Referência de estudo, análise da transcrição completa do tutorial em português, sem teste de execução ou inspeção temporal do vídeo demonstrativo. Aditivo ao Estúdio de Aenvarath e ao PCRA, sem substituir o método multimétodo, sem alterar fila e sem novos custos.

## Evidência diretamente do vídeo
- 00:00–01:03: autora descreve Motion Control como cópia de movimentos de pessoa gravada para personagem IA.
- 01:20–03:39: escolhe vídeo de origem (13 s), produz imagem da personagem e prepara trecho de até 10 s no CapCut, retirando ou mutando áudio.
- 03:39–05:15: insere vídeo e imagem no Google Flow, escolhe Omni Flash 9:16; solicitação demonstrada exibe 20 créditos (não tomar como preço geral da função).
- 05:30–07:23: altera fundo e roupas por edições gerativas posteriores; confessa que os créditos da conta acabaram.
- 08:43–09:31: recompõe áudio no CapCut.
- 01:50–02:21 e 09:31–10:49: recomenda várias contas Gmail e até compra de contas para contornar cotas. NÃO adotar essa estratégia — risco de segurança, termos, descontinuidade; não corresponde a ilimitado verdadeiro.
- O vídeo demonstra transferência de MOVIMENTO EM PIXELS e não revela um rig 3D, armature ou cena Blender editável. A aparência e as roupas ainda podem derivar a cada nova geração. A demo é comercial 9:16, não longa-metragem animado.

## Verificação independente
Google Flow (https://support.google.com/flow/answer/16526234?hl=pt-BR): não assinantes recebem 50 créditos diários, que não acumulam; Omni Flash 1.2 até 10s por geração ou edição a 1 crédito/s em 360p e 3 créditos/s em 720p, sujeitos a mudanças. O valor de 20 exibido é do pedido mostrado, não universal.

ComfyUI/Wan2.2 Animate (https://github.com/Comfy-Org/docs/blob/main/tutorials/video/wan/wan2-2-animate.mdx): possui modo Move — animar personagem de imagem a partir de movimento de vídeo; modo Mix — substituir personagem no vídeo. DWPose extrai guia de pose/face; pode rodar localmente em hardware e quantização compatíveis, mas preservação de face/roupa/cenário não é garantida pelo algoritmo.

FreeMoCap (https://github.com/freemocap/freemocap): captura sem marcadores por MULTICÂMERAS e gera esqueleto 3D e exportação para Blender, funcionando offline após preparação; não inferir que ele reconstrói qualquer vídeo monocular da internet com qualidade equivalente.

FreeClipMoCap (https://github.com/rnsfh/FreeClipMoCap): extensão Blender experimental para captura markerless de arquivo de vídeo via MediaPipe, processamento local e exportação FBX/BVH, com correções IK. Maturidade/versionamento/segurança precisam ser ensaiados; não instalado.

PoseCap (https://github.com/CorridorTech/PoseCap): preview aberto para webcam/vídeo e retarget, backend CPU MediaPipe Lite ou NVIDIA PEAR; depende de modelos corporais SMPL-X que têm licenças NÃO comerciais sem licença comercial adicional. NÃO colocar em rota comercial gratuita sem confirmar direito de uso. Estado de desenvolvimento inicial.

## Arquitetura a reusar no Aenvarath — preferir animação de ossos real em vez de pixels

A. Vídeo de referência com direito de uso → extração 2D/3D das poses → estabilização/limpeza do movimento → retarget ao rig canônico Blender → correção IK de pés/mãos, root motion e contatos → gerar Action/NLA reutilizável → render 3D na mesma cena/roupa com geometria persistente → QA, MP4, projeto editável, logs.

B. Usar Wan2.2 Animate local como camada OPCIONAL para transformar a aparência/iluminação com condicionamento do vídeo/poses. Nunca tratar pixel-to-pixel generativo como prova de rig 3D e continuidade perfeita.

C. Em ações complexas — correr, levantar, abraçar, lutar, interação com objeto — combinar mocap humano e coreografia/constraints/IK no Blender. Asas de Nólyrien, voo/magia e interações de tecidos/objetos requerem rigs e keyframes/simulação adicionais; nenhuma gravação de humano produz automaticamente animação biologicamente correta das asas.

D. Manter biblioteca de movimentos em assets versionados: action_id, provenance, fonte, licença comercial, skeleton map, fps, root trajectory, contatos, mãos, correções, QA. Reutilizar movimento entre personagens preservando modelos, proporções, roupas e materiais; exigir retarget específico quando biotipos diferirem.

## Direitos e uso comercial

Um vídeo sem aviso de copyright, watermark ou reivindicação pública NÃO significa domínio público, autorização de download ou licença de reutilização. Lei 9.610/1998 art. 7º protege obras coreográficas e audiovisuais; há também direitos de artistas e intérpretes: https://www2.camara.leg.br/legin/fed/lei/1998/lei-9610-19-fevereiro-1998-365399-normaatualizada-pl.html.

Preferir vídeo gravado pelo próprio usuário ou colaboradores com consentimento, bibliotecas com licença comprovadamente comercial e, se só for necessário estudar o movimento, analisar gestos genéricos sem republicar a gravação protegida. Uma coreografia expressiva não pode ser automaticamente tratada como movimento sem proteção; verificar direitos caso a caso.

## Ponto de integração e critério de aceite

Somar como MÉTODO ADICIONAL aos engines A/B/C do estúdio e ao protocolo ChatGPT → PCRA → Blender. A OS PCRA #320 permanece backlog condicionado às prioridades atuais. Após acesso REAL, primeira prova: movimento autoral/licenciado curto de Nyraelis ou guarda na vila destruída, extraído para esqueleto, transferido a rig Blender aprovado, corrigido em pés/mãos, renderizado com cenário/roupa persistentes em 2–5s; arquivos originais, rig/action, .blend, MP4, FFprobe, hashes e recibos verificáveis.

Status: PESQUISA E PROPOSTA de integração, sem geração, instalação, aprovação artística, alteração de prioridades ou alegação de que o PCRA já executou Blender.
