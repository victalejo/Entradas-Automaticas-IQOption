from iqoptionapi.stable_api import IQ_Option
import logging
from datetime import datetime
import time
import configparser
from dateutil import tz
import sys

# Configuracion del logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def cargar_configuracion():
    try:
        config = configparser.RawConfigParser()
        config.read('config.txt')
        return {
            'email': config.get('GERAL', 'email'),
            'senha': config.get('GERAL', 'senha')
        }
    except Exception as e:
        logging.error(f"Error al cargar la configuracion: {e}")
        sys.exit(1)


def cargar_senales():
    try:
        with open('sinais.txt', 'r', encoding='UTF-8') as archivo:
            senales = [linea.strip() for linea in archivo.readlines() if linea.strip()]
        return senales
    except Exception as e:
        logging.error(f"Error al cargar las senales: {e}")
        sys.exit(1)


def parsear_fecha_hora(fecha_str, hora_str):
    try:
        fecha_hora = datetime.strptime(f"{fecha_str} {hora_str}", "%d/%m/%Y %H:%M:%S")
        return fecha_hora
    except ValueError as e:
        logging.error(f"Error al parsear fecha/hora: {e}")
        return None


def ejecutar_operacion(API, par, direccion, timeframe, stake):
    try:
        status, id = API.buy(stake, par, direccion, timeframe)
        if status:
            logging.info(f"Operacion exitosa - ID: {id}")
            # Esperar al resultado
            resultado = API.check_win_v4(id)
            logging.info(f"Resultado de la operacion: {resultado}")
        else:
            logging.error("La operacion fallo")
    except Exception as e:
        logging.error(f"Error al ejecutar la operacion: {e}")


def main():
    # Inicializar conexion
    config = cargar_configuracion()
    API = IQ_Option(config['email'], config['senha'])

    # Intentar conectar
    for _ in range(3):  # 3 intentos de conexion
        if API.connect():
            logging.info("Conectado exitosamente")
            break
        logging.warning("Reintentando conexion...")
        time.sleep(5)
    else:
        logging.error("No se pudo establecer conexion")
        sys.exit(1)

    API.change_balance('PRACTICE')  # Modo practica
    senales = cargar_senales()

    for senal in senales:
        try:
            fecha, hora, par, timeframe, direccion, stake = senal.split(',')
            fecha_hora_operacion = parsear_fecha_hora(fecha, hora)

            if not fecha_hora_operacion:
                continue

            # Esperar hasta el momento de la operacion
            while datetime.now() < fecha_hora_operacion:
                time.sleep(1)
                if not API.check_connect():
                    if not API.connect():
                        logging.error("Perdida de conexion")
                        sys.exit(1)

            # Ejecutar la operacion en el momento correcto
            if datetime.now().strftime("%d/%m/%Y %H:%M:%S") == fecha_hora_operacion.strftime("%d/%m/%Y %H:%M:%S"):
                logging.info(f"Ejecutando operacion: {par} {direccion} {timeframe}")
                ejecutar_operacion(API, par, direccion, int(timeframe), float(stake))

        except Exception as e:
            logging.error(f"Error procesando senal: {e}")
            continue


if __name__ == "__main__":
    main()