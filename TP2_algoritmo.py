import cv2
import os
import numpy as np
from geopy import distance

#Ivan
def ABM(dir: str) -> str:
    '''Toma direccion de archivo pedidos y la devuelve.
    Permite modificar, agregar o eliminir pedidos'''
    lineas_nuevo_archivo: list = []
    registro: int = 0
    pedidos_titulos: list = ['Nro. Pedido', 'Fecha', 'Cliente', 'Ciudad', 'Provincia', 'Cod. Artículo', 'Color',
                             'Cantidad', 'Descuento']

    siguiente_linea = input('Los pedidos actuales son: ')

    with open(f"{dir}\pedidos.csv", newline = "", encoding="UTF-8") as archivo_pedidos:
        for linea in archivo_pedidos:
            if registro == 0:
                print(f'Registro, {linea}')
            else:
                print(f'{registro}: {linea}')
            registro += 1

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
            #Saltea el pedido a borrar
            if registro != int(num_pedido):
                lineas_nuevo_archivo.append(linea)

        archivo_pedidos.close()

        archivo_pedidos_nuevo = open(f'{dir}\pedidos.csv', 'w', encoding="UTF-8")
        archivo_pedidos_nuevo.writelines(lineas_nuevo_archivo)
        archivo_pedidos_nuevo.close()


    return dir

def recorrido(zona: dict, palabra: str, dir: str, imprimir: str) -> list:
    '''Toma el diccionario para la zona correspondiente, la palabra norte/centro/sur, direccion de archivo e imprimir como string de si/no
        Devuelve un listado de las ciudades ordenadas por recorrido mas óptimo para usarse en la funcion de procesado de pedidos'''
    # Listado para el procesado de pedidos
    procesado_pedidos_lista: list = []
    # Latitud, Longitud
    planta_campana = [34.1633, 58.9593]

    globals()[f'zona_{palabra}_pedidos']: dict = {}
    globals()[f'zona_{palabra}_pedidos_capitales']: dict = {}

    archivo_pedidos = open(f'{dir}\pedidos.csv', 'r', encoding="UTF-8")

    # Lee linea a linea el archivo pedidos.csv para obtener los pedidos de zona {palabra}
    for registro, linea in enumerate(archivo_pedidos):
        linea = linea.split(',')
        if linea[4].lower() in zona.keys() and linea[3].lower() != 'caba':
            globals()[f'zona_{palabra}_pedidos_capitales'][linea[3].lower()] = \
                [zona.get(linea[4].lower()), linea[4].lower()]
            globals()[f'zona_{palabra}_pedidos'][linea[4].lower()] = \
                [zona.get(linea[4].lower()), linea[3].lower()]

    if not bool(globals()[f'zona_{palabra}_pedidos'].keys()):
        if imprimir == 'si':
            print(f'No hay pedidos para la zona {palabra}')


    else:
        # Calcula menor distancia entre Planta de Campana y ciudades de zona {palabra}.
        distancia_menor: int = 1000000000000
        for i in globals()[f'zona_{palabra}_pedidos'].keys():
            distancia: int = distance.distance(planta_campana,
                                               globals()[f'zona_{palabra}_pedidos'].get(i)[0]).kilometers
            if distancia < distancia_menor:
                distancia_menor = distancia
                provincia_cercana: str = i
                ciudad_cercana: str = globals()[f'zona_{palabra}_pedidos'][provincia_cercana][1]
        if imprimir == 'si':
            print(f'El recorrido mas óptimo va desde la planta en Campana hacia {provincia_cercana}: '
                  f'{ciudad_cercana}')
        procesado_pedidos_lista.append(ciudad_cercana)
        # Calcula cual es la provincia/ciudad mas cercana a la anterior

        ciudades_descarte: list = []
        for x in range(0, len(globals()[f'zona_{palabra}_pedidos_capitales']) - 1):
            distancia_menor: int = 1000000000000

            for i in globals()[f'zona_{palabra}_pedidos_capitales'].keys():

                if ciudad_cercana != i and i not in ciudades_descarte:
                    distancia: int = distance.distance(
                        globals()[f'zona_{palabra}_pedidos_capitales'].get(ciudad_cercana)[0],
                        globals()[f'zona_{palabra}_pedidos_capitales'].get(i)[0]).kilometers
                    if distancia < distancia_menor:
                        distancia_menor = distancia
                        ciudad_cercana2: str = i

            ciudades_descarte.append(ciudad_cercana)
            if imprimir == 'si':
                print(
                    f'Desde {globals()[f"zona_{palabra}_pedidos_capitales"][ciudad_cercana][1]}: {ciudad_cercana} hacia '
                    f'{globals()[f"zona_{palabra}_pedidos_capitales"][ciudad_cercana2][1]}: {ciudad_cercana2}')
            procesado_pedidos_lista.append(ciudad_cercana2)
            ciudad_cercana = ciudad_cercana2

    archivo_pedidos.close()
    return procesado_pedidos_lista

