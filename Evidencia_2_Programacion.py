from collections import namedtuple
import csv
import pandas as pd

def ingresoDatos(x,y):
    global descripcionI,cantidad,precio,Fecha
    descripcionI = diccionario_ventas[x][y].descripcion
    cantidad = diccionario_ventas[x][y].cantidad_pzas
    precio = diccionario_ventas[x][y].precio_venta
    Fecha = diccionario_ventas[x][y].fecha

Datos = namedtuple("Ventas",("descripcion", "cantidad_pzas","precio_venta", "fecha"))
lista_ventas = []
diccionario_ventas = {}

folioNuevo = 0
try:
    with open("datosprueba.csv","r", newline = "") as archivo:
        
        lector = csv.reader(archivo)
        next(lector)
        contador = 0
        
        for folio, descripcion, CantidadPzas, PrecioVenta, FechaVenta in lector:
            if contador == 0:
                folioNuevo = int(folio)
                contador =+1 
                
            if int(folio) == folioNuevo:
                ventas = Datos(descripcion,CantidadPzas, PrecioVenta, FechaVenta)
                lista_ventas.append(ventas)
                
            else:
                lista_ventas = []
                ventas = Datos(descripcion,CantidadPzas, PrecioVenta, FechaVenta)
                lista_ventas.append(ventas)
                folioNuevo = int(folio)
                contador =-1
                
            diccionario_ventas[int(folio)] = lista_ventas
except Exception:
    print("Primer Diccionario")

while True:
    print("***********************************************")
    print("\tLlantas Michelin")
    print("")
    print("1) Registrar una venta")
    print("2) Busqueda especifica de una venta")
    print("3) Guardar datos a CSV")
    print("4) Busqueda por fecha")
    print("5) Salir")
    print("\nPuede ingresar la opcion mediante \nel teclado numerico")
    respuesta = int(input("Elija una opción: "))
    
    if respuesta == 1:
        lista_ventas = []
        while True:
            folio = int(input('\nIngrese el folio de la venta: '))
            if folio in diccionario_ventas.keys():
                print('Esta clave ya existe, porfavor ingresa otra')
            else:
                fecha_venta = input('Ingrese la fecha de venta: ')
                break
            
        while True:
            # Insercion de datos
            descripcion = input('Ingrese la descripcion de la llanta: ')
            cantidad_pzas = input('Ingrese la cantidad de piezas a comprar: ')
            precio_venta = input('Ingrese el precio unitario de cada pieza: ')
            
            print("-----------------------------------------------------------\n")
            # Lista
            ventas = Datos(descripcion,cantidad_pzas, precio_venta, fecha_venta)
            lista_ventas.append(ventas)
            
            # Diccionario
            diccionario_ventas[folio] = lista_ventas
            
            # Seguir agregando
            respuesta1 = int(input('¿Quieres seguir agregando productos?\n\t 1: Si\n\t 2: No\n\t'))
            
            # En caso de que no quiera seguir agregando
            if (respuesta1 != 1):
                tamañoLista = 0
                total_ventas = 0
                while tamañoLista < len(diccionario_ventas[folio]):
                    total_ventas = (int(diccionario_ventas[folio][tamañoLista].precio_venta) * int(diccionario_ventas[folio][tamañoLista].cantidad_pzas)) + total_ventas
                    tamañoLista = tamañoLista + 1
                print(f"Total de las ventas: {total_ventas}")
                print(f"El iva aplicable es de: {total_ventas * .16}")
                print(f"El total con iva aplicado es de: {round(total_ventas*1.16, 2)}")
                break
                
    elif respuesta == 2:
        #Insercion de la busqueda
        busqueda = int(input("Ingresa la clave a buscar: "))
        tamañoLista = 0
        total_ventas = 0
        
        #Iteracion de la busqueda
        if busqueda in diccionario_ventas.keys():
            print(f"\nFolio de la venta: {busqueda}")
            print("*"*90)
            print("{0:<10} {1:<20} {2:<20} {3:<20} {4:<20}".format("Folio","Descripcion","Canitdad","Precio Unitario","Fecha"))
            while tamañoLista < len(diccionario_ventas[busqueda]):
                ingresoDatos(busqueda, tamañoLista)
                print("{0:<10} {1:<20} {2:<20} {3:<20} {4:<20}".format(busqueda,descripcionI,cantidad,precio,Fecha))
                total_ventas = (int(diccionario_ventas[busqueda][tamañoLista].precio_venta) * int(diccionario_ventas[busqueda][tamañoLista].cantidad_pzas)) + total_ventas
                tamañoLista = tamañoLista + 1
            print(f"Total de las ventas: {total_ventas}")
            print(f"El iva aplicable es de: {total_ventas * .16}")
            print(f"El total con iva aplicado es de: {round(total_ventas*1.16, 2)}")
            print("**********************************************\n")
        else:
            print("La clave no esta registrada")
                            
    elif respuesta == 3:
        
        with open("datosprueba.csv","w",newline="") as archivo:
            total_ventas = 0
            grabador = csv.writer(archivo)
            grabador.writerow(("Folio","Descripcion","CanitdadPzas","PrecioVenta","FechaVenta"))
            
            for folio , Lista  in diccionario_ventas.items():
                tamañoLista = 0
                while tamañoLista < len(Lista):
                    # Asignacion de valores
                    ingresoDatos(folio, tamañoLista)
                    #Grabado en el CSV
                    grabador.writerows([[folio, descripcionI, cantidad, precio, Fecha]])
                    tamañoLista = tamañoLista + 1
            print("*"*20)
            print(f"\nCargado Exitosamente \n")
            print("*"*20)
    
    elif respuesta == 4:
        busqueda = input('\nIngrese la fecha a buscar: ')
        print("{0:<10} {1:<20} {2:<20} {3:<20} {4:<20}".format("Folio","Descripcion","Canitdad","Precio Unitario","Fecha"))
        total_ventas = 0
        for folio, lista in diccionario_ventas.items():
            tLista = 0
            while tLista < len(lista):
                if diccionario_ventas[folio][tLista].fecha == busqueda:
                    
                    ingresoDatos(folio, tLista)
                    print("{0:<10} {1:<20} {2:<20} {3:<20} {4:<20}".format(folio,descripcionI,cantidad,precio,Fecha))
                    total_ventas = (int(diccionario_ventas[folio][tLista].precio_venta) * int(diccionario_ventas[folio][tLista].cantidad_pzas)) + total_ventas
                
                tLista = tLista + 1
        print(f"Total de las ventas: {total_ventas}")
        print(f"El iva aplicable es de: {total_ventas * .16}")
        print(f"El total con iva aplicado es de: {round(total_ventas*1.16, 2)}")
              
    elif respuesta == 5:
        print("Finalizando")
        break