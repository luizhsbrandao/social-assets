# Identidade visual X — card 16:9 e hero de artigo

Superfície **EN** (`intelligencenotes.com`) — card de post no X e hero de artigo. Card `t_591d5106`
(perfil `design`), filho de `t_60ddb68d`.

**Proveniência.** Isto não é proposta de estilo: é a identidade **já em produção**, medida. Os três
cards 16:9 desta pasta saem do instrumento `lib/social_card.py::render_en` do `social-pipeline`
(branch `dev/x-card-t_60ddb68d`), o mesmo que produziu os 8 cards reais da 2026-W48. O hero sai do
compositor `tools/build-identidade-x.py::hero` deste repo — divergência declarada em §7, com o
número que a justifica. Texto de amostra: os PNGs são **espécimes** (a linha de fonte diz
`specimen · EN identity v1`); nenhum texto é conteúdo publicado nem citação de terceiro.

## 1. Tokens

Fonte única: `sites-plataforma/sites/intelligencenotes/quartz.config.ts`, bloco `colors.darkMode`
(é o que o site serve). O `PIA/Design/Brand-Sheets.md` §1 registra os mesmos valores; não foram
lidos do vault — foram conferidos no config do site, que é código.

| token | hex | onde | contraste sobre `#040610` |
|---|---|---|---|
| fundo noturno (`light`) | `#040610` | todo o canvas | — |
| corpo (`darkgray`) | `#c8d3d6` | corpo, linha de fonte | **13,23:1** |
| título (`dark`) | `#5ea5cf` | título, `INTELLIGENCE NOTES` | **7,47:1** |
| link (`secondary`) | `#3daee9` | domínio no pé | **8,12:1** |
| acento (`tertiary`) | `#00f2ff` | handle, régua do título | **14,58:1** |
| mudo (`gray`) | `#8a9ba5` | metadado secundário (reserva) | **7,04:1** |

Sétimo hex da mesma paleta, estrutural e não de tinta: painel `#0c1018` (1,06:1 sobre o fundo — só
serve a bloco/inset, nunca a texto).

Derivadas (não são token: são o token reduzido sobre o fundo):
filete `#2f333c` = corpo a 22% (1,60:1 — separador **decorativo**, isento do 3:1 de 1.4.11; não
carrega informação) e véu do hero-02 = fundo a 90→38% da esquerda para a direita.

**Âmbar não entra.** A paleta âmbar da Intellecta e o azul `#003F68` do NEGISC são de outras
superfícies: neste card não há exceção, nem em degradê, nem em ícone, nem em selo. Âmbar sobre
near-black dá 9,7:1 e seria o elemento mais chamativo da peça — é exatamente por isso que está fora.

## 2. Grade e margens

Margem é **proporção**, não número solto: **96 px em 1080 de largura = 8,889%**.

| alvo | canvas | margem | coluna útil |
|---|---|---|---|
| card de post (thread / long post) | 1600×900 | **142 px** | 1316 px |
| hero de artigo (1,91:1) | 1200×628 | **107 px** | 986 px |

Medido nos cinco PNGs: card 142/142/142/146 (a base fecha 4 px abaixo por descendente); hero
107/108/107/102. Nenhuma tinta cruza a margem, nenhuma toca a borda.

O bloco é **ancorado no topo**, como na série publicada: filete do topo em y=201, título a partir de
y=231, corpo abaixo da régua, pé ancorado no fundo. O vazio do terço inferior é do template — é ele
que deixa o título respirar e mantém o olho no mesmo ponto de entrada em todo card da série. Não
centralize o bloco: distribuir no vazio faz o título mudar de altura de card para card.

## 3. Hierarquia tipográfica

| nível | fonte | corpo | entrelinha | linhas |
|---|---|---|---|---|
| título | JetBrains Mono **Bold** | escada **72 / 64 / 56 / 48** px | 1,16 | ≤ 3 |
| corpo | Inter **Regular** | **38** px | 1,42 | ≤ 4 (medido: 2–3) |
| handle | JetBrains Mono Regular | **30** px | — | 1 |
| pé (domínio + fonte) | JetBrains Mono Regular | **32** px | — | 1 |

