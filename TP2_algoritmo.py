#Ivan

import cv2
import os
import numpy as np

def ABM(dir: str) -> str:
    lineas_nuevo_archivo: list = []
    registro: int = 0
    pedidos_titulos: list = ['Nro. Pedido', 'Fecha', 'Cliente', 'Ciudad', 'Provincia', 'Cod. Artículo', 'Color',
                             'Cantidad', 'Descuento']

    siguiente_linea = input('Los pedidos actuales son: ')

    with open(f"{dir}\pedidos.csv", newline="", encoding="UTF-8") as archivo_pedidos:
        for linea in archivo_pedidos:
            if registro == 0:
                print(f'Registro, {linea}')
            else:
                print(f'{registro}: {linea}')
            registro += 1
        # linea = archivo_pedidos.readlines()

    print('\nMENU\n1 - Modificar pedido existente\n2 - Agregar nuevo pedido\n3 - Eliminar pedido')
    accion = input('Elija opcion 1/2/3: ')
    while accion.isnumeric() is False or int(accion) not in (1, 2, 3):
        accion: str = input('Ingrese una opcion valida: ')

    if int(accion) == 1:

        conteo_registro: int = 1
        num_pedido = input('Que pedido quiere modificar?\nEscriba el numero de Registro: ')

        archivo_pedidos = open(f'{dir}\pedidos.csv', 'r', encoding="UTF-8")
        for registro, linea in enumerate(archivo_pedidos):

            if registro == int(num_pedido):
                linea = linea.split(',')
                print('Datos del pedido: ')

                for i in range(0, len(pedidos_titulos)):
                    print(f'{conteo_registro}: {pedidos_titulos[i]} - {linea[i]}')
                    conteo_registro += 1

                accion = input('Cual dato desea modificar? Escriba numero: ')
                while accion.isnumeric() is False or int(accion) not in (1, 2, 3, 4, 5, 6, 7, 8, 9):
                    accion: str = input('Ingrese una opcion valida: ')

                valor = input('Ingrese nuevo valor: ')
                linea[int(accion) - 1] = valor
                nueva_linea = ','.join(linea)
                lineas_nuevo_archivo.append(nueva_linea)

            else:
                lineas_nuevo_archivo.append(linea)

        archivo_pedidos.close()

        archivo_pedidos_nuevo = open(f'{dir}\pedidos.csv', 'w', encoding="UTF-8")
        archivo_pedidos_nuevo.writelines(lineas_nuevo_archivo)
        archivo_pedidos_nuevo.close()

    if int(accion) == 2:

        linea: list = []
        for i in pedidos_titulos:
            if i == 'Nro. Pedido':
                valor = '\n' + input(f'Ingrese {i}: ')
                linea.append(valor)
            else:
                valor = input(f'Ingrese {i}: ')
                linea.append(valor)

        nuevo_registro = ','.join(linea)

        archivo_pedidos_nuevo = open(f'{dir}\pedidos.csv', 'a', encoding="UTF-8")
        archivo_pedidos_nuevo.write(nuevo_registro)
        archivo_pedidos_nuevo.close()

    if int(accion) == 3:

        num_pedido = input('Que pedido quiere borrar?\nEscriba el numero de Registro: ')

        archivo_pedidos = open(f'{dir}\pedidos.csv', 'r', encoding="UTF-8")
        for registro, linea in enumerate(archivo_pedidos):

            if registro != int(num_pedido):
                lineas_nuevo_archivo.append(linea)

        archivo_pedidos.close()

        archivo_pedidos_nuevo = open(f'{dir}\pedidos.csv', 'w', encoding="UTF-8")
        archivo_pedidos_nuevo.writelines(lineas_nuevo_archivo)
        archivo_pedidos_nuevo.close()

    return dir

#Martín

def crear_lista_pedidos_entregados(listado_pedidos: list) -> list:
    lista_entregados: list = [] #lista vacia
    for sublista in listado_pedidos: #recorro sublista 
        if sublista[9] == "si":
            lista_entregados.append(sublista)
    return lista_entregados

def crear_lista_pedidos_no_entregados(listado_pedidos: list) -> list:
    lista_no_entregados: list = [] #lista vacia
    for sublista in listado_pedidos: #recorro sublista 
        if sublista[9] == "no":
            lista_no_entregados.append(sublista)
    return lista_no_entregados

