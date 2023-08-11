# AI_JUEGO

Heuristica:
https://roadtolarissa.com/connect-4-ai-how-it-works/

Ejemplo:
https://github.com/KeithGalli/Connect4-Python


Explicación heuristica según GPT:

¡Por supuesto! Esta heurística es utilizada para evaluar la posición de un tablero en el juego "4 en línea" y asignarle un puntaje a esa posición en función de la probabilidad de ganar para el jugador que controla las fichas en juego.

Voy a explicar paso a paso cómo funciona la heurística y qué hace cada parte del código:

1. `evaluate_window(window, piece)`: Esta función recibe una ventana (window) de longitud 4 y una pieza (piece) que puede ser la del jugador humano (PLAYER_PIECE) o la de la IA (AI_PIECE). Evalúa la ventana y asigna un puntaje a la misma en función de la cantidad y distribución de piezas en esa ventana. Veamos cómo se calcula el puntaje:

   - Si hay 4 piezas del mismo jugador en la ventana, se suma 100 al puntaje.
   - Si hay 3 piezas del mismo jugador y una casilla vacía (EMPTY) en la ventana, se suma 5 al puntaje.
   - Si hay 2 piezas del mismo jugador y 2 casillas vacías en la ventana, se suma 2 al puntaje.
   - Si hay 3 piezas del oponente (opp_piece) y una casilla vacía en la ventana, se resta 4 al puntaje.

2. `score_position(board, piece)`: Esta función recibe el tablero actual y la pieza para la que se está calculando el puntaje (jugador humano o IA). Evalúa el tablero en busca de posibles formaciones de 4 fichas en línea en todas las direcciones posibles (horizontal, vertical y diagonales) y asigna un puntaje total para la posición.

   - Se otorgan puntos basados en la cantidad de piezas del jugador en el centro de la columna del tablero.
   - Se evalúa horizontalmente cada fila del tablero buscando ventanas de longitud 4 y se llama a `evaluate_window` para calcular el puntaje de cada ventana.
   - Se evalúa verticalmente cada columna del tablero buscando ventanas de longitud 4 y se llama a `evaluate_window` para calcular el puntaje de cada ventana.
   - Se evalúan las diagonales positivas (de izquierda a derecha, de arriba a abajo) buscando ventanas de longitud 4 y se llama a `evaluate_window` para calcular el puntaje de cada ventana.
   - Se evalúan las diagonales negativas (de izquierda a derecha, de abajo a arriba) buscando ventanas de longitud 4 y se llama a `evaluate_window` para calcular el puntaje de cada ventana.

3. El puntaje total para la posición se calcula sumando los puntajes obtenidos en cada uno de los pasos anteriores.

En resumen, esta heurística intenta asignar un valor numérico a una posición del tablero en función de la cantidad y distribución de las piezas del jugador y el oponente. Cuanto mayor sea el puntaje, más favorable será la posición para el jugador que controla las piezas evaluadas.
