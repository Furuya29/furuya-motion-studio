# Referência 02 — SHIFT UP / “Wanna be in LOVE” feat. Evie (Stellar Blade: BLOODRAIN)

**Data:** 2026-11-08  
**Escopo:** estudo visual e temporal para o Projeto de Animação Automatizada, NÃO auditoria de assets internos da Shift Up.  
**Proveniência:** MP4 `1000589429.mp4` enviado pelo usuário; mídia de terceiros não copiada ao GitHub.

## Metadados reproduzidos do arquivo

| Propriedade | Valor |
|---|---|
| Vídeo | 1920 × 1080, H.264, 24 fps |
| Áudio | AAC estéreo, 44,1 kHz |
| Duração | 217,663855 s (03:37,66) |
| Frames de vídeo | 5.222 |
| Tamanho do arquivo recebido | 79.784.442 bytes (~76 MiB) |

A inspeção envolveu contatos visuais a cada 5 s ao longo da duração, tiras de 8 frames em 3 s (0,375 s entre amostras) para tomadas representativas e uma varredura de diferenças de luminância **a cada terceiro frame**, com decodificação sequencial do arquivo. Diferença de pixel alta pode significar corte/câmera e **não prova defeito de IA**; diferença baixa não prova frame congelado. Não houve validação objetiva de sincronização por fonema (audio-alignment), nem acesso ao projeto original do estúdio.

## Origem / contextualização verificada

O videoclipe oficial promove *Stellar Blade: BLOODRAIN* e usa IA generativa. O CEO Kim Hyung-tae afirmou que **Evie foi criada por artistas e modeladores humanos por mais de um ano** e que a IA foi usada para representar/apresentar os recursos produzidos; não divulgou o pipeline exato nem custo/hardware do videoclipe. Portanto **não deduzir investimento multimilionário ou “supercomputadores” a partir do acabamento visual**. Os “bastidores” com equipe visível na parte final são encenados com IA; não são registro de filmagem real.

Fontes:
- https://www.videogameschronicle.com/news/are-we-deadass-fans-react-to-official-ai-generated-stellar-blade-music-video/
- https://m.ajupress.com/amp/20260803150638274
- https://www.pushsquare.com/news/2026/08/evie-was-created-by-our-talented-artists-stellar-blade-dev-responds-to-ai-slop-accusations/
- https://www.gamesradar.com/games/action/stellar-blade-blood-rain-gets-official-music-video-full-of-ai-slop-and-fans-arent-happy-its-a-slap-in-the-face-to-your-artists/

## Log visual por tomada/trecho

