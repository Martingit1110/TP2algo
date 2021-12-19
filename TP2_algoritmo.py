import cv2
import numpy as np
import os
from geopy import distance
import unicodedata
from geopy.geocoders import Nominatim
import certifi
import ssl
import geopy.geocoders


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


def load_image(img_path) -> tuple:
    # Pre: Debe recibir la ruta de una imegen
    # Pos: lee la imagen  y cambia su tamaño  y retorna la imagen con las nuevas dimenciones ( alto, ancho..)

    # img = cv2.imread(img_path)
    img = cv2.resize(img_path, None, fx=0.4, fy=0.4)
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


def get_box_dimensions(outputs, height, width) -> tuple:
    """ Esta funcion recibe como parametro :

    outputs: Recibe una lista anidada que contiene información sobre todos los objetos detectados asi como tambien la altura
    y el ancho del cuadro delimitador,la confianza y las puntuaciones para todas las clases de objetos enumerados en coco.names.

    height:Altura de la imagen

    width: Ancho de la imagen

    Retorna una tupla, compuesta por tres lista:
    
    confs: con todos los cuadros delimitadores previstos con una confianza de más del 30 %.
    boxes:los vértices del cuadro delimitador
    class_id : índice de clase del objeto predicha

    """

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


def draw_labels(boxes, confs, colors, class_ids, classes, img) -> str:
    
    # Pre: Recibe varias listas la de puntuaciones que almacena la confianza correspondiente a cada objeto y la lista de puntuacion del mismo
    # Pos: Retorna el objeto detectado

    indexes = cv2.dnn.NMSBoxes(boxes, confs, 0.5, 0.4)
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])

    return label



def image_detect(img_path) -> tuple:
    # Pre: Recibe la ruta de una imagen
    # Pos: Invoca a distintas funciones para retonar la imagen detectada

    model, classes, colors, output_layers = load_yolo()
    image, height, width, channels = load_image(img_path)
    blob, outputs = detect_objects(image, model, output_layers)
    boxes, confs, class_ids = get_box_dimensions(outputs, height, width)

    return draw_labels(boxes, confs, colors, class_ids, classes, image)


def deteccion_colores(imagen) -> str:
    #Pre: la imagen tiene que poder mutar su color al rango hsv.
    #Post: recibe una imagen, verifica si hay alguno de los 5 colores preestablecidos y retorna una cadena que indica el color existente.
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
        resultado = cv2.bitwise_and(imagen, imagen, mask=mask)
        if mask.any():
            color = nombre_color
    return color


def contadores_carpeta(objeto: str, color: str, botellas: dict, vasos: dict) -> dict:
    #Pre: el objeto y el color deben ser cadena, recibe los diccionarios contadores de botellas y vasos.
    #Post: verifica que objeto es y actualiza el diccionario contador correspondiente.
    if objeto == "bottle":
        botellas[color] = botellas[color] + 1
    elif objeto == "cup":
        try:
            vasos[color] = vasos[color] + 1
        except KeyError:
            pass
    return botellas, vasos

def verificacion_escaner(objeto: str) -> str:
    #Pre: el objeto debe ser una cadena.
    #Post: verifica que objeto es y retorna el estado del escaner.
    if objeto == "bottle" or objeto == "cup":
        estado = "ok"
        #print(objeto)
    else:
        estado = "falla"
        #print("PROCESO DETENIDO, se reanudo en un minuto")

    return estado


def imagenes_carpeta(carpeta, contador_botellas: dict, contador_vasos: dict):
    #Pre: tiene que ingresar una direccion que lleve a una carpeta con archivos dentro, recibe los diccionarios contadores de botellas y vasos.
    #Post: recorre, carga y analiza los archivos dentro de la carpeta recibida uno por uno.
    print("Analizando imagenes seleccionadas, por favor aguarde unos instantes")
    for filename in os.listdir(carpeta):
        img = cv2.imread(os.path.join(carpeta, filename))
        objeto = image_detect(img)
        verificacion = verificacion_escaner(objeto)
        if verificacion == "ok":
            color = deteccion_colores(img)
            contadores_carpeta(objeto, color, contador_botellas, contador_vasos)
        # cv2.imshow("escaner", img)
        # cv2.waitKey(0)


def cantidades_txt(contador_botellas: dict, contador_vasos: dict) -> None:
    #Pre: recibe los diccionarios contadores de botellas y vasos.
    #Post: actualiza o crea los archivos botellas.txt y vasos.txt con los diccionarios recibidos.
    with open("botellas.txt", "w") as b:
        for key, value in contador_botellas.items():
            b.write("%s %s\n" % (key, value))
    with open("vasos.txt", "w") as v:
        for key, value in contador_vasos.items():
            v.write("%s %s\n" % (key, value))



