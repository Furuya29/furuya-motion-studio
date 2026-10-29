# Furuya Motion Studio — Plano zero orçamento para geração video-to-video

## Atualização P0 em 29/10/2026 — Rota oficial Viggle V1 Video Remix (sem GPU local)

A API Viggle V1 agora é o primeiro candidato de teste **programático** de 3 segundos. Novo adaptador: `cloud/viggle_remix_api.py`. Ele recebe uma PNG da Albedo e o `driving.mp4`, usa `background_mode=original` e solicita 1 personagem por vez. **Não exige** `repainted-ref.png` para esse endpoint de Remix; o quadro retocado continua obrigatório para o motor aberto Viggle-Animate em separado.

O provedor documenta 100 créditos gratuitos **para novas contas**, custo de cerca de 1 crédito por segundo de Remix e consulta gratuita `GET /v1/credits`. O adaptador só faz upload após `--execute`, precisa de `VIGGLE_API_KEY` em variável de ambiente local, consulta o saldo, não compra créditos, não usa GPU paga e não tenta reenviar automaticamente pedidos incertos. Em caso de erro após a submissão, utilize o `render_id` com `--resume-id` para consultar o trabalho existente. O saldo pode incluir créditos comprados, e o adaptador não consegue distinguir sua origem: não execute se seu objetivo é preservar um saldo previamente adquirido. **Não coloque a API key no GitHub Pages, no JS público, em issues ou no chat.**

```bash
python cloud/viggle_remix_api.py --image albedo_original.png --video driving.mp4 --output albedo_3s.mp4
# Em ambiente próprio, com a variável VIGGLE_API_KEY definida e saldo conferido:
python cloud/viggle_remix_api.py --image albedo_original.png --video driving.mp4 --output albedo_3s.mp4 --execute
# Somente para recuperar um trabalho já submetido, sem cobrar outro:
python cloud/viggle_remix_api.py --image albedo_original.png --video driving.mp4 --output albedo_3s.mp4 --execute --resume-id render_SEU_ID
```

A API específica Viggle-Animate (`/v1/videos`) exige pelo menos 5 s de vídeo de movimento nos modos normais, portanto **não corresponde ao clipe de 3 s**. O Remix usa `/v1/renders` e é o candidato inicial para esse trecho; a fidelidade à Albedo e a manutenção da multidão precisam ser avaliadas no arquivo MP4 resultante. Nenhum render real foi feito na preparação desta integração.

Documentação: https://docs.viggle.ai/v1/guides/quickstart-mix · https://docs.viggle.ai/v1/pricing · https://docs.viggle.ai/v1/api-reference/credits

---

Verificado: 2026-10-28. Objetivo: substituição da pessoa **inteira** (corpo, cabelo, rosto, roupas, acessórios), não só face swap.

## Implantação v0.8 — arquivos e pontos de entrada confirmados