def pedidos_entregados(registros: dict, dir: str):
    '''Toma diccionario de registros como valores para las claves si y no, tambien direccion de carpeta de archivos.
    Crea archivo pedidos_realizados.csv con los pedidos con flag de entregados si/no'''
    lineas_pedidos2: list = []
    archivo_pedidos = open(f'{dir}\pedidos.csv', 'r', encoding="UTF-8")
    # Lee linea a linea el archivo pedidos.csv para obtener los registros y comparar con el dict registros
    for registro, linea in enumerate(archivo_pedidos):
        if registro == 0 and not os.path.isfile(f'{dir}\pedidos_realizados.csv'):
            lineas_pedidos2.append(linea)
        if registro in registros.get('si'):
            linea = linea.rstrip('\n')
            linea = linea + ',si\n'
            lineas_pedidos2.append(linea)

        elif registro in registros.get('no'):
            linea = linea.rstrip('\n')
            linea = linea + ',no\n'
            lineas_pedidos2.append(linea)

    archivo_pedidos.close()
    # Crea nuevo archivo (si no existe) con el flag de entregado si/no
    if not os.path.isfile(f'{dir}\pedidos_realizados.csv'):
        archivo_pedidos = open(f'{dir}\pedidos_realizados.csv', 'w', encoding="UTF-8")
        archivo_pedidos.writelines(lineas_pedidos2)
        archivo_pedidos.close()
    elif os.path.isfile(f'{dir}\pedidos_realizados.csv'):
        archivo_pedidos = open(f'{dir}\pedidos_realizados.csv', 'a', encoding="UTF-8")
        archivo_pedidos.writelines(lineas_pedidos2)
        archivo_pedidos.close()



