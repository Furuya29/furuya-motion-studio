# HANDOFF OFICIAL — Projeto de Animação Automatizada (integração aditiva)
**Data:** 08/11/2026  
**Origem:** chat de referências e pesquisa técnica do Projeto de Animação Automatizada  
**Destino:** chat principal / planejamento-mestre do projeto de animação  
**Natureza:** complementação de requisitos, benchmarks e decisões; **NÃO é redefinição nem substituição da arquitetura anterior**.

## 0. ORDEM DE CONTINUIDADE — NÃO APAGAR NEM SUBSTITUIR O PLANEJAMENTO EXISTENTE

O GPT responsável pelo chat principal deverá **preservar integralmente** as decisões, especificações, pesquisas, planos, experimentos, funcionalidades, módulos, prioridades, arquivos, tarefas e compromissos já aprovados naquele chat. Este handoff é uma **SOMATÓRIA**: comparar item a item com o planejamento vigente, identificar equivalências, unir novos requisitos e registrar conflitos ou dúvidas antes de alterar elementos estruturais.

Regras:
1. **Não recomeçar** o projeto, não descartar trabalho concluído, não rebatizar ou migrar artefatos automaticamente, não remover motores/métodos escolhidos anteriormente.
2. Não interpretar a preferência por rig/3D controlável como proibição de animação 2D japonesa, geração por IA, desenho quadro a quadro ou outros fluxos já estudados. O sistema deverá ser **multimétodo**, selecionando o melhor motor por cena.
3. Não confundir o projeto de **produção original de animação cinematográfica** com o projeto de **recast/motion transfer de vídeos virais**, embora os dois possam reutilizar técnicas e infraestruturas.
4. Resolver eventuais conflitos por avaliação técnica e aprovação do usuário; nenhuma decisão antiga é anulada simplesmente por constar uma alternativa neste documento.
5. Manter documentação cumulativa/versionada no GitHub e referenciar as decisões originais do chat principal, sem afirmar que elas já estão todas transcritas no GitHub.
6. Só classificar recursos como **implementados, testados ou homologados** quando houver evidências reais; estudos e recomendações continuam marcados como propostas.

## 1. Documentação persistente atual — origem verificável

**Repositório atualmente utilizado:** `Furuya29/furuya-motion-studio` — **PÚBLICO** (esta visibilidade foi verificada na conta conectada).  
**Pasta documental dedicada ao Projeto de Animação Automatizada:** `docs/projeto-animacao-automatizada/` na branch `main`.

