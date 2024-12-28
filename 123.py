import pygame
import random
import sys

# 初始化 pygame
pygame.init()

# 遊戲屏幕設置
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30  # 每個方塊的大小
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("俄羅斯方塊")

# 顏色設置
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

COLORS = [CYAN, BLUE, ORANGE, YELLOW, GREEN, MAGENTA, RED]

# 方塊形狀的定義
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
]

# 初始化遊戲
def init_game():
    board = [[0] * (SCREEN_WIDTH // BLOCK_SIZE) for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
    return board

# 顯示文字
def display_text(text, x, y, font, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# 旋轉方塊
def rotate(shape):
    return [list(reversed(col)) for col in zip(*shape)]

# 檢查方塊是否可以放置
def valid_move(board, shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                if x + off_x < 0 or x + off_x >= len(board[0]) or y + off_y >= len(board):
                    return False
                if y + off_y >= 0 and board[y + off_y][x + off_x]:
                    return False
    return True

# 將方塊放置到遊戲區域
def place_shape(board, shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                board[y + off_y][x + off_x] = 1
    return board

# 消除填滿的行
def clear_lines(board):
    full_lines = 0
    for y in range(len(board)):
        if all(board[y]):
            board.pop(y)
            board.insert(0, [0] * len(board[0]))
            full_lines += 1
    return full_lines

# 顯示遊戲區域
def draw_board(board):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            color = WHITE if cell == 0 else COLORS[cell - 1]
            pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, BLACK, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

# 遊戲主循環
def game_loop():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)
    
    board = init_game()
    current_shape = random.choice(SHAPES)
    current_color = random.choice(COLORS)
    current_pos = [5, 0]
    
    game_over = False
    while not game_over:
        screen.fill(BLACK)
        
        # 處理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new_pos = [current_pos[0] - 1, current_pos[1]]
                    if valid_move(board, current_shape, new_pos):
                        current_pos = new_pos
                elif event.key == pygame.K_RIGHT:
                    new_pos = [current_pos[0] + 1, current_pos[1]]
                    if valid_move(board, current_shape, new_pos):
                        current_pos = new_pos
                elif event.key == pygame.K_DOWN:
                    new_pos = [current_pos[0], current_pos[1] + 1]
                    if valid_move(board, current_shape, new_pos):
                        current_pos = new_pos
                elif event.key == pygame.K_UP:
                    new_shape = rotate(current_shape)
                    if valid_move(board, new_shape, current_pos):
                        current_shape = new_shape
        
        # 方塊下落
        if not game_over:
            new_pos = [current_pos[0], current_pos[1] + 1]
            if valid_move(board, current_shape, new_pos):
                current_pos = new_pos
            else:
                board = place_shape(board, current_shape, current_pos)
                cleared_lines = clear_lines(board)
                current_shape = random.choice(SHAPES)
                current_pos = [5, 0]
                if not valid_move(board, current_shape, current_pos):
                    game_over = True

        draw_board(board)
        # 顯示當前方塊
        for y, row in enumerate(current_shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, current_color, ((current_pos[0] + x) * BLOCK_SIZE, (current_pos[1] + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(screen, BLACK, ((current_pos[0] + x) * BLOCK_SIZE, (current_pos[1] + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
        
        # 顯示遊戲結束訊息
        if game_over:
            display_text("Game Over!", 100, 250, font, WHITE)

        pygame.display.update()
        clock.tick(10)  # 設置遊戲速度，控制方塊下落的速度

# 運行遊戲
game_loop()

# 結束遊戲
pygame.quit()
sys.exit()
