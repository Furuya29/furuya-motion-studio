# Referência 08 — vídeo chinês “Wildland Hunters”: direção cinematográfica, edição e atuações (16/11/2026)

> **Estado:** análise visual de material realmente enviado pelo proprietário, com amostragem temporal. **Não** constitui auditoria de todos os quadros, avaliação de fonemas com áudio, comprovação do motor utilizado, aprovação de arquitetura ou homologação do pipeline.

## Origem e medição

- Fonte primária: MP4 do usuário **`1000591963.mp4`**, sem URL pública identificada. O rótulo **“WILDLAND HUNTERS — CORE TRANSFER HALL”** aparece na tela perto de 00:43 e **“WILDLAND HUNTERS — JIANG MEI”** perto de 03:13; **não presumir título oficial completo da obra**, autoria, fornecedor de IA nem autorização de republicação.
- FFprobe do MP4: contêiner **279,986 s** (~04:40), 1920×1080, H.264, 30 fps, **8.397 quadros** no stream principal, áudio AAC; total **65.902.717 bytes** (~62,9 MiB). Existe uma imagem de capa MJPEG adicional (não contar como animação).
- Procedimento: 47 quadros representativos a intervalos de cerca de 6 s entre 00:01 e 04:37 e **oito tiras temporais** de 12 amostras cada, em passos ~0,27–0,30 s, nos trechos 00:13, 00:46, 01:52, 02:28, 02:49, 03:51, 04:04 e 04:19. Seleção de quadros feita por busca temporal com OpenCV; a cobertura de cada tira é cerca de 3,0–3,3 s. Não foi feita inspeção individual dos 8.397 quadros nem escuta crítica/alinhamento fonético da trilha.
- Material protegido de terceiros permanece fora do repositório. As pranchas foram preparadas na sessão de análise apenas para uso de estudo.

## Storyboard observável e linguagem da edição

| Tempo | Observação visual verificada | Técnica a aproveitar / QA pendente |
|---|---|---|
| 00:01–00:38 | Quarto banhado por sol quente, homem deitado e mulher com cabelos presos em conversa; sequências de primeiro plano, over-the-shoulder e close; o homem ergue o tronco e articula boca/expressões em 00:13–00:15 | Motivação do corte por olhar/reação, luz direcional, profundidade de campo, personagens bem distinguidos. Não afirmar sincronia fonética sem comparar áudio |
| 00:43–00:58 | Salão futurista com escrita “WILDLAND HUNTERS — CORE TRANSFER HALL”, caixas tecnológicas com núcleos luminosos; efeito vermelho de energia/objeto movendo até compartimentos em ~00:46–00:49 | Worldbuilding com plano geral seguido de inserts de objeto e VFX. Testar oclusão, persistência geométrica, contato físico, partículas com luz |
| 01:01–01:37 | Personagem masculino em armadura negra com detalhes brancos e mulheres com armaduras escuras/vermelhas; corte para salão de refeição e balcão; tensão e humor por reação | Ambiente coletivo reconhecível, extras e continuidade de figurino. Manter eixos de câmera e ancoragem das posições em montagem |
| 01:43–02:19 | Personagem feminina ornamentada se aproxima e se senta diante de dois personagens; intercala tomadas de mãos, comidas, pernas, expressões e diálogo | Blocking para múltiplas personagens e props (comida, cadeira, mesa); inspeção necessária de dedos, contato e pés |
| 01:52–01:55 | Duas posições de câmera e trocas de expressão; mulher sorri, fala e desloca ombros/cabeça, homem acompanha com olhar | Atuação intratomada e montagem shot/reverse/reaction; exemplos úteis para atuação sem cortes incessantes |
| 02:28–02:31 | Homem apresenta a mão enluvada e personagem feminina toca/aponta para seus dedos; mudança de plano geral para médio | Exemplo ideal de QA de contato mão–mão: ancoragem, número de dedos, luz e oclusão. A amostra não comprova defeito nem certifica ausência de deformação |
| 02:37–03:01 | Personagem de cabelo branco com acessórios dourados em cenário íntimo; ~02:49 corpo/armadura masculina com energia negra e traços vermelhos, corte para close e dissolução do brilho | Camadas de composição, VFX integrado a material e pele; identidade reconhecível entre amostras de uma tomada. Cortes podem mascarar continuidade complexa |
| 03:07–03:49 | Ambiente tecnológico com personagens em vestes vermelhas, planos de duas personagens, close facial e interação com equipagem | Alternância de planos sem perder geografia geral, materialidade de tecidos e armaduras; não equiparar consistência em stills a consistência completa |
| 03:51–03:54 | Mão do personagem masculino diante de mulher sentada, partículas douradas desaparecem sobre roupas/corpo; ela muda olhar e posição | Cues de VFX + reação motivada; QA de oclusão, duração, contato e correspondência da luz com as partículas |
| 04:04–04:08 | Close de personagem de tranças e armadura, corte para atendimento médico com partículas douradas | Variação expressiva e continuidade espacial do atendimento; checar animação de olhos, boca e reação ao efeito |
| 04:19–04:32 | Personagem ornamentada coloca a mão no ombro do protagonista, aproxima-se durante diálogo; plano médio para plano geral com arquitetura em arco | Continuidade de contato com personagem, bloqueio da cena, direção de olhares, transição entre enquadramentos |
| 04:37 | Cartela de personagem/número **009** com escrita em chinês, sem inferir metadados de produção | Formato serial de apresentação de personagem; pode inspirar livremente interfaces autorais e fichas do RPG |

