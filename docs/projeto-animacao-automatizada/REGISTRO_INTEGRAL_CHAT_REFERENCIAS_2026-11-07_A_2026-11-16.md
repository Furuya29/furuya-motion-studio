---
document_id: PAA-CHAT-REFERENCIAS-2026-11-07-2026-11-16
document_type: registro-integral-semantico-e-handoff
project: Projeto de Animação Automatizada
origin: conversa de análise de referências audiovisuais por IA
coverage_start: 2026-11-07
coverage_end: 2026-11-16
compiled_at: 2026-11-16
language: pt-BR
status: consolidado; implementação técnica não homologada
repo: Furuya29/furuya-motion-studio
repo_branch: main
repo_directory: docs/projeto-animacao-automatizada
integration_policy: SOMAR_SEM_APAGAR
priority: preservação completa de contexto e rastreabilidade
---

# REGISTRO INTEGRAL DO CHAT DE REFERÊNCIAS — PROJETO DE ANIMAÇÃO AUTOMATIZADA

**Escopo:** consolidação semântica tão completa quanto possível de tudo o que foi solicitado, observado, respondido, documentado, decidido, qualificado e deixado pendente nesta conversa desde sua primeira mensagem, incluindo os dois vídeos recebidos, as análises, os arquivos derivados, os registros no GitHub e os handoffs. Este documento não é uma transcrição literal de cada palavra emitida pelo assistente ou das saídas internas de ferramentas; é um registro operacional fiel e detalhado, escrito para que um GPT posterior possa recuperar o contexto e continuar o projeto sem precisar reconstruir decisões por suposição.

**Regra superior e inegociável:** **ESTE DOCUMENTO É ADITIVO. NÃO APAGAR, NÃO SUBSTITUIR, NÃO RECOMEÇAR, NÃO INVALIDAR AUTOMATICAMENTE NENHUMA DECISÃO OU ARQUITETURA JÁ ESTABELECIDA NO CHAT PRINCIPAL.** O projeto original continua a possuir seu próprio planejamento, decisões, checkpoints, ferramentas, integrações e prioridades. Conciliar item a item; integrar o que for novo e preservar o que já estiver aprovado. Esta frente é pesquisa cinematográfica, não a totalidade do projeto.

## 0. LEIA PRIMEIRO — RESUMO DE RECUPERAÇÃO EM 90 SEGUNDOS

1. **Meta do usuário:** desenvolver um sistema de produção audiovisual automatizada que supere visual e tecnicamente vídeos de IA muito bem produzidos, com suporte tanto a **anime japonês 2D autêntico** quanto a **animação 3D realista/semirrealista e métodos híbridos**. A meta inclui direção, edição, atuação, câmera, arquitetura, continuidade entre quadros e cenas, proporções corporais, geometria, contato físico, sincronismo e qualidade narrativa; não se limita a imagens bonitas.
2. **Vídeo-referência 01:** Fantasoner, “TS Malfoy”, curta de fãs do universo de Harry Potter; link https://youtu.be/WYRDe8XsRmI?is=H1BwCO2mpf53nZir ; MP4 **1000589408.mp4**; 1920×1080, 30 fps, 16.328 frames de vídeo, ~9min04s. Excelente fotografia dramática, arquitetura gótica, enquadramento, expressão, montagem. Dependência frequente de poses estáveis, microexpressões, pouco movimento corporal complexo e cortes.
3. **Vídeo-referência 02:** Shift Up, Stellar Blade: BLOODRAIN, “Wanna be in LOVE” (Evie); MP4 **1000589429.mp4**; 1920×1080, 24 fps, 5.222 frames, 3min37,66s. Excelente cidade futurista, direção de arte, materiais, atmosfera, planos, paleta, figurino e montagem. Limitações incluem deriva facial em certas tomadas, atuação corporal pouco integrada, contatos complexos, possível incorreção de perspectiva do microfone nas rotações e mudanças de proporções corporais da protagonista.
4. **Achado adicional inequívoco do USUÁRIO:** microfone “levemente fora de perspectiva, principalmente quando a câmera rotaciona”; “diferenças de proporções corporais da personagem” e outras falhas. Essas observações foram explicitamente acrescentadas depois da primeira análise do segundo vídeo. Devem ser verificadas quadro a quadro e tratadas como requisitos P0 de QA, nunca omitidas de futuras sínteses.
5. **Solução de arquitetura proposta, não homologada:** métodos **multimotor/multimétodo**; bíblia de personagem e corpo; modelos/rigs 2D/3D; cinematografia com câmera espacialmente definida; assets e props persistentes; movimento/blocking controlado, IK/FK, pontos de contato, áudio→fonemas→visemas, composição em passes, IA usada de modo supervisionado, QA temporal/cross-shot, FFmpeg e revisão humana.
6. **Limite de custo e hardware:** buscar R$ 0; Windows 10 Pro, AMD FX-4300, ~16 GB RAM, Radeon RX 580 8 GB; Android Redmi K70 Ultra. Não pressupor GPUs de datacenter nem serviços pagos; a RX 580 não atende à via HIP atual do Cycles GPU. Alternativas locais devem ser efetivamente testadas antes de serem apresentadas como funcionais.
7. **Próxima prova sugerida:** piloto de aproximadamente **15 segundos**, 2–3 tomadas, fala/expressão, movimento corporal/câmera e interação com objeto/microfone; mudanças de perspectiva e proporções devem permanecer geometricamente consistentes. Esta sugestão **não reordena automaticamente** tarefas do chat principal. Issue #12 aberta, **não implementada/homologada**.
8. **Documentação persistente:** repositório **público** https://github.com/Furuya29/furuya-motion-studio , branch main, diretório **docs/projeto-animacao-automatizada/**. O contexto desta frente foi escrito lá; **não se deve afirmar** que toda a documentação e arquitetura do chat principal já está espelhada nesse repositório.
9. **Arquivos entregues no chat:** dois PDFs ilustrados e dois ZIPs de evidências. Os arquivos MP4 e PDFs/ZIPs de terceiros/derivados **não foram enviados ao GitHub**. Os nomes e hashes exatos estão na seção 5.
10. **Política de verdade:** distinguir **[USUÁRIO]** observação/decisão expressa, **[ARQUIVO]** metadado ou imagem examinada, **[FONTE]** informação de fonte externa mencionada, **[ANÁLISE]** inferência técnica baseada em amostras, **[PROPOSTA]** sugestão de desenvolvimento e **[EXECUTADO]** ação com commit/arquivo/issue confirmados. Hipótese não é bug confirmado; documentação não é implementação.

## 1. IDENTIDADE, ESCOPO E PREMISSAS DO PROJETO

### 1.1 O que este chat fez e o que não fez

