# Taller 1 Sistemas de Recomendación - Grupo 04

## Integrantes

- Daniel Esteban Aguilera Figueroa
- Angel Abel Arismendy Contreras
- Daniela Alejandra Camacho Molano
- Jairo Alberto Garavito Correa
- Juan Diego Gonzalez Gomez

## Versión recomendada de Python

Python 3.12.9

## Pasos para Ejecutar la Aplicación

### Backend:

1. Desde una terminal, en la carpeta raíz del repositorio, ejecutar los comandos:
   - `pip install -r requirements.txt`
   - `py .\app\manage.py makemigrations`
   - `py .\app\manage.py migrate`
   - `py .\app\manage.py runserver`
2. Agregar el archivo .env con las credenciales de la base de datos
3. Ingresar a la ruta: `http://127.0.0.1:8000/`

### Frontend

1. Desde una terminal, en la carpeta raíz del repositorio, ejecutar los comandos:
   - `cd .\frontend\`
   - `npm install -g pnpm`
   - `pnpm install`
   - `pnpm dev`
2. Agregar el archivo .env con la url del backend
3. Ingresar a la ruta: `http://localhost:5173/`
