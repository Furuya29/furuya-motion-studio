# Openjutsu × Genjutsu — investigação, compatibilidade e rota do Furuya

**Investigação:** 31/10/2026. **Objetivo prioritário:** substituir pessoas de vídeos virais existentes por personagens de anime/cinema, mantendo movimento e, quando pedido, a festa/multidão intactas.

## Conclusão verificada

**Higgsfield Genjutsu** é um produto **proprietário**. Seu modo *Object Swap* altera uma pessoa ou elemento específico enquanto pretende preservar o restante da tomada; *Motion Transfer* transfere coreografia/câmera e pode reconstruir o fundo. O modo Genjutsu Lite é outro produto mais rápido, com limitações próprias. A documentação oficial do site fala em clipes de **4 a 30 segundos**, várias referências e prompts opcionais. A API é paga por segundo; o playground oficial publica **US$0,318/s (480p)** e **US$0,681/s (720p)** no modo Motion Transfer, antes de descontos. **A edição de 3 segundos do nosso piloto não está dentro da duração mínima documentada para a interface web; a API pode ter regras próprias e não foi testada.** Não presumir créditos gratuitos.

**Openjutsu**, projeto independente de D3voz, descreve-se expressamente como *alternativa aberta ao Genjutsu*. Usa ComfyUI, MiniMax H3, SAM 3.1 e modelos de visão. **Não é o código-fonte do produto Higgsfield**. O workflow avançado documenta correspondência por papéis em **1 a 4 pessoas**, mantendo pessoas não selecionadas sem edição. Está de acordo com o objetivo do Furuya, mas não significa que o vídeo viral de terceiros tenha sido produzido nele: não há metadados/fonte do render que atribuam com segurança a ferramenta usada.

Fontes oficiais verificadas:
- https://higgsfield.ai/genjutsu
- https://higgsfield.ai/creator-hub/help-center/tools/how-do-i-use-genjutsu
- https://open.higgsfield.ai/models/higgsfield/genjutsu/motion-transfer/v1.0/playground
- https://github.com/D3voz/openjutsu
- https://github.com/D3voz/openjutsu/blob/main/lib/advanced.ts

## Recursos e modos do Openjutsu relevantes ao Furuya

| Modo | Referências | Aplicação | Estado no Furuya |
| --- | --- | --- | --- |
| Advanced padrão | 1–4 | Reproduzir dança da festa trocando 1 a 4 participantes, com papéis individuais e SAM tracking | **Workflow oficial incluído, adaptador de grafo e interface integrados** |
| Advanced **MaxQ** | 1–2 | Uma passagem separada por personagem; candidato para casos de maior fidelidade, com maior consumo de GPU | **Novo workflow oficial incluído, adaptador, interface e testes** |
| Montage | Depende da montagem | Pessoas se alternando, reaparecendo ou cruzando tomadas; permite análise prévia *Find people* e ajuste de identidades | **Candidato a próxima integração; não executável pela interface Furuya ainda** |
| Simple | 1 | Trocar pessoa principal do quadro | Referência upstream; ainda sem fluxo individual dedicado no Furuya |
| Object swap (projetos do próprio Openjutsu) | Depende do workflow | Editar roupa/objeto/fundo no vídeo | Ainda não conectado ao botão Furuya |

**Não confundir** Advanced MaxQ com a habilidade de transformar 3 ou 4 pessoas no mesmo passo: o workflow publicado possui **duas entradas de imagem** (verificado por IDs). O Furuya bloqueia uma terceira.

### Proveniência dos workflows usados nesta versão

- `workflows/openjutsu_advanced.api.json`: obtido do upstream `D3voz/openjutsu/workflows/advanced.api.json`. Checagem em 31/10/2026 confirmou conteúdo idêntico ao upstream nessa revisão; entradas `2`, `5`, `8`, `11`, vídeo `14`, plano `20`.
- `workflows/openjutsu_advanced_maxq.api.json`: obtido do upstream `D3voz/openjutsu/workflows/advanced_maxq.api.json` (blob Git SHA `4437ea9784b3727929f6579e4d8fa15e7b9d532d`); entradas `2`, `5`, vídeo `8`, plano `14`.
- Código-fonte dos workflows sob a licença MIT do Openjutsu; licença arquivada em `workflows/OPENJUTSU_LICENSE.txt`. **Modelos/LoRAs e vídeos de terceiros têm licenças independentes.**

O adaptador de grafos `cloud/openjutsu_advanced_adapter.py` detecta automaticamente se o workflow tem duas ou quatro entradas, remove imagens e descritores não usados e confere links para nós existentes. O trabalho e o recibo agora incluem `workflow_variant` e `workflow_character_capacity`. A interface `generate.html` permite escolher Standard ou MaxQ; o modo escolhido não submete GPU por conta própria.

## Escolha automática Furuya — sem perder os outros motores

No caso **uma pessoa preservando a cena**, o `routing-policy.json` passa a sugerir Openjutsu antes de Wan2.2-Animate, dado que já existe o fluxo de rastreamento + geração no mesmo grafo e o suporte documentado a multidões. Trata-se de uma **prioridade de avaliação**, não uma afirmação de que o Openjutsu gerará melhor nem de que há GPU pronta.

Os demais motores anteriores seguem no catálogo. **Genjutsu Object Swap e Genjutsu Motion Transfer** foram catalogados como `RESEARCH_ONLY` e `expected_paid_cost=True`; ficam excluídos de `candidates(..., zero_paid_budget=True)`, do roteador automático e dos botões de execução. Nenhuma chave Higgsfield é necessária ou coletada e **nenhuma chamada paga foi realizada**.

## Podemos executar de fato agora?

**Ainda não**: as etapas de importação, preparação, interface, requisição e auditoria são código real, mas a inferência exige nós, pesos MiniMax H3/SAM3.1 e uma GPU NVIDIA adequada. O desenvolvedor do Openjutsu cita testes em **RTX 4060 Ti 16 GB com 64 GB de RAM de sistema** (quantização/streaming); isso não é requisito mínimo universal. Nosso ambiente corrente não está ligado a uma GPU gratuita validada. O **Desktop Commander do PC DESKTOP-71MFUMA foi consultado e estava offline em 31/10/2026**; nenhuma instalação remota foi feita.

**Marco P0 ainda pendente:** executar Openjutsu/MaxQ com GPU gratuita compatível e clipe piloto da Albedo, inspecionar todas as pessoas e quadros, validar chifres, asas, roupas, oclusões e preservar o áudio. Se a primeira rota ficar sem GPU, avaliar provedores **sem pagamento obrigatório** antes de habilitar qualquer fallback. O modo Montage/Find people merece prioridade para as demonstrações multipersonagem quando o ambiente estiver disponível.

## Regras para vídeos com personagens conhecidos

Para testes de fãs, usar referências autorizadas, não atribuir endosso a artistas reais, respeitar direitos das personagens e o vídeo/áudio original, e sinalizar manipulação quando isso evitar engano. Publicação/monetização pode demandar licenças ou autorização adicionais.
