
#Datos a tener en cuenta:
#   para los pedidos, es conveniente una diccionario con el siguiente formato: {NdePedido, [fecha, cliente, ciudad, provincia, cod. articulo, color, cantidad, descuento,entregado]}
#   Realizar algun tipo de checkeo para saber que pedidos fueron entregados y cuales no, tambien saber el motivo.
#   Teniendo el punto anterior en cuenta, lo mejor seria dividir los pedidos en entregados y no entregados, de esta forma las funciones directamente agarran la lista/dict correspondiente sin tener que checkear repetidas veces que si se entrego cada pedido.

#Dudas:
#   Como checkear si un pedido es realizado o no, teniendo en cuenta que pedidos.csv no lo marca. Charlar con el grupo.
#   

import cv2
import os
import numpy as np

def checkeo_pedidos_entregados(listado_pedidos: dict) -> dict: #Solución temporal hasta saber como checkear si un pedido fue entregado
    pedidos_entregados: dict = listado_pedidos.copy() #copio el dict original con TODOS los pedidos
    for i in listado_pedidos: #recorro dict
        if listado_pedidos[i[8]] == "no": #si el pedido no fue entregado, lo borro del dict nuevo que hice. Por lo tanto, te quedan los pedidos que fueron entregados.
            pedidos_entregados.pop(i)
    return pedidos_entregados

def checkeo_pedidos_no_entregados(listado_pedidos: dict) -> dict:
    pedidos_no_entregados: dict = listado_pedidos.copy() #copio dict original con TODOS los pedidos
    for i in listado_pedidos: #recorro dict
        if listado_pedidos[i[8]] == "si": #si el pedido fue entregado, lo borro del dict nuevo que hice. Por lo tanto, te quedan los pedidos que NO fueron entregados.
            pedidos_no_entregados.pop(i)
    return pedidos_no_entregados

def pedidos_realizados(pedidos_entregados: dict) -> None:
    #Pre: recibe todos los pedidos realizados (todavia no se en que formato, es probable que en dict)"
    #Post: Printea los pedidos realizados, en orden de antiguedad y devuelve la cantidad de pedidos realizados en numero. 
    numero_pedidos_entregados: int = 0 #Cantiad de pedidos inicializado
    for i in pedidos_entregados: #recorre lista
        numero_pedidos_entregados += 1 #Cuenta los pedidos realizados 
    sorted(pedidos_entregados, key= lambda fecha: pedidos_entregados[0]) #checkear este sorted
    
    print() # printea la lista por orden de antigüedad.
    print(numero_pedidos_entregados) #printea la cantidad de pedidos realizados.
    return

def pedidos_rosario():
    #Pre: recibir los pedidos 
    #Post: filtrea los que tienen como ciudad rosario, los muestra y los valoriza

    return


def cantidad_de_productos_pedidos():
    #Pre: recibe los pedidos
    #Post: cuenta cada pedido en una lista, mostrando la cantidad de cada producto vendido
    return

def articulo_mas_pedido():
    #Pre: Recibe la lista de cantidad_de_productos_pedidos y deberia recibir otra informacion mas que checkee cuantos fueron entregados.
    #Post: muestra cual es el articulo mas pedido y cuantos fueron entregados.
    return

def imagenes_carpeta(carpeta):
    #Pre: recibe la direccion de una carpeta
    #Post: recorre y carga los archivos dentro de la carpeta recibida uno por uno
    for filename in os.listdir(carpeta):
        img = cv2.imread(os.path.join(carpeta,filename))
        cv2.imshow("escaner", img)
        cv2.waitKey(0)

def main():

    listado_pedidos: dict = {1:[1/11/2021, "Juan Alvarez", "Villa María", "Córdoba", 1334, "Azul", 36, 5, "si"],#{NdePedido: [fecha, cliente, ciudad, provincia, cod. articulo, color, cantidad, descuento, entregado]
    2:[2/11/2021, "Carlos Rodriguez", "Parana", "Santa Fe", 1334, "Negro", 5, 0, "no"]}
    
    pedidos_entregados: dict = checkeo_pedidos_entregados(listado_pedidos)
    pedidos_no_entregados: dict= checkeo_pedidos_no_entregados(listado_pedidos)
    print(pedidos_entregados)
    print(pedidos_no_entregados)
    return


main()