let statusInterval = null;

function startStatusUpdate() {
    if (statusInterval) clearInterval(statusInterval);
    
    statusInterval = setInterval(() => {
        fetch('/api/status')
            .then(response => {
                if (!response.ok) throw new Error("Error en servidor.");
                return response.json();
            })
            .then(data => {
               
                const display = document.getElementById('displayFare');
                if (display) {
                    display.innerText = data.fare.toFixed(2) + "€";
                }
            })
            .catch(err => console.error("Error pidiendo datos a Python:", err));
    }, 500); 
}

function contar() {
    console.log("Botón 'Iniciar Viaje' pulsado. Avisando a Python...");
    fetch('/api/start', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            console.log(" Python ha iniciado el viaje.");
            startStatusUpdate(); 
        })
        .catch(err => alert("Error de conexión. ¿Ejecutaste python app.py?"));
}

function pausar() {
    console.log(" Botón 'Pausar' pulsado. Avisando a Python...");
    fetch('/api/toggle_pause', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            console.log(" Python cambió el estado a: " + data.mode);
        })
        .catch(err => console.error("Error al pausar:", err));
}

function resetear() {
    console.log(" Botón 'Finalizar' pulsado. Avisando a Python...");
    fetch('/api/stop', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            clearInterval(statusInterval);
            statusInterval = null;
            
            if (data.status === "finished") {
               // alert("Viaje Terminado\nCobro realizado: " + data.final_fare.toFixed(2) + "€");

            Swal.fire({
                    title: '¡Viaje Finalizado!',
                    text: `El total a cobrar es de ${data.final_fare.toFixed(2)}€`,
                    icon: 'success',
                    confirmButtonText: 'Entendido',
                    confirmButtonColor: '#6f42c1' // Color morado para tus botones
                });
            
            }
            const display = document.getElementById('displayFare');
            if (display) display.innerText = "00.00€";
        })
        .catch(err => console.error("Error al finalizar:", err));
}

// --- FUNCIONES PARA LA PANTALLA DE AJUSTES DE PRECIOS ---

function abrirModalTarifas() {
    
    document.getElementById('modalTarifas').style.display = 'flex';
}

function cerrarModalTarifas() {
   
    document.getElementById('modalTarifas').style.display = 'none';
}

function guardarTarifas() {
   
    const movePrice = document.getElementById('inputMovePrice').value;
    const stopPrice = document.getElementById('inputStopPrice').value;

    
    fetch('/api/config_prices', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ move_price: movePrice, stop_price: stopPrice })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            cerrarModalTarifas(); 
            
           
            Swal.fire({
                title: '¡Tarifas Actualizadas!',
                text: `Nueva configuración activa: Movimiento ${data.move_price}€/s | Parado ${data.stop_price}€/s`,
                icon: 'success',
                confirmButtonColor: '#6f42c1'
            });
        }
    })
    .catch(err => console.error("Error al actualizar tarifas:", err));
}