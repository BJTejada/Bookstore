 //cargar .js para el acceso dianmico al DOM
 //remover scripts antiguos si existen
function removeScript(scriptId) {
  const oldScript = document.getElementById(scriptId);
  if (oldScript) {
      oldScript.parentNode.removeChild(oldScript);
  }
}
 function loadScript(scriptName, scriptId) {
  removeScript(scriptId)
  const script = document.createElement('script');
  script.src = `static/${scriptName}`;
  script.id = scriptId;
  document.head.appendChild(script);
}
//NAVBAR
//script para poder clickear el navbar y que solo una seccion de la pagina 
//se cargue

document.querySelectorAll('.navbar a').forEach(link => {
  link.addEventListener('click', function(event) {
    event.preventDefault();
    // Remover la clase 'active' de todos los enlaces del navbar
    document.querySelectorAll('.navbar a').forEach(link => {
      link.classList.remove('active');
    });
    // Añadir la clase 'active' al enlace clickeado
    this.classList.add('active');
    const section = this.getAttribute('data-section');
    fetch(`/${section}`)
      .then(response => response.text())
      .then(data => {
        document.getElementById('content').innerHTML = data;
              
        if(section === 'Inventario'){
            loadScript('Inventario.js','Inventario-script');
        } 
          else if(section === 'Entradas_View'){
            loadScript('Entradas.js','Entradas-script');
        } 
          else if(section === 'Productos'){
            loadScript('Productos.js','Productos-script');
        } 
          else if(section === 'Reportes_View'){
            loadScript('Reportes.js','Reportes-script');
        }
      })
      .catch(error => console.error('Error al cargar la sección:', error));
  });
});

const clickInv = document.getElementById('idInventario');
if (clickInv) {
  clickInv.click();
}
