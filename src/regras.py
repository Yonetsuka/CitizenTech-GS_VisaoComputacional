"""
Regras de negócio: transformam as contagens de objetos detectados em informação
para o cidadão. Não depende de visão computacional, então é fácil de testar.

Classes do modelo (mesma ordem do data.yaml):
    onibus, pessoa, guarda_chuva, cadeira_de_rodas
"""
from __future__ import annotations

from collections import deque
from statistics import median

CLASSES = ["onibus", "pessoa", "guarda_chuva", "cadeira_de_rodas"]


def contar(nomes: list[str], classes: list[str] = CLASSES) -> dict[str, int]:
    """Conta quantas vezes cada classe apareceu em um quadro."""
    contagens = {c: 0 for c in classes}
    for nome in nomes:
        if nome in contagens:
            contagens[nome] += 1
    return contagens


class Suavizador:
    """
    A contagem quadro a quadro oscila (uma pessoa some por 2 quadros, por exemplo).
    Usamos a MEDIANA dos últimos N quadros para estabilizar o número mostrado.
    """

    def __init__(self, janela: int = 15, classes: list[str] = CLASSES):
        self.historico = {c: deque(maxlen=max(1, janela)) for c in classes}

    def atualizar(self, contagens: dict[str, int]) -> dict[str, int]:
        for classe, fila in self.historico.items():
            fila.append(contagens.get(classe, 0))
        return self.valores()

    def valores(self) -> dict[str, int]:
        return {c: int(median(f) + 0.5) if f else 0 for c, f in self.historico.items()}


def nivel_lotacao(pessoas: int, limite_media: int = 4, limite_alta: int = 9) -> str:
    """baixa (até 3 pessoas), media (4 a 8) ou alta (9 ou mais). Os limites são ajustáveis."""
    if pessoas >= limite_alta:
        return "alta"
    if pessoas >= limite_media:
        return "media"
    return "baixa"


def indicio_chuva(pessoas: int, guarda_chuvas: int, minimo: int = 2, razao: float = 0.5) -> bool:
    """
    Indício de chuva: 2 ou mais guarda-chuvas, ou metade (ou mais) das pessoas com guarda-chuva.
    É só um INDÍCIO: guarda-chuva também protege do sol. Confirme com a chuva da Open-Meteo.
    """
    if guarda_chuvas >= minimo:
        return True
    return pessoas > 0 and guarda_chuvas >= 1 and guarda_chuvas / pessoas >= razao


def atencao_acessibilidade(cadeiras_de_rodas: int) -> bool:
    return cadeiras_de_rodas >= 1


def resumir(contagens: dict[str, int], **limites) -> dict:
    """Junta tudo em um resumo do ponto de ônibus."""
    pessoas = contagens.get("pessoa", 0)
    guarda = contagens.get("guarda_chuva", 0)
    onibus = contagens.get("onibus", 0)
    cadeiras = contagens.get("cadeira_de_rodas", 0)

    lotacao = nivel_lotacao(pessoas, **{k: v for k, v in limites.items() if k in ("limite_media", "limite_alta")})
    chuva = indicio_chuva(pessoas, guarda, **{k: v for k, v in limites.items() if k in ("minimo", "razao")})
    acess = atencao_acessibilidade(cadeiras)

    partes = [f"Lotação {lotacao} ({pessoas} {'pessoa' if pessoas == 1 else 'pessoas'})"]
    if chuva:
        partes.append(f"indício de chuva ({guarda} {'guarda-chuva' if guarda == 1 else 'guarda-chuvas'})")
    if onibus:
        partes.append(f"{onibus} ônibus à vista")
    if acess:
        partes.append("pessoa em cadeira de rodas no ponto: priorizar veículo acessível")

    return {
        "lotacao": lotacao,
        "indicio_chuva": chuva,
        "atencao_acessibilidade": acess,
        "onibus_a_vista": onibus > 0,
        "mensagem": " · ".join(partes),
    }
