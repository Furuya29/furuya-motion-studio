# Reconciliação cumulativa — Projeto de Animação Automatizada (09/11/2026)

> **Status deste documento:** proposta de integração em branch de revisão; não é comprovação de implementação no PC, não aprova novas prioridades e não substitui qualquer decisão anterior. Referências primárias: [CONTEXTO_MESTRE](CONTEXTO_MESTRE.md), [handoff de 08/11](HANDOFF_INTEGRACAO_CHAT_PRINCIPAL_2026-11-08.md), [análise Bloodrain](REFERENCIA_02_SHIFTUP_BLOODRAIN_2026-11-08.md), [Issue #12](https://github.com/Furuya29/furuya-motion-studio/issues/12).

## 1. Limites de continuidade

- **Não recomeçar** o projeto nem remover processos, engines, ferramentas, modelos ou provas já aprovados; recuperar o checkpoint do projeto principal antes de qualquer execução.
- **Separação de produtos:** este projeto é para **produção de animações originais** (anime japonês 2D, 3D e híbrido; curtas, motion comics, canais e cinemáticas de Aenvarath). O Furuya Motion Studio tem também uma frente de **recasting de vídeos existentes**; compartilhar técnicas e repositório não funde escopo nem prioridade.
- **Matriz de ferramentas prévia preservada:** OpenToonz/Xsheet/Plastic, Krita, Blender/Grease Pencil/rigs, Remotion, FFmpeg, Godot, Inochi2D, CapCut e Premiere como interfaces/rotas alternativas e complementares, não como instalações já verificadas. Motor generativo gratuito é **opcional**, condicionado a licenças, disponibilidade e QA.
- **Estética:** anime japonês autoral; origem histórica do OpenToonz não implica estilo Studio Ghibli.
- **Orçamento:** meta de R$ 0 recorrente; não assumir HIP/Cycles GPU na RX 580 (Polaris), nem GPU grátis permanente. Evitar ocupar o PC enquanto o PCRA estiver indisponível, interferir nos fluxos AVPE ou alterar instalações existentes.
- **Separar estados:** ESTUDADO, PROPOSTO, IMPLEMENTADO EM CÓDIGO, TESTADO EM AMBIENTE CONTROLADO, EXECUTADO EM PC, APROVADO ARTISTICAMENTE e HOMOLOGADO. Nenhum estágio é inferido de outro.

## 2. Reconciliação item a item

| Tema do handoff | Classificação | Fundamento na base anterior | Integração sem substituir |
|---|---|---|---|
| Anime 2D/3D/híbrido; multimétodo por tomada | **Já decidido** | CONTEXTO_MESTRE e estudo anterior de rigs, keyframes, interpolação, 3D e IA | Manter catálogo de motores. Escolher método por tomada; registrar escolha e limitações. |
| 15 segundos de piloto com 3 planos | **Já planejado; não homologado** | Issue #12 e CONTEXTO_MESTRE | Criar *shot spec* inicial sem alterar fila de prioridades vigente. |
| Direção cinematográfica e cenografia TS Malfoy | **Já documentado** | CONTEXTO_MESTRE e handoff | Usar como critério de shot design, sem copiar mídia protegida. |
| Perspectiva do microfone durante rotação de câmera | **Reforço técnico / novo teste explícito** | Adendo Shift Up e handoff | Formalizar teste de coordenadas mundo/mão, projeção, oclusão e parallax. Tratar falha observada como candidata, não medida conclusiva. |
| Proporções corporais entre planos | **Reforço técnico / novo teste explícito** | Adendo Shift Up | Padronizar proporções do personagem por turnaround; comparação pós-projeção, separando perspectiva legítima de deriva. |
| Drift facial em ~00:33–00:35 | **Já documentado; hipótese visual** | Análise Shift Up | Adicionar gate cross-shot e registrar incerteza/causa alternativa. |
| Atuação corpo+rosto, visemas, respiração | **Já planejado; protocolo refinado** | CONTEXTO_MESTRE / Issue #12 | Criar teste de fonemas e visemas com pescoço, mandíbula, ombros e respiração; medir e revisar visualmente. |
| Mãos, dedos, objetos, pé no chão, sombras | **Já documentado; gate refinado** | Análise Shift Up | Introduzir IDs persistentes, sockets/ancoragens, contato e oclusão; preservar tolerância ao estilo artístico aprovado. |
| QA de flicker e cross-shot | **Já planejado; detalhamento novo** | Issue #12 | Especificar evidência por frame/timestamp, severidade, hipótese, medida aplicada e revisão humana. |
| Bastidores gerados da Shift Up; orçamento/hardware desconhecidos | **Restrição de evidência** | Estudos já existentes | Não fazer inferência causal sobre ferramentas, orçamento ou máquinas usadas. |
| Automação PCRA, GPU e custo zero | **Já decidido; integração pendente** | Planejamento geral, independente do recasting | Não alegar execução remota, instalação ou render sem recibos e logs. |

### Conflitos encontrados
Nenhum conflito técnico decisivo foi confirmado a partir dos documentos consultados. **Lacuna de rastreabilidade:** o contexto mestre declara expressamente não conter necessariamente toda a história do chat principal; portanto, este registro não se sobrepõe a checkpoints e prioridades não migrados.

## 3. Decisão de engenharia que pode avançar sem renderizar

Acrescentar uma especificação de tomadas em JSON, independente de engine, para transformar o estudo em contrato verificável:
- timeline exata (intervalos **[início, fim)**, fps, resolução);
- personagem, cenário, props e referências por IDs estáveis;
- câmera com pose e chaves temporais em coordenadas de mundo;
- tipo de ancoragem do prop (mundo ou osso) e sistema de oclusão;
- visemas/gestos/corpo registrados como critérios de teste;
- QA **por tomada e cruzado**; cada falha registrada com timestamp, frame, categoria, gravidade, evidência, origem e status de revisão;
- origem/termos de uso de assets; nunca enviar MP4 de terceiros ao GitHub.

Arquivos propostos nesta branch:
- [piloto_15s_shot_spec_v0_1.json](piloto_15s_shot_spec_v0_1.json): contrato inicial **candidato**, com 3 planos de 120 frames a 24 fps; nenhuma arte ou vídeo está gerado.
- [validador de shot spec](../../tools/animation_pilot/validate_shot_spec.py): pré-validação determinística de estrutura, referências, câmera, continuidade de timeline e gates mínimos. **Não certifica qualidade cinematográfica**.
- [testes unitários](../../tests/test_animation_pilot_spec.py): exemplos de estrutura válida e inválida.

## 4. Próximo checkpoint e critérios de verdade

1. Conciliar este adendo com o estado do chat principal e branch atual. Só alterar prioridade com decisão explícita.
2. Verificar a capacidade efetiva do PCRA para leitura/escrita/renderização; sem simular acesso ao Windows.
3. Preparar asset original: character sheet multivista, mapa de proporções, cenário e objeto com ancoragem. Até lá, JSON é apenas planejamento.
4. Repetir o piloto 15s da Issue #12 **se estiver na sequência autorizada**: A atuação facial/fala, B deslocamento e mudanças de perspectiva, C contato com microfone e câmera em movimento.
5. Registrar como comprovado apenas após: arquivos-fonte + MP4 + ffprobe + QA visual + evidência de câmera/prop/proporções + medição CPU/RAM/tempo/custo + aprovação do usuário.

## 5. Política de não regressão

- Não editar nem descartar scripts de recasting, Android Agent, PCRA, AVPE, Blender ou outras integrações existentes.
- Conservar links para [documento-mestre](CONTEXTO_MESTRE.md), [handoff](HANDOFF_INTEGRACAO_CHAT_PRINCIPAL_2026-11-08.md) e [Issue #12](https://github.com/Furuya29/furuya-motion-studio/issues/12).
- Registrar esta integração como **proposta documentada e código preliminar**, e não como piloto entregue.
