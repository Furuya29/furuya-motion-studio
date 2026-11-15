# P0 — ComfyArt, CreativeField e a alternativa aberta ao Higgsfield (15/11/2026)

## Origem e escopo

Vídeo de referência do usuário: [“A 'NOVA' ComfyUI humilhou o Higgsfield (e é de graça)”](https://youtu.be/ddirEBVYVno), canal Willian IA. O título e o tema foram verificados por metadados públicos; **a reprodução/transcrição integral do vídeo não foi inspecionada**. As conclusões operacionais abaixo usam os repositórios dos autores e o estado atual do Furuya, e não demonstram que a ferramenta foi executada no PC do usuário.

- [ComfyArt oficial](https://github.com/jtydhr88/ComfyArt)
- [CreativeField oficial](https://github.com/rhymeas/Creativefield)
- [OpenJutsu já integrado como adaptador no Furuya](https://github.com/D3voz/openjutsu)
- [Resultado oficial do desafio #OpenSourceHiggsfield](https://comfy.org/open-source-higgsfield)

## Achado decisivo

**ComfyArt e CreativeField são interfaces/orquestradores sobre ComfyUI, e não motores autônomos de inferência.** “Código aberto/gratuito” não é garantia de GPU em nuvem grátis, de pesos compatíveis com a máquina atual ou de substituição perfeita de personagens. Não registrá-los como motores em `cloud/engine_registry.py` nem permitir que apareçam como resposta do roteador para o vídeo dos cinco dançarinos.

| Projeto | Potencial reutilizável | Limite operacional e econômico | Estado no Furuya |
|---|---|---|---|
| ComfyArt (MIT) | Canvas, referências, ativos, storyboards, interface visual e execução em ComfyUI próprio | Sua documentação diz que Comfy Cloud requer plano pago; vídeo depende de modelo e backend compatíveis. Não comprovou recast quadro a quadro. | Pesquisa; não instalado |
| CreativeField (GPL-3.0) | Painéis integrados de vídeo, imagem, máscara e workflows; experimentos com OpenJutsu/SAM | README relata desenvolvimento/teste em RTX 4090, 64 GB RAM; substituição de personagem ainda experimental. Rota Comfy Router utiliza créditos, gratuidade não verificada. | Pesquisa; não instalado |
| OpenJutsu Advanced | Rastreamento SAM 3.1 e associação de até quatro papéis; já possui adaptador Furuya | Inferência MiniMax H3/ComfyUI não homologada no hardware do usuário; cinco alvos numa passagem não foram validados | Candidato prioritário, sem GPU grátis verificada |

## Compatibilidade e custo — proibições

- Máquina do proprietário: Windows 10 Pro, AMD FX-4300, ~16 GB RAM, Radeon RX 580 8 GB. **Não existe evidência de execução real dos workflows MiniMax H3/SAM 3.1 nesse ambiente.** O uso de ComfyUI em CPU é tecnicamente diferente de renderizar modelos grandes com qualidade e velocidade aceitáveis.
- Não instalar frontends por padrão, não baixar modelos enormes, não mudar dependências/versões do PCRA, não contratar nuvem, não criar API keys pagas, não ativar Comfy Router/Comfy Cloud com cobrança.
- CreativeField GPL-3.0: eventual incorporação de código exige análise de obrigações de licença. Preferir integração por protocolo/links configuráveis, sem copiar código do aplicativo.
- As interfaces opcionais jamais devem remover ou renomear os 11 motores catalogados, desviar o roteador automático, promover Flow para recast fiel, nem afirmar que uma página demonstra capacidade de inferência.

## Próximo piloto verificável, orçamento R$0

1. Manter fonte **3,00 s**, original da festa, e a referência 3D aprovada da **Albedo**, sem refazer os outros PNGs.
2. Quando houver um backend ComfyUI com pesos, nós e VRAM **verificados e gratuitos**, realizar diagnóstico prévio somente leitura e associar o dançarino central ao rastreamento/máscara temporal. A opção de frontend é secundária: usar o adaptador OpenJutsu que já existe.
3. Executar **uma** troca corporal gerativa com duração/ritmo/câmera preservados; comparar quadro a quadro as regiões externas à máscara, dança, mãos/pés, oclusões e identidade.
4. Falha em qualquer gate → não promover/homologar. Somente depois organizar passagens por alvo (até cinco) e composição determinística, mantendo espectadores intactos.
5. Na ausência de GPU grátis comprovada, permitir apenas **preparação, prévia por CPU e validação offline**; não anunciar MP4 final.

Critérios de aceite: mesmo número de quadros após normalização de fps, movimento e enquadramento equivalentes, espectadores fora da máscara inalterados, nenhuma pessoa extra, sem alteração involuntária do áudio, sem marcas de personagem rígido. Qualquer duração nova, coreografia substituída ou mudança de fundo reprova.

## Integração adicionada nesta branch

`frontend-catalog.json` registra essas interfaces em categoria separada, marcada `RESEARCH_ONLY`, com `eligible_for_auto_router=false`, `free_gpu_verified=false`, `can_generate_now=false`, `paid_fallback_allowed=false`. `tests/test_frontend_catalog.py` verifica esses guardrails e a manutenção do roteador (1 pessoa → OpenJutsu só para avaliação; 5 → ausência de motor de uma passagem).

Nenhuma instalação, geração, download de modelos, autorização de crédito ou teste GPU foi realizado. A documentação identifica opções sem as promover a recursos homologados.
