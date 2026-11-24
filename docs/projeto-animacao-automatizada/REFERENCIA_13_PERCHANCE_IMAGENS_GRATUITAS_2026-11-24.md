# Referência 13 — Perchance: geração gratuita de imagens sem cadastro

**Data:** 24/11/2026  
**Vídeo enviado pelo proprietário:** https://youtu.be/hCwhdRIdN20?is=cbn9dvuVsqllyCEB  
**Título público confirmado:** “IA que gera imagens de graça e SEM FILTRO E SEM LIMITES”  
**Serviço estudado:** https://perchance.org/ai-text-to-image-generator  
**Estado:** PESQUISA / METADADOS DO VÍDEO E FONTES OFICIAIS VERIFICADOS. Nenhuma geração de imagem foi executada nesta análise; a demonstração audiovisual completa do autor não foi assistida.

> **Regra de continuidade:** este registro é aditivo. Não substituir o pipeline multimétodo por tomada para Aenvarath, nem alterar modelos, imagens canônicas ou prioridade de produção. O Perchance do vídeo é ferramenta de **imagem estática**, não um motor de vídeo, rig, interpolação ou animação corporal.

## 1. O que o vídeo e o fornecedor efetivamente anunciam

O título e a descrição do vídeo apresentam **Perchance** como gerador de imagens por IA gratuito, sem criar conta e sem limites convencionais de créditos. A página oficial descreve o gerador como **“free, no sign-up, unlimited”**, com geração de grandes lotes e estilos como fotos, ilustrações, desenhos, personagens de anime e capas, sem marca d'água.

- Fonte oficial: https://perchance.org/ai-text-to-image-generator
- Termos oficiais, atualizados em 18/07/2026: https://perchance.org/terms-of-service

**Limite de evidência:** a promessa de "sem filtro" é linguagem do vídeo; não significa ausência de políticas, bloqueios de acesso, controles de abuso ou disponibilidade irrestrita de qualquer conteúdo. "Ilimitado" descreve ausência de cotas de créditos convencionais declaradas; **não garante** uptime, capacidade, acesso por automação, qualidade constante ou gerações simultâneas sem restrições.

**Diferenciar domínios:** este estudo refere-se a **perchance.org**, e não a sites homônimos como perchanceai.com, perchanceai.io, perchanceai.app ou perchance.site; seus termos e serviços não devem ser confundidos.

## 2. Licença de saída e restrição relevante para automação

A **FAQ nos Termos do próprio perchance.org** afirma expressamente que imagens e textos criados no Perchance podem ser usados comercialmente, que atribuição não é necessária e que a plataforma não reivindica copyright nas criações; a plataforma destaca que esta resposta da FAQ prevalece onde houver conflito com o contrato genérico sobre uso da saída.

Por outro lado, o texto dos **Termos, seção User Representations** (§3, item 5), declara que o usuário não acessará o serviço por meios automatizados/não humanos, como bot ou script. O texto também proíbe contornar limitações e proteções do serviço.

**Consequência para o PCRA e agentes:** **NÃO** incluir scraper, API reversa/não oficial, ferramenta de geração em massa controlada por bot ou automação por navegador sem autorização formal compatível com os termos e método permitido. Um repositório GitHub de terceiros que automatize Perchance **não comprova permissão de uso**. A possibilidade de fazer imagens manualmente no site permanece separada de integrar automação produtiva. Verificar se o fornecedor oferece meio oficial permitido e documentado antes de qualquer conector.

Embora a FAQ permita uso comercial da **saída** do Perchance, a originalidade, direitos de terceiros, marcas e ativos publicados pelo usuário continuam sujeitos à legislação. **Não publicar fichas canônicas, lore confidencial ou assets privados de Aenvarath em galerias públicas da plataforma.**

## 3. Potencial para a produção de Aenvarath

**Utilidade plausível, sem homologação:** 
1. Moodboards originais de vila destruída, neve, floresta, palácio élfico, luz mágica e criaturas.
2. Exploração rápida de **silhuetas, luz, ângulos, cores e ambientes** para storyboard e busca de direção de arte.
3. Geração de **candidatos** a cenários ou key illustrations secundárias de conteúdo novo, desde que revisados manualmente e aprovados antes de integrar a bíblia visual.
4. Imagens originais para testes de composição, iluminação e camadas, se houver qualidade suficiente.

**Limitação estrutural principal:** o gerador básico por texto não oferece, comprovadamente, um *identity lock* e *reference-image conditioning* robustos; usar o mesmo prompt/seed pode gerar **deriva de rosto, traje, anatomia, coroa e proporções**. Geradores comunitários especiais da plataforma podem oferecer recursos adicionais, mas são produtos/URLs distintos que exigem avaliação própria. Não atribuir ao gerador padrão recursos de img2img ou vídeo que não tenham sido comprovados.

Consequentemente, o Perchance **não deve redesenhar** Nólyrien, Nyraelis, guardas, palácio ou quadros-chave já canonizados, nem gerar múltiplas vistas incompatíveis e chamá-las de turnaround aprovado. **Não substitui** rigs 2D/3D, desenho de poses corretas, inbetweening, IK/contato, controle de câmera e cenários persistentes.

## 4. Comparação com o planejamento existente

| Dimensão | Perchance (estado verificado) | Encaminhamento |
|---|---|---|
| Custo de geração no navegador | Grátis, sem conta e sem créditos convencionais, segundo site oficial | Pode servir a ideação manual, sem garantir operação ilimitada |
| Uso comercial das imagens | Permitido na FAQ oficial; atribuição dispensada | Conferir direitos de ativos próprios/terceiros por caso |
| Geração de vídeo animado | NÃO é a função do gerador indicado | Manter motores de animação existentes |
| Consistência de personagem | Identity lock não demonstrado no gerador padrão | Não usar para mudar cânone nem gerar episódios sem QA |
| Suporte a referências/câmera | Não verificado nesse gerador específico | Não prometer parâmetros/controle de composição indisponíveis |
| Automação PCRA/API | Termos restringem bots/scripts; via oficial permitida não identificada | **NO_AUTO_ROUTE** até autorização oficial |
| Reprodução local offline na RX580 | Trata-se de serviço web; não há pesos locais verificados | Não instalar modelos supostos ou exigir GPU local |
| Qualidade artística para Aenvarath | Não testada | Curadoria manual e comparativo de imagens originais |

## 5. Verificação prática autorizável sem quebrar o projeto

Se houver interesse, conduzir **ensaio manual e não canônico**, sem enviar arquivos privados:
- Usar prompt de **cenário original genérico de fantasia** (não copiar designs protegidos), testar estilo anime 2D, fantasia semirrealista e composição ampla.
- Guardar imagens escolhidas, prompt, configurações permitidas, data, dimensões e hashes em espaço de trabalho privado.
- Avaliar perspectiva, anatomia, luz, identidade, texto/artefatos, estética e uso de recursos frente ao padrão do estúdio.
- **Só promover** imagens aprovadas ao acervo autoral; não forçar reutilização de personagens existentes apenas por semelhança de prompt.
- Registrar automaticamente as etapas de QA e tratamento **depois que a imagem já estiver disponível legalmente**; não fazer automação não autorizada da interação com Perchance.

**Conclusão:** uma fonte útil de **conceitos e imagens estáticas a custo zero**, mas **não** um motor de animação cinematográfica persistente nem uma rota de geração automática apta ao PCRA enquanto os termos restringirem bots e scripts. Nenhuma mudança de arquitetura, instalação, render ou homologação foi realizada nesta etapa.
