#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  GRANJA MASTER v6.0 — PROFESOR SEGURY SSC · SCRIPT ÚNICO DEFINITIVO      ║
# ║  Arquitectura: Modular · Todo en uno · Actualizable en 1 paso            ║
# ║  Plataforma: Termux / Android · Lectura nativa /proc                     ║
# ║  Idiomas: ES · EN · RU · WebSockets en Vivo · 7 Nodos                     ║
# ║  Clave: A52-5538 · Nivel: PRODUCCIÓN · DEFINITIVO                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

from flask import Flask, render_template_string, request, redirect, url_for, session
from flask_socketio import SocketIO
import time
import threading
import os
import subprocess
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════
# MÓDULO 1 — CONFIGURACIÓN GENERAL
# ═══════════════════════════════════════════════════════════════════════════
app = Flask(__name__)
app.secret_key = "A52-PROFESOR-SEGURY-SSC-GRANJA-MASTER-2026"
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

CONFIG = {
    "nombre_sistema": "GRANJA MASTER",
    "version": "v6.0",
    "autor": "PROFESOR SEGURY SSC",
    "puerto": 5538,
    "clave_sistema": "A52-5538"
}

USUARIOS = {
    "segury86@gmail.com": {
        "nombre": "Profesor Segury SSC",
        "pass": "13131313.@",
        "nivel": "DIRECTOR 👑",
        "idioma": "es"
    },
    "appsmobiloficial@gmail.com": {
        "nombre": "Octavio",
        "pass": "14012009",
        "nivel": "OPERADOR 🤝",
        "idioma": "es"
    }
}

# ═══════════════════════════════════════════════════════════════════════════
# MÓDULO 2 — IDIOMAS
# ═══════════════════════════════════════════════════════════════════════════
TEXTOS = {
    "es": {
        "titulo": "GRANJA MASTER · PANEL DE CONTROL v6.0",
        "bienvenida": "Bienvenido",
        "sistemas": "SISTEMAS",
        "granja": "GRANJA DE DISPOSITIVOS",
        "monitoreo": "MONITOREO EN VIVO",
        "herramientas": "HERRAMIENTAS",
        "respaldos": "RESPALDOS",
        "ajustes": "AJUSTES",
        "nodos": "Nodos del Sistema",
        "conexiones": "Estado de Conexiones",
        "escanear": "Escanear Red",
        "recursos": "Recursos del Sistema",
        "diagnostico": "Diagnóstico Completo",
        "limpieza": "Limpieza del Sistema",
        "respaldar": "Crear Respaldo",
        "red": "Estado de Red",
        "encender": "Encender",
        "apagar": "Apagar",
        "reiniciar": "Reiniciar",
        "conectado": "CONECTADO",
        "desconectado": "DESCONECTADO",
        "sin_datos": "Sin datos",
        "idioma": "Idioma",
        "cerrar": "Cerrar Sesión",
        "login_titulo": "ACCESO AUTORIZADO · SEGURY-SYSTEMS",
        "correo": "Correo electrónico",
        "clave": "Contraseña",
        "entrar": "Ingresar al Sistema",
        "sin_permiso": "Credenciales no válidas",
        "nivel": "Nivel",
        "ultima_act": "Última actualización",
        "procesos": "Procesos",
        "memoria": "Memoria",
        "disco": "Disco",
        "cpu": "CPU",
        "estado_red": "Red",
        "filosofia": "Arquitectura: 1 Núcleo + Contenedores = Máxima Eficiencia",
        "resultados": "Resultados aparecerán aquí",
        "respaldo_info": "El respaldo se guarda en Descargas del teléfono",
        "restaurar": "Comando para restaurar",
        "uptime": "Tiempo Activo"
    },
    "en": {
        "titulo": "DEVICE FARM · CONTROL PANEL v6.0",
        "bienvenida": "Welcome",
        "sistemas": "SYSTEMS",
        "granja": "DEVICE FARM",
        "monitoreo": "LIVE MONITORING",
        "herramientas": "TOOLS",
        "respaldos": "BACKUPS",
        "ajustes": "SETTINGS",
        "nodos": "System Nodes",
        "conexiones": "Connection Status",
        "escanear": "Network Scan",
        "recursos": "System Resources",
        "diagnostico": "Full Diagnostics",
        "limpieza": "System Cleanup",
        "respaldar": "Create Backup",
        "red": "Network Status",
        "encender": "Power On",
        "apagar": "Power Off",
        "reiniciar": "Restart",
        "conectado": "CONNECTED",
        "desconectado": "DISCONNECTED",
        "sin_datos": "No data",
        "idioma": "Language",
        "cerrar": "Logout",
        "login_titulo": "AUTHORIZED ACCESS · SEGURY-SYSTEMS",
        "correo": "Email",
        "clave": "Password",
        "entrar": "Enter System",
        "sin_permiso": "Invalid credentials",
        "nivel": "Level",
        "ultima_act": "Last Update",
        "procesos": "Processes",
        "memoria": "Memory",
        "disco": "Disk",
        "cpu": "CPU",
        "estado_red": "Network",
        "filosofia": "Architecture: 1 Core + Containers = Maximum Efficiency",
        "resultados": "Results will appear here",
        "respaldo_info": "Backup saved in phone Downloads folder",
        "restaurar": "Restore command",
        "uptime": "Uptime"
    },
    "ru": {
        "titulo": "УПРАВЛЕНИЕ · СИСТЕМА v6.0",
        "bienvenida": "Добро пожаловать",
        "sistemas": "СИСТЕМЫ",
        "granja": "УСТРОЙСТВА",
        "monitoreo": "МОНИТОРИНГ",
        "herramientas": "ИНСТРУМЕНТЫ",
        "respaldos": "РЕЗЕРВНЫЕ КОПИИ",
        "ajustes": "НАСТРОЙКИ",
        "nodos": "Узлы Системы",
        "conexiones": "Статус Подключения",
        "escanear": "Сканировать Сеть",
        "recursos": "Ресурсы Системы",
        "diagnostico": "Диагностика",
        "limpieza": "Очистка Системы",
        "respaldar": "Создать Копию",
        "red": "Состояние Сети",
        "encender": "Включить",
        "apagar": "Выключить",
        "reiniciar": "Перезапуск",
        "conectado": "ПОДКЛЮЧЕНО",
        "desconectado": "ОТКЛЮЧЕНО",
        "sin_datos": "Нет данных",
        "idioma": "Язык",
        "cerrar": "Выйти",
        "login_titulo": "ДОСТУП РАЗРЕШЁН · СИСТЕМА",
        "correo": "Эл. почта",
        "clave": "Пароль",
        "entrar": "Войти",
        "sin_permiso": "Неверные данные",
        "nivel": "Уровень",
        "ultima_act": "Обновлено",
        "procesos": "Процессы",
        "memoria": "Память",
        "disco": "Диск",
        "cpu": "Процессор",
        "estado_red": "Сеть",
        "filosofia": "Архитектура: 1 Ядро + Контейнеры = Максимум Эффективности",
        "resultados": "Результаты появятся здесь",
        "respaldo_info": "Копия сохранена в папке Загрузки",
        "restaurar": "Команда восстановления",
        "uptime": "Время Работы"
    }
}