def ABM(dir: str, contadores_botellas: dict) -> str:
    '''Toma direccion de archivo pedidos y la devuelve. Tambien toma contadores_botellas para corroborar ingreso de color.
    Permite modificar, agregar o eliminir pedidos'''
    iniciar: str = '1'
    while int(iniciar) == 1:
        lineas_nuevo_archivo: list = []
        registro: int = 0
        pedidos_titulos: list = ['Nro. Pedido', 'Fecha', 'Cliente', 'Ciudad', 'Provincia', 'Cod. Artículo', 'Color',
                                 'Cantidad', 'Descuento']

        siguiente_linea = input('\nPresione ENTER para ver los pedidos actuales:')

        with open(f"{dir}\pedidos.csv", newline="", encoding="UTF-8") as archivo_pedidos:
            for linea in archivo_pedidos:
                if registro == 0:
                    print('\n\nLa información de los pedidos está ordenada de la siguiente manera:')
                    print(f'Registro, {linea}')
                else:
                    print(f'{registro}: {linea}')
                registro += 1

        print('\nABM\n1 - Modificar pedido existente\n2 - Agregar nuevo pedido\n3 - Eliminar pedido')
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
                    print('\nDatos del pedido: ')
                    # Muestra datos enumerados
                    for i in range(0, len(pedidos_titulos)):
                        print(f'{conteo_registro}: {pedidos_titulos[i]} - {linea[i]}')
                        conteo_registro += 1

                    opcion = input('Cual dato desea modificar? Escriba numero: ')
                    while opcion.isnumeric() is False or int(opcion) not in (1, 2, 3, 4, 5, 6, 7, 8, 9):
                        opcion: str = input('Ingrese una opcion valida: ')
                    # Modifica
                    if int(opcion) == 2:
                        dia = input(f'Para la fecha: \n- Ingrese día de dos digitos:')
                        while dia.isnumeric() is False or len(dia) != 2:
                            dia = input('Incorrecto, pruebe nuevamente:')
                        while not 1 <= int(dia) <= 31:
                            dia = input('Incorrecto, pruebe nuevamente:')
                        mes = input('- Ingrese mes de dos digitos:')
                        while mes.isnumeric() is False or len(mes) != 2:
                            mes = input('Incorrecto, pruebe nuevamente:')
                        while not 1 <= int(mes) <= 12:
                            mes = input('Incorrecto, pruebe nuevamente:')
                        anio = input('- Ingrese año de 4 digitos:')
                        while anio.isnumeric() is False or len(anio) != 4:
                            anio = input('Incorrecto, pruebe nuevamente:')
                        valor = f'{dia}/{mes}/{anio}'
                    else:
                        valor = input('Ingrese nuevo valor: ')

                    if int(opcion) == 4:
                        valor = valor.capitalize()
                    elif int(opcion) == 5:
                        # Remueve tildes para provincias
                        valor = unicodedata.normalize("NFKD", valor).encode("ascii", "ignore").decode("ascii")
                    elif int(opcion) == 6:
                        while valor != '1334' or valor != '568':
                            valor = input('Ingrese codigo correcto 1334/568:')
                    elif int(opcion) == 7:
                        while valor.capitalize() not in contadores_botellas.keys():
                            valor = input('Color incorrecto o mal escrito, pruebe nuevamente:')
                        valor = valor.lower()
                    elif int(opcion) == 9:
                        valor = valor + '\n'
                    linea[int(opcion) - 1] = valor
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
                elif i == 'Fecha':
                    dia = input(f'Para la fecha: \n- Ingrese día de dos digitos:')
                    while dia.isnumeric() is False or len(dia) != 2:
                        dia = input('Incorrecto, pruebe nuevamente:')
                    while not 1 <= int(dia) <= 31:
                        dia = input('Incorrecto, pruebe nuevamente:')
                    mes = input('- Ingrese mes de dos digitos:')
                    while mes.isnumeric() is False or len(mes) != 2:
                        mes = input('Incorrecto, pruebe nuevamente:')
                    while not 1 <= int(mes) <= 12:
                        mes = input('Incorrecto, pruebe nuevamente:')
                    anio = input('- Ingrese año de 4 digitos:')
                    while anio.isnumeric() is False or len(anio) != 4:
                        anio = input('Incorrecto, pruebe nuevamente:')
                    valor = f'{dia}/{mes}/{anio}'
                    linea.append(valor)
                elif i == 'Provincia':
                    valor = input(f'Ingrese {i}: ')
                    # Remueve tildes
                    valor = unicodedata.normalize("NFKD", valor).encode("ascii", "ignore").decode("ascii")
                    linea.append(valor)
                elif i == 'Ciudad':
                    valor = input(f'Ingrese {i}: ')
                    valor = valor.capitalize()
                    linea.append(valor)
                elif i == 'Cod. Artículo':
                    valor = input(f'Ingrese {i}\nPara botellas 1334 o para vasos 568:')
                    while valor != '1334' or valor != '568':
                        valor = input('Ingrese codigo correcto 1334/568:')
                elif i == 'Color':
                    valor = input(f'Ingrese {i}: ')
                    # Contadores_botellas tiene todos los colores, no hace falta chequear en vasos
                    while valor.capitalize() not in contadores_botellas.keys():
                        valor = input(f'Color incorrecto o mal escrito, pruebe nuevamente: ')
                    valor = valor.lower()
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
                # Saltea el pedido a borrar
                if registro != int(num_pedido):
                    lineas_nuevo_archivo.append(linea)
            archivo_pedidos.close()

            archivo_pedidos_nuevo = open(f'{dir}\pedidos.csv', 'w', encoding="UTF-8")
            archivo_pedidos_nuevo.writelines(lineas_nuevo_archivo)
            archivo_pedidos_nuevo.close()
        iniciar = input('\n\n1: Continuar en ABM\n2: Volver al MENU principal\nElija opcion 1/2:')
        while iniciar.isnumeric() is False or int(iniciar) not in (1, 2):
            accion: str = input('Ingrese una opcion valida: ')

    return dir

