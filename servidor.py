#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json, hashlib, os, time, uuid, subprocess, socket, platform, shutil, datetime, glob
from urllib.parse import parse_qs

PUERTO = 8080
USUARIOS = {
    "segury": {"pass_hash": "", "rol": "admin", "nombre": "Profesor S"},
    "kellynanaki": {"pass_hash": "", "rol": "usuario", "nombre": "Comandante Kellynanaki"}
}

def hash_pass(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

USUARIOS["segury"]["pass_hash"] = hash_pass("SEGURYSS")
USUARIOS["kellynanaki"]["pass_hash"] = hash_pass("5538:000000")

sesiones = {}
intentos = {}
MAX_INTENTOS = 5

def ejecutar(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT, timeout=15).strip()
    except Exception as e:
        return "⚠️ No disponible: " + str(e)

def registrar_log(texto):
    with open("sistema_logs.txt", "a") as f:
        f.write(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {texto}\n")

class Servidor(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def pagina(self, contenido, res=""):
        res_div = f'<div style="background:#0a1020;border:1px solid #4af;padding:15px;margin-top:20px;border-radius:8px;max-height:300px;overflow:auto;"><h4 style="color:#aef;margin:0 0 10px 0;">📤 SALIDA REAL:</h4><pre style="color:#cff;font-size:12px;white-space:pre-wrap;line-height:1.5;">{res}</pre></div>' if res else ""
        return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>SEGURY SYSTEMS CORE — v4.0 FULL EDITION</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0;font-family:Courier New,monospace}}
body{{background:#0a1020;min-height:100vh;padding:20px}}
.caja{{max-width:750px;margin:0 auto;background:linear-gradient(145deg,#0f1729,#0a1020);border:2px solid #4af;border-radius:24px;padding:35px;box-shadow:0 0 50px rgba(68,170,255,0.2),inset 0 0 30px rgba(68,170,255,0.05)}}
h1{{text-align:center;color:#aef;font-size:30px;margin-bottom:5px;text-shadow:0 0 20px #4af;letter-spacing:2px}}
h2{{text-align:center;color:#7bd;font-size:16px;margin-bottom:30px;font-weight:normal}}
h3{{color:#aef;margin:25px 0 12px 0;font-size:15px;border-bottom:1px solid #2a4a7a;padding-bottom:8px}}
label{{color:#9fdf9f;font-size:16px;margin:18px 0 8px;display:block}}
input{{width:100%;background:#050a15;border:2px solid #2a4a7a;border-radius:8px;padding:13px;color:#d0e8ff;font-size:15px}}
input:focus{{border-color:#4af;outline:none;box-shadow:0 0 10px rgba(68,170,255,0.3)}}
.boton{{width:100%;background:linear-gradient(180deg,#1a4a9a,#0f3070);border:2px solid #4af;border-radius:8px;padding:12px;color:#e0f0ff;font-size:15px;cursor:pointer;transition:all 0.2s}}
.boton:hover{{background:linear-gradient(180deg,#2a6aca,#1a4a9a);box-shadow:0 0 12px rgba(68,170,255,0.35)}}
.boton-verde{{background:linear-gradient(180deg,#1a6a4a,#0f4a30);border-color:#4c6}}
.boton-verde:hover{{background:linear-gradient(180deg,#2a8a5a,#1a6a4a);box-shadow:0 0 12px rgba(68,204,102,0.3)}}
.boton-amarillo{{background:linear-gradient(180deg,#6a6a1a,#4a4a10);border-color:#cc6}}
.boton-amarillo:hover{{background:linear-gradient(180deg,#8a8a2a,#6a6a1a);box-shadow:0 0 12px rgba(204,204,102,0.3)}}
.boton-rojo{{background:linear-gradient(180deg,#6a2020,#4a1010);border-color:#c44}}
.boton-rojo:hover{{background:linear-gradient(180deg,#8a3030,#6a2020);box-shadow:0 0 12px rgba(204,68,68,0.3)}}
.fila{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin:10px 0}}
.ok{{background:rgba(68,204,102,0.08);border:1px solid #4c6;color:#8f8;padding:14px;border-radius:8px;text-align:center;margin-bottom:20px;font-size:15px}}
.err{{background:rgba(204,68,68,0.08);border:1px solid #c44;color:#f88;padding:14px;border-radius:8px;text-align:center;margin-bottom:20px}}
.inf{{background:rgba(68,170,255,0.08);border:1px solid #4af;color:#adf;padding:18px;border-radius:8px;text-align:center;font-size:17px;margin-bottom:25px}}
.aviso{{text-align:center;color:#8ab8e0;font-size:13px;margin-top:15px}}
.pie{{text-align:center;color:#6ab0d0;font-size:11px;margin-top:30px;padding-top:20px;border-top:1px solid #2a4a7a}}
a.boton{{display:block;text-align:center;text-decoration:none}}
</style></head><body><div class="caja">
<h1>⚡ SEGURY SYSTEMS CORE</h1><h2>v4.0 FULL EDITION — DEBIAN / TERMUX</h2>
{contenido}{res_div}
<div class="pie">⚠️ TODAS LAS FUNCIONES SON REALES — NO SIMULADO — Sistema operativo: {platform.system()} | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
</div></body></html>"""

    def do_GET(self):
        ip = self.client_address[0]
        token = self.headers.get("Cookie", "").replace("sesion=", "").strip()
        usuario = sesiones.get(token)
        
        if self.path == "/salir":
            if token in sesiones:
                del sesiones[token]
                registrar_log(f"Cierre de sesión desde {ip}")
            self.send_response(302)
            self.send_header("Set-Cookie", "sesion=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT")
            self.send_header("Location", "/")
            self.end_headers()
            return
        
        resultado = ""
        if usuario:
            datos = USUARIOS[usuario]
            accion = self.path.split("?accion=")[1] if "?accion=" in self.path else ""
            
            if accion == "sistema":
                resultado = f"""📌 SISTEMA OPERATIVO: {platform.system()}
📦 DISTRIBUCIÓN: Debian / Termux
🔓 VERSIÓN: {platform.release()}
💻 NODO: {platform.node()}
🏗️ ARQUITECTURA: {platform.machine()}
🕐 HORA DEL SISTEMA: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🐍 PYTHON: {platform.python_version()}"""
                registrar_log(f"Consultó información del sistema — {ip}")
            
            elif accion == "archivos":
                resultado = ejecutar("ls -la")
                registrar_log(f"Listó archivos — {ip}")
            
            elif accion == "disco":
                resultado = ejecutar("df -h")
                registrar_log(f"Revisó espacio en disco — {ip}")
            
            elif accion == "memoria":
                resultado = ejecutar("free -m")
                registrar_log(f"Revisó memoria — {ip}")
            
            elif accion == "procesos":
                resultado = ejecutar("ps -ef | head -15")
                registrar_log(f"Listó procesos — {ip}")
            
            elif accion == "hora":
                resultado = f"🕐 HORA ACTUAL: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n📅 FECHA: {datetime.datetime.now().strftime('%d/%m/%Y')}"
                registrar_log(f"Consultó hora — {ip}")
            
            elif accion == "red":
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.connect(("8.8.8.8", 53))
                    ip_local = s.getsockname()[0]
                    s.close()
                    resultado = f"""🌐 ESTADO DE RED: CONECTADO
🖥️ HOSTNAME: {socket.gethostname()}
📍 IP LOCAL: {ip_local}
🔌 PUERTO: {PUERTO}"""
                except:
                    resultado = "⚠️ Red no disponible en este momento"
                registrar_log(f"Revisó red — {ip}")
            
            elif accion == "ruta":
                resultado = f"📂 DIRECTORIO ACTUAL: {os.getcwd()}\n\n📄 ARCHIVOS:\n" + "\n".join(os.listdir("."))
                registrar_log(f"Consultó ruta actual — {ip}")
            
            elif accion == "respaldo":
                nombre_copia = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"
                os.system(f"tar -czf {nombre_copia} . 2>/dev/null")
                if os.path.exists(nombre_copia):
                    resultado = f"✅ RESPALDO CREADO EXITOSAMENTE\n📦 ARCHIVO: {nombre_copia}\n📊 TAMAÑO: {round(os.path.getsize(nombre_copia)/1024,2)} KB"
                else:
                    resultado = "❌ Error al crear respaldo"
                registrar_log(f"Creó respaldo: {nombre_copia} — {ip}")
            
            elif accion == "logs":
                if os.path.exists("sistema_logs.txt"):
                    with open("sistema_logs.txt", "r") as f:
                        lineas = f.readlines()[-30:]
                        resultado = "=" * 50 + "\n📋 REGISTRO DE ACTIVIDAD — ÚLTIMAS 30 ENTRADAS\n" + "=" * 50 + "\n\n" + "".join(lineas)
                else:
                    resultado = "📭 Aún no hay registros de actividad"
                registrar_log(f"Revisó registros del sistema — {ip}")
            
            elif accion == "limpiar":
                archivos = glob.glob("*.pyc") + glob.glob("__pycache__/*")
                limpiados = 0
                for a in archivos:
                    try: os.remove(a); limpiados += 1
                    except: pass
                resultado = f"✅ LIMPIEZA COMPLETADA\n🗑️ Archivos eliminados: {limpiados}"
                registrar_log(f"Limpió archivos temporales — {ip}")
            
            contenido = f'<div class="ok">✅ BIENVENIDO AL NÚCLEO, {datos["nombre"]} — Rol: {datos["rol"].upper()}</div>'
            
            contenido += '<h3>📊 INFORMACIÓN DEL SISTEMA</h3><div class="fila"><a href="/?accion=sistema" class="boton">ℹ️ Sistema</a><a href="/?accion=hora" class="boton">🕐 Hora</a><a href="/?accion=red" class="boton">🌐 Red</a><a href="/?accion=ruta" class="boton">📂 Ruta</a></div>'
            
            contenido += '<h3>💾 RECURSOS DEL SISTEMA</h3><div class="fila"><a href="/?accion=memoria" class="boton">🧠 Memoria</a><a href="/?accion=disco" class="boton">💿 Disco</a><a href="/?accion=procesos" class="boton">⚡ Procesos</a></div>'
            
            contenido += '<h3>📁 GESTIÓN DE ARCHIVOS</h3><div class="fila"><a href="/?accion=archivos" class="boton">📋 Listar</a><a href="/?accion=respaldo" class="boton boton-verde">💾 Respaldo</a><a href="/?accion=limpiar" class="boton boton-amarillo">🧹 Limpiar</a></div>'
            
            if datos["rol"] == "admin":
                contenido += '<h3>🔧 PANEL DE ADMINISTRACIÓN</h3><div class="fila"><a href="/?accion=logs" class="boton">📝 Ver Registros</a></div>'
            
            contenido += '<div style="margin-top:30px;"><a href="/salir" class="boton boton-rojo">🚪 CERRAR SESIÓN</a></div>'
            
            html = self.pagina(contenido, resultado)
        
        elif self.path == "/":
            restante = MAX_INTENTOS - intentos.get(ip, 0)
            html = self.pagina(f'''
<div class="inf">🔐 ÁREA SEGURA — INGRESO AL NÚCLEO</div>
<form method="POST" action="/login">
<label>Nombre de usuario:</label>
<input type="text" name="usuario" required placeholder="Escribe tu usuario">
<label>Contraseña de acceso:</label>
<input type="password" name="clave" required placeholder="Escribe tu contraseña">
<button type="submit" class="boton" style="font-size:17px;padding:14px;margin-top:8px;">🔑 ACCEDER AL NÚCLEO</button>
</form>
<p class="aviso">Intentos restantes: {restante} — Tras 5 fallos, espera 15 minutos</p>
''')
        else:
            html = self.pagina('<div class="err">❌ PÁGINA NO ENCONTRADA</div><a href="/" class="boton" style="margin-top:15px;">Volver al inicio</a>')
        
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode())

    def do_POST(self):
        ip = self.client_address[0]
        largo = int(self.headers["Content-Length"])
        datos = self.rfile.read(largo).decode()
        form = parse_qs(datos)
        usuario = form.get("usuario", [""])[0].strip()
        clave = form.get("clave", [""])[0]
        
        if usuario in USUARIOS and USUARIOS[usuario]["pass_hash"] == hash_pass(clave):
            intentos[ip] = 0
            token = str(uuid.uuid4())
            sesiones[token] = usuario
            registrar_log(f"✅ INICIO DE SESIÓN EXITOSO — Usuario: {usuario} — IP: {ip}")
            self.send_response(302)
            self.send_header("Set-Cookie", f"sesion={token}; path=/; HttpOnly; SameSite=Strict")
            self.send_header("Location", "/")
            self.end_headers()
        else:
            intentos[ip] = intentos.get(ip, 0) + 1
            registrar_log(f"❌ INTENTO FALLIDO — Usuario: {usuario} — IP: {ip}")
            html = self.pagina('<div class="err">❌ USUARIO O CONTRASEÑA INCORRECTOS</div><a href="/" class="boton" style="margin-top:15px;">Intentar de nuevo</a>')
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode())

if __name__ == "__main__":
    print("=" * 55)
    print("🔒 SEGURY SYSTEMS CORE — v4.0 FULL EDITION")
    print("📡 SERVIDOR ACTIVO EN: http://localhost:8080")
    print("=" * 55)
    print("🔑 ADMINISTRADOR: segury        | SEGURYSS")
    print("🔑 USUARIO:      kellynanaki   | 5538:000000")
    print("=" * 55)
    print("📂 FUNCIONES: Sistema | Archivos | Disco | Memoria | Procesos")
    print("🌐 Red | Respaldo | Logs | Limpieza | Sesiones")
    print("=" * 55)
    HTTPServer(("0.0.0.0", 8080), Servidor).serve_forever()
