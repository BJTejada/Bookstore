
function UpdateClient(cName){
    const destinationPC = document.getElementById('showClientName')[0];
    destinationPC.textContent = cName;
}
// Verificamos si la variable global window.modalInitialized ya existe. Si no, la creamos y la inicializamos en false.
if (typeof window.modalInitialized === 'undefined') {
    window.modalInitialized = false; // Inicializar la bandera
}
    // Solo inicializa el modal si aún no ha sido inicializado
    if (!window.modalInitialized) {
        const modal = document.getElementById("clientModal");
        const btn = document.getElementById("openModalBtn");
        const span = document.getElementsByClassName("close")[0];
        
        const newClientForm = document.getElementById("newClientForm");

        // Mostrar el modal al hacer clic en el botón
        btn.onclick = function() {
            modal.style.display = "block";
        }
        // Cerrar el modal al hacer clic en la "X"
        span.onclick = function() {
            modal.style.display = "none";
        }
        // Cerrar el modal si se hace clic fuera de él
        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        };
        function transferRowC(row) {
            
            const client = row.cloneNode(true);
            const nameC = client.getElementsByTagName('td')[1].textContent;
            const lNameC = client.getElementsByTagName('td')[2].textContent;
            const Cname = nameC + lNameC;
            const Cid = client.getElementsByTagName('td')[0].textContent;
            // Crea un evento personalizado llamado 'updateshowclient'
            let event = new CustomEvent('updateShowClient', { detail: {Cname: Cname, Cid: Cid} });
            // Despacha el evento en el documento
            document.dispatchEvent(event);
        }
        document.getElementById('newClientForm').onsubmit = function(event){
            event.preventDefault();
            const txtnombre = document.getElementById('newClientName');
            const txtap = document.getElementById('newClientLName');
            const txttel = document.getElementById('newClientPhone');
            const txtdui = document.getElementById('newClientDUI');
            const txtcorreo = document.getElementById('newClientEmail');
            const formClient = new FormData(this);

            fetch(insertClientURL, {
                method: 'POST',
                body: formClient,
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                },
            })
            .then(response => {
                if (response.ok){
                    alert('cliente creado exitosamene');
                    window.location.reload(true);
                    txtnombre.value = "";
                    txtap.value = "";
                    txttel.value = "";
                    txtdui.value = "";
                    txtcorreo.value = "";
                } else {
                    alert('error al crear cliente');
                }
            })
            .catch(error => console.error('Error', error));
        };
        document.getElementById('searchForm').addEventListener('submit', function(event) {
            event.preventDefault(); 
        
            const searchTerm = document.getElementById('clientSearch').value.toLowerCase();
            const tableRows = document.querySelectorAll('#tableClients tbody tr'); 
        
            tableRows.forEach(row => {
                const rowData = row.textContent.toLowerCase();
                if (rowData.includes(searchTerm)) {
                    row.style.display = ''; 
                } else {
                    row.style.display = 'none'; 
                }
            });
        });
        
        window.modalInitialized = true;
    } else {
        const modal = document.getElementById("clientModal");
        const btn = document.getElementById("openModalBtn");
        const span = document.getElementsByClassName("close")[0];
        const createClientBtn = document.getElementById("createClientBtn");
        const newClientForm = document.getElementById("newClientForm");
        // Mostrar el modal al hacer clic en el botón
        btn.onclick = function() {
            modal.style.display = "block";
        }
        // Cerrar el modal al hacer clic en la "X"
        span.onclick = function() {
            modal.style.display = "none";
        }
        // Cerrar el modal si se hace clic fuera de él
        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        };
        //
        function transferRowC(row) {
            const client = row.cloneNode(true);
            const nameC = client.getElementsByTagName('td')[1].textContent;
            const lNameC = client.getElementsByTagName('td')[2].textContent;
            const Cname = nameC + lNameC;
            const Cid = client.getElementsByTagName('td')[0].textContent;
            // Crea un evento personalizado llamado 'updateDetalle'
            let event = new CustomEvent('updateShowClient', { detail: {Cname: Cname, Cid: Cid} });
            // Despacha el evento en el documento
            document.dispatchEvent(event);
        }
        document.getElementById('newClientForm').onsubmit = function(event){
            event.preventDefault();
            const txtnombre = document.getElementById('newClientName');
            const txtap = document.getElementById('newClientLName');
            const txttel = document.getElementById('newClientPhone');
            const txtdui = document.getElementById('newClientDUI');
            const txtcorreo = document.getElementById('newClientEmail');
            const formClient = new FormData(this);

            fetch(insertClientURL, {
                method: 'POST',
                body: formClient,
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                },
            })
            .then(Response => {
                if (Response.ok){
                    alert('cliente creado exitosamete');
                    window.location.reload(true);
                    txtnombre.value = "";
                    txtap.value = "";
                    txttel.value = "";
                    txtdui.value = "";
                    txtcorreo.value = "";
                } else {
                    alert('error al crear cliente');
                }
            })
            .catch(error => console.error('Error', error));
        };

        // Marcamos que ya fue inicializado
        window.modalInitialized = true;
    }