def distancia_ciudades(ciudad1: str, ciudad2: str) -> float:
    '''Toma dos ciudades como parámetros y devuelve la distancia en kilometros como float.'''
    ctx = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ctx
    geolocator = Nominatim(user_agent='ivan')

    ciudad1 = ciudad1 + ', Argentina'
    ciudad2 = ciudad2 + ', Argentina'

    nombre1 = geolocator.geocode(ciudad1)
    nombre2 = geolocator.geocode(ciudad2)

    ubicacion1 = ((nombre1.latitude, nombre1.longitude))
    ubicacion2 = ((nombre2.latitude, nombre2.longitude))

    distancia = float(distance.distance(ubicacion1, ubicacion2).km)

    return distancia

def recorrido(zona: list, palabra: str, dir: str, imprimir: str) -> list:
    '''Toma la lista para la zona correspondiente, la palabra norte/centro/sur, direccion de archivo e
    imprimir como string de si/no ya que esta funcion tambien es usada por procesado_pedidos()
    para corroborar distancia óptima y no quiero que haga prints.
    Devuelve un listado de las ciudades ordenadas por recorrido mas óptimo para usarse en la funcion de
    procesado de pedidos'''

    # Listado para el procesado de pedidos
    procesado_pedidos_lista: list = []

    zona_pedidos_ciudades: dict = {}

    archivo_pedidos = open(f'{dir}\pedidos.csv', 'r', encoding="UTF-8")

    # Lee linea a linea el archivo pedidos.csv para obtener los pedidos de la zona, guarda ciudad y provincia
    for registro, linea in enumerate(archivo_pedidos):
        linea = linea.split(',')
        if linea[4].lower() in zona and linea[3].lower() != 'caba':
            zona_pedidos_ciudades[linea[3].lower()] = linea[4].lower()

    if not bool(zona_pedidos_ciudades.keys()):
        if imprimir == 'si':
            print(f'No hay pedidos para la zona {palabra}')


    else:
        # Calcula menor distancia entre Planta de Campana y ciudades de zona.
        distancia_menor: float = 1000000000000.0
        for i in zona_pedidos_ciudades.keys():
            distancia: float = distancia_ciudades('Campana', i)
            if distancia < distancia_menor:
                distancia_menor = distancia
                ciudad_cercana: str = i
        if imprimir == 'si':
            print(f'El recorrido mas óptimo va desde la planta en Campana hacia {zona_pedidos_ciudades[ciudad_cercana]}'
                  f': {ciudad_cercana}')
        procesado_pedidos_lista.append(ciudad_cercana)

        # Calcula cual es la ciudad mas cercana a la anterior

        ciudades_descarte: list = []
        for x in range(0, len(zona_pedidos_ciudades.keys()) - 1):
            distancia_menor: float = 1000000000000.0

            for i in zona_pedidos_ciudades.keys():
                if ciudad_cercana != i and i not in ciudades_descarte:
                    distancia: float = distancia_ciudades(ciudad_cercana, i)
                    if distancia < distancia_menor:
                        distancia_menor = distancia
                        ciudad_cercana2: str = i

            ciudades_descarte.append(ciudad_cercana)
            if imprimir == 'si':
                print(f'Desde {zona_pedidos_ciudades[ciudad_cercana]}: {ciudad_cercana} hacia '
                    f'{zona_pedidos_ciudades[ciudad_cercana2]}: {ciudad_cercana2}')
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