- Funcionou como **frente de pesquisa/benchmark cinematográfico**, introduzindo vídeos referenciais, avaliando seu acabamento e suas falhas e especificando soluções de engenharia para o sistema original de animação.
- Não implementou o motor de produção, não homologou geração de cenas e não alterou diretamente os projetos de animação anteriormente planejados.
- Não comprova que um gerador de vídeo de IA, Blender, OpenToonz ou qualquer outro software já esteja integrado e funcional no projeto principal.
- Não teve acesso aos projetos internos da Fantasoner ou da Shift Up, nem a seus prompts, rigs, modelos usados, servidores, faturas ou pipeline real; não atribuir tecnologias ou investimentos por mera aparência.
- O objetivo do usuário é **mais exigente** que copiar o aspecto das referências: eliminar defeitos de perspectiva, anatomia e temporalidade, e alcançar direção e edição superiores.

### 1.2 Requisitos e preferências explicitamente reafirmados

- Visual: **anime 2D japonês**, 3D, realista/semirrealista, ou híbrido, de acordo com a produção. Não converter tudo automaticamente em CGI ocidental ou um estilo pictórico alternativo.
- Narrativa: tomadas dirigidas, tempo dramático, edição, composição, emoção, enquadramento, movimentos de câmera, contexto arquitetônico e personagem persistente.
- Movimento: atuar com corpo completo, não apenas boca/olhos; evitar rigidez, deformações, flutuação de peso e deslizamento.
- Continuidade: mesmos personagens, rosto, corpo, cabelo, roupa, objetos, ambientes, dimensões, materiais, iluminação e geometria durante ângulos e cortes.
- Engenharia: seleção de métodos por tomada; evitar dependência de desenhos manuais de cada frame, mas **não proibir** desenho quadro a quadro se for tecnicamente superior em uma cena.
- Operação: alto nível de automação, prova de estabilidade, checkpoints e controle de versões; orçamento recorrente de referência **R$ 0**; não prometer recurso gratuito/externo que não tenha sido testado.
- Organização: toda descoberta relevante deve sobreviver à perda de contexto de um chat, de preferência em arquivos Markdown versionados e separados por projeto/referência.
- Direitos: estudar obras alheias como referência sem copiar músicas, imagens ou vídeos originais para uso comercial nem publicar os MP4s completos no repositório público.

### 1.3 Distinção de projetos e repositórios

- **Projeto de Animação Automatizada:** criação original de animações e obras audiovisuais.
- **Furuya Motion Studio:** outra frente de desenvolvimento que inclui substituição/recast de personagens em vídeos; potencial reutilização de métodos, mas sem confusão de objetivos, entregas ou versões.
- **PCRA/Android Agent:** infraestrutura de automação conexa; nada neste chat autoriza reconfigurá-los ou interromper outros desenvolvimentos.
- O repositório público **Furuya29/furuya-motion-studio** foi escolhido nesta conversa porque já existia e havia acesso GitHub confirmado; a pasta separada foi criada para documentar o projeto de animação. **Necessário validar com o chat principal qual é a documentação canônica de longo prazo**, evitando bifurcação de autoridade.

## 2. CRONOLOGIA EXAUSTIVA DAS INTERAÇÕES E AÇÕES

### 2.1 — 07/11/2026: solicitação inicial, Fantasoner / TS Malfoy

**[USUÁRIO]** Primeira mensagem: “Sei que o foco aqui é animações 3d ou 2d anime realista, mas olha esse exemplo de animação por I.A o absurdo de perfeito que está, sei que ainda tem aquela carinha de I.A, mas o que eu quero é algo melhor ainda que isso, faça uma análise frame a frame desse vídeo”, enviando o URL https://youtu.be/WYRDe8XsRmI?is=H1BwCO2mpf53nZir .

**[ANÁLISE]** O assistente assumiu a tarefa de avaliar composição, movimento, consistência de personagem, câmera, cenário e marcas de IA, diferenciando qualidade de frame isolado e continuidade temporal.

**[EXECUTADO]** Metadados da página identificaram o título coreano “말포이가 여주인 세계선 혼혈왕자편 (TS 말포이)” e descrição declarando produção de fãs por IA. A obra imagina Draco Malfoy feminina em uma linha alternativa de *Harry Potter e o Enigma do Príncipe*. Foram identificadas duas músicas creditadas como “In the Last Light - fantasoner” e “Even There - fantasoner”.

**[BLOQUEIO]** Tentativa de percorrer o player do YouTube com navegação visual encontrou anúncio e não permitiu extrair 12+ amostras cronológicas confiáveis. A duração “2min13s” inicialmente reportada pela navegação era **indevida/incompatível com o MP4 real** e nunca deve ser reutilizada. Uma observação de mulher loira chorando próximo de “00:08” não foi suficientemente isolada da interferência do anúncio para embasar diagnóstico. Uma resposta preliminar também mencionou aproximadamente 9min05s sem verificação de arquivo; depois o MP4 permitiu confirmar os valores técnicos.

**[DECISÃO]** Solicitar o MP4 para análise temporal confiável, ao invés de simular que o filme inteiro havia sido visto. Esse bloqueio não reduz a validade das análises posteriores feitas com o arquivo efetivamente recebido.

### 2.2 — 07/11/2026: recebimento do MP4 TS Malfoy e estudo visual

**[USUÁRIO]** Enviou, sem texto adicional, o arquivo **1000589408.mp4**.

**[EXECUTADO]** O arquivo foi inspecionado em amostras ao longo da duração, tiras temporais e varredura automatizada de quadros; foram produzidos painéis e um PDF de nove páginas.

**[ARQUIVO]** 1920×1080, vídeo H.264 30 fps, 16.328 frames; faixa visual de aproximadamente 09:04,27 (16.328/30), duração do contêiner de cerca de 09:04,37. Esses são valores distintos mas compatíveis; não usar 2:13.

**[ANÁLISE]** Grande impacto de iluminação dramática, pele/rosto, contraluz, cenários góticos, planos gerais e close-ups. O corpo frequentemente permanece estável enquanto a boca, os olhos, os cabelos ou a intensidade da luz se alteram; cortes e emoção sustentam a narrativa. O vídeo não prova ausência de deformações em todos os 16.328 frames.

**[MÉTODO]** Um relatório declarou amostragem a cada 5 s, trechos a aproximadamente 6 fps e varredura automatizada em escala de cinza de 192×108. Aproximadamente **46,1% das transições** tiveram diferença média inferior a **0,5 nível tonal por pixel** nessa métrica e escala. Isso indica **mudança visual discreta**, NÃO “46,1% de quadros congelados”. Escuridão, compressão e gestos sutis afetam a métrica. “Análise frame a frame” foi cumprida parcialmente com processamento automático e inspeção de trechos selecionados, **não** com inspeção humana isolada de cada frame.

**[EXECUTADO]** Foram entregues:
- **Analise_Tecnica_TS_Malfoy_Animacao_IA.pdf**, relatório ilustrado de 9 páginas.
- **Evidencias_Visuais_TS_Malfoy.zip**, 12 entradas, incluindo cópia do PDF, cinco painéis gerais de imagens e seis comparações temporais.

**[PROPOSTA]** Não depender só de imagens bonitas: planejamento por tomadas, identidades persistentes, movimentos dirigidos por rig/keyframe/motion capture, IA supervisionada, QA e edição final; piloto controlado de ~15 s.