def pedidos_realizados(lista_pedidos_entregados: list) -> None:
    #Pre: recibe todos los pedidos realizados (todavia no se en que formato, es probable que en dict)"
    #Post: Printea los pedidos realizados, en orden de antiguedad y devuelve la cantidad de pedidos realizados en numero. 
    numero_pedidos_entregados: int = 0 #Cantidad de pedidos inicializado
    lista_ordenada: list = []
    fecha_antigüedad: list = [32,13,3000] #día, mes, año
    for sublista in lista_pedidos_entregados: #recorre lista
        if sublista[1][2] < fecha_antigüedad[2]:
           fecha_antigüedad[2] = sublista[1][2]
        elif sublista[1][2] == fecha_antigüedad[2]:
            if sublista[1][1] < fecha_antigüedad[1]:
                fecha_antigüedad[1] = sublista[1][1]
        elif sublista[1][2] == fecha_antigüedad[2]:
            if sublista[1][1] == fecha_antigüedad[1]:
                if sublista[1][0] < fecha_antigüedad[0]:
                    fecha_antigüedad[0] = sublista[1][0]
    print(fecha_antigüedad)




        #numero_pedidos_entregados += 1 #Cuenta los pedidos realizados 
        
    #print(lista_pedidos_entregados) # printea la lista por orden de antigüedad.
    print(f"La cantidad de pedidos realizados es: {numero_pedidos_entregados}") #printea la cantidad de pedidos realizados.

def pedidos_rosario(lista_pedidos_entregados: list) -> None:
    #Pre: recibir los pedidos completados
    #Post: filtrea los que tienen como ciudad rosario, los muestra y los valoriza
    pedidos_rosario : list = [] #lista vacia
    print(len(lista_pedidos_entregados))
    for i in range(len(lista_pedidos_entregados)): #recorro dicc
        if lista_pedidos_entregados[i][3] == "Rosario": #si la ciudad es Rosario
            pedidos_rosario.append(lista_pedidos_entregados[i]) # Lo agrega a la lista vacia
    print(pedidos_rosario)
    return


def cantidad_de_productos_pedidos(listado_pedidos: list, productos: dict) -> dict:
    #Pre: recibe los pedidos
    #Post: cuenta cada pedido en una lista, mostrando la cantidad de cada producto vendido
    cantidad_botellas: dict = {"verde": 0, "rojo": 0, "azul": 0, "negro": 0, "amarillo": 0}
    cantidad_vasos: dict = {"negro": 0, "azul": 0,}
    for i in range(len(listado_pedidos)):
        if listado_pedidos[i][5] == 1334:
            if listado_pedidos[i][6] in cantidad_botellas.keys():
                cantidad_botellas[listado_pedidos[i][6]] += listado_pedidos[i][7]
        elif listado_pedidos[i][5] == 568:
            if listado_pedidos[i][6] in cantidad_vasos.keys():
                cantidad_vasos[listado_pedidos[i][6]] += listado_pedidos[i][7]
    productos.update({"botella": cantidad_botellas})
    productos.update({"vaso" : cantidad_vasos})
    return productos

def cantidad_de_productos_entregados(lista_pedidos_entregados: list, productos_entregados: dict) -> dict:
    cantidad_botellas_entregadas: dict = {"verde": 0, "rojo": 0, "azul": 0, "negro": 0, "amarillo": 0}
    cantidad_vasos_entregados: dict = {"negro": 0, "azul": 0,}
    for i in range(len(lista_pedidos_entregados)):
        if lista_pedidos_entregados[i][5] == 1334:
            if lista_pedidos_entregados[i][6] in cantidad_botellas_entregadas.keys():
                cantidad_botellas_entregadas[lista_pedidos_entregados[i][6]] += lista_pedidos_entregados[i][7]
        elif lista_pedidos_entregados[i][5] == 568:
            if lista_pedidos_entregados[i][6] in cantidad_vasos_entregados.keys():
                cantidad_vasos_entregados[lista_pedidos_entregados[i][6]] += lista_pedidos_entregados[i][7]
    productos_entregados.update({"botella": cantidad_botellas_entregadas})
    productos_entregados.update({"vaso" : cantidad_vasos_entregados})
    return productos_entregados

