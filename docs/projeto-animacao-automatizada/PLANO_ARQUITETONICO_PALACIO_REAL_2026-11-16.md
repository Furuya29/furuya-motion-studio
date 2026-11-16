# Palácio real élfico — plano arquitetônico de continuidade v0.1
**Data:** 16/11/2026
**Natureza:** especificação preliminar para projeto autoral, cinematografia e MMORPG de *The Darkness of Aenvarath*. **NÃO é planta final aprovada**, não é malha 3D pronta, não substitui imagens canônicas.
**Referências:** [checkpoint narrativo atualizado](CHECKPOINT_NARRATIVO_ATUALIZADO_AENVARATH_2026-11-16.md), [contexto mestre](CONTEXTO_MESTRE.md), [handoff integral](HANDOFF_INTEGRAL_CHAT_REFERENCIAS_2026-11-16.md).

## 1. Requisitos já fixados pelo proprietário
1. Palácio monumental, colossal, mais imponente do reino, arquitetura **não genérica**, com silhueta inconfundível e estrutura passível de construção no MMORPG.
2. **Torre mais alta:** observatório/cúpula **aberta e absolutamente circular em planta**; nenhuma construção do palácio ou do reino deve ultrapassar sua altura. Vista externa e interna devem concordar.
3. **Salão do trono:** nave longitudinal cujo comprimento supera a largura; portal de entrada e trono sobre **um mesmo eixo**. Tapete vermelho/vinho que sai do trono e segue **reto, sem bifurcações, desvios, emendas diagonais ou mudança súbita de orientação**.
4. **Arquitetura adjacente ao trono:** duas janelas góticas de grandes dimensões, uma em cada lado, nas regiões já mostradas nos frames aprovados, juntamente com pares de estandartes e mobiliário existente. Não inventar nova fachada ou mover janelas entre tomadas.
5. **Brasão real aprovado:** desenho único, sem versão genérica. Em planos abertos distantes, pode ter simplificação LOD consistente; não produzir outro símbolo. Priorizar os estandartes mais próximos da câmera.
6. Materiais e linguagem já visíveis: pedra escura/polida, metal dourado ricamente trabalhado, rubis, veludo vinho, vitrais ogivais, ornamentos élficos, iluminação de velas e clima nevado. Preservar sem transformar em castelo gótico convencional.
7. Exterior do palácio deve ser arquitetonicamente derivado dos ambientes aprovados; jamais criar panoramas independentes com tamanhos/contornos incompatíveis.
8. Portas: física de dobradiças, batentes, maçanetas/fechadores e sentido de abertura; o guarda vem do lado externo e empurra do lado correspondente, nunca atravessa folhas impossíveis.

## 2. Diretriz de projeto: desenho, não decoração
O elemento distintivo não será simplesmente a quantidade de espiras, ouro ou colunas. A identidade deve nascer de uma **lógica formal própria**: geometrias élficas inspiradas na heráldica oficial, hierarquia radial/axial, estrutura consistente, escala monumental, detalhes de construção plausíveis e zonas públicas/cerimoniais/residenciais/defensivas conectadas. O projeto final precisará equilibrar simbolismo da soberania com circulação e física de mundo persistente.

**Não canonizar de antemão** o número de alas, torres menores, perímetros, alturas absolutas, orientação geográfica, nome oficial do palácio ou quantidades de pavimentos. Tais parâmetros exigem estudo de blocagem e aprovação do proprietário.

## 3. Masterplan proposto a desenvolver
Fases, com controle de versão próprio:
- **A. Implantação e topologia:** contorno geral do complexo e capital, limites naturais, orientação solar/noturna, entradas, pátios, relações de terreno e altimetria; torre como cota máxima de todo o conjunto.
- **B. Planta de pavimento principal:** salão do trono, porta principal, eixo do tapete, circulação lateral, acesso ao observatório e aposentos, escadas e ambientes de apoio. Deve ser navegável no MMORPG.
- **C. Planta da torre:** cilindro circular com centro, raio, eixo vertical, apoios, pilares, portas, escada/elevador mágico se canonizado, peitoril circular, vãos ogivais e abertura superior. Não introduzir vigas ou telhados sobre o óculo se não existirem nos quadros.
- **D. Elevações e cortes:** fachadas frontal/traseira/laterais, corte longitudinal trono-porta e corte vertical pelo eixo da torre; conferir alturas, espessuras, vãos, conexão entre andares e linha do horizonte.
- **E. Linguagem de módulos:** família de janelas, colunas, capitéis, arcadas, gradis, portas, painéis e suportes de estandartes; variantes coerentes, não inventar uma a cada geração.
- **F. Blockout 3D + match de câmera:** geometrias-base com escala de referência da personagem/guarda, câmera e lentes reconstruídas dos quadros de aprovação, teste de correspondência entre imagens vistas do trono, corredor, terraço e exterior da torre.
- **G. Assets de produção:** modelos e materiais otimizados para uso cinematográfico e como fonte de conteúdo do Unreal Engine; perfis LOD, separação de colisão, UVs, módulos, iluminação e instanciamento, apenas após aceite do blockout.

