#!/usr/bin/env python3
"""build-identidade-x.py — compõe os 5 PNGs da identidade X (card t_591d5106).

Proveniência, não gosto: os três cards 16:9 saem do **instrumento**, isto é, de
`lib/social_card.py::render_en` do `social-pipeline` (branch `dev/x-card-t_60ddb68d`), o
mesmo que produz os cards reais da 2026-W48. Nada aqui é pintado à mão: o script só
escolhe texto de amostra e entrega o caminho.

O hero de artigo (1200x628) **não** passa por `render_en`, e a razão é medida: no canvas
1200x628 as bandas do card 16:9 (topo com handle + assinatura do site, pé com site +
fonte, hairlines) reservam 163 px em cima e 191 px embaixo, e a sonda devolveu **0 linhas
de corpo em 4 de 5 casos** nesse tamanho. O hero tem bandas próprias (`hero()` abaixo),
com a mesma margem proporcional, as mesmas fontes, os mesmos tokens e o mesmo módulo de
régua (96x6 px). A divergência é declarada em `docs/identidade-x.md` §7 e vira card de
`dev` para o instrumento ganhar `render_hero`.

Determinístico: mesmo texto + mesmas opções ⇒ mesmos bytes. Sem rede, sem IA, sem relógio.
Sem API de imagem paga (ADR-0070): o fundo do hero-02 é desenhado em Pillow a partir da
própria paleta.

    python3 tools/build-identidade-x.py [--saida docs] [--pipeline ~/code/social-pipeline]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PIPELINE_PADRAO = Path.home() / "code" / "social-pipeline"
RAIZ = Path(__file__).resolve().parent.parent

# textos de AMOSTRA: descrevem o próprio ofício da peça, não afirmam nada sobre o mundo.
# O rótulo de fonte diz o que a peça é (specimen) porque inventar citação de terceiro
# seria pior que a ausência dela.
FONTE_AMOSTRA = "specimen · EN identity v1"

AMOSTRAS = {
    "x-card-thread-01.png": dict(
        titulo="Attention before belief",
        paragrafos=["A cognitive operation rarely changes what you know. It changes "
                    "what you notice first, and what you never get to compare."],
        fonte=FONTE_AMOSTRA,
    ),
    # título no limite da escada: 3 linhas a 72 px na coluna de 1316 (teste de viúva)
    "x-card-thread-02.png": dict(
        titulo="When the same claim arrives from three places it stops looking like a claim",
        paragrafos=["Repetition reads as corroboration until the three places are "
                    "checked against each other."],
        fonte=FONTE_AMOSTRA,
    ),
    # long post: título de 2 linhas + 3 linhas de corpo (o vão medido: 82,1% de ocupação do
    # título, contra o mínimo de 65,0% da série publicada; ver `identidade-x.md` §3)
    "x-card-longo-01.png": dict(
        titulo="The same claim in three places is still one claim",
        paragrafos=["Three accounts of the same claim are one account told three times. "
                    "Volume is not a source, and a pattern is not a record. What the long "
                    "post adds is provenance: who recorded it, when, and what stayed "
                    "public. None of that survives a screenshot."],
        fonte=FONTE_AMOSTRA,
    ),
}

HEROES = {
    "x-hero-artigo-01.png": dict(
        titulo="Sources, not volume",
        deck="An intelligence note is worth the provenance it can show.",
        fundo=False,
    ),
    "x-hero-artigo-02.png": dict(
        titulo="The record outlives the narrative",
        deck="What outlives the story is the document.",
        fundo=True,
    ),
}


# ---------------------------------------------------------------- instrumento
def carregar_pipeline(dir_pipeline: Path):
    """Importa o `social_card` do pipeline de publicação (read-only)."""
    sys.path.insert(0, str(dir_pipeline))
    from lib import social_card  # noqa: PLC0415

    return social_card


def card_16x9(sc: object, spec: dict, saida: Path) -> dict:
    """Card de thread/long post pelo próprio instrumento (canvas `x`, 1600x900)."""
    return sc.render_en(spec["titulo"], spec["paragrafos"], spec["fonte"], saida,
                        canvas=sc.CANVAS["x"])


# ---------------------------------------------------------------- hero 1200x628
HERO_L, HERO_A = 1200, 628
HERO_MARGEM = round(96 * HERO_L / 1080)   # mesma proporção do card: 8,89% da largura
HERO_COL = HERO_L - 2 * HERO_MARGEM
HERO_ESCADA = (72, 64, 56, 48)
HERO_TITULO_LH_F = 1.16
HERO_DECK_PT, HERO_DECK_LH_F = 48, 1.42
HERO_MAX_TITULO, HERO_MAX_DECK = 3, 2
HERO_CHROME_PT = 26          # handle, assinatura do site e pé: mono 26 px
HERO_TOPO_GAP = 60           # do topo do bloco de título abaixo da linha do chrome
HERO_REGUA_GAP = 30
HERO_DECK_GAP = 26
HERO_PISO = 40               # ar mínimo entre o bloco e o pé


def _bicubic():
    """PIL 10 moveu os filtros para `Image.Resampling`; o getattr cobre as duas."""
    from PIL import Image  # noqa: PLC0415

    return getattr(Image, "Resampling", Image).BICUBIC


def fundo_escuro(sc) -> "object":
    """Fundo do hero-02: grafismo derivado dos tokens, sem hue novo.

    Três camadas, todas em Pillow e determinísticas: brilho radial (título reduzido sobre
    o fundo), malha de 40 px (link reduzido sobre o fundo) e véu horizontal de EN_FUNDO
    mais denso à esquerda, onde o texto fica — o véu é o que garante o contraste, não a
    sorte de o grafismo cair escuro.
    """
    from PIL import Image, ImageDraw, ImageFilter  # noqa: PLC0415

    fundo = sc.EN_FUNDO
    img = Image.new("RGB", (HERO_L, HERO_A), fundo)

    # 1. brilho radial no canto superior direito, calculado em miniatura e ampliado
    mini_l, mini_a = 96, 50
    mini = Image.new("RGB", (mini_l, mini_a), fundo)
    dm = ImageDraw.Draw(mini)
    cx, cy, raio = 0.80 * mini_l, 0.16 * mini_a, 0.72 * mini_l
    for y in range(mini_a):
        for x in range(mini_l):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            a = max(0.0, 1.0 - (d / raio) ** 2) * 0.30
            if a <= 0:
                continue
            dm.point((x, y), tuple(round(a * t + (1 - a) * f)
                                   for t, f in zip(sc.EN_TITULO, fundo)))
    img = mini.resize((HERO_L, HERO_A), _bicubic())

    # 2. malha de 40 px: 1 px de link reduzido sobre o fundo
    malha = tuple(round(0.10 * c + 0.90 * f) for c, f in zip(sc.EN_LINK, fundo))
    camada = Image.new("RGB", (HERO_L, HERO_A), fundo)
    dc = ImageDraw.Draw(camada)
    for x in range(HERO_MARGEM, HERO_L - HERO_MARGEM + 1, 40):
        dc.line([(x, 0), (x, HERO_A - 1)], fill=malha, width=1)
    for y in range(0, HERO_A, 40):
        dc.line([(0, y), (HERO_L - 1, y)], fill=malha, width=1)
    camada = camada.filter(ImageFilter.GaussianBlur(0.6))
    img = Image.blend(img, camada, 0.55)

    # 3. véu: EN_FUNDO de 0,90 à esquerda a 0,38 à direita (garante o contraste do texto)
    veu = Image.new("L", (HERO_L, 1))
    dv = ImageDraw.Draw(veu)
    for x in range(HERO_L):
        dv.point((x, 0), round(255 * (0.90 - 0.52 * x / (HERO_L - 1))))
    veu = veu.resize((HERO_L, HERO_A), _bicubic())
    img = Image.composite(Image.new("RGB", (HERO_L, HERO_A), fundo), img, veu)
    return img


def hero(sc, titulo: str, deck: str, saida: Path, *, com_fundo: bool = False) -> dict:
    """Hero de artigo 1200x628: título (≤3 linhas) + deck opcional (≤2), medida antes.

    Regras herdadas do card, porque são o que dá série à superfície: título em JetBrains
    Mono Bold com escada determinística (nunca trunca palavra), régua de 96x6 px no acento,
    corpo em Inter, frases inteiras, pé com o site à esquerda e a fonte à direita, margem
    de 8,89% da largura. O que muda é a banda: 1200x628 não tem a altura de 1600x900.
    """
    from PIL import Image, ImageDraw  # noqa: PLC0415

    M, C = HERO_MARGEM, HERO_COL
    img = fundo_escuro(sc) if com_fundo else Image.new("RGB", (HERO_L, HERO_A), sc.EN_FUNDO)
    d = ImageDraw.Draw(img)

    f_chrome = sc.fonte_en("mono", HERO_CHROME_PT)
    f_deck = sc.fonte_en("corpo", HERO_DECK_PT)
    cap_cr, desc_cr = sc._cap(d, f_chrome), sc._desc(f_chrome)
    cap_dk, desc_dk = sc._cap(d, f_deck), sc._desc(f_deck)
    # -------------------------------------------------------------- bandas
    base_topo = M + cap_cr
    tit_cap_top = M + HERO_TOPO_GAP
    pe_base = HERO_A - M
    limite = (pe_base - cap_cr) - HERO_PISO

    def _geometria(pt_tit: int, n_tit: int, n_deck: int):
        f_t = sc.fonte_en("titulo", pt_tit)
        cap_t, desc_t = sc._cap(d, f_t), sc._desc(f_t)
        lh_t = round(pt_tit * HERO_TITULO_LH_F)
        base_last = tit_cap_top + cap_t + (n_tit - 1) * lh_t
        t_bottom = base_last + desc_t
        rule_y = t_bottom + HERO_REGUA_GAP
        deck_base1 = rule_y + 6 + HERO_DECK_GAP + cap_dk
        deck_bottom = ((deck_base1 + (n_deck - 1) * round(HERO_DECK_PT * HERO_DECK_LH_F)
                        + desc_dk) if n_deck else rule_y + 6)
        return f_t, cap_t, lh_t, t_bottom, rule_y, deck_base1, deck_bottom

    frases = sc._frases(deck)
    escolha = None
    motivo = "sem texto"
    for pt in HERO_ESCADA:
        f_t = sc.fonte_en("titulo", pt)
        tit_linhas = sc.balancear(d, titulo, f_t, C)
        if len(tit_linhas) > HERO_MAX_TITULO:
            motivo = (f"título pede {len(tit_linhas)} linhas a {pt} px (máximo "
                      f"{HERO_MAX_TITULO}) na coluna de {C} px")
            continue
        for n_deck in range(HERO_MAX_DECK, -1, -1):
            sel: list[str] = []
            if n_deck:
                acc: list[str] = []
                for fr in frases:
                    if len(sc.balancear(d, " ".join([*acc, fr]), f_deck, C)) <= n_deck:
                        acc = [*acc, fr]
                    else:
                        break
                sel = acc
            deck_linhas = sc.balancear(d, " ".join(sel), f_deck, C) if sel else []
            if len(deck_linhas) > n_deck:
                continue
            (_, cap_t, lh_t, t_bottom, rule_y,
             deck_base1, deck_bottom) = _geometria(pt, len(tit_linhas), len(deck_linhas))
            if deck_bottom <= limite:
                escolha = (pt, f_t, tit_linhas, sel, deck_linhas, cap_t, lh_t,
                           t_bottom, rule_y, deck_base1)
                break
            motivo = (f"bloco de {deck_bottom - rule_y:.0f} px invade o pé em "
                      f"{deck_bottom - limite:.0f} px a {pt} px com {len(deck_linhas)} "
                      f"linha(s) de deck")
        if escolha:
            break
    if escolha is None:
        raise ValueError(f"texto não cabe no hero {HERO_L}x{HERO_A}: {motivo}")

    (titulo_usado, f_tit, tit_linhas, deck_sel, deck_linhas, cap_t, lh_t,
     t_bottom, rule_y, deck_base1) = escolha

    # fail-closed: nada passa da coluna (é a zona de segurança que o card respeita)
    for l in tit_linhas:
        if d.textlength(l, font=f_tit) > C:
            raise ValueError(f"linha de título mais larga que a coluna de {C} px: {l!r}")
    for l in deck_linhas:
        if d.textlength(l, font=f_deck) > C:
            raise ValueError(f"linha de deck mais larga que a coluna de {C} px: {l!r}")

    # -------------------------------------------------------------- chrome do topo
    x = M
    for ch in sc.EN_TOPO_DIREITA:
        d.text((x, base_topo), ch, font=f_chrome, fill=sc.EN_TITULO, anchor="ls")
        x += d.textlength(ch, font=f_chrome) + 4.0
    larg_handle = d.textlength(sc.HANDLE_EN, font=f_chrome)
    if x + 48 + larg_handle > HERO_L - M:
        raise ValueError("chrome do topo colide: assinatura do site + handle")
    d.text((HERO_L - M - larg_handle, base_topo), sc.HANDLE_EN, font=f_chrome,
           fill=sc.EN_ACENTO, anchor="ls")

    # -------------------------------------------------------------- título + deck
    tit_base1 = tit_cap_top + cap_t
    for i, l in enumerate(tit_linhas):
        d.text((M, tit_base1 + i * lh_t), l, font=f_tit, fill=sc.EN_TITULO, anchor="ls")
    d.rectangle([M, rule_y, M + sc.MARK_W - 1, rule_y + 5], fill=sc.EN_ACENTO)
    y = deck_base1
    for l in deck_linhas:
        d.text((M, y), l, font=f_deck, fill=sc.EN_CORPO, anchor="ls")
        y += round(HERO_DECK_PT * HERO_DECK_LH_F)

    # -------------------------------------------------------------- pé
    d.text((M, pe_base), sc.SITE_EN, font=f_chrome, fill=sc.EN_LINK, anchor="ls")
    citacao = FONTE_AMOSTRA
    larg_cit = d.textlength(citacao, font=f_chrome)
    if d.textlength(sc.SITE_EN, font=f_chrome) + larg_cit + 48 > C:
        raise ValueError("pé do hero colide: site + fonte")
    d.text((HERO_L - M - larg_cit, pe_base), citacao, font=f_chrome,
           fill=sc.EN_CORPO, anchor="ls")

    saida.parent.mkdir(parents=True, exist_ok=True)
    img.save(saida, "PNG", optimize=True)

    return {
        "saida": saida,
        "layout": "x-hero",
        "dimensoes": [HERO_L, HERO_A],
        "margem": M,
        "col": C,
        "fundo": "grafismo" if com_fundo else "plano",
        "titulo_pt": titulo_usado,
        "deck_pt": HERO_DECK_PT,
        "linhas_titulo": [(l, round(d.textlength(l, font=f_tit), 1)) for l in tit_linhas],
        "linhas_deck": [(l, round(d.textlength(l, font=f_deck), 1)) for l in deck_linhas],
        "deck_descartado": len(frases) - len(deck_sel),
        "regua": {"y": rule_y, "h": 6, "w": sc.MARK_W},
        "bloco_fim": round(y - round(HERO_DECK_PT * HERO_DECK_LH_F) + desc_dk),
        "limite": limite,
        "pe_base": pe_base,
        "contrastes": {nome: round(sc.contraste(cor, sc.EN_FUNDO), 2)
                       for nome, cor in (("titulo", sc.EN_TITULO), ("corpo", sc.EN_CORPO),
                                         ("site", sc.EN_LINK), ("handle", sc.EN_ACENTO))},
        "fontes": dict(sc.FONTE_USADA),
    }


# ---------------------------------------------------------------- CLI
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="build-identidade-x")
    ap.add_argument("--saida", default=str(RAIZ / "docs"))
    ap.add_argument("--pipeline", default=str(PIPELINE_PADRAO))
    a = ap.parse_args(argv)

    sc = carregar_pipeline(Path(a.pipeline).expanduser())
    destino = Path(a.saida).expanduser()
    destino.mkdir(parents=True, exist_ok=True)

    relatos = []
    for nome, spec in AMOSTRAS.items():
        relatos.append(card_16x9(sc, spec, destino / nome))
    for nome, spec in HEROES.items():
        relatos.append(hero(sc, spec["titulo"], spec["deck"], destino / nome,
                            com_fundo=spec["fundo"]))

    for m in relatos:
        pt = m.get("titulo_pt")
        nt = len(m["linhas_titulo"])
        nd = (len(m.get("linhas_deck") or []) if "linhas_deck" in m
              else sum(len(b["linhas"]) for b in m.get("blocos") or []))
        print(f"{Path(str(m['saida'])).name}: {m['dimensoes'][0]}x{m['dimensoes'][1]} · "
              f"margem {m['margem']} · título {pt} px ({nt} linha(s)) · "
              f"corpo {m['corpo_pt'] if 'corpo_pt' in m else m.get('deck_pt')} px "
              f"({nd} linha(s)) · {m.get('fundo', 'plano')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
