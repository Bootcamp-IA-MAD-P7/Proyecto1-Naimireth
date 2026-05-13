import time 
import logging

# Logs del programa 
logging.basicConfig(
    filename="taximetro.log", # El nombre del archivo donde se guardarán los logs
    level=logging.INFO,       # Nivel Info para registrar eventos importantes
    format="%(asctime)s - %(levelname)s - %(message)s", # Formato del mensaje de log
    datefmt="%Y-%m-%d %H:%M:%S" # Formato de fecha y hora en los logs
) 

def authenticate():
    password_correct = "admin123" 
    attempts = 3  # Número de oportunidades
    
    print("\n🔒 SEGURIDAD: Acceso restringido.")
    
    while attempts > 0:
        entry = input(f"Ingrese la contraseña de conductor (Intentos restantes: {attempts}): ")
        
        if entry == password_correct:
            print("✅ Acceso concedido. Cargando sistema...")
            logging.info("Autenticación exitosa.")
            return True
        else:
            attempts -= 1
            print("❌ Contraseña incorrecta.")
            logging.warning(f"Intento de acceso fallido. Intentos restantes: {attempts}")
            
    print("🚫 Acceso bloqueado. Demasiados intentos fallidos.")
    return False

class Taximeter:
    def __init__(self):
        # Atributos iniciales (Lo que el taxímetro "sabe")
        self.stop_price = 0.02
        self.move_price = 0.05
        self.stopped_seconds = 0
        self.moving_seconds = 0

    def set_prices(self):
       
        print("\n-\n--- Ajustes: Modificar Tarifas ---")
        try:
            self.stop_price = float(input("Ingrese el nuevo precio por segundo PARADO: "))
            self.move_price = float(input("Ingrese el nuevo precio por segundo en MOVIMIENTO:"))
            logging.info(f"Tarifas actualizadas: Parado={self.stop_price}, Movimiento={self.move_price}")
            print("✅ Tarifas actualizadas correctamente.")
        except ValueError:
            print("❌ Entrada inválida. Manteniendo tarifas anteriores.")

    def calculate_fare(self):
        # Calcula la tarifa usando los segundos guardados en el objeto
        fare = (self.stopped_seconds * self.stop_price) + (self.moving_seconds * self.move_price)
        return fare

    def save_to_history(self, total):
        with open("historial_viajes.txt", "a") as file:
            file.write(f"Viaje finalizado - Total: {total:.2f} euros\n")
            logging.info(f"Historial actualizado con un total de {total:.2f}€")

    def start_trip(self):
        print(f"Viaje iniciado.... Rates: Stop={self.stop_price} | Move={self.move_price}")
        logging.info("Usuario seleccionó Iniciar Viaje.")
        
        # Reiniciamos contadores para el nuevo viaje
        self.stopped_seconds = 0
        self.moving_seconds = 0

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
                    self.stopped_seconds += duration
                else:
                    self.moving_seconds += duration
                    
                print(f"✅ Se han registrado {duration:.2f} segundos automáticamente.")  
            
            elif action == "t":
                print("Viaje terminado. Calculando tarifa total...")
                total_fare = self.calculate_fare()
                print(f"Tarifa total: {total_fare:.2f} euros")
                
                logging.info(f"Viaje terminado satisfactoriamente. Total: {total_fare:.2f}")
                self.save_to_history(total_fare) 
                print("✅ Registro guardado en el historial.")
                break
            else:
                logging.warning(f"Intento de acción no válida: {action}")
                print("Opción no válida. Por favor, ingrese 'P', 'M' o 'T'.")

# --- Lógica de ejecución ---

def main():

    if not authenticate():
        return
    # Creamos la instancia del objeto
    my_taximeter = Taximeter()
    
    print("--- Bienvenido al Taxímetro ---")
    logging.info("El programa Taxímetro se ha iniciado.")

    while True:
        print("\nQue desea hacer?")
        print("1. Iniciar viaje")
        print("2. Configurar precios")
        print("3. Salir")
        
        option = input("Ingrese el número de la opción deseada: 1/2/3: ")

        if option == "1":
            my_taximeter.start_trip()
        elif option == "2":
            my_taximeter.set_prices()
        elif option == "3":
            print("Gracias por usar el taxímetro. ¡Hasta luego!")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()

    