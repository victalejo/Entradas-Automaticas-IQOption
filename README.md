# Bot de Trading Automatizado para IQ Option

Este bot permite ejecutar operaciones automáticas en IQ Option basadas en señales predefinidas. Utiliza la API no oficial de IQ Option mantenida por victalejo.

## ⚠️ Descargo de Responsabilidad

Este bot es solo para fines educativos y de prueba. El trading conlleva riesgos significativos y puede resultar en la pérdida de capital. Use este software bajo su propio riesgo.

## 🚀 Características

- Ejecución automática de operaciones basada en señales
- Soporte para múltiples pares de trading
- Control de tiempo preciso para las entradas
- Modo práctica incluido
- Sistema de reconexión automática
- Seguimiento de resultados de operaciones

## 📋 Requisitos Previos

- Python 3.7 o superior
- Cuenta en IQ Option (real o práctica)
- Pip (gestor de paquetes de Python)

## 🔧 Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio
```

2. Instalar la API de IQ Option (versión recomendada de victalejo):
```bash
pip install git+https://github.com/victalejo/iqoptionapi.git
```

3. Instalar dependencias adicionales:
```bash
pip install python-dateutil configparser
```

## ⚙️ Configuración

1. Crear archivo `config.txt` en el directorio raíz:
```ini
[GERAL]
email=tu_email_iqoption
senha=tu_contraseña_iqoption
```

2. Crear archivo `sinais.txt` con el formato:
```
DD/MM/YYYY,HH:MM:SS,PAR,TIMEFRAME,DIRECCION,STAKE
```

Ejemplo de señales:
```
01/01/2025,22:15:00,EURUSD-OTC,5,CALL,5.00
01/01/2025,22:20:00,EURUSD-OTC,5,PUT,5.00
```

### Formato de Señales:
- `DD/MM/YYYY`: Fecha de la operación
- `HH:MM:SS`: Hora exacta de entrada
- `PAR`: Par de trading (ej: EURUSD-OTC)
- `TIMEFRAME`: Duración en minutos
- `DIRECCION`: CALL (para compra) o PUT (para venta)
- `STAKE`: Cantidad a invertir

## 🚀 Uso

1. Ejecutar el bot:
```bash
python bot.py
```

2. El bot:
   - Conectará con IQ Option
   - Cargará las señales del archivo
   - Esperará el momento exacto para cada operación
   - Mostrará resultados en tiempo real

## 📊 Estructura del Proyecto

```
├── bot.py              # Script principal
├── config.txt          # Configuración de credenciales
├── sinais.txt          # Archivo de señales
└── README.md           # Este archivo
```

## 🔍 Características de la API victalejo/iqoptionapi

Esta versión de la API ofrece varias mejoras sobre otras versiones:

- Mayor estabilidad en las conexiones
- Mejor manejo de errores
- Compatibilidad mejorada con versiones recientes de Python
- Funciones adicionales para el trading
- Mantenimiento activo

## 📝 Notas Importantes

1. **Modo Práctica**: Por defecto, el bot opera en cuenta práctica. Para cambiar a cuenta real, modificar:
```python
API.change_balance('PRACTICE')  # Cambiar a 'REAL' para cuenta real
```

2. **Timeframes**: Los timeframes disponibles dependen del tipo de cuenta y activo.

3. **Reconnexión**: El bot intentará reconectarse automáticamente si pierde la conexión.

## 🐛 Solución de Problemas

1. Error de conexión:
   - Verificar credenciales en config.txt
   - Comprobar conexión a internet
   - Verificar que la API de IQ Option esté operativa

2. Error en señales:
   - Verificar formato de fecha/hora
   - Comprobar que el par de trading existe
   - Verificar formato del archivo sinais.txt

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abrir un issue primero para discutir los cambios propuestos.

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.