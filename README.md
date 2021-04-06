# AIVA_2021_Deteccion_de_actividad_grupo_F
Proyecto para la asignatura de Aplicaciones Industriales y comerciales del MUVA



#  GROUP F Detection
En este repositorio se irá desarrollando la aplicación de detección de posibles clientes de una tienda y la detección de las personas que finalmente acaban pasando a la tienda, desarrollandolo con una solución aplicando vision por computador.
<img src="./images/CAPTURA.png">
 
 
# AfluenceCounter
 - [Nombre de la aplicación](#Nombre-de-la-aplicación)
 - [Equipo de Desarrollo](#Equipo-de-Desarrollo)
 - [Profesores](#Profesores)
 - [Documentación de Requisitos](#Documentación-de-Requisitos)
 - [Presupuesto](#Presupuesto)
 - [Interfaz(MOCK-UP)](#Interfaz(MOCK-UP))
 - [Documento de diseño](#Documeto-de-diseño)
 - [Ejecución de la aplicación](#Ejecución-de-la-aplicación)
 - [Testing](#Testing)






## Nombre de la aplicación ##
AfluenceCounter

## Equipo de Desarrollo ##
| Name | Mail | GitHub |
| ---- | ---- | ------ |
| Israel Peñalver Sánchez | i.penalver.2016@alumnos.urjc.es | [IsraelSonseca](https://github.com/IsraelSonseca) |
| David Valladares Vigara |	d.valladaresv@alumnos.urjc.es |	[dvalladaresv](https://github.com/dvalladaresv) |
| Ales Darío Cevallos Juárez |	ad.cevallos@alumnos.urjc.es |	[AlexCeval](https://github.com/AlexCeval) |

## Profesores ##
| Name | Mail | GitHub |
| ---- | ---- | ------ |
| José Francisco Vélez Serrano | jose.velez@urjc.es | [jfvelezserrano](https://github.com/jfvelezserrano) |


## Documentación de Requisitos ##
[Documento de Requisitos](./docs/RequisitosDRS.pdf)

## Presupuesto ##
[Presupuesto](./docs/Presupuesto.pdf)

## INTERFAZ(MOCK-UP) ##
[Interfaz](./docs/mockup.pdf)

## Documento de diseño ##
[Documento de diseño](./docs/documento_de_diseño.pdf)

## Ejecución de la aplicación ##  

### Pre-requisitos    
- El proyecto se ha desarrollado utilizando la versión de python 3.8. Es necesario tener instalado [pip](https://pypi.org/project/pip/) para descargase las librerías necesarias. Se recomienda la creación de un entorno virtual para evitar problemas de dependencias, por ejemplo utilizando [virtualenv](https://virtualenv.pypa.io/en/latest/).   
- Es necesario instalarse las siguientes librerías.   
~~~
    pip install opencv-contrib-python==4.5.1.48
    pip install numpy==1.20.2
    pip install wget==3.2
~~~ 
- Para facilitar la instalación de todas las dependencias se proporciona un fichero [requierements.txt](code/requierements.txt) que se encuentra dentro del directorio code/. Para lanzarlo dirigirse a este directorio y lanzar:
~~~
    pip install -r ./code/requierements.txt
~~~
- Es necesario descargase los pesos de la red Yolo en el directorio [/code/assests/model](/code/assests/model). Para ello ejecutar los siguientes comandos:
~~~ 
cd ./code/assets/model 
wget https://pjreddie.com/media/files/yolov3.weights
~~~ 

### Descargar el repositorio
- Se recomienda utilizar la herramienta de control de versines [git](https://git-scm.com/) para clonarse el repositorio.  
~~~
    git clone https://github.com/dvalladaresv/AIVA_2021_Deteccion_de_actividad_grupo_F.git
~~~
- Si no desea instalarse git, puede descargarse el repositorio como un fichero comprimido .zip. 

### Ejecución

- El lanzamiento de la aplicación se puede realizar por línea de comandos ejecutando:

~~~
    python affluence_counter.py --video_path=<path_video>
~~~
- Un ejemplo de lanzamiento sería:
~~~
   python affluence_counter.py --video_path=../videos/1_EnterExitCrossingPaths1front.mpg
~~~

## Testing ##

- Las [pruebas unitarias](./code/test/) se ecuentran dentro de code/test/. El lanzamiento de un test se puede realizar por línea de comandos ejecutando:   
~~~
    python <test>.py
~~~ 

- Un ejemplo de lanzamiento sería:
~~~
   python test_tracker.py
~~~
    


