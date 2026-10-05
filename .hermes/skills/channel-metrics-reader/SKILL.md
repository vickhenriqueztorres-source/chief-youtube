---
name: channel-metrics-reader
description: "Lê exports de métricas do YouTube Studio (CSV ou JSON) e calcula médias móveis, outliers (2 sigma) e tendências macro."
---

# Skill: channel-metrics-reader

## Objetivo
Processar dados brutos de desempenho de vídeos e canais do YouTube Studio para extrair indicadores quantitativos:
- Impressões totais e por fonte de tráfego (Browse, Suggested, Search, Shorts).
- Taxa de cliques (CTR) e média móvel de 3 e 7 vídeos.
- Retenção inicial (0-30s) e Duração Média de Visualização (AVD %).
- Identificação de outliers estatísticos (> 1.8 sigma).
- Cálculo de razão de conversão Shorts ➔ Vídeos Longos.

## Uso via Python
```python
from src.skills.metrics_reader import metrics_reader
summary = metrics_reader.analyze_channel(channel_raw_data)
```
