---
name: theme-decider
description: "Decide os temas dos próximos vídeos com base em dados, diagnóstico e na equação quantitativa P = D x C x R x E."
---

# Skill: theme-decider

## Objetivo
Priorizar a fila de produção documental dos 3 canais usando critérios quantitativos objetivos:
- **D (Demanda):** Pessoas procuram ativamente ou reagem com curiosidade extrema? (1 a 5)
- **C (Clareza):** A promessa é compreendida instantaneamente na mente do leigo? (1 a 5)
- **R (Relevância / Consequência):** Toca em dinheiro, liberdade, segurança ou perda humana? (1 a 5)
- **E (Evidência Visual):** Existem esquemas 3D, telemetria e cutaways fáceis de demonstrar? (1 a 5)

## Equação:
$$P = D \times C \times R \times E \quad (\text{Pontuação de 1 a 625})$$
$$S = B - C - R \quad (\text{Benefício} - \text{Custo} - \text{Risco})$$

## Passo 0 Obrigatório: Filtro Anti-Duplicação e Memória Persistente
Antes de calcular qualquer pontuação ou aprovar uma pauta, o agente **DEVE OBRIGATORIAMENTE** verificar se o tema já foi postado ou está em produção:
1. Consultar a memória persistente SQLite (`covered_themes` e `video_history`) via `check_topic_coverage`.
2. Se a similaridade semântica ou sobreposição de tokens for relevante, o tema é **SUMARIAMENTE DESQUALIFICADO** com a classificação `DISQUALIFIED_ALREADY_COVERED`.
3. É **TERMINANTEMENTE PROIBIDO** recomendar ou aprovar temas, mecanismos ou ângulos que já possuam vídeos gravados, postados ou briefings abertos no canal.

## Classificação dos Temas Inéditos:
- **P0:** P ≥ 450 (Produção imediata / Top priority e 100% virgem no canal).
- **P1:** P ≥ 320 (Próxima onda de produção / Tema inédito validado).
- **P2:** P < 320 (Backlog / Não recomendado sem refaturação).
- **P3 / BLOQUEADO:** Pauta duplicada já coberta no catálogo ou em produção.
