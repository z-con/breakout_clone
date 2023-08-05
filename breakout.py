import curses
import time

# Define dimensions
BOARD_WIDTH = 120  # 3 times the original width
BOARD_HEIGHT = 60  # 3 times the original height

# Define ASCII characters for empty space and wall
EMPTY = ' '
WALL = '#'

# Define paddle dimensions and position
PADDLE_WIDTH = 18  # 3 times the original width
PADDLE_Y = BOARD_HEIGHT - 2
paddle_x = BOARD_WIDTH // 2

# Define ASCII character for paddle
PADDLE = '='

# Define initial ball position and velocity
ball_x = BOARD_WIDTH // 2
ball_y = BOARD_HEIGHT // 2
ball_dx = 1
ball_dy = -1

# Define ASCII character for ball
BALL = 'O'

# Define brick dimensions, position, and number
BRICK_WIDTH = 12  # 3 times the original width
BRICK_HEIGHT = 1
BRICK_START_Y = 1
BRICK_GAP = 6  # 3 times the original gap
NUM_BRICKS = 5

# Define ASCII character for bricks
BRICK = '*'

# Initialize a list to keep track of bricks
bricks = []

def create_bricks():
    for i in range(NUM_BRICKS):
        brick_x = i*(BRICK_WIDTH + BRICK_GAP) + 1
        brick_y = BRICK_START_Y
        bricks.append((brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT))

def draw_paddle(board, paddle_x):
    board[PADDLE_Y] = [EMPTY]*BOARD_WIDTH
    for i in range(paddle_x, paddle_x + PADDLE_WIDTH):
        board[PADDLE_Y][i] = PADDLE

def move_paddle(dx):
    global paddle_x
    paddle_x = max(min(paddle_x + dx, BOARD_WIDTH - PADDLE_WIDTH - 1), 1)

def draw_ball(board, ball_x, ball_y):
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            if board[y][x] == BALL:
                board[y][x] = EMPTY
    board[ball_y][ball_x] = BALL

def update_ball():
    global ball_x, ball_y, ball_dx, ball_dy
    ball_x += ball_dx
    ball_y += ball_dy
    if ball_x <= 0 or ball_x >= BOARD_WIDTH - 1:
        ball_dx *= -1
    if ball_y <= 0:
        ball_dy *= -1
    if ball_y == PADDLE_Y and paddle_x <= ball_x < paddle_x + PADDLE_WIDTH:
        ball_dy *= -1
    for brick in bricks:
        brick_x, brick_y, brick_width, brick_height = brick
        if brick_y <= ball_y < brick_y + brick_height and brick_x <= ball_x < brick_x + brick_width:
            bricks.remove(brick)
            ball_dy *= -1
            break

def draw_bricks(board):
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            if board[y][x] == BRICK:
                board[y][x] = EMPTY
    for brick_x, brick_y, brick_width, brick_height in bricks:
        for y in range(brick_y, brick_y + brick_height):
            for x in range(brick_x, brick_x + brick_width):
                board[y][x] = BRICK

def main(stdscr):
    global paddle_x, ball_x, ball_y
    # Set up the screen
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    # Create the initial game elements
    board = [[EMPTY]*BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            if x == 0 or x == BOARD_WIDTH-1 or y == 0 or y == BOARD_HEIGHT-1:
                board[y][x] = WALL
    create_bricks()
    draw_paddle(board, paddle_x)
    draw_ball(board, ball_x, ball_y)
    draw_bricks(board)

    # Game loop
    while True:
        # Draw the game board
        stdscr.clear()
        for row in board:
            stdscr.addstr(''.join(row) + '\n')

        # Update game state
        update_ball()
        draw_ball(board, ball_x, ball_y)
        if ball_y >= BOARD_HEIGHT - 1:
            stdscr.clear()
            stdscr.addstr(BOARD_HEIGHT // 2, BOARD_WIDTH // 2 - 4, 'Game Over')
            stdscr.addstr(BOARD_HEIGHT // 2 + 1, BOARD_WIDTH // 2 - 7, 'Retry? (y/n)')
            stdscr.refresh()
            c = stdscr.getch()
            while c not in [ord('y'), ord('n')]:
                c = stdscr.getch()
            if c == ord('y'):
                board = [[EMPTY]*BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
                for y in range(BOARD_HEIGHT):
                    for x in range(BOARD_WIDTH):
                        if x == 0 or x == BOARD_WIDTH-1 or y == 0 or y == BOARD_HEIGHT-1:
                            board[y][x] = WALL
                paddle_x = BOARD_WIDTH // 2
                ball_x = BOARD_WIDTH // 2
                ball_y = BOARD_HEIGHT // 2
                ball_dx = 1
                ball_dy = -1
                bricks = []
                create_bricks()
                draw_paddle(board, paddle_x)
                draw_ball(board, ball_x, ball_y)
                draw_bricks(board)
            else:
                break

        # Handle user input
        c = stdscr.getch()
        if c == ord('q'):
            break
        elif c == ord('a'):
            move_paddle(-5)
            draw_paddle(board, paddle_x)
        elif c == ord('d'):
            move_paddle(5)
            draw_paddle(board, paddle_x)

        # Delay to control game speed
        time.sleep(0.1)  # Increase delay to slow down the game

if __name__ == '__main__':
    curses.wrapper(main)
