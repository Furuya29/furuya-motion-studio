# Checkpoint cumulativo — Projeto de Animação Automatizada (16/11/2026)

> **Natureza:** adendo de continuidade e pesquisa, não aprovação de arquitetura, não homologação cinematográfica, não alteração de prioridades nem substituição de qualquer planejamento anterior. Registrado na branch de revisão do [PR #13](https://github.com/Furuya29/furuya-motion-studio/pull/13); sujeito aos gates de não regressão do PR. Não mesclar automaticamente.

## 1. Fontes canônicas e separação dos projetos

- [Contexto mestre](CONTEXTO_MESTRE.md) e [handoff 08/11](HANDOFF_INTEGRACAO_CHAT_PRINCIPAL_2026-11-08.md): documentação de **pesquisa** já publicada na main.
- [Reconciliação aditiva 09/11](RECONCILIACAO_ADITIVA_2026-11-09.md), [P15 animatic](PROTOTIPO_P15_EXECUTAVEL_2026-11-09.md) e [rig 2D](MODULO_RIG_2D_SPRITES_2026-11-09.md): implementações experimentais **somente na branch do PR #13**, ainda não mescladas à main em 16/11.
- [Issue #12](https://github.com/Furuya29/furuya-motion-studio/issues/12): piloto cinematográfico de 15 s **aberto, não homologado**.
- Produção de **animações autorais** (Nólyrien/Aenvarath, 2D anime, 3D e híbrido) não equivale ao *recast* de vídeos virais do Furuya Motion Studio; compartilham ferramentas e repositório, mas não estado de aceite nem prioridades.
- Há também continuidade narrativa e referências de quadros em conversas e documentos associados a **The Darkness of Aenvarath**. A documentação de pesquisa aqui **não substitui** automaticamente o arquivo canônico de arte, o storyboard ou checkpoints aprovados naquele projeto.
- Orçamento alvo **R$ 0**; não contratar serviços, não exigir GPU paga, não presumir RX 580 compatível com Cycles GPU/HIP moderno; preservar o PCRA e demais sistemas sem mudanças.

## 2. Últimos checkpoints efetivos que não podem ser confundidos

| Frente | Estado com evidência | Pendência / proibição de inferência |
|---|---|---|
| Pesquisa TS Malfoy / Shift Up | Análises e handoff 08/11 versionados na main | Não inventar pipeline/custo dos criadores; defeitos suspeitos exigem validação temporal |
| P15 | Na branch do PR #13 há contrato de 360 frames/15 s/24 fps, validador e renderizador geométrico determinístico; MP4 de teste e FFprobe em ambiente separado | Não foi executado via PCRA/Windows do proprietário; não tem anime final, lip-sync real, contato/IK ou aprovação artística |
| Rig 2D | Código de camadas PNG, FK, keyframes e troca de desenhos, com exemplo 72 frames/3 s em ambiente de desenvolvimento | Não produz por si só personagens, vistas, malhas, IK nem animação cinematográfica final |
| Cena narrativa Nólyrien | Trabalho visual vinha avançando em torno do frame 20 (surgimento das asas) e frame 21 (início de voo), segundo continuidade anterior | A última orientação do proprietário solicitou **correção de simetria/continuidade anatômica**; não considerar a arte pós-correção aprovada ou o voo finalizado sem novo aceite |
| Operação PC | Desktop Commander sem cota de chamadas na sessão atual; conectores MCP sintéticos do PCRA não executam comandos reais | Não alegar instalação, render, operação automática ou homologação pelo PCRA sem recibos produtivos |

## 3. Nólyrien — regras vinculantes para próxima correção visual

Aplicar como **QA de continuidade local**, sem redesenhar personagem, mudar a anatomia previamente aprovada ou refazer quadros já aprovados:

1. **Asas** com plumas negras saindo **da região lombar**, com ponto de ancoragem e transição anatômica coerentes.
2. Na vista de costas, mostrar as **faces externas/dorsais** das asas, não trocar por suas superfícies internas.
3. **Coroa** vista por trás na vista traseira; não projetar indevidamente a face frontal da coroa para o observador.
4. **Silhueta contínua:** alinhar torso, cintura, quadris e membros acima/abaixo da implantação das asas; impedir desalinhamento central e mudanças artificiais de largura.
5. Preservar rosto, cabelo, figurino, cores e proporções canônicas previamente aprovados. Corrigir somente regiões com defeito; não substituir o modelo.
6. Para qualquer imagem/revisão: guardar identificação do frame, referências, defeito descrito, tipo de correção e aprovação expressa do proprietário.

Estas instruções correspondem ao ponto de continuidade reportado, **não são evidência de que a correção já foi executada**.

## 4. Novas referências recebidas em 16/11 — status: pesquisa pendente, não técnicas comprovadas

| Referência | Fonte e observação confirmável | Próxima verificação |
|---|---|---|
| AI manhua, apocalipse gelado | https://youtu.be/AZDzT-4OIY8 — página identifica narrativa de preparo para catástrofe e categoria de drama/manhua feito com IA. | Amostrar tomadas espaçadas, detectar consistência de rosto, cena, câmera, movimento e objetos. Não atribuir motor sem fonte. |
| AI manhua, imperatriz/sistema emocional | https://youtu.be/elGjvl8lJgA — vídeo com título japonês de reencarnação/cultivo, do canal 长風追劇_ShortTV. | Repetir diagnóstico temporal e comparar linguagem visual com referência anterior, sem inferir técnica pela aparência. |
| Tutorial de produção com agente | https://youtu.be/N6uTE2p3lgg — título: “Você vai criar Vídeos Cinematográfico Com O Claude Code Passo A Passo”. | Examinar conteúdo e transcrição antes de afirmar ferramentas, fluxo, preço ou resultado real. Estudar **orquestração por agentes** como possibilidade, não migração obrigatória de ChatGPT/PCRA para Claude. |

- Não há inspeção quadro a quadro concluída dessas três referências, nem transcrição validada do tutorial. Apenas página/metadata foram consultados.
- Como alguns vídeos são longos, preparar **amostragem de trechos curtos**, quadros e tiras temporais com yt-dlp/FFmpeg **quando executável e permitido**, em vez de baixar vídeos completos ou publicar suas mídias no GitHub. Respeitar direitos e termos de uso; registrar apenas observações técnicas, IDs, links e materiais próprios.
- Não adicionar serviços pagos, GPU inexistente ou fluxo exclusivo. O exame pode resultar em nenhuma mudança se as técnicas já estiverem contempladas.

## 5. Matriz de classificação incremental

| Proposta / achado | Classificação | Encaminhamento |
|---|---|---|
| Multimétodo 2D/3D, rigs, keyframes, deformação, IA seletiva, FFmpeg | **Já decidido** | Preservar catálogo; não reduzir a um motor |
| Identidade, câmera e parallax, geometria de microfone, QA facial/corpo | **Complementos já documentados** | Reusar contrato P15 e gates da Issue #12; evitar tickets duplicados |
| Render geométrico P15 e sprites FK | **Código experimental existente no PR #13** | Review de CI e compatibilidade; não confundir com render artístico |
| QA de asas lombares vistas dorsalmente e coroa traseira da Nólyrien | **Requisito específico da cena vigente** | Corrigir e obter aprovação visual antes de avançar o voo |
| AI manhua de episódios extensos | **Nova referência, não validada** | Amostragem, relatório temporal e comparativo |
| Tutorial Claude Code/agentes | **Alternativa de orquestração a avaliar** | Comparar capacidades com PCRA+FFmpeg e sistemas existentes; não migrar automaticamente |
| Piloto P15 vs sequência Nólyrien abrindo asas | **Escopos diferentes; sem conflito necessário** | O P15 é gate experimental genérico; frames de Nólyrien são produção narrativa em andamento; **não reordenar** por esta pesquisa |

## 6. Próxima ação segura, sem reinicialização

1. **Na produção narrativa:** continuar do último frame pendente, com correção localizada de Nólyrien; validar antes de produzir os próximos quadros do voo.
2. **No código de animação:** manter PR #13 em draft e Issue #12 aberta; validar CI vigente, revisar testes de P15/rig e preparar integração não regressiva, sem promover automaticamente.
3. **Na pesquisa:** obter trechos de referência e produzir relatório por timestamps, observações vs hipóteses, defeitos e soluções; incluir evidências no repositório só quando lícitas e próprias.
4. **Para homologar P15:** exigir arte original + fontes, MP4, FFprobe, QA cross-shot/temporal, registro CPU/RAM/tempo/custo e aprovação humana. Um resultado técnico geométrico não satisfaz essa condição.
5. **Para operação via PCRA:** usar somente endpoint produtivo realmente homologado e registrar recibos; conectores sintéticos são insuficientes.

**Regra permanente:** SOMAR; preservar arte, cenários, ferramentas e decisões existentes; versionar checkpoints; nunca declarar concluído algo apenas proposto ou gerado em ambiente de ensaio.
