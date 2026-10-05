# 🏛️ HERMES CHIEF DE ANÁLISE — SISTEMA QUANTITATIVO PARA 3 CANAIS DOCUMENTAIS

> **Tech Lead Quant Sênior:** Inteligência analítica, diagnóstico algorítmico, priorização matemática de pautas e diretrizes de packaging para os canais **O Outro Lado**, **Hidden Systems Lab (HSL)** e **Brecha**.

---

## 📑 1. Visão Geral e Filosofia

O **Hermes Chief** opera como o cérebro estratégico dos 3 canais de documentário. Sua função é transformar dados dispersos do YouTube em decisões de alta convicção, eliminando achismos e alinhando produção a equações empíricas:

1. **Equação Macro de Tráfego:**
   $$\text{Visualizações } (V) \approx \text{Impressões } (I) \times \text{CTR} \times \text{Retenção } (R)$$

2. **Equação de Priorização de Temas (Quant Scoring):**
   $$P = D \times C \times R \times E$$
   - $D \in [1..5]$: Dor / Desejo do espectador
   - $C \in [1..5]$: Curiosidade / Fator WTF
   - $R \in [1..5]$: Relevância / Momento cultural
   - $E \in [1..5]$: Executabilidade técnica do squad
   - Score $P \in [1..625]$. Pauta $P0 \ge 400$, $P1 \in [250..399]$, $P2 < 250$.

3. **Filtro de Segurança Editorial ($S \in [1..5]$):**
   - Garante que a pauta respeite os princípios do canal (mecanismo físico, dignidade da vítima, ausência de sensacionalismo amador).

---

## 🛰️ 2. Os 3 Canais Gerenciados

| Canal | Handle | Formato & Unidade | Gargalo Diagnosticado | Ação Primária de Resgate |
|---|---|---|---|---|
| **O Outro Lado** | `@outroladodetudo` | Doc Investigativo Brasil (5-15 min)<br>Unidade: 1 unidade concreta atravessa sistema invisível | **Descoberta / Cold Start**<br>(Cadência excessiva de 1 longo/dia sem retenção semente) | Reduzir para 2 longos/sem.<br>Vincular os Shorts virais (Santos 1.4k) aos masters via YouTube Studio. |
| **Hidden Systems Lab** | `@HiddenSystemslabss` | Mega-Infraestrutura Global (EN)<br>Unidade: Física e colapso de megassistemas reais | **Packaging / CTR**<br>(Uploads duplicados + shorts com apenas hashtags no feed) | Deletar duplicatas.<br>Renomear Shorts com paradoxos em inglês (*"The 500ms Disaster"*). |
| **Brecha** | `@brechadocs` | Defesa Cotidiana / Golpes Brasil<br>Unidade: A fenda de tempo e psicologia do golpe | **Audiência Fantasma**<br>(1.120 inscritos inativos ignorando longos + ALL CAPS) | Títulos sóbrios no formato forense.<br>Shorts autocontidos sem corte ("Parte 1"). |

---

## 📂 3. Estrutura do Projeto

```
d:/CHIEF YOUTUBE/
├── chief.py                           # CLI executável principal
├── requirements.txt                   # Dependências do projeto
├── README.md                          # Este documento
├── RELATORIO_AUDITORIA_CHIEF_3_CANAIS.html # Dossiê Executivo Interativo (92 KB)
│
├── .hermes/
│   ├── bots/
│   │   └── chief-analyst.json         # Configuração nativa do bot Hermes
│   ├── memory/
│   │   └── chief_memory.db            # Banco SQLite com FTS5 (táticas e aprendizados)
│   └── skills/                        # Espelhamento local das skills
│
├── data/
│   ├── channels/                      # Baselines reais dos 3 canais (75+ vídeos)
│   │   ├── outro_lado_baseline.json
│   │   ├── hsl_baseline.json
│   │   └── brecha_baseline.json
│   ├── briefings_output/              # Briefings JSON emitidos para squads
│   └── weekly_audits/                 # Snapshots semanais da rotina cron
│
├── src/
│   ├── core/
│   │   ├── agent.py                   # Orquestrador ChiefAnalystAgent
│   │   ├── memory.py                  # Engine SQLite FTS5 (busca de aprendizados)
│   │   └── personality.py             # Diretrizes invioláveis e tom de voz
│   ├── interfaces/
│   │   ├── cli.py                     # Interface de linha de comando com Rich/ASCII
│   │   └── telegram_bot.py            # Bot Telegram puro em Python (long-polling)
│   ├── cron/
│   │   └── weekly_audit.py            # Rotina de auditoria semanal agendada
│   ├── mcp/
│   │   ├── youtube_analytics_mcp.py   # Servidor MCP stdio JSON-RPC 2.0
│   │   └── mcp_config.json            # Configuração do MCP para Antigravity/Claude
│   └── skills/                        # Módulos Python das 5 skills estratégicas
│       ├── metrics_reader.py
│       ├── diagnostic.py
│       ├── thumb_audit.py
│       ├── theme_decider.py
│       └── squad_briefing.py
```

