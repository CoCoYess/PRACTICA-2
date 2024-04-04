#!/usr/bin/python

#
# Practica 2
# Nava Badillo Yessica Isabel
#

## Importar librerias
import random
import argparse

## Argumentos de linea de comandos
parser = argparse.ArgumentParser(description='Simulacion de IMSS')

# Numero de pacientes a simular (int)
parser.add_argument('-n', '--numero', type=int, default=10, nargs='?',
                    help='Numero de pacientes a simular.')
# Tiempo de atencion por paciente (float)
parser.add_argument('-a', '--atencion', type=float, default=30, nargs='?',
                    help='Tiempo en minutos que se requiere para atender a un paciente. Debe ser multiplo de 0.5')
# Porcentaje de pacientes que vienen a urgencias (int)
parser.add_argument('-u', '--urgencias', type=int, default=20, nargs='?',
                    help='Porcentaje (0-100) de pacientes que vienen a urgencias.')
# Probabilidad de que un paciente llegue, calculado cada 0.5 minutos (int)
parser.add_argument('-l', '--llegada', type=int, default=2, nargs='?',
                    help='Probabilidad (0-100) de que un paciente llegue, calculado cada 0.5 minutos.')
# Se la da preferencia a personas en urgencias? (bool)
parser.add_argument('-p', '--preferencia', type=bool, default=False, nargs='?',
                    help='Se le da preferencia a las personas que vienen a urgencias?')
# Imprimir mensajes de DEBUG? (bool)
parser.add_argument('-d', '--debug', type=bool, default=False, nargs='?',
                    help='Imprimir mensajes de DEBUG?')
# Imprimir resultados en CSV? (bool)
parser.add_argument('-c', '--csv', type=bool, default=False, nargs='?',
                    help='Imprimir resultados en CSV?')

# Leer argumentos de linea de comandos
opciones = parser.parse_args()

# Ignorar valores no validos
if opciones.urgencias > 100 or opciones.llegada > 100:
    parser.error("El porcentaje no puede ser mayor a 100%")
if opciones.atencion % 0.5 != 0:
    parser.error("El tiempo de atencion debe ser multiplo de 0.5")

## Definir variables
# Asignar valores de argumentos a variables locales
parametrosPacientes       = opciones.llegada
parametrosAtencion        = opciones.atencion
parametrosUrgencias       = opciones.urgencias
parametrosPreferencia     = opciones.preferencia
parametrosNumeroPacientes = opciones.numero
parametrosDebug           = opciones.debug
parametrosCSV             = opciones.csv

# Definir variables de tiempo:
# - simulacionTiempo: tiempo transcurrido en la simulacion
# - simulacionTiempoEspera: tiempo esperado de todos los pacientes
# - simulacionTiempoEsperaNormal: tiempo esperado de los pacientes normales
# - simulacionTiempoEsperaUrgencias: tiempo esperado de los pacientes de urgencias
simulacionTiempo = 0.0
simulacionTiempoEspera = 0.0
simulacionTiempoEsperaNormal = 0.0
simulacionTiempoEsperaUrgencias = 0.0

# Definir variables de cola:
# - pacientesCuenta: numero de paciente asignado conforme llegan
# - pacientesNormal: cola de pacientes de atencion normal (para prioridad)
# - pacientesUrgencia: cola de pacientes de urgencias (para prioridad)
# - pacientesTodos: cola de pacientes de atencion normal y urgencias (para no prioridad)
# - pacientesCola: cola de pacientes de atencion global (normal y urgencias) que no manipulamos, para calculos al finalizar
pacientesCuenta     = 0
pacientesNormal     = []
pacientesUrgencia   = []
pacientesTodos      = []
pacientesCola       = []

# Definir variables de atencion:
# - pacientesAtendiendo: en este momento estamos atendiendo a un paciente? (True = Si, False = no)
# - pacientesAtendiendoClase: que tipo de paciente estamos atendiendo? Se utiliza para la prioridad (0 normal, 1 urgencias)
# - pacientesAtendiendoTiempo: tiempo transcurrido atendiendo a el cliente
pacientesAtendiendo = False
pacientesAtendiendoClase = 0
pacientesAtendiendoTiempo = 0.0