//busqueda de productos
document.getElementById('SFormProd').addEventListener('input', function(event) {
    event.preventDefault(); // Evita que la página se recargue

    const searchTerm = document.getElementById('prodSearch').value.toLowerCase();
    const tableRows = document.querySelectorAll('#SourceTable tbody tr'); // Asegúrate de que el selector sea correcto

    tableRows.forEach(row => {
        const rowData = row.textContent.toLowerCase();
        if (rowData.includes(searchTerm)) {
            row.style.display = ''; // Muestra la fila si contiene el término de búsqueda
        } else {
            row.style.display = 'none'; // Oculta la fila si no contiene el término de búsqueda
        }
    });
});

function transferRow(row) {
        const destinationTable = document.getElementById('SaleTable').getElementsByTagName('tbody')[0];
        const newRow = row.cloneNode(true);

        const productId = newRow.getElementsByTagName('td')[0].innerText;

        const rowExists = Array.from(destinationTable.getElementsByTagName('tr')).some(r => {
            const existingProductId = r.getElementsByTagName('td')[0].innerText;
            return existingProductId === productId;
        });
        if(!rowExists){
            newRow.classList.remove('ocultar');
            newRow.removeAttribute('onclick');
            const cell = newRow.getElementsByTagName('td');
            const value = String(cell[4].textContent).trim();
            const valuecant = String(cell[5].textContent).trim();
            cell[4].setAttribute('value',value);
            cell[4].setAttribute('class','precio');
        
            cell[5].setAttribute('value',valuecant);
            cell[5].setAttribute('contenteditable','true');
            cell[5].setAttribute('class','cantidad');
            destinationTable.appendChild(newRow);
            document.querySelectorAll('.cantidad').forEach(cantidad => {
            cantidad.addEventListener('input', UpdateTotal); // O 'change' si prefieres
            });
            UpdateTotal();
        }else{
            alert('El producto ya ha sido agregado');
        }
}

function UpdateTotal(){
    let total =0;
    const cantidades = document.querySelectorAll('.cantidad');
    const precios = document.querySelectorAll('.precio');

    cantidades.forEach((input, index)=> {
            const cantidad = parseInt(input.textContent) || 0;
            const precio = parseFloat(precios[index].textContent)
            total += cantidad * precio;
    });
    document.getElementById('TotalVenta').textContent = "Total $" + total.toFixed(2);
    document.getElementById('idventatotal').textContent = total.toFixed(2);
    document.getElementById('idventatotal').setAttribute('value',total.toFixed(2));
}
// Escucha el evento 'updateShowClient'
document.addEventListener('updateShowClient', function(event) {
    const flag = document.getElementById('idClienteSeleccionado');
    let detalleP = document.getElementById('showClientName');
    let detalleIdC = document.getElementById('selectClientId');
    detalleP.textContent = "Cliente: "+event.detail.Cname;  
    detalleIdC.textContent = event.detail.Cid.trim();
    flag.textContent= "Cliente "+ event.detail.Cname + 'Seleccionado';
});

