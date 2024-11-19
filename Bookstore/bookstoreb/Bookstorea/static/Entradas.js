//AREA PARA TRANSFERIR PRODUCTOS A LA TABLA DE COMPRA
function TransferProd(row){
    const BuyTable = document.getElementById('BuyTable').getElementsByTagName('tbody')[0];
    const newRow = row.cloneNode(true); 
    

    const productId = newRow.getElementsByTagName('td')[0].innerText;

    const rowExists = Array.from(BuyTable.getElementsByTagName('tr')).some(r => {
        const existingProductId = r.getElementsByTagName('td')[0].innerText;
        return existingProductId === productId;
    });

    if(!rowExists){
        const cell = newRow.getElementsByTagName('td');
        newRow.removeAttribute('onclick');

        const precioCompraCell = document.createElement('td');
        precioCompraCell.contentEditable=true;
        precioCompraCell.setAttribute('class','precioCompra');
        precioCompraCell.setAttribute('style','color: white;');
        newRow.appendChild(precioCompraCell);
    
        const precioVentaCell = document.createElement('td');
        precioVentaCell.contentEditable=true;
        precioVentaCell.setAttribute('class','precioVenta');
        precioVentaCell.setAttribute('style','color: white;');
        newRow.appendChild(precioVentaCell);
    
        const cantidadCell = document.createElement('td');
        cantidadCell.contentEditable=true;
        cantidadCell.setAttribute('class','cantidadP');
        cantidadCell.setAttribute('style','color: white;');
        newRow.appendChild(cantidadCell);
        cell[0].setAttribute('class','ocultar');
        BuyTable.appendChild(newRow);
        //MODIFICA EL TOTAL EN precioCompra
        document.querySelectorAll('.precioCompra').forEach(precioC => {
            precioC.addEventListener('input',UpdateTotalC); 
        });
        //MODIFICA EL TOTAL EN cantidadP
        document.querySelectorAll('.cantidadP').forEach(cantidad => {
            cantidad.addEventListener('input',UpdateTotalC); 
        });
    }else{
        alert('producto ya agregado');
    }
}
//busqueda de productos
document.getElementById('SFormProductoC').addEventListener('input', function(event) {
    event.preventDefault(); 

    const searchTerm = document.getElementById('prodSearchC').value.toLowerCase();
    const tableRows = document.querySelectorAll('#SourceTableC tbody tr'); 

    tableRows.forEach(row => {
        const rowData = row.textContent.toLowerCase();
        if (rowData.includes(searchTerm)) {
            row.style.display = ''; // Muestra la fila si contiene el término de búsqueda
        } else {
            row.style.display = 'none'; // Oculta la fila si no contiene el término de búsqueda
        }
    });
});

function UpdateTotalC(){
    let totalC = 0;
    const cantidadP = document.querySelectorAll('.cantidadP');
    const precioC = document.querySelectorAll('.precioCompra');

    cantidadP.forEach((input, index)=> {
        const cC = parseInt(input.textContent) || 0;
        const pC = parseFloat(precioC[index].textContent);
        totalC += cC * pC;
    })
    document.getElementById('TotalCompra').textContent = "Total $" + totalC.toFixed(2);
    document.getElementById('idCompraTotal').textContent = totalC.toFixed(2);
    document.getElementById('idCompraTotal').setAttribute('value',totalC.toFixed(2));
}

function InsertCompra(){
    const tt = document.getElementById('idCompraTotal').textContent;
    const idUser = document.getElementById('idUserC').textContent
    const lCompra = {
        ttC: tt,
        idUserC: idUser
    }
    const bodyC = JSON.stringify(lCompra);
    const csrfTokenC = document.querySelector('[name=csrfmiddlewaretoken]').value;

    return fetch(insertCompraURL, {
        method: 'POST',
        body: bodyC,
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfTokenC,
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

function InsertDetCompra(){
    const tableDC = document.getElementById('BuyTable');
    const rowsDC = tableDC.querySelectorAll('tbody tr');
    let DetCompraData = [];
    rowsDC.forEach(row =>{
        const precioUDC = row.cells[4].textContent;
        const cantidadDC = row.cells[6].textContent;
        const subtotalDC = parseInt(cantidadDC) * parseFloat(precioUDC);
        const idProdDC = row.cells[0].textContent;
        const precioVentaDC = row.cells[5].textContent;
        DetCompraData.push({precioUDC,cantidadDC,subtotalDC,idProdDC,precioVentaDC});
    });

    const bodyDC = JSON.stringify(DetCompraData);
    const csrfTokenDC = document.querySelector('[name=csrfmiddlewaretoken]').value;

    return fetch(insertDetCompraURL,{
        method: 'POST',
        body: bodyDC,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfTokenDC,
        }, 
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Compra realizada');
            const clickEntries = document.getElementById('idPageEntradas');
            if (clickEntries) {
                clickEntries.click();
            }
        } else {
            alert('DETALLE DE COMPRA NO REALIZADA' + data.error);
            
        }
    });
}

function ProcesarCompra(){
    const edDC = document.querySelectorAll('#BuyTable .editable');
    let corruptCell = false;
    edDC.forEach(cellDC => {
        const vDC = cellDC.textContent.trim();
        if (vDC === '' || isNaN(vDC)){
            corruptCell = true;
            cellDC.style.borderColor ='red';
        } else {
            cellDC.style.borderColor = '';
        }
    });
    if(corruptCell){
        alert('Complete todos los campos de la tabla de compras');
        return;
    }
    InsertCompra()
        .then(() => InsertDetCompra())
        .catch(error => console.error(error));
}