---

## 🛠️ 4. Como Executar

### 1. Linha de Comando (CLI)

```bash
# Executar auditoria quantitativa completa de um canal
python chief.py audit o_outro_lado
python chief.py audit hsl
python chief.py audit brecha

# Avaliar e priorizar próximos temas (Equação P = D x C x R x E)
python chief.py themes hidden_systems_lab

# Emitir briefing técnico JSON para o squad de edição
python chief.py briefing brecha EP_007

# Auditar embalagem (thumbnail + título) nas 4 dimensões (0 a 100)
python chief.py thumb o_outro_lado "O Jammer de 50 Reais" "Dispositivo preto com antena e luz vermelha" --text "SILENCIO"

# Consultar aprendizados históricos na Memória Persistente SQLite FTS5
python chief.py memory santos

# Gerar relatório consolidado dos 3 canais
python chief.py report

# Entrar no console interativo contínuo
python chief.py interactive
```

---

### 2. Bot do Telegram

O Hermes Chief possui interface via Telegram em Python puro (sem dependência de frameworks externos):

```bash
# 1. Definir o token do bot criado no @BotFather
$env:TELEGRAM_BOT_TOKEN="SEU_TOKEN_AQUI"

# 2. Iniciar o bot
python src/interfaces/telegram_bot.py
```

**Comandos Suportados no Telegram:**
- `/status` — Panorama dos 3 canais em tempo real.
- `/audit <canal>` — Diagnóstico de gargalo e experimento ativo.
- `/themes <canal>` — Fila de temas $P0/P1/P2$.
- `/briefing <canal> [ep_id]` — Emissão de briefing JSON oficial.
- `/memory <termo>` — Busca instantânea na memória SQLite FTS5.
- *Texto livre* — Conversa estratégica direta com o Chief Analyst.

---

### 3. Rotina de Auditoria Semanal (Cron)

Para rodar o checkpoint semanal que avalia o progresso, computa trajetórias e gera snapshots em `data/weekly_audits/`:

```bash
python src/cron/weekly_audit.py
```

*Dica:* Pode ser agendado no Windows Task Scheduler toda segunda-feira às 09:00 AM. Se as variáveis `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID` estiverem definidas, um alerta executivo é enviado automaticamente no Telegram.

---

### 4. Servidor MCP (Model Context Protocol)

O Hermes Chief expõe 6 ferramentas MCP para qualquer agente de IA:
- `get_channel_metrics`
- `diagnose_channel`
- `evaluate_themes`
- `audit_packaging`
- `generate_squad_briefing`
- `query_chief_memory`

Para registrar no Antigravity ou Claude Desktop, aponte para `src/mcp/mcp_config.json` ou execute:
```bash
python src/mcp/youtube_analytics_mcp.py
```

---

## 🧠 5. Memória Persistente SQLite FTS5

A memória do Chief é persistente e indexada por texto completo (Full-Text Search FTS5). Ela armazena:
- **Learnings:** Aprendizados derivados de métricas reais (ex: correlação de views em temas de crime vs física).
- **Hypotheses & Experiments:** Registro de testes com metas quantitativas pré-definidas (Método X + Y).
- **Track Record:** Histórico de vídeos postados e anomalias de retenção.

Sincronizada em:
- `d:/CHIEF YOUTUBE/.hermes/memory/chief_memory.db`
- `C:/Users/brend/.hermes/memory/chief_memory.db`

---

## 🛡️ 6. Regras de Fronteira e Isolamento

- **Papel Estritamente Estratégico:** O Hermes Chief **NÃO** edita vídeos, não gera cortes, não escreve roteiros finais e não publica vídeos. Ele define a pauta, audita a embalagem e emite a ordem de produção (briefing) para os 3 squads.
- **Zero Cruzamento com Plataformas Externas:** O banco de dados do Chief é 100% isolado em SQLite FTS5 local e não se comunica com bancos Supabase de outros projetos.
