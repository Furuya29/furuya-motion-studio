# Referência 14 — Google Flow: vídeo longo por tomadas e ferramenta personalizada

**Data da triagem:** 24/11/2026
**Vídeo recebido:** https://youtu.be/gCsVA9UdcAs?is=SLwZkypaSvK13VNq
**Título verificado na página:** Como Fazer Vídeo LONGO Google Flow Automático e Sem Editor + ferramenta Grátis
**Autor indicado nos links/descrição e artigos correspondentes:** Erickson Lourenço
**Estado:** METADADOS E GUIAS DO AUTOR CONSULTADOS, DOCUMENTAÇÃO OFICIAL DO GOOGLE VERIFICADA, DEMONSTRAÇÃO AUDIOVISUAL INTEGRAL **NÃO INSPECIONADA**. Nenhuma criação de Tool, geração de vídeo, gasto de crédito, operação PCRA, instalação ou homologação executadas.

> **Regra de continuidade:** registro **aditivo**; não substituir o Estúdio de Animação & Cinemáticas multimétodo por tomada, não refazer frames aprovados, não transformar Motion Comic em entrega final de Aenvarath, não criar rota paga ou duplicar arquitetura existente. O pipeline canônico utiliza roteiro→shot spec→key drawings/rig 2D/3D→inbetweens→composição/edição→QA→aprovação humana.

## 1. O que se encontra diretamente na fonte enviada

A página do vídeo expõe título, descrição inicial e palavras-chave sobre Google Flow, Omni Flash, criação de vídeos longos, criação de ferramenta, personagens consistentes e automação. O texto inicial remete a:
- https://ericksonlourenco.com.br/bio
- materiais promocionais e ao prompt do autor;
- organização de cenas e vídeo longo sem editor externo.

**Limitação:** a transcrição integral, apresentação de tela, exemplos de filmes renderizados e identificação inequívoca da ferramenta bônus do vídeo não foram acessados. O guia no site é **fonte relacionada do autor**, mas não prova que cada detalhe foi executado no próprio vídeo.

Dois guias diretamente relacionados disponíveis na página do autor:
- https://ericksonlourenco.com.br/google-flow-como-criar-videos-longos-automaticos-ia-canal-dark/
- https://ericksonlourenco.com.br/como-criar-ferramenta-google-flow-omniflash-personagem-consistente/

O primeiro fornece um **prompt de planejamento**: converter roteiro em blocos de 10 s com Omni Flash, tratar o trecho final da tomada anterior como contexto de continuação, armazenar personagens/referências, montar MP4. O segundo fornece **prompt para gerar miniapp** com área de roteiro divido em cenas, referência opcional de personagem, geração de cada tomada, voz/trilha baixa, botão para juntar cenas.

Os artigos afirmam consistência visual alta e edição automatizada; tratá-las como **alegações do autor, não ensaios independentes**. O artigo 1 afirma possível montagem de 60 trechos de 10 s (10 min) em menos de 30 min; não há benchmark verificável de tempo, taxa de falhas, créditos totais e qualidade. O ChatGPT pode estruturar o prompt/arquitetura, mas **não** provou que o Flow ofereça invocação programática irrestrita para gerar lote de dezenas de cenas sem aprovação, quota ou consumo de créditos.

## 2. Contra-verificação indispensável: documentação oficial Google Flow em 24/11/2026

**Criar e gerir Tools no Flow:** https://support.google.com/flow/answer/17104535?hl=en