def procesado_pedidos(zona_norte: list, zona_centro: list, zona_sur: list, zona_caba: list, dir: str,
                      utilitario_asignado: int, contadores_botellas: dict,
                      contadores_vasos: dict, contador: int, utilitarios: dict) -> str:
    '''Toma las listas de zonas, direccion de archivo, la palabra norte/centro/sur, y el
    numero de utilitario ya usado para no tenerlo en cuenta en la próxima corrida.
    Tambien necesita los contadores para procesar con el stock. Una variable contador para solo ejecutarse 4 veces
     -1 vez por zona- y el diccionario utilitarios.
    Devuelve la direccion del archivo'''

    utilitarios.pop(utilitario_asignado, None)
    articulos: dict = {1334: [0.450, 0], 568: [0.350, 0]}  # num_art: [kilos, cantidad]

    if contador < 4:
        if contador == 0:
            zona: list = zona_norte
            palabra: str = 'Norte'
        elif contador == 1:
            zona: list = zona_centro
            palabra: str = 'Centro'
        elif contador == 2:
            zona: list = zona_sur
            palabra: str = 'Sur'
        elif contador == 3:
            zona: list = zona_caba
            palabra: str = 'CABA'

        ciudades_pedidos: list = []
        peso_final: int = 0
        peso_referencia: int = 10000000
        lineas_si_no: dict = {'si': [], 'no': []}
        archivo_pedidos = open(f'{dir}\pedidos.csv', 'r', encoding="UTF-8")

        # Lee linea a linea el archivo pedidos.csv para obtener los pedidos de zona
        for registro, linea in enumerate(archivo_pedidos):
            linea = linea.split(',')
            stock_disponible: str = 'no'  # determina si hay stock para el pedido actual
            if linea[4].lower() in zona:

                if int(linea[5]) == 1334:
                    # Modifico cantidad de acuerdo al stock disponible
                    stock = contadores_botellas[linea[6].capitalize()]
                    if int(linea[7]) <= stock:
                        nuevo_stock = stock - int(linea[7])
                        contadores_botellas[linea[6].capitalize()] = nuevo_stock
                        stock_disponible: str = 'si'

                        nueva_cantidad: int = articulos[int(linea[5])][1] + int(linea[7])
                        peso_final = (articulos[1334][0] * nueva_cantidad) + (articulos[568][0] * articulos[568][1])


                elif int(linea[5]) == 568:
                    # Modifico cantidad de acuerdo al stock disponible
                    stock = contadores_vasos[linea[6].capitalize()]
                    if int(linea[7]) <= stock:
                        nuevo_stock = stock - int(linea[7])
                        contadores_vasos[linea[6].capitalize()] = nuevo_stock
                        stock_disponible: str = 'si'

                        nueva_cantidad: int = articulos[int(linea[5])][1] + int(linea[7])
                        peso_final = (articulos[1334][0] * articulos[1334][1]) + (articulos[568][0] * nueva_cantidad)


                if peso_final <= max(utilitarios.values()) and stock_disponible == 'si':
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
                elif peso_final > max(utilitarios.values()) or stock_disponible == 'no':
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

        if not os.path.isfile(f'{dir}\salida.txt') and utilitario_asignado != 0 and peso_final > 0:
            archivo_salida = open(f'{dir}\salida.txt', 'w', encoding="UTF-8")
            archivo_salida.write(f'Zona {palabra}\nUtilitario 00{utilitario_asignado}\n{int(peso_final)} kg')
            archivo_salida.write(f'\nRecorrido: {mostrar_ciudades}')
            archivo_salida.close()
        elif os.path.isfile(f'{dir}\salida.txt') and utilitario_asignado != 0 and peso_final > 0:
            archivo_salida = open(f'{dir}\salida.txt', 'a', encoding="UTF-8")
            archivo_salida.write(f'\nZona {palabra}\nUtilitario 00{utilitario_asignado}\n{int(peso_final)} kg')
            if palabra != 'CABA':
                archivo_salida.write(f'\nRecorrido: {mostrar_ciudades}')
            elif palabra == 'CABA':
                archivo_salida.write(f'\nRecorrido: CABA')
            archivo_salida.close()

        return procesado_pedidos(zona_norte, zona_centro, zona_sur, zona_caba, dir, utilitario_asignado,
                                 contadores_botellas, contadores_vasos, contador + 1, utilitarios)
    else:
        return dir

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


def normaliza_pedidos(dir: str, contadores_botellas: dict, contadores_vasos: dict):
    '''Toma la direccion del archivo para poder modificar datos que puedan estar incorrectos en pedidos.csv y
    romper el programa. Utiliza los contadores para corroborar que los colores sean validos.
    A su vez elimina archivos pedidos_realizados y salida.txt de corridas previas para no tener informacion vieja'''
    archivo_pedidos = open(f'{dir}\pedidos.csv', 'r', encoding="UTF-8")
    lineas_guardar: list = []
    # Lee linea a linea el archivo pedidos.csv
    for registro, linea in enumerate(archivo_pedidos):
        if registro != 0 and linea != '\n':
            linea = linea.split(',')
            # Chequea colores
            if linea[5] == '1334' and linea[6].capitalize() not in contadores_botellas.keys():
                print(f'\n ALERTA\nEn su archivo de pedidos, en la linea {registro + 1} el color es incorrecto.')
                nuevo_color = input(f'El color actual es {linea[6]} en una botella, por favor ingrese aquí un color valido:')
                while nuevo_color.capitalize() not in contadores_botellas.keys():
                    nuevo_color = input('Ingrese color correcto:')
                linea[6] = nuevo_color
            elif linea[5] == '568' and linea[6].capitalize() not in contadores_vasos.keys():
                print(f'\n ALERTA\nEn su archivo de pedidos, en la linea {registro + 1} el color es incorrecto.')
                nuevo_color = input(
                    f'El color actual es {linea[6]} en un vaso, por favor ingrese aquí un color valido:')
                while nuevo_color.capitalize() not in contadores_vasos.keys():
                    nuevo_color = input('Ingrese color correcto:')
                linea[6] = nuevo_color
            # Quita tildes en provincias
            linea[4] = unicodedata.normalize("NFKD", linea[4]).encode("ascii", "ignore").decode("ascii")
            # Convierte colores en minuscula
            linea[6] = linea[6].lower()
            # Capitaliza ciudades
            linea[3] = linea[3].capitalize()
            linea = ','.join(linea)
            lineas_guardar.append(linea)

        elif registro == 0:
            lineas_guardar.append(linea)

    lineas_guardar[len(lineas_guardar) - 1] = lineas_guardar[len(lineas_guardar) - 1].rstrip('\n')
    archivo_pedidos.close()

    # Guarda cambios
    archivo_pedidos = open(f'{dir}\pedidos.csv', 'w', encoding="UTF-8")
    archivo_pedidos.writelines(lineas_guardar)
    archivo_pedidos.close()
    # Borra archivo de salida y pedidos_realizados viejos
    if os.path.isfile(f'{dir}\pedidos_realizados.csv'):
        os.remove(f'{dir}\pedidos_realizados.csv')
    if os.path.isfile(f'{dir}\salida.txt'):
        os.remove(f'{dir}\salida.txt')