# ═══════════════════════════════════════════════════════════════════════════
# MÓDULO 3 — NODOS / SISTEMAS
# ═══════════════════════════════════════════════════════════════════════════
NODOS = {
    "jarvis": {
        "nombre": "🤖 JARVIS Core",
        "activo": True,
        "desc": "Asistente principal · Protocolo de Comunicación"
    },
    "synapse": {
        "nombre": "📊 SYNAPSE v4.5.1",
        "activo": True,
        "desc": "Monitoreo en Tiempo Real · Análisis de Métricas"
    },
    "alya": {
        "nombre": "💬 ALYA Bot",
        "activo": True,
        "desc": "Coordinación · Automatización de Tareas"
    },
    "starbot": {
        "nombre": "🛡️ STAR-BOT Defensa",
        "activo": True,
        "desc": "Seguridad · Vigilancia · Protección"
    },
    "nanosuite": {
        "nombre": "⚙️ NANOSUITE v2.2.0",
        "activo": True,
        "desc": "Núcleo Central · Diagnóstico y Control"
    },
    "lyra": {
        "nombre": "🎤 LYRA Independiente",
        "activo": True,
        "desc": "Voz · Multilenguaje · Asistente Autónoma"
    },
    "granja": {
        "nombre": "📱 GRANJA DE DISPOSITIVOS",
        "activo": True,
        "desc": "Gestión de Contenedores · Escalabilidad"
    }
}

# ═══════════════════════════════════════════════════════════════════════════
# MÓDULO 4 — DATOS Y LECTURA DEL SISTEMA
# ═══════════════════════════════════════════════════════════════════════════
DATOS = {
    "cpu": "--",
    "memoria_uso": "--",
    "memoria_libre": "--",
    "disco_uso": "--",
    "disco_libre": "--",
    "procesos": 0,
    "red": "Verificando...",
    "tiempo_activo": "00:00:00",
    "salida_herramienta": ""
}

