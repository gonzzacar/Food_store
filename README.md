# Food Store – Programación II

Sistema de consola en Python 3.12+ para gestionar categorías, productos, usuarios y pedidos con POO.

## Ejecución
Desde la carpeta raíz del proyecto:

```bash
python main.py
```

Pruebas básicas:

```bash
python pruebas.py
```

## Credenciales de prueba
- Administrador: `admin@foodstore.com` / `admin123`
- Cliente: `cliente@foodstore.com` / `cliente123`

Los datos se almacenan en memoria y se pierden al cerrar el programa, tal como pide la consigna.

## Arquitectura
- `entidades/`: modelo del dominio y validaciones.
- `enums/`: roles, estados y formas de pago.
- `excepciones/`: excepciones propias.
- `servicios/`: lógica de negocio y colecciones.
- `consola/`: menús por rol y lectura de entradas.
- `main.py`: inicialización, login y ciclo de sesión.
- `pruebas.py`: pruebas manuales automatizadas del modelo y servicios.

## Video e informe
#Enlace al informe: file:///C:/Users/Gonzalo/Downloads/Informe_De_Food_Store.pdf
#Enlace al video: https://youtu.be/4-hDkXY_Z5A?si=fR2Tp8tKOCv9APtz
