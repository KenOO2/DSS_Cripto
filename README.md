# DSS_Cripto
Este es un proyecto desarrollado en phyton para simular un sistema de intercambio de mensajes con enfasis en la encriptación original 
para la materia de Diseño de Sistemas de Seguridad de Redes.

### Guía de Ejecucion y Operación del Sistema (Manual de Usuario)
Para la correcta ejecución del programa con su algoritmo APSG (Algoritmo Polimorfico de Semilla Geofisica), se requiere que ambos nodos (Emisor y Receptor) se encuentren en la misma red de área local (LAN) y tengan instalado el intérprete de Python 3.11 o superior.

## Ejecucion
1.Descargar el programa y extensiones
Al descargar el progama tambien es necesario descargar la extension "psutil" mediante consola con
el comando "pip install psutil".

2.Copiar carpeta
Es recomendable copiar la carpeta donde esta el archivo Main.py y ponerle un nombre como DSS_Cripto2 para posteriormente poder simular el funcionamiento 
de dos computadoras en una sola. *Si se usan dos computadoras fisicas se puede ignorar este paso*

3.Abrir CMD
En el caso de solo usar una pc fisica arir dos ventanas de CMD y en cada una navegar hasta las carpetas DSS_Cripto y DSS_Cripto2 respectivamente para posteriomente ejecutar "phyton Main.py" en cada CMD. *Si son dos pc fisicas solo navegar hasta la carpeta DSS_Cripto y ejecutar*

## Operacion del programa

1. Configuración Inicial e Identidad 
Al ejecutar el programa por primera vez en consola (python main.py), el usuario debe seleccionar la Opción 1: Generar mis llaves. 
El sistema recolectará la entropía geofísica y de hardware para crear el archivo Misllaves.json. 
Nota: Este paso es obligatorio antes de cualquier comunicación, ya que establece la identidad criptográfica del nodo. 

2. Intercambio de Llaves Públicas (Apretón de Manos) 
Para que dos usuarios puedan comunicarse, primero deben intercambiar sus llaves públicas: 
El Receptor debe activar la Opción 2:Escuchar/Recibir conexiones (Servidor) para ponerse en estado de escucha. 
El Emisor debe seleccionar la Opción 3: Conectar/Enviar llaves a otra PC, ingresando la dirección IP del receptor. 
Una vez completado, ambos nodos habrán guardado la llave pública del otro en su archivo llavero.json. 

3. Envío de Mensajes Cifrados 
Con las llaves intercambiadas, el emisor selecciona la Opción 4: Enviar Mensaje: 
El sistema mostrará el listado de contactos disponibles en el "llavero". 
El usuario redacta el mensaje y el sistema mostrará en consola el proceso de XOR y Up Shift en tiempo real. 
El mensaje viaja cifrado por la red y se almacena automáticamente en el receptor. 
Nota: El receptor debe estar en la Opción 2 para poder recibir el mensaje. 

4. Lectura y Descifrado 
El receptor, tras haber recibido un paquete en modo servidor, selecciona la Opción 5: Ver mensajes recibidos: 
Se listarán los criptogramas almacenados en inbox.json. 
Al seleccionar un mensaje, el sistema aplicará el Down Shift y el XOR inverso utilizando la semilla de sesión adjunta al paquete, mostrando el texto original recuperado.

5. Ver llaves Almacenados
Al seleccionar esta opccion se mostraran la llaves publicas de otras pc guardadas en el archivo llavero.json
