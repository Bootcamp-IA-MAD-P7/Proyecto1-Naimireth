import time 
import logging

# Logs del programa 
logging.basicConfig(
    filename="taximetro.log", # El nombre del archivo donde se guardarán los logs
    level=logging.INFO,       # Nivel Info para registrar eventos importantes
    format="%(asctime)s - %(levelname)s - %(message)s", # Formato del mensaje de log
    datefmt="%Y-%m-%d %H:%M:%S" # Formato de fecha y hora en los logs
) 

# Función para calcular la tarifa total del viaje
def calculate_fare(stopped_seconds, moving_seconds):
    stop_price = 0.02
    move_price = 0.05
    fare = (stopped_seconds * stop_price) + (moving_seconds * move_price)
    return fare

# Función para guardar el total del viaje en un archivo de historial
def save_to_history(total):
    with open("historial_viajes.txt", "a") as file:
        file.write(f"Viaje finalizado - Total: {total:.2f} euros\n")
        logging.info(f"Historial actualizado con un total de {total:.2f}€")


def taximeter():
    print("--- Bienvenido al Taxímetro ---")
    logging.info("El programa Taxímetro se ha iniciado.")

    stop_price = 0.02  # valor float para el precio por segundo parado
    move_price = 0.05  # valor float para el precio por segundo en movimiento

    print("Que desea hacer?")
    print("1. Iniciar viaje")            
    print("2. Salir")

    while True:
        option = input("Ingrese el número de la opción deseada: 1/2: ").lower()
           
        if option == "1":
            print("Viaje iniciado.... El taxímetro está en marcha.")
            logging.info("Usuario seleccionó Iniciar Viaje.")

            stopped_seconds = 0
            moving_seconds = 0
    
            while True:
                action = input("\n¿Seleccione una de las opciones? P=Parado, M=Movimiento, T=Terminar: ").lower() 
            
                if action == "p" or action == "m": 
                    status_type = "PARADO" if action == "p" else "MOVIMIENTO"
                    print(f"🚕 El taxi está ahora en modo: {status_type}")
                    logging.info(f"Cambio de estado a: {status_type}")
                    
                    start_time = time.time() 
                    
                    input(f"Presiona ENTER cuando el tramo de {status_type} termine...") 
                    
                    end_time = time.time()    
                    
                    duration = end_time - start_time 
                    
                    if action == "p":
                        stopped_seconds += duration
                    else:
                        moving_seconds += duration
                        
                    print(f"✅ Se han registrado {duration:.2f} segundos automáticamente.")  
                
                elif action == "t":
                    print("Viaje terminado. El taxímetro se detiene. Calculando tarifa total...")
                    
                    total_fare = calculate_fare(stopped_seconds, moving_seconds)
                    print(f"Tarifa total: {total_fare:.2f} euros")
                    print("Gracias por usar el taxímetro. ¡Hasta luego!")
              
                    logging.info(f"Viaje terminado satisfactoriamente. Total: {total_fare:.2f}")

                    save_to_history(total_fare) 
                    
                    print("✅ Registro guardado en el historial.")
                    break
                
                else:
                    logging.warning(f"Intento de acción no válida: {action}")
                    print("Opción no válida. Por favor, ingrese 'P', 'M' o 'T'.")
            
        elif option == "2":
            print("Gracias por usar el taxímetro. ¡Hasta luego!")
            break
            
        else:
            print("Opción no válida. Por favor, ingrese un número del 1 al 2.")

# Llamamos a la función
taximeter()