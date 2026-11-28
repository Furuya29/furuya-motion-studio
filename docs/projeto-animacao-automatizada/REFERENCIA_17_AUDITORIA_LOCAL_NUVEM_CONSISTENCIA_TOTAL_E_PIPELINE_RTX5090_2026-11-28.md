# Referência 17 — Auditoria local/nuvem das referências e metodologia de continuidade cinematográfica

**Data:** 28/11/2026
**Origem:** pergunta do proprietário sobre todos os vídeos previamente enviados, a existência de IA local e a possibilidade de eliminar deriva de personagem, vestuário, cenários e movimento.
**Estado:** relatório comparativo **DOCUMENTADO** a partir das análises e fontes reabertas; arquitetura proposta sem implementação produtiva nem ensaio visual novo.
**Precedência:** aditivo; NÃO substituir módulos/engines aprovados, arte canônica, prioridades do PCRA, scripts existentes ou os checkpoints narrativos. Não confundir pesquisa, implementação, execução local ou homologação.

## 1. Questão central e resposta baseada em prova

**Nenhuma das obras audiovisuais completas enviadas ao projeto foi demonstrada como criada inteiramente offline em uma única GPU local.** Isso não prova que a geração local não tenha participado: significa que o processo dos autores não foi divulgado de forma verificável.

| Fonte | Verificação já documentada | Local/cloud: classificação correta |
|---|---|---|
| TS Malfoy — Fantasoner / https://youtu.be/WYRDe8XsRmI | Relatório histórico 08/11; ~9min04s e estilo cinematográfico | Modelo, hardware, plataforma e cloud/local **NÃO identificados** |
| Shift Up — Stellar Blade: BLOOD RAIN / “Wanna be in LOVE” | Relatório 08/11; **nova evidência**: porta-voz diz que conteúdo foi reconstruído a partir de assets do jogo com IA em função de apoio. Fonte https://www.gamemeca.com/en/view.php?gid=1778577 | Existe base visual/asset preexistente, não é geração totalmente sem material de referência; GPU específica/cloud/local **NÃO identificados** |
| “Global Cold Doom” AI manhua / https://youtu.be/AZDzT-4OIY8 | Metadados e site; sem filme analisado diretamente | **NÃO identificado** |
| Imperatriz, sistema emocional / https://youtu.be/elGjvl8lJgA | Metadados e script de amostragem preparado, não executado no Windows | **NÃO identificado** |
| Seravienne / https://youtu.be/zCiQGSlRgnY | MP4 1000592192.mp4, 24min41s; 64 stills+5 tiras, CGI/donghua semirrealista aparente | **NÃO identificado**, 3D estético não demonstra render 3D local |
| Wildland Hunters (label do MP4) / 1000591963.mp4 | 4min40s; 47 stills+8 tiras; cenas CGI, acting e efeitos | **NÃO identificado** |
| MatteStudio / https://youtu.be/VuP6gPZ0wAI / MP4 1000596761.mp4 | Canal e série confirmados, EP4 ~69h, autor estimou ₩280–300 mil em créditos de vídeo, excluindo ferramentas prévias; reconheceu drift e retakes | **Geração cobrada por créditos CONFIRMADA; serviço hospedado provável; modelo exato e etapas locais não identificados** |
| Willian IA / https://youtu.be/8DALo_Y2Z4I | Tutorial promete filme local; palavras-chave ComfyUI, MiniMax H3, Blender, etc.; não foi inspecionado workflow integral | **Exemplo local anunciado**, modelo local H3 existente, mas **implementação precisa e hardware no vídeo NÃO comprovados** |
| Tutorial APOB+Seedance / https://youtu.be/xREJGxn0IoM | Plataforma de geração hospedada por créditos; preço do exemplo 5s 1.000 créditos | **Serviço cloud** da demo, não é prova de geração offline |
| Google Flow longo / https://youtu.be/gCsVA9UdcAs | Ferramentas Google Flow por crédito e Tools de assinatura para criar miniapps; opção sem assinatura com limites | **Geração cloud**; montagem pode ser local |
| Perchance / https://youtu.be/hCwhdRIdN20 | Web text-to-image; não é vídeo | **Nuvem para imagens**, não animação |
| Claude/Codex Agent Skills e outros tutoriais / https://youtu.be/N6uTE2p3lgg / https://youtu.be/9a2KZBGzEyg | Orquestração por prompts/scripts | **Local/cloud depende dos renderizadores invocados**, não da skill |

