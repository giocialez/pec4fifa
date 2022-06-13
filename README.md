# PEC 4.

El paquete que se va a describir a continuación contiene las soluciones de la PEC4.

El paquete está dividido entre 3 archivos principales:

- `graficos` contiene las funciones para mostrar gráficos en pantalla.
- `funciones` contiene las funciones definidas para solucionar la PEC.
- `main` es el documento principal, el cual será ejecutado.

Por otra parte el paquete contiene los siguientes archivos/carpetas:

- 'data' carpeta donde se encuentran los archivos sobre los que se analiza la información.
- 'test' contiene los documentos para realizar los tests ṕúblicos y creados.
- 'test_imports' módulo que contiene las funciones a testear.
- 'requirements' fichero de texto con las librerías a descargar para que funcione el código.
- 'license'


## Pasos para ejecutar main.py

1. git clone https://github.com/giocialez/pec4fifa.git
2. cd ./pec4fifa
3. pip install -r requirements.txt
4. python main.py

### Pasos para ejecutar Test públicos

1. pip install HTMLTestRunner-rv
2. python3 -m tests.test_public

