---
name: niche-research
description: "Executa pesquisa de nichos para canais faceless no YouTube cruzando demanda (Google Trends + YouTube Data API) com viabilidade de monetização e gate YPP (reused content, inauthentic content, direitos autorais e requisitos 2026-2027)."
---

# Skill: niche-research

## Propósito
Executar pesquisa de nichos para canais faceless no YouTube, cruzando demanda (Google Trends + YouTube Data API) com viabilidade de monetização, bloqueando automaticamente territórios que violam as políticas de *reused content* e *inauthentic content* do YouTube Partner Program (YPP) [26][27][38][39].

## Fontes de Dados
- Google Trends (12 meses, regiões BR + US)
- YouTube Data API v3 / Scraping (top vídeos por termo, métricas de canal, visualizações, inscritos)
- Lista de CPM/RPM por nicho (Benchmarks 2026)
- Políticas oficiais do YouTube: reused content, inauthentic content, YPP eligibility [26][27][29][37][39]

## Regras de Bloqueio (Gate de Monetização)

### 1. Reused Content
Bloqueie nichos onde a maioria dos top vídeos se encaixa em:
- Compilados de clipes sem narrativa original (filmes, esportes, gameplay)
- Coleções de músicas de artistas diferentes
- Conteúdo copiado de outras fontes sem alteração substancial
- Reações não-verbais sem comentário em voz [27]

**Sinal de alerta fatal:** >50% dos top 10 vídeos do nicho são compilados, clipes brutos ou conteúdo duplicado de outras plataformas.

### 2. Inauthentic Content (ex-repetitious)
Bloqueie nichos onde os canais postam templates intercambiáveis em escala, com pouca mudança de substância entre vídeos [39].

**Sinal de alerta fatal:** Canais com >20 vídeos nos últimos 90 dias usando o mesmo formato de roteiro/visual sem variação narrativa.

### 3. Direitos e Licenças
Bloqueie nichos que dependem majoritariamente de:
- Footage protegido por direitos (filmes, séries, eventos esportivos pagos)
- Músicas comerciais sem licença
- Conteúdo de terceiros sem permissão explícita [38]

**Sinal de alerta fatal:** >30% dos top vídeos usam material de terceiros sem camada editorial clara.

### 4. Requisitos YPP 2026-2027
Priorize nichos onde é viável atingir:
- 1.000 inscritos + 4.000 horas qualificadas (12 meses) OU 10M views em Shorts (90 dias) [29][36][37].
- **Atenção:** A partir de 1º de fevereiro de 2027, novos canais precisarão de 8.000 horas ou 20M views em Shorts [28][31][32][33][34][35].

### 5. Formato × Nicho
Avalie cada um dos 4 formatos:
- **Formato 1 (Motion + voz IA):** Ideal para finanças, dados, tech/B2B
- **Formato 2 (Imagens + voz):** Ideal para história, mistérios, biografias
- **Formato 3 (Vídeo IA + voz):** Ideal para documentários cinematográficos, sci-fi, investigações
- **Formato 4 (Vídeo internet + voz):** Risco alto — exigir camada editorial forte (comentário original, análise, narrativa transformativa) [27][38]

**Bloqueio mandatário:** Bloqueie combinações onde o formato 4 é a única opção viável no nicho.

## Metodologia de Cálculo

### Equação do Score Final:
$$\text{Score} = 25\% \times \text{crescimento\_trends} + 30\% \times \text{intensidade\_outliers} + 25\% \times \text{RPM\_estimado} + 20\% \times \text{viabilidade\_formato}$$

**Penalidades e Cortes:**
- Redução de **-50% no Score** se o nicho depende de Formato 4 ou possui riscos moderados de template repetitivo.
- **BLOQUEIO SUMÁRIO (`monetization_safe = False`)** se violar qualquer um dos gates (>50% reused content, >30% copyright, ou dependência exclusiva de Formato 4).

## Gatilhos de Ativação
Execute esta skill quando o usuário solicitar:
- "pesquisa de nichos"
- "quais canais criar no YouTube"
- "encontrar nichos monetizáveis"
- "análise de demanda YouTube"
- "niche research"
- "pesquisa de nichos em html" / "entregar em html"

## Formatos de Entrega
1. **JSON Canônico (Padrão):** Retorna o payload estruturado com ranked_niches, top_niche_briefing e blocked_niches_audit.
2. **Dashboard Visual em HTML:**
   - Execute com a flag `--html` no terminal:
     ```powershell
     python .hermes/skills/niche-research/handler.py --html
     ```
   - Ou solicite diretamente em linguagem natural ao Hermes:
     *"faça a pesquisa de nichos e me entregue isso em html"*
   - O dashboard executivo é gerado automaticamente e salvo em `RELATORIO_NICHOS_MONETIZACAO.html` com ranking visual, medidores de P-Score, badges de formato, 5 títulos por nicho e auditoria de bloqueios YPP.

> **Aviso de Compliance:** Após a execução, aguarde sempre aprovação humana antes de gerar briefings de produção para os squads de edição.