A escada desce até caber e **nunca trunca palavra**: o que não cabe em 3 linhas a 48 px é erro de
conteúdo (recusa declarada pelo renderizador), não convite a reduzir a pó. A quebra é balanceada,
com guarda de viúva — a última linha nunca fica abaixo de 50% da maior.

**Piso de ocupação da coluna.** Medido nos 8 cards publicados da 2026-W48, a linha mais larga do
título ocupa **65,0% a 99,0%** da coluna (mediana ~89%); o card que a auditoria `t_be3a5ff7`
reprovou era justamente o de 65,0%. Trate < 70% como outlier. Os três espécimes desta pasta:
74,5% (thread-01, título de uma linha), 88,0% (thread-02), 82,1% (longo-01). Corpo: 86,9%/78,0% e
98,6% — corpo de thread pode ser mais curto que o título; o do long post acompanha a coluna.

Régua sob o título: **96 × 6 px** no acento — é o mesmo módulo da marca da casa, não um traço
arbitrário. Filete do topo e do pé: 1 px, dentro da margem.

## 4. Tamanho mínimo legível (px efetivos)

O X mostra a imagem do post na largura da coluna: **~600 px** no desktop, **~390 px** no celular
(faixa 375–430). Piso funcional adotado: **10 px efetivos**.

| nível | canvas | 320 px | 390 px | 600 px | largura mínima p/ 10 px |
|---|---|---|---|---|---|
| título | 72 | 14,6 | 17,8 | 27,0 | 222 px |
| corpo | 38 | **7,4** | **9,0** | 14,3 | 421 px |
| pé | 32 | 6,4 | 7,8 | 12,0 | 500 px |
| handle | 30 | 6,0 | 7,3 | 11,3 | 533 px |

Hero (canvas 1200): título 19,4 / 23,7; deck 12,3 / 15,0; chrome 7,3 / 8,9.

**Fato e consequência.** No celular só o título passa o piso: o corpo fica em 9,0 px a 390 e o pé em
7,8. O card 16:9 é **capa** — no feed lê-se o título, e o corpo é apoio para quem abre em tela cheia
ou lê no desktop. A redação do título é, portanto, decisão editorial com peso: é o único texto
garantido no celular.

**Projeção, se a frente exigir corpo legível no celular:** corpo ≥ 48 px (11,7 px a 390) e pé ≥ 42 px
(10,2 px a 390). Custo medido: cada 10 px de corpo tiram ~1 linha do corpo e o título perde a
terceira linha — o card passa a aceitar título de 2 linhas e corpo de 2. **Lacuna do dono:** os 8
cards publicados da 2026-W48 usam 38 px; mudar é decisão da frente, não deste card.

## 5. Handle e pé

- Handle **`@LuizHSBrandao`**, caixa exata, JetBrains Mono 30 px, **acento `#00f2ff`**, no canto
  superior esquerdo. É a única assinatura pessoal da peça; não se abrevia, não se põe em caixa-alta,
  não se repete no pé.
- Canto superior direito: **`INTELLIGENCE NOTES`** em caixa-alta, tracking 4, título `#5ea5cf`.
- Pé: **`intelligencenotes.com`** à esquerda em link `#3daee9`; **linha de fonte** à direita em corpo
  `#c8d3d6`, no formato curto de referência — `Fonte, ano` (ex.: `OpenAI, 2026`, `NATO, 2022`).
  Quando não há fonte, a linha diz o que a peça é (`specimen · …`); **não se inventa citação**.
  O pé é uma linha só: domínio + fonte não podem colidir (o renderizador recusa).
- Sem logo, sem lockup institucional, sem URL de outra frente. A assinatura de terceiro não entra
  neste canvas (ver §8).

