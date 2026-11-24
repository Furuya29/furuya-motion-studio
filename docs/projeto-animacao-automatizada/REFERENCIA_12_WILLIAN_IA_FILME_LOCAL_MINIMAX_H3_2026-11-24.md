# Referência 12 — Willian IA: produção de filme no PC com ferramentas gratuitas / MiniMax H3

**Data da triagem:** 24/11/2026.  
**Fonte enviada pelo proprietário:** https://youtu.be/8DALo_Y2Z4I?is=Fru11L2m0S7SIrOn  
**Título público da página:** “Não Gaste Dinheiro com IA: fiz um FILME 100% Grátis no PC (Passo a Passo)”.  
**Canal atribuído por índice externo:** Willian IA — https://zolotube.com/channel?id=UCeh-h2oateK3IBBT7hSK6Zw  
**Duração indexada do vídeo:** 35min41s.  
**Evidência inspecionada:** página/keywords do YouTube e documentação oficial de ComfyUI e MiniMax H3, mais relato de hardware de fontes secundárias. **A reprodução integral do vídeo, transcrição detalhada e quadros em sequência NÃO foram acessados.** Não atribuir ao autor procedimentos que só aparecem nas keywords.

## 0. Continuidade e preservação

Esta é uma atualização **cumulativa RESEARCH_ONLY**, não uma nova arquitetura, instalação, render, mudança de prioridade ou homologação artística. O Estúdio de Animação e Cinemáticas de Aenvarath permanece **multimétodo por tomada**, com key drawings e inbetweens, rigs 2D/3D, composição, cenário persistente, QA de atuação/câmera/contato e supervisão humana. **Motion Comic não é método principal, etapa obrigatória nem entrega final**. Não substituir imagens, personagens ou frames aprovados. A integração via PCRA continua dependente de execução produtiva demonstrada, não de conectores sintéticos ou status.

