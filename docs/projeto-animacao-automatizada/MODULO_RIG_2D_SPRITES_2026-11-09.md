# Núcleo experimental — Rig 2D por sprites, FK e troca de desenhos (09/11/2026)

> Prova técnica de animação determinística de **PNG em camadas** para o Estúdio de Animação e Cinemáticas. Implementação em branch de revisão (PR #13). Não equivale à automação do OpenToonz/Krita/Blender, à produção de anime final nem à homologação do piloto cinematográfico da Issue #12.

## O que já está em código

- **Composição de camadas PNG RGBA**: cada imagem permanece intacta; não se gera novo desenho com IA.
- **Hierarquia FK**: filho herda transformações do osso/junta pai, com pivot, offset, rotação e escala.
- **Keyframes temporais**: interpolação numérica e canais de deslocamento, escala e rotação.
- **Troca discreta de desenhos**: `sprite` por frame, adequada a olho aberto/fechado, boca aberta/fechada e futuras bibliotecas de visemas.
- **Renderização por FFmpeg**: quadros em memória transmitidos diretamente ao encoder, sem armazenar milhares de PNGs temporários.
- **Restrições de integridade**: ciclos de pais, IDs repetidos, caminhos de sprite que escapam do diretório do rig e escalas inválidas são sinalizados.
- **Demonstração sem mídias de terceiros**: `make_sprite_demo.py` cria suas próprias imagens geométricas e um rig de 72 frames a 24 fps.

### Como executar após validar dependências (Python com Pillow + FFmpeg)
```powershell
python tools/animation_pilot/make_sprite_demo.py --out exemplo_sprite
python -m unittest discover -s tests -p "test_sprite_rig.py" -v
python tools/animation_pilot/sprite_rig.py --rig exemplo_sprite/rig.json --out exemplo_sprite/preview.mp4
```

O `rig.json` aponta para PNGs originais relativos ao seu diretório. Trocar a arte de exemplo por *character sheets* oficiais requer que cada recorte tenha transparência, posição do pivô e hierarquia de articulação aprovadas.

## Contrato v0.1

```json
{
  "version": "sprite-rig/0.1",
  "canvas": [640, 360],
  "fps": 24,
  "frames": 72,
  "parts": [
    {
      "id": "head",
      "sprite": "assets/head.png",
      "parent": "torso",
      "pivot": [70, 112],
      "offset": [0, -67],
      "layer": 2
    }
  ],
  "tracks": [
    {
      "part": "head",
      "property": "rotation_deg",
      "keys": [{"frame": 0, "value": 0}, {"frame": 35, "value": 4}]
    }
  ]
}
```

O exemplo acima ilustra apenas uma parte do rig; para executar é necessário incluir os pais, demais camadas e PNGs correspondentes.

## Limites relevantes para nosso objetivo

- Não implementa deformação de malha, plastic tool, inversa cinemática (IK), *foot locking*, colisão, auto-rigging ou geração de inbetweens.
- **Não cria personagens nem vistas não desenhadas**. Fala animada por trocas de boca não equivale a lip-sync fonético sincronizado.
- Não certifica anatomia, proporção, expressividade ou continuidade entre ângulos diferentes. Cenas complexas exigem outros métodos já aprovados (OpenToonz, Blender, key drawings etc.).
- A implementação inicial compõe o canvas inteiro por sprite. Para Full HD e hardware modesto, otimizar retângulos locais, cache, resolução de preview e uso de memória antes da implantação.
- Testes em ambiente isolado **não comprovam instalação, desempenho ou funcionamento no Windows do usuário via PCRA**.

## Próxima integração proposta

1. Substituir sprites geométricos por PNGs **autoriais aprovados**, incluindo frente, perfil e 3/4.
2. Adaptar a anatomia do rig para pivôs de ombro, cotovelo, pescoço e quadril; implementar IK apenas quando tecnicamente necessário.
3. Criar bibliotecas de visemas, piscar, respiração, ciclo de marcha e poses. Vincular lip-sync ao áudio real.
4. Desenvolver bridges documentadas para OpenToonz (Xsheet/Plastic) e Blender/Grease Pencil sem substituir os editores.
5. Adicionar QA visual e continuidade espacial antes de tratar personagem animado como arte final.

**Regra de continuidade:** este motor é uma opção adicional ao multimétodo, não o motor único do estúdio. Não altera prioridades ou checkboxes do piloto da Issue #12.
