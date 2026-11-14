# Imagens de métricas para o relatório

| Arquivo | Como usar |
|---|---|
| `01_curvas_treinamento.png` | Evolução das perdas, precisão, recall, mAP50 e mAP50-95 durante as épocas |
| `02_matriz_confusao_normalizada.png` | Desempenho por classe e confusões com background |
| `03_rotulos_reais_validacao.jpg` | Anotações verdadeiras do lote de validação |
| `04_predicoes_validacao.jpg` | Previsões do modelo no mesmo tipo de lote |

As imagens devem ser inseridas no relatório com legendas e fonte: resultados gerados pelo treinamento YOLO do projeto.

Os valores numéricos exatos devem ser copiados do `results.csv` ou da saída de `model.val()` no Colab; não devem ser estimados visualmente a partir do gráfico.
