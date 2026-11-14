# Detecção em tempo real de objetos em pontos de ônibus — Ônibus & Chuva SP

## Integrantes
- Nome completo — RM
- Nome completo — RM

## Resumo — 250 palavras
[Preencher com problema, solução, dataset, modelo, métricas e contribuição.]

## Introdução
[Contextualizar chuva, transporte coletivo, lotação, acessibilidade e visão computacional.]

## Objetivo — 50 palavras
[Descrever o objetivo em exatamente 50 palavras.]

## Explicação técnica das ferramentas
[Descrever Python, Ultralytics YOLO, OpenCV, Google Colab, Roboflow e GitHub.]

## Metodologia
### Classes
O modelo utiliza `onibus`, `pessoa`, `guarda_chuva` e `cadeira_de_rodas`. A classe `ponto_de_onibus` foi retirada por falta de imagens anotadas suficientes.

### Dataset
- Imagens: [preencher]
- Fonte: Roboflow Universe
- Licença: CC BY 4.0
- Divisão: treino, validação e teste
- Anotações poligonais convertidas para caixas YOLO

### Treinamento
- Modelo base: [ ]
- Épocas: [ ]
- Imagem: [ ]
- Batch: [ ]
- GPU: [ ]
- Tempo: [ ]

### Inferência e privacidade
[Descrever webcam/vídeo, suavização, CSV, anonimização e regras.]

## Resultados
### Métricas gerais
| Conjunto | Precisão | Recall | mAP50 | mAP50-95 | ms/imagem |
|---|---:|---:|---:|---:|---:|
| Validação | [ ] | [ ] | [ ] | [ ] | [ ] |
| Teste | [ ] | [ ] | [ ] | [ ] | [ ] |

### Métricas por classe
[Inserir tabela real.]

### Exemplos
[Inserir curvas, matriz de confusão, detecções, painel e CSV.]

## Análise
[Classes melhores/piores, erros e limitações.]

## Conclusão
[Resumo, métricas, FPS e contribuição.]

## Limitações e próximos passos
[Preencher.]

## Links
- GitHub: [ ]
- Vídeo: [ ]

## Referências
- Roboflow Universe: https://universe.roboflow.com/cssio-fiap/deteccaoprojetotransporteclima
- Ultralytics: https://docs.ultralytics.com/
- OpenCV: https://opencv.org/