# Definir clase de paciente:
#  - paciente.pacienteNumero: el numero de el paciente (valor de pacientesCuenta cuando llega el paciente)
#  - paciente.pacienteUrgencias: bool denotando si el paciente es de urgencias o no
#  - paciente.tiempoLlegada: el minuto en el que llego el paciente
#  - paciente.tiempoEsperado: cuanto tiempo paso el paciente esperando en cola
class paciente:
    def __init__(self, pacienteNumero, pacienteUrgencias, tiempoLlegada, tiempoEsperado):
        self.pacienteNumero = pacienteNumero
        self.pacienteUrgencias = pacienteUrgencias
        self.tiempoLlegada = tiempoLlegada
        self.tiempoEsperado = tiempoEsperado

## Bucle de llegada y atencion de clientes
# Mientras todavia falten pacientes a llegar...
while pacientesCuenta < parametrosNumeroPacientes:
    ## Llegada de pacientes
    # El parametrosPacientes% de cada medio minuto llega un nuevo paciente
    if random.randrange(0,100) < parametrosPacientes:
        # Incrementar nuestra cuenta de pacientes
        pacientesCuenta += 1

        ## Decidir urgencias
        # El parametrosUrgencias% de cada paciente es un paciente de urgencias, si es de urgencias...
        if random.randrange(0,100) < parametrosUrgencias:
            # En el caso de preferencia...
            if parametrosPreferencia == True:
                # Agregamos al paciente a la cola de urgencias
                pacientesUrgencia.append(paciente(pacientesCuenta, True, simulacionTiempo, 0))
            # En el caso de no preferencia...
            else:
                # Agregamos al paciente a la cola de todos
                pacientesTodos.append(paciente(pacientesCuenta, True, simulacionTiempo, 0))
            # Agregar al paciente a la cola global
            pacientesCola.append(paciente(pacientesCuenta, True, simulacionTiempo, 0))
            # DEBUG: anunciar que llego un paciente y su tipo
            if parametrosDebug:
                print("Urgencias:", pacientesCuenta)
        # Si no es de urgencias...
        else:
            # En el caso de preferencia...
            if parametrosPreferencia == True:
                # Agregamos al paciente a la cola normal
                pacientesNormal.append(paciente(pacientesCuenta, False, simulacionTiempo, 0))
            # En el caso de no preferencia...
            else:
                # Agregamos al paciente a la cola de todos
                pacientesTodos.append(paciente(pacientesCuenta, False, simulacionTiempo, 0))
            # Agregar al paciente a la cola global
            pacientesCola.append(paciente(pacientesCuenta, False, simulacionTiempo, 0))
            # DEBUG: anunciar que llego un paciente y su tipo
            if parametrosDebug:
                print("Normal:", pacientesCuenta)

    ## Atender paciente
    # Si no estamos atendiendo a un paciente y hay pacientes en espera...
    if pacientesAtendiendo == False and len(pacientesNormal) + len(pacientesUrgencia) + len(pacientesTodos) > 0:
        # En el caso de preferencia...
        if parametrosPreferencia == True:
            # Si tenemos pacientes en la cola de urgencias...
            if len(pacientesUrgencia) > 0:
                # Actualizar el tiempo que el paciente se la paso esperando
                pacientesCola[pacientesUrgencia[0].pacienteNumero-1].tiempoEsperado = simulacionTiempo - pacientesUrgencia[0].tiempoLlegada
                # Actualizar la clase de cliente que estamos atendiendo
                pacientesAtendiendoClase = 1
            # Si no tenemos pacientes en la cola de urgencias...
            else:
                # Actualizar el tiempo que el paciente se la paso esperando
                pacientesCola[pacientesNormal[0].pacienteNumero-1].tiempoEsperado = simulacionTiempo - pacientesNormal[0].tiempoLlegada
                # Actualizar la clase de cliente que estamos atendiendo
                pacientesAtendiendoClase = 0
        # En el caso de no preferencia...
        else:
            # Actualizar el tiempo que el paciente se la paso esperando
            pacientesCola[pacientesTodos[0].pacienteNumero-1].tiempoEsperado = simulacionTiempo - pacientesTodos[0].tiempoLlegada
        # Actualizar que estamos atendiendo a un paciente
        pacientesAtendiendo = True

    # Si ya estamos atendiendo...
    if pacientesAtendiendo == True:
        # Si el tiempo que pasamos atendiendo es igual a el tiempo que tardamos en atender... (terminamos)
        if pacientesAtendiendoTiempo == parametrosAtencion:
            # En el caso de no preferencia...
            if parametrosPreferencia == False:
                # DEBUG: anunciar a que paciente atendimos
                if parametrosDebug:
                    print("                 Atendimos a", pacientesTodos[0].pacienteNumero)
                # Eliminar a el paciente que atendimos de la cola
                del pacientesTodos[0]
            # En el caso de preferencia...
            # Si atendimos a un paciente de urgencias...
            elif pacientesAtendiendoClase == 1:
                # DEBUG: anunciar a que paciente atendimos
                if parametrosDebug:
                    print("                 Atendimos a", pacientesUrgencia[0].pacienteNumero)
                # Eliminar a el paciente que atendimos de la cola
                del pacientesUrgencia[0]
            # Si atendimos a un paciente normal...
            elif pacientesAtendiendoClase == 0:
                # DEBUG: anunciar a que paciente atendimos
                if parametrosDebug:
                    print("                 Atendimos a", pacientesNormal[0].pacienteNumero)
                # Eliminar a el paciente que atendimos de la cola
                del pacientesNormal[0]
            # Actualizar que ya no estamos atendiendo a un paciente
            pacientesAtendiendo = False
            # Reiniciar el reloj de tiempo que estamos atendiendo
            pacientesAtendiendoTiempo = 0.0
        # Si todavia no terminamos...
        else:
            # Incrementar el tiempo que llevamos atendiendo
            pacientesAtendiendoTiempo += 0.5

    ## Aumentar el tiempo pasado en la simulacion
    simulacionTiempo += 0.5