Arquivos:
- [CONTEXTO_MESTRE.md](https://github.com/Furuya29/furuya-motion-studio/blob/main/docs/projeto-animacao-automatizada/CONTEXTO_MESTRE.md) — objetivos, restrições, arquitetura sugerida, decisões desta conversa e controle de continuidade.
- [REFERENCIA_02_SHIFTUP_BLOODRAIN_2026-11-08.md](https://github.com/Furuya29/furuya-motion-studio/blob/main/docs/projeto-animacao-automatizada/REFERENCIA_02_SHIFTUP_BLOODRAIN_2026-11-08.md) — análise técnica da Shift Up com log por timestamp e adendo de defeitos no microfone/proporções.
- **Este handoff:** `HANDOFF_INTEGRACAO_CHAT_PRINCIPAL_2026-11-08.md`.
- [Issue #12](https://github.com/Furuya29/furuya-motion-studio/issues/12) — piloto técnico de 15 segundos, ainda **não concluído**.

**Importante:** este diretório preserva as descobertas feitas nesta frente de pesquisa. Ele **não deve ser apresentado como espelho integral de todas as decisões já tomadas no chat principal**, enquanto o chat principal não for reconciliado e indexado ali. O repositório é público: não enviar dados privados, chaves, roteiros confidenciais nem cópias integrais dos vídeos de terceiros sem direitos.

## 2. Objetivos do projeto que devem permanecer

- Animação cinematográfica com estética **anime 2D japonês** autêntica, 3D realista/semi-realista ou híbrida, conforme a obra/cena; evitar estética 2D ocidentalizada quando a direção for anime.
- Personagens belos e únicos, atuação emotiva e natural, desenho coerente e repetível, cenários ricos e consistentes, movimentos, mudança de câmera/ângulo/plano e montagem convincente.
- Buscar acabamento superior ao das referências; tratar a “cara de IA” como problema de engenharia visual e direção, não só de nitidez.
- Eliminar dependência exclusiva de desenho manual quadro a quadro. Investigar/combinar geração de **keyframes**, interpolação orientada, deformação 2D por rig/mesh, recortes/partes, 3D como base de espaço/movimento, captura de movimento, rastreamento, retargeting, ferramentas de animação tradicionais e modelos generativos.
- Manter possibilidade de desenho quadro a quadro, assistido por IA e revisado, onde for a melhor opção: tomadas complexas, expressões únicas, perspectivas extremas e cenas-chave.
- Priorizar **R$ 0 de custo recorrente**, ferramentas gratuitas e automação máxima, com checkpoints de aprovação artística humana. Não assumir disponibilidade de GPU de datacenter nem soluções pagas.

## 3. Referência cinematográfica 01 — Fantasoner / “TS Malfoy”

**Vídeo:** https://www.youtube.com/watch?v=WYRDe8XsRmI  
**MP4 examinado:** `1000589408.mp4`. Aproximadamente **09:04,27**, **1920×1080**, **30 fps**, **16.328 quadros**.

**Forças observadas:** fotografia, cenários góticos detalhados, atmosfera, iluminação dramática, expressões, enquadramentos variados e ritmo de montagem. A direção sustenta um curta longo sem depender de ação extrema ininterrupta.

**Problemas/oportunidades:** repetição de planos com poses sustentadas; pequenas animações de boca, olho e cabelo às vezes substituem atuação corporal integrada; ações com contato e geometria podem ser mais difíceis; expressões devem mobilizar também ombros, respiração, pescoço e mãos. Métricas simples de diferença de pixel não provam quadro congelado ou inconsistência de IA.

**Aproveitar:** fotografia cinematográfica, qualidade de ambientes, planejamento por tomadas, montagem dramática, acting facial e ambientação.

## 4. Referência cinematográfica 02 — Shift Up / Stellar Blade: BLOODRAIN / Evie

**Vídeo enviado:** `1000589429.mp4`; apresentação “Wanna be in LOVE”; **03:37,66**, **1920×1080**, **24 fps**, **5.222 quadros**.

**Contexto verificável:** a personagem foi criada por artistas/modeladores; IA foi empregada na apresentação. Não há comprovação pública do orçamento exato, supercomputadores ou pipeline exato; o “making of” no final é encenado/gerado e não documenta set físico.

**Pontos excelentes que devem ser integrados:**
- Worldbuilding futurista: cidade densa, tubulações, passarelas, metrô, cenas úmidas, jardins e objetos industriais.
- Direção de arte: paleta cromática reconhecível, silhueta/figurino marcante, contraste de luz artificial e atmosfera, iluminação volumétrica, profundidade.
- Câmera: alternância de grande plano, plano médio, close, ângulos inclinados, perfil e giro, paisagens de estabelecimento, ritmo musical.
- Props e detalhes estéticos: microfone retrô, acessórios, guarda-chuva, luzes, fundos e tipografia; som e montagem participam da narrativa.
- Apresentação de personagem predesenhada + geração audiovisual, em lugar de reinventar identidade visual em cada tomada.

**Falhas já identificadas, sem tratar a lista como exaustiva:**
- **Posicionamento/perspectiva do microfone em relação à câmera**, especialmente durante rotações: eixo, orientação, escala projetada, alinhamento com boca, profundidade/oclusão e parallax por vezes destoam.
- **Diferenças nas proporções corporais** de Evie conforme o plano ou perspectiva: cabeça/corpo, ombros, cintura, quadril, comprimento de membros e silhueta merecem verificação cross-shot.
- **Deriva de identidade facial** em determinados cortes/movimentos (ex.: por volta de 00:33–00:35); separar de mudanças legítimas de pose, lente e luz.
- **Atuação corporal limitada em trechos do canto**: movimento de boca não é suficiente para atuação convincente; validar fonemas/visemas e interação com pescoço, mandíbula, tórax e respiração.
- **Mãos, dedos e contato com objetos** (celular/selfie, hashi/comida, guarda-chuva, pingente, microfone, interação nos bastidores sintéticos) são áreas de risco de topologia/oclusão/física.
- **Pés/contato com o chão, escala, roupas/cabelo e continuidade espacial** merecem análise mais fina: não afirmar falha conclusiva quando apenas houver suspeita.
- A encenação cinematográfica pode mascarar erros com cortes curtos; qualidade de um frame não comprova continuidade temporal.

**Rigor da avaliação:** análise baseada em amostras e tiras temporais, não inspeção humana individual de todos os 5.222 frames. Classificar cada suspeita como “observada”, “candidata a falha” ou “não confirmada”. O usuário poderá encontrar outros defeitos e deverá ser possível adicioná-los.

## 5. Correções técnicas para incorporar (compatíveis com arquitetura híbrida)

### 5.1 Estabilidade de personagem e proporções
- Bíblia de personagem com vistas **frontal, perfil, 3/4, costas**, expressões, turnaround, cores e proporções relativas.
- Uma referência anatômica/rig padrão com medidas normalizadas (altura-cabeça, ombro-quadril, braço/antebraço, coxa/perna, mãos e pés); variações somente se aprovadas como estilo.
- Compare silhouette/keypoints entre quadros **após correção de câmera, pose, perspectiva e lente**, não somente pixels crus.
- Para anime 2D, rig/mesh pode ser base, mas desenhos substitutos por ângulo corrigem deformações em poses extremas.

### 5.2 Microfone, acessórios e câmera
- Microfone com **geometria persistente** e identificador único, eixo/pivô, pedestal ou ponto de fixação, materiais, sombras, profundidade e oclusão.
- Se estiver parado, ancorá-lo no sistema de coordenadas do **mundo**; se for segurado, vincular ao rig da mão com IK/constraint e contato correto.
- Câmera com posição/rotação, distância focal/FOV, near/far, possível distorção de lente e trajetória explícitas; testar **parallax** em rotações e tracking de microfone/personagem/fundo.
- Render em passes para personagem/props/ambiente, usando máscaras, sombras de contato e composição para corrigir pequenas distorções sem regenerar toda a tomada.
- Teste de movimento de câmera orbitando personagem e microfone, mantendo geometria e proporções aparentes coerentes com projeção.

### 5.3 Corpo, física e acting
- Rig 2D/3D, IK, FK, constraints, animação de raízes, contato do pé, colisões básicas, peso, balanço e antecipação/seguimento.
- Expressões correlacionadas com olhos, mandíbula, pescoço, ombros e respiração.
- Fonemas e visemas sincronizados com áudio (Rhubarb Lip Sync é candidato para 2D e requer validação em pt-BR); naturalidade avaliada auditivamente e visualmente.

### 5.4 Cena, direção e composição
- Cenários 3D otimizados ou multiplano com regras estáveis de perspectiva, lighting bible, mapas de materiais, layout de objetos e occlusão.
- Shot-list/animatic, direção de câmera, ritmo de montagem, transições de planos, áudio, partículas e efeitos; evitar depender de IA para reinventar cenários em cada frame.
- **Shot spec** versionado: shot_id, duração, cast, referência de personagem, rig/asset, cenário, lente/câmera, blocking, keyframes, ação, emoções, som, fonte de movimento, motor, saídas e status de QA.

### 5.5 QA e produção
- Pipeline por tomada: storyboard → asset/rig/ambiente → animatic/blocking → movimento controlado → estilização/geração por IA (quando apropriada) → composição → QA temporal/cross-shot → edição/FFmpeg.
- Triagens automáticas: landmarks/face consistency (com perspectiva), proporções normalizadas, mudança inesperada de roupa/props, contagem e contato de dedos, foot sliding, drift do microfone, flicker, ghosting, sombras e quebra de geometria.
- Inspeção humana obrigatória em falhas críticas; cada incidente com **timestamp, frame, categoria, evidência, severidade e correção/teste**.
- Falhas podem ser reparadas em partes (prop separado, retake de 1–3 s, troca de keyframe, máscara, ajuste de rig), não é obrigatório regenerar vídeo inteiro.

## 6. Recursos R$ 0 para avaliar, NÃO pré-homologados

- Blender + rigs/câmera/IK/EEVEE em versão compatível; OpenToonz Plastic ou rig 2D; FFmpeg para montagem; Rhubarb Lip Sync para visemas 2D.
- Alternativas de geração por IA e motores gratuitos estudados anteriormente no projeto **devem ser mantidos no catálogo**, sujeitos à prova real de acesso/licença/limites.
- Hardware conhecido: Windows 10 Pro, AMD FX-4300, ~16 GB RAM, Radeon RX 580 8 GB; Android Redmi K70 Ultra. **RX 580 (Polaris) não é elegível a HIP Cycles GPU moderno**; planejar viewport/EEVEE compatível, render CPU otimizado e proxies, sem pressupor GPU gratuita ilimitada.
- Não mudar arquitetura principal, hospedagem, PCRA ou outros projetos sem necessidade e aprovação específica.

## 7. Próxima prova sugerida — piloto incremental de 15 segundos

É proposta complementar, **não cancela nem reordena automaticamente entregas anteriormente acordadas** no chat principal.

- Plano A: personagem original cantando/falando, rosto consistente, boca+expressão+respiração.
- Plano B: corpo inteiro com movimento de câmera, controle de proporções, pés e perspectiva.
- Plano C: personagem e microfone/objeto, câmera orbitando ou mudança forte de ângulo, contato/oclusão e escala corretos.
- Aplicar estética anime 2D japonesa ou 3D conforme direção aprovada **no projeto principal**.
- Gate de aprovação: sem alteração estrutural de rosto/corpo, sem microfone fora do plano perspectivo, sem mão deformada, sem foot sliding crítico, sem cenário/figurino espontaneamente alterado, áudio/ação naturais.
- Entregar vídeo, projeto-fonte reaproveitável, relatório de falhas e medições de custo, tempo, memória e versão dos motores.
- **Status:** apenas especificado e registrado na [Issue #12](https://github.com/Furuya29/furuya-motion-studio/issues/12); NÃO executado/homologado.

## 8. Ação solicitada ao chat principal

1. Ler o planejamento existente e os três documentos desta pasta, **antes de alterar a arquitetura**.
2. Criar uma matriz: **(a)** já decidido anteriormente; **(b)** novidade deste handoff; **(c)** duplicado/complementar; **(d)** conflito real; **(e)** testes pendentes. A matriz não deve apagar nenhuma decisão aprovada.
3. Incorporar de forma aditiva os novos requisitos no backlog e no sistema de QA, respeitando prioridades e recursos já estabelecidos.
4. Confirmar a localização **canônica** da documentação do projeto principal; se este repositório público for apenas uma das frentes, manter links cruzados para evitar duas verdades divergentes. Não migrar automaticamente projetos/arquivos.
5. Continuar do **último checkpoint efetivo** do desenvolvimento original, sem reiniciar, e registrar no GitHub o que foi incorporado e o que continua pendente.
6. Preservar a separação entre **achados comprovados em arquivos**, **relatos visuais do usuário**, **informações de fontes públicas**, **hipóteses técnicas** e **implementações testadas**.

**Ordem final:** INTEGRAR, SOMAR, PRESERVAR e DAR CONTINUIDADE. NÃO SUBSTITUIR, NÃO RECOMEÇAR, NÃO APAGAR O HISTÓRICO DO PROJETO PRINCIPAL.
