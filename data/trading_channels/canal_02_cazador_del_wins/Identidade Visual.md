# EL CAZADOR DEL WINS — Identidade Visual

**Versão:** 1.1 · **Data:** 21/09/2026 · **Canal:** 2 de 3 da rede Trading Labs

**Obedece a:** `02-biblia-arquetipica.md` (seções 4, 5 e 8)

**Herda de:** Placar v2 (Bot a Prueba) — placar mono, linguagem de anotação manual, robô mascote

**Referência de embalagem:** CR TRADER (rosto à direita, título em bloco, mascote, número concreto)

---

## 1. Resumo em uma frase

> A embalagem de canal de guru — rosto grande, robô, título em bloco — virada do avesso: o rosto está na sombra, o robô está quebrado dentro de uma mira, e o número em destaque é o drawdown circulado à caneta.

## 2. Direção e os três sinais

Direção única: **noturna, controlada, cirúrgica.** Escuro não é estética de hacker; é sala de vigilância. Tudo é nítido, nada brilha.

Os três sinais que identificam o canal em 0,3 s numa grade de thumbs, em ordem de leitura:

1. **O capuz** — personagem humano e fotorealista, silhueta escura, rosto na sombra e fino recorte amarelo-ácido na borda. Lado direito, sempre.
    
2. **A mira** — retículo amarelo-ácido fino com o robô quebrado dentro. É o emblema do canal e deve permanecer gráfico, preciso e sem glow.
    
3. **O vermelho circulado** — drawdown do registro com círculo à caneta.
    

Se a thumb tem os três, é do canal. Se tem dois, revisar. Se tem um, está errada.

## 3. Paleta (5 cores, invariáveis)

| Token | Hex | Papel | Regras |

|---|---|---|---|

| `--cz-bg` | `#0A0B0E` | Fundo | Mais escuro que o Placar v2 (`#0E0F12`). Todo fundo de thumb, card, registro. Nunca preto puro |

| `--cz-fg` | `#EDEDED` | Texto | Texto corrido, títulos em bloco, números neutros do registro |

| `--cz-accent` | `#D8F200` | Acento (marca) | Aro do capuz, mira, wordmark, anotações e uma palavra por thumb. **É a única cor de assinatura da marca** |

| `--cz-green` | `#2FBF71` | Dado positivo | Só números do registro e o selo `ATRAPADO`. Nunca decorativo, nunca em fundo |

| `--cz-red` | `#D9403A` | Dado negativo | Só números do registro, selo `ESCAPÓ`, faixa de veredito. **Obrigatório em toda thumb** |

Suporte (não conta como cor): `--cz-muted` `#7A7D86` para labels do registro e metadados; `--cz-line` `rgba(237,237,237,0.10)` para bordas.

**Proibido:** gradientes decorativos, glow, neon, azul como cor de marca, dourado, verde-dinheiro, imagem de dinheiro, seta gráfica genérica, fogo literal, matrix/código caindo. Luz neutra de monitor pode existir no ambiente, sem virar acento visual.

**Sobre o acento amarelo-ácido:** texto sobre `--cz-accent` é sempre `--cz-bg`, nunca branco. O acento aparece em no máximo 3 pontos fortes por thumb — normalmente o aro do capuz, a mira e a palavra/gesto de marca. Ele deve parecer pigmento editorial ou luz de recorte controlada, **nunca neon, glow ou iluminação radioativa**.

## 4. Tipografia (3 famílias, cada uma com função fixa)

| Família | Token | Função | Onde pode | Onde não pode |

|---|---|---|---|---|

| **JetBrains Mono** 700 | `--cz-font-mono` | Dado, registro, wordmark, título em bloco | Registro, thumbs, cards de bloco, lower third, wordmark | Texto corrido |

| **Inter** 400/600 | `--cz-font-sans` | Texto corrido, legendas, descrição | Legendas, end card, descrição | Thumbs, registro |

| **Caveat** 700 | `--cz-font-hand` | A caneta do Cazador | Anotação em thumb, círculo/seta, aparte em lower third | Registro, título, wordmark, legenda, qualquer dado |

**Regra da caneta:** Caveat nunca carrega informação que precise ser verificada. Ela reage ao dado, não é o dado. `escapó el día 9` sim; `-34%` em Caveat, nunca.

Tamanhos de referência (thumb 1280×720):

- Título em bloco: 140–170 px, mono 700, caixa alta, tracking −2%
    
