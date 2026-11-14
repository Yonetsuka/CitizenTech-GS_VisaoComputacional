# Dataset do projeto

## Classes utilizadas

O dataset final usa exatamente quatro classes:

```text
onibus
pessoa
guarda_chuva
cadeira_de_rodas
```

A classe `ponto_de_onibus` não foi incluída por falta de imagens anotadas suficientes e consistentes.

## Dataset atualmente incluído

O pacote contém a versão exportada do Roboflow Universe e preparada para YOLO:

- treino: 170 imagens;
- validação: 31 imagens;
- teste: 26 imagens;
- total: 227 imagens.

As anotações estão em `dataset/<divisão>/labels` e as imagens em `dataset/<divisão>/images`.

Fonte declarada:

<https://universe.roboflow.com/cssio-fiap/deteccaoprojetotransporteclima>

Licença declarada pelo dataset: **CC BY 4.0**.

## Validação

Execute na raiz do repositório:

```bash
python scripts/verificar_dataset.py dataset
```

O arquivo `dataset/data.yaml` define a ordem oficial:

```yaml
names: [onibus, pessoa, guarda_chuva, cadeira_de_rodas]
```

## Observação sobre as anotações

A exportação original continha algumas anotações poligonais. Elas foram convertidas para caixas delimitadoras YOLO. Antes da apresentação final, revise visualmente uma amostra das imagens, principalmente as de ônibus e cadeira de rodas.

## Uso no treinamento

No Ultralytics, use:

```python
from ultralytics import YOLO

modelo = YOLO("yolo11n.pt")
modelo.train(
    data="dataset/data.yaml",
    epochs=60,
    imgsz=640,
    batch=16,
    patience=15,
    seed=42,
)
```

## Privacidade e redistribuição

Não adicione fotos com rostos identificáveis sem autorização. Se novas imagens forem coletadas, registre a origem, a licença e a autorização de uso. O relatório deve citar a fonte do dataset e a licença declarada.
