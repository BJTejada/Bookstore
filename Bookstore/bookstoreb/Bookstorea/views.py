import datetime
import random
import string
import requests
import json
from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import JsonResponse
# Create your views here.
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404,render, redirect
from .models import VENTAS,DETALLEVENTAS,CLIENTES

from django.http import HttpResponse
#def LogIn_View(request):
 #   return render(request, 'Bookstorea/LogIn.html')
#@login_required
def ClientsList():
    with connection.cursor() as cursor_clientes:
        cursor_clientes.execute("select * from bookstorea_clientes")
        rows_clients = cursor_clientes.fetchall()
        columns_clients = [col[0] for col in cursor_clientes.description]
        cl = [
            dict(zip(columns_clients,reg))
            for reg in rows_clients
        ]
    return cl
    

def Index_View(request):
    return render(request, 'Bookstorea/Index.html')

def Inventario_View(request):

    with connection.cursor() as cursor_inventario:
        cursor_inventario.execute("""select p.id_prod,LT.ID_LOTE,p.nombre_prod,p.marca_prod,lt.precio_venta,lt.cantidad from 
            bookstorea_lotes lt 
        join bookstorea_detallecompra dvc 
        on lt.detalle_compra_id=dvc.id_det_compra
        join bookstorea_producto p
        on dvc.producto_id=p.id_prod
        where lt.cantidad >= 1 order by p.nombre_prod;""")
        rows = cursor_inventario.fetchall()
        columns = [col[0] for col in cursor_inventario.description]
    # Transformar los resultados en una lista de diccionarios (opcional)
    inventario_list = [
        dict(zip(columns, row))
        for row in rows
    ]

    clientes_list = ClientsList()        
    context = {
        'inventario_list': inventario_list,
        'clientes_list': clientes_list,
    }
    return render(request, 'Bookstorea/Inventario.html',context)

def InsertClient_View(request):
    if request.method == 'POST':
            clientes_list = ClientsList()            
            names = request.POST.get('newClientName')
            lNames = request.POST.get('newClientLName')
            phone = request.POST.get('newClientPhone')
            dui = request.POST.get('newClientDUI')
            email = request.POST.get('newClientEmail')

            with connection.cursor() as cursor:
                cursor.callproc('INSERT_CLIENT',[names,lNames,phone,dui,email])

            return JsonResponse({"status": "success","clientes_list":clientes_list})
    return JsonResponse({"status": "error", "message": "metodo no permitido"})

def InsertVenta_View(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            total = float(data.get('total'))
            idCliente = int(data.get('idCliente'))
            idUser = int(data.get('idUser'))
            fecha_actual = datetime.datetime.now()
            numero_factura = generar_numero_factura()
        #(NUM_FACTURA_VENTA,FECHA_VENTA,TOTAL,CLIENTE_ID,EMPLEADO_ID)
            with connection.cursor() as cursorVenta:
                cursorVenta.callproc('INSERTVENTA',[numero_factura,fecha_actual,total,idCliente,idUser])
            return JsonResponse({"status": "success"})
        except ValueError as e:
            return JsonResponse({"status": "error", "message": "Error de conversión: " + str(e)})
        except Exception as e:
            return JsonResponse({"status": "error", "message": "Error inesperado: " + str(e)})
        

def InsertDetVenta_View(request):
    if request.method == 'POST':
        datos_json = json.loads(request.body)

        try:
            with connection.cursor() as cursorDetVenta:

                for registro in datos_json:
                    precioU = float(registro.get('precioProd'))
                    cantidadProd = int(registro.get('cantidadPro'))
                    subtotal = float(registro.get('subtotal'))
                    idprod = int(registro.get('idprod'))
                    idlote = int(registro.get('idlote'))

                    cursorDetVenta.callproc('DETXLOTE', [precioU, cantidadProd, subtotal, idprod, idlote])

            return JsonResponse({'status': 'success'})

        except Exception as e:

            return JsonResponse({'status': 'error', 'error': str(e)})

    else:
        return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)


def Entradas_View(request):
    
    with connection.cursor() as cursor_productos:
        cursor_productos.execute("""select pd.id_prod, pd.nombre_prod, pr.nombre_prov, pd.marca_prod
                            from bookstorea_producto pd 
                            join bookstorea_proveedores pr 
                            on pd.proveedor_id=pr.id_prov 
                            order by pd.nombre_prod asc;""")
                
        rows = cursor_productos.fetchall()
        columns = [col[0] for col in cursor_productos.description]
    
    Productos_list = [
        dict(zip(columns, row))
        for row in rows
    ]
    contexto ={
        'Productos_list': Productos_list
    }
    return render(request, 'Bookstorea/Entradas.html',contexto)