function ValidarDui(input) {
    // Solo permite números removiendo letras u otros caracteres no numéricos
    let valor = input.value.replace(/[^0-9]/g, '');
  
    // Agrega el guion en la posición 9 si hay al menos 9 caracteres
    if (valor.length > 8) {
      valor = valor.slice(0, 8) + '-' + valor.slice(8);
    }
  
    // Asigna el valor actualizado al campo de entrada
    input.value = valor;
  }

  function ValidarTelefono(input) {
    // Solo permite números removiendo letras u otros caracteres no numéricos
    let valor = input.value.replace(/[^0-9]/g, '');  
    // Asigna el valor actualizado al campo de entrada
    input.value = valor;
  }

function insertVenta(){
    /*VENTA*/
    const totalV = document.getElementById('idventatotal').textContent;
    const idClienteV = document.getElementById('selectClientId').textContent;
    const idUserV = document.getElementById('idUser').textContent;
    const lVenta = {
        total: totalV,
        idCliente: idClienteV,
        idUser: idUserV
    };
    // Convierte los datos a formato JSON
    const body = JSON.stringify(lVenta);
    const csrfToken =  document.querySelector('[name=csrfmiddlewaretoken]').value;
    // Envía los datos a la vista de Django
    return fetch(insertVentaURL, {
        method: 'POST',
        body: body,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,  
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            
            return data;
        } else {
            alert('Error al enviar datos de venta');
        }
    });
}

function insertDetVenta(){
    /*DETALLE DE VENTA*/
    const table = document.getElementById('SaleTable');
    const rows = table.querySelectorAll('tbody tr');
    let DetVentaData = [];    
    rows.forEach(row => {
        const idprod = row.cells[0].textContent;
        const idlote = row.cells[1].textContent;
        const nombreProd = row.cells[2].textContent;
        const marcaProd = row.cells[3].textContent;
        const precioProd = row.cells[4].textContent;
        const cantidadPro = row.cells[5].textContent;
        const subtotal = parseFloat(precioProd) * parseInt(cantidadPro);
        DetVentaData.push({precioProd,cantidadPro,subtotal,idprod,idlote});
    });
    // Convierte los datos a formato JSON
    const body = JSON.stringify(DetVentaData);
    const csrfToken =  document.querySelector('[name=csrfmiddlewaretoken]').value;
    // Envía los datos a la vista de Django
    return fetch(insertDetVentaURL, {
        method: 'POST',
        body: body,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,  
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Venta realizada');
            const clickInve = document.getElementById('idInventario');
            if (clickInve) {
                clickInve.click();
            }
            FacturaVenta();
        } else {
            console.error('Error en el servidor:', data.error || data.message);
            // Muestra el mensaje de error en el frontend
            alert('Error: ' + (data.error || data.message));
            
        }
    });
}

function ProcesarVenta(){
    const table = document.getElementById('SaleTable');
    const idClienteV = document.getElementById('selectClientId').textContent;
    // Verificar si el cliente está seleccionado
    if (!idClienteV) {
        alert('Por favor, selecciona un cliente antes de procesar la venta.');
        return;
    }

    // Verificar si hay productos en la tabla de productos seleccionados
    if (table.rows.length <= 1) { // Asume que la primera fila es el encabezado
        alert('Por favor, selecciona al menos un producto para procesar la venta.');
        return; 
    }
    insertVenta()
        .then(() => insertDetVenta())
        .catch(error => console.error(error));
}

function FacturaVenta(){
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        // Aquí, puedes hacer la solicitud GET para generar la factura
        fetch(GenerarFacturaURL, {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrfToken
            },
        })
        .then(response => response.blob())  // Asumimos que la factura es un PDF
        .then(blob => {
            // Crear un enlace para descargar el archivo PDF
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'factura.pdf';  // Nombre del archivo de la factura
            link.click();
        })
        .catch(error => {
            console.error('Error al generar la factura:', error);
            alert('Hubo un error al generar la factura.');
        });
    
}