## Avaliação qualitativa e limites

**Forças evidentes na amostra:** cinematografia com contraste âmbar/branco, desenho de luz, escala e arquitetura de cenários, materiais de vestimentas, acabamento facial detalhado, transições entre plano geral/médio/close/reaction, VFX de energia inseridos em ações, arcos de expressão com movimentos faciais e corporais e construção serial de mundo. O vídeo é **fantasia científica com visual 3D/CGI semirrealista**, não anime 2D japonês puro.

**Pontos de falha a investigar, não diagnosticar sem prova:** visão inconsistente do mesmo personagem em tomadas distantes; mão–mão e mão–objeto em 02:28–02:31; oclusão e sombreamento de efeitos 02:49 e 03:51; geometria persistente de roupas e armaduras; olhares e lip-sync real; dinâmica de multidão/background; saltos de câmera/continuidade espacial. A amostragem mostrou **movimento dentro das tomadas**, mas não valida a completude de todos os gestos. Não declarar “falha de IA” apenas por mudança de lente, pose ou corte.

**Atenção à estética:** iluminação, textura e enquadramento dessa referência são úteis como parâmetros de qualidade; **não** copiar personagens, vestimentas, cenas ou marcas. O projeto mantém **anime 2D japonês** como modo artístico distinto e a opção de **3D semirrealista** quando aprovada.

## Requisitos de produção a somar sem duplicar arquitetura

1. **Cinematic Direction & Editorial Bible** no contrato de shot: intenção dramática, escala (establishing/medium/close/insert/reaction), ângulo/eixo, referência de lente, movimentos, ritmo e raccord (olhar, gesto, posição, luz).
2. **Luz e composição por sequência:** key/fill/rim, valor, contraste, paleta emocional, profundidade atmosférica e passes de personagem/fundo/props/VFX; políticas de luz persistentes por ambiente.
3. **Atuação em camadas:** linha narrativa, áudio/visema, expressões, olhar, respiração, postura, gesto, reação e acabamento cabelo/roupa; preservar identidade entre tomadas.
4. **VFX com causalidade:** disparo por evento/gesto, fase de acumulação, pico, dissipação e resposta física/visual do ambiente, com oclusão consistente; evitar partículas sem vínculo causal.
5. **Edição orientada à narrativa:** shot list/animatic, seleção de takes, continuidade de ação e olhar, inserts, reação e pausas; som e edição tratados como etapas próprias, não apenas junção de clips.
6. **QA temporal/cross-shot e assets persistentes:** mãos, roupas, adereços, objetos pequenos, cenário, contato, perspectiva e luz; cada suspeita traz timestamp, evidência e revisor.

## Relação com o P15 e com a cena canônica Nólyrien

- Reutilizar [Issue #12](https://github.com/Furuya29/furuya-motion-studio/issues/12) e PR #13, com o piloto P15 (15s de blocking geométrico e prova experimental de sprites) **ainda não homologados artisticamente**.
- Esta referência fundamenta principalmente a camada **Direção / Luz / Editorial / VFX / Acting**; **não** substitui os motores de animação ou exige Claude, Higgsfield ou assinatura paga.
- O checkpoint da produção de Nólyrien continua dependente de correções em **asas implantadas na lombar**, faces dorsais voltadas à câmera traseira, coroa posterior, simetria de torso/quadril e arquitetura da torre redonda/cúpula conforme imagens canônicas já aprovadas. Não refazer quadros aceitos ou mudar proporções por inspiração neste vídeo.
- A meta da produção permanece **R$ 0**, preferencialmente com ferramentas existentes (FFmpeg, Blender/EEVEE compatível, OpenToonz/rigs 2D e orquestração PCRA quando disponível); não assumir GPU externa, implantação local ou capacidade de animar episódios inteiros sem provas.
- Toda referência externa fica como melhoria cumulativa. Nenhuma transição para 3D ou mudança de prioridade acontece sem decisão artística do proprietário.

**Próximo gate de evidência:** tornar os critérios de direção/edição verificáveis em um teste com vídeo original curto, comparar com amostras da referência e registrar defeitos por quadro e custo/tempo real; só promover o workflow depois de QA e aprovação humana.
