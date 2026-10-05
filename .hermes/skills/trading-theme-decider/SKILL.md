---
name: trading-theme-decider
description: "Avalia e prioriza pautas de trading pela equação quantitativa P = D x C x R x E e bloqueia temas duplicados via memória SQLite FTS5."
---

# Skill: trading-theme-decider

## Objetivo
Priorizar pautas matemáticas de trading filtrando fadiga de audiência:
1. Dor/Desejo do iniciante (D: 1-5).
2. Curiosidade e Anti-intuição (C: 1-5).
3. Relevância e Padrões de Mercado (R: 1-5).
4. Executabilidade em Tela Demo (E: 1-5).
5. Filtro de Segurança Editorial e YPP (S: 1-5).
6. Protocolo de Anti-Duplicação em 4 camadas via SQLite FTS5.

## Saída
Fila de temas classificados em P0 (Produção Imediata >= 400), P1 (Em Fila 250-399) e P2 (< 250), com tese e gancho de 15 segundos.