def articulo_mas_pedido(productos: dict, productos_entregados: dict) -> None:
    #Pre: Recibe el diccionario de productos y productos entregados.
    #Post: muestra cual es el articulo mas pedido y cuantos fueron entregados.
    producto_mas_pedido: str = "-" #inicializo variables
    color: str = ""
    cantidad_producto_mas_pedido: int = 0
    if productos["botella"]["verde"] > cantidad_producto_mas_pedido: #si tiene la mayor cantidad de pedidos
        cantidad_producto_mas_pedido = productos["botella"]["verde"] #lo guardo en esta variable
        producto_mas_pedido = "botella"
        color = "verde"
    elif productos["botella"]["rojo"] > cantidad_producto_mas_pedido: #repito proceso con cad producto
        cantidad_producto_mas_pedido = productos["botella"]["rojo"]
        producto_mas_pedido = "botella"
        color = "rojo"
    elif productos["botella"]["azul"] > cantidad_producto_mas_pedido:
        cantidad_producto_mas_pedido = productos["botella"]["azul"]
        producto_mas_pedido = "botella"
        color = "azul"
    elif productos["botella"]["negro"] > cantidad_producto_mas_pedido:
        cantidad_producto_mas_pedido = productos["botella"]["negro"]
        producto_mas_pedido = "botella"
        color = "negro"
    elif productos["botella"]["amarillo"] > cantidad_producto_mas_pedido:
        cantidad_producto_mas_pedido = productos["botella"]["amarillo"]
        producto_mas_pedido = "botella"
        color = "amarillo"
    elif productos["vaso"]["negro"] > cantidad_producto_mas_pedido:
        cantidad_producto_mas_pedido = productos["vaso"]["negro"]
        producto_mas_pedido = "vaso"
        color = "negro"
    elif productos["vaso"]["azul"] > cantidad_producto_mas_pedido:
        cantidad_producto_mas_pedido = productos["vaso"]["azul"]
        producto_mas_pedido = "vaso"
        color = "azul"
    print(f"El producto más pedido es: {producto_mas_pedido} de color {color} con {cantidad_producto_mas_pedido} unidades.\n De esa cantidad, {productos_entregados[producto_mas_pedido][color]} fueron entregados.")

def volver_menu():
    input('Presione ENTER para volver al menu: ')
    
def main():

    #Martín

    listado_pedidos: list = [[1,[1,11,2021],"Juan Alvarez", "Rosario", "Córdoba", 1334, "azul", 36, 5, "si"],#[NdePedido, fecha, cliente, ciudad, provincia, cod. articulo, color, cantidad, descuento, entregado]
    [2, [2,11,2021], "Carlos Rodriguez", "Parana", "Santa Fe", 1334, "azul", 5, 0, "no"], [3, [2,11,2021], "Carlos Rodriguez", "Rosario", "Santa Fe", 1334, "negro", 5, 0, "no"]]
    productos: dict = {}
    productos_entregados: dict = {}
    lista_pedidos_entregados: list = crear_lista_pedidos_entregados(listado_pedidos)
    lista_pedidos_no_entregados: list = crear_lista_pedidos_no_entregados(listado_pedidos)
    


    #Ivan
    pedir_ruta_abm: int = 0
    dir_abm: str = ''
    cerrar_menu: bool = False

    #Menú --> Ivan = 1, 2, 3
    #Martín = 4, 5, 6

    while cerrar_menu == False:
        print('Bienvenido al MENU')
        print('1: Alta - Baja - Modificacion de pedidos\n4:Listado de pedidos que fueron completados.\5Pedidos de Rosario con su valorización\n6.Artículo más pedido y cuantos fueron entregados.\n7.Salir')

        accion = input('Elija opcion escribiendo el numero correspondiente: ')
        while accion.isnumeric() is False or int(accion) not in (1, 2, 3, 4, 5, 6, 7):
            accion: str = input('Ingrese una opcion valida: ')

        if int(accion) == 1:

            if pedir_ruta_abm == 0:
                print('Por favor, ingrese la ruta en donde se encuentra su archivo de pedidos usando " \ "')
                print('Ejemplo: D:\Documentos\Python Proyectos\prueba')
                dir_abm = input('')
                while not os.path.isdir(dir_abm):
                    dir_abm = input('Directorio invalido, pruebe nuevamente: ')
                pedir_ruta_abm = 1

            dir_abm = ABM(dir_abm)
            volver_menu()
        elif int(accion) == 2:
            return #ivan
        elif int(accion) == 3:
            return # ivan
        elif int(accion) == 4:
            pedidos_realizados(lista_pedidos_entregados)
        elif int(accion) == 5:
            pedidos_rosario(lista_pedidos_entregados)
        elif int(accion) == 6:
            cantidad_de_productos_pedidos(listado_pedidos, productos)
            cantidad_de_productos_entregados(lista_pedidos_entregados, productos_entregados)
            articulo_mas_pedido(productos, productos_entregados)
            volver_menu()
        elif int(accion) == 7:
            print("Abandonando el menú...")
            cerrar_menu = True 
    
  
   
    


main()