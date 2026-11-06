# P0 — Find People → revisão de identidades → Openjutsu Montage

**Data:** 06/11/2026. **Estado:** integração implementada e sujeita a CI; **nenhum MP4 generativo produzido**.

## Objetivo

Transformar o resultado real do **Find People** do Openjutsu em um workflow **Montage** executável, respeitando os papéis aprovados pelo usuário na multidão da festa do Rio. O programa não deve trocar uma pessoa só porque o modelo Qwen sugeriu uma correspondência.

Este estágio complementa, e não substitui, Standard, MaxQ, Viggle, Wan ou outros motores do catálogo.

## Fluxo integrado no Furuya

1. Na interface `generate.html`, abrir o painel Openjutsu, importar o vídeo viral (MP4) e até quatro imagens de referência de personagem. Preparar o trabalho **sem GPU**.
2. Com ComfyUI local equipado com GPU e modelos comprovadamente disponíveis, executar `Find People` uma única vez, mediante confirmação. O processo gera recortes e máscaras temporárias; não gera vídeo.
3. Conferir cada aparição identificada na galeria. **Por padrão todas ficam inalteradas.** Escolher explicitamente quais aparições devem virar as referências 1–4. A interface mostra até 40 aparições; aparições não exibidas também permanecem originais.
4. Clicar **Aprovar pessoas selecionadas e preparar Montage (sem GPU)**. O gateway valida todos os IDs de trilha e intervalos e transforma o workflow oficial `montage.api.json` num job preparado. Ele remove os nós de análise duplicados, substitui conexões de SAM pelo `H3MontageTracks`, informa os rótulos aprovados a `H3MontagePlan` e mantém as fotos distintas de cada personagem.
5. O botão de geração original do Furuya poderá enviar esse workflow revisado ao ComfyUI, após uma **nova pré-verificação de nós/modelos/GPU/RAM e autorização explícita**, usando o recibo anti-reenvio existente.
6. Somente depois de receber um vídeo e passar por `ffprobe` e auditoria visual poderá ser considerado um MP4 de render; **`RENDERED_UNREVIEWED` ainda não significa substituição bem-sucedida**.

## Implementação

- `workflows/openjutsu_montage.api.json`: workflow API oficial do Openjutsu (MIT upstream); referência https://github.com/D3voz/openjutsu/blob/main/workflows/montage.api.json .
- `cloud/openjutsu_montage_review.py`: preparação de grafo a partir de seleções explícitas; não envia nada à rede. Segue a lógica oficial `pruneMontage()` em https://github.com/D3voz/openjutsu/blob/main/lib/montage.ts .
- `cloud/openjutsu_find_people_jobs.py`: `approve_montage` valida que revisão e vídeo são do **mesmo job**, salva cópia do workflow original e guarda recibo seguro. Uma interrupção na transição coloca a tarefa em estado de bloqueio (falha fechada), sem permitir render enganoso.
- `cloud/local_render_gateway.py`: `POST /api/comfy/people/approve`, com JSON limitado a 32 KiB e proteção de origem/ação local. Não permite submissão de GPU por este endpoint.
- `people.js`: controles de correspondência por aparição e botão de aprovação.
- `comfy.js`: identifica `reviewed_montage_4slot` e libera o botão de geração somente sob as proteções já existentes.
- `tests/test_openjutsu_montage.py` e extensão de `tests/test_find_people.py`: garantem correspondências, preservação de pessoas não selecionadas, recusa de IDs forjados e nenhuma execução de GPU.

## Limites e riscos remanescentes

**Não foi encontrada uma instalação operacional de ComfyUI no PC durante inspeção de leitura de processos em 06/11/2026.** O equipamento está online via conector, mas usa GPU AMD RX 580 8GB e não atende ao perfil testado pelo Openjutsu (NVIDIA RTX 4060 Ti 16GB e 64GB RAM).

O `H3MontageTracks` consome arquivo `h3_montage_people_XXXXX_.npz` temporário do **mesmo ComfyUI**; se ele reiniciar, limpar temporários ou receber outro trecho de vídeo, o nó pode recusar o render. O Furuya não copia esse arquivo para fora do servidor nem afirma verificá-lo antecipadamente.

Em vídeos com muitas pessoas, até as aparições revisadas podem ser classificadas incorretamente ou mudar identidade durante o rastreamento; conferir as correspondências é obrigatório para declarar qualidade. Máscaras e clipes não são preservados automaticamente fora do trabalho ComfyUI.

**Custo extra desta integração: R$ 0.** Nenhuma GPU, assinatura, API paga ou chamada a provedor foi acionada. A implementação não libera automaticamente um executor cloud.

## Próximo bloqueio real

Encontrar/autorizar uma **GPU compatível sem cobrança**, com nós oficiais, MiniMax H3, SAM 3.1, Qwen e todos os checkpoints instalados. Em seguida realizar o primeiro render real da Albedo (3 s) e auditar quadro a quadro a permanência do cenário, o movimento e as pessoas não alteradas.
