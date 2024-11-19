document.getElementById('BtnEnviarReporte').addEventListener('click', function(event){
    event.preventDefault();
    const BeginDate = document.getElementById('fecha_inicio').value;
    const EndDate = document.getElementById('fecha_fin').value;
    if (!BeginDate || !EndDate) {

        alert("AMBOS CAMPOS DEBEN TENER SELECCIONADA UNA FECHA");
        return;
    }
    const datos ={
        'BeginDate': BeginDate,
        'EndDate': EndDate
    }
    Body = JSON.stringify(datos)
    const csrfToken =  document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch(ReportViewURL,{
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: Body
    })
    .then(response => response.json())
    .then(data =>{
        const tbody = document.getElementById('ReportTBody');
        tbody.innerHTML = ''; 
        
        data.Report_list.forEach(item => {
            const row = document.createElement('tr');
            row.style.cursor = 'pointer';
            for (let key in item) {
                const td = document.createElement('td');
                td.style.color = 'white';
                let value = item[key];
                if(key === 'FECHA_VENTA' && value && value.includes('T')){
                    const date = new Date(value);
                    const options = {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit',
                        hour12: true
                    };
                    value = date.toLocaleString('es-ES',options);
                }
                td.textContent = value;
                row.appendChild(td);
            }

            tbody.appendChild(row);
        });

    })
    .catch(error => console.error('error',error));

})

function GenerarReporte(){
    const { jsPDF } = window.jspdf;  // Usamos el espacio de nombres global jsPDF
    const doc = new jsPDF();

    doc.autoTable({ 
        html: '#ReportTable', 
        startY: 20,  
    });

    
    doc.save("reporte.pdf");
}