Referências de continuidade:
- [ARQUITETURA_CONSOLIDADA_MEGA_ESTUDIO_ANIMACAO_2026-11-16.md](ARQUITETURA_CONSOLIDADA_MEGA_ESTUDIO_ANIMACAO_2026-11-16.md)
- [CONTEXTO_MESTRE.md](CONTEXTO_MESTRE.md)
- [REFERENCIA_09_APOB_SEEDANCE_25_CINEMA_2026-11-18.md](REFERENCIA_09_APOB_SEEDANCE_25_CINEMA_2026-11-18.md)
- [REFERENCIA_10_VIDEOS_IA_GRATUITOS_GOOGLE_EVERYPIXEL_VIDOGRID_FREEBEAT_2026-11-20.md](REFERENCIA_10_VIDEOS_IA_GRATUITOS_GOOGLE_EVERYPIXEL_VIDOGRID_FREEBEAT_2026-11-20.md)
- [Issue #12](https://github.com/Furuya29/furuya-motion-studio/issues/12) e [PR #13](https://github.com/Furuya29/furuya-motion-studio/pull/13).

## 1. Conteúdo verificável do vídeo e limites

A página original identifica a promessa de criação de filme “100% grátis no PC (passo a passo)”. Keywords públicas incluem:
MiniMax H3, ComfyUI, IA local, vídeo longo, multitrack, Pika LoRA / H3, Qwen Image Edit, Krea 2, Blender, Claude/skills e Seedance. **Keywords = indícios de temas, NÃO prova de que o autor tenha utilizado todos esses componentes**. A descrição inicialmente extraída destaca também propaganda de cursos/pacotes próprios, não um contrato técnico detalhado de software e hardware.

Página do canal indexa duração **35:41** e título. O computador exato do criador, versão do workflow, modelo, quantização, arquivos utilizados, consumo VRAM/RAM, tempo de render, sequência de cenas, custo total, licenças e qualidade temporal do curta **NÃO foram verificados**. Não afirmar que o fluxo roda em GPU Radeon RX 580, nem que criou cinema autoral completo ou animação por rigs.

## 2. O que foi verificado diretamente nos fabricantes

### ComfyUI + MiniMax H3

Documentação primária: https://docs.comfy.org/tutorials/video/minimax/minimax-h3

- O H3 é um modelo com **pesos abertos sob licença comunitária própria**, e possui integração com ComfyUI para texto→vídeo, imagem→vídeo e referências→vídeo.
- Suporte anunciado para som estéreo nativo (fala/efeitos/música); até ~15 s e 24 fps por geração com os pesos locais em ~768 px de lado curto; qualidade 2K hospedada não é prova de 2K local na mesma configuração.
- ComfyUI lista templates T2V, I2V, R2V, multiframe reference e Fun ControlNet Union. Este último pode condicionar movimento por **pose, depth, canny/edges** e suportar inpainting de vídeo. Esses controles são tecnicamente relevantes para Aenvarath, mas os requisitos são maiores do que simples geração a partir de texto.
- O modelo original e os arquivos empacotados estão em https://huggingface.co/MiniMaxAI/MiniMax-H3 e https://huggingface.co/Comfy-Org/MiniMax-H3.
- O desenvolvedor do ComfyUI afirma explicitamente que **uso comercial de outputs produzidos localmente requer licença comercial MiniMax via Comfy**; gerações Comfy Cloud incluem direitos comerciais segundo a página, mas Comfy Cloud **não foi comprovado gratuito**. Não assumir que “pesos grátis” autoriza publicar/anunciar/monetizar episódios ou trailers do MMORPG.
- Licença do modelo original: https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE (Community License, não licença permissiva genérica; inclui restrições territoriais — EUA, UE, UK e Coreia do Sul são excluídos na licença consultada. Brasil não consta nos territórios excluídos, mas o uso deve obedecer às demais obrigações).
- Não confundir termos dos componentes auxiliares, LoRAs ou código aberto com direitos sobre pesos e outputs do modelo principal.

### Recursos mínimos e realidade do PC

Computador conhecido: **Windows 10 Pro, AMD FX-4300, ~16 GB RAM, Radeon RX 580 8 GB**.

Relato técnico comparativo: https://nuvalab.ai/blog/run-minimax-h3-locally-gpu-vram-requirements/

- MiniMax H3 modelo pleno possui dezenas de bilhões de parâmetros. Configuração ComfyUI reduzida documentada usa ~42,5 GB de arquivos de modelos na quantização estudada (transformer+encoder+VAEs), e diversas configurações de inferência demandam **GPU NVIDIA CUDA + VRAM e RAM** mais elevadas.
- Receita de consumo para o H3 base: em torno de **12 GB VRAM + 32 GB RAM** na referência citada; full precision é muito mais pesado.
- Existe ajuste experimental **FastH3 Trim** relatado em 8 GB VRAM/480p, porém os benchmarks citados foram feitos em **RTX 4090 com memória artificialmente limitada a 8 GB**, não na RX 580, e a RAM necessária naquele caminho não estava especificada.
- A RX 580 8 GB (AMD Polaris) **não ganha suporte CUDA** por possuir 8 GB VRAM; versões/complementos CUDA/INT8 não podem ser supostos compatíveis; o FX-4300 com 16 GB RAM aumenta risco de swapping, lentidão, OOM e incompatibilidade.
- **Não é possível concluir que H3 executa viavelmente no PC existente sem validar backend AMD/CPU, quantização, dependências, RAM, licencia, tempo e qualidade**. Dado o estado da arte, **não recomendar a instalação de dezenas de GB de pesos no PC como próxima etapa** antes da triagem.
- Mesmo modelos menores/recortados publicitados em 2026 precisam de benchmark **na RX 580 real**, não se pode assumir paridade por capacidade nominal de VRAM.

## 3. Matriz com a arquitetura de Aenvarath

| Ideia | Situação | Decisão documental |
|---|---|---|
| ComfyUI como gerenciador de modelos de vídeo | Já previsto / explorado no estúdio conexo | Preservar; avaliar uso como *adapter* secundário |
| MiniMax H3 com referências de personagem/voz | Candidato externo com documentação oficial | Pesquisa de engine, não elegível ao auto-route até recursos/termos e QA |
| Pose/depth/inpainting como controle do vídeo | Complemento técnico de interesse | Analisar como possível ponte entre blocking 3D/rig e IA, não substituir blocking |
| Roteiro/shot list, filmagem por tomadas e edição | Já decidido na arquitetura original | Reutilizar shot spec, cinematic composition e QA existentes |
| Vídeo “grátis” local | Pesos disponíveis; custo de API potencialmente zero | Não confundir com suporte GPU, energia, licença comercial ou ausência de custo/tempo |
| Compatibilidade RX 580 8 GB, RAM 16 GB | **Não comprovada**; GPU AMD sem CUDA | Bloquear instalação produtiva e qualquer alegação de execução viável até prova local |
| Produção comercial de Aenvarath / monetização | Exige clareza jurídica | Verificar licença comercial antes de usar outputs |
| Nólyrien com asas/voo e continuidade de palácio | Cânone e checkpoint prévios | Preservar; nunca regenerar automaticamente quadros aprovados |
| Motor de animação completo do estúdio | Ainda não homologado | Não alegar que H3, ComfyUI ou o tutorial o concluem |

## 4. Encaminhamento eficiente e sem reconstrução

1. **Não instalar agora o H3 ou sua pilha CUDA no PC sem pré-voo**; nenhuma execução real no PCRA foi conduzida nesta referência.
2. Buscar o workflow **exato** (versão e download oficial) e o hardware usado no tutorial, se a transcrição/descrição completa ficar acessível. Separar componentes genuinamente locais de eventuais serviços de nuvem, propaganda ou pacotes vendidos.
3. Catalogar H3 como **RESEARCH_ONLY / local_hardware_unverified / commercial_license_pending / autoroute_disabled / paid_fallback_disabled**.
4. Preservar o pipeline principal da animação: **keyframes e rigs**, desenho de vistas corretas, intervalação, 3D persistente, composição por FFmpeg/editores e QA temporal/cross-shot; geração de vídeo como rota adicional se passar gates.
5. Quando o PCRA produtivo estiver pronto, fazer inventário autorizado de programas/VRAM/driver/versões/backend sem baixar modelos gigantes; buscar um motor menor e licitamente utilizável que suporte o hardware, se necessário.
6. Testar com **2–5 s de personagem original com movimento corporal verificável**, fontes, MP4, FFprobe, RAM/VRAM/custo, QA e aprovação artística; continuar cenas já aprovadas sem reinício.
7. Não modificar prioridades da fila PCRA nem mesclar PR #13 automaticamente.

**Conclusão:** a possibilidade de gerar vídeos localmente usando pesos abertos é real para hardware compatível, mas o tutorial não comprova execução local sustentável no **Windows + RX580 + 16GB** do proprietário; a licença comercial do MiniMax H3 requer verificação/licenciamento adicional. Nenhum filme ou instalação foi realizado neste chat.
