#!/usr/bin/env python3
import sys, os, time, datetime, getpass, socket
from pathlib import Path

BASE = Path.home() / "Segury-Systems-Core"
REGISTRO = BASE / "nucleo_registro.log"
CLAVE = "SEGURYSS"
MAX_INT = 3

def hablar(txt):
    try: os.system(f"termux-tts-speak '{txt}' 2>/dev/null &")
    except: pass

def registrar(tipo, dato):
    BASE.mkdir(exist_ok=True)
    with open(REGISTRO,"a") as f:
        f.write(f"[{datetime.datetime.now():%Y-%m-%d %H:%M:%S}] [{tipo}] {dato}\n")

def cabecera():
    os.system("clear")
    print("""
╔══════════════════════════════════════════════════════════════╗
║  🔰 NÚCLEO SEGURY-HACKING CORE v1.7 — ACTIVO                  ║
║  👑 MANDO: PROFESOR SEGURY SSC                                ║
║  ⚠️  SOLO UNA PERSONA PUEDE ENTRAR                             ║
╚══════════════════════════════════════════════════════════════╝
""")

def entrar():
    cabecera()
    print("🔑 CLAVE\n")
    for n in range(1, MAX_INT+1):
        c = getpass.getpass(f"INTENTO {n}/{MAX_INT} → ")
        if c == CLAVE:
            registrar("ACCESO", "ENTRADA OK")
            cabecera()
            print(f"""
    ✅ DESBLOQUEADO
    👑 PROFESOR SEGURY SSC — EN CONTROL
    ⏰ {datetime.datetime.now():%d/%m/%Y %H:%M:%S}
""")
            hablar("Bienvenido Profesor Segury")
            return True
        print(f"    ❌ INCORRECTO. Quedan {MAX_INT-n}\n")
    registrar("BLOQUEO", "CERRADO")
    print("    🚫 ACCESO DENEGADO")
    sys.exit(1)

def menu():
    while True:
        cabecera()
        print("""
  📋 MENÚ PRINCIPAL

  [1] SISTEMA Y RECURSOS
  [2] RED Y CONEXIONES
  [3] SEGURIDAD Y REGISTRO
  [4] EJECUTAR COMANDO
  [0] SALIR
""")
        op = input("  → ")
        if op == "1":
            cabecera()
            print(f"  HOST: {socket.gethostname()}\n  USR: {os.getlogin()}\n  DIR: {os.getcwd()}\n")
            os.system("df -h ~")
            input("\n  ENTER → ")
        elif op == "2":
            cabecera()
            os.system("ss -tuln")
            input("\n  ENTER → ")
        elif op == "3":
            cabecera()
            if REGISTRO.exists(): os.system(f"cat {REGISTRO}")
            input("\n  ENTER → ")
        elif op == "4":
            cabecera()
            os.system(input("  COMANDO → "))
            input("\n  ENTER → ")
        elif op == "0":
            registrar("SALIDA", "CERRADO")
            print("\n  🔒 BLOQUEADO")
            sys.exit(0)

if __name__ == "__main__":
    if entrar(): menu()

