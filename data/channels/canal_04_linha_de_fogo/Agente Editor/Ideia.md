![[Pasted image 20260930032606.png]]

1 - Temas (ideias de temas ) -  Hermes Agent

2- Roteiro Hipnotico 

3 - Editor para definir as cenas 

- a ideia seria basicamente gerar isso em:
- imagens + motion designer 2d e 3d
- IMAGEM + RECORTE + COMPOSIÇÃO + MOTION

4 -  Transiçao, edicao, sfx etc.

5 - Render

6 - Tumb, Desc...


Langgraph

Jev



````
# LINHA DE FOGO — Brief do Pipeline de Edição Automática
**Versão 1.0 · Executor: Claude Code / Codex / Antigravity · Orquestração: LangGraph**

---

## 1. Objetivo

Gerar vídeos documentais de 11–14 min no estilo **Thriller de Espionagem Anos 60/70** de forma automatizada, com o mínimo de intervenção humana e **o mesmo acabamento visual em todos os episódios**.

**Princípio central:**
> **A IA gera PEÇAS. O código monta a CENA.**
> Imagem = recorte + composição + multiply sobre papel.

**O que já foi testado e descartado:** gerar tudo em CSS/HTML puro. Fica "desenhado", sem textura de impressão convincente. O código fica responsável só pelo que ele faz bem: fundo, texto, movimento e acabamento.

---

## 2. Restrições

- **Sem API externa de imagem.** As imagens saem via **CLI do Codex ou do Gemini**, chamadas pelo agente.
- Tudo roda local, na IDE.
- Texto **nunca** vem na imagem gerada. Todo texto é feito por código.
- Logos de marca são redesenhados como asset vetorial próprio, nunca gerados pela IA.
- Personagens reais aparecem como **silhuetas estilizadas**, sem rosto fotorrealista (YPP + direito de imagem).

---

## 3. Divisão de responsabilidades

| Camada | Quem faz | Exemplos |
|---|---|---|
| **Gerado por IA** (CLI) | Codex / Gemini | Personagens, prédios, veículos, objetos, submarinos, garrafas |
| **Processado** (Python) | rembg + script de look | Recorte, posterização, halftone, mapeamento de paleta, borda rasgada |
| **Gerado por código** (Remotion) | Componentes | Fundo de papel, mapas, faixas vermelhas, cortes diagonais, blocos de texto, carimbos, cartelas, lower thirds |
| **Acabamento global** | Remotion / FFmpeg | Grão, ruído de papel, vinheta, desregistro de cor |
| **Áudio** | FFmpeg | Voz + jazz + SFX + mix em −14 LUFS |

---

## 4. Stack

| Etapa | Ferramenta |
|---|---|
| Orquestração | LangGraph |
| Geração de imagem | CLI do Codex / Gemini |
| Recorte | **rembg** (padrão) → **SAM/SAM2** (fallback com pontos) |
| Look / tratamento | Python: Pillow + OpenCV + numpy |
| Composição + animação + render | **Remotion** |
| Áudio e export final | **FFmpeg** |
| Voz | ElevenLabs (já definido no canal) |

Alternativas para avaliar depois (não no MVP): HyperFrames e Revideo.

---

## 5. Grafo de agentes (LangGraph)

```
[1] Roteirista ──► ✋ Aprovação humana do roteiro
      │
[2] Decupador (roteiro → cenas → lista de elementos)
      │
[3] Bibliotecário (o elemento já existe na biblioteca?)
      │ não                          │ sim → pula para [7]
[4] Gerador de peças (CLI Codex/Gemini, 1 elemento por imagem)
      │
[5] Recortador (rembg → QA de borda → fallback SAM)
      │
[6] Tratador de look (script Python único) → salva na biblioteca
      │
[7] Compositor (monta o JSON de cena com camadas e movimentos)
      │
[8] Animatic (render rápido em baixa resolução) ──► ✋ Aprovação humana do ritmo
      │
[9] Sonoplasta (voz + trilha + SFX + mix)
      │
[10] Render final (Remotion 4K + FFmpeg)
      │
[11] QA visual (extrai frames e compara com o manual) ──► ✋ Aprovação final
```

**Loops de correção:**
- [5] falhou no QA de borda → volta para [4] com prompt ajustado (máx. 2 tentativas) → depois escala para um humano.
- [11] reprovou → devolve a correção para a cena específica em [7], nunca refaz o vídeo inteiro.

---

## 6. Regras para a geração de peças

- **1 elemento por imagem**, isolado, **em fundo liso off-white ou cinza neutro** (é o que faz o recorte funcionar).
- Iluminação lateral dura, silhueta clara e sem objetos encostados nas bordas.
- Prompt-base fixo com a paleta em hex + "posterized silhouette, no gradient, no text".
- Personagens recorrentes: ficha com referência fixa, sempre reutilizada.
- **Proibido gerar cena inteira** (exceto fundos amplos, como porto e cidade, que viram camada de fundo).

