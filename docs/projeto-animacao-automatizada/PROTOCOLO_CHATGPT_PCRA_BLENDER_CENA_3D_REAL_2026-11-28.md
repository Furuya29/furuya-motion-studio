# Decisão do proprietário — ChatGPT controlando Blender real via PCRA

**Data:** 28/11/2026  
**Origem da decisão:** usuário confirmou explicitamente que deseja **ChatGPT normal dirigindo Blender diretamente** para construir cenas 3D reais e persistentes do estúdio `The Darkness of Aenvarath`, **desde que o funcionamento seja comprovado**. Esta é uma explicitação de capacidade do núcleo 3D/híbrido já aprovado, não uma arquitetura nova.

**Status:** DECISÃO REGISTRADA / EXECUÇÃO PENDENTE. Não confundir com código concluído, instalação, sessão remota ativa, Blender em execução, render ou homologação.

## 1. Objetivo operacional

Transformar ordens de direção em operações reais sobre arquivos Blender, por canal autorizado:

`ChatGPT (chat normal) → GitHub/Cloudflare/PCRA autorizado → Blender Python API (bpy) / CLI → arquivos .blend editáveis, renders e recibos → ChatGPT (QA e próxima correção)`

MCP for Blender poderá ser **adaptador opcional** sob revisão de segurança, mas **não** pré-requisito nem novo transporte obrigatório. Não requer Claude Code pago. O ChatGPT planeja ações; o PCRA executa somente quando seu acesso produtivo, concessão e recibo estiverem efetivamente comprovados. Não burlar HOLD/OwnerSeal, não executar Python arbitrário recebido de fontes não auditadas e não presumir poderes ilimitados por autorização verbal.

## 2. Comportamento esperado da automação

**Criar:** construir geometria 3D persistente, transformar objetos, importar assets autorizados, aplicar materiais, posicionar luz/câmera, editar armatures/rigs, keyframes e constraints.  
**Editar sem perder:** após salvar um `.blend`, abrir **o mesmo projeto** numa execução seguinte e mudar apenas o objeto/propriedade solicitado, com backup, checkpoint e comparação dos objetos não alvos.  
**Animar:** alterar estados de personagem, IK dos pés/mãos, root motion, roupa, cabelo, ossos das asas e relações com objetos, renderizar ação real da personagem quadro a quadro. Não confundir movimento de câmera sobre ator parado com animação completa.  
**Revisar:** renderizar preview e final, entregar fonte `.blend`, sequência/MP4, relatório de objetos alterados, hashes, parâmetros, consumo e timestamps de falhas.  
**Retomar:** recuperar projeto, versões e continuidade no próximo turno/chat, com GitHub como documentação e arquivos canônicos locais/privados sob acesso permitido.

## 3. Prova inicial vinculada ao projeto, não demo genérica