## 4. Sistema métrico, coordenadas e rastreabilidade
**Proposta técnica, ainda NÃO valor canônico:**
- Um sistema mundial fixo por locação; unidades em **metros**, eixo vertical positivo e norte de referência definido no masterplan.
- Pontos estáveis de controle: centro do trono; centro da porta principal; centro do óculo circular; extremidades da passadeira; eixos de cada janela, estandarte e pilar; pontos de câmera originais.
- Toda vista terá `location_id`, `revision`, `camera_id`, `lens_mm/fov`, `camera_transform`, `look_target`, `reference_image_id`, `reference_sha256` e status `proposto/aprovado/superado`.
- Projeção: um círculo geométrico em planta pode parecer **elíptico em perspectiva**, o que não autoriza uma torre elíptica, poligonal ou achatada em planta.
- Os estandartes terão um `emblem_asset_id` e duas resoluções/LODs derivadas do mesmo brasão.

## 5. QA de arquitetura obrigatório antes de cenas novas
| Teste | Critério / falha bloqueante |
|---|---|
| Torre | seção horizontal circular, topo circular; nenhuma torre externamente mais alta |
| Trono | eixo da câmera e do tapete consistente com portal principal; salão mais longo que largo |
| Janelas | duas grandes janelas simétricas atrás/ao lado da região do trono conforme frames aprovados, sem trocar de lugar |
| Brasão | geometria aprovada idêntica nos estandartes; LOD sem reinvenção |
| Percurso | personagem e guarda não teleportam entre portas/corredores; direção de movimento preservada |
| Portas | dobradiças e ferragens corretas; sentido de abertura e mão em contato plausíveis |
| Perspectiva | proporção espacial consistente ao mudar distância focal/posição; sem crescimento artificial de paredes |
| Escala | portas, corrimões e degraus navegáveis; rainha >1,80 m conforme correção recente da ficha, medida exata pendente |
| Continuidade de imagem | mesma arquitetura e materiais em todas as câmeras; sem alteração não autorizada de trajes/corpo |
| Evidência | diferenças documentadas por par antes/depois, com aprovação humana; still bonito não é prova de mapa consistente |

## 6. Decisão operacional até finalizar as plantas
- **Não gerar novas vistas externas definitivas** do palácio com geometria improvisada.
- Os quadros já aceitos do trono, guarda, corredor, torre interna e voo externo seguem como **referências de projeto**, não devem ser descartados por incompatibilidades corrigíveis.
- É válido continuar, **se for a sequência autorizada**, o teste de animação a partir da vila destruída, pois essa frente não depende de fechar a planta do palácio. Não confundir tal teste com o piloto técnico P15 da [Issue #12](https://github.com/Furuya29/furuya-motion-studio/issues/12).
- Antes da próxima tomada de voo mostrando uma panorâmica inédita, montar **silhueta externa + blockout 3D persistentes** do palácio, incluindo a torre circular.
- O custo alvo permanece **R$ 0**, com revisão de limitações de hardware e licenças; nenhuma alteração no PCRA, ramo recast ou `main` por esta documentação.

## 7. Critérios de aceite da planta definitiva — ainda pendentes
1. Planta geral e de níveis com corredores/conexões coerentes.
2. Elevações e pelo menos dois cortes que comprovem forma, proporções e a torre circular dominante.
3. Blockout 3D com match-camera de pelo menos quatro quadros aprovados (trono frontal, porta/guarda, torre interna, exterior/cúpula).
4. Biblioteca única de arquitetura e brasão com IDs e checksums.
5. Revisão explícita do proprietário sobre proporções, monumentalidade e originalidade.
6. Só então elevar a versão de **plano proposto** para **arquitetura canônica aprovada**, registrando commit e mudanças sem apagar histórico.

**Status em 16/11:** plano de execução documentado; nenhuma geometria 3D, planta final ou vídeo foi gerado/validado por este arquivo.