INICIO = time.time()
CPU_ANTERIOR = None
IDLE_ANTERIOR = None

def actualizar_datos():
    """Lectura en tiempo real desde /proc — sin librerías externas"""
    global CPU_ANTERIOR, IDLE_ANTERIOR
    while True:
        try:
            # Memoria
            with open("/proc/meminfo", "r") as f:
                mem = f.read()
            total = int([l for l in mem.split("\n") if "MemTotal" in l][0].split()[1]) / 1024 / 1024
            libre = int([l for l in mem.split("\n") if "MemAvailable" in l][0].split()[1]) / 1024 / 1024
            DATOS["memoria_uso"] = f"{round(total - libre, 1)} GB"
            DATOS["memoria_libre"] = f"{round(libre, 1)} GB"

            # Disco
            statvfs = os.statvfs(os.path.expanduser("~"))
            total_d = statvfs.f_frsize * statvfs.f_blocks / (1024**3)
            libre_d = statvfs.f_frsize * statvfs.f_bfree / (1024**3)
            DATOS["disco_uso"] = f"{round(total_d - libre_d, 1)} GB"
            DATOS["disco_libre"] = f"{round(libre_d, 1)} GB"

            # Procesos
            DATOS["procesos"] = len([d for d in os.listdir("/proc") if d.isdigit()])

            # Red
            try:
                subprocess.run(["ping", "-c", "1", "-W", "2", "8.8.8.8"],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                DATOS["red"] = "✅ Conectado"
            except:
                DATOS["red"] = "❌ Sin conexión"

            # CPU
            try:
                with open("/proc/stat", "r") as f:
                    vals = list(map(int, f.readline().split()[1:]))
                total_cpu = sum(vals)
                idle = vals[3] + vals[4]
                if CPU_ANTERIOR is not None:
                    dt = total_cpu - CPU_ANTERIOR
                    di = idle - IDLE_ANTERIOR
                    uso = 100 * (dt - di) / dt if dt > 0 else 0
                    DATOS["cpu"] = f"{round(uso)}%"
                CPU_ANTERIOR, IDLE_ANTERIOR = total_cpu, idle
            except: pass

            # Tiempo activo
            seg = int(time.time() - INICIO)
            h = seg // 3600
            m = (seg % 3600) // 60
            s = seg % 60
            DATOS["tiempo_activo"] = f"{h:02d}:{m:02d}:{s:02d}"

        except Exception:
            pass

        socketio.emit("actualizar", {"nodos": NODOS, "datos": DATOS})
        time.sleep(2)

# ═══════════════════════════════════════════════════════════════════════════
# MÓDULO 5 — HERRAMIENTAS
# ═══════════════════════════════════════════════════════════════════════════
def ejecutar_herramienta(nombre):
    salida = ""
    try:
        if nombre == "nodos":
            salida = "📱 === NODOS DEL SISTEMA ===\n"
            salida += f"Equipo: {os.uname()[1]}\n"
            salida += f"Sistema: {os.uname()[0]} / {os.uname()[4]}\n\n"
            for k, v in NODOS.items():
                estado = "🟢 ACTIVO" if v["activo"] else "🔴 INACTIVO"
                salida += f"  {estado} | {v['nombre']}\n"
            salida += "\n💙 Dirigido por el Profesor Segury SSC\n"

        elif nombre == "conexiones":
            salida = "🌐 === CONEXIONES ===\n"
            salida += f"Puerto: {CONFIG['puerto']}\n"
            salida += f"CPU: {DATOS['cpu']}\n"
            salida += f"Memoria: {DATOS['memoria_uso']}\n"
            salida += f"Tiempo Activo: {DATOS['tiempo_activo']}\n"

        elif nombre == "escanear":
            salida = "🔌 === ESCANEO DE RED ===\n"
            try:
                res = subprocess.run(["ip", "-br", "link"], capture_output=True, text=True, timeout=8)
                salida += "Interfaces:\n" + res.stdout + "\n"
            except:
                salida += "Comando `ip` no disponible\n"

        elif nombre == "recursos":
            activos = sum(1 for v in NODOS.values() if v["activo"])
            salida = "📊 === RECURSOS DEL SISTEMA ===\n"
            salida += f"CPU:          {DATOS['cpu']}\n"
            salida += f"Memoria Uso:  {DATOS['memoria_uso']}\n"
            salida += f"Memoria Libre:{DATOS['memoria_libre']}\n"
            salida += f"Disco Uso:    {DATOS['disco_uso']}\n"
            salida += f"Disco Libre:  {DATOS['disco_libre']}\n"
            salida += f"Procesos:     {DATOS['procesos']}\n"
            salida += f"Red:          {DATOS['red']}\n"
            salida += f"Nodos Activos:{activos}/{len(NODOS)}\n"

        elif nombre == "diagnostico":
            salida = "🔍 === DIAGNÓSTICO COMPLETO ===\n"
            salida += f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
            salida += f"Sistema: {os.uname()[0]} {os.uname()[4]}\n"
            salida += f"CPU: {DATOS['cpu']}\n"
            salida += f"Memoria: {DATOS['memoria_uso']} / {DATOS['memoria_libre']}\n"
            salida += f"Disco: {DATOS['disco_uso']} / {DATOS['disco_libre']}\n"
            salida += f"Procesos: {DATOS['procesos']}\n"
            salida += f"Red: {DATOS['red']}\n"

        elif nombre == "limpieza":
            salida = "🧹 === LIMPIEZA DEL SISTEMA ===\n"
            try:
                res = subprocess.run(["apt", "autoremove", "-y"], capture_output=True, text=True, timeout=30)
                salida += res.stdout[-500:] if len(res.stdout) > 500 else res.stdout
                salida += "\n✅ Limpieza completada"
            except Exception as e:
                salida += f"Resultado: {str(e)}\n"

        elif nombre == "respaldar":
            fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
            archivo = f"GranjaMaster_BACKUP_{fecha}.tar.gz"
            destino = os.path.expanduser(f"~/storage/downloads/{archivo}")
            salida = "💾 === CREANDO RESPALDO ===\n"
            try:
                subprocess.run(["tar", "-zcf", destino, "-C", os.path.expanduser("~"), "Segury-Systems-Core"],
                              capture_output=True, timeout=120)
                tamaño = os.path.getsize(destino) / 1024
                salida += f"✅ RESPALDO CREADO\n"
                salida += f"Archivo: {archivo}\n"
                salida += f"Ubicación: Descargas\n"
                salida += f"Tamaño: {round(tamaño)} KB\n"
            except Exception as e:
                salida += f"❌ Error: {str(e)}\nInstala tar: pkg install tar"

        elif nombre == "red":
            salida = "🌐 === ESTADO DE RED ===\n"
            salida += f"Conexión: {DATOS['red']}\n"
            try:
                ip = subprocess.run(["curl", "-s", "--connect-timeout", "4", "ifconfig.me"],
                                   capture_output=True, text=True, timeout=8).stdout.strip()
                salida += f"IP Externa: {ip or 'No detectada'}\n"
            except:
                salida += "IP Externa: Sin respuesta\n"

        DATOS["salida_herramienta"] = salida
    except Exception as e:
        DATOS["salida_herramienta"] = f"❌ Error: {str(e)}"

# ═══════════════════════════════════════════════════════════════════════════
# MÓDULO 6 — RUTAS / CONTROLADORES
# ═══════════════════════════════════════════════════════════════════════════
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form.get("correo", "")
        clave = request.form.get("clave", "")
        if correo in USUARIOS and USUARIOS[correo]["pass"] == clave:
            session["usuario"] = correo
            session["lang"] = USUARIOS[correo]["idioma"]
            return redirect("/")
        return render_template_string(LOGIN_HTML, t=TEXTOS["es"], error=True)
    return render_template_string(LOGIN_HTML, t=TEXTOS["es"], error=False)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/lang/<codigo>")
def cambiar_idioma(codigo):
    if "usuario" in session and codigo in TEXTOS:
        session["lang"] = codigo
    return redirect("/")

@app.route("/")
def inicio():
    if "usuario" not in session:
        return redirect("/login")
    t = TEXTOS.get(session.get("lang", "es"), TEXTOS["es"])
    usuario = USUARIOS[session["usuario"]]
    return render_template_string(PRINCIPAL_HTML, t=t, usuario=usuario, datos=DATOS, nodos=NODOS, cfg=CONFIG)

@app.route("/encender/<nodo>")
def encender(nodo):
    if "usuario" in session and nodo in NODOS:
        NODOS[nodo]["activo"] = True
    return redirect("/")

@app.route("/apagar/<nodo>")
def apagar(nodo):
    if "usuario" in session and nodo in NODOS:
        NODOS[nodo]["activo"] = False
    return redirect("/")

@app.route("/reiniciar/<nodo>")
def reiniciar(nodo):
    if "usuario" in session and nodo in NODOS:
        NODOS[nodo]["activo"] = False
        time.sleep(0.5)
        NODOS[nodo]["activo"] = True
    return redirect("/")

@app.route("/ejecutar/<herramienta>", methods=["POST"])
def ejecutar(herramienta):
    if "usuario" not in session:
        return redirect("/login")
    ejecutar_herramienta(herramienta)
    return redirect("/")

# ═══════════════════════════════════════════════════════════════════════════
# MÓDULO 7 — INTERFAZ / PLANTILLAS
# ═══════════════════════════════════════════════════════════════════════════
LOGIN_HTML = """
<!DOCTYPE html><html lang="es">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{t['login_titulo']}}</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:'Segoe UI',system-ui}
body{background:linear-gradient(135deg,#0b1020,#1a1f3a,#0b1020);min-height:100vh;display:flex;align-items:center;justify-content:center;color:#e0e7ff}
.caja{background:rgba(20,27,51,.9);padding:40px;border-radius:20px;border:1px solid rgba(59,130,246,.3);width:90%;max-width:420px;box-shadow:0 0 40px rgba(59,130,246,.15)}
h1{font-size:24px;background:linear-gradient(90deg,#3b82f6,#8b5cf6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-align:center;margin-bottom:8px}
.sub{text-align:center;color:#94a3b8;margin-bottom:30px;font-size:13px}
input{width:100%;padding:14px;margin:8px 0;border-radius:10px;border:none;background:rgba(59,130,246,.1);color:white;font-size:15px;outline:1px solid rgba(59,130,246,.2)}
button{width:100%;padding:14px;margin-top:10px;border-radius:10px;border:none;background:linear-gradient(90deg,#3b82f6,#6366f1);color:white;font-weight:bold;font-size:16px;cursor:pointer;transition:transform .2s}
button:hover{transform:scale(1.02)}
.error{color:#f87171;text-align:center;margin-top:15px}
</style></head>
<body>
<div class="caja">
<h1>⚡ GRANJA MASTER</h1>
<p class="sub">{{t['login_titulo']}}</p>
<form method="post">
<input type="email" name="correo" placeholder="{{t['correo']}}" required>
<input type="password" name="clave" placeholder="{{t['clave']}}" required>
<button type="submit">{{t['entrar']}}</button>
</form>
{% if error %}<p class="error">{{t['sin_permiso']}}</p>{% endif %}
</div>
</body></html>
"""

PRINCIPAL_HTML = """
<!DOCTYPE html><html lang="es">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{cfg['nombre_sistema']}} {{cfg['version']}}</title>
<script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:system-ui}
:root{--fondo:#0b1020;--tarjeta:#141b33;--azul:#3b82f6;--verde:#10b981;--rojo:#ef4444;--dorado:#f59e0b;--texto:#e0e7ff;--suave:#94a3b8}
body{background:linear-gradient(135deg,var(--fondo),#1a1f3a,var(--fondo));min-height:100vh;color:var(--texto)}
.barra-sup{position:fixed;top:0;left:0;right:0;background:rgba(17,24,39,.9);backdrop-filter:blur(12px);padding:12px 20px;display:flex;justify-content:space-between;align-items:center;z-index:999;border-bottom:1px solid rgba(59,130,246,.2)}
.estado-socket{padding:6px 14px;border-radius:20px;font-weight:bold;font-size:13px;background:rgba(239,68,68,.2);color:#fca5a5}
.idiomas{display:flex;gap:6px}
.idioma{padding:6px 12px;border-radius:8px;border:none;background:rgba(255,255,255,.08);color:white;cursor:pointer;font-weight:bold;text-decoration:none}
.idioma.activo{background:linear-gradient(90deg,#3b82f6,#8b5cf6);box-shadow:0 0 12px rgba(59,130,246,.4)}
.contenedor{max-width:1200px;margin:70px auto 40px;padding:0 20px}
.titulo{font-size:26px;font-weight:bold;background:linear-gradient(90deg,#3b82f6,#8b5cf6,#ec4899,#3b82f6);background-size:300% 100%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-align:center;margin-bottom:5px;animation:titulo 8s linear infinite}
@keyframes titulo{0%{background-position:0% 50%}100%{background-position:300% 50%}}
.subtitulo{text-align:center;color:var(--suave);font-size:13px;margin-bottom:25px}
.usuario{text-align:right;margin-bottom:15px;font-size:14px}
.cerrar{color:#94a3b8;text-decoration:none;margin-left:10px}
.pestanas{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:20px;border-bottom:1px solid rgba(59,130,246,.15);padding-bottom:8px}
.pestana{padding:10px 16px;background:transparent;border:none;color:var(--suave);cursor:pointer;font-weight:600;border-radius:10px 10px 0 0}
.pestana.activa{color:var(--azul);background:rgba(59,130,246,.1);border-bottom:2px solid var(--azul)}
.panel{display:none}
.panel.activo{display:block;animation:aparecer .3s ease-out}
@keyframes aparecer{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:15px}
.tarjeta{background:var(--tarjeta);border-radius:16px;padding:20px;border:1px solid rgba(59,130,246,.15);transition:transform .2s,box-shadow .2s}
.tarjeta:hover{transform:translateY(-2px);box-shadow:0 8px 25px rgba(59,130,246,.1)}
.etiqueta{padding:5px 14px;border-radius:20px;font-size:12px;font-weight:bold;display:inline-block;margin-bottom:10px}
.et-on{background:rgba(16,185,129,.12);color:#34d399;border:1px solid rgba(16,185,129,.25)}
.et-off{background:rgba(239,68,68,.12);color:#f87171;border:1px solid rgba(239,68,68,.25)}
.botones{display:flex;gap:6px;margin-top:12px}
.btn{flex:1;padding:9px 8px;border:none;border-radius:10px;font-weight:bold;cursor:pointer;font-size:13px;transition:transform .15s;text-decoration:none;text-align:center;color:white}
.btn:active{transform:scale(.96)}
.btn-verde{background:linear-gradient(90deg,#10b981,#34d399)}
.btn-rojo{background:linear-gradient(90deg,#ef4444,#f87171)}
.btn-dorado{background:linear-gradient(90deg,#f59e0b,#fbbf24);color:#1f2937}
.btn-azul{background:linear-gradient(90deg,#3b82f6,#6366f1)}
.mon-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin-bottom:20px}
.mon-tarjeta{background:var(--tarjeta);border-radius:14px;padding:18px;text-align:center;border:1px solid rgba(59,130,246,.15)}
.mon-val{font-size:28px;font-weight:bold;color:var(--azul);margin:5px 0}
.herramienta{background:var(--tarjeta);border-radius:14px;padding:16px;border:1px solid rgba(59,130,246,.15);display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
.resultado{background:rgba(0,0,0,.3);border-radius:10px;padding:15px;margin-top:15px;font-family:monospace;font-size:12px;white-space:pre-wrap;max-height:350px;overflow-y:auto;color:#94f9d0;line-height:1.6}
.pie{text-align:center;margin-top:40px;color:var(--suave);font-size:12px;padding-bottom:20px}
</style></head>
<body>

<div class="barra-sup">
    <div><strong>⚡ {{cfg['nombre_sistema']}} {{cfg['version']}}</strong></div>
    <div id="estado-socket" class="estado-socket">🔴 Conectando...</div>
    <div class="idiomas">
        <a href="/lang/es" class="idioma {{'activo' if session.lang=='es' else ''}}">🇪🇸</a>
        <a href="/lang/en" class="idioma {{'activo' if session.lang=='en' else ''}}">🇬🇧</a>
        <a href="/lang/ru" class="idioma {{'activo' if session.lang=='ru' else ''}}">🇷🇺</a>
    </div>
</div>

<div class="contenedor">
    <div class="usuario">
        {{t['bienvenida']}}, <strong>{{usuario['nombre']}}</strong>
        <span style="color:#94a3b8;font-size:12px">({{usuario['nivel']}})</span>
        <a href="/logout" class="cerrar">{{t['cerrar']}}</a>
    </div>

    <h1 class="titulo">📱 GRANJA DE DISPOSITIVOS · SEGURY-SYSTEMS</h1>
    <p class="subtitulo">Dirigido por {{cfg['autor']}} · Lectura nativa /proc · WebSockets en vivo</p>

    <div class="pestanas">
        <button class="pestana activa" data-p="sistemas">{{t['sistemas']}}</button>
        <button class="pestana" data-p="granja">{{t['granja']}}</button>
        <button class="pestana" data-p="monitoreo">{{t['monitoreo']}}</button>
        <button class="pestana" data-p="herramientas">{{t['herramientas']}}</button>
        <button class="pestana" data-p="respaldos">{{t['respaldos']}}</button>
        <button class="pestana" data-p="ajustes">{{t['ajustes']}}</button>
    </div>

    <!-- SISTEMAS -->
    <div class="panel activo" id="p-sistemas">
        <h3 style="margin-bottom:15px;color:#93c5fd;">⚙️ {{t['sistemas']}}</h3>
        <div class="grid">
            {% for k, v in nodos.items() %}
            <div class="tarjeta">
                <span class="etiqueta {{'et-on' if v.activo else 'et-off'}}">
                    {{'✅ ' + t['conectado'] if v.activo else '❌ ' + t['desconectado']}}
                </span>
                <h4 style="margin:8px 0 4px;">{{v['nombre']}}</h4>
                <p style="font-size:12px;color:#94a3b8;margin-bottom:12px;">{{v['desc']}}</p>
                <div class="botones">
                    <a href="/encender/{{k}}" class="btn btn-verde">{{t['encender']}}</a>
                    <a href="/apagar/{{k}}" class="btn-rojo btn">{{t['apagar']}}</a>
                    <a href="/reiniciar/{{k}}" class="btn-dorado btn">{{t['reiniciar']}}</a>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>

    <!-- GRANJA -->
    <div class="panel" id="p-granja">
        <h3 style="margin-bottom:15px;color:#93c5fd;">📱 {{t['granja']}}</h3>
        <form action="/ejecutar/nodos" method="post" class="herramienta">
            <span>🟢 {{t['nodos']}}</span>
            <button class="btn btn-azul" type="submit">▶</button>
        </form>
        <form action="/ejecutar/conexiones" method="post" class="herramienta">
            <span>🌐 {{t['conexiones']}}</span>
            <button class="btn btn-azul" type="submit">▶</button>
        </form>
        <form action="/ejecutar/escanear" method="post" class="herramienta">
            <span>🔌 {{t['escanear']}}</span>
            <button class="btn btn-verde" type="submit">▶</button>
        </form>
        <form action="/ejecutar/recursos" method="post" class="herramienta">
            <span>📊 {{t['recursos']}}</span>
            <button class="btn btn-dorado" type="submit">▶</button>
        </form>
        <div class="resultado" id="res-granja">{{datos['salida_herramienta'] or t['resultados']}}</div>
    </div>

    <!-- MONITOREO -->
    <div class="panel" id="p-monitoreo">
        <h3 style="margin-bottom:15px;color:#93c5fd;">📈 {{t['monitoreo']}}</h3>
        <div class="mon-grid">
            <div class="mon-tarjeta"><div>{{t['cpu']}}</div><div class="mon-val" id="m-cpu">{{datos['cpu']}}</div></div>
            <div class="mon-tarjeta"><div>{{t['memoria']}}</div><div class="mon-val" id="m-mem">{{datos['memoria_uso']}}</div></div>
            <div class="mon-tarjeta"><div>{{t['disco']}}</div><div class="mon-val" id="m-disco">{{datos['disco_uso']}}</div></div>
            <div class="mon-tarjeta"><div>{{t['procesos']}}</div><div class="mon-val" id="m-proc">{{datos['procesos']}}</div></div>
            <div class="mon-tarjeta"><div>{{t['estado_red']}}</div><div class="mon-val" id="m-red" style="font-size:16px;">{{datos['red']}}</div></div>
            <div class="mon-tarjeta"><div>{{t['uptime']}}</div><div class="mon-val" id="m-uptime" style="font-size:16px;">{{datos['tiempo_activo']}}</div></div>
        </div>
        <p style="text-align:center;color:#94a3b8;font-size:12px;margin-top:10px;">💡 {{t['filosofia']}}</p>
    </div>

    <!-- HERRAMIENTAS -->
    <div class="panel" id="p-herramientas">
        <h3 style="margin-bottom:15px;color:#93c5fd;">🛠️ {{t['herramientas']}}</h3>
        <form action="/ejecutar/diagnostico" method="post" class="herramienta">
            <span>🔍 {{t['diagnostico']}}</span>
            <button class="btn btn-azul" type="submit">▶</button>
        </form>
        <form action="/ejecutar/limpieza" method="post" class="herramienta">
            <span>🧹 {{t['limpieza']}}</span>
            <button class="btn btn-azul" type="submit">▶</button>
        </form>
        <form action="/ejecutar/red" method="post" class="herramienta">
            <span>🌐 {{t['red']}}</span>
            <button class="btn btn-azul" type="submit">▶</button>
        </form>
        <div class="resultado" id="res-herramientas">{{datos['salida_herramienta'] or t['resultados']}}</div>
    </div>

    <!-- RESPALDOS -->
    <div class="panel" id="p-respaldos">
        <h3 style="margin-bottom:15px;color:#93c5fd;">💾 {{t['respaldos']}}</h3>
        <form action="/ejecutar/respaldar" method="post" class="herramienta">
            <span>📦 {{t['respaldar']}}</span>
            <button class="btn btn-verde" type="submit">▶</button>
        </form>
        <div class="resultado" id="res-respaldos">{{datos['salida_herramienta'] or t['respaldo_info']}}</div>
        <p style="margin-top:20px;color:#94a3b8;font-size:13px;">
            🔄 {{t['restaurar']}}:<br>
            <code style="background:rgba(0,0,0,.3);padding:8px;border-radius:6px;display:inline-block;margin-top:5px;">
                tar -zxf nombre_del_archivo.tar.gz -C ~/
            </code>
        </p>
    </div>

    <!-- AJUSTES -->
    <div class="panel" id="p-ajustes">
        <h3 style="margin-bottom:15px;color:#93c5fd;">⚙️ {{t['ajustes']}}</h3>
        <div class="tarjeta" style="margin-bottom:15px;">
            <h4 style="margin-bottom:10px;">🌐 {{t['idioma']}} / Language / Язык</h4>
            <div style="display:flex;gap:10px;">
                <a href="/lang/es" class="btn btn-azul">🇪🇸 Español</a>
                <a href="/lang/en" class="btn btn-verde">🇬🇧 English</a>
                <a href="/lang/ru" class="btn btn-dorado">🇷🇺 Русский</a>
            </div>
        </div>
        <div class="tarjeta">
            <h4 style="margin-bottom:10px;">ℹ️ Información del Sistema</h4>
            <p style="color:#94a3b8;font-size:13px;line-height:1.8;">
                Versión: {{cfg['nombre_sistema']}} {{cfg['version']}}<br>
                Autor: {{cfg['autor']}}<br>
                Plataforma: Termux / Android · Lectura nativa /proc<br>
                Tecnología: Flask + WebSockets · Actualización cada 2s<br>
                Clave: {{cfg['clave_sistema']}}<br>
                Arquitectura: Modular · Todo en uno · Fácil de actualizar 💙
            </p>
        </div>
    </div>

    <div class="pie">
        ⚡ {{cfg['nombre_sistema']}} {{cfg['version']}} · Dirigido por {{cfg['autor']}} · Hecho con 💙
    </div>
</div>

<script>
const socket = io();
const lang = "{{session.lang or 'es'}}";

socket.on("connect", () => {
    const estado = document.getElementById("estado-socket");
    estado.textContent = "🟢 " + (lang=="es"?"CONECTADO":lang=="ru"?"ПОДКЛЮЧЕНО":"CONNECTED");
    estado.style.background = "rgba(16,185,129,.2)";
    estado.style.color = "#94f9d0";
});
socket.on("disconnect", () => {
    const estado = document.getElementById("estado-socket");
    estado.textContent = "🔴 " + (lang=="es"?"DESCONECTADO":lang=="ru"?"ОТКЛЮЧЕНО":"DISCONNECTED");
    estado.style.background = "rgba(239,68,68,.2)";
    estado.style.color = "#fca5a5";
});

socket.on("actualizar", (msg) => {
    document.getElementById("m-cpu").textContent = msg.datos.cpu;
    document.getElementById("m-mem").textContent = msg.datos.memoria_uso;
    document.getElementById("m-disco").textContent = msg.datos.disco_uso;
    document.getElementById("m-proc").textContent = msg.datos.procesos;
    document.getElementById("m-red").textContent = msg.datos.red;
    document.getElementById("m-uptime").textContent = msg.datos.tiempo_activo;
});

document.querySelectorAll(".pestana").forEach(b => {
    b.addEventListener("click", () => {
        document.querySelectorAll(".pestana").forEach(p => p.classList.remove("activa"));
        document.querySelectorAll(".panel").forEach(p => p.classList.remove("activo"));
        b.classList.add("activa");
        document.getElementById("p-" + b.dataset.p).classList.add("activo");
    });
});
</script>
</body></html>
"""

# ═══════════════════════════════════════════════════════════════════════════
# ARRANQUE DEL SISTEMA
# ═══════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("="*65)
    print(f"  ⚡ {CONFIG['nombre_sistema']} {CONFIG['version']}")
    print(f"  👑 DIRIGIDO POR: {CONFIG['autor']}")
    print(f"  🔐 Clave: {CONFIG['clave_sistema']}")
    print(f"  🌐 Acceso: http://127.0.0.1:{CONFIG['puerto']}")
    print(f"  📦 Modular · Todo en 1 archivo · Fácil de actualizar")
    print("="*65)
    threading.Thread(target=actualizar_datos, daemon=True).start()
    socketio.run(app, host="0.0.0.0", port=CONFIG["puerto"], debug=False, allow_unsafe_werkzeug=True)