## 6. Contraste e recorte

- Toda tinta de texto da peça fica **≥ 7,0:1** (título 7,47; corpo 13,23; link 8,12; acento 14,58;
  mudo 7,04) — acima do 4,5:1 de texto pequeno e acima do 7:1 de AAA. Filete é decorativo: 1,60:1.
- Sobre grafismo (hero-02) o contraste é medido na **cor composta**: pior caso 7,17:1 (título),
  12,80:1 (corpo), 14,10:1 (acento). O véu de fundo existe para isso — não confie no grafismo.
- **16:9 → card de link.** X exibe o post em 16:9 e recorta `summary_large_image` em **1,91:1**:
  1600×900 → 1600×838, ou seja **31 px por lado**. A margem de 142 px (4,6× o recorte) garante que
  nenhum texto se perde no crop. Nunca aproxime texto da borda "porque no post cabe".
- **Hero 1200×628 já é 1,9108:1** — é o formato de `og:image`/hero de artigo; não recortar.

## 7. Divergência declarada

**O hero não passa por `render_en`.** Sonda com o instrumento no canvas 1200×628: as bandas do card
16:9 reservam ~163 px de topo e ~191 px de pé, e o corpo saiu com **0 linhas em 4 de 5 casos** — no
formato 1,91:1 o card não cabe dentro do próprio template. O compositor do hero usa bandas próprias
(topo em y=107, bloco a 167, pé ancorado em y=521) com a mesma margem proporcional, as mesmas fontes,
os mesmos tokens e o mesmo módulo de régua (96×6). O que difere: chrome a 26 px, deck em Inter 48 px
(≤2 linhas), sem filetes de topo/pé. **O instrumento não sabe gerar hero** — card de `dev` aberto
para `render_hero` no `social_card.py`, usando este compositor como spec.

**Premissas do gate que não valem para esta superfície** (medido, não desculpa):

1. `medir_card:contraste` escolhe a tinta como a **cor modal mais escura** da faixa. Em card de fundo
   escuro essa cor é a borda antialias do glifo (`#090F1B`), não a tinta — daí o 1,05:1 repetido em
   todo texto. Isolando o glifo por distância ao fundo, as tintas reais medem 7,47 / 13,23 / 8,12 /
   14,58:1. Defeito do motor em superfície invertida (escuro-sobre-claro assumido); card de correção
   aberto para `dev`.
2. `leitura-feed` mede px efetivos a **320 px** de exibição. Para card de X o número honesto é a
   largura da coluna (~390 no celular, ~600 no desktop) — a §4 traz as duas colunas.
3. `corte: tinta toca a borda` no hero-02 é a definição de fundo full-bleed; o texto está a 107 px
   da borda em todos os lados.

## 8. O que nunca aparece

- Âmbar da Intellecta (nem em selo, ícone ou gradiente).
- Símbolo/wordmark **NEGISC**, `IREL | UnB`, marca do GEPSI, papel `#F7F5F0` e o azul `#003F68`.
- Logo, nome ou cor da **Intellecta** em qualquer forma.
- Emoji, gradiente multicolor, sombra, contorno, textura de "IA" (brilho, partícula, orbe).
- Citação, dado, valor, nome de pessoa ou material não publicado: card não é veículo de conteúdo
  sensível. PII não entra na peça nem no prompt que a gera.

## 9. Como regenerar e conferir

```
python3 tools/build-identidade-x.py            # docs/*.png + relatório por peça
sha256sum -c docs/identidade-x.sha256          # 5 × OK
file docs/x-card-thread-01.png                 # 1600 x 900
file docs/x-hero-artigo-01.png                 # 1200 x 628
```

Determinístico: mesmo texto + mesmas opções ⇒ mesmos bytes. Sem rede, sem IA, sem relógio, sem API
de imagem paga (ADR-0070) — o fundo do hero-02 é desenhado em Pillow a partir da paleta.
