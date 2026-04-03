import os #Obtener nombre PC y limpiar consola
import json #Guardar y leer llaveros, Guardar mensajes y identidades
import socket #Conexion LAN entre las PCs
import threading #Recibir mensajes en segundo plano
import hashlib #Generar hashes para llaves, mensajes y firmas
import random #Generar numeros aleatorios
import time #Timestamp para la semilla polimorfica
import math #Calculos matematicos
import psutil  #Ver uso de RAM y tiempo activo del sistema
import sys 

#---------------------------------------------------------------------------------
#Funcion para limpiar consola
#---------------------------------------------------------------------------------
def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')

#---------------------------------------------------------------------------------
# Menu principal    
#---------------------------------------------------------------------------------
def menu():

    while True: 
        limpiar()
        print("=" * 45)
        print("   CRIPTO-P2P  |  Cifrado Polimórfico")
        print("   DSS101 - Universidad Don Bosco")
        print("=" * 45)
        print("  1. Generar mis llaves")
        print("  2. Escuchar/Recibir conexiones (Servidor)")
        print("  3. Conectar/Enviar llaves a otra PC   (Cliente)")
        print("  4. Enviar mensaje cifrado")
        print("  5. Mensajes recibidos")
        print("  6. Ver llavero")
        print("  7. Salir")
        print("=" * 45)
        opcion = input("  Selecciona una opción: ").strip()
        opciones(opcion)

#---------------------------------------------------------------------------------
# Manejo de opciones
#---------------------------------------------------------------------------------
def opciones(opcion):
    match opcion:
        case "1":
            generar_llaves()
        case "2":
            modo_servidor()
        case "3":
            modo_cliente()
        case "4":
            enviar_mensaje()
        case "5":
            mensajes_recibidos()
        case "6":
            ver_llavero()
        case "7":
            print("\n  Saliendo... ¡Hasta luego!")
            sys.exit()
        case _:  # Caso por defecto"
            print("\n  Opción inválida.")
            input("  Presiona Enter para continuar...") 

#---------------------------------------------------------------------------------
# Calculo de semilla polimorfica 
#---------------------------------------------------------------------------------
OMEGA = 7.27e-5  # Velocidad angular de la Tierra en rad/s

def semilla_polimorfica():
    print("\n  [*] Calculando entropía polimórfica...")
    
    # Factor 1: Rotación de la Tierra
    #t = Tiempo transcurrido desde el 1 de Enero de 1970 a las 00:00:00 UTC
    #Fecha llamada Unix Epoch
    t = time.time() 
    # t*OMEGA = Radianes totales que ha girado la tierra desde Epoch
    # % (2 x pi): El modulo 2pi deja unicamente el angulo actual y quita el acumulado
    theta = (t * OMEGA) % (2 * math.pi) #Angulo actual de rotacion de la tierra
    print(f"  [1] Ángulo de rotación terrestre : {theta:.6f} rad")

    # Factor 2: Telemetría de la PC
    ram = psutil.virtual_memory().percent #Obtenemos uso actual de RAM
    uptime = int(time.time() - psutil.boot_time()) #Obtenemos tiempo que ha estado activo el sistema
    nombre_pc = os.environ.get("COMPUTERNAME", "PC") #Obtenemos nombre del PC
    #Mostramos informacion obtenida
    print(f"  [2] Uso de RAM                   : {ram}%")
    print(f"  [3] Uptime del sistema           : {uptime} seg")
    print(f"  [4] Nombre de PC                 : {nombre_pc}")

    # Mezclar todo en un hash SHA-256
    #raw = una cadena de todos los datos obtenidos
    cadena = f"{theta}{ram}{uptime}{nombre_pc}{random.random()}"
    #raw.encode combierte la cadena en bytes
    #hashlib.sha256() aplica algoritmo SHA-256 para covertir cadena en hash de 256 bits
    #hexdigest() covierte los 256 bit en un strin de 64 carateres hexadecimales
    semilla = hashlib.sha256(cadena.encode()).hexdigest()
    print(f"\n  [*] Semilla polimórfica generada : {semilla[:32]}...") #Mostramos 32 caracteres de la semilla
    
    return semilla


