# Referência 18 — Claude + Blender MCP: 3D editável e cenas persistentes, mas não animação corporal completa

**Data:** 28/11/2026  
**Vídeo enviado:** https://youtu.be/HeOIltnhpVo?is=W3R6rgdoOuBqJh0a  
**Título:** “Claude + Blender é a Melhor Maneira de Criar Vídeos com IA (Tutorial Completo)”  
**Fonte inspecionada:** página original + **transcrição integral em português com timestamps (aproximadamente 10min)**, obtida do próprio vídeo. Fontes externas oficiais do Blender, Poly Haven, Blender MCP e Anthropic consultadas separadamente. **Não** houve avaliação da sequência visual quadro a quadro nem instalação/execução no computador do proprietário.  
**Classificação:** **REFERÊNCIA TÉCNICA ÚTIL / INTEGRAÇÃO PROPOSTA**, sem substituir a arquitetura consolidada do Estúdio de Animação e Cinemáticas.

> Regra: preservar todas as decisões e prioridades do projeto principal, sobretudo animação integral (não Motion Comic), rigs e quadros-chave, personagens e cenários canônicos, composição, PCRA e metas R$0. O tutorial reforça o núcleo **3D & Hybrid Engine** e **Cinematic Composition**, mas não homologa a animação de personagens Nível B/C.

## 1. Conteúdo demonstrado/alegado no próprio vídeo

| Timestamp | Conteúdo verbal do tutorial e importância |
|---|---|
| 00:00–00:47 | Autor afirma ter feito floresta noturna, neblina, carro, personagem, câmera, luz e render com comandos em português dirigidos ao **Claude**, produzindo uma **cena Blender 3D editável**, não um vídeo por prompt probabilístico |
| 01:34–02:06 | Declara usar **Claude Code**, incluído em planos pagos, mais **Blender gratuito**. PC razoável permite montagem; render requer mais compute |
| 02:21–03:59 | Conecta Claude Code ao Blender por **Blender MCP** e complemento; teste de cubo vermelho; descreve opção de não pedir confirmação a cada ação. **Atenção**: confiança ampla de código Python executável tem risco operacional |
| 03:59–04:48 | Usa objetos, materiais e HDRIs do **Poly Haven**; curadoria humana dos elementos centrais de estilo |
| 05:03–05:51 | Exemplo de prompt para floresta noturna, estrada de terra, carro, iluminação azul/fria, neblina, faróis; cena criada e revista em linguagem natural (autor afirma montagem em ~10–20 min, não há benchmark independente) |
| 06:23–07:29 | Para personagens específicos, recomenda geração externa de **modelos 3D**, com **Hyper3D** e um gerador referido na transcrição como “Runway One 3D” — nome/transcrição exatos devem ser revisados por fonte oficial, NÃO presumir integração comprovada com marca/capacidade específica. O autor indica créditos grátis para testes e depois cobrança; sugere solicitar esqueleto/rig |
| **07:29–07:45** | **Limitação expressa decisiva:** personagens gerados não caminham bem; autor contorna com personagem parado/de costas/em silhueta, mantendo a câmera em movimento. **NÃO demonstra locomoção natural, atuação corporal, mãos, pés, diálogos ou combate** |
| 07:45–08:33 | Compõe homem junto do carro e criatura ao fundo; dirige emoção e composição, não só coordenadas |
| 08:33–09:54 | Anima movimento de câmera, cortes e render MP4; recomenda **Eevee** por desempenho e preview em resolução baixa; objetos, cenário e câmeras permanecem editáveis para reutilizar em outros planos |
| 09:54–10:12 | Direção editorial/roteiro, reutilização da cena e importância da narrativa |

### Fato versus inferência

- O autor apresenta um método baseado em **cena 3D real e parametrizável**, não uma suposta IA que gera frames sem geometria; isso coincide tecnicamente com Blender Python API e MCP.
- A narrativa sobre rapidez/qualidade é **demonstração autorrelatada**, não teste reproduzido nesta sessão.
- O tutorial não demonstra personagens **anatomicamente perfeitos em movimentos complexos**, nem vista dorsal/front/3⁄4 continuamente on-model.
- Não comprova custo **R$0 do fluxo completo**: o próprio vídeo afirma Claude Code pago e geração de personagem 3D possivelmente cobrada.
- Se o render for feito na máquina do autor, isso é **renderização local 3D determinística**, não geração local por difusão de vídeo.
- A câmera sobre personagem estático pode ser uma boa decisão editorial em documentário, mas **não atende à entrega exigida de animação corporal real de Aenvarath**.

## 2. Verificações externas independentes

1. **Blender MCP / código fonte comunitário:** https://github.com/ahujasid/mcp-for-blender  
   Implementa comunicação por MCP e execução de código Python dentro do Blender, manipulação da cena, acesso a assets e screenshot. Não é exclusiva do Claude como tecnologia; um cliente MCP compatível ou o PCRA pode fornecer ações similares.
2. **Blender Python API oficial:** https://docs.blender.org/api/current/info_quickstart.html  
   Permite definir objetos, transformações, câmeras, armatures, keyframes, materiais e cenas por código; render em lote/background também é suportado: https://docs.blender.org/manual/en/latest/advanced/command_line/render.html.
