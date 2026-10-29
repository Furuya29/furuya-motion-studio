# Furuya Motion Studio — Motores e rota multimotor (29/10/2026)

## Compromisso da arquitetura

Produto Furuya = interface e controle de jobs, captura da referência, controle de alvo, validação, seleção de modelo, preparação, pós-produção, histórico e download. Motor de terceiros = plugin intercambiável, nunca produto obrigatório.

**Meta imediata:** vídeo de 3 s / 576×1024 / 24 FPS (72 quadros) da festa do Rio, Albedo adulta e idêntica ao PNG canônico, substituindo **somente o dançarino central**, com pessoas adjacentes, luzes e ambiente mantidos. Segundo modo: personagens de anime e cinema executando movimentos de vídeos virais, mesmo que se refaça o cenário.

## Matriz técnica verificada

| Motor | Tarefa realmente adequada | Integração nesta versão | Fatores limitantes |
|---|---|---|---|
| Wan2.2-Animate-14B, modo replacement | **Substituição localizada na cena**, com pose + face + fundo + máscara + relighting | CLI oficial de 2 etapas, preparado; sem inferência | Modelo 14B e preprocessamento pesados, GPU livre não confirmada; máscara manual Furuya NÃO equivale a tensor preparado |
| Viggle-Animate aberto (MiniMax-H3) | Propagar um quadro da mesma cena integralmente retocado | Adaptador CLI preexistente | 33.1B, GPU ~96 GB em BF16; ZeroGPU 5 min/dia não garante sucesso |
| Wan-Animate-2 (lançado agosto de 2026) | **Transferência de movimento** diretamente de vídeo para imagem, com identidade e novos ângulos | CLI oficial Base/Distillation, preparado; sem inferência | Usos oficiais 720p com 8×A800; 480p com 2×A800; **NÃO tratar como troca cirúrgica preservando a multidão** |
| Viggle V1 Video Remix | Personagem + vídeo de dança; primeira animação hosted de custo potencial zero | API e gateway local experimental existentes | Créditos de conta não confirmados, cobrança por créditos, seleção do dançarino na multidão não garantida |
| Kling VIDEO 3.0 Motion Control | Movimento de uma pessoa e imagem de personagem, boa rota potencial para vídeos virais | Candidato apenas; não conectado | Serviço/API medido em créditos, tende a novo cenário, ator dominante, não garante conservar outros dançarinos |

Fontes oficiais:
- Wan2.2: https://github.com/Wan-Video/Wan2.2 ; https://huggingface.co/Wan-AI/Wan2.2-Animate-14B
- Wan-Animate-2: https://github.com/Wan-Video/Wan-Animate-2 ; https://blog.comfy.org/p/wan-animate-2-is-now-available-in
- Viggle aberto: https://huggingface.co/Viggle/Viggle-Animate
- Viggle V1: https://docs.viggle.ai/v1/guides/quickstart-mix
- Kling 3.0 Motion: https://kling.ai/quickstart/motion-control-user-guide

### Onde conseguir GPU/credits a custo adicional zero — ainda NÃO validados na conta

1. **Vercel AI Gateway** anuncia US$5 de crédito a cada 30 dias para contas Free sem pagamentos prévios. O Kling 3.0 Motion Control aparece com tarifa base de US$0,13/s (~US$0,39 para três segundos, antes de variações). Requer conta, autorização, verificação de saldo e teto de gasto zero com recarga automática desabilitada. A disponibilidade e a contabilização efetiva do vídeo não foram confirmadas. É um candidato para MOTION_TRANSFER, não garantia de substituição do Rio. Fontes: https://vercel.com/ai-gateway/models/kling-v3.0-motion-control e https://vercel.com/docs/ai-gateway/pricing
2. **Comfy Cloud** anuncia cinco execuções experimentais gratuitas em GPUs reais, sem cartão. A execução específica de Wan-Animate-2, duração das sessões, disponibilidade e política de retenção não foram testadas na conta. Fonte: https://comfy.org/wan-animate-2/
3. **Hugging Face ZeroGPU**: Free 5 minutos de GPU/dia, compartilhada. Pode não executar modelo pesado em tempo de quota. Fonte: https://huggingface.co/docs/hub/en/spaces-zerogpu
4. **Colab Free/Kaggle**: GPU gratuita eventual, sem reserva/VRAM garantida. Triagem sempre antes de qualquer download grande.