Fontes específicas: [Ref07 Seravienne](REFERENCIA_07_SERAVIENNE_FANTASIA_ELFOS_2026-11-16.md), [Ref08 Wildland](REFERENCIA_08_WILDLAND_HUNTERS_DIRECAO_CINEMATOGRAFICA_2026-11-16.md), [Ref12 Comfy H3](REFERENCIA_12_WILLIAN_IA_FILME_LOCAL_MINIMAX_H3_2026-11-24.md), [Ref15 MP4 MatteStudio](REFERENCIA_15_MALFOID_FILME_12MIN_CONTINUIDADE_PRODUCAO_2026-11-27.md), [Ref16 canal/créditos](REFERENCIA_16_MATTESTUDIO_AUTORIA_CUSTOS_CLOUD_E_ROTA_LOCAL_RTX5090_2026-11-27.md).

## 2. Precisão conceitual: perfeição não equivale a ausência de erro observado

As obras editadas podem parecer impecáveis porque selecionam takes curtos, usam enquadramentos previsíveis, cobrem problemas com cutaways e reações, revisam prop/contact e descartam falhas. **Nenhum gerador probabilístico puro oferece garantia formal de identidade e geometria perfeita em filmagem ilimitada.** O método mais forte é usar estados e geometria **determinísticos** como base e IA de vídeo como opção de aparência, com QA e retake. A Shift Up confirmou reutilização de game assets no MV: https://www.gamemeca.com/en/view.php?gid=1778577.

## 3. Arquitetura de invariantes canônicos — especificação recomendada

### 3.1 Fonte única de verdade, versionada

**character_id** persistente + versão de character bible. Rosto, dimensões normalizadas, paleta e materiais, cabelos e penteado por ID, elementos distintivos, turnaround 4–8 vistas *da mesma geometria*, textura, pesos/rig, expressões e voz. **Aprovado/imutável**; alterações devem ser intencionais, revisadas e versionadas. LoRA pode auxiliar reproduzir a aparência, mas **não garante** anatomia/topologia/perspectiva.

**costume_id + version + state**: roupa específica (vestido/armadura/capa), materiais em PBR, cores, bordados, costuras, capas, manchas/danos, acessórios, ajustes por episódio. Rig de roupa, cloth simulation/skin quando 3D; em 2D, layers e modelos de referência por vista. **Não depender de texto repetido no prompt para garantir roupa idêntica**.

**scene_id + layout_version**: planta de sala/palácio/vila, arquitetura e medidas aprovadas, iluminação, clima, posição de mesas/portas/objetos, direção de luz, pass de profundidade, referências de lente/câmera, cenário de fundo persistente e geografia. Para filmagem 3D/híbrida, construir geometria real e usar composição/mattes para integrar estilo anime ou semirrealismo.

**shot_id + take_id**: personagem, costume, scene, pose/câmera/lente/trajectória/fps/duração, ação dramática, fala/áudio, estado de cada prop no mundo ou na mão, primeiro/último quadro, keyposes e blocking de contato, controle por rig/depth/edge/pose, motor/modelo/pesos/seeds/denoise/config, custos, outputs e hashes. A seed sozinha **não trava** identidade.

**continuity ledger**: cronologia/posição de personagem, roupa e dano, props (mão direita/esquerda, posição na sala, visibilidade e orientação), emoção, olhares, som e iluminação; updated only on approved action/shot. Shot novo **não tem permissão de alterar estado sem evento no roteiro**.

### 3.2 Animação por tomada, método adaptativo A/B/C já decidido