Conforme a documentação:
- O Flow realmente oferece **Tools**, miniapps reutilizáveis criados com linguagem natural. O Flow escreve código e interface.
- **CRIAR/EDITAR TOOLS PERSONALIZADOS exige Google AI Plus, Pro ou Ultra.** Sem assinatura é possível **usar e explorar ferramentas pré-criadas**, mas não criar livremente as próprias.
- Tools, na documentação atual, são disponibilizadas na **web/PC**. Qualquer mídia que uma Tool gere consome os **créditos do Flow**, com aviso quando há consumo; queries do agente podem não cobrar créditos, mas há cota diária de criações.
- O fato de conseguir gerar um app não demonstra a presença das APIs, quotas e permissões para automatizar o processamento em lote; cada chamada deve ser validada.
- Links compartilhados de Tools permitem acesso por terceiros ao **código, nome e miniatura**; não publicar lore, fichas privadas, cenas canônicas confidenciais ou assets protegidos sem revisão.

**Créditos/limites por conta:** https://support.google.com/flow/answer/16526234?hl=pt-BR
- **50 créditos por dia** para não assinantes e assinantes, não acumuláveis de um dia para outro. Em picos de 14–17h UTC pode não ser possível gerar vídeo sem assinatura.
- **Omni Flash 1.2:** sem plano, geração/edição de **3–10 s**; custo **1 crédito/segundo a 360p** ou **3 créditos/segundo a 720p**.
- **Omni Flash 1.2 3–15 s** e **Extensão nativa (3–10 s adicionais)** disponíveis a assinantes Plus/Pro/Ultra; custo variável por resolução e duração.
- **Veo 3.1 Lite 720p:** vídeos de 4/6/8 s; 10 créditos/geração para usuários não Ultra, conforme página atual. Não presumir ausência de limites de simultaneidade ou disponibilidade.
- Em **05/11/2026**, o modelo/função antiga **Veo Extend foi desativado**. Extensão nativa atual requer assinatura e Omni Flash 1.2.
- Em **05/12/2026**, estão previstas aposentadorias Veo 3.1 Fast/Quality e Omni Flash 1.1; revisar compatibilidade e custos quando ocorrerem.
- O custo é **por geração de vídeo**, e um pedido pode gerar dois vídeos. O custo final de 60 clipes com múltiplas tentativas é materialmente maior que uma única geração, e 50 créditos/dia não garantem episódios longos rápidos.

**Funcionalidades por plano/modelo:** https://support.google.com/flow/answer/16352836?hl=en
- Omni Flash 1.2 sem assinatura: text-to-video, frames-to-video web, ingredients/references-to-video, edição vídeo→vídeo de 3–10 s. Atenção: recursos variam por região e modelo.
- A edição de vídeos e suporte a imagens de referência **não equivalem a rastreamento perfeito do personagem, continuidade anatômica ou animação 2D profissional**.
- Mesmo com vídeos diferentes compartilhando frame final/inicial, a montagem não garante transição sem salto, fidelidade de roupa/rosto ou contato físico.

### Contradição prática com alegações de "100% grátis"

O método técnico de **criar uma ferramenta personalizada dentro do Flow** é real e documentado, mas a gratuidade integral da construção é desmentida pela documentação de assinaturas. É possível **usar Tools prontas gratuitamente**, sob os limites e eventual consumo de créditos. A promessa de 10 min totalmente automatizados e a confiabilidade de aparência não foram reproduzidas. O Google Flow e o Google Vids são produtos distintos: não misturar suas cotas (Flow diário x Vids mensal).

## 3. Consequências para o Estúdio de Aenvarath

**Incorporar SOMENTE como padrão de orquestração das etapas já aprovadas:**

