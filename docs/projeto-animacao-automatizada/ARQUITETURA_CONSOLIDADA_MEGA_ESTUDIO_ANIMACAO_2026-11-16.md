# Arquitetura consolidada — Estúdio de Animação & Cinemáticas (v0.1)
**Data:** 16/11/2026  
**Estado:** **decisões de método reconciliadas e registradas; implementação artística completa pendente**. Este documento é aditivo e está em *branch* de revisão do [PR #13](https://github.com/Furuya29/furuya-motion-studio/pull/13). Não equivale à homologação do estúdio, à aprovação de nova ferramenta nem à alteração de prioridades.

## Decisão mais recente — produção de animação completa, não motion comic (16/11/2026)

**Diretriz expressa do proprietário:** o histórico de um Motion Comic anterior revelou complexidade e resultados insatisfatórios. **Aenvarath NÃO adotará Motion Comic como pipeline principal, como estilo de entrega nem como fase obrigatória.** O objetivo artístico é animação completa e detalhada com atuação, locomoção, asa/voo, câmera, combate, contato, continuidade espacial e som. Movimentar uma imagem inteira com zoom, partículas e cortes **não** constitui prova de animação completa.

O módulo Motion Comic permanece somente como **opção desativada (opt-in) para projetos editoriais independentes** ou animação de pré-visualização sem pretensão de ser resultado final; sua eventual utilização só ocorrerá com aprovação explícita e prova de que pode atingir a meta pretendida. Não eliminar código ou interromper operações existentes de recap/AVPE.

**Núcleos no caminho crítico de Aenvarath:** Asset & Character Consistency, 3D & Hybrid, Traditional 2D Animation, Cinematic Composition. O processo seleciona os recursos que de fato consigamos operar e testar, sem implantar softwares novos antes de provar capacidade. A escolha técnica por plano deve demonstrar **movimento genuíno dos elementos dramáticos**, não somente câmera sobre still, antes de ser considerada método de personagem.

**Gate de realismo operacional:** cada etapa precisa produzir arquivo reproduzível, comando/código, checksum, relatório, limitações explícitas e aceite visual. Promessas de um estúdio autônomo completo não substituem testes. Caso faltem modelos, camadas, pivôs, 3D, permissões, compute ou fontes, marcar **BLOQUEADO/PENDENTE** e executar apenas uma prova reduzida, nunca improvisar homologação.

## 0. Fonte, escopo e precedência
**Fonte primária do plano inicial:** handoff integral fornecido pelo proprietário, `HANDOFF_INTEGRAL_MEGA_ESTUDIO_ANIMACAO_2026-11-16.md` (16/11/2026; 644 linhas; SHA-256 do upload `e897606c8b75d918e2915ca680f84270994d4a2075f022153474bae60177e3fe`). O original foi arquivado **integralmente no repositório privado do projeto narrativo**, não copiado para este repositório público.

**Fontes posteriores complementares:** [CONTEXTO_MESTRE.md](CONTEXTO_MESTRE.md), [handoff 08/11](HANDOFF_INTEGRACAO_CHAT_PRINCIPAL_2026-11-08.md), [reconciliação 09/11](RECONCILIACAO_ADITIVA_2026-11-09.md), [handoff de referências 16/11](HANDOFF_INTEGRAL_CHAT_REFERENCIAS_2026-11-16.md), [P15](PROTOTIPO_P15_EXECUTAVEL_2026-11-09.md), [rig experimental](MODULO_RIG_2D_SPRITES_2026-11-09.md), [checkpoint narrativo](CHECKPOINT_NARRATIVO_ATUALIZADO_AENVARATH_2026-11-16.md), [palácio](PLANO_ARQUITETONICO_PALACIO_REAL_2026-11-16.md).

**Precedência:** pedido explícito e mais recente do proprietário > assets e checkpoints efetivamente aprovados > canon versionado posterior > decisões anteriores não revogadas > propostas técnicas. **Não descartar nem reescrever uma técnica já escolhida** só porque outra referência mostrou resultados visualmente impressionantes. Não transformar proposta em recurso homologado.

**Separação:** (i) Estúdio de Animação & Cinemáticas — produção autoral; (ii) AVPE/RendaOnline — vídeos e operações editoriais/comerciais; (iii) Furuya Motion Studio — recast de vídeos existentes; (iv) MMORPG de Aenvarath — arte, lore e Unreal; (v) PCRA — orquestração do Windows. Interfaces compartilhadas não implicam união de código, dados, permissões ou prioridades.

## 1. Decisão central e definitivo critério de escolha
O modelo adotado é **MULTIMÉTODO POR TOMADA** (*shot-adaptive animation pipeline*), não um gerador universal de vídeo, nem desenho individual de cada frame como regra.

O pipeline combina, conforme necessidade:
- **Key drawings/genga** autorais ou assistidos por IA de imagem, aprovados como arte; desenhos intermediários/douga **geométricos ou desenhados** de acordo com dificuldade.
- **Rigs 2D/cut-out, sprites, pivôs FK, IK, malhas deformáveis/Plastic**, bibliotecas de visemas, loops e animações reutilizáveis.
- **OpenToonz / Krita / Blender Grease Pencil** e similares para exposição, arte, animação de linhas e correções.
- **Modelos e cenários 3D persistentes**, câmeras reais, bloqueio, rigging, captura/retargeting quando útil, cel shading/NPR/híbrido.
- **Composição, edição, som e QA** usando FFmpeg/Python e Remotion, com Kdenlive/MLT, CapCut e Premiere como editores complementares preservados.
- **IA de vídeo** apenas rota opcional/experimental para tomadas onde agrega valor real, sujeita a limite gratuito, licença, consistência temporal e aprovação. **Nunca tornar obrigatória nem gerar todos os quadros isoladamente do zero por padrão.**

**Níveis de complexidade:**
- **A — limitada inteligente:** diálogos, olhos, visemas, respiração, balanço de cabelo/capa, movimentos sutis, animação ambiente, cenários em multiplano, parallax, ciclos de caminhada. Preferir rig, keyframes, loops, camadas e composição.
- **B — 2D tradicional assistida:** mudanças de pose significativas, acting de tronco/braço, deslocamentos, substituição de vistas 3/4/perfil/costas, ações moderadas. Exigir desenhos-chave, Xsheet, intervalação apropriada e *on-model QA*.
- **C — sakuga/ação complexa:** combate, contato, grandes rotações, perspectiva dinâmica, múltiplos corpos/armas, transformações. Exigir blocking espacial 3D/mocap quando útil, poses aprovadas, inbetweens corretivos, recursos de animação tradicional e edição; IA generativa supervisionada só quando passar nos gates.
- **Cinemáticas 3D/híbridas:** usar 3D como base geométrica persistente quando há arquitetura monumental, órbita de câmera, contato ou necessidade de reutilização no jogo, podendo manter desenho/anime como acabamento. O modo 3D **não revoga** o modo 2D puro.

**Regra de troca de vista:** não deformar ilustração frontal para fingir perfil/costas ou grandes rotações. Requerer múltiplas vistas aprovadas ou rig/3D que preserve anatomia em perspectiva. O método pode mudar **dentro da mesma cena**, mas cada *shot* tem fonte de geometria/movimento declarada.

## 2. Os cinco núcleos funcionais (decididos como escopo; não todos implementados)
| Núcleo | Responsabilidade | Estado neste checkpoint |
|---|---|---|
| **Traditional 2D Animation Engine** | Storyboard/animatic, genga/douga, Xsheet, exposição 1s/2s/3s, traço/pintura, rigs, malhas, inbetweens e export | Planejado; existe **rig sprite/FK experimental**, não o motor tradicional completo |
| **Motion Comic Engine (fora do caminho crítico)** | Recurso editorial opcional/legado para outros projetos e eventual pré-visualização; **não é formato-alvo de Aenvarath** | Suspenso para Aenvarath, só com opt-in explícito, sem remover projetos existentes |
| **3D & Hybrid Engine** | Cenários/modelos persistentes, rigs 3D, câmeras, perspectiva, IK/contato, estilização e cinemáticas do MMORPG | Planejado; nenhum palácio definitivo/modelo canônico homologado |
| **Cinematic Composition Engine** | Iluminação, VFX, câmera, narrativa, pacing, sound design, edição, cor, legenda, encode e QA | Planejado; FFmpeg já usado no **animatic geométrico**, não em filme final |
| **Asset & Character Consistency Engine** | Bible de personagens, turnarounds, ID/hash/estado, poses, roupas, expressões, animações e cenários, preservação cross-shot | Planejado; schemas/validadores estruturais experimentais não validam identidade artística |

**Orquestração transversal:** ChatGPT/planejador → PCRA autorizado → job/versionamento/artefatos → engine específico → QA e aprovação humana. Reusar AVPE para operações técnicas compartilháveis sem torná-lo proprietário do cânone de animação.

## 3. Ferramentas: catálogo mantido, sem declarações falsas de instalação
**Pilares prioritários para testes e integração por capacidade:**
- `Krita` para arte/character sheets/genga/pintura.
- `OpenToonz` para Xsheet e Plastic Tool; comparar `Tahoma2D` antes de instalar duplicidades.
- `Blender` para Grease Pencil, câmera, rig, cenários, cel shading e bloqueio 3D; `EEVEE` ou alternativas compatíveis com hardware real.
- `Python + FFmpeg/FFprobe` para processamento, testes e render/controlabilidade; `Remotion` para composição programática quando licenciamento/desempenho permitirem.
- `CapCut` e `Premiere` continuam ferramentas de edição/pós-produção e automações em andamento. **Não abandonar** nem sobrescrever projetos.
**Candidatos não obrigatórios:** `Godot`, `Inochi2D`, `Live2D` (ver limitações free/comercial), `Kdenlive/MLT`, `Rhubarb Lip Sync` (provar pt-BR), `RIFE/optical flow`, `EbSynth`, motion capture/retargeting e modelos generativos. A disponibilidade, licença, integração e custo **precisam de prova para cada instalação**.

**Prioridade de controle:** API/scripting documentado > edição reprodutível de projetos permitidos > UI Automation > coordenadas absolutas. **Não** usar dependência de um serviço de vídeo pago. Controle real do PC só mediante grants/recibos do PCRA compatíveis com a operação; status read-only não concede shell, render ou administrador.

## 4. Modelo de dados mínimo da tomada (shot contract)
**Preservar o JSON P15 como experimento; não substituir por este texto.** Futuras evoluções deverão manter compatibilidade, validade determinística e histórico de versões.

Campos previstos:
- `project_id`, `sequence_id`, `shot_id`, `revision`, `status`, `approval_ref`, `source_canon`.
- `frame_start`, `frame_end_exclusive`, `fps`, `duration`, `resolution` e convenção de amostragem/desenhos em 1s/2s/3s.
- `characters[]`: ID e estado/forma, character sheet, referências e SHA-256, medidas/poses/emotion/visemas/roupa por versão, permissões de alteração e ângulo da câmera.
- `environment_id`, `architecture_revision`, `set_transform`, `lighting_look`, `background_layers`, `occlusion_masks` e vínculos com a geometria persistente.
- `camera`: transform/FOV/lente/foco/keyframes/eixo de ação/look-target; `blocking`, `motion_source`, `engine_selection` e razões da escolha A/B/C.
- `props[]`: ID, geometria, pivot, ancoragem em mundo/osso, mãos, contato, oclusão, sombra e persistência.
- `audio`, `dialogue/visemes`, `acting`, `VFX_events` e timing de montagem.
- `source_files`, `derived_from`, `output_artifacts`, `ffprobe`, `render_metrics`, `qa_findings`, `evidence_refs` e `human_acceptance`.

**Estados de asset:** RASCUNHO → CANDIDATO → APROVADO → ÂNCORA CANÔNICA, com DESCARTADO/SUPERADO históricos. *Approval* de imagem **não** equivale a aprovação de vídeo ou de rig; não enviar arte privada/cânone narrativo ao repositório público.

## 5. Pipeline de produção decidido, em ordem
1. **Roteiro/decupagem** e intenção dramática por shot; gerar *shot list* sem reinventar fala ou cânone.
2. **Ingestão de assets reais**, hashes, vista, arquivo de origem, licença, estado de aprovação; restaurar apenas o que realmente está disponível.
3. **Blocking e storyboard/animatic** com cenário e câmera; duração, ritmo, raccord de geografia e olhar, eixo 180°, cortes de reação, inserts.
4. **Escolha A/B/C/3D/híbrida por shot** e registro de capacidade/custo, com fallback controlado.
5. **Criação/rig/poses**: key drawings e vistas adicionais quando necessárias; FK/IK, deformação e animação de corpo/rosto/cabelo/roupas.
6. **Atuação e som**: voz natural PT-BR, visemas, mandíbula, olhar, ombros, respiração, gestos, pausas, sound design e ambiente.
7. **Luz/efeitos/magia** com causalidade (preparação → evento → pico → dissipação → reação), sombras, contato e oclusão.
8. **Composição e edição** por sequência com câmeras, lentes, continuação de movimentos e materiais. Render por cenas/camadas para retakes localizados.
9. **QA temporal/cross-shot**: faces, figurino, proporções corrigidas por câmera, cabelo, membros, dedos/contato, cenário, props, perspectiva/parallax, flicker/ghosting, lip-sync, cortes, áudio e materiais.
10. **Render/entrega**: fontes editáveis, MP4/FFprobe, logs/recibos, medição CPU/RAM/VRAM/tempo/custo, relatório timestamp/frame/severidade/correção e aprovação humana.
11. **Versionamento e rollback**: guardar tudo com IDs, hashes, auditoria, retries idempotentes e checkpoints; alterações aprovadas não desaparecem em regenerações.

**Regra de qualidade:** resolução final 4K/1080p não corrige textura facial borrada, subdetalhe, geometria inconsistente ou animação ruim. QA começa com fontes e movimento, não com upscale.

## 6. Incorporação cumulativa das referências estudadas
| Fonte/estudo | Somatória ao plano original | Não implica |
|---|---|---|
| TS Malfoy | Fotografia atmosférica, direção de câmera, microatuação e montagem | Que movimentos corporais discretos bastem para todas as cenas |
| Shift Up / Evie | Testes explícitos de contato, props, perspectiva do microfone, anatomia cross-shot e atuação | Conhecimento do motor, hardware ou orçamento dos criadores |
| Seravienne (fantasia/elfos) | Cenários monumentais, raças/montarias, blocking de luta, worldbuilding e ritmo | Trocar o estilo autoral/rig por pipeline idêntico ao vídeo |
| Wildland Hunters | Direção editorial, acting, luz, inserts/reação, VFX e continuidade de objetos | Homologação de lip-sync, IA ou ação sem auditoria |
| AI manhua longos | Pesquisa para episódios, reaproveitamento e montagem serial | Que qualidade e custo de produção estejam comprovados |
| Tutorial de agente / novas ferramentas “grátis” | Possíveis adapters/motores a comparar | Instalação, migração para Claude ou gratuidade ilimitada |

As pesquisas de 08/11 e 16/11 **refinam critérios de qualidade e gates**; não alteram a decisão multimétodo original.

## 7. Provas distintas, nenhum piloto substitui outro
1. **POC artístico inicial do estúdio — 12–20 s (proposta):** diálogos/respiração, caminhada/gesto, mudança de câmera, golpe/impacto; aceitar somente com arte real, som, fontes, QA e hardware medido.
2. **Piloto técnico P15 — 15 s, três shots (código experimental):** [Issue #12](https://github.com/Furuya29/furuya-motion-studio/issues/12), [shot spec](piloto_15s_shot_spec_v0_1.json), validador e render geométrico; demo **640×360, 24fps, 360 quadros**, sem arte real/lip-sync. Rig de sprite demo: **72 quadros, 3 s**. Provas de ambiente isolado/CI são base de engenharia, **não** arte homologada.
3. **Primeira prova com cenas reais de Aenvarath (escopo narrativo separado):** aproveitar imagens aprovadas. Começar por tomada curta e controlável (neve, fumaça, brasa, câmera/parallax na vila; ou microatuação em close). **Não** recomeçar storyboard nem exigir luta complexa como teste inicial. Voo e palácio permanecem no checkpoint mais recente; o teste da abertura não retrocede o estado narrativo.
4. **Longa duração e combate complexo:** metas posteriores, dependentes de assets multivista, rigs, geografia, lip-sync, benchmark e aprovação.

**Em novembro de 2026:** P15/rig têm **código e ensaios técnicos** na branch draft; execução de filme com personagem real, OpenToonz/Krita/Blender/Remotion no PC, visemas de voz, IK, palácio 3D final e entrega artística **não estão comprovados por estas fontes**.

## 8. Dependências de arquitetura e restrições operacionais
- **Custo recorrente alvo R$ 0**. Verificar preço, licenças e uso comercial antes de promover qualquer alternativa.
- PC de desenvolvimento informado: Windows 10 Pro, AMD FX-4300, ~16 GB RAM, Radeon RX 580 8 GB. Não supor HIP/Cycles GPU moderno para Polaris, GPUs cloud grátis permanentes, render 4K em tempo real ou licença comercial automática de plugins.
- Priorização de *proxy render* 640×360 / 540p, processamento serial, caches, arte editável e retakes por fragmento. Medir antes de dimensionar Full HD.
- **PCRA** é caminho preferencial de orquestração, com controle escopado e comprovado; Desktop Commander apenas fallback. **Não** inferir capacidade de shell/admin a partir de status read-only. Não modificar PCRA, Sentinel, Android Agent, AVPE, Unreal, browser/login ou máquinas paralelas a partir deste ADR.
- Produção narrativa/lore/frames canônicos e arquivos privados ficam sob gerenciamento **privado do projeto Aenvarath**. Aqui registrar arquitetura genérica, evidências técnicas e links publicáveis, sem expor segredos da trama ou dados de controle.
- PR #13 permanece em draft até revisão de divergência de base, diff, CI e autorização de merge. A Issue #12 permanece aberta até prova artística completa.

## 9. Critérios para considerar o ESTÚDIO integrado e posteriormente homologado
**Gate G0 — Inventário:** confirmar software, versões, Python/FFmpeg, memória, runners e permissões PCRA; não reinstalar automaticamente.
**G1 — Assets reais:** character sheet ou imagem de cena com arquivo original, hash e aprovação, camadas quando cabível.
**G2 — Movimento verificável:** teste curto com geometria e atuação desejada, export MP4 auditável.
**G3 — Qualidade temporal:** QA na sequência (não somente frame parado), identificação/contato/perspectiva/roupa/câmera/iluminação, defeitos localizados com antes/depois.
**G4 — Performance e custo:** CPU/RAM/VRAM/tempo, custo efetivo R$0, integridade de arquivos e compatibilidade Windows.
**G5 — Aceite humano:** aprovação explícita da obra, não só sucesso de script; registrar sem apagar histórico.
**G6 — Homologação de automação:** repetir do prompt ao MP4 via canal produtivo autorizado do PCRA, com recibos, rollback e não regressão de projetos adjacentes.

Em cada gate, o resultado pode ser PASSOU/REPROVOU/PENDENTE, com evidência específica. Não marcar `HOMOLOGADO` por uma imagem isolada, uma CI verde ou um render geométrico.

## 10. Próximo passo seguro integrado
1. Preservar e catalogar assets originais aprovados do projeto narrativo, com políticas de divulgação.
2. Verificar inventário/possibilidades reais do PCRA antes de prometer operação do PC.
3. Usar **uma tomada curta existente** para testar camadas, animação de ambiente, câmera e export; QA e aprovar.
4. Conservar P15 e o rig PNG como módulos experimentais, evoluindo-os por capacidades sem declará-los os únicos motores.
5. Projetar a planta/blockout do palácio **sem refazer** frames visuais aprovados e sem migrar o cânone ao repositório público.
6. Somente depois expandir para visemas/corpo/rig avançado, multiplano, combate e animação narrativa longa, na prioridade decidida no projeto principal.

**Resultado deste documento:** plano de animação inicial + pesquisas posteriores + provas técnicas têm **uma arquitetura única, cumulativa e verificável**, mas **não** representam implantação artística completa nem alteração do último checkpoint da animação.
