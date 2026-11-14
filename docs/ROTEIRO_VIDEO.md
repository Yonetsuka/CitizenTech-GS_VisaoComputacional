# Roteiro do vídeo de demonstração (4 a 5 minutos)

O vídeo vale até **5 pontos** e o critério é a **solução funcionando**. O que mais pesa é o professor ver o sistema detectando de verdade, em tempo real. Mostre o programa rodando, não só slides.

## Estrutura

| Tempo | O que mostrar | O que falar |
|---|---|---|
| 0:00 a 0:25 | Tela de abertura com o nome do projeto e dos integrantes | "Somos o grupo X. Esta é a parte de Visão Computacional do projeto Ônibus & Chuva SP." |
| 0:25 a 0:55 | Uma imagem do ponto de ônibus e o diagrama do projeto | O problema: quem espera no ponto, a chuva, idosos e pessoas com deficiência. O papel da visão: enxergar o ponto e transformar em informação |
| 0:55 a 1:35 | Roboflow ou a pasta do dataset, com exemplos anotados | Quantas imagens, de onde vieram, as 4 classes e como foi a anotação |
| 1:35 a 2:20 | O notebook do Colab com o treino e as métricas | Modelo YOLO com pesos pré-treinados, parâmetros, mAP50 e a matriz de confusão |
| **2:20 a 3:50** | **O programa rodando em tempo real** (núcleo do vídeo) | Mostre as 4 cenas abaixo, com o FPS visível |
| 3:50 a 4:15 | O CSV gerado e o painel com os alertas | Como as contagens alimentam o pipeline de dados |
| 4:15 a 4:40 | Limitações e próximos passos | O que erra, por quê e o que fariam depois |
| 4:40 a 5:00 | Tela com o link do repositório | Encerramento |

## As 4 cenas da demonstração (2:20 a 3:50)

Rode `python src/detectar_tempo_real.py --pesos models/best.pt --fonte 0 --anonimizar --csv saidas/contagens.csv` (ou com um vídeo) e mostre, na ordem:

1. **Ponto vazio ou com poucas pessoas:** lotação baixa.
2. **Mais pessoas na cena:** o número sobe e a lotação passa para média ou alta.
3. **Guarda-chuvas abertos:** aparece "Indicio de chuva: SIM" no painel.
4. **Cadeira de rodas:** aparece o alerta vermelho "ALERTA: cadeirante no ponto".

Se houver um ônibus (de verdade ou em um vídeo), mostre também a detecção e o contador de ônibus.

**Mostre a anonimização:** deixe claro que a cabeça das pessoas aparece pixelizada.

## Como filmar a cena sem um ponto de ônibus de verdade

- Reproduza um **vídeo de ponto de ônibus** em um segundo monitor ou no celular e aponte a webcam para ele, ou rode o programa direto sobre o arquivo de vídeo.
- Use fotos e cenas feitas por vocês, com guarda-chuvas de verdade e um integrante em cadeira de rodas **só se houver consentimento** e segurança. Caso contrário, use um vídeo de apoio e diga isso no vídeo.
- Seja transparente: diga se o cenário é uma simulação. Isso não tira nota e evita problemas.

## Dicas de gravação

- Grave a tela com o **OBS Studio** (gratuito) ou, no Windows, o `Win + G` (Xbox Game Bar).
- Grave a webcam e a tela juntas, se der.
- Deixe o **terminal visível** com a linha de comando e o FPS.
- Fale devagar e use frases curtas. Se errar, corte e regrave: edição simples no próprio OBS ou no Clipchamp.
- Resolução de 1080p e áudio claro (teste o microfone antes).
- Legendas ajudam se o áudio ficar baixo.

## Antes de enviar

- [ ] O vídeo mostra o programa **detectando** de verdade, não só imagens estáticas.
- [ ] As 4 cenas aparecem (lotação, chuva, acessibilidade e, se possível, ônibus).
- [ ] O link do repositório aparece na tela e no PDF.
- [ ] O vídeo está em um link que o professor consegue abrir (YouTube como **não listado** ou Google Drive com acesso por link). Abra em janela anônima para testar.
- [ ] Nenhum rosto identificável aparece sem anonimização.
- [ ] Confirme com o professor o canal de envio do vídeo (o enunciado de Visão não detalha; as outras disciplinas usam o Teams).