def procesado_pedidos(zona: dict, dir: str, utilitario_usado: int, palabra: str) -> int:
    '''Toma el diccionario para la zona correspondiente, direccion de archivo, la palabra norte/centro/sur, y el numero de utilitario ya usado para no tenerlo en cuenta en la
        próxima corrida. Devuelve el numero de utilitario usado.'''
    utilitarios: dict = {1: 600, 2: 1000, 3: 500, 4: 2000}  # num_utilitario: kilos
    utilitarios.pop(utilitario_usado, None)
    articulos: dict = {1334: [0.450, 0], 568: [0.350, 0]}  # num_art: [kilos, cantidad]

    peso_final: int = 0
    peso_referencia: int = 10000000
    utilitario_asignado: int = 0

    ciudades_pedidos: list = []

    lineas_pedidos: list = [] # Para marcar pedidos entregados o no
    lineas_si_no: dict = {'si': [], 'no': []}

    archivo_pedidos = open(f'{dir}\pedidos.csv', 'r', encoding="UTF-8")

    # Lee linea a linea el archivo pedidos.csv para obtener los pedidos de zona {palabra}
    for registro, linea in enumerate(archivo_pedidos):
        linea = linea.split(',')
        if linea[4].lower() in zona.keys():

            nueva_cantidad = articulos[int(linea[5])][1] + int(linea[7])
            if int(linea[5]) == 1334:
                peso_final = (articulos[1334][0] * nueva_cantidad) + (articulos[568][0] * articulos[568][1])


            elif int(linea[5]) == 568:
                peso_final = (articulos[1334][0] * articulos[1334][1]) + (articulos[568][0] * nueva_cantidad)

            if peso_final <= max(utilitarios.values()):
                # Calcula resta entre pesos de utilitarios y peso de articulos actuales
                for i in utilitarios.keys():
                    resta = utilitarios[i] - peso_final
                    if 0 <= resta < peso_referencia:
                        articulos[int(linea[5])][1] = nueva_cantidad
                        utilitario_asignado = i
                        peso_referencia = resta
                        ciudades_pedidos.append(linea[3].lower())
                        # Pedidos entregados
                        lineas_si_no['si'].append(registro)
            # Pedidos no entregados
            elif peso_final > max(utilitarios.values()):
                lineas_si_no['no'].append(registro)
    archivo_pedidos.close()

    # Genero archivo pedidos nuevo con flag de entregados si/no
    pedidos_entregados(lineas_si_no, dir)
    # Obtengo recorrido optimo
    ciudades_recorridas = recorrido(zona, palabra.lower(), dir, 'no')

    ciudades_salida_txt: list = []
    # Comparo recorrido optimo con las ciudades a las que sí podrán entregarse los pedidos
    for i in ciudades_recorridas:
        if i in ciudades_pedidos:
            ciudades_salida_txt.append(i)
    mostrar_ciudades = ", ".join(ciudades_salida_txt)

    peso_final = (articulos[1334][0] * articulos[1334][1]) + (articulos[568][0] * articulos[568][1])

    if not os.path.isfile(f'{dir}\salida.txt') and utilitario_asignado != 0:
        archivo_salida = open(f'{dir}\salida.txt', 'w', encoding="UTF-8")
        archivo_salida.write(f'Zona {palabra}\nUtilitario 00{utilitario_asignado}\n{int(peso_final)} kg')
        archivo_salida.write(f'\nRecorrido: {mostrar_ciudades}')
        archivo_salida.close()
    elif os.path.isfile(f'{dir}\salida.txt') and utilitario_asignado != 0:
        archivo_salida = open(f'{dir}\salida.txt', 'a', encoding="UTF-8")
        archivo_salida.write(f'\nZona {palabra}\nUtilitario 00{utilitario_asignado}\n{int(peso_final)} kg')
        archivo_salida.write(f'\nRecorrido: {mostrar_ciudades}')
        archivo_salida.close()

    return utilitario_asignado

def crea_lista_pedidos(dir: str) -> list:
    '''Toma la direccion para archivos. Abre el archivo pedidos_realizados.csv y devuelve en lista los pedidos
    con flag de entregado si/no'''
    listado_pedidos: list = []

    archivo_pedidos = open(f'{dir}\pedidos_realizados.csv', 'r', encoding="UTF-8")
    for registro, linea in enumerate(archivo_pedidos):
        if registro != 0:
            linea = linea.rstrip('\n')
            linea = linea.split(',')
            # Transformo numeros de la lista a int
            for i in range(0, len(linea)):
                if linea[i].isnumeric() is True:
                    linea[i] = int(linea[i])

            linea[1] = linea[1].split('/')
            for i in range(3):
                if linea[1][i].isnumeric() is True:
                    linea[1][i] = int(linea[1][i])

            listado_pedidos.append(linea)
    archivo_pedidos.close()
    return listado_pedidos


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

def ordenar_pedidos(listado_pedidos: list) -> list:
    listado_pedidos_ordenado: list = []
    for item in listado_pedidos:
        if item[9] == "si":
            listado_pedidos_ordenado.append(item)
    listado_pedidos_ordenado = ordenamiento_burbuja(listado_pedidos_ordenado)
    return listado_pedidos_ordenado

def ordenamiento_burbuja(listado_pedidos_ordenado):
    orden: bool = False
    while (orden == False):
        orden = True
        for i in range(len(listado_pedidos_ordenado) - 1):
            dia = listado_pedidos_ordenado[i][1][0]
            mes = listado_pedidos_ordenado[i][1][1]
            anio = listado_pedidos_ordenado[i][1][2]

            diaSig = listado_pedidos_ordenado[i + 1][1][0]
            mesSig = listado_pedidos_ordenado[i + 1][1][1]
            anioSig = listado_pedidos_ordenado[i + 1][1][2]
           
            if anio > anioSig:
                intercambiar(listado_pedidos_ordenado,i)
                orden = False

            elif anio == anioSig and mes > mesSig:
                intercambiar(listado_pedidos_ordenado,i)
                orden = False

            elif anio == anioSig and mes == mesSig and dia > diaSig:
                intercambiar(listado_pedidos_ordenado,i)
                orden = False

    return listado_pedidos_ordenado

