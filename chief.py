#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hermes Chief - CLI Entrypoint
Run: python chief.py [command] [args] or python chief.py for interactive mode.
"""

import sys
import io
from pathlib import Path

# Safe UTF-8 output on Windows consoles
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# Ensure root dir is in path
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

if len(sys.argv) > 1 and (sys.argv[1] in ["trading", "--trading"] or any("profe" in arg.lower() or "vela" in arg.lower() for arg in sys.argv)):
    if sys.argv[1] in ["trading", "--trading"]:
        sys.argv.pop(1)
    from chief_trading import main as trading_main
    if __name__ == "__main__":
        trading_main()
else:
    from src.interfaces.cli import main
    if __name__ == "__main__":
        main()