**Regra financeira:** catálogo não autoriza consumir nenhum recurso automaticamente. Nenhum fallback pago. Todo motor com uso medido requer verificação de saldo gratuito, limites e consentimento explícito. Não habilitar API key no JavaScript público.

## Mudanças entregues no código

- cloud/engine_registry.py: catálogo estruturado, tarefas, capacidades, limites, custo e condição de execução, com plano zero orçamento e bloqueio de engines incompatíveis.
- cloud/wan22_animate_adapter.py: **pré-processar/gerar** através da CLI oficial, duas etapas distintas, dry-run por padrão.
- cloud/wan_animate2_adapter.py: Base ou Distillation, comando oficial; não confunde reprodução de coreografia com preservar cenário.
- cloud/local_render_gateway.py: GET /api/engines retorna apenas candidatos compatíveis, POST /api/prepare guarda tarefa e motor escolhido e bloqueia POST de inferência para mecanismos sem backend autorizado.
- generate.html / generate.js: seleção de tarefa e motor; botão Gerar ativado apenas se backend e saldo confirmados. Nesse estágio, somente Viggle Remix possui adaptador HTTP de submissão. Os demais são adaptadores de execução offline opcional.

## Aceitação do primeiro MP4

O novo comando CPU-only `tools/audit_generated_video.py` lê metadados reais por FFprobe e recusa um resultado que seja apenas uma cópia byte a byte do vídeo de entrada. Também testa duração, proporções e quantidade de quadros. A saída só pode receber `PASS_REVIEWED` quando os dez critérios de auditoria visual forem explicitamente revisados e aprovados, incluindo cabelo, chifres, asas, roupas, movimento, cenário e outros dançarinos.

Exemplo **somente depois** de obter um vídeo real:

```bash
python tools/audit_generated_video.py --source assets/driving.mp4 --output albedo_3s_rendered.mp4
```

Se não houver arquivo MP4 realmente renderizado, o comando devolve NO_GO. Um resultado `RENDERED_NEEDS_VISUAL_REVIEW` significa apenas que a estrutura do vídeo é compatível, **não que IA ou substituição fiel tenham sido provadas**. O JSON opcional de revisão precisa ser preenchido a partir de inspeção dos quadros. Não automatizar essa aprovação com respostas simuladas.

## O que continua faltando para renderizar o Rio

1. Verificar disponibilidade e instalar checkout + pesos do Wan2.2-Animate onde houver GPU gratuita suficiente. **Ainda não foi executado.**
2. Rodar pré-processamento **oficial** com detecção da pessoa central, face, máscara e fundo para toda a sequência, não apenas o quadro de segundo 1. Rever seleção de alvo na multidão.
3. Produzir arquivo MP4 e comparar com os 72 quadros originais. A Albedo deve manter chifres, asas, roupas, cabelos, rosto adulto e proporções sem distorções.
4. Documentar métricas de quadros, deformação e alterações indesejadas de outros participantes. Somente depois expandir para dois personagens e clipes virais longos.
5. Se o Wan2.2 não rodar na cota disponível, testar Viggle-Animate aberto e/ou serviço de geração com créditos promocionais com limite estrito e sem cobrança real, mantendo transparência.

## Qualidade, identidade e direitos

O usuário pode usar referências visuais de personagens conhecidos para **fan edits** e experiências criativas; para publicar ou monetizar, verifique direitos e regras aplicáveis às personagens, áudio e vídeos de terceiros. Distinguir conteúdo sintético de imagens autênticas; não insinuar que artistas/atores reais endossaram a edição.

## Status honesto em 29/10/2026

**Código:** integração estrutural com catálogo e CLI para Wan2.2 e Wan-Animate-2. **Testes:** inicialmente apenas simulados/offline, sem pesos nem GPU. **Vídeo final da Albedo:** NÃO RENDERIZADO. **Custo adicional:** R$0.
