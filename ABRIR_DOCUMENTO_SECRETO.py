#!/usr/bin/env python3
import os, getpass, hashlib
CLAVE = "5538000000"
CARPETA = os.path.expanduser("~/Segury-Systems-Core/.SECRETO_5538")
ARCHIVO = f"{CARPETA}/MANUAL_MITIGACION_WASHINGTON.txt.gpg"
HASH = f"{CARPETA}/HASH_VERIFICACION.txt"
os.system("clear")
print("""
🔒 DOCUMENTO CLASIFICADO — AGENTE 86
CIFRADO AES-256 · ACCESO RESTRINGIDO
""")
c = getpass.getpass("CLAVE → ")
if c != CLAVE:
    print("\n🚫 DENEGADO")
    exit(1)
with open(HASH, "r") as f: hash_ok = f.read().split()[0]
with open(ARCHIVO, "rb") as f: hash_act = hashlib.sha256(f.read()).hexdigest()
if hash_act != hash_ok:
    print("⚠️ ALERTA: DOCUMENTO ALTERADO")
    exit(1)
print("✅ VERIFICADO — ABRINDO...\n")
os.system(f"gpg --decrypt --batch --passphrase '{CLAVE}' '{ARCHIVO}' 2>/dev/null")
print("\n🔒 CERRADO")
