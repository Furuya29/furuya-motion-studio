# Furuya Motion Studio — Escolha automática de motores para vídeos virais

**Data:** 29/10/2026. Escopo atual: o usuário envia um vídeo viral existente, escolhe uma ou várias pessoas e associa personagens de anime, cinema ou originais. Não é geração text-to-video de cenas inéditas.

## Decisão de arquitetura

**Nenhum dos oito motores existentes foi excluído do repositório ou do catálogo:** Wan2.2-Animate, Viggle-Animate aberto, Viggle Video Remix, Wan-Animate-2, Openjutsu Advanced, Henge TARA, Wan VACE e Kling Motion Control. Motores em pesquisa aparecem como opções registradas, não como inferência funcional. Custos pagos continuam bloqueados no modo orçamento zero.

A interface mostra **Automático** por padrão e oferece **Avançado** para escolha manual da categoria e do motor. O motor selecionado fica nos bastidores, mas a recomendação e seus impedimentos podem ser visualizados para transparência. Não é necessário digitar um prompt de engenharia de IA.

### Regras automáticas compartilhadas

A única fonte de prioridades é `routing-policy.json`, utilizada pela UI e pelo servidor local. O Python `cloud/auto_router.py` publica um plano de recomendação auditável. É um mecanismo determinístico baseado nas capacidades, não uma chamada a um modelo de linguagem que supostamente conhece recursos externos.

| Pedido do usuário | Categoria | Ordem de avaliação |
| --- | --- | --- |
| Uma pessoa; preservar multidão/câmera | `scene_replacement` | Wan2.2 Replace, Viggle-Animate Open |
| Uma pessoa; apenas movimento, fundo pode mudar | `motion_transfer` | Wan-Animate-2, Viggle Video Remix |
| 2–4 pessoas no mesmo vídeo | `multi_scene_replacement` | Openjutsu, Wan VACE, Henge |

Cada motor precisa de validação operacional independente: pesos, GPU, créditos gratuitos, duração, licença, acesso à API, status do render e aprovação visual. Uma recomendação **nunca** confirma que o mecanismo pode renderizar naquele momento.

**Para dois a quatro personagens**, o Furuya direciona ao módulo `multicast.html` que guarda o elenco e suas marcações; esse módulo ainda não oferece rastreamento automático nem produção de MP4.

### Como crescer depois, sem refazer estrutura

Novos motores entram em `cloud/engine_registry.py` e na lista de prioridade compatível de `routing-policy.json`. Um backend separado deve ser testado e conectado antes de o botão Gerar ser habilitado. A versão estática em GitHub Pages exibe o mesmo catálogo e as regras via arquivos JSON estáticos; a versão local exibe o catálogo pelo gateway. **Nenhuma chave de API é incorporada ao site.**

Prompt descritivo de estilo/resultado pode ser adicionado como opção futuramente. A categoria e o número de pessoas são suficientes para a primeira decisão, e não exigem uso de tokens pagos de LLM.

### Segurança e orçamento

- A seleção automática é `ADVISORY_ONLY`, sem auto-execução nem fallback pago.
- O Kling permanece catalogado para pesquisa, porém excluído da escolha com orçamento R$0 sem comprovar cota gratuita específica.
- O código atual de backend pronto para uma tentativa de submissão é o Viggle V1 Video Remix, **somente para motion transfer**, com autorização explícita e consulta prévia de créditos. Ele não atende ao requisito de preservar a festa do Rio de modo garantido.
- A página pública não gera IA sozinha. O Wan2.2, Openjutsu, Henge e Wan-Animate-2 continuam precisando de ambiente GPU/pesos válidos; nenhum MP4 novo foi gerado por esta integração.

**Próximo P0:** obter uma inferência real de substituição de personagem inteira na festa do Rio, preservando pessoas não selecionadas, e só então oferecer o mesmo fluxo para múltiplos personagens.
