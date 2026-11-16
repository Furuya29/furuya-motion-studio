---
document_id: PAA-HANDOFF-CHAT-REFERENCIAS-2026-11-16
titulo: Handoff integral do chat de pesquisa, referências e qualidade cinematográfica
data_corte: "2026-11-16"
idioma: pt-BR
escopo: "Conversa integral desde https://youtu.be/AZDzT-4OIY8 até a solicitação de handoff completo"
natureza: "Registro cumulativo de continuidade e recuperação de contexto"
status: "DOCUMENTADO; não equivale a homologação ou mudança de prioridades"
repositorio: Furuya29/furuya-motion-studio
branch_de_registro: docs/animacao-integracao-cumulativa-20261109
pr_integracao: 13
issue_piloto: 12
---

# HANDOFF MESTRE — PESQUISA CINEMATOGRÁFICA E ANIMAÇÃO AUTOMATIZADA
**Projeto:** Projeto de Animação Automatizada — The Darkness of Aenvarath  
**Data do registro:** 16/11/2026  
**Base:** toda esta conversa, incluindo a transcrição do handoff oficial de 08/11, links fornecidos, constatações do assistente, MP4s anexados, pranchas geradas e registros GitHub consultados.  
**Uso esperado:** entregar este arquivo a um futuro chat para que ele recupere decisões, evidências, prioridades, riscos, links e próximos passos **sem solicitar novamente o que já foi fornecido**.

> AVISO SUPERIOR E VINCULANTE — ESTE DOCUMENTO É ADITIVO. NÃO REINICIAR O PROJETO, NÃO DESCARTAR NENHUM PLANEJAMENTO, MÉTODO, FERRAMENTA, REFERÊNCIA, MODELO, QUADRO OU CHECKPOINT PREVIAMENTE APROVADO. NÃO MESCLAR AUTOMATICAMENTE PRS, NÃO MUDAR PRIORIDADES SEM CONSENTIMENTO E NÃO CHAMAR PESQUISA OU TESTE GEOMÉTRICO DE ANIMAÇÃO ARTÍSTICA HOMOLOGADA.

## 0. INSTRUÇÕES DE LEITURA E HIERARQUIA DE EVIDÊNCIA

Este documento foi preparado para preservar **todo o conteúdo substantivo, links, decisões, observações, dificuldades, ressalvas e resultados** surgidos neste chat, desde a primeira mensagem até a solicitação atual. Não é uma transcrição literal de todas as saudações ou mensagens de progresso, mas mantém a sequência integral de assuntos, os detalhes operacionais, as decisões e suas fontes. O texto completo do handoff fornecido pelo proprietário em 08/11 está preservado no arquivo original no GitHub, referenciado na seção 2 e reproduzido semanticamente de forma detalhada nas seções 4–8. Para verificação palavra por palavra, consultar o original; este registro não o reescreve nem o apaga.

**Taxonomia obrigatória:**
- **PROPOSTO / PESQUISA:** sugestão ou tema a investigar; nenhum código/render validado por essa classificação.
- **METADADOS VERIFICADOS:** título/descrição de plataforma ou ffprobe; não significa que o vídeo foi assistido.
- **OBSERVADO EM MP4:** fato visual derivado de amostragem real de frames/trechos, com as limitações de cobertura declaradas.
- **HIPÓTESE / FALHA CANDIDATA:** aparência suspeita, ainda sem demonstração técnica conclusiva.
- **IMPLEMENTADO EM CÓDIGO:** função presente no repositório/branch; não demonstra render artístico nem execução no PC.
- **TESTADO EM AMBIENTE ISOLADO:** execução real de ensaio, mas não no equipamento do proprietário.
- **EXECUTADO NO PC:** requer registro/recibo de máquina produtiva; **não comprovado neste chat**.
- **APROVADO ARTISTICAMENTE / HOMOLOGADO:** exige prova de vídeo, fontes, QA e aceite humano; não presumir a partir de resultados anteriores.

É expressamente proibido atribuir um motor de IA, orçamento, hardware, fluxo de produção ou capacidade permanente a qualquer referência apenas pela estética ou por propaganda. Distinguir o que o **proprietário observou**, o que foi **inspecionado no arquivo** e o que surgiu de **pesquisa pública**.

## 1. OBJETIVO ARTÍSTICO E INTENÇÃO EXPLÍCITA DO PROPRIETÁRIO

A intenção foi reiterada ao longo do chat e culminou na frase: **“Eu quero fazer meus vídeos com essa qualidade absurda e direção e edição.”** As referências foram enviadas para estudar e incorporar **qualidade audiovisual de altíssimo nível**, inclusive animações longas de fantasia, criaturas/elfos, atuação e montagem narrativa.

O projeto deve desenvolver um **estúdio próprio de produção cinematográfica automatizada**, e não simplesmente um gerador de imagens estáticas, slides animados ou um serviço dependente de um único provedor. Deve suportar:
- **Anime japonês 2D autêntico**, autoral, sem converter compulsoriamente a estética para CGI/3D nem “estilo Ghibli”.
- **3D realista/semirrealista** e **híbrido 2D/3D** como linguagens opcionais e artisticamente aprovadas; não substituir a identidade canônica das personagens.
- Personagens únicos, turnarounds, proporções, rostos, cabelos, vestimentas e objetos consistentes, inclusive entre ângulos/episódios.
- Cenários monumentais, detalhados e **persistentemente modelados**; geografia, arquitetura e perspectiva estáveis entre tomadas e úteis também para o MMORPG.
- Câmera cinematográfica, encenação, luz, profundidade, composição, acting corporal/facial, lip-sync, interação física, combates, magia, VFX, som, dublagem, transições, edição narrativa e ritmo.
- **Automação máxima com supervisão artística humana**, workflow controlável/reproduzível/inspecionável, reparos localizados e QA temporal/cross-shot.
- Ferramentas gratuitas e orçamento operacional alvo **R$ 0**, sem supor créditos ilimitados, datacenter gratuito ou assinaturas de Runway/Higgsfield/Claude.
- Separação entre **animações originais de Aenvarath** e o projeto conexo **Furuya Motion Studio de substituição de personagens em vídeos existentes**; compartilhar tecnologias sem fundir estado, escopo ou prioridades.

A ambição é **igualar ou superar** visualmente e tecnicamente as referências, mas **não** afirmar que isso já é possível com o hardware e métodos atuais sem demonstração.

## 2. DOCUMENTAÇÃO OFICIAL, FONTES E LOCALIZAÇÃO