| Timestamp (mm:ss) | O que está presente na tela | Qualidade / defeito a investigar |
|---|---|---|
| 00:00–00:10 | Microfone retrô em primeiro plano, título, reveal de Evie, arranha-céus verticais, cabos e tubulações. | Composição, profundidade, camadas e textura excelentes; a apresentação por objeto cria antecipação. |
| 00:10–00:18 | Performance frontal em macacão branco; movimentos de boca, piscadas, alterações discretas de cabeça e mãos. | Boca ativa com pouco deslocamento de ombros/peito/pescoço: microatuação limitada. |
| 00:18–00:21 | Extreme close de boca, depois face e olhos; personagens com aparência mais estilizada em um plano do que em outros. | Possível variação de identidade/escala ocular entre tomadas; model sheet obrigatório. |
| 00:25–00:35 | Tipografia “Wanna Be in LOVE”, performance em perfil, metrô; rosto passa do olhar baixo para alto. | Em 00:33–00:35 a aparência do rosto/olhos/cabelo varia perceptivelmente; parte pode ser motion blur/câmera. Evidência visual de inconsistência candidata. |
| 00:35–01:00 | Trem, mercado interno, cidade e performance ao microfone em vários ângulos. | Boa montagem de elipses espaciais; planos evitam longas interações sem controle. |
| 01:00–01:14 | Multidão e interior de trabalho; Evie observa cidade de passarela. | Parallax e escala interessantes; comportamento dos figurantes deve ser auditado. |
| 01:15–01:35 | Canto em perfil, mudanças de câmera, chuva/rua molhada e passarelas. | Ótima atmosfera; validar contornos estáveis do microfone e figurino durante movimento de câmera. |
| 01:35–01:45 | Figurantes no ambiente, Evie abaixa perto de personagem, close retorna à apresentação. | Contato no piso, anatomia de joelhos e equilíbrio são pontos de alto risco. |
| 01:45–01:55 | Evie usa hashi com comida em espaço movimentado. | Movimento mão-hashi-comida não deve virar textura sem geometria persistente. |
| 01:55–02:00 | Close da mão segurando objeto pendente diante de robô, deslocamento em corredor, paisagem urbana. | Topologia do objeto, oclusões e estabilidade da mão precisam de teste dedicado. |
| 02:00–02:15 | Pequeno jardim incrustado na cidade, cantora em close e planos em movimento. | Contraste orgânico/industrial muito forte; luz atmosférica e establishing shots úteis. |
| 02:15–02:20 | Corte entre perfil de corpo inteiro, câmera inclinada e giro da cantora. | Testar coerência da transformação espacial, giro corporal e proporções. |
| 02:20–02:26 | Sorriso com olhos em destaque, selfie e sinal V com mão. | Celular, dedos e contato são pontos frágeis; verificação explícita de contagem e geometria. |
| 02:26–02:35 | Caminhada sob guarda-chuva amarelo em corredor com poças; área industrial. | Destaque de cor; testar pé-no-chão, reflexo e geometria do guarda-chuva em todos os frames. |
| 02:35–02:50 | Sentada ao lado de vegetação, close dramático e perfil, volta a ambiente cinzento. | Boa alternância emocional; persistência de cabelo e figurino requer conferência. |
| 02:50–03:00 | Personagem deitada no microjardim, título final. | Pausa visual útil; composição mais fácil de manter porque movimento é reduzido. |
| 03:00–03:28 | “Making of”: operador, diretor, luzes, câmeras, cumprimentos, ajuste de cabelo e mãos. | A “veracidade” documental é deliberadamente fabricada; interações pessoa-objeto-mão continuam criticamente difíceis. |
| 03:28–03:37,66 | Cartelas, avisos e encerramento. | Não confundir texto ficcional/cenas de set com prova de método real. |

## Matriz de qualidade (avaliação qualitativa da amostragem, não nota de um benchmark formal)

| Critério | Diagnóstico |
|---|---|
| Cenografia, escala e atmosfera | **Forte**: arquitetura, neblina, cores, profundidade, objetos industriais. |
| Direção de câmera e montagem | **Forte**: alternância plano aberto / médio / close; diversidade de ambientes e ritmo. |
| Rosto e identidade cross-shot | **Insuficiente para nosso alvo**: diferenças visuais perceptíveis em 00:18–00:21 / 00:33–00:35. |
| Atuação corporal | **Mediana**: canto em boa parte sustentado por poses e microexpressões. |
| Sincronismo labial | **A revisar**: boca articula, mas não foi feito alinhamento técnico áudio/fonemas; críticas externas apontaram problema. |
| Mãos/contato com props | **Área de risco alto**: hashi, objeto pendente, telefone, guarda-chuva, cumprimentos. Nem toda cena mostra falha conclusiva. |
| Continuidade espacial | **Misto**: planos individuais fortes; cortes rápidos reduzem necessidade de provar topologia persistente. |
| Realismo da produção exibida | **Encenação**: falso making-of não pode provar set/hardware/custo. |

## Decisões incorporadas ao nosso pipeline