def intercambiar(listado_pedidos_ordenado, index):
    aux: list = listado_pedidos_ordenado[index]
    listado_pedidos_ordenado[index] = listado_pedidos_ordenado[index + 1]
    listado_pedidos_ordenado[index + 1] = aux
    

def pedidos_realizados(listado_pedidos_ordenado: list) -> None:
    #Pre: recibe todos los pedidos realizados en formato de lista"
    #Post: Printea los pedidos realizados, en orden de antiguedad y devuelve la cantidad de pedidos realizados en numero. 
    numero_pedidos_entregados: int = 0
    numero_de_pedido: int = 0
    for i in range(len(listado_pedidos_ordenado)):
        if listado_pedidos_ordenado[i][0] != numero_de_pedido:
            numero_pedidos_entregados += 1
            numero_de_pedido = listado_pedidos_ordenado[i][0]
    print(f"La cantidad de pedidos realizados es: {numero_pedidos_entregados}") #printea la cantidad de pedidos realizados.
    print(f"A continuación se mostrará la lista por orden de antigüedad:\n{listado_pedidos_ordenado}")

def pedidos_rosario(lista_pedidos_entregados: list) -> None:
    #Pre: recibir los pedidos completados
    #Post: filtrea los que tienen como ciudad rosario, los muestra y los valoriza
    pedidos_rosario : list = [] #lista vacia
    precio_botella: int = 15
    precio_vaso: int = 8
    dicc_valores_por_pedido: dict = {}
    for i in range(len(lista_pedidos_entregados)): #recorro dicc
        if lista_pedidos_entregados[i][3] == "Rosario": #si la ciudad es Rosario
            pedidos_rosario.append(lista_pedidos_entregados[i]) # Lo agrega a la lista vacia
    for i in range(len(pedidos_rosario)):
        valor_pedido: float = 0
        if pedidos_rosario[i][5] == 1334: #si es una botella
            try: #si aplica descuento
                valor_pedido += precio_botella * pedidos_rosario[i][7] - (15 * pedidos_rosario[i][7]) / pedidos_rosario[i][8] # valor_producto * cantidad de producto pedido - descuento
            except ZeroDivisionError: #si no aplica descuento
                valor_pedido += precio_botella * pedidos_rosario[i][7]
        elif pedidos_rosario[i][5] == 568: #si es un vaso
            try: 
                valor_pedido += precio_vaso * pedidos_rosario[i][7] - (15 * pedidos_rosario[i][7]) / pedidos_rosario[i][8]
            except ZeroDivisionError:
                valor_pedido += precio_botella * pedidos_rosario[i][7]
        dicc_valores_por_pedido.update({pedidos_rosario[i][0]: valor_pedido}) 
    print(f"A continuación se mostrarán los pedidos que fueron entregados en la ciudad de Rosario:\n {pedidos_rosario}")
    print(f"Se mostrará el valor en dolares de cada pedido entregado:\nNumero de pedido: valor\n{dicc_valores_por_pedido}")
    


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
    #Pre: recibe los pedidos que fueron entregados
    #Post: cuenta cada pedido en una lista, mostrando la cantidad de cada producto vendido
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

    
def load_yolo():
    # Pos: levanta la red Neuronal con los archivos de pesos pre-entrenados de YoloV3, el archivo de configuración y el archivo de nombres

    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    classes: list = []
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layers_names = net.getLayerNames()
    output_layers = [layers_names[i - 1] for i in net.getUnconnectedOutLayers()]

    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    return net, classes, colors, output_layers

def load_image(img_path):
    # Pre: Debe recibir la ruta de una imegen
    # Pos: lee la imagen  y cambia su tamaño  y retorna la imagen con las nuevas dimenciones ( alto, ancho..)

    img = cv2.imread(img_path)
    img = cv2.resize(img, None, fx=0.4, fy=0.4)
    height, width, channels = img.shape

    return img, height, width, channels

