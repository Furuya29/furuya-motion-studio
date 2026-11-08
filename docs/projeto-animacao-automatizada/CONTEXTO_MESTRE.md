# Projeto de Animação Automatizada — contexto mestre

> Registro persistente de continuidade do projeto de produção cinematográfica e animação (2D anime japonês / 3D semi-realista e realista), separado do fluxo de *recast* de vídeos virais do Furuya Motion Studio. Atualizado em 2026-11-08.

## Missão e requisitos permanentes

- Construir um pipeline de animação audiovisual com qualidade cinematográfica superior às referências observadas, evitando “cara de IA”.
- Preservar identidade de personagens (rosto, cabelo, anatomia, roupas), relações espaciais, continuidade de cenários e objetos, materiais, iluminação e direção entre cortes.
- Permitir **anime 2D japonês** genuíno, 3D ou estética híbrida, sem obrigar a renderização em estilo ocidental.
- Não limitar a produção a desenho quadro a quadro: combinar **quadros-chave**, rigs 2D/3D, captura/retargeting de movimento, interpolação guiada, composição e geração de vídeo por IA apenas onde melhora o resultado.
- Dar suporte a atuação expressiva, movimentação corporal, câmera (planos, ângulos, movimento), cenários persistentes, interação e multidões.
- Custo operacional alvo: **R$ 0**; privilegiar software livre, recursos locais e opções gratuitas realmente disponíveis. Não supor acesso a GPU de datacenter.
- Hardware previamente informado: PC Windows 10 Pro, AMD FX-4300, ~16 GB RAM, Radeon RX 580 8 GB; Android Redmi K70 Ultra. Projetos conexos (PCRA / Android Agent / Furuya Motion Studio) permanecem independentes; não confundir produção de filmes com substituição de dançarinos.
- Supervisão humana para aprovação artística, QA e intervenções inevitáveis; automatizar a rotina técnica sempre que possível.

## Evidência nº 1 — “TS Malfoy” (Fantasoner)

- Referência: https://www.youtube.com/watch?v=WYRDe8XsRmI — curta de fãs do universo Harry Potter, personagem Draco Malfoy feminina, declarado gerado com IA.
- Arquivo examinado pelo usuário: `1000589408.mp4` (não armazenado neste repositório por direitos e tamanho).
- Propriedades observadas: **1920 × 1080, 30 fps, 16.328 frames, 09:04,27**.
- Artefatos locais derivados na conversa: `Analise_Tecnica_TS_Malfoy_Animacao_IA.pdf`, `Evidencias_Visuais_TS_Malfoy.zip`. Esses arquivos não estão hospedados no GitHub; a presença apenas nesta conversa não garante acesso permanente ao binário.
- Observações resumidas: fotografia e direção de arte fortes; arquitetura e atmosfera coerentes na amostragem; atuação facial expressiva; montagem por cortes e poses relativamente sustentadas, com movimentos discretos de boca/olho/cabelo; desafios de animação corporal, continuidade de objetos, contato e movimentos longos.
- Sequências estudadas: 00:00–00:02 (olhos), 01:20–01:22 (fala), 04:40–04:42 (interação com armário), 06:20–06:22 (gesto/ameaça), 07:15–07:17 (duas personagens), 08:40–08:42 (close).
- Nota de QA: diferenças de pixels entre quadros **não equivalem** diretamente a deformações ou a “quadros congelados”; cenas escuras e compressão enviesam métricas. Não atribuir pipeline específico sem evidência do criador.

## Decisões após referência 1

1. **Priorizar representação consistente de personagens e cenários** antes de renderizar sequências longas.
2. **Direção por tomada** (shot specification: personagens, câmera, lente, movimento, duração, luz, ação, emoções, continuidade).
3. **Animação controlável**: usar rig / keyframes / motion tracking / retargeting como fonte geométrica do movimento, quando necessário.
4. **Geração de IA como camada supervisionada**, com comparação temporal e revisão de falhas em mãos, cabelos, roupas, objetos e expressões.
5. **Montagem / composição final** em editor/FFmpeg, com som e efeitos.
6. Teste-alvo inicial: **15 segundos**, planos distintos e pelo menos uma interação física, sob critérios mensuráveis; não prometer longa-metragem homogêneo por custo zero antes de validar.

## Referência nº 2 — Shift Up / Stellar Blade: BLOODRAIN

- Video recebido: `1000589429.mp4`, videoclipe **“Wanna be in LOVE” (Evie)**, duração **3:37,66**, **1920 × 1080, 24 fps, 5.222 frames**.
- Identificação pela cartela do próprio arquivo e fontes externas.
- Fontes públicas: https://www.videogameschronicle.com/news/are-we-deadass-fans-react-to-official-ai-generated-stellar-blade-music-video/ ; https://m.ajupress.com/amp/20260803150638274 ; https://www.pushsquare.com/news/2026/08/evie-was-created-by-our-talented-artists-stellar-blade-dev-responds-to-ai-slop-accusations .
- O CEO descreveu Evie como personagem desenvolvida por artistas e modeladores por mais de um ano, com apoio de IA na apresentação audiovisual; custo, hardware e pipelines exatos do videoclipe **não confirmados**.
- O “making of” ao final é encenado/gerado; não interpretar como evidência documental de filmagem física.
- Análise aprofundada e medidas para integrar ao pipeline registradas no documento de referência 2 (a ser acrescentado nesta pasta).
- **Não armazenar MP4 de terceiros nem materiais protegidos neste repositório** sem licença. Guardar metadados, fontes, anotações técnicas e decisões.

## Próximas provas

- Personagem com identidade invariável frente/perfil/3⁄4 e em movimento.
- Microatuação: emoções, olhar, fala com fonemas e respiração coordenados.
- Ação com contato: mãos, objeto, chão/parede, oclusão.
- Camera-tracking espacial, cenário persistente e continuidade entre dois takes.
- Registro de defeitos com timestamp, severidade, categoria e solução; reprovação automática de deformação crítica.

## Política de evidência

Distinguir: (A) fatos dos metadados do arquivo; (B) inspeção de frames; (C) fatos de fontes públicas; (D) hipóteses, recomendações ou testes pendentes. Nunca relatar hipótese como resultado comprovado.

## Controle de continuidade

Este documento é a referência mestre, que deve ser atualizada em novas análises, sem excluir as decisões existentes. Não transferir credenciais, dados pessoais ou arquivos protegidos de terceiros ao GitHub.
