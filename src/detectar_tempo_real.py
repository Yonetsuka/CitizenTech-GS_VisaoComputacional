#!/usr/bin/env python3
"""
Detecção em tempo real de objetos em pontos de ônibus (Ônibus & Chuva SP).

Lê webcam, arquivo de vídeo, imagem ou URL de câmera; detecta com o modelo YOLO treinado
(best.pt); suaviza as contagens; aplica as regras de negócio; mostra o resultado na tela;
e grava um CSV e, se pedido, um vídeo de saída.

Exemplos:
    # webcam, com anonimização das cabeças e CSV
    python src/detectar_tempo_real.py --pesos models/best.pt --fonte 0 --anonimizar --csv saidas/contagens.csv

    # vídeo gravado, sem abrir janela (Colab/servidor), salvando o resultado
    python src/detectar_tempo_real.py --pesos models/best.pt --fonte ponto.mp4 --sem-janela \
        --salvar-video saidas/demo.mp4 --csv saidas/contagens.csv

Tecla q fecha a janela.
"""
from __future__ import annotations

import argparse
import csv
import sys
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import cv2
import numpy as np

from regras import CLASSES, Suavizador, contar, resumir

# cores em BGR (padrão do OpenCV)
CORES = {
    "onibus": (0, 140, 255),
    "pessoa": (80, 200, 60),
    "guarda_chuva": (255, 160, 0),
    "cadeira_de_rodas": (60, 60, 230),
}
EXT_IMAGEM = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


# --------------------------------------------------------------------------- #
# Entrada e saída
# --------------------------------------------------------------------------- #
def abrir_fonte(fonte: str) -> cv2.VideoCapture:
    """'0' abre a webcam 0; qualquer outro texto é caminho de vídeo/imagem ou URL (rtsp/http)."""
    return cv2.VideoCapture(int(fonte) if fonte.isdigit() else fonte)


def extrair(resultado, nomes: dict) -> list[tuple[str, float, tuple[float, float, float, float]]]:
    """Converte o resultado do YOLO em uma lista simples: (classe, confiança, (x1, y1, x2, y2))."""
    caixas = getattr(resultado, "boxes", None)
    if caixas is None or len(caixas) == 0:
        return []
    xyxy = caixas.xyxy.cpu().numpy()
    classes = caixas.cls.cpu().numpy().astype(int)
    confs = caixas.conf.cpu().numpy()
    return [(nomes[int(c)], float(p), tuple(float(v) for v in b)) for b, c, p in zip(xyxy, classes, confs)]


