# Base de Conhecimento RAG // Edição de Vídeos Cinematográficos

Base de conhecimento estruturada e motor de busca semântica/textual contendo o conhecimento prático e técnico dos maiores profissionais de edição e criação cinematográfica do YouTube brasileiro.

---

## 🎬 Criadores e Vídeos Mapeados

| Criador | Título do Vídeo | Views | Foco Principal | Video ID |
| :--- | :--- | :--- | :--- | :--- |
| **Andre Pilli** | *Faça um filme, não um vídeo* | 166k | Storytelling cinematográfico, propósito de cena, ritmo e intenção | `O41Ixys3BkA` |
| **Gaveta** | *Meu modo de editar vídeos* | 450k | Fluxo de trabalho, timing dramático/cômico, decupagem e ritmo | `bZdmAIzekN0` |
| **Brendo Rannov** | *5 Técnicas para Fazer Vídeos CINEMATOGRÁFICOS* | 145k | Composição, iluminação dramática, movimentos de câmera e sound design | `5xR3w0bbxOs` |
| **Brendo Rannov** | *4 Técnicas simples de EDIÇÃO para deixar qualquer vídeo DINÂMICO* | 90k | Cortes na ação, J-Cut, L-Cut, efeitos sonoros diegéticos | `LGwuAvuE3A8` |
| **Gabriel Saab** | *Aprenda a EDITAR como um PROFISSIONAL* | 512k | Estrutura de timeline, atalhos, cortes invisíveis e acabamento | `gWfOdT8TK7E` |
| **Giulia Paié** | *Como fazer seus vídeos parecerem filme* | 270k | Estética de cinema solo, luz difusa, regra dos terços e texturas | `hRjzXFScKZc` |
| **Gus Avancini** | *Color Grading no CapCut - COR de FILME* | 199k | Curvas de tom, saturação seletiva, contraste e Teal & Orange | `T-akUfaSuiA` |
| **Jefe Vilanova** | *Vídeo CINEMATOGRÁFICO com o CELULAR* | 457k | Taxa de 24fps, regra dos 180° (shutter), estabilização e mobile | `bPhVgGJcsk4` |
| **Brainstorm Tutoriais** | *Como GRAVAR VÍDEOS cinematográficos* | 64k | Iluminação de três pontos, profundidade de campo e desfoque | `pPKiE4OFRlo` |

---

## 🏗 Arquitetura do RAG

```
d:\CHIEF YOUTUBE\rag_cinematic_editing\
├── data/
│   ├── audio/                  # 9 Áudios MP3 originais
│   ├── raw_transcripts/        # 9 Transcrições brutas Whisper em JSON com timestamps
│   ├── processed_markdowns/    # 9 Markdowns curados de alta densidade (100% desruidizados)
│   ├── knowledge_base.sqlite   # SQLite FTS5 multi-campo (conceito, princípio, execução, tags)
│   └── chroma/                 # Vector Store ChromaDB com embeddings sem ruído (Cosine)
├── search_rag.py               # Motor de busca híbrido (FTS5 BM25 + Vetorial Chroma)
├── curate_and_rebuild_rag.py   # Pipeline de curadoria, desruidização e reconstrução do RAG
├── transcribe_and_build_rag.py # Pipeline de transcrição Whisper local
└── README.md                   # Documentação do sistema
```

---

## 🧹 Engenharia e Curadoria dos Dados (RAG Pro Level)

A transcrição automática por voz (ASR) gera dois grandes problemas em bases RAG: **poluição por ruído conversacional** (jabás, piadas paralelas, saudações) e **erros fonéticos em jargões técnicos**. O pipeline aplicou:

1. **Eliminação de Stop-Context & Jabás**: Remoção total de anúncios (ex: Epidemic Sound), links de afiliados, pedidos de like/inscrição e conversas paralelas irrelevantes.
2. **Correção Léxica & Fonética**: Correção de jargões técnicos corrompidos pelo ASR (`Is Light Cut` ➔ `Slide Cut`, `cilos copo` ➔ `Osciloscópio / Waveform`, `Mético-Cut` ➔ `Match Cut`, `cartibressão` ➔ `Henri Cartier-Bresson`, `ratinhos` ➔ `rebarbas/silêncios mortos`, `tá milagem` ➔ `Timeline`, `Reck 719` ➔ `Rec. 709`).
3. **Chunking Semântico Atômico**: Cada bloco é uma **Unidade de Conhecimento** contendo:
   - **Técnica / Conceito**
   - **Princípio Causal (Por que funciona)**
   - **Instrução Técnica Prática de Timeline / Câmera**
   - **Minutagem exata com link direto no YouTube**
   - **Tags técnicas para busca léxica e vetorial**

---

## 🚀 Como Utilizar

### 1. Via Linha de Comando (CLI)

```bash
# Busca Híbrida (Recomendado)
python search_rag.py "como fazer corte na acao"

# Busca Textual FTS5 (BM25)
python search_rag.py "J-Cut e L-Cut" --mode fts

# Busca Vetorial Semântica (ChromaDB)
python search_rag.py "como dar tom dramático e escuro na cor" --mode vector

# Retornar em JSON estruturado
python search_rag.py "sound design diegético" --json
```

### 2. Via Skill no Hermes Agent

A skill `cinematic-video-editing` está instalada e ativa no Hermes:
- Arquivo de definição: `.hermes/skills/cinematic-video-editing/SKILL.md`
- Handler Python: `.hermes/skills/cinematic-video-editing/handler.py`

Exemplo de chamada direta:
```python
from handler import handle

results = handle("regra dos 180 graus shutter speed", top_k=3)
print(results)
```