# Martín
def crear_lista_pedidos_entregados(listado_pedidos: list) -> list:
    #Pre: Recibe la lista con TODOS los pedidos.
    #Post: Entrega una nueva lista solo con los pedidos que fueron entregados.
    lista_entregados: list = []  # lista vacia
    for sublista in listado_pedidos:  # recorro sublista
        if sublista[9] == "si":
            lista_entregados.append(sublista)
    return lista_entregados


def crear_lista_pedidos_no_entregados(listado_pedidos: list) -> list:
    #Pre: Recibe la lista con TODOS los pedidos.
    #Post: Entrega una nueva lista solo con los pedidos que NO fueron entregados.
    lista_no_entregados: list = []  # lista vacia
    for sublista in listado_pedidos:  # recorro sublista
        if sublista[9] == "no":
            lista_no_entregados.append(sublista)
    return lista_no_entregados


def ordenar_pedidos(lista_entregados: list) -> list:
    #Pre: Recibe una lista un  con los pedidos entregados.
    #Post: Crea y devulve una lista con los pedidos ordenados por fecha.
    listado_pedidos_ordenado: list = []
    for item in lista_entregados:
        listado_pedidos_ordenado.append(item)
    listado_pedidos_ordenado = ordenamiento_burbuja(listado_pedidos_ordenado)
    return listado_pedidos_ordenado


def ordenamiento_burbuja(listado_pedidos_ordenado) -> list:
    #Pre: Recibe una lista con los pedidos entregados.
    #Post: Devuelve una lista con los pedidos ordenados por fecha.
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
                intercambiar(listado_pedidos_ordenado, i)
                orden = False

            elif anio == anioSig and mes > mesSig:
                intercambiar(listado_pedidos_ordenado, i)
                orden = False

            elif anio == anioSig and mes == mesSig and dia > diaSig:
                intercambiar(listado_pedidos_ordenado, i)
                orden = False

    return listado_pedidos_ordenado


def intercambiar(listado_pedidos_ordenado, index) -> None:
    #Pre: Recibe una lista y una posición dentro de la lista.
    #Post: Devuelve una nueva posición para el numero dentro de la lista. Es parte del proceso de ordenamiento de la lista.
    aux: list = listado_pedidos_ordenado[index]
    listado_pedidos_ordenado[index] = listado_pedidos_ordenado[index + 1]
    listado_pedidos_ordenado[index + 1] = aux


def pedidos_realizados(listado_pedidos_ordenado: list) -> None:
    # Pre: Recibe una lista con los pedidos realizados ordenados por fecha.
    # Post: Muestra los pedidos realizados, en orden de antiguedad y la cantidad de pedidos realizados en numero.
    numero_pedidos_entregados: int = 0
    numero_de_pedido: int = 0
    for i in range(len(listado_pedidos_ordenado)):
        if listado_pedidos_ordenado[i][0] != numero_de_pedido:
            numero_pedidos_entregados += 1
            numero_de_pedido = listado_pedidos_ordenado[i][0]
   # Printea la cantidad de pedidos realizados.
    print(f"La cantidad de pedidos realizados es: {numero_pedidos_entregados}\n")
    print("A continuación se mostrará la lista por orden de antigüedad:\n")
    for i in range(len(listado_pedidos_ordenado)):
        print(f"Fecha: {listado_pedidos_ordenado[i][1]}, numero de pedido: {listado_pedidos_ordenado[i][0]}, "
              f"cliente: {listado_pedidos_ordenado[i][2]}, ciudad: {listado_pedidos_ordenado[i][3]}, "
              f"provincia: {listado_pedidos_ordenado[i][4]}, código de articulo: {listado_pedidos_ordenado[i][5]}, "
              f"color: {listado_pedidos_ordenado[i][6]}, cantidad: {listado_pedidos_ordenado[i][7]}, "
              f"descuento: {listado_pedidos_ordenado[i][8]}\n")

