#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
HERMES CHIEF TRADING // GRAVADOR DE AULA 100% AUTOMÁTICO - IQ OPTION
Canal: El Cazador del Wins (@elcazadordelwins)
Carrega o mapeamento persistente 'iqoption_mapped_coords.json' de alta precisão
=============================================================================
"""

import sys
import os
import time
import json
import threading
from pathlib import Path
import pyautogui
import cv2
import numpy as np
import mss

# Safe stdout on Windows UTF-8
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

CONFIG_FILE = Path("D:/CHIEF YOUTUBE/iqoption_mapped_coords.json").resolve()
OUTPUT_DIR = Path("D:/CHIEF YOUTUBE/gravacoes_iqoption").resolve()
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Mapeamento padrão automático para monitor 1920x1080
MAPA_PADRAO = {
    "tipo_grafico": (28, 775),
    "opcao_velas": (115, 775),
    "periodo_vela": (28, 830),
    "opcao_5s": (115, 830),
    "indicadores": (28, 935),
    "busca_indicadores": (180, 220),
    "btn_call": (1835, 515),
    "btn_put": (1835, 625),
    "centro_grafico": (960, 540),
    "topo_grafico": (960, 350),
    "fundo_grafico": (960, 730)
}

def carregar_mapa_precisao():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "elements" in data:
                    res = {}
                    for k, v in data["elements"].items():
                        res[k] = (v["x"], v["y"])
                    return res, data.get("metadata", {})
        except Exception:
            pass
    return MAPA_PADRAO, {"status": "PADRAO_1080P"}

BANNER = r"""
╔══════════════════════════════════════════════════════════════════════════════╗
║   🎯 AULA 100% AUTOMATIZADA: IQ OPTION (5 SEGUNDOS + BOLLINGER)             ║
║   Canal: El Cazador del Wins (@elcazadordelwins)                              ║
║   Precisão: Carregando 'iqoption_mapped_coords.json'                         ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

def print_sep(char="─", length=76):
    print(char * length)

def mover_suave(x, y, dur=0.7):
    """Move o mouse com aceleração natural e suave para parecer humano na aula."""
    pyautogui.moveTo(x, y, duration=dur, tween=pyautogui.easeInOutQuad)