1. **Roteiro e shot specification:** cenas com identificadores persistentes, personagens, cenário, câmera, pose de abertura/fechamento, áudio, tempo e continuidade espacial e narrativa; NÃO engessar Aenvarath em clipes de 10 s quando o blocking exige duração distinta.
2. **Biblioteca canônica:** character sheets originais aprovados, snapshots, vistas corretas, roupas, coroas, anatomia, assets, ambientes e hashes. Referência de 1–3 imagens é ajuda, não substitui a bible e geometria persistente.
3. **Método por tomada:** rigs 2D/3D, keyframes/intervalação/desenhos em perspectiva, modelos 3D, VFX e **IA generativa apenas quando o custo/QA permitir**. Motion Comic NÃO é o formato final.
4. **Edição automatizada gratuita e reprodutível:** FFmpeg/ffprobe, Kdenlive/MLT ou Remotion/editores já previstos, render por pipeline local autorizado. Roteiro para ordem, cortes, raccord, transições, áudio e passes; manter saída MP4 e arquivos-fonte, sem necessidade de editor externo manual em cada corte.
5. **Continuidade de imagem e som:** guardião entre takes mede identidade, rosto, roupa, coroa, wings, iluminação, geometria, contato e tempo de fala. Retake localizado sem apagar assets aprovados.
6. **Rota Flow (opcional):** geração manual/semiautomatizada de curtas apenas sob conta elegível e respeito às condições oficiais. Sem licença de Tool ou API autenticada, não assumir batch de 60 vídeos. **Nenhum pagamento/autorização de plano concedidos pelo estudo.**
7. **PCRA:** o canal produtivo para PC ainda precisa de evidência de execução/receipts; não tratar prompt ou documentação como comando executado em Windows.

**Aplicação direta ao checkpoint narrativo:** preservação de Nólyrien e de seu corpo/roupa/coroa; asas negras com implantação lombar/vista dorsal, torre externa circular e cena de voo; não trocar frames aprovados só por um estilo gerativo novo. Nenhum render da cena foi realizado neste estudo.

## 4. Gate para adoção e status

| Item | Estado |
|---|---|
| Ideia de divisão de roteiro em tomadas e exportação montada | Já existente no planejamento; artigo reforça |
| Miniapps do Google Flow criados por prompt | Capacidade oficial VERIFICADA |
| Criar Tool personalizada gratuitamente | NÃO — assinatura Google AI Plus/Pro/Ultra exigida |
| Usar Tools já criadas sem assinatura | Disponível segundo Google, sujeito a créditos e limitações |
| Geração de clipes Flow sem pagar | 50 créditos/dia; Omni 1.2 até 10s; Veo 3.1 Lite 10 créditos/4-8s, conforme documentação |
| Extender tomadas nativamente no plano gratuito | NÃO — assinatura exigida |
| Continuidade 100% entre 60 tomadas | NÃO COMPROVADA |
| 10 minutos de vídeo "automaticamente em 30min" | Alegação não validada |
| Criação efetiva de Tool nesse chat | NÃO EXECUTADA |
| Geração de vídeo Aenvarath nesse chat | NÃO EXECUTADA |
| Implementação de novo software ou modificações no PC | NÃO EXECUTADA |
| Merge do PR #13, conclusão de Issue #12 | NÃO EXECUTADOS |

**Decisão técnica:** registrar como **REFERÊNCIA 14 / pesquisa verificada**. O padrão de planejamento e montagem por cenas é adequado para integrar a automação **local e gratuita existente**, porém **não adotar a criação de Tool paga do Google Flow como dependência crítica**. Seguir o projeto principal e a priorização do PCRA sem modificação.

**Documentos de continuidade relevantes:**
- [CONTEXTO_MESTRE.md](CONTEXTO_MESTRE.md)
- [ARQUITETURA_CONSOLIDADA_MEGA_ESTUDIO_ANIMACAO_2026-11-16.md](ARQUITETURA_CONSOLIDADA_MEGA_ESTUDIO_ANIMACAO_2026-11-16.md)
- [HANDOFF_INTEGRAL_CHAT_REFERENCIAS_2026-11-16.md](HANDOFF_INTEGRAL_CHAT_REFERENCIAS_2026-11-16.md)
- [Issue #12](https://github.com/Furuya29/furuya-motion-studio/issues/12) e [PR #13](https://github.com/Furuya29/furuya-motion-studio/pull/13).

**Nenhum conteúdo anterior removido, nenhuma mudança de prioridades ou de motor, nenhum gasto/autorização paga.**