def pedidos_rosario(lista_pedidos_entregados: list) -> None:
    # Pre: recibe los pedidos entregados.
    # Post: filtra los que tienen como ciudad rosario, los muestra y los valoriza.
    pedidos_rosario: list = []  # lista vacia
    precio_botella: int = 15
    precio_vaso: int = 8
    dicc_valores_por_pedido: dict = {}
    for i in range(len(lista_pedidos_entregados)):  # recorro dicc
        if lista_pedidos_entregados[i][3] == "Rosario":  # si la ciudad es Rosario
            pedidos_rosario.append(lista_pedidos_entregados[i])  # Lo agrega a la lista vacia
    for i in range(len(pedidos_rosario)):
        valor_producto: float = 0
        if pedidos_rosario[i][5] == 1334:  # si es una botella
            try:  # si aplica descuento
                valor_producto += precio_botella * pedidos_rosario[i][7] - (15 * pedidos_rosario[i][7]) / \
                                  pedidos_rosario[i][8]  # valor_producto * cantidad de producto pedido - descuento
                pedidos_rosario[i].append(valor_producto)
            except ZeroDivisionError:  # si no aplica descuento
                valor_producto += precio_botella * pedidos_rosario[i][7]
                pedidos_rosario[i].append(valor_producto)
        elif pedidos_rosario[i][5] == 568:  # si es un vaso
            try:
                valor_producto += precio_vaso * pedidos_rosario[i][7] - (15 * pedidos_rosario[i][7]) / \
                                  pedidos_rosario[i][8]
                pedidos_rosario[i].append(valor_producto)
            except ZeroDivisionError:
                valor_producto += precio_botella * pedidos_rosario[i][7]
                pedidos_rosario[i].append(valor_producto)
    valor_pedido_lista: list = valores_por_pedido(pedidos_rosario)
    for i in range(len(valor_pedido_lista)):
        dicc_valores_por_pedido.update({i + 1: valor_pedido_lista[i]})
    if pedidos_rosario == []:
        print("No hay pedidos que fueron entregados en la ciudad de Rosario.")
    elif pedidos_rosario != []:
        print(f"A continuación se mostrarán los pedidos que fueron entregados en la ciudad de Rosario:\n {pedidos_rosario}")
        print(f"Se mostrará el valor en dolares de cada pedido entregado con el siguiente formato: Numero de pedido: valor\n{dicc_valores_por_pedido}")

def valores_por_pedido(pedidos_rosario: list) -> list:
    #Pre: Recibe una lista con todos los pedidos que fueron entregados en la ciudad de Rosario.
    #Post: Devuelve la misma lista con el agregado en cada pedido del valor en dolares.
    valor_pedido_lista: list = []
    valor_pedido: float = 0
    numero_de_pedido: int = 1
    for i in range(len(pedidos_rosario)):
        if pedidos_rosario[i][0] == numero_de_pedido:
            valor_pedido += pedidos_rosario[i][10]
        else:
            valor_pedido_lista.append(valor_pedido)
            valor_pedido = 0
            valor_pedido += pedidos_rosario[i][10]
            numero_de_pedido = pedidos_rosario[i][0]
    valor_pedido_lista.append(valor_pedido)
    return valor_pedido_lista


def cantidad_de_productos_pedidos(listado_pedidos: list, productos: dict) -> dict:
    # Pre: Recibe la lista con los todos los pedidos y un diccionario vacio.
    # Post: Devuelve el mismo diccionario con la información de cuantos productos fueron pedidos de cada color, en un formato de: diccionario dentro de diccionario.
    cantidad_botellas: dict = {"verde": 0, "rojo": 0, "azul": 0, "negro": 0, "amarillo": 0}
    cantidad_vasos: dict = {"negro": 0, "azul": 0, }
    for i in range(len(listado_pedidos)):
        if listado_pedidos[i][5] == 1334:
            if listado_pedidos[i][6] in cantidad_botellas.keys():
                cantidad_botellas[listado_pedidos[i][6]] += listado_pedidos[i][7]
        elif listado_pedidos[i][5] == 568:
            if listado_pedidos[i][6] in cantidad_vasos.keys():
                cantidad_vasos[listado_pedidos[i][6]] += listado_pedidos[i][7]
    productos.update({"botella": cantidad_botellas})
    productos.update({"vaso": cantidad_vasos})
    return productos


def cantidad_de_productos_entregados(lista_pedidos_entregados: list, productos_entregados: dict) -> dict:
    # Pre:  Recibe la lista con los todos los pedidos entregados y un diccionario vacio.
    # Post: Devuelve el mismo diccionario con la información de cuantos productos fueron entregados de cada color, en un formato de: diccionario dentro de diccionario.
    cantidad_botellas_entregadas: dict = {"verde": 0, "rojo": 0, "azul": 0, "negro": 0, "amarillo": 0}
    cantidad_vasos_entregados: dict = {"negro": 0, "azul": 0, }
    for i in range(len(lista_pedidos_entregados)):
        if lista_pedidos_entregados[i][5] == 1334:
            if lista_pedidos_entregados[i][6] in cantidad_botellas_entregadas.keys():
                cantidad_botellas_entregadas[lista_pedidos_entregados[i][6]] += lista_pedidos_entregados[i][7]
        elif lista_pedidos_entregados[i][5] == 568:
            if lista_pedidos_entregados[i][6] in cantidad_vasos_entregados.keys():
                cantidad_vasos_entregados[lista_pedidos_entregados[i][6]] += lista_pedidos_entregados[i][7]
    productos_entregados.update({"botella": cantidad_botellas_entregadas})
    productos_entregados.update({"vaso": cantidad_vasos_entregados})
    return productos_entregados


