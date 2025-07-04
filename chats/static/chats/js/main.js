document.addEventListener('DOMContentLoaded', function () {
    // Elementos del DOM
    const mensajesContainer = document.getElementById('mensajes-container');
    const seccionEnviar = document.getElementById('seccion-enviar');
    const campoTexto = document.getElementById('texto');
    const botonEnviar = document.getElementById('enviar');
    const nombreContacto = document.getElementById('nombre-contacto');

    // Variables globales
    let chatSocket = null;
    let usuarioSeleccionadoId = null;
    let usuarioSeleccionadoUsername = null;

    // Función para conectar al WebSocket
    function conectarWebSocket() {
        if (!usuarioSeleccionadoId) return;

        // Cerrar conexión existente si hay una
        if (chatSocket) {
            chatSocket.close();
        }

        // Construir la URL del WebSocket
        const socketUrl = `ws://${window.location.host}/ws/private-chat/${usuarioSeleccionadoId}/`;

        // Crear nueva conexión WebSocket
        chatSocket = new WebSocket(socketUrl);

        // Eventos del WebSocket
        chatSocket.onopen = function () {
            console.log('Conexión WebSocket establecida');
        };

        chatSocket.onclose = function () {
            console.log('Conexión WebSocket cerrada');
        };

        chatSocket.onerror = function (error) {
            console.error('Error en WebSocket:', error);
        };

        chatSocket.onmessage = function (event) {
            const data = JSON.parse(event.data);
            agregarMensajeAlHTML(data);
        };
    }

    // Función para agregar un mensaje al HTML
    function agregarMensajeAlHTML(data) {
        const esPropio = data.sender_id == USUARIO_ACTUAL_ID;
        const nombre = esPropio ? 'Tú' : usuarioSeleccionadoUsername;

        const mensajeHTML = `
            <div class="${esPropio ? 'text-right ml-12' : 'mr-12'} mb-3">
                <div class="${esPropio ? 'bg-blue-500 text-white' : 'bg-gray-200'} rounded-lg p-3 inline-block">
                    <p>${data.message}</p>
                    <span class="text-xs opacity-70 block mt-1">
                        ${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                </div>
            </div>
        `;

        mensajesContainer.innerHTML += mensajeHTML;

        // Scroll al final
        mensajesContainer.scrollTop = mensajesContainer.scrollHeight;
    }

    // Función para cargar mensajes de una conversación
    function cargarMensajes(userId) {
        fetch(`/chats/obtener-mensajes/${userId}/`)
            .then(response => response.text())
            .then(html => {
                mensajesContainer.innerHTML = html;
                // Scroll al final
                mensajesContainer.scrollTop = mensajesContainer.scrollHeight;
            })
            .catch(error => console.error('Error al cargar mensajes:', error));
    }

    // CORRECCIÓN PRINCIPAL: Manejar correctamente el evento
    function seleccionarContacto(event) {
        // Usar event.target.closest para encontrar el botón padre
        const boton = event.target.closest('.contacto-btn');
        if (!boton) return;

        const userId = boton.dataset.userId;
        const username = boton.dataset.username;

        // Guardar el usuario seleccionado
        usuarioSeleccionadoId = userId;
        usuarioSeleccionadoUsername = username;

        // Actualizar la cabecera
        nombreContacto.textContent = username;

        // Mostrar la sección de enviar mensajes
        seccionEnviar.classList.remove('hidden');

        // Cargar mensajes existentes
        cargarMensajes(userId);

        // Conectar al WebSocket
        conectarWebSocket();
    }

    // Función para enviar un mensaje
    function enviarMensaje() {
        const mensaje = campoTexto.value.trim();
        if (!mensaje) return;

        // Enviar a través del WebSocket
        if (chatSocket && chatSocket.readyState === WebSocket.OPEN) {
            chatSocket.send(JSON.stringify({
                'message': mensaje
            }));
        }

        // Limpiar el campo
        campoTexto.value = '';
    }

    // Event listeners
    document.addEventListener('click', function (event) {
        // Verificar si se hizo clic en un contacto o en sus hijos
        if (event.target.closest('.contacto-btn')) {
            seleccionarContacto(event);
        }
    });

    botonEnviar.addEventListener('click', enviarMensaje);
    campoTexto.addEventListener('keyup', function (e) {
        if (e.key === 'Enter') {
            enviarMensaje();
        }
    });
});