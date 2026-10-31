# Furuya Motion Studio — GPU gratuita e diagnóstico do Openjutsu

**Pesquisa e implementação:** 31/10/2026. **Primeiro vídeo Albedo/Rio:** ainda sem inferência comprovada.

## Fatos técnicos confirmados

O [Openjutsu](https://github.com/D3voz/openjutsu) descreve execução em uma **RTX 4060 Ti de 16 GB VRAM e 64 GB de RAM de sistema**. O pipeline utiliza ComfyUI, MiniMax H3, SAM 3.1 e vários packs de custom nodes. Os autores descrevem de 6 a 13 minutos para seis segundos de vídeo em 480p em seu ambiente; isso é referência observada, **não promessa de duração no Furuya**.

A página oficial de suporte do [Comfy Cloud sobre custom nodes](https://support.comfy.org/articles/6791455062-custom-nodes-on-cloud) afirma que usuários **não podem instalar custom nodes arbitrários** na nuvem gerenciada; somente o catálogo já homologado. Não presumir compatibilidade com os packs necessários do Openjutsu.

A documentação oficial do [Kaggle Notebooks](https://www.kaggle.com/docs/notebooks) descreve opções de P100/T4 e **aproximadamente 29 GB RAM** nas opções GPU, abaixo da memória de sistema usada nos testes do Openjutsu. A documentação do [Colab gratuito](https://research.google.com/colaboratory/intl/pt-BR/faq.html) declara que o tipo de GPU e os limites variam sem garantia. Nenhuma dessas opções está aprovada como executor automático na conta do usuário.

Essas comparações servem para descartar tentativas improváveis e selecionar ambientes promissores; **não provam impossibilidade matemática** de usar quantização/offload diferentes.

## O que o Furuya verifica automaticamente

O módulo `cloud/comfyui_readiness.py` trabalha só por consultas locais de leitura:
- Compara todas as classes de nós do **workflow realmente selecionado** com `GET /object_info` do ComfyUI.
- Verifica os nomes dos checkpoints referenciados em nós ComfyUI padrão (UNET, LoRA, CLIP, VAE, checkpoint, SAMLoader) contra as listas de escolha dos respectivos nós.
- Consulta `GET /system_stats` para GPU, VRAM e RAM, sem expor `argv` nem outros argumentos do processo na interface.
- Compara o ambiente com a configuração publicada de **16 GB de VRAM NVIDIA e 64 GB de RAM**. Para tolerar diferenças entre GB/GiB e memória reservada, a ferramenta considera **15 GiB de VRAM e 58 GiB de RAM reportados** como aproximadamente equivalentes ao perfil testado, sem tratá-los como requisitos mínimos universais.

Resultados possíveis:
- `NO_GO_MISSING_COMPONENTS`: nós ou modelos listados necessários ausentes;
- `BELOW_OPENJUTSU_TESTED_BASELINE`: GPU/RAM não atingem o perfil testado ou a consulta não confirmou esses recursos;
- `UNVERIFIED_MODEL_CHOICES`: ComfyUI não anunciou opções verificáveis de modelos para algum nó;
- `PREFLIGHT_PASSED_NOT_RENDERED`: os critérios de **pré-verificação** passaram. **Não significa que a inferência rodará ou que a GPU é gratuita**.

O botão **Gerar vídeo pelo Furuya + ComfyUI** só é habilitado quando a verificação é positiva e a pessoa confirma explicitamente que o ambiente é autorizado e não gera custo. O servidor repete essa verificação imediatamente antes da submissão, mesmo que a interface seja manipulada.

**Limitações importantes:** ComfyUI mostrar um modelo em suas listas não prova integridade dos pesos, disponibilidade atual de toda a VRAM, adequação dos custom nodes, licença, nem garantia de geração. O programa não faz downloads, pagamento, instalação de drivers ou reserva de GPU.

## Status de disponibilidade de execução

| Plataforma | Disponibilidade gratuita geral | Openjutsu Advanced no Furuya |
| --- | --- | --- |
| PC atual (GPU RX580 8 GB, segundo handoff) | Local | **Abaixo do perfil testado; NO-GO para esta rota** |
| Comfy Cloud gerenciado | Pode oferecer testes gratuitos | **Não confirmado; instalação livre dos custom nodes necessária não está disponível** |
| Kaggle P100/T4 | GPU grátis com cotas | **Não validado; RAM documentada abaixo do teste Openjutsu** |
| Google Colab Free | GPU eventual, sem garantia | **Não validado; recurso disponível varia** |
| Outra GPU compatível sem cobrança | Depende de disponibilidade autorizada | Verificar automaticamente no Furuya antes de iniciar |

## Critério para liberar um render real

O primeiro trabalho só deve ser submetido depois de confirmar: (a) workflow + nós + nomes de modelo; (b) GPU e RAM suficientes no ambiente existente; (c) nenhuma cobrança/assinatura; (d) vídeo e referência corretos; (e) autorização explícita. Mesmo assim, a aprovação final exige MP4 produzido e auditoria visual do dançarino central, Albedo, multidão, asas/chifres/roupa e áudio.

Nenhum dos **oito motores multimotor** foi removido. Caso Openjutsu esteja indisponível, o orquestrador poderá recomendar outra rota **após avaliação de recursos**; não deve iniciar provedores pagos como fallback.
