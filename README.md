# prog2-25-B1
Trabajo de prog-2 sistema de gestión de reparto.

## Autores
* (Coordinador) [Pablo García Beltrá](https://github.com/pgb64)
* [Andrés Segurado Climent](https://github.com/Bonew24)
* [Jorge Izquierdo Baeza](https://github.com/jorgeizquierdo-git)
* [Guillermo Espinosa Ruiz](https://github.com/ruukhaUA)
* [Alejandro Parraga Sanchez](https://github.com/w4lexf)
* [Ignacio Mendoza Diaz](https://github.com/w4lexf)
* [Ignacio Mendoza Diaz](https://github.com/imd24)

## Profesor
[Miguel A. Teruel](https://github.com/materuel-ua)

## Requisitos
* Gestión de paquetes y artículos, incluyendo su creación, modificación y eliminación. Cada paquete deberá contener al menos un artículo y el sistema manejará los posibles errores derivados de su gestión. (Jorge Izquierdo Baeza)  
* Gestión de repartidores y furgonetas por provincia, estableciendo un sitema de estados para controlar la disponibilidad y optimizar la distribución de envíos.  (Alejandro Párraga Sánchez) 
* Generación y visualización de mapas interactivos con rutas optimizadas, calculando estimaciones de tiempo de entrega mediante integración con APIs como Google Maps y open Source Routing. (Pablo García Beltrá) 
* Almacenamiento y gestión de datos en una BD (info de paquetes, usuarios, repartidores...), desde la terminal se podrán consultar y modificar. (Andrés Segurado Climent) 
* Creación de una API que coordine la base de datos con el resto del programa y la interfaz de usuario, así como el login y la gestión de tokens. También un archivo main y unos menús que controlen el correcto flujo de ejecución (Guillermo Espinosa Ruiz) 
* Implementación de un sistema de simulación con variables ajustables (cantidad pedidos, nº repartidores...) usando métodos probabilísticos avanzados, esto permitirá experimentar en diferentes escenarios. (Ignacio Mendoza Díaz) 

## Instrucciones de instalación y ejecución
[//]: # (En primer lugar hay que activar el entorno virtual, para ello, ejecuta en la terminal el siguiente comando: python -m venv venvpaquetes) 
[//]: # (luego: source entorno_virtual/bin/activate.)
[//]: # (IMPORTANTE: No ejecutar en thonny, usar Visual Studio)

[//]: # (Ahora procedemos a instalar todas las dependencias:)

**pip install -r requirements.txt**

Haz pip install -r requirements.txt y tendras todo lo necesario para poder ejecutar la aplicación sin problemas.


## Resumen de la API
Se encuentra subida a pythonanywhere.com, al igual que la base de datos. La ruta de acceso es ruukha.pythonanywhere.com
Tiene distintas rutas con varios métodos para asegurar su correcta implementación
Por cómo está hecho este programa, no será necesario conocer el funcionamiento de la API para usarla, pero sí es interesante saber que en el instante en el que se cree, modifique o elimine un elemento, esos cambios se verán reflejados en tiempo real en la base de datos, que podrá ser accedida desde otra instancia del programa.