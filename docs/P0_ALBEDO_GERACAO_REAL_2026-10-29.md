# P0 — Geração real Albedo (prévia 29/10/2026)

## Objetivo e arquitetura

Gerar um MP4 animado de ~3 segundos em que a Albedo substitua integralmente o dançarino central, mantendo o restante da multidão. Não é face swap, rastreamento MediaPipe nem sprite rígido. Para o teste curto escolhemos a API oficial Viggle V1 Video Remix. A rota aberta Viggle-Animate de vídeo + quadro repintado permanece separada, e ainda requer GPU de grande memória.

## Ativos de entrada no pacote do usuário (NÃO comitados ao GitHub)

- assets/Albedo_original_2731x4096.png: imagem canônica original; não a substitua pelas gerações experimentais.
- assets/driving.mp4: 576x1024, 24fps, 3s, previamente convertido de uma exportação WebM do editor.
- assets/source-ref.png: quadro original do instante de ~1s.
- assets/Albedo_768_transparente.png e assets/Albedo_768_fundo_neutro.png: auxiliares.
- Quadro repainted-ref.png existente em sessão anterior foi experimental e ainda não aprovado como fiel a todos os espectadores; não foi adotado como referência original.

## O que foi implementado

- recast.html v0.8.1 permanece editor de preparação. Seu Play sempre reproduz o original.
- generate.html + generate.js: tela separada para carregamento dos ativos, preparação, verificação de créditos, confirmação explícita, envio, acompanhamento e download de MP4 gerado.
- cloud/local_render_gateway.py: gateway Python de uso pessoal, sem GPU local, na interface 127.0.0.1:8765; serve a tela e protege VIGGLE_API_KEY fora do JavaScript e do GitHub Pages.
- cloud/viggle_remix_api.py: adaptador Viggle Video Remix oficial; background_mode=original.
- tests/test_local_render_gateway.py: testes offline, sem POST real ou consumo de créditos.
- Recibos persistidos localmente em local-render-jobs/job-*/receipt.json, com retomada conservadora.

## Como executar no PC autorizado

Requisitos: Python 3.10+, ffprobe no PATH, acesso à internet, chave Viggle V1 e créditos disponíveis. Nenhuma GPU é necessária para este gateway.

PowerShell (em uma cópia local do repositório):

    $env:VIGGLE_API_KEY = (Read-Host "Chave Viggle V1")
    python cloud/local_render_gateway.py --port 8765 --workdir local-render-jobs

Abrir: http://127.0.0.1:8765/generate.html

1. Selecionar Albedo_original_2731x4096.png e driving.mp4.
2. Clicar em Validar e preparar geração (não cobra nem envia ao Viggle).
3. Clicar em Consultar créditos; confirmar se o saldo disponível é gratuito, caso não queira usar créditos comprados.
4. Assinalar a autorização e confirmar Gerar Albedo dançando. Isso envia arquivos ao Viggle e consome créditos JÁ disponíveis, sem fazer compras.
5. Consultar andamento. Quando READY, a página oferece MP4 para reprodução e download.
6. Verificar coreografia, silhueta, chifres, asas, cabelo, roupas, outras pessoas e oclusões antes de aprovar.

## Regras de segurança e custo

- Orçamento adicional zero. Nenhum serviço de GPU pago, assinatura, upgrade, cartão ou cobrança automática.
- A API pública anuncia 100 créditos iniciais para contas novas e 1 crédito/segundo de Video Remix; consultar saldo primeiro. API só apresenta saldo, NÃO origem (grátis ou comprado).
- Chave em variável de ambiente do servidor, jamais no repositório, navegador público, comentários ou prompt.
- Gateway acessível só em 127.0.0.1, portanto a versão GitHub Pages da tela NÃO executa render sozinha. Redmi Android também não acessa o localhost do PC sem uma infraestrutura adicional.
- Um único POST de geração por confirmação; nenhum POST é repetido automaticamente após timeout. Se estado SUBMISSION_UNCERTAIN, verificar painel do Viggle antes de qualquer outra tentativa.
- O envio de vídeo e imagem a provedor externo precisa ser consentido; gateway não faz uploads na preparação.
- Status RENDERED_UNREVIEWED significa apenas arquivo entregue, não sucesso de substituição da Albedo.

## Limitações objetivas

Nenhuma renderização temporal executada na conta Viggle; sem credencial nem saldo confirmado. O modelo pode modificar pessoas adjacentes e falhar em selecionar o dançarino correto no meio da multidão. A primeira execução real precisa demonstrar corpo, asas e vestes coerentes. Múltiplos personagens e integração direta na versão Android seguem futuras.

Documentação oficial:
https://docs.viggle.ai/v1/guides/quickstart-mix
https://docs.viggle.ai/v1/pricing
https://docs.viggle.ai/v1/api-reference/credits
