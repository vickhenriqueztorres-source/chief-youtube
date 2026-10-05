---
name: trading-diagnostic
description: "Diagnostica gargalos causais em canais de trading (Ponte Shorts->Longos, Cold Start, Audiência de Cassino, Embalagem Inerte) e gera experimentos Método X+Y."
---

# Skill: trading-diagnostic

## Objetivo
Mapear em qual ponto exato do funil de distribuição o canal de trading está perdendo audiência:
1. Ponte Desconectada Shorts ➔ Longos (Shorts de tração sem link para o walkthrough em demo).
2. Cold Start e Prateleira Rasa (Catálogo com menos de 5-10 vídeos longos estruturantes).
3. Poluição de Hashtags / Audiência de Cassino (Hashtags que atraem caçadores de sinal rápido).
4. Embalagem Inerte (CTR < 4.0% por falta de contraste causal no pavio/corpo da vela).
5. Abandono aos 30s (Falta de exibição imediata do gráfico com o erro nos primeiros 15s).

## Saída
Gargalo primário identificado e experimento falseável de 14 dias no formato canônico:
"Se eu fizer [X] ➔ então [Y] deverá melhorar porque [Z]."
