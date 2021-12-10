
# Datos a tener en cuenta:
#   para los pedidos, es conveniente una diccionario con el siguiente formato: {NdePedido, [fecha, cliente, ciudad, provincia, cod. articulo, color, cantidad, descuento,entregado]}
#   Realizar algun tipo de checkeo para saber que pedidos fueron entregados y cuales no, tambien saber el motivo.
#   Teniendo el punto anterior en cuenta, lo mejor seria dividir los pedidos en entregados y no entregados, de esta forma las funciones directamente agarran la lista/dict correspondiente sin tener que checkear repetidas veces que si se entrego cada pedido.

# Dudas:
#   Como checkear si un pedido es realizado o no, teniendo en cuenta que pedidos.csv no lo marca. Charlar con el grupo.
#

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


def checkeo_pedidos_entregados(
        listado_pedidos: dict) -> dict:  # Solución temporal hasta saber como checkear si un pedido fue entregado
    pedidos_entregados: dict = listado_pedidos.copy()  # copio el dict original con TODOS los pedidos
    for i in listado_pedidos:  # recorro dict
        if listado_pedidos[i[
            8]] == "no":  # si el pedido no fue entregado, lo borro del dict nuevo que hice. Por lo tanto, te quedan los pedidos que fueron entregados.
            pedidos_entregados.pop(i)
    return pedidos_entregados


def checkeo_pedidos_no_entregados(listado_pedidos: dict) -> dict:
    pedidos_no_entregados: dict = listado_pedidos.copy()  # copio dict original con TODOS los pedidos
    for i in listado_pedidos:  # recorro dict
        if listado_pedidos[i[
            8]] == "si":  # si el pedido fue entregado, lo borro del dict nuevo que hice. Por lo tanto, te quedan los pedidos que NO fueron entregados.
            pedidos_no_entregados.pop(i)
    return pedidos_no_entregados


def pedidos_realizados(pedidos_entregados: dict) -> None:
    # Pre: recibe todos los pedidos realizados (todavia no se en que formato, es probable que en dict)"
    # Post: Printea los pedidos realizados, en orden de antiguedad y devuelve la cantidad de pedidos realizados en numero.
    numero_pedidos_entregados: int = 0  # Cantiad de pedidos inicializado
    for i in pedidos_entregados:  # recorre lista
        numero_pedidos_entregados += 1  # Cuenta los pedidos realizados
    sorted(pedidos_entregados, key=lambda fecha: pedidos_entregados[0])  # checkear este sorted

    print()  # printea la lista por orden de antigüedad.
    print(numero_pedidos_entregados)  # printea la cantidad de pedidos realizados.
    return


def pedidos_rosario():
    # Pre: recibir los pedidos
    # Post: filtrea los que tienen como ciudad rosario, los muestra y los valoriza

    return


def cantidad_de_productos_pedidos():
    # Pre: recibe los pedidos
    # Post: cuenta cada pedido en una lista, mostrando la cantidad de cada producto vendido
    return


def articulo_mas_pedido():
    # Pre: Recibe la lista de cantidad_de_productos_pedidos y deberia recibir otra informacion mas que checkee cuantos fueron entregados.
    # Post: muestra cual es el articulo mas pedido y cuantos fueron entregados.
    return


def deteccion_colores(imagen):
    # Pre: la imagen tiene que poder mutar su color al rango hsv.
    # Post: recibe una imagen y verifica si hay alguno de los 5 colores preestablecidos.
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
    colores_rango = {
        "verde": ([40, 100, 100], [75, 255, 255]),
        "negro": ([0, 0, 0], [0, 0, 10]),
        "rojo": ([161, 155, 84], [179, 255, 255]),
        "azul": ([94, 80, 2], [126, 255, 255]),
        "amarillo": ([25, 100, 100], [30, 255, 255])}
    for nombre_color, (lower, upper) in colores_rango.items():
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)
        mask = cv2.inRange(hsv, lower, upper)
        resultado = cv2.bitwise_and(imagen, imagen, mask=mask)
        if mask.any():
            print(nombre_color)


def imagenes_carpeta(carpeta):
    # Pre: tiene que ingresar una direccion que lleve a una carpeta con archivos dentro.
    # Post: recorre y carga los archivos dentro de la carpeta recibida uno por uno.
    for filename in os.listdir(carpeta):
        img = cv2.imread(os.path.join(carpeta, filename))
        deteccion_colores(img)
        cv2.imshow("escaner", img)
        cv2.waitKey(0)


#Genesis---Deteccion Imagen 
import cv2
import numpy as np
import os


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


def images_folder(folder):
    # Pre: Recibe una carpeta con varios archivos
    # Pos: Recorre todos los archivos que estan en la carpeta e invocan las funciones  image_detect y deteccion_colores pasado como parametro la ruta

    for filename in os.listdir(folder):
        image_path = os.path.join(folder, filename)
        imagen_detectada = image_detect(image_path)

        if imagen_detectada == 'cup' or imagen_detectada == 'bottle':
            print(imagen_detectada)
        else:
            print("PROCESO DETENIDO, se reanuda en 1 minuto")

        while imagen_detectada == 'cup' or imagen_detectada == 'bottle':
            #deteccion_colores(image_path) # esto retorna el color



def main():
    listado_pedidos: dict = {1: [1 / 11 / 2021, "Juan Alvarez", "Villa María", "Córdoba", 1334, "Azul", 36, 5, "si"],
                             # {NdePedido: [fecha, cliente, ciudad, provincia, cod. articulo, color, cantidad, descuento, entregado]
                             2: [2 / 11 / 2021, "Carlos Rodriguez", "Parana", "Santa Fe", 1334, "Negro", 5, 0, "no"]}

    pedidos_entregados: dict = checkeo_pedidos_entregados(listado_pedidos)
    pedidos_no_entregados: dict = checkeo_pedidos_no_entregados(listado_pedidos)
    print(pedidos_entregados)
    print(pedidos_no_entregados)
    return

    # Ivan---------------
    # Variables para ABM
    pedir_ruta_abm: int = 0
    dir_abm: str = ''
    inicio_menu: int = 0

    while inicio_menu == 0:

        print('Bienvenido al MENU')
        print('1: Alta - Baja - Modificacion de pedidos')

        accion = input('Elija opcion escribiendo el numero correspondiente: ')
        while accion.isnumeric() is False or int(accion) not in (1, 2, 3, 4):
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
            volver_menu = input('Presione ENTER para volver al menu: ')


main()
