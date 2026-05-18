import flet as ft

def main(page: ft.Page):
    #  Configuración de la ventana 
    page.title = "TAXIGOTECH - Inicio"
    page.window_width = 400
    page.window_height = 300
    page.bgcolor = "#121212" # Tu color negro de fondo
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    #  Elementos visuales (Widgets)
    texto_bienvenida = ft.Text("Bienvenido al Sistema", size=20, color="#8a3ffc")
    
    #  Acción al pulsar el botón
    def saludar(e):
        texto_bienvenida.value = "¡Acceso Iniciado!"
        texto_bienvenida.color = "#00ff88" 
        page.update() 

    btn_entrar = ft.ElevatedButton(
        text="Entrar", 
        on_click=saludar,
        bgcolor="#8a3ffc",
        color="white"
    )

    #  Añadir todo a la página
    page.add(
        texto_bienvenida,
        btn_entrar
    )

#  Ejecutar la aplicación
ft.app(target=main)