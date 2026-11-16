# Ônibus & Chuva SP — Visão Computacional

Projeto de detecção de objetos em cenas de transporte coletivo usando YOLO e OpenCV. O sistema detecta ônibus, pessoas, guarda-chuvas e cadeiras de rodas e transforma as detecções em informações sobre lotação, possível chuva, ônibus à vista e acessibilidade.

## Integrantes

| Nome completo | RM |
|---|---:|
| Cássio Eid Kobayashi Yonetsuka | 99678 |
| FIlipe Prado Menezes | 98765 |
| Pedro Henrique Salvitti Habiru | 88166 |

## Classes do modelo

- `onibus`
- `pessoa`
- `guarda_chuva`
- `cadeira_de_rodas`

A classe `ponto_de_onibus` não foi utilizada porque não havia imagens anotadas suficientes e consistentes. O contexto do ponto de ônibus é fornecido pelo vídeo analisado.

## Estrutura do projeto

```text
ONIBUS_CHUVA_SP/
├── amostras/
│   └── video_ponto_onibus.mp4
├── dataset/
│   ├── data.yaml
│   ├── train/
│   ├── valid/
│   └── test/
├── docs/
│   ├── DATASET.md
│   ├── METRICAS_FINAIS.md
│   ├── ARTEFATOS_DEMONSTRACAO.md
│   └── Relatorio_Visao_Computacional_Onibus_Chuva_SP_FINAL.docx
├── models/
│   └── best.pt
├── notebook/
│   └── execucao_colab.ipynb
├── saidas/
│   └── contagens.csv
├── src/
│   ├── detectar_tempo_real.py
│   └── regras.py
└── README.md
```

## Instalação local

É necessário ter Python 3.10 ou superior. Na raiz do projeto, execute:

```bash
python -m pip install ultralytics opencv-python-headless pandas pyyaml jupyter
```

## Execução local do vídeo

Execute os comandos a partir da raiz do projeto, onde estão as pastas `dataset/`, `models/`, `src/`, `amostras/` e `saidas/`:

```bash
python src/detectar_tempo_real.py \
  --pesos models/best.pt \
  --fonte amostras/video_ponto_onibus.mp4 \
  --anonimizar \
  --sem-janela \
  --salvar-video saidas/demo_local.mp4 \
  --csv saidas/contagens_local.csv
```

Os arquivos gerados serão `saidas/demo_local.mp4` e `saidas/contagens_local.csv`.

Para usar uma webcam local, retire `--sem-janela` e substitua a fonte por `0`:

```bash
python src/detectar_tempo_real.py \
  --pesos models/best.pt \
  --fonte 0 \
  --anonimizar \
  --csv saidas/contagens_webcam.csv
```

## Avaliação do modelo

O arquivo `models/best.pt` já contém os pesos treinados. Para avaliar no conjunto de teste, execute na raiz do projeto:

```bash
python -c "from ultralytics import YOLO; m=YOLO('models/best.pt'); r=m.val(data='dataset/data.yaml', split='test', imgsz=640, plots=True); print(f'Precisão: {r.box.mp*100:.2f}%'); print(f'Recall: {r.box.mr*100:.2f}%'); print(f'mAP50: {r.box.map50*100:.2f}%'); print(f'mAP50-95: {r.box.map*100:.2f}%')"
```

A configuração `dataset/data.yaml` usa caminhos relativos à raiz do projeto:

```yaml
path: dataset
train: train/images
val: valid/images
test: test/images
```

## Notebook

O notebook de avaliação está em `notebook/execucao_colab.ipynb`. Apesar do nome histórico do arquivo, ele também pode ser executado localmente. Abra o Jupyter a partir da raiz do projeto:

```bash
jupyter notebook notebook/execucao_colab.ipynb
```

O notebook usa `PROJETO = Path.cwd()`. Por isso, não utiliza `/content`, Google Drive ou caminhos fixos de outro computador.

## Métricas finais

A avaliação reproduzida com `models/best.pt` no conjunto `test` apresentou:

| Avaliação | Precisão | Recall | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|
| `best.pt` — conjunto `test` | 62,99% | 60,21% | 68,41% | 38,92% |

A precisão indica a proporção das detecções realizadas que estavam corretas. O recall indica a proporção dos objetos anotados que foram encontrados. O mAP50 utiliza IoU de 0,50. O mAP50-95 é mais rigoroso porque calcula a média em vários limiares de IoU.

## Dataset

O dataset possui 227 imagens: 170 de treino, 31 de validação e 26 de teste. A fonte declarada é o Roboflow Universe, com licença indicada como CC BY 4.0:

<https://universe.roboflow.com/cssio-fiap/deteccaoprojetotransporteclima>

## Artefatos e limitações

O repositório contém o modelo treinado, o vídeo original, o CSV de contagens e o relatório final. O vídeo processado pode ser gerado novamente com o comando de inferência acima.

O dataset é pequeno para um sistema de produção. Oclusão, baixa iluminação e objetos pequenos podem causar erros. Guarda-chuva é apenas um indício de chuva, pois também pode ser utilizado contra o sol. O modelo não identifica pessoas; ele detecta e conta objetos. A opção `--anonimizar` pixeliza a região superior das pessoas antes da gravação.

## Privacidade

Não publique imagens com rostos identificáveis sem autorização. O modelo foi desenvolvido como prova de conceito acadêmica.
