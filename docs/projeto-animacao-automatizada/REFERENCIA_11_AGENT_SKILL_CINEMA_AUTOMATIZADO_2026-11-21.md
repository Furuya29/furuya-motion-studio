# Referência 11 — Agent Skill para criar vídeos cinematográficos automaticamente

**Data da pesquisa:** 21/11/2026  
**Fonte enviada:** https://youtu.be/9a2KZBGzEyg?is=2KiK4PHG2ZdOXoI3  
**Título público verificado:** “Essa Skill Faz Vídeos de CINEMA Sozinha (Grátis no Claude Code, Codex e Antigravity)”  
**Canal:** Web Dark  
**Data anunciada na página YouTube:** 20/11/2026  
**Duração exibida na página:** 14min57s  
**Estado:** RESEARCH_ONLY / metadados da página verificados; arquivo exato da skill, licença, repositório original e transcrição integral **não identificados**.

> Preservar toda a arquitetura técnica multimétodo de Aenvarath, o planejamento de produção original, os assets e a fila PCRA. Esta referência representa possibilidade de **orquestração e direção cinematográfica por Agent Skills**, não mudança do motor de animação, validação de filme completo nem autorização para instalar software de terceiros.

## 1. Evidências realmente recuperadas

Consulta à página original do YouTube confirmou canal Web Dark, título, data e duração. A página informa conteúdo com dublagem automática, mas não disponibilizou ao extrator uma transcrição completa utilizável nem o repositório específico da skill. Não foram inspecionados os quadros do filme demonstrativo, scripts, exemplos renderizados, permissões, utilização de modelos ou custos de geração.

Uma busca pública retorna **vários repositórios diferentes** que oferecem skills cinematográficas para agentes (por exemplo, bibliotecas de Remotion, edição por código e roteirização com direção). **Não é possível atribuir um desses projetos ao vídeo sem referência explícita do criador.** Não incluir nenhum desses repositórios na lista de dependências do estúdio nem executar scripts desconhecidos como se fossem a skill do vídeo.

## 2. O que uma Agent Skill é — contexto técnico independente do vídeo

A convenção Agent Skills permite organizar em arquivo de instruções `SKILL.md` e recursos auxiliares uma tarefa reaproveitável por agentes que implementam o formato. Agentes diferentes podem interpretar o mesmo núcleo de instruções, mas dependem de suas próprias ferramentas, permissões, executores, modelos e limites; a existência da skill **não gera automaticamente frames, áudio, vídeo ou acesso ao sistema operacional**.

Referências externas sobre o padrão:
- Microsoft VS Code — https://code.visualstudio.com/docs/agent-customization/agent-skills
- Documentação de renderização programática Remotion — https://www.remotion.dev/docs/render

Remotion permite render programático com sua CLI, porém a documentação não comprova que **o autor desse vídeo** use Remotion. Também não comprova criação de animação corporal genuína de personagens sem modelos/rigs.

**“Grátis”** pode significar somente o download do arquivo com a skill. O custo de chamadas de IA, modelos de vídeo, computação GPU, assinatura/conta e exportação permanece sujeito à execução concreta e aos termos de cada fornecedor. Não presumir Claude Code, Codex ou Google Antigravity grátis/ilimitados para todos os usuários.

## 3. Relação com a arquitetura vigente

Consultar antes de implementar:
- [Arquitetura consolidada de animação multimétodo](ARQUITETURA_CONSOLIDADA_MEGA_ESTUDIO_ANIMACAO_2026-11-16.md)
- [Contexto mestre](CONTEXTO_MESTRE.md)
- [Handoff integral de referências](HANDOFF_INTEGRAL_CHAT_REFERENCIAS_2026-11-16.md)
- [P15 animatic](PROTOTIPO_P15_EXECUTAVEL_2026-11-09.md)
- [Rig experimental](MODULO_RIG_2D_SPRITES_2026-11-09.md)
- [Issue #12](https://github.com/Furuya29/furuya-motion-studio/issues/12) e [PR #13](https://github.com/Furuya29/furuya-motion-studio/pull/13)

**Classificação:** alternativa de empacotamento da **orquestração**, não novo núcleo de animação e não aprovação de migração para Claude. Compatível com o princípio existente ChatGPT planeja → PCRA produtivo/permitido executa → ferramentas de animação e composição → QA → revisão/aceite humano.

## 4. Ideia de integração aditiva: uma skill própria de direção cinematográfica

**PROPOSTA; NÃO IMPLEMENTADA:** desenhar um pacote interno independente de fornecedor, como `animation-cinematic-director/SKILL.md`, exclusivamente como *interface de trabalho* do pipeline já aprovado, reaproveitando cada módulo existente, com rotinas:

1. Receber roteiro e referências **autorais/canônicas**.
2. Converter em `shot spec`: duração, fps, personagens, cenário, câmera/lente, acting, props, VFX, áudio, continuidade e gate de QA.
3. Escolher método por tomada **A (limitada), B (corporal completa), C (ação/voo/combate)** e especificar por que a escolha cobre as necessidades de movimento.
4. Verificar estado técnico e licenças de Blender, Krita, OpenToonz, Python, FFmpeg, Remotion e demais engines antes de selecionar um executor.
5. Executar somente por canal produtivo **PCRA homologado e autorizado** ou em ambiente local de teste separadamente rotulado; registrar recibos reais, input/output, hashes, custos e consumo de CPU/RAM/VRAM.
6. Gerar e validar **quadros realmente animados**, com rigs/key poses/desenhos intermediários/3D conforme necessário. Nunca declarar motion comic, câmera sobre still ou partículas artificiais como prova de atuação.
7. Compor, editar, aplicar som/VFX e verificar continuidade de identidade, mãos/contato, asas, perspectiva, arquitetura, iluminação e lip-sync.
8. Inspecionar MP4 final, guardar relatório QA/timestamps, propor reparo localizado, solicitar aprovação artística e só depois promover checkpoint.

**O que NÃO deve fazer:** instalar silenciosamente dependências desconhecidas, usar serviços pagos sem autorização, descartar o estilo anime 2D, reabrir quadros canônicos aprovados, substituir o controle de scripts/objetos do estúdio, tentar gerar cenas pela mesma imagem frontal deformada até as costas ou contornar os controles reais do PCRA.

## 5. Próximo gate e critério de adoção

- Recuperar o **link exato** para a skill apresentada, seu conteúdo `SKILL.md`, dependências, código auxiliar, licença e funções; revisar os arquivos antes de execução.
- Comparar o pipeline do autor com o sistema existente: identificação de novos recursos versus duplicidade, e relato de onde ele obtém frames, voz, efeitos e render.
- Testar com **assets originais do projeto** e exigência de movimento corporal real em tomada de 2–5 s, usando o protótipo P15 apenas como base de testes, sem chamar P15 de filme final.
- Medir custo R$0, disponibilidade offline, licenças, automação efetiva via PCRA, qualidade e fricção operacional.
- Se o pacote apenas automatizar slide, motion comic, colagem de fotos ou vinheta, classificá-lo como **não apto a produzir as cenas principais de Aenvarath**, mesmo que a montagem seja visualmente atrativa.

**Conclusão:** boa ideia de organização/automação, porém **nem a skill específica nem a alegação de geração cinematográfica grátis e autônoma foram homologadas**. Registrar esta referência sem alterar prioridades.