def detect_objects(img, net, outputLayers):
    # Pre: Recibe una imagen, y las capas de salida de la red
    # Pos: Se aplica la  red neuronal sobre la imagen

    blob = cv2.dnn.blobFromImage(img, scalefactor=0.00392, size=(320, 320), mean=(0, 0, 0), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward(
        outputLayers)  # devuelve una lista anidada con toda la info del onj detectado, ancho, alto etc
    return blob, outputs

def get_box_dimensions(outputs, height, width):
    # Pre:
    # Pos:

    boxes = []
    confs = []
    class_ids = []
    for output in outputs:
        for detect in output:
            scores = detect[5:]
            # print(scores)
            class_id = np.argmax(scores)
            conf = scores[class_id]
            if conf > 0.3:
                center_x = int(detect[0] * width)
                center_y = int(detect[1] * height)
                w = int(detect[2] * width)
                h = int(detect[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confs.append(float(conf))
                class_ids.append(class_id)
    return boxes, confs, class_ids

def draw_labels(boxes, confs, colors, class_ids, classes, img):
    # Pre:
    # Pos:

    indexes = cv2.dnn.NMSBoxes(boxes, confs, 0.5, 0.4)
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])

    return label

def image_detect(img_path):
    # Pre: Recibe la ruta de una imagen
    # Pos: Invoca a distintas funciones para retonar la imagen detectada

    model, classes, colors, output_layers = load_yolo()
    image, height, width, channels = load_image(img_path)
    blob, outputs = detect_objects(image, model, output_layers)
    boxes, confs, class_ids = get_box_dimensions(outputs, height, width)
    return draw_labels(boxes, confs, colors, class_ids, classes, image)

def deteccion_colores(imagen) -> str:
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
    colores_rango = {
        "Verde": ([40, 100, 100], [75, 255, 255]),
        "Negro": ([0, 0, 0], [0, 0, 10]),
        "Rojo": ([161, 155, 84], [179, 255, 255]),
        "Azul": ([94, 80, 2], [126, 255, 255]),
        "Amarillo": ([25, 100, 100], [30, 255, 255])}
    for nombre_color, (lower, upper) in colores_rango.items():
        lower = np.array(lower)
        upper = np.array(upper)
        mask = cv2.inRange(hsv, lower, upper)
        resultado = cv2.bitwise_and(imagen, imagen, mask = mask)
        if mask.any():
            color = nombre_color
    return color

def contadores_carpeta(objeto: str, color: str, botellas: dict, vasos: dict) -> dict:
    if objeto == "bottle":
        botellas[color] = botellas[color] + 1
    elif objeto == "cup":
        try:
            vasos[color] = vasos[color] + 1
        except KeyError:
            pass
    return botellas, vasos

def verificacion_escaner(objeto: str) -> str:
    if not objeto == "bottle" or objeto == "cup":
        estado = "falla"
        print("PROCESO DETENIDO, se reanudo en un minuto")
    else:
        estado = "ok"
    return estado

def imagenes_carpeta(carpeta, contador_botellas: dict, contador_vasos: dict):
    for filename in os.listdir(carpeta):
        img = cv2.imread(os.path.join(carpeta,filename))
        objeto = image_detect(img)
        verificacion = verificacion_escaner(objeto)
        if not verificacion == "falla":
            color = deteccion_colores(img)
            contadores_carpeta(objeto, color, contador_botellas, contador_vasos)
        cv2.imshow("escaner", img)
        cv2.waitKey(0)

def cantidades_txt(contador_botellas: dict, contador_vasos: dict) -> None:
    with open("botellas.txt", "w") as b:
        for key, value in contador_botellas.items():
            b.write("%s %s\n" % (key, value))
    with open("vasos.txt", "w") as v:
        for key, value in contador_vasos.items():
            v.write("%s %s\n" % (key, value))

def main():
    contadores_botellas: dict = {"Verde": 0, "Negro": 0, "Rojo": 0, "Azul": 0, "Amarillo": 0}
    contadores_vasos: dict = {"Negro": 0, "Azul": 0}
        
    #Ivan
    #Latitudes, Longitudes
    zona_norte = {'catamarca': [28.4696, 65.7795], 'cordoba': [31.4201, 64.1888],
                                    'chaco': [26.5858, 60.9540], 'corrientes': [28.5842, 58.0072],
                                    'formosa': [26.1858, 58.1756],
                                    'jujuy': [24.1858, 65.2995], 'la rioja': [29.4135, 66.8565],
                                    'misiones': [26.9377, 54.4342],
                                    'salta': [24.7821, 65.4232], 'santiago del estero': [27.7834, 64.2642],
                                    'tucuman': [26.8083, 65.2176],
                                    'entre rios': [32.5176, 59.1042], 'mendoza': [32.8895, 68.8458],
                                    'san juan': [31.5351, 68.5386],
                                    'san luis': [33.3017, 66.3378], 'santa fe': [31.6107, 60.6973],
                                    'buenos aires': [34.6037, 58.3816]}

    zona_centro = {'la pampa': [37.8957, 65.0958], 'neuquen': [38.9517, 68.0592]}

    zona_sur = {'chubut': [43.6846, 69.2746], 'rio negro': [40.7344, 66.6176],
                                'santa cruz': [48.7737, 69.1917], 'tierra del fuego': [54.3084, 67.7452]}
    #Direccion archivo
    print('Antes de iniciar, por favor, ingrese la ruta en donde se encuentra su archivo de pedidos usando " \ "')
    print('Ejemplo: D:\Documentos\Python Proyectos\prueba')
    direccion_archivo = input('')
    while not os.path.isdir(direccion_archivo):
        direccion_archivo = input('Directorio invalido, pruebe nuevamente: ')
    
    
    #Martín

    productos: dict = {}
    productos_entregados: dict = {}
    
    
    cerrar_menu: bool = False

    #Menú --> Ivan = 1, 2, 3
    #Martín = 4, 5, 6

    while cerrar_menu == False:
        print('Bienvenido al MENU')
        print('1: Alta - Baja - Modificacion de pedidos\n2: Determinar un recorrido por zona\n3: Procesar los pedidos\n4:Listado de pedidos que fueron completados.'
              '\n5Pedidos de Rosario con su valorización\n6.Artículo más pedido y cuantos fueron entregados.\n7.Salir')

        accion = input('Elija opcion escribiendo el numero correspondiente: ')
        while accion.isnumeric() is False or int(accion) not in (1, 2, 3, 4, 5, 6, 7):
            accion: str = input('Ingrese una opcion valida: ')

        if int(accion) == 1:

            direccion_archivo = ABM(direccion_archivo)
            volver_menu() #ivan
            
        elif int(accion) == 2:
            print('Zonas:\n1: Norte\n2: Centro\n3: Sur')
            accion = input('Para que zona desea ver el recorrido? 1/2/3: ')
            while accion.isnumeric() is False or int(accion) not in (1, 2, 3):
                accion: str = input('Ingrese una opcion valida: ')
            if int(accion) == 1:
                recorrido(zona_norte, 'norte', direccion_archivo, 'si')
            if int(accion) == 2:
                recorrido(zona_centro, 'centro', direccion_archivo, 'si')
            if int(accion) == 3:
                recorrido(zona_sur, 'sur', direccion_archivo, 'si')
            volver_menu() #ivan
        elif int(accion) == 3: #ivan
            utilitario_asignado = procesado_pedidos(zona_norte, direccion_archivo, 0, 'Norte')
            utilitario_asignado = procesado_pedidos(zona_centro, direccion_archivo, utilitario_asignado, 'Centro')
            utilitario_asignado = procesado_pedidos(zona_sur, direccion_archivo, utilitario_asignado, 'Sur')
            #Martin
            listado_pedidos: list = crea_lista_pedidos(direccion_archivo)
            lista_pedidos_entregados: list = crear_lista_pedidos_entregados(listado_pedidos)
            lista_pedidos_no_entregados: list = crear_lista_pedidos_no_entregados(listado_pedidos)
            volver_menu() 
        elif int(accion) == 4:
            listado_pedidos_ordenado: list = ordenar_pedidos(listado_pedidos)
            pedidos_realizados(listado_pedidos_ordenado)
            volver_menu()
        elif int(accion) == 5:
            pedidos_rosario(lista_pedidos_entregados)
            volver_menu()
        elif int(accion) == 6:
            cantidad_de_productos_pedidos(listado_pedidos, productos)
            cantidad_de_productos_entregados(lista_pedidos_entregados, productos_entregados)
            articulo_mas_pedido(productos, productos_entregados)
            volver_menu()
        elif int(accion) == 7:
            print("Abandonando el menú...")
            cerrar_menu = True 
    
  
   
    
    imagenes_carpeta("TP_Arch_config/Lote0001", contadores_botellas, contadores_vasos)
    cantidades_txt(contadores_botellas, contadores_vasos)

main()
