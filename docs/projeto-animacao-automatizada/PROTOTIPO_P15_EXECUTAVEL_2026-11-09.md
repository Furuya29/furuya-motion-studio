# P15 — protótipo executável de blocking (09/11/2026)

> **Status:** renderização demonstrativa executada em ambiente isolado de desenvolvimento, **não no Windows do proprietário**. Não é produção artística, homologação do piloto #12, validação de lip-sync nem contato físico real. Não inclui a geração dos desenhos-chave originais.

## Escopo

O renderizador `tools/animation_pilot/preview_animatic.py` interpreta `piloto_15s_shot_spec_v0_1.json`, consulta a pré-validação estrutural existente e transforma 360 amostras temporais em quadros rasterizados e MP4:

- Plano A (frames 0–119): figura geométrica com piscadas, boca e respiração/gesto paramétricos; **não sincronizado com áudio**.
- Plano B (frames 120–239): deslocamento e câmera com chaves em coordenadas do mundo; marcha **esquemática**, sem ciclo de caminhada artisticamente aprovado nem pé travado por IK.
- Plano C (frames 240–359): câmera em arco; microfone fixo no mundo com facetas projetadas em perspectiva; proximidade da mão **não certifica** contato ou oclusão corretos.

A animação usa coordenadas 3D para bloqueio de cena e figuras geométricas 2D para visualizar. Os olhos/boca são desenhos simplificados. A câmera funciona com transformação *look-at*; os efeitos de cena não implicam reconstrução física de objetos nem visão multivista real de personagem.

**Importante:** o personagem gráfico é um marcador técnico propositalmente simples. A qualidade de anime 2D depende de camadas, model sheets, rigs, poses/arte original e revisão.

## Pré-requisitos locais

- Python 3.10 ou mais recente.
- Pillow (biblioteca de imagem gratuita).
- FFmpeg no `PATH`.
- Python padrão também executa o validador estrutural; o renderizador requer Pillow.

Em um ambiente Python virtual, instalar apenas a dependência do POC:

```powershell
python -m pip install Pillow
python -m unittest discover -s tests -p "test_animation_pilot_spec.py" -v
python -m unittest discover -s tests -p "test_animatic_preview.py" -v
python tools/animation_pilot/preview_animatic.py --out preview_p15.mp4 --width 640 --height 360
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,nb_frames,r_frame_rate -show_entries format=duration,size -of json preview_p15.mp4
```

**Não executar automaticamente no PC:** exigir inventário prévio de Python/FFmpeg/Pillow/PCRA, validar diretórios de saída e testar uso de CPU/RAM antes de render em 1080p.

## Verificações realizadas nesta conversa

- Em ambiente isolado, uma versão funcional equivalente do renderizador criou um arquivo MP4 de **15,000 s**, **640×360**, **24 fps**, **360 quadros** (FFprobe).
- Testes locais de câmera, continuidade de tomadas e determinismo de render passaram (4 testes). A versão copiada ao GitHub exige execução de CI ou teste local antes de promover o PR.
- A renderização local tem quadros geométricos sem áudio. A revisão visual desses quadros **não é aprovação artística**.
- Não foi lido ou escrito nenhum arquivo no Windows do usuário; o PC Remote Agent não foi acionado.

## Limitações explícitas

1. Personagem ainda é um rig ilustrativo por primitivas 2D, não model sheet ou anime autoral.
2. Visemas não estão alinhados à voz: o movimento de boca é periódico e meramente demonstrativo.
3. Mãos/pés não passam por solver de IK/contact QA.
4. Cenário é grade geométrica, não cenário persistente artístico definitivo.
5. Renderizador não é um adapter de OpenToonz, Godot, Blender, Inochi2D, Remotion ou Premiere.
6. Não foram medidos CPU/RAM/VRAM do desktop FX-4300/RX 580.

## Próxima entrega de engenharia sugerida (sem inverter prioridades)

- Integrar **Asset & Character Consistency Engine** com um personagem original de múltiplas vistas/camadas e uma bíblia de proporções.
- Substituir figura geométrica por desenhos aprovados, controlar visemas com áudio e aplicar rigs onde útil.
- Introduzir FK/IK, contato de pés/mãos e máscaras de oclusão de objetos.
- Executar no PCRA após validar autorização e endpoint produtivo; registrar recibos e timings; realizar QA completo do piloto antes de marcar qualquer checkbox na Issue #12.

## Referências

- [Contexto mestre](CONTEXTO_MESTRE.md)
- [Reconciliação cumulativa](RECONCILIACAO_ADITIVA_2026-11-09.md)
- [Issue #12](https://github.com/Furuya29/furuya-motion-studio/issues/12)
