                                              ---> Sopa de letras <---


- Funcionamiento del programa:
  - El programa debe de ejecutarse desde el archivo main.py
  - Al principio de la ejecucion se le pide al profesor ingresar palabras para jugar. En caso de que no haya ingresado palabras, se le pedirá que vuelva a ingresar palabras
  - Cada palabra ingresada pasara por un proceso de validacion
  - Una vez que haya ingresado palabras, se mostrará un reporte de palabras que generaron conflicto entre Pattern y Wikcionario (si es que hubo palabras en conflicto. En caso contrario se mostrará que no habrá reporte).
   A la hora de mostrar el menú, se le dará la posibilidad de elegir:
    --> Cantidad de palabras que se mostrarán para cada tipo
    --> Colores para cada tipo
    --> Orientacion del juego: Verticual u Horizontal
    --> Tipo de Ayuda. Si el tipo de ayuda elegido es Ninguno, se mostrarán las cantidades dispersas de palabras para cada tipo.
                       En caso de que no hubiese definciones, se le indicará con una ventana que no habrá definiciones disponibles
  - Si los colores se repiten, se le informará en que tipos se han repetido y se pedirá que ingrese nuevos colores.
  - Si para TODOS los tipos se seleccionan 0 cantidades, se le pedirá que, para almenos un tipo, se ingrese 1 o más palabras


                                  ------------------ ° --------------------

  Ventana de juego:
    --> Al iniciar el juego, al alumno se le mostrará una barra de selección donde podrá seleccionar el tipo de palabra que desea marcar,
      por tanto al tocar sobre una celda, se mostrará la misma coloreada con el color que haya elegido para ese tipo en el menu de configuración de la sopa de letras.

    --> Debajo, se mostrará la grilla con las palabras distribuidas.

    --> Del lado derecho de la grilla, se mostrará la ayuda que se haya elegido en el menu de configuración.


                                  ------------------ ° --------------------

  Forma de juego:
    --> El alumno tendrá la posibilidad de marcar las celdas que se corresponderán con las palabras distribuidas de los tipos.
    --> A la hora de seleccionar una celda, deberá elegir, de la barra de tipos, un tipo de palabra para que sea marcada con el color correspomdiente para ese tipo.
    --> Una vez que el alumno haya terminado de elegir las palabras y considere que ha completado la sopa de letras, se deberá presionar el boton "Terminar" el cual mostrará una ventana con una lista de palabras acertadas y no acertadas.


                                  ------------------ ° --------------------

  Informacion de la sopa de letras:
    ---> La distribución de palabras es al azar.
    --> Se seleccionaran palabras de forma aleatoria de acuerdo a la cantidad deseada, y que estén disponibles para cada tipo de palabra.
    --> Si la cantidad total de palabras elegidas entre los tipos es menor a 8, la grilla poseerá un tamaño máximo de 8 por la longitud de la palabra más larga de las elegidas, caso contrario, la grilla poseerá el tamaño correspondiente al tamaño de la palabra más grande y la cantidad de palabras elegidas


Autores: Azcona Marcos
         Alvarez Cristian Gabriel
