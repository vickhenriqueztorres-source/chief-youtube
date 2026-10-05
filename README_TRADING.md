# 🏛️ HERMES CHIEF TRADING — SISTEMA ESTRATÉGICO QUANT PARA CANAIS DE TRADING

> **Diretoria Estratégica & Tech Lead:** Sistema de inteligência analítica quantitativa, diagnóstico de funil algorítmico, priorização matemática de pautas (P-Score) e diretrizes de packaging/compliance para os canais de **Trading e Mercado Financeiro**.

---

## 📑 1. Arquitetura de Isolamento (Decoupled Memory)

O **Hermes Chief Trading** opera em isolamento absoluto dos canais documentais (`o_outro_lado`, `hidden_systems_lab`, `brecha`), garantindo que aprendizados de velas e finanças não se misturem com temas de infraestrutura física ou investigações.

- **Configuração Hermes:** [.hermes/bots/chief-trading.json](file:///d:/CHIEF%20YOUTUBE/.hermes/bots/chief-trading.json)
- **Memória SQLite FTS5 Isolada:** [.hermes/memory/chief_trading_memory.db](file:///d:/CHIEF%20YOUTUBE/.hermes/memory/chief_trading_memory.db)
- **Baseline Data:** [data/trading_channels/el_profe_de_velas_baseline.json](file:///d:/CHIEF%20YOUTUBE/data/trading_channels/el_profe_de_velas_baseline.json)
- **CLI Dedicado:** [chief_trading.py](file:///d:/CHIEF%20YOUTUBE/chief_trading.py) (ou `python chief.py audit el_profe_de_velas`)

---

## 🛰️ 2. Canais no Escopo

| Canal | Handle | Arquétipo & Plataforma | Status |
|---|---|---|---|
| **El Profe de Velas** | `@profedevelas` / `@ElProfdelLasVelas` | O Professor-Verificador (Conta Demo · Deriv / IQ Option) | **Ativo · Baseline Carregado** |
| **El Cazador del Wins** | @elcazadordelwins | O Fora-da-Lei com ética de Investigador (Caça de Bots / Deriv DBot em Demo) | **Ativo • Baseline e Docs Carregados** |

---

## 🛡️ 3. Regras Invioláveis de Compliance Financeiro (YPP 2026/2027)

1. **Conta Demo Obrigatória:** Todo vídeo longo, short ou briefing exige demonstração explícita na interface com o indicador de "DEMO / PRACTICE ACCOUNT" visível na tela e no áudio.
2. **Proibido Prometer Lucro:** Banimento sumário de termos como *"ganancia segura"*, *"señal infalible"*, *"recupera tu pérdida"*, *"duplica tu saldo"* ou afirmações de lucro em primeira pessoa (*"yo gané"*).
3. **Zero Ostentação:** A autoridade do personagem vem do processo e da verificação na tela, nunca de carros de luxo, mansões, maços de dinheiro ou prints de ganhos.
4. **Disclosure de Mídia Sintética:** Checkbox obrigatório no YouTube Studio e TikTok para pessoas sintéticas / avatares de IA.
5. **Character Lock Facial & Vocal:**
   - **Voz:** Eric (ElevenLabs ID: `cjVigY5qzO86Huf0OWal`), 140 palavras/minuto, espanhol latino neutro.
   - **Visual:** Homem 34-38 anos, bomber azul canelado (Look A) ou polo preta (Look B).
   - **PiP:** 20-25% no canto inferior apontando para o gráfico. Tela cheia só no hook (3-5s) e CTA (5-8s).
6. **Mantra Operacional:** *"Antes de arriesgar, entiende. Antes de creer, comprueba. Sin adivinar."*

---

## 💻 4. Como Executar (Comandos CLI)

```bash
# 1. Auditoria Quantitativa Completa (Métricas, Gargalo Primário e Experimento de 14 dias)
python chief_trading.py audit el_profe_de_velas

# 2. Avaliação de Temas P0/P1 com Guardião Anti-Duplicação em 4 camadas
python chief_trading.py themes el_profe_de_velas

# 3. Emissão de Briefing Estratégico de Produção (Roteiro em 6 Atos, PiP, Áudio e Compliance)
python chief_trading.py briefing el_profe_de_velas EP_004

# 4. Auditoria de Embalagem (Thumbnail + Título) nas 4 dimensões
python chief_trading.py thumb el_profe_de_velas "La Trampa del Martillo" "Zoom na mecha e o Profe em PiP" --text "REBOTE O TRAMPA"

# 5. Projeção do Ecossistema Integrado de Descoberta (7 peças)
python chief_trading.py ecosystem el_profe_de_velas --tema "El Error del Martingale"

# 6. Sincronização em Tempo Real no YouTube via yt-dlp
python chief_trading.py live el_profe_de_velas

# 7. Consulta na Memória Persistente SQLite FTS5 de Trading
python chief_trading.py memory "martillo"

# 8. Console Interativo Contínuo
python chief_trading.py interactive
```

---

## 🔌 5. Como Plugar o Canal 02

Quando estiver pronto para enviar os dados do segundo canal de trading, basta enviar os dados no formato:
1. Nome, Handle e Link do YouTube
2. Arquétipo, Tom de Voz e Promessa Central
3. Plataformas/Ativos de Trading trabalhados
4. Parâmetros visuais/vocais

O sistema fará a ingestão automática no `chief-trading.json`, gerará a baseline em `data/trading_channels/` e ativará as skills dedicadas instantaneamente.
