document.addEventListener('DOMContentLoaded', function () {
    //Logica detras del chat

    // Define el nombre de la sala
    const SALA_CHAT = 'python';

    // Conecta con WebSockets
    const CHAT_SOCKET = new WebSocket('ws://localhost:8000/ws/chat/' + SALA_CHAT + '/');

    // Captura elementos del DOM
    const CAMPO_NOMBRE = document.querySelector('#nombre');
    const MENSAJES = document.querySelector('#mensajes');
    const CAMPO_TEXTO = document.querySelector('#texto');
    const BOTON_ENVIAR = document.querySelector('#enviar');

    // Función para añadir un mensaje al HTML
    function anyadirNuevoMensajeAlHTML(nombre, texto, propio = false) {
        const contenedor = document.createElement('div');
        contenedor.classList.add(propio ? 'bg-primary' : 'bg-secondary', 'p-2');

        const nombreElem = document.createElement('h2');
        nombreElem.classList.add('text-tiny', 'text-bold', 'mt-2');
        nombreElem.textContent = nombre;
        contenedor.appendChild(nombreElem);

        const textoElem = document.createElement('p');
        textoElem.classList.add('my-2');
        textoElem.textContent = texto;
        contenedor.appendChild(textoElem);

        MENSAJES.appendChild(contenedor);
    }

    // Enviar nuevo mensaje por WebSocket
    function enviarNuevoMensaje() {
        if (!CAMPO_NOMBRE.value.trim() || !CAMPO_TEXTO.value.trim()) return;

        CHAT_SOCKET.send(JSON.stringify({
            name: CAMPO_NOMBRE.value,
            text: CAMPO_TEXTO.value
        }));

        CAMPO_TEXTO.value = '';
        CAMPO_TEXTO.focus();
    }

    // Eventos WebSocket
    CHAT_SOCKET.addEventListener('open', () => {
        console.log('Conectado');
    });

    CHAT_SOCKET.addEventListener('close', () => {
        console.log('Desconectado');
    });

    CHAT_SOCKET.addEventListener('message', (event) => {
        const data = JSON.parse(event.data);
        const esPropio = data.name === CAMPO_NOMBRE.value;
        anyadirNuevoMensajeAlHTML(data.name, data.text, esPropio);
    });

    // Eventos DOM
    BOTON_ENVIAR.addEventListener('click', enviarNuevoMensaje);
    CAMPO_TEXTO.addEventListener('keyup', (e) => {
        if (e.keyCode === 13) enviarNuevoMensaje();
    });
});