#---------------------------------------------------------------------------------
# Proceso de Generacion de llaves
#---------------------------------------------------------------------------------
# Parámetros globales (estándar para todos en la red)
# P es un número primo grande en formato Hexadecimal
P = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AAAC42DAD33170D04507A33A85521ABDF1CBA64ECFB850458DBEF0A8AEA71575847732677407
G = 2 #G es un generador

#Funcion para generar llaves
def generar_llaves():
    print("\n" + "="*45)
    print("   GENERANDO PAR DE LLAVES POLIMÓRFICAS")
    print("="*45)

    #Verifica las llaves ya han sido creadas
    if not os.path.exists("Misllaves.json"):#Si no hay llaves se generan nuevas
     #Obtener la semilla polimórfica 
     semilla = semilla_polimorfica()
    
     #Calculamos la llave privada (x)
     #Convertimos el hash de la semilla a un número entero
     privada_int = int(semilla, 16)
     # La mantenemos dentro del rango del numero primo P
     privada = privada_int % P
    
     #Calcular la Llave Pública (y)
     print("  [*] Calculando llave pública (Exponenciación modular)...")
     # y = G^x mod P 
     publica = pow(G, privada, P)
    
     #Se crea un diccionario con el nombre de la pc si se conoce
     #ademas se almacenan la llave privada y publica en el diccionario Identidad
     identidad = {
        "nombre": os.environ.get("COMPUTERNAME", "PC-DESCONOCIDA"),
        "llave_privada": hex(privada),
        "llave_publica": hex(publica)
       }
     #Se crea un archivo .json llamado "Misllaves" para almacenar informacion del diccionario Identidad
     with open("Misllaves.json", "w") as f:
        json.dump(identidad, f, indent=4)

     #Se confirma creacion de llaves y se muestra llave publica    
     print("\n  [OK] Llaves generadas y guardadas en 'Misllaves.json'")
     print(f"  [Púb] {hex(publica)[:20]}...")
     input("\nPresiona Enter para continuar...") 
    else:#Si ya existen llaves se muestran
        print("Las llaves ya han sido generadas")
        with open("Misllaves.json", "r") as f:#Si existe se muestra info en pantalla
            Misllaves = json.load(f)

        print(f"  PC     : {Misllaves['nombre']}")
        print(f"  Pública: {Misllaves['llave_publica'][:50]}...")
        print(f"  Privada: {'*' * 20} (oculta)")# Solo mostramos el inicio de la llave publica para no llenar la pantalla

        print("\n[1] Continuar")
        print("\n[2] Borrar y Crear nuevas llaves")#Opcion para eliminar llaves y regenerar
        opcion = input("\nSeleccione una opcion: ")
        match(opcion):
            case "1":
                 print("\n  [OK] Usando llaves existentes.")
                 input("  Presiona Enter para continuar...")
            case "2":
                confirm = input("\n  [!] ¿Estás seguro? Perderás tus llaves actuales (s/n): ").strip().lower()
                if confirm == "s":
                     os.remove("Misllaves.json") #Se elimina el archivo Misllaves.json
                     print("  [*] Llaves eliminadas. Regenerando...")
                     generar_llaves() #Se redunda la funcion para crear las llaves
                else:
                     print("  [*] Operación cancelada.")
                     input("\n  Presiona Enter para continuar...")
            case _: 
                print("  Opción inválida.")
                input("  Presiona Enter para continuar...")
               
    return                         