def articulo_mas_pedido(productos: dict, productos_entregados: dict) -> None:
    # Pre: Recibe el diccionario de productos y productos entregados.
    # Post: Muestra cual es el articulo mas pedido y cuantos fueron entregados.
    producto_mas_pedido: str = ""  # inicializo variables
    color: str = ""
    cantidad_producto_mas_pedido: int = 0
    if productos["botella"]["verde"] > cantidad_producto_mas_pedido:  # si tiene la mayor cantidad de pedidos
        cantidad_producto_mas_pedido = productos["botella"]["verde"]  # lo guardo en esta variable
        producto_mas_pedido = "botella"
        color = "verde"
    elif productos["botella"]["rojo"] > cantidad_producto_mas_pedido:  # repito proceso con cad producto
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

    if color!= "":
        print(
            f"El producto más pedido es: {producto_mas_pedido} de color {color} con {cantidad_producto_mas_pedido} unidades.\n De esa cantidad, {productos_entregados[producto_mas_pedido][color]} fueron entregados.")


def volver_menu():
    #Pre: No hay condiciones previas.
    #Post: Muestra un mensaje avisando que se volverá al menú. 
    input('Presione ENTER para volver al menu: ')


def validar_archivo() -> str:
    print('Antes de iniciar, por favor, ingrese la ruta en donde se encuentra su archivo de pedidos usando " \ "')
    print('Ejemplo: D:\Documentos\Python Proyectos\prueba')

    direccion_archivo = input('')
    while not os.path.isdir(direccion_archivo) or not os.path.isfile(f'{direccion_archivo}\pedidos.csv'):
        direccion_archivo = input('Directorio invalido o archivo no encontrado, pruebe nuevamente: ')

    return direccion_archivo


def determina_recorrido(zona_norte: list, zona_centro: list, zona_sur: list, direccion_archivo: str) -> None:
    '''Tomas las zonas, y direccion de archivo para ejecutar los recorridos'''
    iniciar: str = '1'
    while int(iniciar) == 1:
        print('Zonas:\n1: Norte\n2: Centro\n3: Sur')

        opcion = input('Para que zona desea ver el recorrido? 1/2/3: ')

        while opcion.isnumeric() is False or int(opcion) not in (1, 2, 3):
            opcion: str = input('Ingrese una opcion valida: ')
        print('\nAguarde, calculando el recorrido mas óptimo...')

        if int(opcion) == 1:

            recorrido(zona_norte, 'norte', direccion_archivo, 'si')

        elif int(opcion) == 2:

            recorrido(zona_centro, 'centro', direccion_archivo, 'si')

        else:
            recorrido(zona_sur, 'sur', direccion_archivo, 'si')

        iniciar = input('\n\n1: Continuar viendo recorridos\n2: Volver al MENU principal\nElija opcion 1/2:')
        while iniciar.isnumeric() is False or int(iniciar) not in (1, 2):
            accion: str = input('Ingrese una opcion valida: ')

def procesar_pedido(zona_norte: list, zona_centro: list, zona_sur: list, direccion_archivo: str,
                    contadores_botellas: dict, contadores_vasos: dict) -> list:
    '''Toma las zonas para usarlas en la funcion procesado_pedidos, tambien los contadores para armar pedidos de acuerdo
     al stock y devuelve el listado de pedidos con flag de entregado si/no'''

    listado_pedidos: list = []
    zona_caba: list = ['buenos aires']
    utilitarios: dict = {1: 600, 2: 1000, 3: 500, 4: 2000}  # num_utilitario: kilos

    print('\nAguarde, procesando los pedidos...')

    procesado_pedidos(zona_norte, zona_centro, zona_sur, zona_caba, direccion_archivo, 0,
                      contadores_botellas, contadores_vasos, 0, utilitarios)

    listado_pedidos = crea_lista_pedidos(direccion_archivo)

    if os.path.isfile(f'{direccion_archivo}\salida.txt'):
        print(f'Se han procesado los pedidos. Guardado en:\n{direccion_archivo}\salida.txt')
    elif not os.path.isfile(f'{direccion_archivo}\salida.txt'):
        print('No se envía ningun pedido por falta de stock o por ser demasiado peso para los utilitarios')

    return listado_pedidos

def pedidos_completados(listado_pedidos:list , direccion_archivo:str)->None:

    listado_pedidos_ordenado:list

    if not os.path.isfile(f'{direccion_archivo}\pedidos_realizados.csv'):
        print(
            "Todavia el programa no tiene la información de que pedidos fueron entregados. En el menú, elija la opción \"3\" para actualizar los pedidos entregados.")
    elif os.path.isfile(f'{direccion_archivo}\pedidos_realizados.csv'):
        listado_pedidos_ordenado= ordenar_pedidos(listado_pedidos)
        pedidos_realizados(listado_pedidos_ordenado)