**Repositório conectado e verificado via GitHub:** https://github.com/Furuya29/furuya-motion-studio  
**Pasta de pesquisa:** docs/projeto-animacao-automatizada/  
**Branch de trabalho de integração (PR #13, draft):** docs/animacao-integracao-cumulativa-20261109  
**Documentação-mestre publicada na main:** https://github.com/Furuya29/furuya-motion-studio/blob/main/docs/projeto-animacao-automatizada/CONTEXTO_MESTRE.md  
**Handoff oficial de 08/11 (fonte textual íntegra):** https://github.com/Furuya29/furuya-motion-studio/blob/main/docs/projeto-animacao-automatizada/HANDOFF_INTEGRACAO_CHAT_PRINCIPAL_2026-11-08.md  
**Análise Shift Up:** https://github.com/Furuya29/furuya-motion-studio/blob/main/docs/projeto-animacao-automatizada/REFERENCIA_02_SHIFTUP_BLOODRAIN_2026-11-08.md  
**Issue #12 (piloto de 15 s, NÃO homologado):** https://github.com/Furuya29/furuya-motion-studio/issues/12  
**PR #13 (implementações experimentais / reconciliação, draft):** https://github.com/Furuya29/furuya-motion-studio/pull/13

**Documentos que existiam apenas na branch do PR #13 durante este chat:**
- RECONCILIACAO_ADITIVA_2026-11-09.md — matriz de decisões existentes versus novos testes.
- PROTOTIPO_P15_EXECUTAVEL_2026-11-09.md — renderizador geométrico / animatic técnico.
- MODULO_RIG_2D_SPRITES_2026-11-09.md — sprites, pivôs, FK e keyframes.
- CHECKPOINT_CUMULATIVO_2026-11-16.md — atualização desse chat com Nólyrien e primeiras referências.
- REFERENCIA_06_FERRAMENTAS_CHINESAS_VIDEO_2026-11-16.md.
- REFERENCIA_07_SERAVIENNE_FANTASIA_ELFOS_2026-11-16.md — posteriormente enriquecido com análise real do MP4.
- REFERENCIA_08_WILDLAND_HUNTERS_DIRECAO_CINEMATOGRAFICA_2026-11-16.md — análise real do outro MP4.
- O presente HANDOFF_INTEGRAL_CHAT_REFERENCIAS_2026-11-16.md.

**Questão ainda aberta:** essa pasta documenta a **frente de pesquisa e experimentos**; o planejamento principal da animação narrativa de Aenvarath pode manter referências canônicas e checkpoints adicionais em outro repositório/documento/chat. **Não declarar a pasta a única fonte de todas as decisões artísticas anteriores** até conciliação. Criar referências cruzadas, não duas verdades incompatíveis.

**Política de armazenamento:** versionar decisões, análises, especificações, commits, falhas e checkpoints. Não publicar senhas, tokens, dados privados nem MP4s/frames de terceiros sem autorização; documentar links, metadados e análises próprias. Os pacotes de evidências foram criados na conversa, **não** commitados no GitHub.

## 3. CRONOLOGIA COMPLETA DESTE CHAT, EM ORDEM

### 3.1 Primeira obra — “Global Cold Doom” (YouTube AZDzT-4OIY8)
**Mensagem inicial:** “Olha isso que absurdo de incrível: https://youtu.be/AZDzT-4OIY8?is=Mr_Nbb3IDhAFWKJE”.

Foi identificado, pela página pública, o vídeo de título aproximado **“Global cold doom! Girl follows reborn neighbor, hoards early, builds top shelter, lives well in doom”**, do canal **長風追劇_ShortTV**, publicado em **03/11/2026**. A página se autodescreve como canal de **AI manhua dramas**, com múltiplos idiomas de áudio e legendas; o vídeo traz marcação de conteúdo feito/alterado por IA. A página mostrava cerca de 298,7 mil views e 5,1 mil likes **na consulta**, métricas perecíveis e não constitutivas de qualidade. **Não foi assistido quadro a quadro**, não foram verificados motor e pipeline. Foram propostos estudos de identidade visual, continuidade, movimentos, câmera, cenário e automação sem custos.

### 3.2 Questão do tamanho de upload
O proprietário perguntou se poderia enviar vídeo de **mais de 1 hora e 1,7 GB**. Foi respondido que o limite nominal de upload de arquivos do ChatGPT era **512 MB por arquivo** no contexto da resposta, e que suporte à análise direta de vídeo não é garantido mesmo sob o limite. A decisão prática foi **evitar download e upload integral**: estudar pequenos trechos e quadros para economizar tráfego e armazenamento. O proprietário confirmou que **não havia baixado o vídeo**, pois desistira devido ao tamanho.

### 3.3 Método de amostragem sem baixar toda a obra
Foi sugerido **yt-dlp + FFmpeg**, com coleta de segmentos curtos, extração de quadros, pranchas, identificação de cenas complexas e exame temporal. Ressalvas: determinadas entregas do YouTube podem baixar dados extras ao buscar uma janela; falhas de autenticação/restrições de streaming; respeitar direitos e termos; amostras **não equivalem a inspeção integral**.

### 3.4 Segunda obra AI manhua — imperatriz (YouTube elGjvl8lJgA)
**Mensagem:** “Dá pra fazer isso agora? Porque acabei de ver outra obra feita por IA que eu fiquei encantado!” + https://youtu.be/elGjvl8lJgA?is=wUbLeLdlZqFy7cu_.

Identificada pela página como obra chinesa em título japonês: **“爆笑アニメ新作！転生早々処刑寸前、絶体絶命で感情システムが覚醒！女帝の心を揺さぶるたび修為が上昇し、彼女を真っ赤にさせて修仙界最強に！”** — reencarnação, execução iminente, despertar de sistema emocional, imperatriz/cultivo. Mesmo canal **長風追劇_ShortTV** da primeira referência. Não foi possível assistir à sequência integral ou extrair os frames diretamente do ambiente da conversa nesse ponto.

**Tentativa operacional:** o conector de navegador exigia sessão de origem conectada; **Desktop Commander comprovou 0% de cota restante**; os conectores PCRA disponíveis eram pilotos **sintéticos**, sem execução real de PowerShell/Windows. Não prometer acesso ao PC.

**Entregável:** arquivo **Estudo_Animacoes_IA_2_Videos.zip**, contendo:
- LEIA_PRIMEIRO.txt
- INICIAR_ESTUDO.cmd
- Coletar_Amostras_IA.ps1

O script usa PowerShell no Windows, localiza FFmpeg, baixa **yt-dlp.exe** oficial para pasta local se ausente, consulta duração, tenta extrair **7 trechos de 10 s por vídeo** (14 no total) em até 720p nos percentuais **5%, 19%, 33%, 47%, 61%, 77%, 92%**, retira dois frames por trecho (+2 e +7 s), gera pranchas e **amostras.csv**, log e ZIP leve em **Desktop/Estudo_Animacoes_IA**. Pode reaproveitar segmentos já existentes. **A execução no PC não foi demonstrada neste chat**; script e ZIP foram produzidos, não homologados. Pré-requisitos: FFmpeg e acesso válido ao YouTube.

### 3.5 Tutorial Claude Code / automatização cinematográfica
**Link:** https://youtu.be/N6uTE2p3lgg?is=P5dFwM_qUyq5mqOg.  
**Título verificado na página:** “Você vai criar Vídeos Cinematográfico Com O Claude Code Passo A Passo”, promovido pelo portal **TubeMakers**. Foi citada outra publicação relacionada de animação viral com Claude Code, mas o vídeo indicado **não foi examinado integralmente** e seu passo a passo **não foi confirmado**. 

**Análise proposta:** o Claude Code é **orquestrador/automatizador**, não um modelo que necessariamente gera os pixels de vídeo. Comparar agentes programáticos, Remotion, FFmpeg, edição e coordenação com a arquitetura **ChatGPT + PCRA**; **não migrar nem pagar Claude** sem justificativa e aprovação. Remotion é **candidato de ferramenta de edição**, e não uma dependência comprovada do tutorial.

### 3.6 Entrega do grande HANDOFF OFICIAL de 08/11
O proprietário colou o documento intitulado **“HANDOFF OFICIAL — PROJETO DE ANIMAÇÃO AUTOMATIZADA”**, data 08/11/2026, oriundo de chat de pesquisa cinematográfica. **Ordem superior:** integrar por soma; não apagar/alterar prioridades, motores, decisões ou checkpoints do projeto principal; consultar GitHub e classificar complementos. Abrange integralmente TS Malfoy, Shift Up/Bloodrain, deficiências de câmera/objetos/corpo/acting, bible de personagens, QA, ferramentas gratuitas, hardware e piloto P15. Seu **arquivo original completo** é mantido no link da seção 2. A seção 4 deste handoff consolida **todos os requisitos** e diagnósticos daquele documento.

O assistente **verificou via conector GitHub** repositório, contexto-mestre, análise Shift Up, issue #12 e PR #13, leu o material da branch e descobriu o seguinte:
- **main:** os estudos de 08/11 já estavam versionados.
- **PR #13 draft, não mesclado:** P15 em JSON, validador estrutural, animatic geométrico e motor FK de sprites, com testes e workflow.
- **Issue #12 aberta:** sem aceite do piloto cinematográfico artístico.
- **P15 geométrico** foi realmente renderizado em ambiente isolado: **15 s, 640×360, 24 fps, 360 quadros**, ffprobe verificado; **sprite demo**: **3 s, 72 quadros**; oito testes locais (4+4) reportados aprovados; as duas CI na revisão anterior **1f329089e3d7e0456491e9719e15fd01f9bad458** foram verificadas como sucesso.
- Nada disso comprova anime 2D final, lip-sync ligado a áudio, contato IK de mãos/pés, aderência ao Windows FX-4300/RX580 ou autorização de execução produtiva via PCRA.

**Ação no GitHub em 16/11:** criação de CHECKPOINT_CUMULATIVO_2026-11-16.md no PR #13 (commit inicial **ce888259...**), adição de índice no CONTEXTO_MESTRE.md da branch (commit **37fcf9f...**), comentário no Issue #12 (id **6924439614**), sem fechar issue ou alterar tarefas. As duas CI no commit 37fcf9f estavam **em execução quando consultadas**; não extrapolar esse estado para hoje sem rever.

### 3.7 Vídeo de ferramentas chinesas gratuitas
**Link:** https://youtu.be/UJ0Qh4BCzok?is=XCQor9VD_XI_n5wd.  
**Título de página:** “Finally! China Just Dropped NEW FREE AI Video Tools to Challenge Higgsfield!”; canal citado como **Becky the Ai Girl**. Descrição anuncia **três ferramentas + prompts** disponibilizados via Discord. Keywords de página incluem Seedance 2.5/2.0, Higgsfield e Veo; **keywords NÃO comprovam quais três ferramentas são demonstradas**.

**Decisão/avaliação:** estudar ferramentas de texto-imagem-vídeo, controle de personagem, image-to-video/video-to-video, câmera, continuidade, motion, duração, edição, créditos gratuitos, resolução, marca d'água, uso comercial, limites e APIs. “Free” no título é alegação promocional, **não gratuidade homologada**. Sem download de pesos, teste de contas, geração, identificação conclusiva das três ferramentas ou alteração do catálogo. Criado **REFERENCIA_06_FERRAMENTAS_CHINESAS_VIDEO_2026-11-16.md** e índice no master **na branch draft**.

### 3.8 Animação de fantasia/elfos: Seravienne — descoberta da página
**Link:** https://youtu.be/zCiQGSlRgnY?is=7AEHrxcQPR7stQt_.  
**Título chinês verificado:** **《塞拉維恩 - 天幕之下篇》EP01-03 少女，命運改寫了嗎？** (tradução aproximada “Seravienne — Sob o Véu do Céu, episódios 1–3: Garota, o destino foi reescrito?”).
Foi encontrada também edição **relacionada** divulgada como “SERAVIENNE: Under the Skyveil”, de ~24,7 min; observar que **relacionada não significa automaticamente mesmo upload** antes de comparar. A sinopse pública citava RPG/MMO, heranças/legados, herdeiros, cidades-estado, ataque de orcs e destino.

O proprietário declarou-se **encantado pela fantasia com elfos**; o assistente propôs comparar direção, raças, biomas, cenários, magia, arquitetura, movimento e câmera com Aenvarath. Criou **REFERENCIA_07_SERAVIENNE_FANTASIA_ELFOS_2026-11-16.md**, inicialmente limitada a metadados.

### 3.9 Upload e inspeção REAL de Seravienne
**Mensagem:** “Olha o vídeo:” + MP4 **1000592192.mp4**. O arquivo foi aberto e medido:
- **H.264, 1920×1080, 30 fps**, duração **1.481,038367 s ≈ 24min41s**, **44.429 quadros** de vídeo principal, áudio AAC, **327.407.584 bytes**. Há stream MJPEG de capa, não confundir com vídeo animado.
- Foram analisados **64 stills** distribuídos na duração (aprox. intervalo 23,3 s), **4 pranchas visuais** e **5 tiras temporais de 12 amostras**, passo ~0,25 s, cobrindo aproximadamente 2,75 s por tira (01:00; 03:56; 07:32; 08:15; 13:15). **Não é exame individual dos 44.429 quadros**.
- Evidências locais preservadas em **Evidencias_Seravienne_Analise_Visual.zip**: 4 sheets, strips **ride, combat, wolf, sword, dialogue** e LEIA_ME.

**Constatações visuais relevantes:**
- Cenários de pradarias de altitude, montanhas, arquitetura pétrea/monumental, estátuas aladas, espaços urbanos, docas, áreas iluminadas e construções majestosas; fotografia com contraste frio/quente, névoa/luz, profundidade e escala.
- Criaturas de montaria peludas, seres de aparência animal/felina, guerreiros e elfos, armaduras ornamentadas, cabelo/pelagem/materiais e efeitos; **fantasia 3D/CGI realista ou semirrealista**, não prova de anime 2D puro.
- **00:05:** personagem de cabelos claros e orelhas longas; abertura aparentemente credita **NEOWON**. Trata-se de **leitura visual preliminar do letreiro**, **não** identificação certificada de motor/provedor.
- **00:51–01:03 / tira 01:00:** montarias e personagem gesticulando; existe **movimento dentro das tomadas**, não só imagens estáticas; câmera e corte variam.
- **02:48–03:35:** grupo/escultura alada/arquitetura de mundo.
- **03:56–03:59:** guerreiro com escudo e atacante; preparação de golpe, alternância plano/corte; avaliar contato físico sem inferir erro automaticamente.
- **04:45–05:55:** movimentos, corridas/quedas de montaria, confronto.
- **07:32–07:35:** feras cruzam primeiro plano com oclusão e noção de profundidade; nada estruturalmente grosseiro foi comprovado na amostra.
- **08:15–08:18:** ataque com machado/espada, motion blur e corte; exige QA de continuidade de arma/contato.
- **09:48–10:35:** capuz, combate, criaturas, variedade de enquadramentos.
- **10:58:** imagem parcialmente pixelizada/mosaico; **não chamar automaticamente erro do gerador** (pode ser edição/censura).
- **11:45–13:42:** guerreira/elfa de cabelos brancos, acessórios dourados, efeitos azuis, cenários grandiosos e quedas d'água.
- **13:15–13:18:** virada sutil de cabeça/rosto/cabelo da elfa; identidade reconhecível nas amostras, sem deriva facial grosseira visível nessa tira curta; **não** prova consistência em episódios inteiros.
- **14:05–18:45:** cenas de diálogo, bolsas, papéis, docas e interiores; investigar interação mão-objeto.
- **19:09–22:39:** pequenos seres animais/raposa, olhos sob luz noturna, diálogos; direção de arte consistente visualmente na amostra.
- **23:25–24:35:** cavaleiro, cenas noturnas e encerramento.

**Qualidades extraídas:** worldbuilding de alto nível, arquitetura, montarias, materiais, fotografia, diversidade de criaturas, movimento intratomada, edição e emoção. **Pendências de verificação:** proporções cross-shot, mãos, contato/armas, biomécanica de golpes, física de pelagem/roupas, lip-sync e relação com áudio. O usuário não autorizou substituir visual de Nólyrien por esse acabamento: preservar estilo 2D canônico e usar essa obra como **referência para modo 3D/híbrido opcional**.

**Ações:** referência 07 recebeu relatório técnico real com timestamps na branch PR #13 (commit **b0d99e766758b0809106839482a6973fc5d4a1bf**); índice atualizado (commit **fa78e1eb...** antecedente). Pacote ZIP criado **fora do GitHub**. Não houve animação nova de Aenvarath nem execução via PCRA.

### 3.10 Segundo MP4 enviado: fantasia científica / “Wildland Hunters”
**Mensagem explícita do proprietário:** **“Eu quero fazer meus vídeos com essa qualidade absurda e direção e edição. Segue outro vídeo que eu me encantei.”**  
Arquivo: **1000591963.mp4**. **Não** foi fornecido URL do upload original. Letreiros visíveis em tela sugerem “WILDLAND HUNTERS — CORE TRANSFER HALL” (~00:43) e “WILDLAND HUNTERS — JIANG MEI” (~03:13); não inferir título oficial da obra, autoria ou motor de IA.

**FFprobe confirmado:** MP4 H.264, **1920×1080**, **30 fps**, **8.397 quadros**, **279,986213 s ≈ 4min40s**, áudio AAC, tamanho **65.902.717 bytes** (~62,9 MiB); MJPEG de capa adicional. Procedimento: **47 imagens fixas** espaçadas ~6 s, **4 pranchas**, **8 tiras temporais** de ~12 imagens cada, intervalos 00:13, 00:46, 01:52, 02:28, 02:49, 03:51, 04:04 e 04:19. Não houve inspeção quadro a quadro integral nem avaliação técnica de fonemas/áudio.

**Temas e cenários:** quarto com luz dourada, sala futurista de transferência de núcleos, refeitório, balcão, atendimento/ambiente médico, armaduras negras/vermelhas e vestes ornamentadas, personagens masculinos e femininos; coreografia de gestos, olhar, reação, mudança de planos e partículas mágicas/energia.

**Sequências registradas:**
- **00:01–00:38 / tira 00:13:** quarto, diálogo, over-the-shoulder, close e personagem movendo torso/boca; atuação não meramente estática. Edição motivada pelo olhar/reação, luz quente e profundidade.
- **00:43–00:58 / tira 00:46:** salão de transferência, núcleos/caixas, energia vermelha movendo entre compartimentos; ideal para estudar VFX e objetos persistentes.
- **01:01–01:37:** personagens de armadura, refeitório/balcão, tensão e humor, cenário coletivo.
- **01:43–02:19 / tira 01:52:** personagem senta, interação entre personagens, comida, olhares, atuação corporal e close; montagem diálogo/reação.
- **02:28–02:31:** contato mão enluvada/mão feminina; **testar geometria, dedos, contato, oclusão e luz sem declarar defeito como provado**.
- **02:37–03:01 / tira 02:49:** mulher de cabelos brancos/ornamentos dourados; energia negra/vermelha envolvendo personagem, corte para close, dissipação.
- **03:07–03:49:** personagens em roupas vermelhas, local tecnológico, diálogo e proximidade.
- **03:51–03:54:** partículas douradas somem durante interação mão–personagem sentada; resposta facial e efeito em camadas.
- **04:04–04:08:** personagem de tranças/armadura e área médica, energia.
- **04:19–04:32:** aproximação, mão no ombro e planos de arquitetura; estudar contato e raccord.
- **04:37:** cartela/número 009; apresentação seriada de personagem.

**Qualidades fortes:** fotografia, luz dourada e contraste, cenografia, materiais, caráter reconhecível dos personagens, ritmo cinematográfico, inserts, reaction shots, eye-lines, blocking, VFX e atuação em diálogo; gênero **3D/CGI fantasia científica semirrealista**. **Defeitos candidatos/QA:** movimento dos dedos, contato mãos/objetos, escala/rosto em ângulos distintos, armaduras e adereços entre tomadas, oclusão/iluminação de VFX, lip-sync, eixos de câmera e continuidade espacial. **Nenhuma deformação crítica inequívoca foi comprovada na amostra**; não tratar ausência de observação como perfeição comprovada.

**Ações:** foi criado na branch PR #13 o relatório **REFERENCIA_08_WILDLAND_HUNTERS_DIRECAO_CINEMATOGRAFICA_2026-11-16.md** (commit **da51cf760400de2c340fb8cd02f34c2854965cbb**) e indexado no mestre (commit **ea8c2950055d7ceb41d64477b259d3dcb223ac47**). Foi gerado **Evidencias_Direcao_Cinematografica_Video_1000591963.zip** com 4 pranchas, 8 tiras e LEIA_ME. O ZIP **não** foi publicado no GitHub. Nenhum clipe novo do projeto foi renderizado.

### 3.11 Pedido final deste chat
O proprietário pediu: **“Prepare um documento completo na forma mais eficiente para você mesmo ler depois de tudo o que foi dito e decidido nesse chat, sem deixar nada de fora desde a primeira mensagem desse chat.”**

Esta é a finalidade do presente documento: **recuperação integral do contexto substantivo da conversa**, com links/etapas/estados claramente classificados.

## 4. HANDOFF DE 08/11 — CONTEÚDO CANÔNICO QUE DEVE SER PRESERVADO

O texto original completo foi fornecido pelo proprietário nesta conversa e continua acessível em:
https://github.com/Furuya29/furuya-motion-studio/blob/main/docs/projeto-animacao-automatizada/HANDOFF_INTEGRACAO_CHAT_PRINCIPAL_2026-11-08.md

**0. Ordem principal:** o documento é soma; não reiniciar, apagar, substituir, descartar motores, sobrepor prioridades, duplicar funcionalidades sem checar ou confundir sugestões com arquitetura obrigatória. Recuperar checkpoint comprovado. Qualquer conflito com planejamento prévio exige comparação técnica e manutenção da decisão vigente até aprovação. Registrar novidades e rastreabilidade no GitHub.

**1. Documentação:** repo Furuya29/furuya-motion-studio; pasta docs/projeto-animacao-automatizada; CONTEXTO_MESTRE.md; REFERENCIA_02_SHIFTUP_BLOODRAIN_2026-11-08.md; HANDOFF_INTEGRACAO_CHAT_PRINCIPAL_2026-11-08.md; Issue #12. A pasta não contém necessariamente toda a história do chat principal; se houver outra canonicidade, conciliá-la por links cruzados. Não registrar mídia protegida nem credenciais.

**2. Objetivo:** produção de anime japonês 2D, 3D realista/semirrealista e híbrido com personagens/situações/câmera/cenários consistentes, cenas complexas e automatização com supervisão; meta R$ 0. Métodos **mantidos em paralelo**: quadros-chave por IA, rigs 2D, malhas deformáveis, interpolação, animação tradicional/quadro a quadro assistido, mocap/retargeting, animação 3D, IA generativa conforme tomada. Separação de animação original e recast de vídeo viral.

**3. Referência 01 TS Malfoy:** https://youtu.be/WYRDe8XsRmI; curta do Fantasoner, Draco Malfoy feminina; arquivo analisado historicamente 1000589408.mp4, **~09min04s, 1920×1080, 30 fps, 16.328 quadros**. Pontos fortes: composição, fotografia, luz, cenários, enquadramentos, rostos, atmosfera; limitações: atuação corporal restrita em muitas tomadas, olhos/boca/cabelo animados com corpo estático, contato/ações longas complexas. Aplicar shot planning, luz, composição, edição, atuação completa e controle de movimento. Não foi reanalisado neste chat.

**4. Referência 02 Shift Up / Stellar Blade: BLOODRAIN:** videoclipe **“Wanna be in LOVE”**, personagem Evie, arquivo histórico 1000589429.mp4, **~03min37s, 1920×1080, 24 fps, 5.222 quadros**. Cenários urbanos/futuristas, metrô, tubulações, vegetação, iluminação atmosférica, câmera variada, ritmo, acessórios como microfone/guarda-chuva/celular/hashi. Artistas criaram base da personagem e IA auxiliou apresentação; **orçamento, render hardware e pipeline exatos não confirmados**; making-of final representado com IA, **não prova de filmagem real**. Defeitos/hipóteses: microfone ligeiramente incoerente em perspectiva durante rotação; proporções corporais entre planos (apurar perspectiva/lente/pose); deriva facial perto de 00:33–00:35; canto com atuação corporal limitada e lip-sync não comprovado foneticamente; mãos, dedos, contato, pés, roupas, cabelo e objetos com risco de deformações; não considerar lista exaustiva. Detalhes temporais e evidências na análise oficial.

**5. Correções:** bible de identidade e anatomia normalizada por personagem (frente/perfil/3⁄4/costas, expressões, proporções, cores, figurino); câmera com pose, FOV/lente, projeção, parallax e oclusão; props com geometria persistente, pivot, world vs hand attachment, sombra/passes; rigs 2D/3D, IK/FK/constraints/meshes/mocap e contato; fonemas/visemas/mandíbula/olhar/pescoço/respiração/ombro, Rhubarb Lip Sync como candidato PT-BR; cenários 3D leves/multiplano/híbridos fixos; QA de identidade/contato/proporção/perspectiva/flicker/ghosting e falha por timestamp, severidade, evidência e reparo localizado. Distinguir artefatos causados por câmera e cortes legítimos de falhas reais de IA.

**6. Hardware:** Windows 10 Pro, AMD FX-4300, ~16 GB RAM, Radeon RX 580 8 GB; Redmi K70 Ultra. Investigar Blender, OpenToonz, FFmpeg, Rhubarb e opções reais gratuitas; **RX 580 Polaris não qualificada para HIP Cycles GPU moderno**; evitar superestimar GPU grátis ou render local. Respeitar orçamento.

**7. Piloto proposto:** ~15 segundos em 2–3 planos: A rosto/fala/canto/respiração, B deslocamento/mudança de ângulo/corpo e pé no chão, C mão/microfone ou outro objeto/câmera em movimento. Aceite: nenhum drift crítico, geometria de microfone correta, mãos/pés sem deformação crítica, atuação e áudio naturais, cenografia/figurino estáveis, arquivos-fonte+MP4+relatório QA+tempo/RAM/VRAM/custo. Issue #12 aberta, **não implementado nem homologado artisticamente** no momento do handoff.

**8. Instrução ao chat principal:** consultar planejamento anterior, GitHub, classificar novidade como existente/reforço/nova/alternativa/conflito, integrar só o compatível, atualizar documentação e retomar último checkpoint real. Nenhum reset.

**9. Diretriz permanente:** construir sistema **controlável, reproduzível, consistente e expressivo** para narrativas completas; combinar geratividade visual com controle espacial/temporal da animação tradicional; manter liberdade estilística de 2D e 3D.

## 5. MATRIZ DE REFERÊNCIAS CONSOLIDADA

| ID | Referência | Fonte primária | Evidência disponível neste chat | Valor para projeto | Estado |
|---|---|---|---|---|---|
| 01 | TS Malfoy / Fantasoner | https://youtu.be/WYRDe8XsRmI | Handoff prévio e estudos GitHub | Luz, close, ambientes, atmosfera | Análise histórica documentada |
| 02 | Shift Up — “Wanna be in LOVE”, Evie | arquivo histórico 1000589429.mp4 / referência GitHub | Relatório de 08/11 | Fotografia, worldbuilding, VFX, falhas de câmera/props | Análise histórica documentada |
| 03 | Global Cold Doom / AI manhua | https://youtu.be/AZDzT-4OIY8 | Página/metadados, sem MP4 | Episódios longos, linguagem manhua | Sem análise temporal |
| 04 | Imperatriz e sistema emocional / AI manhua | https://youtu.be/elGjvl8lJgA | Página/metadados; script de coleta preparado | Narrativa longa e IA serializada | Sem análise temporal |
| 05 | Tutorial cinematográfico Claude Code | https://youtu.be/N6uTE2p3lgg | Página/metadados | Orquestração agente, edição, workflow | Conteúdo completo não verificado |
| 06 | 3 ferramentas chinesas “free” | https://youtu.be/UJ0Qh4BCzok | Página/metadados/keywords | Motores alternativos gratuitos a investigar | Alegação de gratuidade não comprovada |
| 07 | Seravienne: Under the Skyveil, EP 01–03 | https://youtu.be/zCiQGSlRgnY | MP4 1000592192, pranchas e 5 tiras | Fantasia, elfos, monstros/montarias, direção 3D | Inspeção amostral real |
| 08 | Wildland Hunters (títulos parciais em tela) | MP4 1000591963.mp4, sem URL original | Pranchas e 8 tiras | Fotografia, edição, acting, interação, VFX | Inspeção amostral real |

**As referências 07/08 têm evidência material mais forte neste chat**, porque o usuário enviou os arquivos e houve inspeção de movimento amostrado. Isso **não** dá acesso ao pipeline de seus autores.

## 6. SISTEMA TÉCNICO PREVISTO — SOMAR, NÃO SUBSTITUIR

**Arquitetura desejada multimétodo, com escolha por tomada (não decisão de trocar tudo):**

1. **Story / direção:** texto/roteiro → breakdown de cenas → narrativa, direção de atores, emoção, duração, storyboard/animatic e shot list.
2. **Biblioteca de cânones:** character bible, turnaround, proportions, palette, expressão, voz, objetos, rig, arquitetura/cenário/planta e versões imutáveis de assets aprovados. Identificadores persistentes de personagem/objeto/cenário/tomada.
3. **Contrato por tomada (shot spec):** shot_id, tempo/fps, personagens, locação, câmera/lente/FOV/pose/trajetória, blocking, gestos/falas, look/lighting, props world/bone attachment, máscaras, fontes/saídas e checklist QA.
4. **Geometria e movimento:** rig 2D em camadas, mesh/plastic, desenho substituto em perfil/3⁄4, FK/IK, constraints, animação 3D, mocap, retargeting, interpolações; IA text/image/video apenas quando realmente ajuda.
5. **Cenário / câmera:** 3D leve ou multiplano, geometria estável, posição dos elementos, sombras e perspectiva, câmera coherente. Objetos em passes separados com depth/occlusion.
6. **Atuação completa:** expressão facial, olhar, lábios/fonemas/visemas, mandíbula, cabeça, pescoço, postura, ombro, respiração, gesto, reação e cabelo/roupa com movimento secundário.
7. **Efeitos e magia:** evento causal → preparação → pico → dissipação → reação/oclusão/iluminação consistente, partículas e composição por camadas; não “textura mágica flutuante” incoerente.
8. **Direção editorial:** coverage de establishing/medium/close/insert/reaction, shot-reverse-shot, eixo de ação, raccord de olhares/gestos/posição/cor/luz, ritmo, pausas, montagem, transições, sound design, música e dublagem PT-BR.
9. **Composição/finalização:** FFmpeg, Remotion e editores/softwares já previstos como opções complementares; escolher por custo/compatibilidade, sem substituir motores ou comprometer projeto existente.
10. **QA de aceitação:** verificação temporal/cross-shot de identidade, proporções corrigidas por perspectiva, continuidade de roupa/cabelo, contato mão-objeto/pé-chão, perspectiva de microfone, oclusão, flicker, ghosting, sombras, sincronia áudio/visema, layout do cenário; registrar **timestamp, frame, hipótese, evidência, gravidade, causa candidata, reparo e aprovação humana**.
11. **Correção incremental:** retake de poucos segundos, re-render de pass, máscara, keyframe ou rig antes de regenerar tudo; comparar versão aprovada anterior e não reverter decisões artísticas.
12. **Orquestração:** PCRA/ChatGPT quando **produtivamente apto**; agentes executam scripts, verificam resultados, guardam logs/recibos e versionam mudanças. Pilotos MCP do PCRA disponíveis neste chat **são sintéticos**; não alegar acesso PowerShell pleno.

**Ferramentas citadas como existentes/candidatas, sem afirmar que todas estão instaladas/homologadas:** FFmpeg, yt-dlp (somente amostragem), Blender EEVEE/rig/Grease Pencil, OpenToonz/Xsheet/Plastic, Krita, Godot, Inochi2D, Remotion, Rhubarb Lip Sync, CapCut/Premiere como interfaces alternativas, Python/Pillow, Flow, motores generativos gratuitos efetivamente testados, mocap/retargeting. Respeitar compatibilidade do FX-4300 e RX 580.

**Duas novidades de requisitos vindas das referências recentes:**
- Fantasia/MMORPG de escala cinematográfica: raças distintas, cenários/arquiteturas monumentais persistentes, monstros/montarias, efeitos mágicos, atuação e profundidade (Ref. 07).
- **Cinematic Direction & Editorial Bible**: casting/blocking, coverage, planos de reação, raccord, ritmo, luz/contraste, VFX causais e áudio para cenas dialogadas (Ref. 08).

## 7. CHECKPOINT DE CENA: NÓLYRIEN E PALÁCIO/TORRE — NÃO REINICIAR

Conforme continuidade reconciliada na conversa e registrada no CHECKPOINT_CUMULATIVO_2026-11-16.md:

- Personagem: **Nólyrien**, aparência e proporções previamente aprovadas no projeto canônico; não redesenhar rosto, cabelo, coroa, figurino, cores ou proporções ao incorporar referências externas.
- A animação narrativa estava na transição do **surgimento das asas (frame ~20)** para **início do voo (frame ~21)**, segundo o checkpoint discutido; verificar o arquivo de trabalho principal antes de afirmar número exato/status definitivo.
- **Asas negras nascem da região lombar**, com ponto de implantação anatômica coerente; vista de costas deve mostrar **face dorsal/externa** correta das asas, e a **coroa vista por trás**; eixo de torso/quadril e largura/simetria preservados.
- O quadro da correção ainda exigia aceite visual; **não** considerar asas/voo finalizados.
- Torre e **cúpula perfeitamente circulares**, em vez de torre/cúpula com arestas; não trocar a arquitetura e geometria já aprovadas.
- O **palácio inteiro deve ser colossal, imponente, único e não genérico**, com arquitetura definitiva e planta coerente que possa servir também no MMORPG. Cenário deve continuar igual de tomada a tomada.
- Não confundir proposta do piloto genérico P15 (15 s, QA) com sequência narrativa de Nólyrien. São frentes complementares, **sem permissão para sobrepor a prioridade do chat principal**.
- A preferência do usuário por acabamento **3D/semirrealista** em referências de fantasia foi interpretada como possível **modo opcional**, não aprovação automática para converter toda a produção originalmente anime 2D.

**Próxima ação narrativa segura:** recuperar frame e referência aprovados no chat principal, corrigir **apenas** implantação/dorsal das asas, coroa posterior e simetria conforme criticado; validar; continuar a decolagem sobre torre/cúpula circular. Separadamente consolidar geografia/planta do palácio antes de múltiplas cenas novas.

## 8. STATUS REAL DE CÓDIGO, CI, OPERAÇÃO E HOMOLOGAÇÃO

**PR #13**, criado 09/11 e ainda **aberto/draft** nas consultas do chat:
- Especificação do piloto de 15 s em JSON, 3 tomadas de 120 frames a 24 fps, IDs persistentes e gates.
- Validador estrutural offline e testes para lacunas, props ausentes e bloqueio de falsa homologação.
- Animatic determinístico Python/Pillow/FFmpeg com look-at/câmera/props geometricamente ancorados; vídeo geométrico **640×360 15s/360 frames**, renderizado em ambiente isolado, sem áudio ou desenho anime.
- Motor 2D de sprites PNG por camadas, pivôs, hierarquia FK, keyframes e troca de olho/boca; exemplo de **72 frames/3s**, não arte final.
- Testes de animatic e rig 4+4 concluídos no ambiente de ensaio; CI de animação e regressão do projeto legado passaram na revisão anterior do PR. **Uma nova revisão precisa checar checks novamente**.
- Não houve execução do código no PC do usuário neste chat, nem lip-sync com voz real, IK/foot locking, contato/oclusão final, aprovação artística, desempenho local medido ou merge do PR.
- Issue #12 segue aberta; checkboxes do piloto não foram marcados como concluídos.
- PRs do Furuya Motion Studio **#14–#16** pertencem majoritariamente à frente de recasting e foram encontrados **mesclados na main** na consulta. Exemplo importante: **Flow** foi mantido como geração criativa, mas retirado de roteamento automático de recast estritamente fiel após vídeo real não preservar coreografia. Essas decisões **não equivalem** a homologação do pipeline original cinematográfico.
- O ambiente mostrou Desktop Commander **0% de chamadas**, navegador conectado não disponível via sessão de origem, e PCRA com conectores experimentais sintéticos sem operação produtiva de PowerShell. Não prometer que ChatGPT operou o PC nessa conversa.

**Estados observados nas integrações realizadas neste chat** (todos na branch de revisão, salvo comentário público na Issue #12):
1. CHECKPOINT_CUMULATIVO_2026-11-16.md — criado, indexado no contexto mestre.
2. REFERENCIA_06_FERRAMENTAS_CHINESAS_VIDEO_2026-11-16.md — pesquisa, sem teste da demo.
3. REFERENCIA_07_SERAVIENNE_FANTASIA_ELFOS_2026-11-16.md — primeiro metadata, depois **relatório de MP4 amostrado**, indexado.
4. REFERENCIA_08_WILDLAND_HUNTERS_DIRECAO_CINEMATOGRAFICA_2026-11-16.md — **relatório de MP4 amostrado**, indexado.
5. HANDOFF_INTEGRAL_CHAT_REFERENCIAS_2026-11-16.md — **o presente documento**.

Não mesclar automaticamente; revisão de diffs/CI, preservação de base e autorização permanecem obrigatórias.

## 9. ARTEFATOS, IDENTIFICADORES E INTEGRIDADE

**MP4s realmente anexados a ESTA conversa (não publicar no GitHub):**
- Seravienne: **1000592192.mp4** — 327.407.584 bytes; SHA-256 **8f65a8e692f55658c2cab8e2483d4ff8c588c52c09b0a72e4077a08b24e4d520**.
- Wildland Hunters: **1000591963.mp4** — 65.902.717 bytes; SHA-256 **6c10912ccb5f240cb8588fe6bac38c5feff2ffbfbab87a70b2c5d5d101cb854e**.

**ZIPs efetivamente gerados nesta conversa, disponíveis no armazenamento desta sessão quando conferido:**
- **Estudo_Animacoes_IA_2_Videos.zip** — script para coletar 7 trechos de 10 s em cada vídeo AI manhua; 4.8 KiB. SHA-256 **bfee848879d3229930ea4d84ca292dff42943010554dc0eac45da50f8e9b4556**.
- **Evidencias_Seravienne_Analise_Visual.zip** — quatro sheets, cinco strips e LEIA_ME; ~3,2 MiB. SHA-256 **a80693afc4ef40657d99b8032a554db2322ba9d16456f2781b83b86774f4e609c**.
- **Evidencias_Direcao_Cinematografica_Video_1000591963.zip** — quatro sheets, oito strips e LEIA_ME; ~2,8 MiB. SHA-256 **78b48776d3c28514f2113a2e08d7ff373c691a5accf5b03f0358**.
- Os nomes/links de sessão acima **não garantem** persistência em outro chat. Recuperar pelo material do usuário, pela biblioteca/arquivos disponíveis ou solicitar apenas o arquivo ausente se imprescindível. Nunca criar links fictícios nem tratar ZIP de evidência como autoria da obra.

**Artefatos de outro chat citados no handoff histórico, NÃO reabertos aqui:** 1000589408.mp4 (TS Malfoy), 1000589429.mp4 (Shift Up), Analise_Tecnica_TS_Malfoy_Animacao_IA.pdf, Evidencias_Visuais_TS_Malfoy.zip. Não presumir que estejam montados neste chat.

**Sem arquivos próprios de produção final gerados aqui:** não existe MP4 novo de Nólyrien ou cena final de Aenvarath produzido nesta conversa.

## 10. MATRIZ DE DECISÕES: EXISTENTE × NOVO × PENDENTE

| Área | Situação em 16/11 | O que fazer |
|---|---|---|
| Produção multimétodo 2D/3D/híbrida | **Decidida** anteriormente | Preservar; escolher mecanismo por tomada |
| Personagem/cenário/objeto persistentes | **Decididos, reforçados** | QA com registros, bases canônicas e IDs |
| Câmera/projeção/microfone | **Reforço técnico** da Ref. 02 | Testar parallax, eixos, sombras e contato |
| Atuação corpo + voz/visemas | **Planejada, não homologada** | Testar fonemas, movimentos sincronizados |
| P15 15 s + sprites FK | **Código/ensaio na PR #13** | Revisar CI, testar em PC autorizado, tornar artístico |
| Nólyrien asas/coroa/torre | **Checkpoint narrativo pendente** | Corrigir antes de prosseguir; não reinventar arquitetura |
| Duas novelas AI manhua de longa duração | **Metadados, sem amostras analisadas** | Executar ou revisar script/trechos, se útil |
| Tutorial Claude Code | **Metadados/alternativa** | Validar conteúdo antes de inferir pipeline |
| “3 ferramentas chinesas grátis” | **Alegação não verificada** | Identificar URLs, termos, limites, teste R$0 |
| Seravienne | **Amostragem real + doc** | Futuro QA aprofundado de cena/movimento/magia |
| Wildland Hunters | **Amostragem real + doc** | Incorporar critérios editoriais, VFX, acting sem migração de motor |
| Qualidade excepcional como objetivo | **Pedido explícito do proprietário** | Direção/editorial/QA no mesmo patamar da geração |
| Acesso PC/PCRA | **Não produtivo neste chat** | Não executar nem alegar recibo até homologação real |
| Despesa recorrente | **R$ 0 como alvo firme** | Validar quotas/termos; evitar cobranças |

## 11. O QUE NÃO FOI FEITO — PROIBIDO APRESENTAR COMO CONCLUÍDO

- **Não** foi baixado o vídeo completo de 1,7 GB da primeira referência.
- **Não** foram executadas no Windows as amostragens do ZIP inicial.
- **Não** foi assistido integralmente nem transcrito o vídeo Claude Code ou a demonstração de ferramentas chinesas.
- **Não** foram identificadas conclusivamente as três ferramentas anunciadas como gratuitas.
- **Não** foram comprovados modelos/motores, orçamento nem hardware dos criadores de Seravienne/Wildland Hunters.
- **Não** ocorreu varredura manual de todos os 44.429 + 8.397 quadros dos dois MP4s; apenas amostragem e tiras.
- **Não** foi realizada validação fonética de áudio/lip-sync dos MP4s.
- **Não** foi criada animação original nova ou render cinematográfico de Aenvarath/Nólyrien neste chat.
- **Não** houve instalação ou teste de render no PC FX-4300/RX580 por este assistente.
- **Não** houve homologação do P15, nem merge do PR #13 ou alteração de prioridades.
- **Não** foi aprovada a substituição da estética anime 2D por 3D para todo o projeto.
- Miniaturas ilustrativas eventualmente exibidas na conversa **não devem substituir as pranchas e arquivos realmente extraídos** como evidência temporal.

## 12. PLANO DE RETOMADA RECOMENDADO — SEM MUDAR PRIORIDADES

**A. Recuperação contextual, antes de tocar no projeto:** ler este arquivo, HANDOFF_INTEGRACAO_CHAT_PRINCIPAL_2026-11-08.md, CONTEXTO_MESTRE.md, RECONCILIACAO_ADITIVA_2026-11-09.md, relatórios 02/06/07/08, Issue #12 e PR #13; conciliar com o planejamento efetivo do chat narrativo de Aenvarath. Validar estado de branch/CI; não inferir que a situação segue idêntica após a data do relatório.

**B. Continuidade artística imediata:** respeitar último frame aprovado da personagem Nólyrien e geometria circular/colossal da torre, corrigir partes indicadas sem refazer o que já está correto e submeter à aprovação antes de seguir as cenas do voo. A produção narrativa pode usar as referências cinematográficas como parâmetros de qualidade, mas não precisa esperar o piloto P15 caso o planejamento original não determine isso.

**C. Engenharia e QA:** preservar P15/sprite como base experimental; implementar versões com assets autorais aprovados, animação do corpo, áudio/visemas, contato, VFX e cinematografia, com relatório por falha e medição de consumo. Revisar CI e não regressão de recast antes de qualquer merge.

**D. Pesquisa por evidências:** estudar episódios de Seravienne e vídeo Wildland Hunters de forma localizada, em tomadas onde qualidade de edição/câmera/atuação são evidentes; atribuir automaticamente status de HIPÓTESE a defeito sem prova de frame. Investigar NEOWON e motores só mediante documentação oficial. Executar amostragem dos manhuas longos apenas se houver vantagem prática.

**E. Infraestrutura gratuita:** priorizar CPU e previews leves, Blender/EEVEE compatível, OpenToonz/rigs 2D/FFmpeg, ferramentas gratuitas reais; não assumir suporte HIP moderno da RX580, GPU gratuita ilimitada ou controle via conectores sintéticos. Não pagar nada sem solicitação e autorização expressas.

**F. Aceite final:** apenas após **fonte + MP4 original do projeto + inspeção temporal + QA cross-shot + medições CPU/RAM/VRAM/tempo/custo + revisão e aprovação humana** marcar piloto artístico como concluído.

## 13. INSTRUÇÃO EXPLÍCITA AO PRÓXIMO GPT

1. **Não fazer perguntas cujas respostas constem deste documento**; consultar referências e arquivos associados antes de solicitar repetição ao proprietário.
2. Não apagar nem reordenar trabalho feito nos outros chats do projeto; este documento agrega pesquisa e checkpoint, **não afirma possuir todos os arquivos canônicos externos**.
3. Ao receber novo vídeo, identificar URL/título/autor pelo que é verificável; se MP4 for enviado, medir ffprobe, amostrar por toda a duração e examinar tiras consecutivas, sempre descrevendo limites de cobertura.
4. Registrar novidades no GitHub (branch de revisão e PR, salvo instrução diferente) com **estado de evidência e autoria**; nunca declarar concluído sem execução.
5. Para o estilo visual, **manter o anime japonês 2D autoral** e a opção 3D/híbrida. As referências externas são padrões de qualidade, **não templates para copiar personagens ou ativos protegidos**.
6. Tratar “direção e edição” como requisitos de primeira classe: composição, luz, ritmo, atuação, reação e continuidade, não apenas efeito generativo.
7. Reusar os scripts e módulos existentes, validar compatibilidade e custos, medir resultados, corrigir trechos localmente quando possível.
8. Quando o proprietário pedir retomada, apresentar **o último checkpoint comprovado** da frente correspondente, não declarar que o projeto foi reiniciado.
9. Se existir divergência entre este documento e registro posterior com evidência, **preferir o mais recente verificado e conservar o histórico**.
10. A instrução superior é a do proprietário: **“PRESERVAR TUDO O QUE JÁ FOI DECIDIDO, INTEGRAR AS NOVAS DESCOBERTAS COMO SOMATÓRIA E CONTINUAR O DESENVOLVIMENTO ORIGINAL.”**

## 14. ÍNDICE RÁPIDO DE LINKS FORNECIDOS NO CHAT

**Vídeos, na ordem de apresentação:**
1. https://youtu.be/AZDzT-4OIY8?is=Mr_Nbb3IDhAFWKJE
2. https://youtu.be/elGjvl8lJgA?is=wUbLeLdlZqFy7cu_
3. https://youtu.be/N6uTE2p3lgg?is=P5dFwM_qUyq5mqOg
4. Referência histórica TS Malfoy: https://youtu.be/WYRDe8XsRmI
5. https://youtu.be/UJ0Qh4BCzok?is=XCQor9VD_XI_n5wd
6. https://youtu.be/zCiQGSlRgnY?is=7AEHrxcQPR7stQt_
7. Upload 1000592192.mp4 (Seravienne; sem link público de arquivo)
8. Upload 1000591963.mp4 (Wildland Hunters; sem URL de YouTube fornecida)

**Documentos e desenvolvimento:**
- https://github.com/Furuya29/furuya-motion-studio
- https://github.com/Furuya29/furuya-motion-studio/blob/main/docs/projeto-animacao-automatizada/CONTEXTO_MESTRE.md
- https://github.com/Furuya29/furuya-motion-studio/blob/main/docs/projeto-animacao-automatizada/REFERENCIA_02_SHIFTUP_BLOODRAIN_2026-11-08.md
- https://github.com/Furuya29/furuya-motion-studio/blob/main/docs/projeto-animacao-automatizada/HANDOFF_INTEGRACAO_CHAT_PRINCIPAL_2026-11-08.md
- https://github.com/Furuya29/furuya-motion-studio/issues/12
- https://github.com/Furuya29/furuya-motion-studio/pull/13
- https://github.com/Furuya29/furuya-motion-studio/blob/docs/animacao-integracao-cumulativa-20261109/docs/projeto-animacao-automatizada/CHECKPOINT_CUMULATIVO_2026-11-16.md
- https://github.com/Furuya29/furuya-motion-studio/blob/docs/animacao-integracao-cumulativa-20261109/docs/projeto-animacao-automatizada/REFERENCIA_06_FERRAMENTAS_CHINESAS_VIDEO_2026-11-16.md
- https://github.com/Furuya29/furuya-motion-studio/blob/docs/animacao-integracao-cumulativa-20261109/docs/projeto-animacao-automatizada/REFERENCIA_07_SERAVIENNE_FANTASIA_ELFOS_2026-11-16.md
- https://github.com/Furuya29/furuya-motion-studio/blob/docs/animacao-integracao-cumulativa-20261109/docs/projeto-animacao-automatizada/REFERENCIA_08_WILDLAND_HUNTERS_DIRECAO_CINEMATOGRAFICA_2026-11-16.md

## 15. DECLARAÇÃO DE INTEGRIDADE

Este registro conserva as informações **deste chat** com detalhes de cada referência, as solicitações do proprietário, decisões e ressalvas, entregas de scripts e pacotes, avaliações de imagem e movimento, estado real de GitHub/CI, limitações de ferramenta e instruções do handoff anterior. O fato de um link estar listado não comprova que seu conteúdo audiovisual integral foi visto; o fato de uma proposta estar catalogada não a torna implementada. Em caso de necessidade de auditoria literal do handoff original de 08/11, reler o documento integral indicado na seção 2 e o texto do usuário nesta conversa.

**REGRA FINAL:** REAPROVEITAR, COMPLEMENTAR, DOCUMENTAR, TESTAR E CONTINUAR. NUNCA APAGAR, REINICIAR, PRESUMIR HOMOLOGAÇÃO OU ALTERAR PRIORIDADES SEM EVIDÊNCIA E APROVAÇÃO.
