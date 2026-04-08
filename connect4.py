from kandinsky import *
from ion import *
from time import sleep

GRID = (20, 40, 200)
RED = (220, 40, 40)
YELLOW = (240, 220, 0)
BLUE = (50, 120, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ROWS = 6
COLS = 7
CELL = 24
OX = 70
OY = 30
score_r = 0
score_y = 0


def create_board():
    return [[0]*COLS for _ in range(ROWS)]


def disc(cx, cy, r, color):
    for y in range(-r, r):
        for x in range(-r, r):
            if x*x + y*y <= r*r:
                set_pixel(cx+x, cy+y, color)


def draw_ui():
    fill_rect(0, 0, 70, 240, BLACK)
    fill_rect(250, 0, 70, 240, BLACK)
    fill_rect(0, 190, 320, 50, BLACK)
    draw_string("P-1", 10, 20, WHITE, BLACK)
    disc(25, 50, 8, RED)
    draw_string("Score:", 10, 80, WHITE, BLACK)
    draw_string(str(score_r), 10, 100, WHITE, BLACK)
    draw_string("P-2", 260, 20, WHITE, BLACK)
    disc(275, 50, 8, YELLOW)
    draw_string("Score:", 260, 80, WHITE, BLACK)
    draw_string(str(score_y), 260, 100, WHITE, BLACK)


def draw_board(board, win=None):
    for r in range(ROWS):
        for c in range(COLS):
            x = OX + c*CELL
            y = OY + r*CELL

            fill_rect(x, y, CELL, CELL, GRID)

            cx = x + CELL//2
            cy = y + CELL//2

            val = board[r][c]

            color = WHITE
            if val == 1:
                color = RED
            elif val == 2:
                color = YELLOW

            disc(cx, cy, CELL//2 - 3, color)

            if win and (r, c) in win:
                disc(cx, cy, 5, BLUE)


def draw_cursor(col, player):
    cx = OX + col*CELL + CELL//2
    cy = OY - CELL//2

    color = RED if player == 1 else YELLOW
    disc(cx, cy, CELL//2 - 3, color)


def clear_cursor(col):
    fill_rect(OX + col*CELL, OY-CELL, CELL, CELL, BLACK)


def column_full(board, col):
    return board[0][col] != 0


def get_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == 0:
            return r
    return -1


def wait_release():
    while keydown(KEY_LEFT) or keydown(KEY_RIGHT) or keydown(KEY_OK):
        pass


def animate(board, col, row, player):
    color = RED if player == 1 else YELLOW

    for r in range(row+1):
        x = OX + col*CELL
        y = OY + r*CELL
        if r > 0:
            fill_rect(x, OY+(r-1)*CELL, CELL, CELL, GRID)
            disc(x+CELL//2, OY+(r-1)*CELL+CELL//2, CELL//2-3, WHITE)
        fill_rect(x, y, CELL, CELL, GRID)
        disc(x+CELL//2, y+CELL//2, CELL//2-3, color)
        sleep(0.01)

def check_win(b, p):
    for r in range(ROWS):
        for c in range(COLS-3):
            if all(b[r][c+i]==p for i in range(4)):
                return [(r, c+i) for i in range(4)]

    for r in range(ROWS-3):
        for c in range(COLS):
            if all(b[r+i][c]==p for i in range(4)):
                return [(r+i, c) for i in range(4)]

    for r in range(ROWS-3):
        for c in range(COLS-3):
            if all(b[r+i][c+i]==p for i in range(4)):
                return [(r+i, c+i) for i in range(4)]

    for r in range(3, ROWS):
        for c in range(COLS-3):
            if all(b[r-i][c+i]==p for i in range(4)):
                return [(r-i, c+i) for i in range(4)]

    return None


def board_full(board):
    for c in range(COLS):
        if board[0][c] == 0:
            return False
    return True


def show_message(text):
    fill_rect(0, 190, 320, 50, BLACK)
    draw_string(text, 0, 200, WHITE, BLACK)


def game():
    global score_r, score_y

    board = create_board()
    player = 1
    col = 3

    fill_rect(0, 0, 320, 240, BLACK)
    draw_ui()
    draw_board(board)

    while True:
        draw_cursor(col, player)

        if keydown(KEY_LEFT):
            clear_cursor(col)
            col = max(0, col-1)
            wait_release()

        elif keydown(KEY_RIGHT):
            clear_cursor(col)
            col = min(COLS-1, col+1)
            wait_release()

        elif keydown(KEY_OK):

            if not column_full(board, col):

                row = get_row(board, col)
                animate(board, col, row, player)
                board[row][col] = player

                win = check_win(board, player)

                if win:
                    if player == 1:
                        score_r += 1
                        msg = "RED wins."
                    else:
                        score_y += 1
                        msg = "YELLOW wins."

                    draw_ui()
                    draw_board(board, win)
                    show_message(msg + " Press OK to continue")

                    while True:
                        if keydown(KEY_OK):
                            wait_release()
                            return

                elif board_full(board):
                    draw_ui()
                    draw_board(board)
                    show_message("Draw. Press OK to continue")

                    while True:
                        if keydown(KEY_OK):
                            wait_release()
                            return

                player = 2 if player == 1 else 1

            wait_release()


while True:
    game()
