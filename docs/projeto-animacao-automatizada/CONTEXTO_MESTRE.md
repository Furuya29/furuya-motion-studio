# Projeto de Animação Automatizada — contexto mestre

> Registro persistente de continuidade do projeto de produção cinematográfica e animação (2D anime japonês / 3D semi-realista e realista), separado do fluxo de *recast* de vídeos virais do Furuya Motion Studio. Atualizado em 2026-11-08.

## Missão e requisitos permanentes

- Construir um pipeline de animação audiovisual com qualidade cinematográfica superior às referências observadas, evitando “cara de IA”.
- Preservar identidade de personagens (rosto, cabelo, anatomia, roupas), relações espaciais, continuidade de cenários e objetos, materiais, iluminação e direção entre cortes.
- Permitir **anime 2D japonês** genuíno, 3D ou estética híbrida, sem obrigar a renderização em estilo ocidental.
- Não limitar a produção a desenho quadro a quadro: combinar **quadros-chave**, rigs 2D/3D, captura/retargeting de movimento, interpolação guiada, composição e geração de vídeo por IA apenas onde melhora o resultado.
- Dar suporte a atuação expressiva, movimentação corporal, câmera (planos, ângulos, movimento), cenários persistentes, interação e multidões.
- Custo operacional alvo: **R$ 0**; privilegiar software livre, recursos locais e opções gratuitas realmente disponíveis. Não supor acesso a GPU de datacenter.
- Hardware previamente informado: PC Windows 10 Pro, AMD FX-4300, ~16 GB RAM, Radeon RX 580 8 GB; Android Redmi K70 Ultra. Projetos conexos (PCRA / Android Agent / Furuya Motion Studio) permanecem independentes; não confundir produção de filmes com substituição de dançarinos.
- Supervisão humana para aprovação artística, QA e intervenções inevitáveis; automatizar a rotina técnica sempre que possível.

## Evidência nº 1 — “TS Malfoy” (Fantasoner)

- Referência: https://www.youtube.com/watch?v=WYRDe8XsRmI — curta de fãs do universo Harry Potter, personagem Draco Malfoy feminina, declarado gerado com IA.
- Arquivo examinado pelo usuário: `1000589408.mp4` (não armazenado neste repositório por direitos e tamanho).
- Propriedades observadas: **1920 × 1080, 30 fps, 16.328 frames, 09:04,27**.
- Artefatos locais derivados na conversa: `Analise_Tecnica_TS_Malfoy_Animacao_IA.pdf`, `Evidencias_Visuais_TS_Malfoy.zip`. Esses arquivos não estão hospedados no GitHub; a presença apenas nesta conversa não garante acesso permanente ao binário.
- Observações resumidas: fotografia e direção de arte fortes; arquitetura e atmosfera coerentes na amostragem; atuação facial expressiva; montagem por cortes e poses relativamente sustentadas, com movimentos discretos de boca/olho/cabelo; desafios de animação corporal, continuidade de objetos, contato e movimentos longos.
- Sequências estudadas: 00:00–00:02 (olhos), 01:20–01:22 (fala), 04:40–04:42 (interação com armário), 06:20–06:22 (gesto/ameaça), 07:15–07:17 (duas personagens), 08:40–08:42 (close).
- Nota de QA: diferenças de pixels entre quadros **não equivalem** diretamente a deformações ou a “quadros congelados”; cenas escuras e compressão enviesam métricas. Não atribuir pipeline específico sem evidência do criador.

## Decisões após referência 1

1. **Priorizar representação consistente de personagens e cenários** antes de renderizar sequências longas.
2. **Direção por tomada** (shot specification: personagens, câmera, lente, movimento, duração, luz, ação, emoções, continuidade).
3. **Animação controlável**: usar rig / keyframes / motion tracking / retargeting como fonte geométrica do movimento, quando necessário.
4. **Geração de IA como camada supervisionada**, com comparação temporal e revisão de falhas em mãos, cabelos, roupas, objetos e expressões.
5. **Montagem / composição final** em editor/FFmpeg, com som e efeitos.
6. Teste-alvo inicial: **15 segundos**, planos distintos e pelo menos uma interação física, sob critérios mensuráveis; não prometer longa-metragem homogêneo por custo zero antes de validar.

## Referência nº 2 — Shift Up / Stellar Blade: BLOODRAIN