def Productos_View(request):
    with connection.cursor() as cursor:
        cursor.execute("""select p.id_prod,p.categoria_id,p.proveedor_id,p.nombre_prod,p.marca_prod,pr.nombre_prov,ct.nombre_categ
                            from bookstorea_producto p 
                                join bookstorea_proveedores pr on p.proveedor_id = pr.id_prov
                                join bookstorea_categorias ct on p.categoria_id = ct.id_categ;""")
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]

    productos_list = [
        dict(zip(columns, row))
        for row in rows
    ]
    with connection.cursor() as cursorCat:
        cursorCat.execute("""select * from bookstorea_categorias;""")
        rows = cursorCat.fetchall()
        columns = [col[0] for col in cursorCat.description]
    categorias_list =[
        dict(zip(columns, row))
        for row in rows
    ]
    with connection.cursor() as cursorProv:
        cursorProv.execute("""select * from bookstorea_proveedores;""")
        rows = cursorProv.fetchall()
        columns = [col[0] for col in cursorProv.description]
    proveedores_list =[
        dict(zip(columns, row))
        for row in rows
    ]
    contexto = {
        'productos_list': productos_list,
        'categorias_list': categorias_list,
        'proveedores_list': proveedores_list
    }
    return render(request, 'Bookstorea/Productos.html',contexto)

def ProductoCRUD_View(request):
    if request.method == 'POST':
            id = request.POST.get('ProdSEdit')
            nombre = request.POST.get('nombreProd')
            marca = request.POST.get('marcaProd')
            categoria = request.POST.get('categoriaProd')
            proveedor = request.POST.get('proveedorProd')
        #IDP IN NUMBER,NOMBRE IN VARCHAR2,MARCA IN VARCHAR2,CATEGORIA IN NUMBER,PROVEEDOR IN NUMBER
            with connection.cursor() as cursorP:
                    try:
                        if id:
                            cursorP.callproc('UPDATEPROD',[id,nombre,marca,categoria,proveedor])
                            return JsonResponse({'message': 'Producto guardado con éxito', 'status': 'success'})
                        else:
                            cursorP.callproc('INSERTPROD',[nombre,marca,categoria,proveedor])
                            return JsonResponse({'message': 'Producto guardado con éxito', 'status': 'success'})
                    except Exception as e:
                        return JsonResponse({'message': f'Error al guardar el producto: {str(e)}', 'status': 'error'})

    # VISTA  DE AUTENTICACIÓN DE USUARIOS LOGIN Y REGISTRER