**Nível A — diálogo:** rig facial/olhos/mandíbula/visemas (som PT-BR), olhar, gestos de mãos, postura/respiração, roupas/cabelo secundários; tomadas com cobertura master/medium/close/reaction que preservem geografia. Para naturalidade, não mover só boca: sobrancelha, olhar, pescoço, corpo e gestos **planejados**.

**Nível B — caminhada/manipulação/ação moderada:** animação IK para pés e mãos, *root motion* e contato com chão/objeto, animação 2D tradicional multivista, ou 3D com rig/malha e física; on-model em todo frame. **Uma única imagem frontal distorcida NÃO representa turnaround/perfil/costas**.

**Nível C — combate, asa e voo:** blocking de ações com rigs 3D e trajetórias 3D mensuráveis, animação mecânica/constraints/colisão; em 2D, genga/douga a partir de várias vistas; IA condicionada por pose+depth+normals+occlusion+control video apenas onde complementa. Asas possuem pivôs/implantação/faces, animação de ossos/penas e interação com capa/torso; não animar asa como efeito genérico colado.

### 3.3 Pipeline local de alta consistência

1. **Previs/animatic tecnicamente sólido:** storyboard + layout 3D ou poses 2D multivista + câmeras aprovadas; primeiro validar história/ação.
2. **Animação base determinística:** rigs/blendshapes/IK para atores, props e roupa; cenários 3D persistentes; 2D com intervalação desenhada/geometria correta; render base.
3. **Guia de geração por frame (opcional):** render poses, depth, masks, segmentation, normals, canny e imagens-chave aprovadas; IA vídeo usa I2V, first/last frame, motion-control e/ou stylization; preservar a coerência do controlador, sem aceitar improvisos visuais fora do cânone.
4. **Composição de passes:** personagem/fundo/props/efeitos isolados; máscaras e oclusão; luz da magia afeta superfícies; render correções localizadas (face, mão, prop) onde possível.
5. **QA:** revisar sequência temporal 100% do produto aprovado para erros grandes e amostrar métricas automáticas para todas as tomadas; comparar identidade/face embedding, silhueta, bordado/coroa, cores, landmarks de mãos/pés, pés travados, contato mão-objeto, depth/occlusion, câmera, corte, lip-sync, flicker/optical flow e estados do ledger.
6. **Gate de decisão:** render/take rejeitado gera relatório com timestamp, severidade, evidência e proposta de patch; só permitir merge/export de shot aceito. Não afinar manualmente uma imagem canônica para “mascarar” erro entre cenas.
7. **Edição narrativa:** cobertura e raccord, som, SFX, gradação e export via FFmpeg/Kdenlive/Remotion. Montagem pode esconder transições difíceis, mas a ação relevante da narrativa deve permanecer realmente animada.

## 4. Modelos locais com CONTROLE REAL (fontes oficiais atualizadas)

