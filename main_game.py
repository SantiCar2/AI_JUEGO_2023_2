
# FUNCIONES DE JUEGO
def se_puede(board, col, ROWS): # Verificar si se puede poner una pieza en la columna
    return board[ROWS - 1][col] == 0 # Si la ultima fila de la columna esta vacia


def siguiente_fila_disp(board, col, ROWS): # Obtener la siguiente fila disponible
    for r in range(ROWS): # Recorrer las filas
        if board[r][col] == 0: # Si la fila esta vacia
            return r # Retornar la fila


def poner_pieza(board, row, col, piece): # Poner una pieza en el tablero
    board[row][col] = piece
    return board


def verificar_ganador(board, piece, COLS, ROWS): # Verificar si hay un ganador
    # Verificar horizontal
    for c in range(COLS - 3): # Recorrer las columnas excepto las ultimas 3
        for r in range(ROWS): # Recorrer las filas
            if (
                board[r][c] == piece
                and board[r][c + 1] == piece
                and board[r][c + 2] == piece
                and board[r][c + 3] == piece
            ): # Si hay 4 piezas iguales en horizontal
                return True

    # Verificar vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c] == piece
                and board[r + 2][c] == piece
                and board[r + 3][c] == piece
            ):
                return True

    # Verificar diagonal positiva
    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == piece
            ):
                return True

    # Verificar diagonal negativa
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if (
                board[r][c] == piece
                and board[r - 1][c + 1] == piece
                and board[r - 2][c + 2] == piece
                and board[r - 3][c + 3] == piece
            ):
                return True
    return False
def vaciar_tablero(board, COLS, ROWS): # Vaciar el tablero
    for row in range(ROWS):
        for col in range(COLS):
            board[row][col] = 0
    return board

def calcular_puntaje(board, ficha, COLS, ROWS): # Calcular el puntaje de un tablero
    puntaje = 0
    # Verificar horizontal
    for c in range(COLS - 3): # Recorrer las columnas excepto las ultimas 3
        arreglo_fila = [int(i) for i in list(board[r, :])]
        for r in range(ROWS): # Recorrer las filas
            opor = arreglo_fila[c : c + 4] # Obtener 4 elementos de la fila
            puntaje += oportunidad(opor, ficha) # Calcular el puntaje de la oportunidad
    # Verificar vertical
    for c in range(COLS):
        arreglo_col = [int(i) for i in list(board[:, c])]
        for r in range(ROWS - 3):
            opor = arreglo_col[r : r + 4]
            puntaje += oportunidad(opor, ficha)
    # Verificar diagonal positiva
    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            opor = [board[r + i][c + i] for i in range(4)]
            puntaje += oportunidad(opor, ficha)
    # Verificar diagonal negativa
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            opor = [board[r - i][c + i] for i in range(4)]
            puntaje += oportunidad(opor, ficha)
    return puntaje


def oportunidad(opor, ficha):
    puntaje = 0
    if opor.count(ficha) == 4: # Si hay 4 piezas iguales en horizontal
        puntaje += 100
    elif opor.count(ficha) == 3 and opor.count(0) == 1: # Si hay 3 piezas iguales y 1 vacia
        puntaje += 5
    elif opor.count(ficha) == 2 and opor.count(0) == 2: # Si hay 2 piezas iguales y 2 vacias
        puntaje += 2
    elif opor.count(ficha) == 1 and opor.count(0) == 3: # Si hay 1 pieza igual y 3 vacias
        puntaje += 1
    elif opor.count(0) == 1 and opor.count(ficha) == 0: # Si hay 1 vacia y 3 piezas diferentes
        puntaje -= 5