# -- Aqui termina el bucle de llegada y atencion de pacientes --

# DEBUG: anunciar final de bucle de llegada
if parametrosDebug:
    print("Final de bucle de llegada de pacientes")

## Bucle de solamente atencion de pacientes
# Si todavia tenemos pacientes en alguna cola...
while len(pacientesNormal) + len(pacientesUrgencia) + len(pacientesTodos) > 0:
    ## Atender paciente (mismo codigo de arriba)
    # Si no estamos atendiendo a un paciente y hay pacientes en espera...
    if pacientesAtendiendo == False and len(pacientesNormal) + len(pacientesUrgencia) + len(pacientesTodos) > 0:
        # En el caso de preferencia...
        if parametrosPreferencia == True:
            # Si tenemos pacientes en la cola de urgencias...
            if len(pacientesUrgencia) > 0:
                # Actualizar el tiempo que el paciente se la paso esperando
                pacientesCola[pacientesUrgencia[0].pacienteNumero-1].tiempoEsperado = simulacionTiempo - pacientesUrgencia[0].tiempoLlegada
                # Actualizar la clase de cliente que estamos atendiendo
                pacientesAtendiendoClase = 1
            # Si no tenemos pacientes en la cola de urgencias...
            else:
                # Actualizar el tiempo que el paciente se la paso esperando
                pacientesCola[pacientesNormal[0].pacienteNumero-1].tiempoEsperado = simulacionTiempo - pacientesNormal[0].tiempoLlegada
                # Actualizar la clase de cliente que estamos atendiendo
                pacientesAtendiendoClase = 0
        # En el caso de no preferencia...
        else:
            # Actualizar el tiempo que el paciente se la paso esperando
            pacientesCola[pacientesTodos[0].pacienteNumero-1].tiempoEsperado = simulacionTiempo - pacientesTodos[0].tiempoLlegada
        # Actualizar que estamos atendiendo a un paciente
        pacientesAtendiendo = True

    # Si ya estamos atendiendo...
    if pacientesAtendiendo == True:
        # Si el tiempo que pasamos atendiendo es igual a el tiempo que tardamos en atender... (terminamos)
        if pacientesAtendiendoTiempo == parametrosAtencion:
            # En el caso de no preferencia...
            if parametrosPreferencia == False:
                # DEBUG: anunciar a que paciente atendimos
                if parametrosDebug:
                    print("                 Atendimos a", pacientesTodos[0].pacienteNumero)
                # Eliminar a el paciente que atendimos de la cola
                del pacientesTodos[0]
            # En el caso de preferencia...
            # Si atendimos a un paciente de urgencias...
            elif pacientesAtendiendoClase == 1:
                # DEBUG: anunciar a que paciente atendimos
                if parametrosDebug:
                    print("                 Atendimos a", pacientesUrgencia[0].pacienteNumero)
                # Eliminar a el paciente que atendimos de la cola
                del pacientesUrgencia[0]
            # Si atendimos a un paciente normal...
            elif pacientesAtendiendoClase == 0:
                # DEBUG: anunciar a que paciente atendimos
                if parametrosDebug:
                    print("                 Atendimos a", pacientesNormal[0].pacienteNumero)
                # Eliminar a el paciente que atendimos de la cola
                del pacientesNormal[0]
            # Actualizar que ya no estamos atendiendo a un paciente
            pacientesAtendiendo = False
            # Reiniciar el reloj de tiempo que estamos atendiendo
            pacientesAtendiendoTiempo = 0.0
        # Si todavia no terminamos...
        else:
            # Incrementar el tiempo que llevamos atendiendo
            pacientesAtendiendoTiempo += 0.5

    ## Aumentar el tiempo pasado en la simulacion
    simulacionTiempo += 0.5

