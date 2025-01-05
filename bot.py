#!/usr/bin/env python
# -*- coding: utf-8 -*-

from iqoptionapi.stable_api import IQ_Option
from datetime import datetime
import time
import configparser
import sys


def cargar_configuracion():
    try:
        config = configparser.RawConfigParser()
        config.read('config.txt')
        return {
            'email': config.get('GERAL', 'email'),
            'senha': config.get('GERAL', 'senha')
        }
    except Exception as e:
        print(f"Error al cargar la configuracion: {e}")
        sys.exit(1)


def cargar_senales():
    try:
        with open('sinais.txt', 'r', encoding='utf-8') as archivo:
            senales = [linea.strip() for linea in archivo.readlines() if linea.strip()]
        return senales
    except Exception as e:
        print(f"Error al cargar las senales: {e}")
        sys.exit(1)


def parsear_fecha_hora(fecha_str, hora_str):
    try:
        fecha_hora = datetime.strptime(f"{fecha_str} {hora_str}", "%d/%m/%Y %H:%M:%S")
        return fecha_hora
    except ValueError as e:
        print(f"Error con el formato de fecha/hora: {e}")
        return None


def ejecutar_operacion(API, par, direccion, timeframe, stake):
    try:
        print(f"\n{'=' * 50}")
        print(f"Ejecutando operacion:")
        print(f"Par: {par}")
        print(f"Direccion: {direccion}")
        print(f"Timeframe: {timeframe}")
        print(f"Inversion: {stake}")
        print(f"{'=' * 50}")

        status, id = API.buy(stake, par, direccion, timeframe)

        if status:
            print(f"\n[+] Operacion colocada exitosamente!")
            print(f"ID de operacion: {id}")

            # Esperar al resultado
            time.sleep(timeframe * 60)  # Esperar el tiempo del timeframe
            resultado = API.check_win_v4(id)

            if resultado > 0:
                print(f"[+] Ganancia: ${resultado}")
            elif resultado == 0:
                print("[=] Empate")
            else:
                print(f"[-] Perdida: ${resultado}")
        else:
            print("\n[-] La operacion no pudo ser colocada")

    except Exception as e:
        print(f"\n[!] Error durante la operacion: {e}")


def main():
    print("\n=== Bot de Trading IQ Option ===\n")

    # Inicializar conexion
    config = cargar_configuracion()
    API = IQ_Option(config['email'], config['senha'])

    # Intentar conectar
    print("Conectando a IQ Option...")
    for intento in range(3):
        if API.connect():
            print("[+] Conexion exitosa!")
            break
        print(f"[!] Intento {intento + 1}/3 fallido, reintentando...")
        time.sleep(5)
    else:
        print("[-] No se pudo establecer conexion")
        sys.exit(1)

    API.change_balance('PRACTICE')
    print("Modo practica activado")

    print("\nCargando senales...")
    senales = cargar_senales()
    print(f"Se encontraron {len(senales)} senales para operar")

    print("\nIniciando operaciones...")
    for senal in senales:
        try:
            fecha, hora, par, timeframe, direccion, stake = senal.split(',')
            fecha_hora_operacion = parsear_fecha_hora(fecha, hora)

            if not fecha_hora_operacion:
                continue

            print(f"\nEsperando momento de entrada para {par} a las {hora}")

            # Esperar hasta el momento de la operacion
            while datetime.now() < fecha_hora_operacion:
                time.sleep(1)
                if not API.check_connect():
                    print("\n[!] Conexion perdida, reconectando...")
                    if not API.connect():
                        print("[-] No se pudo restablecer la conexion")
                        sys.exit(1)

            # Ejecutar la operacion en el momento correcto
            if datetime.now().strftime("%d/%m/%Y %H:%M:%S") == fecha_hora_operacion.strftime("%d/%m/%Y %H:%M:%S"):
                ejecutar_operacion(API, par, direccion, int(timeframe), float(stake))

        except Exception as e:
            print(f"\n[!] Error procesando senal: {e}")
            continue

    print("\nTodas las operaciones han sido completadas!")


if __name__ == "__main__":
    main()