#---------------------------------------------------------------------------------
# Funcion para guardar llaves publicas de otro usuarios
#---------------------------------------------------------------------------------
def guardar_en_llavero(nombre_remoto, llave_publica_remota):
    #Intentar leer el llavero.json si ya existente
    if os.path.exists("llavero.json"):
        with open("llavero.json", "r") as f:
            llavero = json.load(f)
    else:
        llavero = {}

    #Agregar o actualizar la llave publica de otra pc en el diccionario llavero
    llavero[nombre_remoto] = llave_publica_remota

    #Guardar de nuevo la informacion del diccionario llavero en llavero.json
    with open("llavero.json", "w") as f:
        json.dump(llavero, f, indent=4)
    
    #Imprime confirmacion de que la llave ha sido guardada y el nombre de la pc remota
    print(f"\n  [+] Llave de '{nombre_remoto}' guardada en el llavero.")

#---------------------------------------------------------------------------------
# Funcion para ver llaves guardadas
#---------------------------------------------------------------------------------
def ver_llavero():
    print("\n" + "="*45)
    print("   LLAVERO DE CONTACTOS (PÚBLICAS)")
    print("="*45)
    
    #Verifica que el llavero exista
    if not os.path.exists("llavero.json"):
        print("  El llavero está vacío.")#Si no existe no hay llaves almacenadas
    else:
        with open("llavero.json", "r") as f:#Si existe se muestra info en pantalla
            llavero = json.load(f)
            for nombre, llave in llavero.items():
                print(f"\n  PC: {nombre}")
                print(f"  Llave: {llave[:32]}...") # Solo mostramos el inicio de la llave para no llenar la pantalla
    
    input("\nPresiona Enter para continuar...")

#---------------------------------------------------------------------------------
# Verifiaccion de llaves propias
#---------------------------------------------------------------------------------
def obtener_mi_identidad():
    if not os.path.exists("Misllaves.json"):#Verifica que exista Misllaves.json
        print("\n  [!] Error: Primero debes generar tus llaves (Opción 1).")
        return None
    with open("Misllaves.json", "r") as f: #Si existen Misllaves.json extrae la informacion
        return json.load(f)

#---------------------------------------------------------------------------------
# Conexion en modo Servidor (escuchar)
#---------------------------------------------------------------------------------
def modo_servidor():
    mi_id = obtener_mi_identidad()
    if not mi_id:
        input("\n  Presiona Enter para continuar...")
        return

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 5555))
    server.listen(1)

    print("\n" + "="*45)
    print("   MODO SERVIDOR ACTIVO")
    print("="*45)
    print(f"  [*] Escuchando en el puerto 5555...")
    print(f"  [*] Tu IP: {socket.gethostbyname(socket.gethostname())}")
    print(f"  [*] Esperando conexión entrante...")

    try: #Intentamos establecer conexion
        conn, addr = server.accept()
        print(f"\n  [+] Conexión recibida de: {addr[0]}")

        data = conn.recv(65536).decode() #Recibimos datos desde PC Cliente
        #Estos datos puede ser un intercambio de llaves o un mensaje
        payload = json.loads(data)

        #Filtramos que tipo de info llego
        match payload.get("tipo"):

            case "INTERCAMBIO":
                #Se inicia intercambio de llaves publicas
                #Guardamos los datos de la PC Cliente en un diccionario
                info_remota = payload["datos"]
                
                #Ingresamos nuestra informacion (nombre y llave) al diccionario mi_info
                mi_info = {
                    "tipo": "INTERCAMBIO",
                    "datos": {
                        "nombre": mi_id["nombre"],
                        "publica": mi_id["llave_publica"]
                    }
                }
                #Mandamos nuestra informacion a la PC Cliente
                conn.send(json.dumps(mi_info).encode())
                
                #Guardamos la llave publica en llavero.json
                guardar_en_llavero(info_remota["nombre"], info_remota["publica"])
                #Confirmamos el intercambio
                print(f"  [OK] Llaves intercambiadas con '{info_remota['nombre']}'.")

            case "MENSAJE":
                #Alguien mandó un mensaje cifrado
                #alamcenamos informacion del paquete
                paquete = payload["datos"]
                #Almacenamos informacion del emisor
                emisor = paquete.get("emisor", "Desconocido")
                print(f"  [+] Mensaje cifrado recibido de: {emisor}")

                #Guardamos el paquete/mensaje en inbox.json
                if os.path.exists("inbox.json"):
                    with open("inbox.json", "r") as f:
                        inbox = json.load(f)
                else:
                    inbox = []

                inbox.append(paquete)
                #Guardmos la info del paquete en inbox.json
                with open("inbox.json", "w") as f:
                    json.dump(inbox, f, indent=4)
                #Se confirma que el mensaje ha sido guardado
                print(f"  [OK] Mensaje guardado en 'inbox.json'.")
                conn.send(json.dumps({"status": "OK"}).encode())

            case _: #No se conoce el tipo de paquete
                print("  [!] Paquete desconocido recibido.")

    except Exception as e:
        #No se logro hacer conexion y se muestra el error
        print(f"  [!] Error en el servidor: {e}")
    finally:
        #Cerramos conexiones
        conn.close()
        server.close()

    input("\nPresiona Enter para continuar...")