- **LTX-2.3 em ComfyUI:** templates oficiais para text-to-video, image-to-video, First/Last Frame, image+audio-to-video (lip sync), **IC-LoRA pose/depth/edges** e **ID-LoRA**. Controle estrutural depende de frames de controle alinhados; pode reduzir deriva, mas não garantir invariantes geométricos. Fonte: https://github.com/Comfy-Org/docs/blob/main/tutorials/video/ltx/ltx-2-3.mdx.
- **Wan2.2 Animate 14B:** modo `Move` transfere movimento de vídeo de controle para personagem em imagem; modo `Mix` substitui personagem no vídeo; suporte a extração de pose por DWPose e guias de expressão. Fonte: https://github.com/Comfy-Org/docs/blob/main/tutorials/video/wan/wan2-2-animate.mdx e https://github.com/Wan-Video/Wan2.2. **Não** afirmar que movimentos ficam perfeitos automaticamente; mãos/oclusão/perspectiva podem falhar.
- **LTX Desktop (Lightricks) local:** https://github.com/Lightricks/LTX-Desktop. Recomenda Windows NVIDIA com **24GB+ VRAM (32GB preferidos), 64GB RAM e NVMe**; 32GB RAM é possível com modelo no NVMe para todos os tools conforme documentação. Modelos 2.5 Fast/2.3 Fast locais; variantes 2.5 Pro/2.3 Pro **API-only**. Exige licença adequada para uso autoral/comercial, inclusive para pesos com termos comunitários.
- **HunyuanVideo-1.5:** modelo local que anuncia mínimo de **14GB VRAM com offload**, conforme https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5. Não confundir com HunyuanVideo clássico que requer VRAM bem maior.
- **RTX 5090:** 32GB GDDR7, TGP 575W; fonte de sistema dimensionada para 1000W recomendados pela NVIDIA (varia com CPU/periféricos). https://www.nvidia.com/pt-br/geforce/graphics-cards/50-series/rtx-5090/. GPU excelente para modelos quantizados/filmes curtos, mas não transforma filmagem contínua de 12–25 min em tarefa de um único prompt.
- **Outros componentes que continuam centrais:** Blender (rig/IK/constraints/simulação/câmera), Krita, OpenToonz, Godot, FFmpeg, Kdenlive/MLT, Python, Remotion e automação PCRA comprovada.

## 5. O que torna aparência realmente estável: a hierarquia de confiança

| Nível de controle | Benefício | Limitação |
|---|---|---|
| Só prompt + seed | Repetição aproximada | Muita deriva, sobretudo ângulos/figurino |
| Referências e image-to-video | Melhora identidade e composição no início do clip | Deriva temporal e cross-shot ainda possível |
| LoRA/ID-LoRA + refs multivista | Melhora semelhança de rosto/roupa e identidade no domínio do modelo | Não trava física/rig/cenário/topologia |
| Pose/depth/edges + multi-keyframe | Reduz ambiguidade de movimento e enquadramento | Movimento complexo e contato ainda podem falhar |
| **Rig/malha/cena/câmera determinística + render e controle** | Preserva geometria/topologia/estado do mundo; pode impedir alteração real de roupas/props | Exige modelagem/animador ou geração de assets, render e tempo |
| QA temporal + revisão + retake local | Mantém qualidade no vídeo aprovado | Consome tempo, não garante perfeição universal em futuro clipe |

Não existe algoritmo que certifique automaticamente que toda arte está perfeita. Métricas de similaridade facial ou correspondência óptica **não substituem revisão artística humana**.

## 6. Critério de validação progressiva de Aenvarath

**Sem criar cena genérica que não será reutilizada:**
- Selecionar quadro narrativo real autorizado da sequência de Nólyrien, com personagem/costume/cenário e posições canônicas existentes.
- Criar **mesma personagem** em dois enquadramentos (frente / 3/4 ou costas já aprovada) e pelo menos uma ação corporal genuína de 2–5s; usar duas tomadas consecutivas com raccord de cabeça/mão/figurino/ambiente.
- Para a asa, preservar **implantação lombar, face dorsal, geometria da torre perfeitamente circular, coroa vista atrás** e movimentos de voo.
- Exigir fonte, MP4, frames de prova, receita de render, checksum, logs CPU/RAM/VRAM, revisão de identidade/roupa/câmera/contato e aceite humano.
- Com o PC atual, priorizar especificações/rigs/arte/preview leve e evitar projetos GPU CUDA pesados; com futuro hardware NVIDIA, comparar **LTX-2.3/2.5 local, Wan2.2 Animate e HunyuanVideo-1.5** em mesma tomada e sem assumir direitos comerciais irrestritos.
- Não remover ou trocar o pipeline já decidido; implementar controles em adaptadores à arquitetura.

**Conclusão:** ninguém provou que os melhores filmes enviados foram todos feitos offline. O caminho mais preciso para *resultados de aparência profissional consistentemente alta* é **controle determinístico de assets, movimento e cena + IA visual condicionada + comp + QA obrigatório**. A futura 5090 acelera esse desenho sem reconstruir o estúdio.