def valorizacion_pedidos_rosario(lista_pedidos_entregados:list, direccion_archivo:str )->None:

    if not os.path.isfile(f'{direccion_archivo}\pedidos_realizados.csv'):
        print(
            "Todavia el programa no tiene la información de que pedidos fueron entregados. En el menú, elija la opción \"3\" para actualizar los pedidos entregados.")
    elif os.path.isfile(f'{direccion_archivo}\pedidos_realizados.csv'):
        pedidos_rosario(lista_pedidos_entregados)

def articulos_mas_pedidos(direccion_archivo:str,lista_pedidos_entregados:list ,productos_entregados:dict , productos:dict ,listado_pedidos:list  )->None:

    if not os.path.isfile(f'{direccion_archivo}\pedidos_realizados.csv'):
        print(
            "Todavia el programa no tiene la información de que pedidos fueron entregados. En el menú, elija la opción \"3\" para actualizar los pedidos entregados.")
    elif os.path.isfile(f'{direccion_archivo}\pedidos_realizados.csv'):
        cantidad_de_productos_pedidos(listado_pedidos, productos)
        cantidad_de_productos_entregados(lista_pedidos_entregados, productos_entregados)
        articulo_mas_pedido(productos, productos_entregados)


def imprimir_menu(zona_norte: list, zona_centro: list, zona_sur: list, direccion_archivo: str, productos: dict,
                  productos_entregados: dict, contadores_botellas: dict, contadores_vasos: dict):
    '''Pre: Recibe varios diccionarios y un string, entre esos son: Ubicaciones de distintas provincias dividias en zona 
    norte, central y sur; una dirección de archivos (string), y dos diccionarios vacios que se usarán en las funciones.
    Post: Muestra el menú y deja al usuario decidir que función quiere ejecutar mediante el uso de opciones numéricas. 
    Dependiendo la opción decidida, se mostrará la información correspondiente hasta que el usuario decida salir del menú.'''
    cerrar_menu:bool = False
    accion:str
    opcion:str
    lista_pedidos_no_entregados: list = []
    lista_pedidos_entregados: list = []
    listado_pedidos:list=[]

    while cerrar_menu == False:

        accion = input("""  Bienvenido al MENU

                    1.Alta - Baja - Modificacion de pedidos
                    2.Determinar un recorrido por zona
                    3.Procesar los pedidos
                    4.Listado de pedidos que fueron completados
                    5.Pedidos de Rosario con su valorización
                    6.Artículo más pedido y cuantos fueron entregados
                    7.salir
                   

                    Elija opcion escribiendo el numero correspondiente: """)


        while accion.isnumeric() is False or int(accion) not in (1, 2, 3, 4, 5, 6, 7):
            accion = input('Ingrese una opcion valida: ')

        if int(accion) == 1:

            direccion_archivo = ABM(direccion_archivo, contadores_botellas)
            normaliza_pedidos(direccion_archivo, contadores_botellas, contadores_vasos)

        elif int(accion) == 2:

            determina_recorrido(zona_norte, zona_centro, zona_sur, direccion_archivo)

        elif int(accion) == 3:

            listado_pedidos = procesar_pedido(zona_norte, zona_centro, zona_sur, direccion_archivo, contadores_botellas,
                                              contadores_vasos)
            lista_pedidos_entregados = crear_lista_pedidos_entregados(listado_pedidos)
            lista_pedidos_no_entregados = crear_lista_pedidos_no_entregados(listado_pedidos)
            volver_menu()

        elif int(accion) == 4:

            pedidos_completados(listado_pedidos, direccion_archivo)
            volver_menu()

        elif int(accion) == 5:

            valorizacion_pedidos_rosario(lista_pedidos_entregados,direccion_archivo)
            volver_menu()

        elif int(accion) == 6:
            articulos_mas_pedidos(direccion_archivo,lista_pedidos_entregados,productos_entregados,productos , listado_pedidos)
            volver_menu()

        else:
            print("Vuelva pronto ")
            cerrar_menu = True


def main():

    productos: dict = {}
    productos_entregados: dict = {}
    contadores_botellas: dict = {"Verde": 0, "Negro": 0, "Rojo": 0, "Azul": 0, "Amarillo": 0}
    contadores_vasos: dict = {"Negro": 0, "Azul": 0}

    zona_norte: list = ['catamarca', 'cordoba', 'chaco', 'corrientes', 'formosa', 'jujuy', 'la rioja', 'misiones',
                        'salta', 'santiago del estero', 'tucuman', 'entre rios', 'mendoza', 'san juan', 'san luis',
                        'santa fe', 'buenos aires']

    zona_centro: list = ['la pampa', 'neuquen']

    zona_sur: list = ['chubut', 'rio negro', 'santa cruz', 'tierra del fuego']


    folder: str = os.getcwd() + "\Lote0001"

    imagenes_carpeta(folder, contadores_botellas, contadores_vasos)
    direccion_archivo: str = validar_archivo()
    normaliza_pedidos(direccion_archivo, contadores_botellas, contadores_vasos)
    imprimir_menu(zona_norte, zona_centro, zona_sur, direccion_archivo, productos, productos_entregados,
                  contadores_botellas, contadores_vasos)
    cantidades_txt(contadores_botellas, contadores_vasos)


main()

