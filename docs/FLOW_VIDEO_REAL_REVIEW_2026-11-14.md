# P0 — Teste real do Google Flow para substituição de cinco dançarinos

**Data da análise:** 14/11/2026. **Proveniência:** MP4 entregue pelo usuário nesta conversa. O arquivo do usuário não foi publicado neste repositório.

## Observação do vídeo

- Saída do Flow: vídeo H.264 **15,04 s**, **360×640**, **24 FPS**, com uma faixa AAC.
- Fonte de controle: trecho original da festa **3,00 s**, vertical, **30 FPS**, com dançarino central de camisa jeans e outras pessoas.
- A saída inclui **Albedo, Shalltear, Solution, Lupusregina e Narberal**, com figurinos visualmente reconhecíveis.
- Em vez de substituir corpos nas posições/movimentos originais, a saída distribui as cinco personagens em **uma linha frontal** e executa novos gestos, sem a coreografia específica da fonte.
- Iluminação e parte do ambiente continuam semelhantes, mas o posicionamento dos espectadores e personagens no fundo não foi conservado rigorosamente.
- A duração mudou de 3 para 15 segundos. Uma faixa AAC está presente, mas **não foi verificada a preservação do áudio original**.
- Segundo o usuário, retirar o áudio da entrada permitiu superar o filtro de edição de falas; isso não significa fidelidade de movimento.

## Veredicto

**Não atende à substituição corporal fiel sobre vídeo existente.** O Flow gerou uma *reinterpretação visual* da festa com cinco personagens; não editou de forma localizada e sincronizada cada pessoa original. O resultado não prova que o Flow seja incapaz de toda edição em outro material, apenas que este teste não cumpre os requisitos.

## Revisão do roteamento

- O motor Flow (flow_omni_edit) **permanece catalogado** para composições criativas ou preparação de imagens 3D.
- Foi retirado da prioridade automática para **substituição fiel**, em que fundo, papéis, coreografia e tempos devem permanecer.
- Para **1–4 pessoas**, Openjutsu Advanced é a primeira tecnologia a **avaliar** com máscaras e rastreamento; nenhuma instalação GPU gratuita ou render real foi confirmada.
- Para **cinco pessoas**, não há motor de uma passagem validado. O roteador retorna NO_SOURCE_FAITHFUL_FIVE_PERSON_ENGINE, sem indicar Flow como resposta.
- O orçamento continua **R$ 0** e o roteador nunca efetua render ou compra automaticamente.

## Próximo experimento de qualidade, verificável

1. Um único dançarino central, 3 segundos, Albedo como referência.
2. Uma **GPU gratuita realmente disponível e compatível** com o motor escolhido; caso ausente, manter o trabalho não executável.
3. Máscara e rastreamento temporal para preservar espectadores e arquitetura fora da área selecionada.
4. Gerar a mesma duração e verificar braços/pernas, oclusões, sombra, áudio autorizado e identidade quadro a quadro.
5. Somente depois adicionar as demais personagens por passagens controladas e composição.

Critérios de reprovação: PNG rígido, dança nova, mudança de câmera, pessoas extras modificadas, duração diferente, oclusões incompatíveis.

**A prévia por CPU continua válida para composição/teste de rastreamento, não como prova de substituição corporal generativa.**
