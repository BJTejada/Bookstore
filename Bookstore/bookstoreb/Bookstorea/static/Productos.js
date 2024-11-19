

document.getElementById('SFormProducto').addEventListener('input', function(event) {
    event.preventDefault(); 

    const searchTerm = document.getElementById('idSearchProd').value.toLowerCase();
    const tableRows = document.querySelectorAll('#TableProduct tbody tr'); 

    tableRows.forEach(row => {
        const rowData = row.textContent.toLowerCase();
        if (rowData.includes(searchTerm)) {
            row.style.display = ''; 
        } else {
            row.style.display = 'none'; 
        }
    });
});


function TransferProduct(button){
    const productSelected = document.getElementById('idProdSEdit');
    const categoriasList = JSON.parse(document.getElementById('categoriasData').textContent);
    const proveedoresList = JSON.parse(document.getElementById('proveedoresData').textContent);
    const row = button.closest('tr');
    const selectCat = document.getElementById('idCategoriaProd');
    const selectProv = document.getElementById('idProveedorProd');
    productSelected.textContent = row.cells[0].textContent; 
    productSelected.value = row.cells[0].textContent;
    const categoriaID = row.cells[1].textContent; 
    const proveedorID = row.cells[2].textContent; 
    const nombreProducto = row.cells[3].textContent; 
    const marcaProducto = row.cells[4].textContent; 
    const btnEdit = document.getElementById('idBtnGuardarProd'); 

    document.getElementById('idNombreProd').value = nombreProducto;
    document.getElementById('idMarcaProd').value = marcaProducto;
    document.getElementById('idNombreProd').textContent = nombreProducto;
    document.getElementById('idMarcaProd').textContent = marcaProducto;

    selectCat.innerHTML = '';
    categoriasList.forEach(categoria => {
        const option = document.createElement('option');
        option.value = categoria.ID_CATEG;
        option.textContent = categoria.NOMBRE_CATEG;
        if(categoria.ID_CATEG == categoriaID){
            option.selected = true;
        }
        selectCat.appendChild(option);
    })

    selectProv.innerHTML = '';
    proveedoresList.forEach(proveedor => {
        const optionP = document.createElement('option');
        optionP.value = proveedor.ID_PROV;
        optionP.textContent = proveedor.NOMBRE_PROV;
        if(proveedor.ID_PROV == proveedorID){
            optionP.selected = true;
        }
        selectProv.appendChild(optionP);
    })
    maquetaEdicion();
}

function CancellEditProduct(){
    const categoriasList = JSON.parse(document.getElementById('categoriasData').textContent);
    const proveedoresList = JSON.parse(document.getElementById('proveedoresData').textContent);
    const btnForm = document.getElementById('idBtnGuardarProd');
    const formP = document.getElementById('idProductForm');
    const btnC = document.getElementById('btnCancellEditProduct');
    const title = document.getElementById('idHeadAction');
    const lblNombre = document.getElementById('lblNombreProd');
    const lblMarca = document.getElementById('lblMarcaProd');
    const lblCat = document.getElementById('lblCategoriaProd');
    const lblProv = document.getElementById('lblProveedorProd');
    const selectCat = document.getElementById('idCategoriaProd');
    const selectProv = document.getElementById('idProveedorProd');
    formP.reset();
    formP.style.backgroundColor ='#1a2d1d';
    formP.style.border ='3px solid #5fef34'
    btnForm.style.backgroundColor ='#6de571';
    btnForm.style.color ='#3e3e3e';
    btnForm.textContent = 'GUARDAR PRODUCTO';
    btnForm.style.border = '3px solid #ffffff';
    btnC.classList.add("ocultar");
    title.textContent = '➕ CREAR NUEVO PRODUCTO';
    lblNombre.style.color = '#ffffff';
    lblMarca.style.color = '#ffffff';
    lblCat.style.color = '#ffffff';
    lblProv.style.color = '#ffffff';
    selectCat.innerHTML = '';
    categoriasList.forEach(categoria => {
        const option = document.createElement('option');
        option.value = categoria.ID_CATEG;
        option.textContent = categoria.NOMBRE_CATEG;
        selectCat.appendChild(option);
    })

    selectProv.innerHTML = '';
    proveedoresList.forEach(proveedor => {
        const optionP = document.createElement('option');
        optionP.value = proveedor.ID_PROV;
        optionP.textContent = proveedor.NOMBRE_PROV;
        selectProv.appendChild(optionP);
    })

    isEditMode = false;
}

function maquetaEdicion(){
    const formP = document.getElementById('idProductForm');
    const headAction = document.getElementById('idHeadAction');
    const btnCancell = document.getElementById('btnCancellEditProduct');
    const btnForm = document.getElementById('idBtnGuardarProd');
    const lblNombre = document.getElementById('lblNombreProd');
    const lblMarca = document.getElementById('lblMarcaProd');
    const lblCat = document.getElementById('lblCategoriaProd');
    const lblProv = document.getElementById('lblProveedorProd');
    headAction.textContent ="✏️ EDITANDO PRODUCTO...";
    formP.style.backgroundColor ='#344ea9b1';
    formP.style.border ='3px solid #a6a0eb'
    btnCancell.classList.remove('ocultar');
    btnCancell.style.border = '2px solid #ffffff';
    btnForm.textContent = 'EDITAR PRODUCTO';
    btnForm.style.backgroundColor = '#1a2d1d';
    btnForm.style.color='#ffffff';
    btnForm.style.border = '2px solid #ffffff';
    lblNombre.style.color = '#ffffff';
    lblMarca.style.color = '#ffffff';
    lblCat.style.color = '#ffffff';
    lblProv.style.color = '#ffffff';
}

document.getElementById('idProductForm').onsubmit = function(event){
    event.preventDefault();
    const idProdEditing = document.getElementById('idProdSEdit').value;
    if(idProdEditing){
        EditProd();
    } else if(!idProdEditing){
        AddProd();
    }
}

function EditProd(){
    const form = document.getElementById('idProductForm');
    const formProduct = new FormData(form);

    fetch(ProductoURL, {
        method: 'POST',
        body: formProduct,
        headers:{
            'X-CSRFToken': '{{ csrf_token }}',
        }
    })
    .then(response => response.json())  
    .then(data => {
        if (data.status === 'success') {
            alert('PRODUCTO MODIFICADO EXITOSAMENTE');
            const clickProd = document.getElementById('idPageProductos');
            if (clickProd) {
                clickProd.click();
            }
        } else {
            alert('Error al actualizar producto');
        }
    })
    .catch(error => console.error('Error:', error));
}

function AddProd(){
    const form = document.getElementById('idProductForm');
    const formProduct = new FormData(form);
    
    fetch(ProductoURL, {
        method: 'POST',
        body: formProduct,
        headers:{
            'X-CSRFToken': '{{ csrf_token }}',
        }
    })
    .then(response => response.json())  
    .then(data => {
        if (data.status === 'success') {
            alert('PRODUCTO AGREGAR EXITOSAMENTE');
            const clickProd = document.getElementById('idPageProductos');
            if (clickProd) {
                clickProd.click();
            }
        } else {
            alert('Error al insertar producto');
        }
    })
    .catch(error => console.error('Error:', error));
}