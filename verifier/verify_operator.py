#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from cryptocert.operator import verify_L4
ok,bad,_=verify_L4()
print(f"[{'PASS' if ok else 'FAIL'}] L^4 = 0xD8 I on all 16 GF(2^8) basis vectors")
raise SystemExit(0 if ok else 1)