#---------------------------------------------------------------------------------
# Conexion en modo Cliente (Conectarse a Servidor)
#---------------------------------------------------------------------------------
def modo_cliente():
    mi_id = obtener_mi_identidad() #Obtenemos nombre y llave publica propia
    if not mi_id: return #Si no estan regeneradas se retorna

    #Pedimos ip de la pc a la que quermos conectarnos
    #PC Cliente llama
    ip_destino = input("\n  [*] Ingresa la IP de la otra PC (Servidor): ").strip()
    
    # Se crea el socket TCP
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        #Intentamos conectarnos al pc servidor en el puerto 5555
        print(f"  [*] Conectando a {ip_destino} en el puerto 5555...")
        cliente.connect((ip_destino, 5555))
        print("  [+] Conexión exitosa.")

        #Enviamos nuestro nombre y llave publica al servidor
        mi_info_publica = { #Aqui guardamos la info
         "tipo": "INTERCAMBIO", #Tipo de conexion
         "datos": {
         "nombre": mi_id["nombre"],
         "publica": mi_id["llave_publica"]
         }
        }
        #Mandamos la info en un .json al servidor
        cliente.send(json.dumps(mi_info_publica).encode())

        #Recibimos nombre y llave publica del servidor 
        data = cliente.recv(4096).decode()
        paquete_recibido = json.loads(data) #Cargamos los datos recibidos a una variable
        
        # Extraemos los datos reales del paquete
        if paquete_recibido.get("tipo") == "INTERCAMBIO":
         info_remota = paquete_recibido["datos"]

        #Guardamos los datos en llavero.json
        guardar_en_llavero(info_remota["nombre"], info_remota["publica"])
        print("\n  [OK] Intercambio de llaves exitoso.")#Confirmamos intercambio de llaves

    except Exception as e:
        #Si hay un error se muestra la informacion de este
        print(f"  [!] Error de conexión: {e}")
    finally:
        #Se cierra la conexion del cliente luego del interacambio
        cliente.close()
    
    input("\nPresiona Enter para continuar...")

