# Usar una imagen base de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos de requisitos
COPY requirements.txt /app/

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código del proyecto
COPY . /app/

# Exponer el puerto en el que correrá el servidor Django
EXPOSE 8000

# Comando para ejecutar el servidor de desarrollo de Django

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
