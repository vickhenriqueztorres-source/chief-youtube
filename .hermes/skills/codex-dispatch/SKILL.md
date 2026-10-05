---
name: codex-dispatch
description: "Disparo e sincronização de Temas e Roteiros do Hermes diretamente para o Codex (e projetos de vídeo/edição como VoiceCut, Canal Brecha, HSL Studio, etc.) usando o MCP hermes_codex_bridge."
---

# SKILL: CODEX DISPATCH // HERMES -> CODEX BRIDGE

Esta skill ensina o Hermes a despachar ideias validadas, Big Ideas, temas e roteiros completos para o Codex e pipelines de produção locais.

## Quando usar:
- Quando o usuário disser:
  - "Manda esse tema pro Codex"
  - "Envia esse roteiro pro Codex"
  - "Despacha pro Codex iniciar a produção"
  - "Coloca no pipeline do VoiceCut / Brecha / Cazador"
  - "Quais temas/roteiros estão no inbox do Codex?"

## Ferramentas Disponíveis no MCP `hermes_codex_bridge`:
1. `send_theme_to_codex`:
   - Use para registrar temas validados, hooks e Big Ideas.
   - Parâmetros: `title`, `channel`, `big_idea`, `hook`, `target_audience`, `angles_and_research`, `notes`, `target_project_path`, `auto_trigger_codex`.

2. `send_script_to_codex`:
   - Use para enviar roteiros completos com marcações de cena, narração e CTA.
   - Parâmetros: `title`, `channel`, `script_content`, `hook`, `cta`, `voice_id`, `notes`, `target_project_path`, `auto_trigger_codex`.

3. `list_codex_inbox`:
   - Use para consultar itens pendentes, em progresso ou concluídos.

4. `get_codex_inbox_item`:
   - Detalhes e conteúdo completo de um item específico por ID.

5. `list_codex_projects`:
   - Descobre projetos e diretórios de vídeo cadastrados no Codex.

6. `trigger_codex_task`:
   - Dispara uma execução autônoma via CLI do Codex (`codex exec`).

## Boas Práticas:
- Sempre confirme o `channel` (ex: "Canal Brecha", "El Cazador de Wins", "Trading Labs", "VoiceCut", "O Outro Lado").
- Se o roteiro tiver sugestão de voz (ElevenLabs), preencha o campo `voice_id`.
- Se o usuário pedir para o Codex já começar a rodar ou produzir, defina `auto_trigger_codex=True`.
- Após o envio, informe o ID gerado (ex: `THM-20261001-XXXX` ou `SCR-20261001-XXXX`) e o caminho do arquivo gerado para que o usuário saiba exatamente onde o material foi salvo.