- Palavra em acento: mesma linha, mesmo tamanho
    
- Anotação à caneta: 60–80 px, rotação −4° a −8°
    
- Registro compacto: labels 22 px muted, valores 34 px
    

## 5. Wordmark e emblema

### 5.1 Wordmark

```

EL CAZADOR

DEL WINS

```

- JetBrains Mono 700, caixa alta, tracking −3%, duas linhas alinhadas à esquerda.
    
- **"WINS"** em `--cz-accent`; o resto em `--cz-fg`.
    
- Um círculo à caneta (Caveat-stroke, 3–4 px, `--cz-accent`, levemente aberto) envolvendo **"WINS"** — a única palavra caçada.
    
- Versão uma linha (lower third, marca d'água): `EL CAZADOR DEL WINS` com "WINS" em `--cz-accent`, sem círculo.
    
- Tamanhos: `sm` 14 px (marca d'água) · `md` 28–40 px (lower third, end card) · `lg` 64–120 px (banner, intro).
    

**Proibido:** itálico, caixa baixa, ícone de alvo dentro da letra, efeito de "texto rasgado", qualquer fonte que não seja JetBrains Mono.

### 5.2 Emblema

Retículo de mira: quatro traços finos (2 px em 64 px) em `--cz-accent` com abertura no centro, e dentro dele a silhueta do robô quebrado em `#3A3D46`. Referência gerada: `/cazador/emblema.png`.

Usos: avatar de perfil do YouTube (sobre `--cz-bg`), marca d'água em vídeo (canto superior esquerdo, 5% da largura, opacidade 70%), favicon, selo no template do Telegram.

**Nunca:** mira com o Cazador dentro (ele é quem mira, não o alvo). Nunca mira sobre rosto de pessoa real.

## 6. O Cazador (avatar)

Referência visual oficial: personagem humano fotorealista do board v1.1 — capuz preto, rosto parcialmente oculto, pele e barba reais, iluminação de sala de monitoramento, recorte amarelo-ácido controlado.

### 6.1 Ficha visual fixa (prompt-base para todas as poses)

```
Photorealistic cinematic portrait of a believable Latin American man, age 32-38,
black hoodie with hood UP, realistic heavyweight cotton fabric and natural folds,
face mostly hidden by deep hood shadow; eyes never visible; only nose edge,
cheeks, lips, lower jaw and short natural beard stubble partially readable.

Real human skin texture with pores, subtle imperfections, natural beard density,
realistic lips, realistic jaw anatomy, no beauty retouching, no waxy skin,
no plastic CGI face, no videogame character look, no superhero styling.

Serious controlled expression, closed mouth, no smile.
Thin acid yellow-green (#D8F200) practical rim light tracing only selected parts
of the hood and right shoulder edge; no glow halo and no neon spill.

Very faint neutral cool-white monitor light from the left, never blue-saturated.
Dark charcoal surveillance / trading-monitor room (#0A0B0E) with 2-3
out-of-focus screens in the background. Screens may contain abstract
red/green market charts but no readable third-party branding.

Chest-up portrait, high dynamic range, cinematic full-frame camera realism,
50-85mm portrait-lens feel, realistic depth of field, physically believable
lighting, restrained contrast, subtle film grain, sharp facial microtexture.

No text, no mask, no visible eyes, no glowing eyes, no smile, no cyberpunk,
no neon room, no glossy 3D render, no artificial skin, no exaggerated muscles.
```

**Princípio de realismo:** o Cazador deve parecer uma pessoa filmada por uma câmera real dentro de uma sala escura — não um avatar, personagem de videogame ou render 3D.

O que muda entre poses: **só braços/mãos, ângulo da cabeça e microexpressão da boca/maxilar.** Rosto, idade aparente, barba, estrutura facial, roupa, luz, lente e ambiente permanecem consistentes.

### 6.2 As 6 poses

|#|Pose|Uso principal|Nota|
|---|---|---|---|
|1|Braços cruzados, cabeça baixa|Thumbs de veredito · padrão|Referência oficial|
|2|Apontando para a câmera|Thumbs de pergunta|Dedo em foco, rosto na sombra, anatomia realista|
|3|Mão em "pare", palma para a câmera|Thumbs de alerta|Mão humana nítida com leve recorte `--cz-accent`|
|4|Mão no queixo|Thumbs de La Trampa|Único momento com maxilar um pouco mais legível|
|5|Segurando o robô quebrado|Thumbs de troféu|Robô no nível do peito; sem faísca fantasiosa|
|6|De costas, olhando monitor|Intro · end card · banner|Fino recorte `--cz-accent` no contorno do capuz|

### 6.3 Regras do avatar

- **Fotorealismo obrigatório.** Pele, barba, mãos, tecido e iluminação precisam parecer captados por câmera real.
    
- **Rosto nunca completo.** Se uma geração mostra os olhos, descartar. O limite é o nariz e parte das maçãs do rosto.
    
- **Nunca sorri.** Nem na boca visível.
    
- **Capuz sempre levantado.** Sem exceção, nem "revelação" futura.
    
- **Mesma pessoa em todas as poses.** Não variar idade, barba, formato do nariz, mandíbula ou tom de pele.
    
- **Ocupa 35–40% da largura** da thumb, lado direito, cortado no peito.
    
- **Em vídeo:** só PiP 15% (hook e veredito) e end card. Nunca tela cheia, salvo abertura vertical prevista no §10.7.
    
- **Sem tratamento de recorte:** sem contorno branco, drop shadow, halo ou glow. Ele está _na_ cena, não colado sobre ela.
    
- **Mãos precisam ser anatomicamente corretas.** Sem dedos extras, deformações ou poses impossíveis.
    
- **Iluminação:** `--cz-accent` funciona apenas como rim light controlado; não colore a pele inteira.
    
- **Monitores:** desfocados, sem logos de terceiros, sem textos legíveis que possam parecer evidência.
    
- **Proibido:** aparência de CGI, pele encerada, face perfeita demais, cyberpunk, máscara, olhos brilhantes, tatuagens adicionadas pela IA, sorriso, pose de influencer.
    

## 7. O robô (mascote-alvo)

Referência gerada: `/cazador/bot-roto.png` (herdado de `/canal2/bot-roto.png`).

- Robô retro caixote, cinza-fosco `#3A3D46`, uma pequena luz indicadora em `--cz-accent`, rachado ou caído, com peças e parafusos soltos. Sem expressão humana e sem efeitos fantasiosos.
    
- **Sempre "sofrendo":** quebrado, caído, fumaçando, dentro da mira. Nunca inteiro e feliz — inteiro é o robô da referência.
    
- Na thumb: 16–20% da largura, base, entre o registro e o Cazador. Dentro da mira quando o veredito é `ESCAPÓ`; fora dela, apenas caído, quando é `ATRAPADO` (o Cazador pegou algo, o robô sobreviveu parcialmente).
    
- Nunca antropomorfizar além do básico: sem olhos expressivos, sem boca, sem bracinhos gesticulando.
    

## 8. O Registro de Caça (ex-placar)

Componente herdado do Placar v2, com dois ajustes de rótulo e um de veredito.

### 8.1 Estrutura (6 campos, ordem fixa)

```

REGISTRO DE CAZA                        [ESCAPÓ]

PERÍODO       14 días

OPERACIONES   184

ACIERTOS      61%

PAYOUT        82%

DRAWDOWN      -34%          ← --cz-red, sempre

SALDO DEMO    $1.000 → $1.140

```

- Título `REGISTRO DE CAZA` em mono 700, `--cz-muted`.
    
- Selo de veredito no canto superior direito: `ESCAPÓ` (fundo `--cz-red`, texto `--cz-bg`) ou `ATRAPADO` (fundo `--cz-green`, texto `--cz-bg`). Um terceiro estado, `CONDICIONAL` (borda `--cz-accent`, sem fundo), para "atrapa si".
    
- Versão **compacta** (thumb, lower third): 4 campos — PERÍODO, ACIERTOS, DRAWDOWN, SALDO. Drawdown nunca sai.
    
- Versão **troféu** (tela cheia, bloco 6): 6 campos, 60% da largura, centralizado, fundo `--cz-bg`, sem nada mais na tela.
    

### 8.2 Tratamento "cartão de caça"

- Rotação −2°, fita adesiva no topo (retângulo `--cz-fg` a 25% de opacidade, 60×14 px).
    
- Círculo de risco em `--cz-red`, 4 px, irregular e levemente aberto, em volta do DRAWDOWN. Sempre. O vermelho marca falha/risco; `--cz-accent` fica reservado para a assinatura do Cazador.
    
- Opcionalmente, um risco em `--cz-red` sobre o valor de ACIERTOS quando o veredito for `ESCAPÓ` e a taxa parecer boa — a marcação de risco contradiz o dado bonito.
    

### 8.3 Animação (Remotion)

- Entrada: campos aparecem um a um, 120 ms entre eles, de cima para baixo. Drawdown entra por último com 400 ms de atraso.
    
- Círculo de risco vermelho: traçado em 500 ms, easing `ease-out`, depois do drawdown.
    
- Selo de veredito: aparece com um corte seco (sem fade) 200 ms após o círculo.
    
- Durante a caça: valores atualizam com corte seco. Nenhum número faz "contagem" animada.
    
- Troféu final: 2 s de silêncio total, sem música, antes do CTA.
    

## 9. Thumbnail (template de 5 slots)

Formato 1280×720. Fundo `--cz-bg` com vinheta muito sutil nas bordas (máx. 15%).

```

┌──────────────────────────────────────────────────────────────┐

│ [A] EL CAZADOR DEL WINS (sm, marca d'água)                    │

│                                                               │

│ [B] TÍTULO EM BLOCO                          [E]              │

│     LINHA 1 (fg)                          CAZADOR             │

│     LINHA 2 (uma palavra em acento)          pose N             │

│                                            35-40%             │

│       [D] anotação à caneta ↘                                 │

│ [C] REGISTRO           [robô na mira]                         │

│     compacto, −2°                                             │

└──────────────────────────────────────────────────────────────┘

```

| Slot | Conteúdo | Regras |

|---|---|---|

| **A** | Wordmark uma linha, 14 px, opacidade 70% | Canto superior esquerdo, 5% da largura |

| **B** | Título em bloco, 2 linhas, mono 700, caixa alta, máx. 5 palavras | Uma palavra em `--cz-accent`. Sempre pergunta ou veredito. Nunca promessa |

| **C** | Registro compacto rotacionado −2° com círculo vermelho no drawdown | 40–44% da largura, base esquerda |

| **D** | Anotação à caneta (Caveat), 60–80 px, −4° a −8° | Uma só. Do banco aprovado (§11). Aponta para o robô ou para o drawdown |

| **E** | Cazador, pose conforme tipo de vídeo | 35–40%, direita, cortado no peito. Sem tratamento |

| — | Robô quebrado dentro da mira | 16–20%, base, entre C e E |

Faixa de veredito opcional: retângulo `--cz-red` inclinado −6° com `ESCAPÓ` em `--cz-bg`, atravessando o canto inferior direito por cima do Cazador. Só em thumbs de resultado.

### 9.1 Fórmulas de título por formato

| Formato | Padrão | Exemplos |

|---|---|---|

| La Cacería (pergunta) | `¿[AFIRMACIÓN]?` + `[CAZADOR pose 2]` | `¿FUNCIONA O ES ESTAFA?` · `¿ESTE BOT ATRAPA EL WINS?` |

| La Cacería (veredito) | `[N DÍAS] · [RESULTADO]` + `[pose 1]` | `14 DÍAS · ESCAPÓ` · `30 DÍAS · −41%` |

| La Trampa | `LO ARMÉ [CONDIÇÃO]` + `[pose 4]` | `LO ARMÉ SIN PROGRAMAR` · `LA TRAMPA DESDE CERO` |

| El Rastro | `EL BOT DE [PREÇO/AFIRMAÇÃO]` + `[pose 3]` | `EL BOT DE $997` · `"$500 AL DÍA" · RASTREADO` |

| Alerta | `NO CARGUES ESTO` + `[pose 3]` | `NO CARGUES ESTO` · `ANTES DE CARGARLO, MIRA` |

Sempre: dias em vez de dinheiro; drawdown em vez de lucro; pergunta em vez de afirmação; "¿ESTAFA?" só com interrogação.

## 10. Aplicações em vídeo

### 10.1 Intro (2 s)

Fundo `--cz-bg`. A mira se desenha (4 traços, 400 ms). O robô aparece dentro dela com corte seco. Wordmark `lg` entra abaixo, "WINS" em `--cz-accent`, e o círculo de marca ao redor de "WINS" se traça em 500 ms. Som: um clique metálico único, sem música. Corta direto para a carnada.

### 10.2 PiP do Cazador

Retângulo 15% da largura, canto inferior direito, borda 1 px `--cz-line`, sem arredondamento além de 4 px. Aparece com corte seco. Pose 1 no hook, pose 1 ou 2 no veredito. Máximo 20 s no hook, 30 s no veredito.

### 10.3 Cards de bloco (1 s, tela cheia)

Fundo `--cz-bg`. Nome do bloco em mono 700, 96 px, `--cz-fg`, centralizado: `LA CARNADA` · `LA TRAMPA` · `POR DENTRO` · `LA CACERÍA` · `AQUÍ ESCAPÓ` (em `--cz-red`) · `AQUÍ LO ATRAPAMOS` (em `--cz-green`) · `EL TROFEO` · `VEREDICTO`. Linha fina `--cz-accent` de 120 px abaixo do texto. Corte seco na entrada e na saída.

### 10.4 Lower third

Faixa inferior esquerda, fundo `--cz-bg` a 90%, borda esquerda 3 px `--cz-accent`. Linha 1: wordmark `md`. Linha 2: contexto em Inter 600 (`Deriv · Volatility 75 · M5 · demo`). Opcionalmente uma anotação à caneta acima da faixa (`escapó el día 9`), −5°.

### 10.5 Registro durante a caça

Compacto, canto inferior direito (quando o PiP não está), sem rotação, sem fita — durante a caça ele é instrumento, não troféu. Vira "cartão" só no bloco 6.

### 10.6 End card (últimos 15 s)

Fundo `--cz-bg`. Esquerda: Cazador pose 6 (de costas), 40% da altura. Centro: dois slots de vídeo do YouTube com borda `--cz-line`. Direita, em Caveat 72 px `--cz-accent`, −5°: `monta la trampa →` apontando para o slot do Telegram. Abaixo, em mono `--cz-muted`: `t.me/lacaceria`.

### 10.7 Vertical 9:16 (Trofeo)

Fundo `--cz-bg`. Topo 20%: título em bloco 2 linhas. Meio 55%: replay do gráfico. Base 25%: registro compacto sem rotação + faixa de veredito. Cazador pose 2/3 nos 3 primeiros segundos em tela cheia recortada no peito; depois sai. Anotação à caneta aparece no momento exato do "aquí escapó".

### 10.8 Banner do canal (2560×1440, área segura 1546×423)

Fundo `--cz-bg`. Esquerda da área segura: Cazador pose 6, cortado, ocupando toda a altura. Centro-direita: wordmark `lg` em duas linhas, "WINS" circulado. Abaixo, Inter 600 `--cz-muted`: `Cazamos el bot que te prometieron.` Nada mais. Sem "inscreva-se", sem sino, sem leão.

### 10.9 Avatar de perfil

Emblema (mira + robô) sobre `--cz-bg`, mira ocupando 70% do círculo. Não usar o rosto do Cazador no perfil — a mira é mais legível em 48 px e mantém o mistério.

## 11. A caneta do Cazador

A identidade passa a ter **dois gestos manuais diferentes**, com funções que não podem ser confundidas:

- **Caneta do Cazador (**`**--cz-accent**`**)** → comentário, observação, direção de leitura, assinatura.
    
- **Marcação de risco (**`**--cz-red**`**)** → falha, perda, drawdown, fuga, evidência negativa.
    

### 11.1 Regras da caneta de comentário

1. **Uma anotação por tela.** Nunca duas.
    
2. **Reage, não informa.** Comenta o dado; nunca substitui o dado.
    
3. **Sempre** `**--cz-accent**` **(**`**#D8F200**`**)**, 3–4 px, traço levemente aberto.
    
4. **Rotação −4° a −8°.** Nunca reta, nunca exageradamente inclinada.
    
5. **Aponta para algo:** pequeno gesto, sublinhado ou seta manual ligando a frase ao robô, condição ou área relevante.
    
6. **Só em Caveat 700.** Nenhuma outra fonte manuscrita.
    
7. O traço deve parecer **marcador editorial real**, não neon. Sem glow.
    

### 11.2 Regras da marcação de risco

1. **Sempre** `**--cz-red**` **(**`**#D9403A**`**)**.
    
2. Usada para círculos, riscos ou marcações que identifiquem drawdown, falha, perda ou `ESCAPÓ`.
    
3. O DRAWDOWN deve continuar numericamente vermelho e pode receber o círculo vermelho.
    
4. Não usar vermelho para comentário casual; vermelho é consequência, não decoração.
    
5. Máximo de uma marcação de risco dominante por quadro.
    

### 11.3 Banco inicial de anotações (10 aprovadas)

|Frase|Quando|
|---|---|
|`escapó el día 9`|Thumb de veredito, apontando para a área do drawdown|
|`esto no estaba en el video de ellos`|Thumb, apontando para a evidência negativa|
|`la carnada`|Apontando o robô|
|`mira la condición`|Veredito ATRAPADO/CONDICIONAL|
|`14 días. sin cortes.`|Thumb de La Cacería|
|`$997 por esto`|El Rastro, apontando o robô (preço, não pessoa)|
|`lo armé yo. sin código.`|La Trampa|
|`no lo cargues todavía`|Alerta|
|`con el rojo`|Troféu|
|`monta la trampa →`|End card|

### 11.4 Proibidas

Qualquer frase com dinheiro ganho, "gana", "fácil", "garantizado", nome de pessoa, @, "estafa" afirmativo, emoji, ponto de exclamação duplo, frases sobre o público ("tú también caíste").

## 12. Motion e som

- **Cortes secos** em tudo. Nenhum fade, nenhum wipe, nenhum zoom-in dramático de título.
    
- **Zoom** só no gráfico, máx. 1,8×, sempre retornando ao enquadramento original.
    
- **Ritmo:** o vídeo respira no ritmo da voz (145–155 ppm). Sem B-roll de dinheiro, sem stock footage.
    
- **Som:** um clique metálico na intro; um "tick" seco a cada campo do troféu; silêncio absoluto por 2 s no troféu final. Sem trilha durante o registro. Trilha, se houver, só na caça (bloco 4), grave, sem melodia, −24 dB.
    
- **Vermelho piscando, alarme, glitch, glow ácido ou iluminação cyberpunk:** nunca. Autoridade é quietude.
    

## 13. Checklist de publicação (thumb + vídeo)

- Cazador fotorealista: capuz na sombra, lado direito, sem olhos visíveis, sem sorriso, pele/mãos/tecido naturais
    
- Robô quebrado presente (na mira se ESCAPÓ)
    
- Drawdown vermelho visível e circundado por marcação de risco vermelha
    
- Título: pergunta ou veredito, ≤ 5 palavras, no máximo uma palavra em `--cz-accent`
    
- No máximo uma anotação em `--cz-accent`, do banco aprovado, apontando para algo
    
- Zero: dinheiro, seta, azul, glow, nome próprio, @, logo de terceiro, "estafa" sem interrogação
    
- Wordmark `sm` no canto superior esquerdo
    
- Máximo 3 pontos fortes de `--cz-accent` na thumb
    
- Vídeo: PiP ≤ 20 s no hook, cards de bloco presentes, troféu em tela cheia com 2 s de silêncio
    
- Vídeo: nenhum rosto de terceiro, nenhum print com nome ou @ legível
    

## 14. Tokens (CSS de referência)

```

:root {

  --cz-bg: #0A0B0E;

  --cz-fg: #EDEDED;

  --cz-accent: #D8F200;

  --cz-green: #2FBF71;

  --cz-red: #D9403A;

  --cz-muted: #7A7D86;

  --cz-line: rgba(237, 237, 237, 0.10);

  

  --cz-font-mono: 'JetBrains Mono', ui-monospace, monospace;

  --cz-font-sans: 'Inter', system-ui, sans-serif;

  --cz-font-hand: 'Caveat', cursive;

  

  --cz-tilt: -2deg;        /* cartão de caça */

  --cz-hand-tilt: -6deg;   /* anotação */

  --cz-stroke: 4px;        /* caneta */

  --cz-radius: 4px;        /* único raio permitido */

}

```

## 15. Arquivos de referência gerados

| Arquivo | Conteúdo |

|---|---|

| `/cazador/avatar-v1.1.png` | Cazador fotorealista, pose 1 |

| `/cazador/emblema-v1.1.png` | Mira em `--cz-accent` com robô quebrado |

| `/canal2/bot-roto.png` | Robô quebrado |

| `/placar/bot-mascota.png` | Robô caído com fumaça (alternativa) |  
| `/cazador/identity-board-v1.1.png` | Board oficial: personagem humanizado + acento `#D8F200` |

Próximos a gerar: poses 2–6 do **mesmo Cazador fotorealista**, banner, template de thumb com slots, Registro de Caça em Remotion, pacote de anotações `--cz-accent` em SVG e pacote de marcações de risco `--cz-red`.

---

_Fim do documento. A versão 1.1 consolida o Cazador fotorealista/humanizado e substitui o antigo laranja pelo acento amarelo-ácido_ `_#D8F200_`_. Alterações futuras de paleta, tipografia ou regras do avatar exigem revisão da Bíblia §4 e §8 em conjunto._