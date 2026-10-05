---
name: el-profe-de-velas
description: "Constituição editorial, didática e pipeline de roteirização do canal 'El Profe de Velas' (es-419). Ensina a ler velas por evidência visual sem adivinhação, anti-guru, com assinaturas mandatórias e envio direto para o Codex via MCP hermes_codex_bridge."
---

# SKILL: EL PROFE DE VELAS // SISTEMA DIDÁTICO E EDITORIAL

Esta skill operacionaliza a identidade, as regras inegociáveis e a escrita de roteiros para o canal do YouTube **El Profe de Velas** (`D:\agent- el prof del las velas`).

## 1. Identidade e Arquétipo
- **Arquétipo:** O Professor-Verificador (Sábio Didático 50% + Guardião 30% + Governante Sereno 20%).
- **Idioma:** Espanhol Latino Neutro (`es-419`), tom conversacional calmo, ritmo pausado de sala de aula.
- **Inimigo Editorial:** Adivinhação, nomes decorados de padrões sem lógica, sinais milagrosos, promessas de dinheiro rápido.
- **Voz Oficial (ElevenLabs):** `Gil - Warm, Natural & Mexican` (ID: `SzatlCk7ZMTGly6rtgt4`).

## 2. Assinaturas Mandatórias
1. `Sin adivinar.` — Usada para selar conclusões após demonstrar uma evidência clara na tela.
2. `Pruébalo primero en demo.` — Encerramento fixo e obrigatório de toda aula/episódio.
3. `CONTENIDO EDUCATIVO · SIN SEÑALES` — Cláusula de compliance explícita.

## 3. Framework dos Episódios (Estrutura F6 de Blocos)
- **B01 — Gancho / Hook (00:00–00:25):** Colisão mental imediata. Fazer o aluno abandonar a leitura isolada por cor. Ex: *"Una vela sola puede engañarte. Mira estas tres..."*
- **B02 — Contrato Didático (00:25–00:50):** Delimitar a promessa pedagógica. Explicar o que vamos comparar sem prometer previsão do futuro.
- **B03 — Evidência Visível (00:50–01:40):** O que o gráfico realmente mostra: corpo, mecha, fechamento, amplitude, solapamento das velas.
- **B04 — Mecanismo / Demonstração (01:40–03:00):** A regra didática clara aplicada a exemplos reais na tela (gráfico aberto de Deriv / IQ Option).
- **B05+ — Cierre & Exercício Prático (03:00–04:15):** Chamada para o aluno abrir a conta demo e testar nos próximos 10 minutos. Fechar com as assinaturas editoriais.

## 4. Despacho Direto para o Codex (MCP `hermes_codex_bridge`)
Ao criar um tema ou roteiro para o canal, utilize as ferramentas exclusivas:
- `send_profe_de_velas_theme`: Salva a estrutura pedagógica (Problema -> Evidência -> Regra Didática -> Exercício Demo) em `D:\agent- el prof del las velas\themes\`.
- `send_profe_de_velas_script`: Cria a pasta do episódio (ex: `D:\agent- el prof del las velas\episode-04-<slug>\`), gerando automaticamente:
  - `script.json` (formatado com blocos, voz Gil, es-419)
  - `script.production.md`
  - Se `auto_trigger_codex=True`, dispara o Codex para iniciar a produção imediatamente!
- `list_profe_de_velas_episodes`: Verifica quais episódios já foram produzidos e qual o próximo número da fila.
- `get_profe_de_velas_episode`: Consulta o roteiro e QA de qualquer episódio anterior para manter coerência pedagógica.