def Registrar_Usuario_View(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        user = User.objects.create_user(username=username, password=password, email=email)
        messages.success(request, 'Usuario registrado exitosamente.')
        return redirect('Bookstorea/LogIn.html')

    return render(request, 'Bookstorea/Registrar.html')

def Iniciar_Sesion_View(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('Index')
        else:
            messages.error(request, 'Credenciales incorrectas.')

    return render(request, 'Bookstorea/LogIn.html')

def generar_numero_factura():
    letras = ''.join(random.choices(string.ascii_uppercase, k=3))  # Tres letras aleatorias
    numeros = ''.join(random.choices(string.digits, k=5))  # Cinco números aleatorios
    return f"{letras}{numeros}"


def generar_factura(request):
    if request.method =='GET':
        venta = VENTAS.objects.last()
        if venta:
            venta_id = venta.id_venta
    
    # Obtener el cliente
        cliente = get_object_or_404(CLIENTES, id_cliente=venta.cliente_id)
    
    # Obtener el usuario (empleado) que realizó la venta
        empleado = get_object_or_404(User, id=venta.empleado_id)
    
    # Obtener los detalles de la venta
        detalles = DETALLEVENTAS.objects.filter(venta_id=venta_id)
    
        # Estructurar los productos
        items = []
        for detalle in detalles:
            items.append({
                "name": detalle.producto.nombre_prod,
                "quantity": detalle.cantidad,
                "unit_cost": float(detalle.precio_unit)
            })

    # Datos de la factura
        datos_factura = {
            "from": f"BOOKSTORE\nLIBRERIA Y PAPELERIA\n2222",
            "to": f"{cliente.nombre_cliente}\n{cliente.correo_cliente}",
            "currency": "USD",
            "number": f"INV-{venta_id}",  # o cualquier formato que quieras
            "items": items,
            "notes": f"Empleado : {empleado}",
            "terms": "Devolucion o reembolso valido por 5 dias"
        }

    # Llamada a la API de Invoice Generator
        response = requests.post("https://invoice-generator.com",
                                    json=datos_factura,
                                    headers={"Authorization": "Bearer sk_7sbhmJpme2BGE51YlkUFmQ9Qc4Q5OYdR"}
                                )
    
        if response.status_code == 200:
            pdf = response.content
            return HttpResponse(pdf, content_type='application/pdf')
        else:
            # Manejo de errores
            return HttpResponse("Error al generar la factura.", status=response.status_code)
    return HttpResponse("Método no permitido o venta no encontrada.", status=405)

def InsertCompra_View(request):
    if request.method == 'POST':
        try:
            dataC = json.loads(request.body)
            ttC = float(dataC.get('ttC'))
            idUserC = int(dataC.get('idUserC'))
            facturaC = generar_numero_factura()
            fecha_actualC =datetime.datetime.now()
            #(NUM_FACTURA,FECHA_COMPRA,TOTAL_COMPRA,EMPLEADO_ID)
            with connection.cursor() as cursorC:
                cursorC.callproc('INSERTCOMPRA',[facturaC,fecha_actualC,ttC,idUserC])

            return JsonResponse({"status":"success"})
        except ValueError as e:
            return JsonResponse({"status":"error","message":"Error de conversión :" + str(e)})
        except ValueError as e:
            return JsonResponse({"status":"error","message":"Error de inesperado :" + str(e)})

def InsertDetCompra_View(request):
    if request.method == 'POST':
        datos_jsonDC = json.loads(request.body)
        try:
            with connection.cursor() as cursorDC:
                for registro in datos_jsonDC:
                    precioUDC = float(registro.get('precioUDC'))
                    cantidadDC = float(registro.get('cantidadDC'))
                    subtotalDC = float(registro.get('subtotalDC'))
                    idProdDC = float(registro.get('idProdDC'))
                    fEntradaDC = datetime.datetime.now()
                    fechaVencDC = fEntradaDC + relativedelta(years=5)
                    precioVentaDC = float(registro.get('precioVentaDC'))
                    cursorDC.callproc('INSERT_DET_COMPRA_LOTE',
                                      [precioUDC,cantidadDC,subtotalDC,idProdDC,fEntradaDC,fechaVencDC,precioVentaDC])
            
            return JsonResponse({'status':'success'})
        except Exception as e:
            return JsonResponse({'status': 'error','error': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'metodo no permitido'}, status=405)
        
def Reportes_View(request):
        fecha_actualC =datetime.datetime.now()
        Back_year = fecha_actualC - relativedelta(years=1)
        fecha_actualC_str = fecha_actualC.strftime('%Y-%m-%d')
        Back_year_str = Back_year.strftime('%Y-%m-%d')

        if request.method == 'POST':
            data = json.loads(request.body)
            fi = data.get("BeginDate")
            ff = data.get("EndDate")
            fecha_inicio = fi
            fecha_fin = ff
        else:
            fecha_inicio = Back_year_str
            fecha_fin = fecha_actualC_str

        with connection.cursor() as cursor_report:
        
            cursor_report.execute("""
                SELECT v.id_venta, v.fecha_venta,
                        c.nombre_cliente, c.apellido_cliente,
                        v.total, u.username
                    FROM bookstorea_ventas v
                        JOIN auth_user u ON v.empleado_id = u.id
                        JOIN bookstorea_clientes c ON v.cliente_id = c.id_cliente
                        WHERE v.fecha_venta BETWEEN '{}' AND '{}';""".format(fecha_inicio, fecha_fin))
                
            rows = cursor_report.fetchall()
            columns = [col[0] for col in cursor_report.description]
    
        Report_list = [
            dict(zip(columns, row))
            for row in rows
        ]
        contexto ={
        'Report_list': Report_list
        }

        if request.method == 'POST':
            return JsonResponse(contexto, safe=False)
        else:
            return render(request, 'Bookstorea/Reportes.html',contexto)
    
            
    


