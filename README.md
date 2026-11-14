# Ônibus & Chuva SP — Visão Computacional

Projeto de detecção de objetos em cenas de transporte coletivo usando YOLO e OpenCV. O sistema transforma detecções em informações sobre lotação, possível chuva, ônibus à vista e acessibilidade.

## Integrantes

| Nome completo | RM |
|---|---|
| **PREENCHER** | **PREENCHER** |
| **PREENCHER** | **PREENCHER** |
| **PREENCHER** | **PREENCHER** |

> Substitua os campos acima antes da entrega.

## Classes

O modelo usa quatro classes:

- `onibus`
- `pessoa`
- `guarda_chuva`
- `cadeira_de_rodas`

A classe `ponto_de_onibus` foi retirada porque não havia imagens anotadas suficientes e consistentes. O contexto do ponto é definido pelo vídeo ou câmera analisado; o modelo concentra-se nos objetos necessários para produzir as informações ao cidadão.

## O que o sistema faz

A aplicação:

1. detecta objetos com um modelo YOLO treinado de forma customizada;
2. conta ônibus, pessoas, guarda-chuvas e cadeiras de rodas;
3. suaviza a contagem usando a mediana dos últimos quadros;
4. classifica a lotação como baixa, média ou alta;
5. indica possível chuva quando há guarda-chuvas suficientes;
6. informa quando há ônibus à vista;
7. gera alerta de acessibilidade quando detecta cadeira de rodas;
8. pode pixelizar a parte superior das pessoas com `--anonimizar`;
9. salva as contagens em CSV.

## Estrutura

```text
src/
  detectar_tempo_real.py
  regras.py
scripts/
  verificar_dataset.py
  extrair_frames.py
notebooks/
  treinamento_onibus_chuva_github.ipynb
dataset/
  data.yaml
  train/
  valid/
  test/
docs/
  DATASET.md
  ROTEIRO_VIDEO.md
  ESQUELETO_RELATORIO_4_CLASSES.md
  Relatorio_Visao_Computacional_Onibus_Chuva_SP_ESQUELETO.docx
tests/
models/
  best.pt                 # modelo treinado incluído
amostras/
  video_ponto_onibus.mp4  # vídeo original da demonstração
saidas/
data.yaml
requirements.txt
```

## Dataset

O dataset preparado possui 227 imagens, distribuídas em:

- 170 imagens de treino;
- 31 imagens de validação;
- 26 imagens de teste.

A fonte declarada é o Roboflow Universe, com licença CC BY 4.0:

<https://universe.roboflow.com/cssio-fiap/deteccaoprojetotransporteclima>

As anotações poligonais encontradas na exportação foram convertidas para caixas delimitadoras YOLO. Essa conversão deve ser revisada visualmente antes da apresentação final.

Para conferir o dataset:

```bash
python scripts/verificar_dataset.py dataset
```

## Instalação

```bash
python -m pip install -r requirements.txt
```

## Treinamento no Google Colab

Abra:

```text
notebooks/treinamento_onibus_chuva_github.ipynb
```

O notebook foi preparado para funcionar com o pacote no Colab e salvar os resultados no Google Drive. Ele treina, localiza o `best.pt`, avalia validação e teste, gera predições e processa um vídeo.

O notebook não contém tokens ou chaves privadas. Para usar o projeto clonado do GitHub, ajuste apenas `PROJETO_DIR` para o caminho da pasta clonada no Colab.

## Inferência

Depois do treinamento, coloque o arquivo `best.pt` em `models/best.pt` e execute:

```bash
python src/detectar_tempo_real.py \
  --pesos models/best.pt \
  --fonte video.mp4 \
  --anonimizar \
  --salvar-video saidas/demo.mp4 \
  --csv saidas/contagens.csv \
  --sem-janela
```

Com webcam local, use `--fonte 0` e retire `--sem-janela` se quiser abrir a janela:

```bash
python src/detectar_tempo_real.py --pesos models/best.pt --fonte 0 --anonimizar --csv saidas/contagens.csv
```

## Testes

```bash
python -m unittest discover -s tests -v
```

Os testes usam um modelo falso e vídeos sintéticos; não exigem GPU nem o arquivo `best.pt`.

## Artefatos de demonstração

O repositório inclui os arquivos usados na demonstração:

- `models/best.pt`: pesos treinados;
- `amostras/video_ponto_onibus.mp4`: vídeo original;
- `saidas/demo.mp4`: vídeo processado com caixas e painel;
- `saidas/contagens.csv`: contagens geradas pela inferência;
- `docs/metricas/`: curvas, matriz de confusão, rótulos e previsões para o relatório.

O vídeo processado tem aproximadamente 16 segundos, resolução 1920×1080 e mostra detecções de ônibus e pessoas, contagem no painel, FPS e anonimização.

## Resultados

Preencha esta tabela com os valores reais gerados pelo notebook:

| Avaliação | Precisão | Recall | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|
| `best.pt` — avaliação final | 77,67% | 79,01% | 82,97% | 56,84% |

### Interpretação das métricas

Na avaliação informada para o `best.pt`, o modelo alcançou 77,67% de precisão, 79,01% de recall, 82,97% de mAP50 e 56,84% de mAP50-95. A precisão indica a proporção das detecções realizadas que estavam corretas; o recall indica a proporção dos objetos anotados que foram encontrados. O mAP50 usa uma tolerância de IoU de 0,50, enquanto o mAP50-95 é mais rigoroso por calcular a média em várias tolerâncias. Ao finalizar o relatório, informe se essa avaliação foi realizada no conjunto `test` ou `val`.

## Privacidade

O sistema não identifica pessoas; ele detecta e conta objetos. A opção `--anonimizar` pixeliza a região superior das pessoas antes de exibir ou gravar. Não publique imagens com rostos identificáveis sem autorização.

## Limitações

- o dataset é pequeno para um sistema robusto de produção;
- as imagens podem não representar todos os pontos de ônibus de São Paulo;
- objetos pequenos, oclusão, baixa iluminação e sobreposição podem causar erros;
- guarda-chuva é apenas um indício de chuva, pois também pode ser usado contra o sol;
- a classe `ponto_de_onibus` não foi treinada por falta de exemplos consistentes;
- as métricas devem ser interpretadas como prova de conceito.
