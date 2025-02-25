// Referencias comunes
const body = document.querySelector("body");

// Variables
let tamanio = 0.50;  
let cantidadContraste = 100;  

// Crear contenedor de botones
let contenedor = document.createElement("div");
contenedor.classList.add("jvampliador");

// Función para crear botones con eventos
function crearBoton(texto, titulo, accion) {
    let boton = document.createElement("button");
    boton.textContent = texto;
    boton.title = titulo; // Tooltip
    boton.onclick = accion;
    contenedor.appendChild(boton);
}
// Función para actualizar el tamaño de la fuente
function actualizarTamanio() {
    body.style.fontSize = `${tamanio}cm`;
    actualizarEstado();
}
// Etiqueta para mostrar valores
let estado = document.createElement("div");
estado.classList.add("estado");
actualizarEstado();

// Aumentar fuente en pasos de 0.10 cm
crearBoton("+", "Aumentar tamaño", function() {
    tamanio = parseFloat(tamanio) + 0.10; // Convertimos a número y sumamos
    if (tamanio > 2.0) tamanio = 2.0; // Límite superior en 2.0 cm
    actualizarTamanio();
});

// Disminuir fuente en pasos de 0.10 cm
crearBoton("-", "Disminuir tamaño", function() {
    tamanio = parseFloat(tamanio) - 0.10; // Convertimos a número y restamos
    if (tamanio < 0.10) tamanio = 0.10; // Límite inferior en 0.10 cm
    actualizarTamanio();
});



// Alternar contraste entre 100%, 80% y 120%
crearBoton("C", "Ajustar contraste", function() {
    cantidadContraste += 10;
    if (cantidadContraste > 100) {
        cantidadContraste = 10; // Reinicia a 10% después de 100%
    }
    body.style.filter = `contrast(${cantidadContraste}%)`;
    actualizarEstado();
});


// Invertir colores con toggle
crearBoton("I", "Invertir colores", function() {
    let filtroActual = body.style.filter;

    if (filtroActual.includes("invert(1)")) {
        body.style.filter = filtroActual.replace("invert(1)", "").trim();
    } else {
        body.style.filter += " invert(1)";
    }
});




// Agregar contenedor y estado al body
contenedor.appendChild(estado);
body.appendChild(contenedor);

// Función para actualizar el estado en pantalla
function actualizarEstado() {
    estado.textContent = `Tamaño: ${tamanio.toFixed(2)}cm | Contraste: ${cantidadContraste}%`;
}
