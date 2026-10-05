---
name: voice-of-customer
description: "Minera a linguagem espontânea do público (Eugene Schwartz Passo 2): extrai citações viscerais, dores, dúvidas não respondidas e mitos populares de comentários do YouTube (próprios e concorrentes), YouTube Suggest e fóruns de queixas."
---

# Skill: voice-of-customer

## Objetivo
Capturar a forma exata como o público real reclama, expressa frustração e faz perguntas espontâneas, evitando o jargão corporativo ou acadêmico.

> *"O desejo real do mercado não aparece nos manuais técnicos; aparece na forma como as pessoas reclamam nos comentários e fóruns."*

## Fontes de Mineração
1. **YouTube Suggest API:** Variações exatas de busca em tempo real que milhares de pessoas digitam.
2. **Comentários de Vídeos Concorrentes:** Extração via `yt-dlp` filtrando por marcadores de dor (*"perdi"*, *"não consegui"*, *"falso"*), dúvidas (*"como faço"*, *"por que"*) e mitos (*"pensei que"*).
3. **Comunidades e Fóruns:** Reddit (`r/golpes`, `r/brasil`) e fóruns de queixas de consumidores.

## Saída Estruturada
1. **Citações Viscerais (Visceral Quotes):** Frases literais do público para ancorar o gancho dos primeiros 15 segundos.
2. **Lacunas dos Concorrentes (Unresolved Doubts):** As perguntas que os vídeos de concorrentes deixaram sem resposta.
3. **Mitos a Desmascarar (Popular Myths):** As falsas seguranças que o documentário deve desarmar no Ato 2.
4. **Script Anchors:** Recomendações diretas para a equipe de roteiro / agentes de execução.