- Video recebido: `1000589429.mp4`, videoclipe **“Wanna be in LOVE” (Evie)**, duração **3:37,66**, **1920 × 1080, 24 fps, 5.222 frames**.
- Identificação pela cartela do próprio arquivo e fontes externas.
- Fontes públicas: https://www.videogameschronicle.com/news/are-we-deadass-fans-react-to-official-ai-generated-stellar-blade-music-video/ ; https://m.ajupress.com/amp/20260803150638274 ; https://www.pushsquare.com/news/2026/08/evie-was-created-by-our-talented-artists-stellar-blade-dev-responds-to-ai-slop-accusations .
- O CEO descreveu Evie como personagem desenvolvida por artistas e modeladores por mais de um ano, com apoio de IA na apresentação audiovisual; custo, hardware e pipelines exatos do videoclipe **não confirmados**.
- O “making of” ao final é encenado/gerado; não interpretar como evidência documental de filmagem física.
- Análise detalhada concluída em `REFERENCIA_02_SHIFTUP_BLOODRAIN_2026-11-08.md`, com diagnóstico temporal por timestamp, limites de evidência, recomendações e gates de QA. Implementação do piloto está aberta em https://github.com/Furuya29/furuya-motion-studio/issues/12.
- **Não armazenar MP4 de terceiros nem materiais protegidos neste repositório** sem licença. Guardar metadados, fontes, anotações técnicas e decisões.

## Próximas provas

- Personagem com identidade invariável frente/perfil/3⁄4 e em movimento.
- Microatuação: emoções, olhar, fala com fonemas e respiração coordenados.
- Ação com contato: mãos, objeto, chão/parede, oclusão.
- Camera-tracking espacial, cenário persistente e continuidade entre dois takes.
- Registro de defeitos com timestamp, severidade, categoria e solução; reprovação automática de deformação crítica.

## Política de evidência

Distinguir: (A) fatos dos metadados do arquivo; (B) inspeção de frames; (C) fatos de fontes públicas; (D) hipóteses, recomendações ou testes pendentes. Nunca relatar hipótese como resultado comprovado.

## Controle de continuidade

Este documento é a referência mestre, que deve ser atualizada em novas análises, sem excluir as decisões existentes. Não transferir credenciais, dados pessoais ou arquivos protegidos de terceiros ao GitHub.

## Handoff integrador para o chat principal (08/11/2026)

- [Handoff completo e aditivo](HANDOFF_INTEGRACAO_CHAT_PRINCIPAL_2026-11-08.md) — consolida TS Malfoy e Shift Up, novos defeitos de perspectiva do microfone e variações das proporções corporais, estratégias de correção, requisitos de QA e plano de integração.
- **Regra superior de continuidade:** este handoff **NÃO substitui** as decisões, planos, arquiteturas ou checkpoints existentes no chat principal. Integrar como complemento, reconciliando com o histórico principal.
- A pasta atual documenta **esta frente de pesquisa**, não é prova de que toda documentação histórica do chat principal tenha sido migrada.

## Registro de reconciliação aditiva — 09/11/2026 (em revisão)

- [Reconciliação cumulativa](RECONCILIACAO_ADITIVA_2026-11-09.md): classifica fatos anteriormente decididos, testes reforçados, restrições e pendências após o handoff; **não substitui o planejamento principal**.
- [Shot spec do piloto 15 s](piloto_15s_shot_spec_v0_1.json): três planos de 120 quadros a 24 fps, com IDs de personagem/cenário/prop, câmera/contato e gates de QA. **Especificação, não vídeo renderizado**.
- [Validador estrutural](../../tools/animation_pilot/validate_shot_spec.py) e [testes de contrato](../../tests/test_animation_pilot_spec.py): checam integridade dos dados, não qualidade artística. A execução no PC, materiais originais, aprovação do usuário e homologação seguem pendentes.
- Nenhuma ferramenta, serviço, projeto de recasting, prioridade ou arquitetura anterior foi removido; a adoção definitiva depende de revisão e conciliação com o chat principal.

## Avanço experimental do motor — 09/11/2026