# --------------------------------------------------------------------------- #
# Desenho e privacidade (LGPD)
# --------------------------------------------------------------------------- #
def anonimizar_pessoas(frame: np.ndarray, caixas: list, fracao_topo: float = 0.30) -> None:
    """Pixeliza o TOPO (cabeça) de cada pessoa detectada, direto no quadro. Rode antes de desenhar/gravar."""
    altura, largura = frame.shape[:2]
    for x1, y1, x2, y2 in caixas:
        x1, y1 = max(0, int(x1)), max(0, int(y1))
        x2, y2 = min(largura, int(x2)), min(altura, int(y2))
        topo = y1 + max(1, int((y2 - y1) * fracao_topo))
        topo = min(topo, altura)
        if x2 - x1 < 4 or topo - y1 < 4:
            continue
        regiao = frame[y1:topo, x1:x2]
        h, w = regiao.shape[:2]
        pequeno = cv2.resize(regiao, (max(1, w // 8), max(1, h // 8)), interpolation=cv2.INTER_LINEAR)
        frame[y1:topo, x1:x2] = cv2.resize(pequeno, (w, h), interpolation=cv2.INTER_NEAREST)


def desenhar(frame: np.ndarray, deteccoes: list) -> None:
    for nome, conf, (x1, y1, x2, y2) in deteccoes:
        cor = CORES.get(nome, (255, 255, 255))
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), cor, 2)
        rotulo = f"{nome} {conf:.2f}"
        (tw, th), _ = cv2.getTextSize(rotulo, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        yb = max(int(y1), th + 6)
        cv2.rectangle(frame, (int(x1), yb - th - 6), (int(x1) + tw + 4, yb), cor, -1)
        cv2.putText(frame, rotulo, (int(x1) + 2, yb - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)


def painel(frame: np.ndarray, contagens: dict, resumo: dict, fps: float) -> None:
    """Painel no canto superior esquerdo. O OpenCV não desenha acentos, então o texto aqui é sem acento."""
    linhas = [f"{c}: {contagens.get(c, 0)}" for c in CLASSES]
    linhas += [
        f"Lotacao: {resumo['lotacao']}",
        f"Indicio de chuva: {'SIM' if resumo['indicio_chuva'] else 'nao'}",
        f"FPS: {fps:.1f}",
    ]
    if resumo["atencao_acessibilidade"]:
        linhas.append("ALERTA: cadeirante no ponto")

    altura = 12 + 22 * len(linhas)
    largura = 270
    fundo = frame.copy()
    cv2.rectangle(fundo, (0, 0), (largura, altura), (0, 0, 0), -1)
    cv2.addWeighted(fundo, 0.55, frame, 0.45, 0, frame)
    for i, texto in enumerate(linhas):
        cor = (0, 0, 255) if texto.startswith("ALERTA") else (255, 255, 255)
        cv2.putText(frame, texto, (10, 24 + 22 * i), cv2.FONT_HERSHEY_SIMPLEX, 0.6, cor, 1, cv2.LINE_AA)


# --------------------------------------------------------------------------- #
# Laço principal
# --------------------------------------------------------------------------- #
def executar(args: argparse.Namespace, modelo) -> dict:
    """Roda a detecção. `modelo` é qualquer objeto com .predict(...) e .names (o YOLO, ou um falso nos testes)."""
    cap = abrir_fonte(args.fonte)
    if not cap.isOpened():
        raise SystemExit(f"Não foi possível abrir a fonte: {args.fonte}")

    eh_arquivo = not args.fonte.isdigit()
    eh_imagem = eh_arquivo and Path(args.fonte).suffix.lower() in EXT_IMAGEM
    fps_origem = cap.get(cv2.CAP_PROP_FPS)
    fps_origem = fps_origem if fps_origem and fps_origem > 1 else 25.0

    suavizador = Suavizador(janela=1 if eh_imagem else args.janela)
    escritor = None
    arquivo_csv = None
    gravador_csv = None
    if args.csv:
        Path(args.csv).parent.mkdir(parents=True, exist_ok=True)
        novo = not Path(args.csv).exists()
        arquivo_csv = open(args.csv, "a", newline="", encoding="utf-8")
        gravador_csv = csv.writer(arquivo_csv)
        if novo:
            gravador_csv.writerow(
                ["timestamp", "segundo_video", *CLASSES, "lotacao", "indicio_chuva", "atencao_acessibilidade", "fps"]
            )

    n = 0
    fps = 0.0
    ultimo_csv = -1e9
    inicio = time.time()
    linhas_csv = 0
    ultimo_resumo = None
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            t0 = time.time()

            resultado = modelo.predict(frame, conf=args.conf, imgsz=args.imgsz, verbose=False)[0]
            deteccoes = extrair(resultado, modelo.names)
            suave = suavizador.atualizar(contar([d[0] for d in deteccoes]))
            resumo = resumir(suave)
            ultimo_resumo = resumo

            if args.anonimizar:
                anonimizar_pessoas(frame, [d[2] for d in deteccoes if d[0] == "pessoa"])
            desenhar(frame, deteccoes)

            dt = max(time.time() - t0, 1e-6)
            fps = (1.0 / dt) if fps == 0 else 0.9 * fps + 0.1 * (1.0 / dt)
            painel(frame, suave, resumo, fps)

            tempo_ref = (n / fps_origem) if eh_arquivo else (time.time() - inicio)
            if gravador_csv and tempo_ref - ultimo_csv >= args.intervalo:
                ultimo_csv = tempo_ref
                gravador_csv.writerow(
                    [
                        datetime.now(ZoneInfo("America/Sao_Paulo")).isoformat(timespec="seconds"),
                        round(tempo_ref, 1),
                        *[suave[c] for c in CLASSES],
                        resumo["lotacao"],
                        int(resumo["indicio_chuva"]),
                        int(resumo["atencao_acessibilidade"]),
                        round(fps, 1),
                    ]
                )
                linhas_csv += 1

            if args.salvar_video:
                if escritor is None:
                    Path(args.salvar_video).parent.mkdir(parents=True, exist_ok=True)
                    h, w = frame.shape[:2]
                    escritor = cv2.VideoWriter(
                        args.salvar_video, cv2.VideoWriter_fourcc(*"mp4v"), fps_origem if eh_arquivo else 20.0, (w, h)
                    )
                escritor.write(frame)

            if eh_imagem and args.salvar_imagem:
                Path(args.salvar_imagem).parent.mkdir(parents=True, exist_ok=True)
                cv2.imwrite(args.salvar_imagem, frame)

            n += 1
            if n % 30 == 0:
                print(f"[quadro {n}] {fps:.1f} FPS | {resumo['mensagem']}")

            if not args.sem_janela:
                cv2.imshow("Onibus & Chuva SP - Visao Computacional (q para sair)", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            if args.max_quadros and n >= args.max_quadros:
                break
            if eh_imagem:
                break
    except KeyboardInterrupt:
        print("Interrompido pelo usuário.")
    finally:
        cap.release()
        if escritor:
            escritor.release()
        if arquivo_csv:
            arquivo_csv.close()
        if not args.sem_janela:
            cv2.destroyAllWindows()

    return {"quadros": n, "fps_medio": round(n / max(time.time() - inicio, 1e-6), 1), "linhas_csv": linhas_csv,
            "ultimo_resumo": ultimo_resumo}


def ler_args(argv=None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Detecção em tempo real em pontos de ônibus")
    p.add_argument("--pesos", required=True, help="arquivo .pt do modelo treinado (best.pt)")
    p.add_argument("--fonte", default="0", help="índice da webcam (0), caminho de vídeo/imagem ou URL")
    p.add_argument("--conf", type=float, default=0.35, help="confiança mínima (0 a 1)")
    p.add_argument("--imgsz", type=int, default=640, help="tamanho da imagem na inferência")
    p.add_argument("--janela", type=int, default=15, help="quadros usados na suavização das contagens")
    p.add_argument("--intervalo", type=float, default=5.0, help="segundos entre linhas do CSV")
    p.add_argument("--csv", help="grava as contagens neste CSV (acrescenta se já existir)")
    p.add_argument("--salvar-video", help="grava o vídeo anotado neste .mp4")
    p.add_argument("--salvar-imagem", help="se a fonte for uma imagem, grava o resultado aqui")
    p.add_argument("--anonimizar", action="store_true", help="pixeliza a cabeça das pessoas (LGPD)")
    p.add_argument("--sem-janela", action="store_true", help="não abre janela (Colab, servidores)")
    p.add_argument("--max-quadros", type=int, default=0, help="para depois de N quadros (0 = sem limite)")
    return p.parse_args(argv)


def main(argv=None) -> None:
    args = ler_args(argv)
    from ultralytics import YOLO  # importação tardia: as regras e os testes não precisam do ultralytics

    resumo = executar(args, YOLO(args.pesos))
    print(f"Concluído: {resumo['quadros']} quadros, {resumo['fps_medio']} FPS médio, {resumo['linhas_csv']} linhas no CSV.")


if __name__ == "__main__":
    sys.exit(main())