def executar_aula_e_gravar(pontos):
    """Grava a tela em 1080p e executa toda a sequência da aula passo a passo."""
    video_file = OUTPUT_DIR / f"aula_cazador_5s_{int(time.time())}.mp4"
    
    print("\n" + "═" * 76)
    print("🎬 INICIANDO GRAVAÇÃO AUTOMÁTICA DA AULA COM ALTA PRECISÃO!")
    print("Ao apertar ENTER:")
    print("1. Você terá 5 segundos de contagem para deixar a IQ Option em TELA CHEIA.")
    print("2. O gravador 1080p começa a rodar.")
    print("3. O robô vai mover o mouse sozinho, clicar no menu, aplicar os 5s,")
    print("   abrir os indicadores, fazer a análise visual e disparar as ordens ao vivo.")
    print("═" * 76)
    
    input("\n[Pressione ENTER para iniciar a contagem e gravar] >>> ")
    
    for c in range(5, 0, -1):
        print(f"⏱️ Gravando em {c}s... (Deixe a IQ Option aberta em tela cheia)")
        time.sleep(1)
        
    stop_event = threading.Event()
    
    def gravador():
        with mss.mss() as sct:
            # Monitor 1 (Principal 1920x1080)
            monitor = sct.monitors[1]
            w = monitor["width"]
            h = monitor["height"]
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(str(video_file), fourcc, 25.0, (w, h))
            
            while not stop_event.is_set():
                img = np.array(sct.grab(monitor))
                frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                out.write(frame)
                time.sleep(1 / 30.0)
            
            out.release()
            
    thread = threading.Thread(target=gravador, daemon=True)
    thread.start()
    
    print("\n🔴 [GRAVAÇÃO ATIVADA] O robô está executando a aula na tela...")
    print_sep()
    
    # ATO 1: Configuração do Gráfico para Velas
    print("📌 [ATO 1] Clicando no menu para colocar em Velas (Candles)...")
    mover_suave(*pontos["tipo_grafico"], dur=1.0)
    time.sleep(0.4)
    pyautogui.click()
    time.sleep(0.7)
    
    mover_suave(*pontos["opcao_velas"], dur=0.6)
    time.sleep(0.4)
    pyautogui.click()
    time.sleep(1.0)
    
    # ATO 2: Configuração do Tempo para 5 Segundos
    print("📌 [ATO 2] Clicando para ajustar o tempo de vela em 5 Segundos (5s)...")
    mover_suave(*pontos["periodo_vela"], dur=0.8)
    time.sleep(0.4)
    pyautogui.click()
    time.sleep(0.7)
    
    mover_suave(*pontos["opcao_5s"], dur=0.6)
    time.sleep(0.4)
    pyautogui.click()
    time.sleep(1.2)
    
    # ATO 3: Indicadores (Bandas de Bollinger)
    print("📌 [ATO 3] Abrindo Indicadores e aplicando Bandas de Bollinger...")
    mover_suave(*pontos["indicadores"], dur=0.9)
    time.sleep(0.4)
    pyautogui.click()
    time.sleep(1.0)
    
    pyautogui.write("Bollinger", interval=0.08)
    time.sleep(0.8)
    pyautogui.press("enter")
    time.sleep(1.2)
    
    # Fecha menu de indicadores clicando de volta no gráfico
    mover_suave(*pontos["centro_grafico"], dur=0.8)
    pyautogui.click()
    time.sleep(1.2)
    
    # ATO 4: Gestos Didáticos no Gráfico (Explicando a estratégia)
    print("📌 [ATO 4] Movendo o mouse pelo gráfico para explicar suporte/resistência...")
    # Aponta para a banda de cima (Resistência)
    mover_suave(*pontos["topo_grafico"], dur=1.2)
    time.sleep(1.5)
    # Aponta para o meio
    mover_suave(*pontos["centro_grafico"], dur=0.9)
    time.sleep(1.0)
    # Aponta para a banda de baixo (Suporte)
    mover_suave(*pontos["fundo_grafico"], dur=1.2)
    time.sleep(1.5)
    
    # ATO 5: Executando a 1ª Operação de VENDA (PUT) no topo
    print("📌 [ATO 5] Vela tocou no topo: Executando 1ª Operação de VENDA (PUT)...")
    mover_suave(*pontos["btn_put"], dur=0.8)
    time.sleep(0.3)
    pyautogui.click()
    print("   ⚡ Ordem de Venda Enviada! Acompanhando oscilação de 5s...")
    
    # Volta o mouse pro centro e espera a vela oscilar
    mover_suave(*pontos["centro_grafico"], dur=0.6)
    time.sleep(7.0)
    
    # ATO 6: Rompimento / 2ª Operação de Venda (Martingale)
    print("📌 [ATO 6] Tendência continua rompendo: Executando 2ª Operação (Martingale de Venda)...")
    mover_suave(*pontos["btn_put"], dur=0.6)
    time.sleep(0.2)
    pyautogui.click()
    print("   ⚡ Segunda Ordem Enviada! Gravando o Loss da micro-tendência ao vivo...")
    
    mover_suave(*pontos["centro_grafico"], dur=0.6)
    time.sleep(8.0)
    
    # ATO 7: Tentativa de reversão no fundo (COMPRA / CALL)
    print("📌 [ATO 7] Reversão no fundo: Executando Operação de COMPRA (CALL)...")
    mover_suave(*pontos["btn_call"], dur=0.8)
    time.sleep(0.3)
    pyautogui.click()
    print("   ⚡ Ordem de Compra Enviada!")
    
    mover_suave(*pontos["centro_grafico"], dur=0.6)
    time.sleep(10.0)
    
    # ATO 8: Finalização
    print("📌 [ATO 8] Finalizando a aula e registrando o saldo...")
    mover_suave(*pontos["centro_grafico"], dur=1.0)
    time.sleep(4.0)
    
    # Stop recording
    stop_event.set()
    thread.join(timeout=3)
    
    print("\n" + "═" * 76)
    print("🎉 AULA GRAVADA COM SUCESSO EM 1080P!")
    print(f"📹 Arquivo de Vídeo: {video_file}")
    print(f"📁 Pasta: {OUTPUT_DIR}")
    print("═" * 76)

def main():
    print(BANNER)
    pontos, meta = carregar_mapa_precisao()
    w, h = pyautogui.size()
    print(f"🖥️ Monitor: {w}x{h} | Mapeamento Ativo: {meta.get('status', 'OK')}")
    print(f"📁 Arquivo de Configuração: {CONFIG_FILE}")
    print("─" * 76)
    
    executar_aula_e_gravar(pontos)

if __name__ == "__main__":
    main()
