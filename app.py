from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import logging
import time

# 1. CONEXIÓN 
from taximetrov1 import Taximeter

app = Flask(__name__, template_folder='.')

app.secret_key = 'taxigotech_secret_key_123'

# Logs para monitorear eventos importantes y errores en la aplicación
logging.basicConfig(
    filename="taximetro.log", 
    level=logging.INFO,      
    format="%(asctime)s - %(levelname)s - %(message)s", 
    datefmt="%Y-%m-%d %H:%M:%S" 
) 


my_taximeter = Taximeter()

# Variables de control para la Web
web_state = {
    "is_running": False,
    "current_mode": "MOVIMIENTO",
    "start_time": None,
    "total_fare": 0.0
}

def calculate_web_fare():
    """Calcula la tarifa en tiempo real sumando lo acumulado en tramos anteriores 
       más el tiempo transcurrido en el tramo actual."""
    if not web_state["is_running"] or not web_state["start_time"]:
        return web_state["total_fare"]
        
    now = time.time()
    elapsed = now - web_state["start_time"] # Tiempo en segundos del tramo actual
    
    
    rate = my_taximeter.move_price if web_state["current_mode"] == "MOVIMIENTO" else my_taximeter.stop_price
    
    return web_state["total_fare"] + (elapsed * rate)

# --- RUTAS DE COMUNICACIÓN  ---

@app.route('/')
def home():
    """Si el usuario NO está logueado, ve al login. Si sí, ve al taxímetro."""
    if not session.get('logged_in'):
        return render_template('login.html')
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    """Recibe la contraseña del formulario web y verifica si es admin123"""
    password_entered = request.form.get('password')
    
    if password_entered == "admin123":
        session['logged_in'] = True  # Guarda el pase de seguridad
        logging.info("Autenticación exitosa desde la interfaz web.")
        return redirect(url_for('home'))
    else:
        logging.warning("Intento de acceso fallido en la interfaz web.")
        return render_template('login.html', error="Contraseña incorrecta. Inténtalo de nuevo.")

@app.route('/logout')
def logout():
    """Borra la sesión del conductor y vuelve a bloquear la pantalla"""
    session.clear()
    logging.info("El usuario ha cerrado sesión.")
    return redirect(url_for('home'))

@app.route('/api/start', methods=['POST'])
def start_trip():
    if not web_state["is_running"]:
        web_state["is_running"] = True
        web_state["start_time"] = time.time()
        web_state["total_fare"] = 0.0
        web_state["current_mode"] = "MOVIMIENTO"
        logging.info("Web: Viaje iniciado en interfaz gráfica.")
    return jsonify({"status": "running", "fare": web_state["total_fare"]})

@app.route('/api/toggle_pause', methods=['POST'])
def toggle_pause():
    if web_state["is_running"]:
        #  Guardamos en Euros lo acumulado HASTA ESTE SEGUNDO exacto
        web_state["total_fare"] = calculate_web_fare()
        
        # Reiniciamos el reloj para el nuevo tramo (Parado o Movimiento)
        web_state["start_time"] = time.time()
        
        #  Cambiamos de modo alternadamente
        if web_state["current_mode"] == "MOVIMIENTO":
            web_state["current_mode"] = "PARADO"
        else:
            web_state["current_mode"] = "MOVIMIENTO"
            
        logging.info(f"Web: Cambio de estado a: {web_state['current_mode']}")
        return jsonify({"status": "running", "mode": web_state["current_mode"]})
    return jsonify({"status": "stopped"})

@app.route('/api/status', methods=['GET'])
def get_status():
    """Ruta de consulta continua. Fuerza a retornar True enis_running para que el JS no se congele"""
    current_fare = calculate_web_fare()
    return jsonify({
        "fare": round(current_fare, 2),
        "is_running": True,  #True mientras el servidor responda
        "mode": web_state["current_mode"]
    })

@app.route('/api/stop', methods=['POST'])
def stop_trip():
    if web_state["is_running"]:
        final_fare = calculate_web_fare()
        
        
        web_state["is_running"] = False
        web_state["start_time"] = None
        
        
        my_taximeter.save_to_history(final_fare)
        logging.info(f"Web: Viaje terminado satisfactoriamente. Total: {final_fare:.2f}")
        
        return jsonify({"status": "finished", "final_fare": round(final_fare, 2)})
    return jsonify({"status": "not_running"})

@app.route('/api/config_prices', methods=['POST'])
def config_prices():
    try:
        data = request.get_json()
        nuevo_precio_movimiento = float(data.get('move_price'))
        nuevo_precio_parado = float(data.get('stop_price'))
        
        my_taximeter.move_price = nuevo_precio_movimiento
        my_taximeter.stop_price = nuevo_precio_parado
        
        logging.info(f"Configuración: Tarifas actualizadas -> Movimiento: {nuevo_precio_movimiento}€/s, Parado: {nuevo_precio_parado}€/s")
        return jsonify({"status": "success", "move_price": my_taximeter.move_price, "stop_price": my_taximeter.stop_price})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    print("\n🚀 Servidor de TAXIGOTECH activo conectando con tu lógica original.")
    print("👉 Abre tu navegador en: http://127.0.0.1:5000\n")
    app.run(debug=True)