### 2.3 — 08/11/2026: solicitação de persistência + segundo vídeo Shift Up

**[USUÁRIO]** Pediu “Guarde essas informações num repositório destinado a esse projeto na minha conta conectada do @GitHub para não perdermos contexto de acordo com que esse projeto evolui”. Em seguida pediu “a mesma análise profunda” do vídeo Shift Up, identificando pontos fortes e falhas, buscando soluções para problemas de IA e integrando os aprendizados ao projeto. O usuário conjecturou que a Shift Up teria investido muito dinheiro e hardware excepcional (“computadores da NASA”): **isso foi uma hipótese retórica do usuário, NÃO um fato comprovado**. Enviou **1000589429.mp4**.

**[EXECUTADO]** O GitHub conectado foi inspecionado. Repositório existente selecionado: **Furuya29/furuya-motion-studio**, público, branch main. Criada pasta documental **docs/projeto-animacao-automatizada/**. As decisões foram preservadas como documentos e commits, sem publicação do vídeo integral.

**[EXECUTADO]** Identificação do segundo MP4: “Wanna be in LOVE”, com **Evie**, associado a **Stellar Blade: BLOODRAIN** / Shift Up; 1920×1080, 24 fps, 5.222 frames, 03:37,66; H.264 + áudio AAC estéreo 44,1 kHz.

**[FONTE]** Fontes mencionadas nessa conversa atribuíram a artistas/modeladores humanos o desenvolvimento da personagem Evie por mais de um ano, com utilização de IA generativa na apresentação audiovisual. O “making of” final é retratado como encenação feita por IA. Nenhuma dessas informações permite deduzir orçamento ou hardware real. Ver URLs na seção 8. Essas afirmações foram registradas como contextualização externa, não como dados inferidos do MP4.

**[ANÁLISE]** Acertos: cidade futurista e arquitetura industrial, profundidade, passarelas, metrô, ambientes úmidos, volumetria, materiais, paleta, figura e figurino, microfone retrô, enquadramentos variados e montagem musical. Limitações: deriva de traços faciais em certos trechos, pouca atuação corporal em relação ao canto, dedos/mãos e objetos delicados, occlusão/contato, pés/apoio, transições espaciais, figurantes.

**[EXECUTADO]** Relatório PDF de 10 páginas e pacote ZIP de evidências visuais de 18 imagens. Os dados do vídeo e recomendações foram salvos em documentação Markdown do GitHub. Aberta a **Issue #12** para o piloto de 15 s (não implementado).

### 2.4 — 08/11/2026: o usuário corrige e amplia a análise

**[USUÁRIO]** “Tem muitas mais falhas como posicionamento do microfone levemente fora de perspectiva, principalmente quando a câmera rotaciona. Diferenças de proporções corporais da personagem, entre outras.”

**[DECISÃO]** A identificação de defeitos NÃO está concluída. As duas observações são prioritárias; a análise precisa considerar falhas sutis e cross-shot, não apenas deformações grosseiras. A observação do usuário foi explicitamente integrada à documentação como suspeita técnica de alta prioridade para validação e correção.

**[PROPOSTA]** Registrar câmera no espaço 3D, pivô/eixo do microfone, geometria persistente do objeto e da personagem, relação mundo/mão e oclusões, parallax em rotação de câmera, rig anatômico com medidas e limites projetados; investigar a proporção corpo/rosto entre planos considerando lente/ângulo/pose antes de acusar drift.

### 2.5 — 08/11/2026: handoff solicitado pelo usuário

**[USUÁRIO]** Pediu um handoff completo para enviar ao chat principal e integrar as novidades e soluções, indicando onde a documentação oficial está salva. Reforçou de forma inequívoca: **“esse handoff não apague e nem substitua tudo o que o GPT decidiu ou planejou para o desenvolvimento desse projeto por lá”**; precisa ser “somatória das decisões e planejamento de lá”.

**[EXECUTADO]** Criado e commitado no GitHub **HANDOFF_INTEGRACAO_CHAT_PRINCIPAL_2026-11-08.md**; índice no **CONTEXTO_MESTRE.md** atualizado. Foi entregue também um longo handoff em bloco de escrita pronto para copiar.

**[DECISÃO]** O chat principal deve: (1) ler seu próprio histórico/checkpoint; (2) ler documentos daqui; (3) classificar cada novidade como já existente, complementar, conflito ou pendência; (4) integrar aditivamente; (5) versionar o resultado; (6) continuar o trabalho, não reiniciar ou migrar sem aprovação.

### 2.6 — 16/11/2026: solicitação atual de documentação integral

**[USUÁRIO]** “Prepare um documento completo na forma mais eficiente para você mesmo ler depois de tudo o que foi dito e decidido nesse chat, sem deixar nada de fora desde a primeira mensagem desse chat”.

**[EXECUTADO nesta atualização]** Este registro detalhado foi criado após reabrir os documentos existentes do GitHub, reler os dois PDFs produzidos e examinar os metadados/identificadores reais dos MP4 e ZIPs disponíveis na conversa. Serve como **memória técnica de alta fidelidade**, com sumário prioritário, cronologia, evidências, decisões, limites, backlog e instruções de retomada.

## 3. ESTUDO DETALHADO — REFERÊNCIA 01 TS MALFOY

### 3.1 Ficha

- URL exata enviada: https://youtu.be/WYRDe8XsRmI?is=H1BwCO2mpf53nZir
- URL canônica: https://www.youtube.com/watch?v=WYRDe8XsRmI
- Título original: 말포이가 여주인 세계선 혼혈왕자편 (TS 말포이)
- Canal/criador: Fantasoner (informado no player da análise anterior).
- Tema: curta de fãs, personagem Draco Malfoy feminina, universo Harry Potter / Enigma do Príncipe.
- Descrição da página: vídeo produzido com IA; músicas citadas na seção 2.1.
- Arquivo fonte recebido: 1000589408.mp4 (detalhes/hashes na seção 5).
- Estética: fantasia gótica em live-action estilizado/realismo generativo, útil como benchmark mesmo que o objetivo final possa ser anime 2D.
- Limite: não se conhece o modelo de IA, o hardware, a frequência real de geração, seeds, base 3D ou método de montagem do autor.

### 3.2 Cronologia de imagens representativas do relatório de nove páginas

| Tempo | Registro visual / construção de cena | Diagnóstico / implicação |
|---|---|---|
| 00:00 | close da abertura, personagem com olhos fechados/abrindo | abertura de olhos, expressão sustentada e luz emocional |
| 00:00–00:02 | sequência comparada ~0,33 s entre amostras | microatuação facial e pouquíssima alteração de pose |
| 00:20 | cama vazia em enfermaria | pausa narrativa e composição ambiental |
| 00:40 | castelo em plano aberto e exterior | cenário gótico, grande escala e atmosfera |
| 01:05 | perfil da protagonista sob contraluz | cabelo iluminado e volume facial |
| 01:20–01:22 | Harry em diálogo | mudança de lábios/mandíbula com tronco contido |
| 01:55 | Harry lendo em luz quente | close, profundidade e pausa |
| 02:05 | escadaria e silhueta | perspectiva arquitetônica |
| 02:40 | personagem junto de pequeno objeto/ave | interação e oclusão potenciais |
| 03:05 | close íntimo | deslocamento facial mínimo |
| 03:25 | perfil junto da janela | contraluz, silhueta e geometria de ambiente |
| 03:40 | vista externa por janela | relação interior/exterior e enquadramento |
| 04:05 | objeto examinado nas mãos, exterior | geometria de mão/objeto a testar |
| 04:20 | diálogo de duas pessoas | campo/contracampo, acting conjunto |
| 04:40–04:42 | Harry interagindo com armário | braço e corpo se deslocam; teste interessante de contato |
| 05:00 | protagonista em perfil, luz recortada | modelagem facial por luz |
| 05:25 | close estático na sombra | microexpressões |
| 05:40 | confronto em terraço, personagem idoso | tensão, cenário e iluminação |
| 06:20–06:22 | braço apontado, ameaça/feitiço | gestual ancorado, fala/cabelo em movimento localizado |
| 06:40 | sapatos e objeto no chão | tensão por detalhe físico |
| 07:15–07:17 | duas personagens lado a lado | boca/expressões variam mais que as posturas |
| 07:45 | personagem de cabelos negros em close | acting e composição |
| 08:15 | silhueta no escuro com deslocamento lateral | movimento/controlabilidade em iluminação baixa |
| 08:40–08:42 | Harry em close com fundo quente/partículas | rosto quase imóvel, brilho do fundo sustenta ritmo |
| 08:50 | cabana em chamas ao anoitecer | escala, efeitos e conclusão dramática |
| 09:04 | término | completar com som/edição conforme obra |

### 3.3 Avaliação

**Pontos que o usuário quer superar mantendo o que funciona:**
- fotografia: contraste, luz recortada, contraluz, texturas, profundidade de campo;
- direção: close, plano amplo, corredores, ambientes internos, campo/contracampo;
- emoção: lágrimas, tensão, olhares, pausas, montagem dramática;
- cenário: ambientes góticos consistentes nos trechos vistos e forte impacto visual.

**Deficiências/risco de IA e de direção observados:**
- movimento limitado a boca, olhos, cabelos e pequenas inclinações;
- respostas emocionais com pouco ajuste do corpo (pescoço, ombros, respiração, distribuição do peso);
- ações de longa duração, interações de mão, contatos, articulações complexas e movimento de câmera desafiadores;
- um plano bem composto não comprova continuidade geométrica em mudança forte de perspectiva.

**Método/limites:**
- análise sequencial computacional de todo o vídeo e amostragem visual pontual; não inspeção humana de cada frame;
- valor 46,1% corresponde a transições muito parecidas num cálculo reduzido, não quadros travados;
- preservar a diferença entre cena estática artisticamente deliberada e falha;
- qualidade de rosto/roupa “aparentemente estável” em trechos não garante perfeição do vídeo inteiro.

**Conclusão incorporada:** usar a força cinematográfica/expressiva da referência e adicionar controle anatômico, espacial, de mãos/objetos e direção de performance.

## 4. ESTUDO DETALHADO — REFERÊNCIA 02 SHIFT UP / EVIE / BLOODRAIN

### 4.1 Ficha

- Nome do videoclipe: “Wanna be in LOVE”.
- Personagem: Evie.
- Associação: Shift Up / Stellar Blade: BLOODRAIN.
- Arquivo fonte recebido: 1000589429.mp4.
- Arquivo: 1920×1080, H.264, 24 fps, 5.222 frames, contêiner 217,663855 s, áudio AAC estéreo 44,1 kHz.
- Não estabelecer valor de orçamento, GPUs “NASA”, serviço ou modelo de IA usados; isso não foi demonstrado.
- Reportagens citadas na conversa afirmam que a construção da personagem partiu do trabalho humano de artistas/modeladores; a produção audiovisual utilizou IA. O “making of” entre aproximadamente 03:00–03:28 é fictício/encenado por IA, não evidência de um set de filmagem.
- Análise real: painéis a cada aproximadamente 5 s; comparações de oito quadros ao longo de 3 s (~0,375 s); varredura computacional em cada terceiro frame, **não auditoria perceptual manual de todos os 5.222 frames**.

### 4.2 Timeline detalhada e oportunidades

| Trecho | O que foi identificado | Acertos / possíveis falhas |
|---|---|---|
| 00:00–00:10 | microfone retrô em primeiro plano, revelação de Evie, letras/título, prédios, cabos e tubos | excelente introdução pelo prop, profundidade, escala e composição |
| 00:10–00:18 | cantora de macacão branco em plano frontal, canto e expressão | boca/olhos mais ativos que tronco, ombros e mãos; testar respiração |
| 00:12–00:15 | tira temporal em intervalos ~0,375 s | microvariação de lábios, olhar, cabeça e expressão; necessidade de acting total |
| 00:18–00:21 | transição de close extremo dos lábios para olhos/rosto | alteração relativa de olhos e estilização do rosto entre planos; não ignorar se acidental |
| 00:25–00:35 | tipografia, performance de perfil e cena em metrô, olhar de baixo para cima | entre ~00:33–00:35, contorno facial/olhos/cabelo variam perceptivelmente; motion blur/lente podem contribuir |
| 00:35–01:00 | trem, mercado, cidade e performance ao microfone em diferentes ângulos | montagem variada e cortes que evitam tomadas de ação longas |
| 01:00–01:14 | multidão, interiores de trabalho e passarela com vista sobre a cidade | sensação de escala e parallax; figurinistas/caminhadas e mãos dos figurantes necessitam QA |
| 01:15–01:35 | canto lateral, chuva, construção industrial, passarelas, câmera movendo | atmosfera forte; monitorar microfone/pedestal e limites do figurino |
| 01:35–01:45 | rua/mercado, Evie abaixando junto de outra figura | verificar joelhos, peso, contato, apoio e oclusões |
| 01:45–01:55 | Evie com hashi e comida, ambiente movimentado | geometria mão-hashi-comida e trajetória persistentes |
| 01:55–02:00 | objeto pendente segurado diante de robô, corredor/rua | fingers, topologia, reflexo, oclusão, escala e persistência do objeto |
| 02:00–02:15 | jardim em cidade densamente construída, performance e câmera em movimento | contraste orgânico-industrial, establishing shots, parallax e continuidade |
| 02:15–02:20 | planos de perfil/corpo inteiro, câmera inclinada, personagem girando | diferenciar giro de câmera e rotação corporal, preservando proporções |
| 02:20–02:26 | sorriso, close de olhos, selfie com smartphone, gesto em V | ângulos de mão/celular, contagem de dedos, contato, perspectiva |
| 02:26–02:35 | caminhada sob guarda-chuva amarelo e reflexos nas poças, corredor industrial | cor focal, câmera; foot sliding, sombra/reflexo, geometria do guarda-chuva |
| 02:35–02:50 | personagem sentada ao lado de vegetação, close de perfil | variação de emoção e pausas; cabelo/roupa/silhueta cross-shot |
| 02:50–03:00 | Evie deitada em microjardim, cartela | descompressão narrativa, plano contido |
| 03:00–03:28 | falso making-of com diretor, operador, câmeras, luzes, contatos interpessoais | aparência de bastidores não é prova do método; mãos/câmeras/objetos e continuação de corpos difíceis |
| 03:28–03:37,66 | cartelas e finalização | não extrapolar da ficção para descrição do workflow |

### 4.3 Direção de arte a preservar como inspiração (não como cópia)

- cidade futurista vertical, construções densas, passarelas, tubulações, neblina, materiais industriais, grande profundidade;
- paleta coerente cinza-esverdeada/âmbar, contraste entre macacão branco/microfone e espaços densos;
- textura úmida, chuva, piso refletivo, luz volumétrica, vegetação inserida em ambientes industriais;
- estrutura musical: performance + cenas cotidianas + transições + epílogo; variedade de planos e foco narrativo;
- objetos como âncoras visuais; alternância de objeto primeiro e personagem depois;
- enquadramentos intencionais: close, medium, wide, perfil, inclinados, câmera em movimento.

### 4.4 Falhas, suspeitas e investigação ainda aberta

1. **[USUÁRIO; prioridade P0] Microfone levemente fora de perspectiva em rotações de câmera.** Hipóteses testáveis: eixo, pivô, rotação do pedestal, altura relativa à boca, escala projetada, profundidade, lente/FOV, parallax, contato, sombras ou oclusão. Não considerar só a detecção de drift facial.
2. **[USUÁRIO; prioridade P0] Proporções corporais variam entre tomadas.** Medir razões de cabeça/corpo, busto/torso, largura de ombros, cintura/quadril, extensão de braços e pernas, mãos/pés e silhueta. Variabilidade deve ser normalizada pela projeção; ângulo, pose, roupa, motion blur e focal não devem ser falsamente considerados erro de anatomia.
3. **[ANÁLISE] Rosto altera traços/estilização** em 00:18–00:21 e 00:33–00:35, incluindo aparência dos olhos/mandíbula/contorno. Parte é suspeita, não demonstração causal de IA.
4. **[ANÁLISE] Lip-sync e atuação global:** boca movimenta enquanto tronco/ombro/pescoço ficam contidos; o áudio não foi tecnicamente alinhado por fonemas, portanto não declarar erro fonético específico comprovado.
5. **[ÁREA DE RISCO] Mãos, dedos, contato e props:** hashi, alimento, pendente, robô, smartphone, gesto em V, guarda-chuva, microfone, cumprimentos e equipamentos dos “bastidores”. Nem todos os quadros representam falha comprovada.
6. **[ÁREA DE RISCO] Física e continuidade:** foot sliding, agarramento, joelho, gravidade, colidir com chão, câmeras que orbitam, sombras, reflexos, cabelagem, figurino, oclusões e interação entre pessoas.
7. **[USUÁRIO] “entre outras”:** o catálogo de defeitos permanece aberto. Revisão precisa ser mais crítica que os relatórios iniciais; falhas sutis de engenharia visual são tão importantes quanto artefatos óbvios.
8. **[LIMITE]** Os cuts rápidos podem mascarar transições incertas; não confundir montagem competente com animação tecnicamente estável.
9. **[LIMITE]** Não atribuir os defeitos à tecnologia exata, pois pipeline e assets internos não estão disponíveis.

### 4.5 Comparação qualitativa entre as duas obras

- **TS Malfoy:** ~9 min, dramático/fantasia gótica, boa atuação facial e luz, muitos planos sustentados; útil para ritmo narrativo e identidade emocional.
- **Shift Up:** ~3m38s, urbano-industrial e musical, grande diversidade de planos e cenários, cor e worldbuilding excelentes; desafios acentuados de câmera/prop/corpo/identidade.
- **Composição desejada no projeto:** reunir a força narrativa/luz de TS Malfoy e a escala/worldbuilding/variedade de Shift Up com controles de geometria, anatomia, movimento e continuidade mais robustos do que os das duas referências.

## 5. INVENTÁRIO EXATO DOS ARQUIVOS ENTREGUES E GERADOS

Os MP4, relatórios e ZIPs estavam disponíveis neste ambiente ao compilar este registro. Hashes SHA-256 foram calculados a partir dos bytes atuais; usam-se para distinguir arquivos homônimos e reconfirmar integridade. **Não assumir que caminhos locais de uma conversa ficarão montados em outra sessão.** Os binários não foram copiados para o GitHub.

| Arquivo | Tipo / conteúdo | Bytes | SHA-256 |
|---|---|---:|---|
| 1000589408.mp4 | vídeo original TS Malfoy | 81530392 | a49a8262f1a5944008b0195f21c17d7ac8d34d1fd395757294340035d9f6a55f |
| 1000589429.mp4 | vídeo original Shift Up Evie | 79784442 | 971c9a54886b628d32d7109004eaa0a0c772fe1b498d6ad95828ecb8ccfef342 |
| Analise_Tecnica_TS_Malfoy_Animacao_IA.pdf | PDF técnico 9 páginas | 1584007 | 2da08560b6e3c2af6557f65d903333dd89c0393be5e55c6a7f9f2dd3bf8df071 |
| Evidencias_Visuais_TS_Malfoy.zip | 12 evidências e PDF | 2803934 | e35b545c0922aa35af0456193c917c2c42064865d09d30a1c8a93a0f7469a589 |
| Relatorio_ShiftUp_Bloodrain_Analise_Audiovisual.pdf | PDF técnico 10 páginas | 2282876 | 999744ab946c864421231c3df47d7b6d0a2ffdeedc3ee78e4a8d0db82555bd7c |
| Evidencias_Quadros_ShiftUp_Bloodrain.zip | 18 montagens/quadros | 4083348 | 7f9db6ba51398e8a487bc1d3c8539b85f7d8006910f207b46c6d05b50d1722d7 |

**Detalhe dos ZIPs:**

- TS Malfoy: Relatorio_Analise_Tecnica.pdf; Visao_Geral_A_Cada_5s_01.jpg a 05.jpg; Comparacao_Quadros_000.jpg, 080.jpg, 280.jpg, 380.jpg, 435.jpg, 520.jpg.
- Shift Up: contact_01.jpg, contact_02.jpg, contact_03.jpg, contact_04.jpg; strip_012.jpg, strip_018.jpg, strip_033.jpg, strip_069.jpg, strip_087.jpg, strip_111.jpg, strip_115.jpg, strip_135.jpg, strip_145.jpg, strip_170.jpg, strip_185.jpg, strip_200.jpg; highres_1.jpg e highres_2.jpg.

**Links usados na resposta anterior (válidos apenas quando o arquivo exato estiver disponível no ambiente de conversa):**
- sandbox:/mnt/data/Analise_Tecnica_TS_Malfoy_Animacao_IA.pdf
- sandbox:/mnt/data/Evidencias_Visuais_TS_Malfoy.zip
- sandbox:/mnt/data/Relatorio_ShiftUp_Bloodrain_Analise_Audiovisual.pdf
- sandbox:/mnt/data/Evidencias_Quadros_ShiftUp_Bloodrain.zip

**Observação sobre vídeo:** os contadores de frames correspondem ao fluxo principal H.264; os MP4 também contêm áudio AAC e uma imagem/anexo MJPEG. A taxa do arquivo não prova a taxa original de geração por IA.

## 6. REQUISITOS CUMULATIVOS DE ENGENHARIA EXTRAÍDOS DA CONVERSA

### R-01 — Personagem mestre e identidade multivista

- Modelo/canonical sheet único: frente, perfil, costas, 3/4, poses neutras, expressões, roupas, acessórios, penteado e paleta.
- Proporções relativas aprovadas: altura em cabeças, largura de ombro, peito/torso, cintura, quadril, braço/antebraço, coxa/perna, mãos e pés.
- Não misturar aparência frontal gerada independente de perfil. Persistir rig/mesh/referências e controlar mudanças estilísticas deliberadas.
- Verificar consistência entre planos após considerar câmera, pose e iluminação; “silhueta parece diferente” precisa de teste, não apenas impressão.

### R-02 — Cinematografia espacialmente coerente

- Shot spec inclui câmera como objeto com posição/rotação, focal/FOV, clipping, trajetória, enquadramento, blocking, movimento e luz.
- Cenário tem escala definida, layout e relações de profundidade persistentes.
- Teste específico de **rotação de câmera ao redor da cantora e microfone**, avaliando parallax, projeção, escala/oclusão e anatomia. A câmera não pode fazer o microfone “sair” do espaço plausível.
- Separar movimento de câmera e do personagem; atentar a lentes distintas e poses.

### R-03 — Props e contato

- Cada prop tem asset_id persistente, malha/contorno, pivô, material, socket, dono, estado, transform no mundo e regras de contato.
- Microfone em pedestal: ligado ao mundo; microfone de mão: ligado ao rig com IK e constraints; os dois exigem oclusão, sombras, reflexos e distância para a boca corretas.
- Mãos e utensílios devem mover-se juntos como geometria relacionada; evitar fusão, desaparecimento ou duplicação de dedos/objetos.
- Utilizar passes/máscaras/retakes curtos para corrigir sem regenerar tudo.

### R-04 — Movimento humano e atuação

- Rig 2D/3D, IK/FK, root motion, movimento secundário e antecipação, contato pés-chão, peso e equilíbrio.
- Integração de músculos faciais/olhar, mandíbula, língua quando visível, pescoço, ombro, tórax, respiração e emoção.
- Lip-sync: alinhar áudio/fonemas/visemas, depois naturalidade de expressão/corpo; não basta mandíbula abrir/fechar em ritmo aproximado.
- Para anime 2D, combinar rig e desenho substituto por ângulo, evitando deformação mecânica exagerada.

### R-05 — Arte, arquitetura, mundo e continuidade

- Cenários 3D otimizados ou multiplano 2D com perspectiva/oclusão controlada.
- Bíblia de cenário: plantas/layout, escala, portas/escadas/objetos, materiais, iluminação e horário; câmera e personagem ocupam mundo estável.
- Preservar estilo artístico sem copiar cenários concretos de obras alheias.
- Montagem com close/plano médio/plano aberto, pausas, música, ambientação, atmosfera e cortes planejados; usar edição para efeito dramático, não para esconder falhas sistematicamente.

### R-06 — IA como ferramenta do pipeline, não substituta de controle

- Opções: gerar concept sheets, quadros-chave, texturas, fundos, stylization de render/rig, refinamento de tomadas e vídeo curado.
- Manter motor selecionável conforme cena, orçamento, personagem e exigência de ação; catálogo de métodos previamente pesquisados pelo chat principal deve sobreviver.
- Registrar modelo/versão, seed se disponível, prompts, arquivos de referência, máscaras, frames de entrada/saída, duração e restrições de uso.
- Evitar reconstruir o mundo, a face e o prop do zero em cada quadro; adicionar controle temporal.

### R-07 — QA automatizado e humano

- Auditar continuidade temporal e entre planos: landmarks e identidade, proporções normalizadas, qualidade de face, corpo, mãos, pés, props, oclusão, geometria, roupa, fundo, iluminação, flicker, ghosting e cortes.
- QA deve diferenciar movimento de câmera/corte, expressão/pose deliberada e drift indevido.
- Cada falha precisa de id, timestamp, frame, shot_id, gravidade, evidência, diagnóstico provável, proposta de correção e status.
- Falhas críticas em rosto/corpo, microfone/câmera, mãos e props reprovam o take; revisão humana confirma.
- Diff simples de pixel é só indicador técnico; não comprova congelamento, identidade nem causa IA.
- Em plano aprovado, executar inspeção sequencial de todos os quadros exportados (idealmente assistida por mecanismos automáticos mais revisão humana de ocorrências).

### R-08 — Áudio, edição e acabamento

- Música, voz, efeitos, desenho de som, ritmo e montagem devem integrar a especificação do take.
- Edição e composição final gratuitas, com FFmpeg/editor compatível.
- Exportar vídeo e também fontes/projetos/metadata para revisões sem recriação completa.

## 7. ARQUITETURA CANDIDATA E PROVA DE 15 SEGUNDOS

### 7.1 Fluxo não destrutivo sugerido

1. **Brief + cânone:** personagens, estética (anime 2D, 3D, híbrida), contexto narrativo, assets e restrições.
2. **Preprodução:** bíblia de personagem/proporções, cenário com planta/escala, roteiro, storyboard, animatic e shot list.
3. **Shot spec:** IDs de plano, duração, câmera, lente, ação, atuação, falas e fonemas, objetos, blocking, iluminação, rigs, perspectiva, continuidade e riscos.
4. **Bloqueio 2D/3D:** câmera e geometria, corpo/IK, props e contato; priorizar movimento controlável antes de stylization.
5. **Geração IA seletiva:** keyframes, materiais, estilização, refinamento e tomadas onde os métodos livres sejam confiáveis; preservar estados e seeds.
6. **Composição:** camadas, máscaras, sombras, reflexos, partículas, correções localizadas.
7. **QA:** auditoria de toda tomada e comparação cross-shot por atributos, incluindo perspectiva de microfone e proporções corporais.
8. **Montagem e áudio:** edição, mixagem e export via editor/FFmpeg.
9. **Entrega/versionamento:** MP4, arquivos-fonte, especificações, relatório de defeitos, medições de hardware/tempo/custo e checkpoint aprovado.

Este fluxo é uma **proposta documentada**. O chat principal poderá já ter arquitetura mais avançada ou diferente; conciliar e incorporar somente o que somar valor.

### 7.2 Piloto proposto (Issue #12, não homologado)

**Duração alvo:** ~15 segundos, com 2–3 planos, personagem original e cenário persistente.

- **Plano A:** face em fala ou canto; boca/mandíbula, olhos, expressão, ombro/pescoço, respiração e identidade.
- **Plano B:** corpo inteiro com deslocamento, mudança de direção e/ou câmera; proporções estáveis, apoio correto e roupa consistente.
- **Plano C:** personagem interage com microfone ou objeto ao variar fortemente a perspectiva; câmera orbita/muda ângulo, objeto mantém geometria, distância, escala, sombras, contato e oclusão.
- **Possível complexidade complementar:** segunda personagem ou outro contato, se a prioridade original do projeto assim exigir; não impor como reordenação.
- **Gate P0:** sem drift estrutural de face, sem mudança espontânea de proporções, sem microfone fora da geometria de câmera, sem deformação crítica de dedos, sem foot sliding grave, sem teleporte de cenários/objetos.
- **Revisão final:** todos os frames entregues, inclusive entradas/saídas de corte, com relatório de incidentes, memória, tempo e custo e aprovação artística.
- **Status:** BACKLOG / PROPOSTA; não há prova neste chat de produção real nem de software homologado.

### 7.3 Ferramentas candidatas gratuitas, sujeitos a testes

| Ferramenta | Uso pretendido | Situação documentada |
|---|---|---|
| Blender / versões compatíveis | rig, IK, câmera, assets, Grease Pencil, shape keys, EEVEE, renders | candidato, não validado integralmente neste chat |
| OpenToonz / Plastic Tool | mesh e deformação de 2D entre keyframes | candidato, não homologado |
| Rhubarb Lip Sync | fonemas/visemas para animação 2D, adaptação a 3D | candidato, naturalidade PT-BR precisa validação |
| FFmpeg | extração, comparação, transcodificação, composição, export | utilizado na pesquisa de arquivos; pipeline de produção não homologado |
| Motores generativos/motion capture/retargeting anteriormente pesquisados | geração supervisionada por cena | consultar catálogo vigente no projeto principal; não remover ou instalar cegamente |
| Nuvem GPU grátis | eventuais tomadas custosas | não assumir cota ou acesso persistente |

**Hardware:** AMD FX-4300/16 GB/RX 580 8 GB é limitante para vídeo difusivo pesado. Testar versões de Blender/driver; na GPU RX 580 Polaris, o caminho Cycles GPU via HIP moderno não é suportado. Cenários leves, passes, proxies, CPU e soluções específicas podem ajudar; não prometer longa produção estilo estúdio com custo financeiro nulo e sem custo de trabalho humano.

## 8. DOCUMENTAÇÃO DO GITHUB, LINKS, COMMITS E ESTADO

### 8.1 Repositório existente, efetivamente acessado

**Conta/repositório:** https://github.com/Furuya29/furuya-motion-studio  
**Visibilidade verificada:** público.  
**Branch:** main.  
**Pasta de pesquisa:** https://github.com/Furuya29/furuya-motion-studio/tree/main/docs/projeto-animacao-automatizada

Arquivos criados por este chat, com links diretos:
- **CONTEXTO_MESTRE.md:** https://github.com/Furuya29/furuya-motion-studio/blob/main/docs/projeto-animacao-automatizada/CONTEXTO_MESTRE.md
- **REFERENCIA_02_SHIFTUP_BLOODRAIN_2026-11-08.md:** https://github.com/Furuya29/furuya-motion-studio/blob/main/docs/projeto-animacao-automatizada/REFERENCIA_02_SHIFTUP_BLOODRAIN_2026-11-08.md
- **HANDOFF_INTEGRACAO_CHAT_PRINCIPAL_2026-11-08.md:** https://github.com/Furuya29/furuya-motion-studio/blob/main/docs/projeto-animacao-automatizada/HANDOFF_INTEGRACAO_CHAT_PRINCIPAL_2026-11-08.md
- **ESTE REGISTRO INTEGRAL:** https://github.com/Furuya29/furuya-motion-studio/blob/main/docs/projeto-animacao-automatizada/REGISTRO_INTEGRAL_CHAT_REFERENCIAS_2026-11-07_A_2026-11-16.md
- **Issue #12 (piloto):** https://github.com/Furuya29/furuya-motion-studio/issues/12

**Commits confirmados ao longo da conversa anterior:**
- 07816623bfc79e727df82e6995316d990bdbe0f7 — criou contexto mestre inicial e preservou TS Malfoy.
- b64b8827a301a06eb5e6a59d25a56653f26033ff — criou documento Shift Up.
- 315b89a23c05c8f814a1860d45992806437c8803 — vinculou referência Shift Up e issue ao contexto.
- a5138dff36f6bd229df74c5f7da5d47b841fd945 — adicionou correção do usuário sobre microfone/perspectiva/proporções.
- 5239da746d8baf2694507c00d18a0a21beff745d — salvou handoff de integração aditiva.
- 26f538640da36280c022d9755cc988df33de8926 — indexou handoff no contexto mestre.
- O commit deste arquivo deverá ser registrado na resposta de conclusão desta atualização.

**Não confundir documentação com código implementado**: esses commits são Markdown/organização, não provas de entrega do motor 2D/3D. A issue #12 foi aberta, não declarada concluída.

### 8.2 Fontes de consulta externa mencionadas na pesquisa anterior

- Página original TS Malfoy: https://www.youtube.com/watch?v=WYRDe8XsRmI
- Videogames Chronicle (31/07/2026, contexto Shift Up): https://www.videogameschronicle.com/news/are-we-deadass-fans-react-to-official-ai-generated-stellar-blade-music-video/
- AJP (03/08/2026): https://m.ajupress.com/amp/20260803150638274
- Push Square (contexto Evie e declarações): https://www.pushsquare.com/news/2026/08/evie-was-created-by-our-talented-artists-stellar-blade-dev-responds-to-ai-slop-accusations
- GamesRadar (reações/críticas): https://www.gamesradar.com/games/action/stellar-blade-blood-rain-gets-official-music-video-full-of-ai-slop-and-fans-arent-happy-its-a-slap-in-the-face-to-your-artists/
- Blender requisitos: https://www.blender.org/download/requirements/
- Blender Cycles/HIP: https://docs.blender.org/manual/id/4.5/render/cycles/gpu_rendering.html
- OpenToonz Plastic Tool: https://opentoonz.readthedocs.io/en/latest/create_animations_using_plastic_tool.html
- Rhubarb Lip Sync: https://github.com/DanielSWolf/rhubarb-lip-sync

URLs são referências que constaram de estudos e documentos desta conversa; ao tomar novas decisões dependentes de versões/licenças/fatos externos, revalidar data e disponibilidade.

## 9. ERROS, INCERTEZAS E DISTINÇÕES OBRIGATÓRIAS

1. **Duração falsa de 2:13:** ocorreu apenas porque o navegador do YouTube estava bloqueado por anúncio. Descartar; usar arquivo real de ~09:04 para TS Malfoy.
2. **9:05 preliminar:** arredondamento/estimativa anterior. O número sólido é 16.328 frames a 30 fps (tempo de imagens ~544,27 s) e contêiner ~544,37 s.
3. **“Frame a frame” não significa que cada frame foi examinado visualmente por um humano:** houve análise automática do conjunto e inspeções visuais por amostragem; ser transparente. Para aceitação final do nosso pipeline, prever auditoria mais rigorosa.
4. **46,1% do Malfoy não indica quadros congelados:** métrica com threshold de diferença luminosa em imagem reduzida.
5. **Erros em mãos, figurantes, pés e objetos na Shift Up:** alguns são riscos a examinar, não defeitos comprovados em minutagem específica; não descrever o risco como falha medida.
6. **Perspectiva de microfone e proporções corporais:** achados expressos pelo usuário; preservá-los como requisitos prioritários e validar sua manifestação e gravidade em frames concretos.
7. **Lip-sync:** movimento de boca observado; nenhum alinhamento automatizado por fonema foi demonstrado. Não afirmar quantitativamente que está fora de sincronia sem executar teste.
8. **Custo/equipamentos da Shift Up:** não há prova de “hardware da NASA”, supercomputadores ou cifra exata de orçamento. “Um ano de trabalho artístico na personagem” não equivale a “um ano ou orçamento do videoclipe”.
9. **Falso making-of:** sequência de set encenada não revela processo real.
10. **Blender/EEVEE/RX 580:** capacidades reais dependem de versão/driver; não afirmar EEVEE homologado no PC sem teste; RX 580 não satisfaz HIP Cycles GPU moderno.
11. **GitHub público:** não enviar material protegido/privado. Não dizer que PDFs, ZIPs e MP4s estão no GitHub quando apenas os documentos Markdown e a issue foram salvos.
12. **Arquitetura principal não lida integralmente:** nada aqui autoriza substituir decisões, stacks, motores, aprovações ou metas estabelecidos fora desta conversa.
13. **Os dois vídeos são referências, não assets oficiais do nosso produto:** não redistribuir conteúdo protegido.
14. **Status de disponibilidade de links sandbox:** somente apresentar links de download quando caminho existe na sessão atual; outro chat pode precisar do upload ou localizar os materiais no projeto.
15. **Data de compilação diferente da data das decisões:** análises principais ocorreram 07–08/11/2026, este registro foi compilado em 16/11/2026. Não confundir com um experimento novo de 16/11.

## 10. BACKLOG UNIFICADO E STATUS — NÃO USAR COMO REORDENAÇÃO AUTOMÁTICA

| Item | Importância | Status nesta conversa | Dependência / verificação |
|---|---|---|---|
| Preservar estudos Malfoy e Shift Up em texto | Alta | **feito no GitHub** | documentos e links conferidos |
| Incorporar observação microfone nas rotações | Crítica | **documentado, teste pendente** | baseline de câmera/prop |
| Controlar proporções anatômicas cross-shot | Crítica | **documentado, teste pendente** | bíblia de personagem, rig, landmarks |
| Definir shot spec único | Alta | proposto | comparar com schema do chat principal |
| Implementar rigs e contato físico | Alta | proposto | motor e hardware escolhidos no principal |
| Testar animação facial e lip-sync PT-BR | Alta | proposto | áudio, fonemas, visemas e revisão |
| Construir ambiente persistente e câmera orbitante | Alta | proposto | viewport/performance locais |
| QA temporal e cross-shot com classificação de falhas | Alta | proposto | capturas e métricas contextualizadas |
| Sistema de retake/repair localizado | Média/alta | proposto | passes/máscaras e projeto-fonte |
| Piloto ~15 s, três tipos de tomadas | Alta como benchmark | **Issue #12 aberta; sem homologação** | prioridades do chat principal |
| Integrar handoff no desenvolvimento principal | Alta | **handoff criado; adoção não confirmada nesta conversa** | chat principal precisa ler e conciliar |
| Validar repositório canônico do projeto principal | Alta | **pendente** | reconciliar documentação entre chats |
| Validar Blender/OpenToonz/Rhubarb/FFmpeg no PC | Alta | **pendente**, salvo uso de FFmpeg na análise | testes reais de versão/memória/GPU |
| Criar política de preservação de binários | Média | não decidido | direitos autorais, limites de armazenamento |

**Estado total:** documentação e pesquisa avançadas; nenhum mecanismo de animação foi homologado neste chat. Não confundir trabalho no repositório Furuya Motion Studio com alterações funcionais no pipeline original.

## 11. INSTRUÇÕES DE RETOMADA PARA UMA FUTURA INSTÂNCIA DO GPT

Este é o procedimento que um futuro GPT deve executar ao receber este arquivo:

1. **Ler a seção 0** e entender que tudo é cumulativo.
2. **Ler o histórico integral deste arquivo**, especialmente as seções 2, 3 e 4 (referências, correções do usuário e limites de evidência).
3. **Consultar no GitHub** CONTEXTO_MESTRE.md, REFERENCIA_02_SHIFTUP_BLOODRAIN_2026-11-08.md e HANDOFF_INTEGRACAO_CHAT_PRINCIPAL_2026-11-08.md.
4. **Recuperar do próprio chat principal** o planejamento de animação vigente e o último checkpoint real. A documentação presente **não tem autoridade para substituir esse conteúdo**.
5. Montar matriz de reconciliação: decisão antiga, evidência/novo requisito desta pesquisa, duplicação, complementaridade, conflito, testes restantes, caminho de integração.
6. Preservar as tecnologias já aprovadas, somente acrescentar testes e controles geométricos úteis, sem reinstalar, reorganizar ou cancelar trabalhos sem motivo.
7. Integrar os controles de microfone/câmera e proporções corporais como QA de prioridade alta, sem esquecer encenação, atuação, áudio, cenários e montagem.
8. Antes de prometer produção, **testar no hardware real, custos, licenças, acesso e formatos**.
9. Preservar cada novo achado em Markdown versionado, com data, origem, nível de evidência, decisão, responsável e status. Se houver novo vídeo, repetir metadados, amostragem temporal e QA.
10. Ao concluir alguma entrega, anexar prova real e atualizar status; não transformar proposta em “implementado” por ser repetida em vários documentos.
11. Manter **estética original desejada pelo usuário** e não transferir compulsoriamente estética da Fantasoner/Shift Up para os personagens próprios.
12. Não declarar que “tudo foi copiado para o GitHub”: só estes documentos e os links estão lá; materiais binários foram entregues na conversa.
13. Ao detectar incompatibilidade com o planejamento principal, registrar conflito e solicitar decisão específica em vez de substituir silenciosamente.

## 12. ORDEM PERMANENTE DE NÃO REGRESSÃO

> **INTEGRAR, SOMAR, PRESERVAR E DAR CONTINUIDADE.**
>
> Os achados desta conversa ampliam o nível de exigência do Projeto de Animação Automatizada: mais controle de personagem, corpo, câmera, objetos, relações físicas, atuação e qualidade temporal. **Eles NÃO revogam, não sobrescrevem e não invalidam a arquitetura, os motores, as decisões artísticas ou o backlog que o chat principal já estabeleceu.** A próxima instância deve começar da última situação aprovada no projeto principal, reconciliar as novidades e avançar.

**Fim do registro integral semântico desta conversa — versão de 16/11/2026.**
