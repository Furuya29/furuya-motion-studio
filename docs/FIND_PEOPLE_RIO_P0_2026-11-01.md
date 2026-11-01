# Furuya Motion Studio — Openjutsu Find People antes do render

**Versão:** 01/11/2026. **Estado:** integração de transporte implementada e testável com servidor ComfyUI sintético. **Nenhuma inferência SAM/Qwen real feita no Furuya.**

## Fundamento oficial

O upstream Openjutsu disponibiliza `workflows/people.api.json`, com nove nós:

1. `VHS_LoadVideo` — vídeo MP4 original; entrada `video` no nó 1.
2. `CheckpointLoaderSimple` — modelo SAM 3.1.
3. `CLIPTextEncode` — prompt `person`.
4. `ImageScaleToMaxDimension` — quadros para rastreamento.
5. `SAM3_VideoTrack` — rastrear todas as pessoas.
6. `H3TrackCrops` — recortes e papéis por pessoa; entrada `people` com `<Subject 1>: the central dancer`.
7. `CLIPLoader` — Qwen3-VL para identificar papéis.
9. `H3TrackRoles` — correspondência das aparições com papéis.
10. `H3MontagePeople` — salva JSON com aparições e um arquivo temporário `.npz` de máscaras no ComfyUI.

Fonte: https://github.com/D3voz/openjutsu/blob/main/workflows/people.api.json e https://github.com/D3voz/comfyui-h3-oneclick-swap .

**O Find People não gera vídeo.** No Openjutsu original, sua revisão é utilizada no modo *Montage* com `H3MontageTracks`. O Furuya **ainda não conecta** o resultado revisado a um trabalho Montage: as versões Advanced Standard e MaxQ permanecem com seus próprios fluxos SAM.

## Etapas implementadas

- `workflows/openjutsu_find_people.api.json`: cópia do workflow oficial sob atribuição MIT.
- `cloud/openjutsu_find_people_jobs.py`: objeto separado que aceita **somente** o vídeo de uma tarefa Openjutsu já preparada; associa as descrições de personagens/pessoas aos nós oficiais, valida pré-requisitos e envia apenas um `POST /prompt` ao ComfyUI local após autorização explícita.
- `/api/comfy/people/start`: precisa do cabeçalho `X-Furuya-Confirm: AUTHORIZE_LOCAL_GPU` e confirmação de que há recursos gratuitos.
- `/api/comfy/people/status`: consulta sem reenviar.
- `/api/comfy/people/review`: entrega o JSON verdadeiro obtido do `H3MontagePeople`, com recortes JPEG e intervalos. Limitado a respostas que passam validações de forma, nomes e tamanho de payload. Nenhum nome de pasta externo é aceito.
- `/api/comfy/people/resume`: retoma apenas consultas GET pelo ID já recebido; jamais uma segunda submissão.
- `generate.html` e `people.js`: painel de revisão por aparição, sem atribuir sucesso a uma inferência não realizada e sem download dos pesos automaticamente.
- Recibos `local-render-jobs/people-jobs/receipt.json` e relatório `people-review.json` são separados dos trabalhos generativos. ComfyUI poderá limpar máscaras temporárias `.npz` ao reiniciar, invalidando um futuro render Montage; é necessário refazer Find People nessa situação.

## Condições de segurança e custo

- Somente ComfyUI em 127.0.0.1, sem proxy aberto ou GPU paga configurada.
- Pré-verificação exige disponibilidade de nós/modelos e confronta recursos CUDA/RAM com o perfil de referência testado no Openjutsu. Isso não garante inferência nem direitos sobre pesos.
- Respostas de rastreamento são marcadas `TRACKS_READY_UNREVIEWED`, não `approved`.
- Proteção contra reenvio após falha, timeout ou recibo incerto.
- **Sem GPU gratuita compatível não há render nem rastreamento real.** O Furuya apenas prepara o código para executar uma vez que exista infraestrutura.
- Não usar saída do Find People como máscara definitiva para Albedo sem revisar chifres, asas e passagens na multidão.

## Aplicação ao caso Rio + Albedo

1. Importar clipe original + Albedo, definir quem substituir (`the central dancer - light shirt, center of the frame`), e preparar o workflow Openjutsu.
2. Conferir o diagnóstico de hardware, modelos e custo zero.
3. Com GPU realmente disponível, marcar autorização e usar **Encontrar pessoas**, que não realiza o render final.
4. Revisar recortes, identidade e períodos de oclusão; **não enviar** se a pessoa alvo não for clara.
5. Após suporte completo a edição de papéis e integração do resultado com Montage, gerar o MP4 e auditar cena, áudio e personagem.

## Vídeo externo fornecido para análise nesta conversa

URL: https://youtu.be/oTPyqqZD8Iw

Na sessão de 01/11/2026, o vídeo não pôde ser aberto pelo mecanismo de leitura pública do YouTube, e as buscas pelo ID não retornaram título/transcrição verificável. Portanto, não atribuir técnicas específicas, demonstrações ou timestamps a esse vídeo sem obter o arquivo ou uma transcrição. O usuário pode enviar o MP4 ou uma captura da descrição se desejar análise fiel.