A [OS PCRA #320](https://github.com/Furuya29/desktop-tutorial/issues/320) prevê como primeiro piloto **a vila humana destruída** (Nyraelis), não a caminhada de Nólyrien nem uma floresta arbitrária de tutorial. Assim, o teste deve usar a sequência narrativa e as referências aprovadas, com arte privada armazenada somente em local autorizado.

**Gate 0 — pré-voo read-only:** confirmar PCRA realmente operacional no PC; programa Blender instalado/versão/caminho, driver RX580, Eevee disponível, Python e FFmpeg/ffprobe, assets aprovados, capacidade de backups, paths e permisos. Sem rebaixar medidas de segurança do PCRA.

**Gate 1 — geometria editável:** em cópia de trabalho versionada, construir ou atualizar **vila 3D com volumes, fachadas, estrada e cena espacial** correspondentes ao storyboard aprovado; salvar `vila_piloto.blend`. Deve ser possível abrir, selecionar e editar cada casa/prop, suas medidas e materiais.

**Gate 2 — edição cirúrgica sob instrução:** numa segunda ordem real, modificar **somente** a câmera (ex.: redução de velocidade e trajetória) no mesmo arquivo. Comparar ids/nomes, malhas, transforms e materiais dos objetos não alvos antes/depois; invariante esperada: **nenhum objeto/prop/personagem/ambiente não autorizado se altera**. O arquivo binário `.blend` pode mudar por regravação; comparar dados semânticos, não exigir SHA binário inalterado.

**Gate 3 — movimento verdadeiro:** renderizar **2–5 s a 24 fps** de personagem reconhecível na sequência real, com movimento de corpo/ossos/keyframes e contato espacial, não apenas sprites/motion comic/câmera sobre still. Preferir Nyraelis entrando na vila ou ação curta já contida nas tomadas canônicas, conforme assets efetivamente aprovados. Testar mãos/pés/sombras e mudanças de ângulo. Não inventar redesign canônico.

**Gate 4 — efeitos e composição:** neve integrada ao espaço, fogo com emissividade/luz, fumaça e brasas em movimento, câmera e profundidade corretas, sem sobreposições artificiais que já foram rejeitadas em provas antigas.

**Gate 5 — QA e entrega:** verificar preview e `.blend` reaberto; capturar ffprobe, frames/timestamps, lista de objetos e alterações, logs de duração/CPU/RAM/VRAM, receita de render, hashes, aprovação artística explícita e falhas pendentes. Só então declarar Blender **OPERACIONAL PARA ESSA CAPACIDADE**; controle de câmera não homologa automaticamente rig/animação/magia/voo.

## 4. Decisões de implementação e prioridades

1. **Reutilizar** o núcleo `3D & Hybrid Engine`, o `Asset & Character Consistency`, `Cinematic Composition` e o `Traditional 2D Animation Engine`; Blender pode renderizar geometria, base de anime cel-shaded, Grease Pencil, blocking e animação híbrida sem substituir arte tradicional.
2. **Rota inicial preferida:** scripts `bpy` e Blender em background/CLI com operações tipadas e idempotentes; registrar alterações e hashes. Avaliar MCP for Blender apenas depois de revisar código, versão, privilégios, exposição e proteção dos arquivos.
3. **Custo obrigatório R$0:** Blender/Python/FFmpeg/recursos licenciados corretamente. Claude Code e Hyper3D pagos não são dependências. Poly Haven é CC0; conferir licenças de todo conteúdo extra.
4. **PCRA:** respeitar a OS #320 como secundária pós-PowerShell produtivo/Aenvarath prioritário. A confirmação artística **não é ordem de furar a fila nem autorização para instalar imediatamente**; execução depende da condição registrada na issue ou liberação expressa posterior.
5. **Preservar** scripts/engines de Aenvarath, backlog, modelos canônicos, checkpoints, bancos, sessões, segurança e rollback. Não fazer merge automático do PR #13.
6. **Não afirmar** que nosso ChatGPT já controlou Blender só por existir esta documentação ou por scripts locais preparados.

## 5. Critério de sucesso da promessa ao usuário

O teste só será considerado verdadeiro quando uma **ordem recebida nesta conversa** resultar, comprovadamente, no Windows autorizado, numa **alteração específica em uma cena `.blend` real**, com recibo do PCRA, projeto editável reaberto, movimento real renderizado, inspeção e continuidade de assets demonstradas. Até lá, usar o status **planejado/documentado**, nunca `funcionando`.

**Documentos relacionados:** [Referência 18 — tutorial Claude/Blender](REFERENCIA_18_CLAUDE_BLENDER_MCP_CENARIOS_PERSISTENTES_2026-11-28.md), [arquitetura consolidada](ARQUITETURA_CONSOLIDADA_MEGA_ESTUDIO_ANIMACAO_2026-11-16.md), [CONTEXTO_MESTRE](CONTEXTO_MESTRE.md), [PCRA OS #320](https://github.com/Furuya29/desktop-tutorial/issues/320), [piloto Furuya Motion Studio #12](https://github.com/Furuya29/furuya-motion-studio/issues/12).