**Exemplo de decupagem (Take 01):**
| Elemento | Origem |
|---|---|
| Fundo papel vermelho | Código |
| Neblina / linhas de água | Código |
| Submarino | IA → recorte → look |
| Garrafa refletida | IA → recorte → look (espelhado por código) |
| Corte diagonal de torpedo | Código |
| Texto "17 SUBMARINOS" | Código |
| Grão + desregistro | Acabamento global |

---

## 7. O "look" (script Python único, sem exceções)

Toda peça passa pela mesma receita, na mesma ordem:

1. Escala de cinza
2. Curva de contraste agressiva
3. Posterização em **4 níveis** (faixa de 3 a 5)
4. Mapeamento para a paleta: `#111111` · `#EDE6D6` · `#C62D1F` · `#D4A537`
5. Halftone leve
6. Borda de papel rasgado
7. Exporta PNG com alfa + metadados

**Duotones por ato:** Papel (padrão) · Vermelho (Ato 0 e pico do Ato 3) · Mostarda (Ato 4).
O duotone é aplicado **na composição**, não na peça. Assim a mesma peça serve para qualquer ato.

---

## 8. JSON de cena (fonte única da verdade)

Cada cena é descrita por um arquivo que o Remotion lê. Campos mínimos:

| Campo | Conteúdo |
|---|---|
| `id` | EP01_T01 |
| `ato` / `duotone` | 0 / vermelho |
| `inicio` / `duracao` | Tempo sincronizado com a narração |
| `camadas` | Lista ordenada: fundo → mapa → prédios → personagem → faixa → texto |
| `camada.asset` | ID da peça na biblioteca ou componente de código |
| `camada.posicao/escala/rotacao` | Composição assimétrica, com diagonal |
| `camada.movimento` | Um dos 6 movimentos oficiais |
| `texto` | Palavras, estilo do bloco (preto, vermelho ou mostarda) |
| `sfx` | Isqueiro, carimbo, rasgo, teletipo... |
| `camera` | Zoom/pan lento, parallax |

**Vocabulário de movimento (só estes 6):** corte seco · slide de papel · zoom lento · carimbo · rasgo diagonal · tremor.

---

## 9. Biblioteca de assets (o ativo do canal)

- Toda peça aprovada é salva com tags (`personagem`, `prédio`, `veículo`, `objeto`, `época`, `país`).
- O Bibliotecário **sempre busca antes de gerar**.
- Meta: a partir do EP05, **≥ 50% das peças reutilizadas** (Kremlin, Capitólio, mapa, espião, dinheiro, fábricas).
- Padrão de nome: `LF_[categoria]_[descrição]_[###]`

---

## 10. QA automático (critérios do agente [11])

- Máximo de 4 cores por frame (a paleta oficial)
- Proporção papel/preto/vermelho/mostarda ≈ 60/25/10/5 (exceto nos momentos planejados)
- Nenhum rosto fotorrealista
- Nenhum texto dentro das peças geradas
- Mudança visual a cada 4–6 s, nenhum frame parado por mais de 8 s
- Áudio: −14 LUFS · −1 dBTP · voz sempre na frente

---

## 11. Plano de validação (MVP)

1. **Fase 1:** só o **Ato 0 do EP01 (T01–T04, ~15 s)**, de ponta a ponta. Se ficar bom, o pipeline está validado.
2. **Fase 2:** Ato 1 completo, testando reaproveitamento da biblioteca e sincronia com a voz.
3. **Fase 3:** EP01 inteiro.
4. **Fase 4:** EP02 usando a biblioteca do EP01. Aqui se mede o ganho de tempo.

**Critério de sucesso da Fase 1:** um frame qualquer do render, colocado ao lado do painel de identidade, parece da mesma "gráfica".

---

## 12. Riscos e atenção

| Risco | Mitigação |
|---|---|
| A CLI entrega imagem fotográfica demais (visto na grade de 39 takes) | O script de look força posterização; o QA reprova rostos realistas |
| Recorte ruim em cabelo/fumaça | Fallback com SAM usando pontos; evitar esses elementos na geração |
| Inconsistência de personagem | Ficha fixa + reuso da biblioteca |
| Limites de uso da CLI | Gerar em lotes por ato; priorizar reuso |
| Licença de modelos (rembg/SAM) | Checar a licença de cada modelo antes do uso comercial |
| Erro histórico na imagem | Conferir figuras e datas no roteiro (ex.: Debate da Cozinha = Nixon × Khrushchev) |
| Marca errada no objeto | Garrafa da Coca ≠ garrafa da Pepsi; manter um asset próprio para cada |

---

## 13. Entregáveis por episódio

- Roteiro aprovado
- Pasta de JSONs de cena
- Peças novas adicionadas à biblioteca
- Animatic aprovado
- Render 4K + mix final
- 3 thumbnails (compostas pelo mesmo sistema)
- 2 Shorts recortados do longo
- Relatório do QA
````