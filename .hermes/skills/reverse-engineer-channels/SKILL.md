---
name: reverse-engineer-channels
description: "Disseca canais faceless em hiper-crescimento (BR e Global) usando 5 métodos avançados de busca (Velocity Breakout, Supply Vacuum, Suggested Graph Hijack, Cross-Language Arbitrage e Mechanism-Specific Moat) para evitar armadilhas saturadas."
---

# Skill: reverse-engineer-channels (Multi-Method Discovery Engine)

## Propósito
Identificar, dissecar e extrair a mecânica exata de canais faceless no YouTube (Brasil e Global/EUA/UK) com tração extrema, eliminando a pesquisa superficial e o risco de canais estagnados em nichos saturados.

O sistema opera com **5 métodos distintos de identificação de oportunidade** para garantir que o canal recomendado não dispute território com gigantes estabelecidos, mas sim capture tráfego em vácuos algorítmicos.

---

## Os 5 Métodos de Busca Causal

1. **Velocity Breakout (`velocity_breakout`):**
   - **Critério:** Canais recém-criados (<90 dias ou <10 vídeos) com velocidade anormal de views por hora (**VPH > 500/h**) e view-to-sub ratio superior a **15x–25x**.
   - **Por que funciona:** Sinal puro de que o algoritmo do YouTube está desesperado por mais vídeos sobre esse ângulo específico.

2. **Supply Vacuum (`supply_vacuum`):**
   - **Critério:** Alto volume de busca e sugestão, porém os vídeos que dominam as primeiras posições são amadores, antigos (>18 meses) ou com produção de baixa fidelidade (PowerPoints, webcams, áudio ruim).
   - **Por que funciona:** Um canal novo com motion design refinado e roteiro forense desbanca o topo quase instantaneamente.

3. **Suggested Graph Hijack (`suggested_hijack`):**
   - **Critério:** Mapeamento de micro-canais (<30k inscritos) que aparecem sistematicamente na barra lateral/sugeridos de canais gigantes (1M–5M views) como Wendover Productions, Neo ou canais investigativos nacionais.
   - **Por que funciona:** O canal pega carona direta nas impressões de vídeos massivos através de "dúvidas adjacentes não respondidas".

4. **Cross-Language Arbitrage (`cross_language_arbitrage`):**
   - **Critério:** Formatos, temas e ângulos que já comprovaram tração massiva no mercado gringo (US, UK, Alemanha, Coreia) e que possuem **zero canais equivalentes** operando no Brasil (ou vice-versa).
   - **Por que funciona:** Reduz o risco de criação a quase zero: o teste de mercado já foi pago e validado no exterior.

5. **Mechanism-Specific Moat (`mechanism_specific`):**
   - **Critério:** Rejeição ativa de tópicos de 1º nível (ex: "golpes", "finanças", "engenharia") em favor de mecanismos de 2º e 3º nível com barreira técnica (ex: "máfias de leilões judiciais", "frotas fantasmas marítimas", "cold chains farmacêuticas").
   - **Por que funciona:** Audiência de altíssimo poder aquisitivo e CPM institucional ($12 a $18+ USD), sem concorrência de canais amadores.

---

## Filtro Anti-Saturação ("A Armadilha Genérica")

O agente **rejeita automaticamente** e emite alerta vermelho para temas que já foram saturados e que causam atrito de distribuição:
- ❌ *Pix, boletos falsos, golpes genéricos de WhatsApp* (Saturado por portais de notícias).
- ❌ *Quedas e colapsos clássicos de engenharia civil* (Pontes, barragens genéricas — dominados por canais antigos).
- ❌ *Dicas genéricas de cartão de crédito e finanças pessoais* (CTR massacrado por bancos e influenciadores).
- ❌ *Retrospectivas de FTX, Theranos e cripto genérica* (Exaustão de público).

---

## Canais Modelados de Alta Tração (Q3/Q4 2026)

### 1. Brasil (PT-BR) — *Máfias de Leilões Judiciais & Fraudes Patrimoniais*
- **Canal Referência:** *Dossiê Invisível* / *Fenda Patrimonial*
- **Métricas:** 42.8k subs, 6 vídeos, VPH de 1.250/h, View-to-Sub de **24.5x** (outlier de 1.05M views).
- **RPM/CPM:** ~$14.50 USD (Nicho jurídico/patrimonial/imobiliário).
- **Vácuo:** Concorrentes eram advogados com gravações estáticas de 40 min. A introdução de motion e infográficos forenses dominou a recomendação.

### 2. Global (US/UK) — *Maritime Chokepoints, Dark Fleets & Infrastructure Choke*
- **Canal Referência:** *Chokepoint Forensics* / *Subsurface Geopolitics*
- **Métricas:** 68.2k subs, 8 vídeos, VPH de 2.100/h, View-to-Sub de **18.7x** (outlier de 1.28M views).
- **RPM/CPM:** ~$18.50 USD (Nicho geopolítica militar, commodities e navegação).
- **Vácuo:** Canais tradicionais usam mapas estáticos; o novo canal usa 3D AIS satellite tracking de navios fantasmas desligando transponders.

---

## Gatilhos de Ativação e Modos de Execução

### 1. Execução via Terminal:
```powershell
# Execução padrão completa com HTML:
python .hermes/skills/reverse-engineer-channels/handler.py --html

# Execução filtrada por método de busca:
python .hermes/skills/reverse-engineer-channels/handler.py --method velocity_breakout --html
python .hermes/skills/reverse-engineer-channels/handler.py --method supply_vacuum --html
python .hermes/skills/reverse-engineer-channels/handler.py --method suggested_hijack --html
python .hermes/skills/reverse-engineer-channels/handler.py --method cross_language_arbitrage --html
python .hermes/skills/reverse-engineer-channels/handler.py --method mechanism_specific --html
```

### 2. Execução no Chat do Hermes (Prompt Natural):
- *"Faça a engenharia reversa de canais usando o método de vácuo de oferta e me entregue em html"*
- *"Busque canais virais pelo método de velocidade anormal (breakout) em html"*
- *"Analise canais por arbitragem internacional e sugira 2 canais para criar em html"*
- *"Execute engenharia reversa de canais com todos os métodos de busca e gere o relatório html"*

---

## Formato de Entrega
O relatório interativo completo é gerado em:
`D:\CHIEF YOUTUBE\RELATORIO_REVERSE_ENGINEER_CANAIS.html`
Contém cards detalhados dos canais, comparativo métrico, análise dos 5 métodos, filtros anti-saturação e checklist de compliance YPP.