3. **Poly Haven:** https://polyhaven.com/license — assets 3D, HDRIs e texturas **CC0**, inclusive uso comercial; conferir licença de qualquer asset de terceiros fora do Poly Haven.
4. **Eevee:** https://docs.blender.org/manual/en/4.5/render/introduction.html — motor de renderização em tempo real/fisicamente baseado, adequado a previews e produção otimizada. Sua qualidade depende de assets, materiais, luz e iluminação; noite/neblina/silhueta não provam animação completa.
5. **Hardware presente:** AMD RX 580 (Polaris) consta no grupo **RX 400–600** de suporte à plataforma Eevee 4.5, dependendo de drivers/versão, https://developer.blender.org/docs/release_notes/4.5/eevee/. **Cycles HIP GPU exige AMD RDNA1+**, e não pode ser declarado disponível na RX 580: https://docs.blender.org/manual/en/4.5/render/cycles/gpu_rendering.html. Com FX-4300, 16GB RAM e 8GB VRAM, começar com cenas low-poly/otimizadas, texturas controladas e previs leves.
6. **Claude Code preço:** https://claude.com/pricing — planos pagos com Claude Code. O proprietário não autorizou assinatura; **não é necessário assinar Claude para usar a arquitetura Blender em si**.
7. **Riscos de código e instalação:** Blender MCP documenta `execute_blender_code` e capacidade de executar Python arbitrário, com advertência de segurança no README; repositório inclui mecanismos de modo seguro, mas requer auditoria de versão/configuração e restrição de acesso. Evitar instalação sem revisão, serviços expostos e execução contra arquivos canônicos sem backup.

## 3. Aplicação real à arquitetura aprovada de The Darkness of Aenvarath

**A proposta NÃO é “adotar Claude” nem criar novo motor:** é aproveitar **o conceito de dirigir o Blender em linguagem natural e scripts versionados via ChatGPT + PCRA**, dentro dos núcleos atuais.

- **Cenários persistentes:** vila destruída com planta/coordenadas, casas, cavalinho, neve/brasas/fumaça/fogo volumétricos; palácio longitudinal com tapete reto, janelas góticas e estandartes; torre mais alta circular com abertura no topo; floresta de inspiração apenas para estudo, não gerar cenário genérico em lugar do cânone.
- **Direção de câmera:** positions/world transforms, lens/FOV, easing, dope sheet, tracking e plano/contraplano sem cenário “mudar” a cada geração.
- **Iluminação/VFX causais:** key/fill/rim, fog volume, neve integrada à profundidade, fogo com emissão e reflexos, fumaça e brasas animadas; render por passes, oclusão e sombras.
- **Personagens canônicos:** importação/desenvolvimento de modelos multivista/rigs do projeto, roupas e asas aprovadas; animação com armatures, constraints, IK, clips, mocap/retargeting, física e 2D genga/douga. O pedido genérico “gera e coloca esqueleto” **não substitui rigging/skinning/animation QA reais**.
- **Modo híbrido ou 2D:** usar Blender como base para blocking/3D persistente e render toon/NPR ou Grease Pencil quando as escolhas artísticas exigirem anime 2D, preservando também OpenToonz/Krita.
- **IA generativa local futura:** possível pós-processamento condicionado por pose/depth/edges/keyframes em Wan/LTX etc., depois de controlar geometria e atuação; não obrigatória nem executada por este estudo.

## 4. Proposta de integração sem gastos e sem reiniciar

**Trilha técnica recomendada, AINDA NÃO EXECUTADA:**
1. Após o PCRA produtivo estar comprovado, inventariar Blender, driver AMD, versão, plugins, compatibilidade Eevee e assets canônicos (somente leitura). Não instalar blindly.
2. Implementar **adapter de controle Blender Python** com scripts idempotentes, persistência `.blend`, JSON shot spec, logs, outputs e hashes, em diretório de projeto autorizado, com checkpoint e rollback. **Não depender de Claude pago ou de instância MCP com Python irrestrito**; MCP pode ser camada opcional após auditoria de segurança.
3. Produzir **um teste útil à narrativa existente**: cenário/torre circular em versão leve preservando dimensões aprovadas, câmera controlada, nevasca/fumaça/fogo ou movimento simples com rigs existentes, sem criar figuras estáticas como suposta animação.
4. Testar personagem Nólyrien apenas quando os assets/fontes aprovados estiverem disponíveis: asas negras **enraizadas na lombar**, superfície dorsal e coroa posterior corretas, movimento real das asas e início de voo; verificar identidade e continuidade, fonte/MP4 e revisão artística.
5. Testar percurso de câmera e variações de luz em **mesma cena .blend**, comparar renders e medir custo real (tempo/CPU/RAM/VRAM/energia). Depois expandir para movimento corporal, IK/contato/roupas e diálogo, sem deixar efeitos estáticos.
6. Conservar arte, decisões, scripts anteriores e GitHub. Documentar novo adapter em branch/revisão antes de mesclar, mantendo as prioridades do PCRA e a Issue P15 conforme estado verificado.

## 5. Conclusão objetiva

**Resolve:** geografia e geometria permanentes, câmera, iluminação, props, render repetível, cenografia tridimensional, versões de uma mesma cena e automação de programação. **Não resolve sozinho:** rigging/skin, movimento natural de personagem, corpo e contato, roupas/cabelos, animação tradicional de alto nível, roteiro dramático ou IA local fotorealista de 12 minutos. **Grátis em parte:** Blender + Poly Haven + Python; **pago no tutorial:** Claude Code e frequentemente modelagem 3D gerativa. **Rota R$0 da arquitetura:** ChatGPT/PCRA para scripts + Blender local; custos futuros de energia/tempo permanecem.

**Status final:** estudo técnico e comparação com transcrição completa; sem MP4 gerado, script instalado, conexão MCP/Blender/PCRA homologada, render de Aenvarath nem alteração de prioridades.