# -- Aqui termina el bucle de solamente atencion de pacientes --

## Sacar el promedio de el tiempo esperado de todos los pacientes
# Sumar todos los valores
for i in range(len(pacientesCola)):
    simulacionTiempoEspera += pacientesCola[i].tiempoEsperado
# Dividir la suma entre la cantidad de valores
simulacionTiempoEspera = simulacionTiempoEspera / len(pacientesCola)

## Definir variable para contar el numero de pacientes para nuestros promedios
pacienteCuentaPromedio = 0

## Sacar el promedio de el tiempo esperado de los pacientes normales
# Sumar todos los valores y contar el numero de pacientes normales
for i in range(len(pacientesCola)):
    if pacientesCola[i].pacienteUrgencias == False:
        simulacionTiempoEsperaNormal += pacientesCola[i].tiempoEsperado
        pacienteCuentaPromedio += 1
# Dividir la suma entre la cantidad de valores
simulacionTiempoEsperaNormal = simulacionTiempoEsperaNormal / pacienteCuentaPromedio

## Reiniciar variable para contar
pacienteCuentaPromedio = 0

## Sacar el promedio de el tiempo esperado de los pacientes de urgencias
# Sumar todos los valores y contar el numero de pacientes de urgencias
for i in range(len(pacientesCola)):
    if pacientesCola[i].pacienteUrgencias == True:
        simulacionTiempoEsperaUrgencias += pacientesCola[i].tiempoEsperado
        pacienteCuentaPromedio += 1
# Dividir la suma entre la cantidad de valores
simulacionTiempoEsperaUrgencias = simulacionTiempoEsperaUrgencias / pacienteCuentaPromedio

## Imprimir resultados
# Si requerimos formato CSV...
if parametrosCSV:
    # Formato: tiempo simulado, espera promedio, espera promedio (normal), espera promedio (urgencias)
    print(f"{simulacionTiempo},{simulacionTiempoEspera},{simulacionTiempoEsperaNormal},{simulacionTiempoEsperaUrgencias}")
# Si requerimos formato para humano...
else:
    print()
    # Imprimir lista de pacientes
    # Formato: 'Numero de paciente' 'El paciente es de urgencias?' 'Tiempo de llegada de el paciente' 'Tiempo que el paciente espero'
    print("Lista de pacientes:")
    for i in range(len(pacientesCola)):
        print(pacientesCola[i].pacienteNumero, pacientesCola[i].pacienteUrgencias, pacientesCola[i].tiempoLlegada, pacientesCola[i].tiempoEsperado)
    
    print()
    
    # Imprimir las estadisticas
    print("=== Estadisticas ===")
    print("Tiempo transcurrido en simulacion:", simulacionTiempo)
    print("Tiempo de espera promedio:", simulacionTiempoEspera)
    print("Tiempo de espera promedio (Normal):", simulacionTiempoEsperaNormal)
    print("Tiempo de espera promedio (Urgencias):", simulacionTiempoEsperaUrgencias)