- Interface de preparação principal: https://furuya29.github.io/furuya-motion-studio/recast.html?v=0.8
- `recast.js`: editor **sem MediaPipe**, várias pessoas, máscaras e referências temporais independentes, importação/exportação de projeto JSON `furuya-recast-project/0.8`.
- `tools/prepare_clip.py`: prepara clipe H.264 24 fps `driving.mp4`, quadro do mesmo clipe `source-ref.png` e, se um quadro totalmente retocado tiver sido fornecido, `repainted-ref.png`. Usa FFmpeg já disponível; por padrão NÃO executa (dry-run).
- `cloud/viggle_inference.py`: adaptador do `inference/sample.py` oficial; aponta para checkout e checkpoints existentes. Sem download, GPU, pagamento ou inferência a menos que `--execute` seja solicitado.
- Testes CI: `tests/recast_smoke.mjs`, `tests/test_prepare_clip.py`, `tests/test_viggle_adapter.py`; compilação sintática Python e JavaScript. GitHub Actions em `.github/workflows/validate-recast.yml`.
- Space público oficial [Viggle-Animate ZeroGPU](https://huggingface.co/spaces/Viggle/viggle-animate) estava marcado **Running on Zero** em 2026-10-28. Isso só confirma a disponibilidade pública da interface, **não** confirma que a quota Free completará o render do usuário. O uso envia vídeo e imagem ao provedor; é totalmente opcional.
- **Sem teste final de inferência até esta data**. Não declarar que o fluxo IA está pronto ou que múltiplas pessoas terão fidelidade perfeita.

### Preparação por CPU sem pagamento

```bash
python tools/prepare_clip.py --project furuya-projeto-recasting.json --video original.mp4 --outdir pasta_saida --repaint quadro_final_retocado.png
# Se a validação estiver correta e FFmpeg já estiver instalado:
python tools/prepare_clip.py --project furuya-projeto-recasting.json --video original.mp4 --outdir pasta_saida --repaint quadro_final_retocado.png --execute
```

### Adaptador de inferência (somente onde modelo e GPU já existirem)

```bash
python cloud/viggle_inference.py --checkout /caminho/Viggle-Animate --model-dir /caminho/MiniMax-H3 --video pasta_saida/driving.mp4 --repaint pasta_saida/repainted-ref.png --output resultado.mp4
# Somente em ambiente previamente validado, adicione --execute; pode exigir >=96GB VRAM.
```

Para o teste generativo real, verificar antes consentimento e direitos de uso dos vídeos, licença de pesos, armazenamento e franquias do ambiente.

---

## Estado real implementado

- **v0.7 local no navegador**: `recast.html` + `recast.js`.
- Importe vídeo real e **múltiplas referências de personagens**; defina segmento de 3/5/8 segundos.
- Busque quadro no vídeo, marque manualmente o contorno da pessoa com toques, desenhe uma sobreposição provisória e importe o **quadro definitivo retocado**.
- Exporte quadro original PNG, rascunho PNG, máscara por pessoa PNG, quadro retocado PNG, projeto JSON e (se o navegador suportar) vídeo-base recortado WebM sem áudio.
- O editor não envia arquivos a servidores, não executa modelos de vídeo e **não usa o JSON MediaPipe**. A sobreposição é um rascunho, não uma alteração generativa do corpo.
- Para Viggle-Animate, o requisito crítico é um quadro da **mesma tomada**, já retocado para mostrar o personagem substituindo completamente a pessoa, com pose e cenário alinhados. Mesmo uma PNG colocada por cima do ator pode não ser suficiente para garantir boa propagação temporal.
- O projeto não integra nem ativa um provedor externo automaticamente.

## Critérios de teste zero custo antes de qualquer download enorme

Passo 1: `python cloud/free_gpu_preflight.py --workdir . --project furuya-projeto-recasting.json`, em Python local/Colab/Kaggle. Essa análise é somente leitura, sem instalar bibliotecas, baixar pesos, iniciar GPU ou gerar cobranças. Use a saída como **triagem**, nunca como garantia.

Passo 2: confirmar que o provedor oferece GPU e RAM apropriadas **sem pagamento**, espaço de disco suficiente, tempo de sessão, regras de uso compatíveis e cotas disponíveis antes de baixar dezenas de GB. Não contratar plano nem adicionar cartão para contornar limites.

Passo 3: usar **um único trecho de 3 segundos** com um personagem. Executar o pipeline oficial completo, documentando velocidade, RAM, VRAM, qualidade, artefatos, restrições e possibilidade de reprodutibilidade. O modelo somente será integrado ao app depois de **PASS**.

Passo 4: avaliar oclusão, corpo integral e fidelidade de acessórios e depois múltiplos personagens. Nunca registrar uma simples face swap como aprovação do recasting integral.

## Provedores gratuitos (documentação pública)

| Provedor | Condições divulgadas | Viabilidade para os candidatos |
|---|---|---|
| Hugging Face ZeroGPU | Contas Free elegíveis podem hospedar até 2 Spaces; GPU `large` 48 GB ou `xlarge` 96 GB; 5 min/dia para usuário Free; `xlarge` consome 2× quota, filas maiores; somente Gradio | Candidato a **ensaio controlado** do Viggle-Animate; a carga do modelo, o tempo total e o limite de duração podem inviabilizar um único render. Nenhum Space foi implantado nem testado aqui. |
| Google Colab Free | GPU/TPU ocasional, cotas dinâmicas não garantidas, tempo máximo de runtime variável e acesso restrito à GPU; até ~12 horas sujeito a limites | Testar somente versões quantizadas/segmentos muito curtos quando memória/disk preflight passar. Não presumir GPU de 96 GB. |
| Kaggle Notebook | A documentação oficial oferece NVIDIA P100 gratuita, quando disponível, com filas; quotas e capacidade mudam | Triagem de pré-processamento ou modelos mais leves, não assumir 96 GB. |

Fontes:
- https://huggingface.co/docs/hub/spaces-zerogpu
- https://research.google.com/colaboratory/intl/pt-BR/faq.html
- https://www.kaggle.com/docs/notebooks

### Atenção ao ZeroGPU
O Viggle-Animate oficial informa um pico de aproximadamente 80.1 GiB de VRAM BF16 e GPU recomendada de 96 GB. O ZeroGPU xlarge divulga 96 GB, mas um app comunitário indicou demanda maior que a quota de um dia Free. **GPU com VRAM suficiente NÃO garante que seja possível gerar dentro dos 5 minutos de quota (cobrados 2×) nem carregar o checkpoint na janela alocada.** Não classificar como solução provada.

Fontes:
- https://huggingface.co/Viggle/Viggle-Animate
- https://viggle.ai/research/viggle-animate-character-replacement-from-a-repainted-frame
- https://huggingface.co/spaces/akhaliq/viggle-animate/blob/main/app.py

## Motores abertos avaliados

### A) Viggle-Animate: video + quadro repintado
- 33.1B, estágio temporal sem pose/face/máscara.
- Usa vídeo original e um frame desse próprio vídeo onde o personagem já substituiu o ator.
- Mais alinhado com nosso fluxo v0.7 do que sprite+MediaPipe.
- Restrições: muitos personagens, interações, cortes, características invisíveis e formas corporais muito diferentes. Modelo aberto não replica necessariamente o serviço Viggle comercial.
- Execução local no Redmi/RX 580: **não viável no perfil atual**. Ensaio em ZeroGPU xlarge: **NÃO VALIDADO**, sujeito a cota.
- Código/pesos: https://huggingface.co/Viggle/Viggle-Animate

### B) Wan2.2-Animate-14B: vídeo + personagem + pré-processamento
- Modo `replacement` oficial; exige extração e preparação de pose, face, fundo, máscara e referenciais por pipeline próprio.
- Quantização/offload não elimina necessidade de RAM/disco/tempo. Casos comunitários de 4 GB VRAM não são garantia no nosso hardware nem no Colab.
- Para teste com GPU gratuita limitada, começar pelo script de triagem; só executar notebook se pré-processamento completo e modelo couberem.
- Código: https://github.com/Wan-Video/Wan2.2
- Guia: https://github.com/Wan-Video/Wan2.2/blob/main/wan/modules/animate/preprocess/UserGuider.md

## Critérios objetivos GO / NO-GO

- **GO** apenas se: um vídeo de 3 s foi renderizado sem pagamento; toda pessoa (não apenas rosto) foi substituída, movimento preservado, corpo e vestes consistentes, sem troca de identidade; hardware, prazo de cota e logs documentados; mesma execução pode ser repetida.
- **NO-GO** se: necessidade comprovada de GPU paga, franquia exaurida antes do output, memória/disk insuficientes, restrição de licença ou termos de serviço incompatíveis, ou instabilidade grave com um ator.
- **INDETERMINADO** se: somente a página do modelo, promessa ou demonstração existe, sem render real verificável no ambiente gratuito do usuário.
- **Fallback local**: continuar produzindo máscaras, quadros-chave e composição controlada no navegador; sem simular que isso gera vídeo com IA.

## Próximas tarefas de engenharia

- Exportar projeto e quadro retocado com alinhamento e proporções verificadas.
- Criar adapter específico para modelo somente depois de passar preflight e teste real.
- Implementar segmentação semântica/track de identidade quando um motor precisar disso, sem criar ponte obrigatória para MediaPipe.
- Montar cortes/segmentos gerados e medir fidelidade quadro a quadro.
- Manter o trabalho sem despesa, sem serviço pago automático e sem qualquer associação a conta em nuvem não autorizada.