1. **Bíblia de personagem obrigatória**: rosto neutro, 3⁄4, perfil; turnaround corporal; paleta de roupa; props com geometria fixa; mapas de oclusão. Uma imagem de referência não é garantia de consistência cross-shot.
2. **Shot spec como unidade de produção**: shot_id, intervalo, ação, câmera (focal/posição/movimento), geometrias, personagens, falas, emoção, continuidade, material/luz, máscara, input/output, revisão.
3. **Movimento ANTES da estilização**: no 3D usar rig de esqueleto, IK e constraints; no 2D usar deformação por esqueleto, meshes e troca de desenho para extrema mudança de perspectiva. Gerar movimentos com IA livre apenas como opção controlada, não fonte primária para todas as cenas.
4. **Voz/expressão coordenadas**: sequência fonética, pose de boca, mandíbula, olhos, respiração, pescoço e ombros. Comparar fonemas com trilha; não tomar boca que abre e fecha como lip-sync validado.
5. **Props persistentes e interação física**: object IDs, sockets de mão, pontos de contato, profundidade e materiais. Objetos pequenos exigem render ou máscara em passe próprio.
6. **Cenário 3D leve ou multiplano** para câmera e parallax reais, luz consistente, perspectiva de linhas e volumetria econômica.
7. **Módulo de QA temporal e cross-shot**: detectar falsos cortes, drift de rosto/cabelo/roupa, mudanças de mãos/props, foot sliding, oclusão, ghosting e flicker; classificação automática como triagem, revisão visual para aprovação.
8. **Áudio e montagem**: os cortes, pausas, cores e trilha devem ser desenhados conscientemente; montar no editor e FFmpeg. Cortes mascaram defeitos, mas não devem substituí-los por padrão.
9. **Não copiar imagens/música/assets da Shift Up** para o nosso produto: inspiração técnica e estilística não substitui licenciamento.

## Ferramentas candidatas reais R$ 0 (precisam de testes no nosso hardware)

- **Blender 4.5 LTS / 5.x (conforme compatibilidade)**: armature/IK, shape keys e câmera; EEVEE/viewport são prioridade local. Docs: https://www.blender.org/download/requirements/ e https://developer.blender.org/docs/release_notes/4.5/eevee/
- **Atenção RX 580:** Blender Cycles GPU/HIP exige AMD RDNA1 ou superior; RX 580 (Polaris) não se qualifica. Não inventar suporte HIP. Docs: https://docs.blender.org/manual/id/4.5/render/cycles/gpu_rendering.html
- **OpenToonz / Plastic Tool**: estrutura de esqueleto e mesh para animação 2D limitada entre desenhos-chave. https://opentoonz.readthedocs.io/en/latest/create_animations_using_plastic_tool.html
- **Rhubarb Lip Sync**: geração automática de formas de boca 2D com base no áudio; verificar naturalidade/PT-BR e adaptar a plano facial 3D se necessário. https://github.com/DanielSWolf/rhubarb-lip-sync
- **FFmpeg**: montagem, análise, comparação, extração temporal, render e transcodificação.
- Computação em nuvem grátis: **não assumir GPU ilimitada ou serviço permanente**; só incluir após prova de disponibilidade, restrições e termos.

## Gate de aceite — piloto de 15 segundos

- 2–3 planos: (A) apresentação e close com fala; (B) corpo em deslocamento e mudança de câmera; (C) mão interagindo com objeto em cenário persistente.
- Rosto, figurino, cabelo, objeto e escala iguais entre vistas, sem deformação crítica.
- Pés fixam no chão durante fases de apoio; mãos não mudam de contagem nem se fundem a objetos.
- Boca e olhar coerentes com fala/emoção e movimento de mandíbula/respiração.
- Export sequencial frame a frame, análise cruzada dos 3 planos e aprovação humana.
- Tempo de produção, versão das ferramentas, consumo local de RAM/VRAM e custo externo registrados.
- **Status atual:** pesquisa e análise do vídeo concluídas; pipeline proposto **não implementado ou homologado** neste commit.

## Comparação com referência 01 — TS Malfoy

- **TS Malfoy**: 09:04, 30 fps, fotogramas atraentes, longos segmentos dramáticos sustentados por poses e rosto.
- **Shift Up**: 03:37, 24 fps, design urbano e linguagem de videoclipe com cenografia expressiva, rosto com deriva e plano BTS sintético.
- **Transferir para o projeto** a fotografia do primeiro e a profundidade/variedade de cenas do segundo, combinando com gestual e controles geométricos que ambos deixam como oportunidades de melhoria.