- [Protótipo P15 executável](PROTOTIPO_P15_EXECUTAVEL_2026-11-09.md): *blocking* técnico determinístico de 15 s/360 frames, motor de câmera e microfone persistente; demonstração **não é arte final nem QA da Issue #12**.
- [Rig 2D por sprites](MODULO_RIG_2D_SPRITES_2026-11-09.md): motor experimental de PNGs por camadas, pivôs FK, interpolação e troca discreta de desenhos; amostra criada programaticamente, sem IA generativa.
- Implementações propostas em `tools/animation_pilot/`, com testes em `tests/` e CI isolada. A validação no Windows do usuário e a aprovação estética permanecem pendentes.
- PR [#13](https://github.com/Furuya29/furuya-motion-studio/pull/13) em revisão; nenhuma dessas adições substitui as ferramentas, prioridades ou decisões do planejamento anterior.

## Atualização aditiva em revisão — 16/11/2026

- [Checkpoint cumulativo 16/11](CHECKPOINT_CUMULATIVO_2026-11-16.md): reconcilia o handoff de 08/11 com o P15 e rig 2D experimentais da [PR #13](https://github.com/Furuya29/furuya-motion-studio/pull/13), a continuidade visual ainda pendente de Nólyrien (asas lombares, vista dorsal, coroa posterior e simetria do torso) e as três referências audiovisuais recentes (dois AI manhua e tutorial Claude Code).
- Esta anotação está **na branch de revisão**, não na `main`, até aprovação do PR. Não representa renderização de novos frames, homologação do piloto cinematográfico nem acesso produtivo ao PCRA.
- Preservar prioridades do chat narrativo e manter a [Issue #12](https://github.com/Furuya29/furuya-motion-studio/issues/12) aberta até evidências de arte, vídeo, QA, desempenho e aprovação humana.

- [Referência 06 — novas ferramentas chinesas anunciadas como gratuitas](REFERENCIA_06_FERRAMENTAS_CHINESAS_VIDEO_2026-11-16.md): triagem inicial do vídeo de 16/11/2026, baseada exclusivamente em metadados públicos; três plataformas, gratuidade, resultados e integração ainda **não verificados**. Nenhuma mudança de motor, custo ou prioridade foi autorizada.

- [Referência 07 — Seravienne / fantasia com elfos](REFERENCIA_07_SERAVIENNE_FANTASIA_ELFOS_2026-11-16.md): obra de inspiração RPG/MMO (EP01–03) e edição relacionada, registrada como referência temática/de direção artística. Sem inspeção quadro a quadro, motor de IA verificado ou homologação; não alterar prioridades nem cenas aprovadas de Aenvarath.

- [Referência 08 — vídeo enviado: Wildland Hunters, direção cinematográfica e edição](REFERENCIA_08_WILDLAND_HUNTERS_DIRECAO_CINEMATOGRAFICA_2026-11-16.md): análise visual real do MP4 de 04:40, 1920×1080/30 fps, 47 stills e oito tiras temporais; estudo de luz, enquadramentos, atuação, VFX e raccord, com limites explícitos de QA. Não substitui estética 2D, arquitetura, decisões ou gates do P15.

## Handoff integral da conversa de referências — 16/11/2026

- [Handoff integral 16/11 (50 mil caracteres)](HANDOFF_INTEGRAL_CHAT_REFERENCIAS_2026-11-16.md): história cronológica completa deste chat, decisão superior de preservação, handoff original de 08/11, oito referências, MP4s analisados, artefatos e hashes, resultados do P15/rig, restrições do PCRA, continuidade Nólyrien, decisões, pendências, riscos e roteiro de retomada.
- **Uso em novo chat:** ler o handoff integral em conjunto com as fontes canônicas anteriores e com os checkpoints artísticos do chat principal. Trata-se de documentação **aditiva na branch draft**, não reordenação de prioridades ou autorização de merge/homologação.

## Continuidade do chat narrativo e arquitetura do palácio — 16/11/2026

- [CHECKPOINT_NARRATIVO_ATUALIZADO_AENVARATH_2026-11-16.md](CHECKPOINT_NARRATIVO_ATUALIZADO_AENVARATH_2026-11-16.md) — registra a progressão do chat principal para além da fase das asas, até a imagem da rainha voando acima da torre circular, sem confundir quadro estático e MP4 homologado; preserva as regras de canon e os estados de prova.
- [PLANO_ARQUITETONICO_PALACIO_REAL_2026-11-16.md](PLANO_ARQUITETONICO_PALACIO_REAL_2026-11-16.md) — pré-especificação do palácio colossal e geometria circular da torre, eixo longitudinal do salão do trono, tapete, brasão, janelas, projeto de planta e gates de match-camera/Unreal; **proposto, não uma planta final aprovada**.
- Esta atualização é **aditiva e somente na branch draft**; não altera os estudos anteriores, não significa merge para a main, não muda prioridade do P15/Issue #12, não é renderização nem homologação do PCRA.

## Modelo definitivo de engenharia do Estúdio de Animação — reconciliação do plano inicial em 16/11/2026

- **Documento de leitura principal do modelo de animação:** [ARQUITETURA_CONSOLIDADA_MEGA_ESTUDIO_ANIMACAO_2026-11-16.md](ARQUITETURA_CONSOLIDADA_MEGA_ESTUDIO_ANIMACAO_2026-11-16.md) — integra o plano original de Estúdio de Animação & Cinemáticas (Traditional 2D, Motion Comic, 3D & Hybrid, Cinematic Composition, Asset & Character Consistency), a decisão **multimétodo por tomada**, técnicas de key drawings/inbetweens, rigs/Plastic/IK/FK, cenários 3D, composição, QA e os critérios cinematográficos das referências mais recentes, sem substituir os módulos existentes.
- O handoff integral original do plano inicial, fornecido pelo proprietário, foi conservado **em repositório privado de Aenvarath**, para proteger lore e informações operacionais. Este documento público registra apenas a arquitetura técnica reconciliada e o hash da fonte, sem republicar o conteúdo integral privado.
- **Status real:** documento e protótipos experimentais versionados na branch draft do [PR #13](https://github.com/Furuya29/furuya-motion-studio/pull/13). A [Issue #12](https://github.com/Furuya29/furuya-motion-studio/issues/12) segue aberta; nenhum filme artístico, rig completo, pipeline Windows/PCRA ou estúdio foi homologado apenas por este registro. Não alterar a `main` sem revisão e aceite.

## Decisão de produção — não usar Motion Comic como formato final de Aenvarath (16/11/2026)

- O proprietário registrou experiência anterior insatisfatória com Motion Comic. Para **The Darkness of Aenvarath**, Motion Comic não é motor principal, fase obrigatória nem entrega cinematográfica final. Mantê-lo apenas como módulo **opcional fora do caminho crítico**, sem eliminar integrações editoriais prévias.
- Foco de engenharia: personagem realmente animado e on-model via **3D/híbrido, rig 2D apropriado e desenho/intervalação onde necessário**, com geometria de cenário e câmeras persistentes, não uma apresentação de stills com pan/zoom.
- A política e os gates realistas estão no [documento consolidado de arquitetura](ARQUITETURA_CONSOLIDADA_MEGA_ESTUDIO_ANIMACAO_2026-11-16.md).
- **Prova inicial de capacidade executada:** preview de 4 segundos de ambiente (neve, fumaça, brasas e câmera), 960×540/24fps/96 frames, com FFmpeg/FFprobe e script [`preview_village_environment.py`](../../tools/animation_pilot/preview_village_environment.py). É **movimento ambiental validado em ambiente isolado**, não atuação, rig, lip-sync ou anime final, nem execução Windows/PCRA. Os assets de Aenvarath e a evidência narrativa permanecem no repositório privado.
- **Próxima barreira de aceite:** demonstrar animação corporal verdadeira em uma personagem identificável com assets canonizados, fontes de movimento e QA, antes de declarar que a técnica alcança a animação completa pretendida.

## Nova referência — Seedance 2.5 e APOB AI (18/11/2026)

- [Referência 09 — tutorial cinematográfico com Seedance 2.5 e APOB AI](REFERENCIA_09_APOB_SEEDANCE_25_CINEMA_2026-11-18.md): descreve personagem consistente, roteiro via ChatGPT, geração por texto/imagem, edição e extensão de tomadas e limites promocionais. Documentação oficial da ByteDance confirma até 30 s e multirreferência; **APOB informa plano Nano 80 créditos/dia, mas exemplo Seedance 2.5 custa 1.000 créditos por 5 s**, logo R$0 sustentável **não foi comprovado**. Manter apenas como referência/pesquisa sem alterar o multimétodo, o caminho crítico de animação corporal ou as prioridades do PCRA/Aenvarath. Nenhuma renderização executada.

## Referência 10 — alegações de IA gratuita diária (20/11/2026)

- [Verificação de Google Vids, Everypixel, VidoGrid e Freebeat AI](REFERENCIA_10_VIDEOS_IA_GRATUITOS_GOOGLE_EVERYPIXEL_VIDOGRID_FREEBEAT_2026-11-20.md): análise independente das cotas reais relacionadas ao vídeo de Mari C. Google Vids: 3 vídeos de até 15s por mês; Everypixel: 300 créditos/mês e teto diário de 40; VidoGrid: anúncios de gerações diárias sem cota quantitativa comprovada; Freebeat: 500 créditos iniciais e ilimitado associado a planos pagos específicos. **Nenhuma alternativa foi homologada como geradora gratuita ilimitada**. Pesquisa aditiva, sem alterar prioridades, PR #13 ou a exigência de animação corporal real em Aenvarath.

## Referência 11 — Skill cinematográfica por agentes (21/11/2026)

- [Vídeo “Essa Skill Faz Vídeos de CINEMA Sozinha” — Web Dark](REFERENCIA_11_AGENT_SKILL_CINEMA_AUTOMATIZADO_2026-11-21.md): triagem de uma proposta de skill portátil para Claude Code/Codex/Antigravity. Identificação do vídeo confirmada, mas arquivo `SKILL.md`, repositório oficial, licença, custo efetivo e resultados audiovisuais completos **não localizados nem testados**. Potencial de **orquestração de direção/edição por agente** como camada adicional sobre a arquitetura já aprovada, sem substituir animação por quadros-chave/rigs/3D, sem mudar o ChatGPT/PCRA e sem instalação ou homologação de software.

## Referência 12 — filme local com IA: MiniMax H3 e ComfyUI (24/11/2026)

- [Estudo do vídeo de Willian IA e do MiniMax H3](REFERENCIA_12_WILLIAN_IA_FILME_LOCAL_MINIMAX_H3_2026-11-24.md): a página do tutorial anuncia criação de filme “100% grátis no PC”; palavras-chave abrangem ComfyUI/MiniMax H3, Blender, Qwen Image Edit e LoRAs, mas **não há inspeção integral do vídeo nem do workflow do criador**. Fontes oficiais confirmam H3 com pesos distribuídos e controle por referências/poses/áudio. **Riscos importantes:** execução local não comprovada no FX-4300/16GB/RX580 8GB e, segundo ComfyUI, outputs comerciais exigem licença apropriada. Catalogar como RESEARCH_ONLY, sem instalação, auto-route, despesa, alteração do método multimétodo ou homologação cinematográfica.

## Referência 13 — Perchance, imagens gratuitas (24/11/2026)

- [Análise do Perchance e vídeo de “imagens grátis, sem filtro e sem limites”](REFERENCIA_13_PERCHANCE_IMAGENS_GRATUITAS_2026-11-24.md): site oficial perchance.org confirma gerador de **imagens** sem cadastro/quotas de créditos convencionais, com FAQ permitindo uso comercial da saída sem atribuição. Entretanto, **os termos de serviço restringem bots e scripts**, e o gerador de texto→imagem não demonstra travamento robusto de identidade/câmera entre imagens. Catalogar como **pesquisa e ideação manual**, sem auto-route PCRA, sem substituir animação real, fichas canônicas ou método multimétodo, e sem reproduzir dados privados em galerias públicas. Nenhum teste de geração foi feito.

## Referência 14 — Google Flow e automação de vídeos longos por Tool (24/11/2026)

- [Análise do tutorial de Erickson Lourenço sobre Flow, Omni Flash, Tools e montagem de vídeos longos](REFERENCIA_14_FLOW_LONGFORM_AUTOMACAO_TOOLS_2026-11-24.md): guias do autor consultados e documentação oficial do Google confrontada. **Criar Tools personalizadas realmente existe, porém requer assinatura Google AI Plus/Pro/Ultra; só explorar/usar Tools prontas é possível sem assinatura.** A conta não assinante tem 50 créditos Flow/dia; Omni Flash 1.2 gera/edita clipes de 3–10s e extensão nativa exige assinatura. Preservar como referência de **orquestração de tomada + montagem local automática**, sem depender de Tool paga, sem duplicar o motor multimétodo de Aenvarath, sem eliminar rig/keyframes/QA e sem afirmar vídeo longo produzido ou edição comprovada. Pesquisa/registro apenas, PR #13 continua em revisão.