#---------------------------------------------------------------------------------
# Cifrado polimorfico
#--------------------------------------------------------------------------------- 
def cifrado_polimorfico(mensaje, llave_publica_destino):
    print("\n" + "="*45)
    print("   INICIANDO PROCESO DE CIFRADO POLIMÓRFICO")
    print("="*45)

    #Generamos una Semilla de Sesión (Mutación). El tipo de cifrado sera diferente cada segundo
    #Usamos nuestra función de entropía para que este cifrado sea unico de este segundo
    semilla_sesion = semilla_polimorfica()
    
    shift = (int(semilla_sesion, 16) % 7) + 1  # Valor entre 1 y 7
    print(f"  [*] Mutación Geofísica: Desplazamiento de {shift} bits")

    #Se preparara la llave de cifrado (Mezclamos llave pública del destino + nuestra semilla)
    # Esto asegura que solo el dueño de la llave privada destino pueda abrirlo
    key_material = hashlib.sha256((semilla_sesion + llave_publica_destino).encode()).digest()
    
    ciphertext = []
    print("\n  [*] Cifrando bytes del mensaje...")
    
    for i, char in enumerate(mensaje):
        byte_original = ord(char)
        
        #XOR con la llave de sesión (Capa 1)
        key_byte = key_material[i % len(key_material)]
        byte_xor = byte_original ^ key_byte
        
        #Rotación de bits polimórfica (Capa 2)
        #Movemos los bits a la izquierda según la rotación de la Tierra
        byte_shifted = ((byte_xor << shift) | (byte_xor >> (8 - shift))) & 0xFF
        
        ciphertext.append(byte_shifted)
        
        #Mostrmos el proceso para los primeros 5 caracteres
        if i < 5:
            print(f"      '{char}' ({hex(byte_original)}) -> XOR -> Shift({shift}) -> {hex(byte_shifted)}")

    t_actual = time.time() # Definimos el tiempo aquí para el paquete
    #Empaquetar todo (Mensaje cifrado + Semilla de sesión para que el otro pueda recrear la llave)
    paquete = {
        "emisor": os.environ.get("COMPUTERNAME", "PC"),
        "semilla_sesion": semilla_sesion,
        "contenido_cifrado": ciphertext,
        "timestamp": t_actual
    }
    
    print("\n  [OK] Cifrado completado con éxito.")
    return paquete

#---------------------------------------------------------------------------------
# Funcion enviar Mensaje
#---------------------------------------------------------------------------------
def enviar_mensaje():
    #Primero elegimos el destinatario del llavero
    if not os.path.exists("llavero.json"):# Verifica que halla llaves publicas (contactos)
        print("\n  [!] No tienes contactos en el llavero. Conéctate primero (Opción 2-3).")
        return
    
    #Si hay llaves publicas las lee y las almacena en el diccionaro llavero
    with open("llavero.json", "r") as f:
        llavero = json.load(f)
    #Mostramos una lista de las llaves publicas de los "Contactos"
    print("\n  --- CONTACTOS DISPONIBLES ---")
    contactos = list(llavero.keys())
    for i, nombre in enumerate(contactos):
        print(f"  {i+1}. {nombre}")
    
    try:#Seleccionamos un contacto de la lista
        sel = int(input("\n  Selecciona el número de contacto: ")) - 1
        nombre_destino = contactos[sel]
        pub_destino = llavero[nombre_destino]
    except:#Si no se selecciona un contacto nos salimos
        print("  Selección inválida."); return

    #Luego de seleccionar el contacto escribimos el mensaje
    mensaje_claro = input(f"\n  Escribe el mensaje para {nombre_destino}: ")
    
    #Mandamos el mensaje junnto con la llave pubica del destino
    paquete_cifrado = cifrado_polimorfico(mensaje_claro, pub_destino)
    
    #Enviaamos mensaje por la red
    #Seleccionamos la ip del destino
    ip_destino = input("\n  [*] Ingresa la IP del destinatario para enviar: ").strip()
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Se abre un socket para la comunicacion
    
    try:
        #Intentamos conectarnos
        cliente.connect((ip_destino, 5555))
        # Mandamos una cabecera para que el servidor sepa que es un MENSAJE y no un intercambio
        payload = {"tipo": "MENSAJE", "datos": paquete_cifrado}
        cliente.send(json.dumps(payload).encode()) #Eviamos el paquete
        print(f"\n  [OK] Mensaje enviado a {nombre_destino}!") #confirmamos envio
    except Exception as e:
        #Mostramos info del error en caso de haberlo
        print(f"  [!] Error al enviar: {e}")
    finally:
        #Cerramos el socket de conexion
        cliente.close()
    
    input("\nPresiona Enter para continuar...")


#---------------------------------------------------------------------------------
# Funcion para descrifrar
#---------------------------------------------------------------------------------
def descifrar_polimorfico(paquete):
    print("\n" + "="*45)
    print("   INICIANDO PROCESO DE DESCIFRADO")
    print("="*45)

    #Obtenemos la semilla de sesión del paquete
    semilla_sesion = paquete["semilla_sesion"] #Semilla de sesion para poder descifrar el paquete
    contenido_cifrado = paquete["contenido_cifrado"] #Paquete cifrado
    emisor = paquete.get("emisor", "Desconocido") # Nombre deEmisor
    
    #Mostrar informacion
    print(f"  [*] Mensaje de        : {emisor}")
    print(f"  [*] Semilla de sesión : {semilla_sesion[:32]}...")

    #Obtener mi llave pública (El emisor la utilizo para cifrar)
    with open("Misllaves.json", "r") as f:
        mi_id = json.load(f)
    mi_publica = mi_id["llave_publica"]
    
    
    #Recreamoa la misma llave de cifrado (mismo proceso que al cifrar)
    key_material = hashlib.sha256((semilla_sesion + mi_publica).encode()).digest()

    #Recuperar el shift (mismo cálculo que al cifrar)
    shift = (int(semilla_sesion, 16) % 7) + 1
    print(f"  [*] Desplazamiento    : {shift} bits")

    #Descifrar byte por byte en un proceso inverso
    mensaje_claro = []
    print("\n  [*] Descifrando bytes...")

    for i, byte_cifrado in enumerate(contenido_cifrado):

        #Rotación inversa (derecha en vez de izquierda)
        byte_unshifted = ((byte_cifrado >> shift) | (byte_cifrado << (8 - shift))) & 0xFF

        #XOR inverso (XOR con la misma llave = resultado original)
        key_byte = key_material[i % len(key_material)]
        byte_original = byte_unshifted ^ key_byte

        mensaje_claro.append(chr(byte_original))

        #Mostramos el proceso para los primeros 5 caracteres
        if i < 5:
            print(f"      {hex(byte_cifrado)} -> Unshift({shift}) -> XOR -> '{chr(byte_original)}'")

    resultado = "".join(mensaje_claro)
    print(f"\n  [OK] Mensaje descifrado: {resultado}") #Inprimimos el mensaje
    return resultado

#---------------------------------------------------------------------------------
# Ver Mensajes recibidos
#---------------------------------------------------------------------------------
def mensajes_recibidos():
    print("\n" + "="*45)
    print("   BANDEJA DE MENSAJES RECIBIDOS")
    print("="*45)

    #Primero verificamos que exista inbox.json
    if not os.path.exists("inbox.json"):
        print("  No tienes mensajes recibidos.")
        input("\n  Presiona Enter para continuar...")
        return #Si no hay retornamos

    with open("inbox.json", "r") as f:
        inbox = json.load(f) #Cargamos inbox.json a "inbox"

    if len(inbox) == 0: #Verificamos que inbox.json no este vacio
        print("  La bandeja está vacía.")
        input("\n  Presiona Enter para continuar...")
        return

    #Listamos losmensajes
    print(f"  Tienes {len(inbox)} mensaje(s):\n")
    for i, paquete in enumerate(inbox):
        print(f"  {i+1}. De: {paquete.get('emisor', 'Desconocido')} | "
              f"Hora: {time.strftime('%H:%M:%S', time.localtime(paquete['timestamp']))}")

    #Seleccionamos un  mensaje
    try:
        sel = int(input("\n  Selecciona el número de mensaje a descifrar: ")) - 1
        if sel < 0 or sel >= len(inbox):
            print("  Selección inválida.")
            input("\n  Presiona Enter para continuar...")
            return
    except:
        print("  Entrada inválida.")
        input("\n  Presiona Enter para continuar...")
        return

    #Luego se seleccionar mandamos a descifrar el mensaje seleccionado
    descifrar_polimorfico(inbox[sel])
    input("\n  Presiona Enter para continuar...")

#---------------------------------------------------------------------------------
# Codigo de ejecucion
#---------------------------------------------------------------------------------
if __name__ == "__main__":
    menu()