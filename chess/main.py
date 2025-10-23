import pygame

pygame.init()
# Get screen info for fullscreen
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Two-Player Pygame Chess!')
font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 40)
big_font = pygame.font.Font('freesansbold.ttf', 50)
timer = pygame.time.Clock()
fps = 60

# Chess board size and positioning
BOARD_SIZE = min(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200)  # Leave more space for UI
SQUARE_SIZE = BOARD_SIZE // 8

# Calculate board position to center it with space for status bar
BOARD_X = (SCREEN_WIDTH - BOARD_SIZE) // 2
BOARD_Y = (SCREEN_HEIGHT - BOARD_SIZE - 100) // 2  # Leave space for status bar at bottom

# Status bar positioning
STATUS_HEIGHT = 100
STATUS_Y = SCREEN_HEIGHT - STATUS_HEIGHT

# game variables and images
white_pieces = [
    'rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn'
]
white_locations = [
    (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
    (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)
]

black_pieces = [
    'rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn'
]
black_locations = [
    (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
    (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)
]

captured_pieces_white = []
captured_pieces_black = []

# turn_step:
# 0 - white's turn no selection
# 1 - white's turn piece selected
# 2 - black turn no selection
# 3 - black turn piece selected
turn_step = 0
selection = 100
valid_moves = []

# load in game piece images (queen, king, rook, bishop, knight, pawn) x 2
# Update these paths to point to where your assets actually are.
ASSET_BASE = r'C:\Users\A\Desktop\chess'

black_queen = pygame.image.load(fr'{ASSET_BASE}\black queen (1).png')
black_queen = pygame.transform.scale(black_queen, (SQUARE_SIZE - 20, SQUARE_SIZE - 20))
black_queen_small = pygame.transform.scale(black_queen, (45, 45))

black_king = pygame.image.load(fr'{ASSET_BASE}\black king.png')
black_king = pygame.transform.scale(black_king, (SQUARE_SIZE - 20, SQUARE_SIZE - 20))
black_king_small = pygame.transform.scale(black_king, (45, 45))

black_rook = pygame.image.load(fr'{ASSET_BASE}\black rook.png')
black_rook = pygame.transform.scale(black_rook, (SQUARE_SIZE - 20, SQUARE_SIZE - 20))
black_rook_small = pygame.transform.scale(black_rook, (45, 45))

black_bishop = pygame.image.load(fr'{ASSET_BASE}\black bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (SQUARE_SIZE - 20, SQUARE_SIZE - 20))
black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))

black_knight = pygame.image.load(fr'{ASSET_BASE}\black knight.png')
black_knight = pygame.transform.scale(black_knight, (SQUARE_SIZE - 20, SQUARE_SIZE - 20))
black_knight_small = pygame.transform.scale(black_knight, (45, 45))

black_pawn = pygame.image.load(fr'{ASSET_BASE}\black pawn (1).png')
black_pawn = pygame.transform.scale(black_pawn, (SQUARE_SIZE - 35, SQUARE_SIZE - 35))
black_pawn_small = pygame.transform.scale(black_pawn, (45, 45))

white_queen = pygame.image.load(fr'{ASSET_BASE}\white queen.png')
white_queen = pygame.transform.scale(white_queen, (SQUARE_SIZE - 20, SQUARE_SIZE - 20))
white_queen_small = pygame.transform.scale(white_queen, (45, 45))

white_king = pygame.image.load(fr'{ASSET_BASE}\white king.png')
white_king = pygame.transform.scale(white_king, (SQUARE_SIZE - 20, SQUARE_SIZE - 20))
white_king_small = pygame.transform.scale(white_king, (45, 45))

white_rook = pygame.image.load(fr'{ASSET_BASE}\white rook.png')
white_rook = pygame.transform.scale(white_rook, (SQUARE_SIZE - 20, SQUARE_SIZE - 20))
white_rook_small = pygame.transform.scale(white_rook, (45, 45))

white_bishop = pygame.image.load(fr'{ASSET_BASE}\white bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (SQUARE_SIZE - 20, SQUARE_SIZE - 20))
white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))

white_knight = pygame.image.load(fr'{ASSET_BASE}\white knight.png')
white_knight = pygame.transform.scale(white_knight, (SQUARE_SIZE - 20, SQUARE_SIZE - 20))
white_knight_small = pygame.transform.scale(white_knight, (45, 45))

white_pawn = pygame.image.load(fr'{ASSET_BASE}\white pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (SQUARE_SIZE - 35, SQUARE_SIZE - 35))
white_pawn_small = pygame.transform.scale(white_pawn, (45, 45))

white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small, white_rook_small,
                      white_bishop_small]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small, black_rook_small,
                      black_bishop_small]
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

# check variables / flashing counter
counter = 0
winner = ''
game_over = False


# ---------- drawing functions ----------

def draw_board():
    # Draw the main board background
    pygame.draw.rect(screen, 'dark gray', [BOARD_X, BOARD_Y, BOARD_SIZE, BOARD_SIZE])

    # Draw alternating light gray squares
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 0:
                color = 'light gray'
            else:
                color = 'dark gray'
            pygame.draw.rect(screen, color,
                             [BOARD_X + col * SQUARE_SIZE,
                              BOARD_Y + row * SQUARE_SIZE,
                              SQUARE_SIZE, SQUARE_SIZE])

    # Draw board border
    pygame.draw.rect(screen, 'gold', [BOARD_X, BOARD_Y, BOARD_SIZE, BOARD_SIZE], 5)

    # Draw status area at the bottom (separate from board)
    pygame.draw.rect(screen, 'gray', [0, STATUS_Y, SCREEN_WIDTH, STATUS_HEIGHT])
    pygame.draw.rect(screen, 'gold', [0, STATUS_Y, SCREEN_WIDTH, STATUS_HEIGHT], 5)

    status_text = [
        'White: Select a Piece to Move!', 'White: Select a Destination!',
        'Black: Select a Piece to Move!', 'Black: Select a Destination!'
    ]
    screen.blit(big_font.render(status_text[turn_step], True, 'black'), (20, STATUS_Y + 20))

    # Draw forfeit button in status area
    forfeit_width = 150
    forfeit_x = SCREEN_WIDTH - forfeit_width - 20
    forfeit_y = STATUS_Y + 20
    pygame.draw.rect(screen, 'red', [forfeit_x, forfeit_y, forfeit_width, 60])
    screen.blit(medium_font.render('FORFEIT', True, 'white'), (forfeit_x + 10, forfeit_y + 10))


def draw_pieces():
    # white pieces
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        x = BOARD_X + white_locations[i][0] * SQUARE_SIZE
        y = BOARD_Y + white_locations[i][1] * SQUARE_SIZE

        if white_pieces[i] == 'pawn':
            pawn_offset = (SQUARE_SIZE - (SQUARE_SIZE - 35)) // 2
            screen.blit(white_pawn, (x + pawn_offset, y + pawn_offset))
        else:
            piece_offset = (SQUARE_SIZE - (SQUARE_SIZE - 20)) // 2
            screen.blit(white_images[index], (x + piece_offset, y + piece_offset))

        if turn_step < 2 and selection == i:
            pygame.draw.rect(screen, 'red',
                             [x + 1, y + 1, SQUARE_SIZE - 2, SQUARE_SIZE - 2], 2)

    # black pieces
    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        x = BOARD_X + black_locations[i][0] * SQUARE_SIZE
        y = BOARD_Y + black_locations[i][1] * SQUARE_SIZE

        if black_pieces[i] == 'pawn':
            pawn_offset = (SQUARE_SIZE - (SQUARE_SIZE - 35)) // 2
            screen.blit(black_pawn, (x + pawn_offset, y + pawn_offset))
        else:
            piece_offset = (SQUARE_SIZE - (SQUARE_SIZE - 20)) // 2
            screen.blit(black_images[index], (x + piece_offset, y + piece_offset))

        if turn_step >= 2 and selection == i:
            pygame.draw.rect(screen, 'blue',
                             [x + 1, y + 1, SQUARE_SIZE - 2, SQUARE_SIZE - 2], 2)


# ---------- move-calculation functions ----------
# (These remain the same as your original code)
def check_options(pieces, locations, turn):
    all_moves_list = []
    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list = check_king(location, turn)
        else:
            moves_list = []
        all_moves_list.append(moves_list)
    return all_moves_list


def check_king(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations

    # 8 squares to check for king
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for dx, dy in targets:
        target = (position[0] + dx, position[1] + dy)
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list


def check_queen(position, color):
    moves_list = check_bishop(position, color)
    second_list = check_rook(position, color)
    for item in second_list:
        moves_list.append(item)
    return moves_list


def check_bishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations

    # four diagonal directions
    directions = [(1, -1), (-1, -1), (1, 1), (-1, 1)]
    for x, y in directions:
        path = True
        chain = 1
        while path:
            new_pos = (position[0] + (chain * x), position[1] + (chain * y))
            if new_pos not in friends_list and 0 <= new_pos[0] <= 7 and 0 <= new_pos[1] <= 7:
                moves_list.append(new_pos)
                if new_pos in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


def check_rook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations

    # four orthogonal directions
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for x, y in directions:
        path = True
        chain = 1
        while path:
            new_pos = (position[0] + (chain * x), position[1] + (chain * y))
            if new_pos not in friends_list and 0 <= new_pos[0] <= 7 and 0 <= new_pos[1] <= 7:
                moves_list.append(new_pos)
                if new_pos in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


def check_knight(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations

    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for dx, dy in targets:
        target = (position[0] + dx, position[1] + dy)
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list


def check_pawn(position, color):
    moves_list = []
    if color == 'white':
        direction = 1
        enemies = black_locations
        friends = white_locations
        start_row = 1
    else:
        direction = -1
        enemies = white_locations
        friends = black_locations
        start_row = 6

    # one forward
    forward = (position[0], position[1] + direction)
    if 0 <= forward[1] <= 7 and forward not in friends and forward not in enemies:
        moves_list.append(forward)

        # two squares from start
        two_forward = (position[0], position[1] + 2 * direction)
        if position[1] == start_row and 0 <= two_forward[
            1] <= 7 and two_forward not in friends and two_forward not in enemies:
            moves_list.append(two_forward)

    # capture moves
    for dx in (-1, 1):
        cap = (position[0] + dx, position[1] + direction)
        if 0 <= cap[0] <= 7 and 0 <= cap[1] <= 7 and cap in enemies:
            moves_list.append(cap)

    return moves_list


def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    if 0 <= selection < len(options_list):
        return options_list[selection]
    return []


def draw_valid(moves):
    color = 'red' if turn_step < 2 else 'blue'
    for m in moves:
        x = BOARD_X + m[0] * SQUARE_SIZE + SQUARE_SIZE // 2
        y = BOARD_Y + m[1] * SQUARE_SIZE + SQUARE_SIZE // 2
        pygame.draw.circle(screen, color, (x, y), 5)


def draw_captured():
    # Position captured pieces display on the right side
    captured_x = SCREEN_WIDTH - 100
    captured_y = 50

    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_black_images[index], (captured_x, captured_y + 50 * i))

    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_white_images[index], (captured_x + 50, captured_y + 50 * i))


def draw_check():
    global counter
    if turn_step < 2:
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]
            for i in range(len(black_options)):
                if king_location in black_options[i]:
                    if counter < 15:
                        x = BOARD_X + king_location[0] * SQUARE_SIZE
                        y = BOARD_Y + king_location[1] * SQUARE_SIZE
                        pygame.draw.rect(screen, 'dark red',
                                         [x + 1, y + 1, SQUARE_SIZE - 2, SQUARE_SIZE - 2], 5)
    else:
        if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    if counter < 15:
                        x = BOARD_X + king_location[0] * SQUARE_SIZE
                        y = BOARD_Y + king_location[1] * SQUARE_SIZE
                        pygame.draw.rect(screen, 'dark blue',
                                         [x + 1, y + 1, SQUARE_SIZE - 2, SQUARE_SIZE - 2], 5)


def draw_game_over():
    pygame.draw.rect(screen, 'black', [SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50, 400, 100])
    screen.blit(big_font.render(f'{winner} won the game!', True, 'white'),
                (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 40))
    screen.blit(font.render(f'Press ENTER to Restart!', True, 'white'),
                (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 + 10))


# ---------- main game loop setup ----------
black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')

run = True
while run:
    timer.tick(fps)
    if counter < 30:
        counter += 1
    else:
        counter = 0

    screen.fill('dark gray')
    draw_board()
    draw_pieces()
    draw_captured()
    draw_check()

    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            x_coord = event.pos[0]
            y_coord = event.pos[1]

            # Check if click is within board bounds
            if (BOARD_X <= x_coord < BOARD_X + BOARD_SIZE and
                    BOARD_Y <= y_coord < BOARD_Y + BOARD_SIZE):

                # Convert to board coordinates
                board_x = (x_coord - BOARD_X) // SQUARE_SIZE
                board_y = (y_coord - BOARD_Y) // SQUARE_SIZE
                click_coords = (board_x, board_y)

                # white's turn (turn_step 0 or 1)
                if turn_step <= 1:
                    if click_coords in white_locations:
                        selection = white_locations.index(click_coords)
                        if turn_step == 0:
                            turn_step = 1

                    if click_coords in valid_moves and selection != 100:
                        # move white piece
                        white_locations[selection] = click_coords
                        if click_coords in black_locations:
                            black_piece = black_locations.index(click_coords)
                            captured_pieces_white.append(black_pieces[black_piece])
                            if black_pieces[black_piece] == 'king':
                                winner = 'white'
                            black_pieces.pop(black_piece)
                            black_locations.pop(black_piece)

                        black_options = check_options(black_pieces, black_locations, 'black')
                        white_options = check_options(white_pieces, white_locations, 'white')
                        turn_step = 2
                        selection = 100
                        valid_moves = []

                # black's turn (turn_step 2 or 3)
                if turn_step >= 2:
                    if click_coords in black_locations:
                        selection = black_locations.index(click_coords)
                        if turn_step == 2:
                            turn_step = 3

                    if click_coords in valid_moves and selection != 100:
                        # move black piece
                        black_locations[selection] = click_coords
                        if click_coords in white_locations:
                            white_piece = white_locations.index(click_coords)
                            captured_pieces_black.append(white_pieces[white_piece])
                            if white_pieces[white_piece] == 'king':
                                winner = 'black'
                            white_pieces.pop(white_piece)
                            white_locations.pop(white_piece)

                        black_options = check_options(black_pieces, black_locations, 'black')
                        white_options = check_options(white_pieces, white_locations, 'white')
                        turn_step = 0
                        selection = 100
                        valid_moves = []

            # Check for forfeit button click (separate from board)
            forfeit_x = SCREEN_WIDTH - 170
            forfeit_y = STATUS_Y + 20
            if (forfeit_x <= x_coord <= forfeit_x + 150 and
                    forfeit_y <= y_coord <= forfeit_y + 60):
                if turn_step <= 1:
                    winner = 'black'
                else:
                    winner = 'white'

        # restart on ENTER after game over
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                game_over = False
                winner = ''
                white_pieces = [
                    'rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn'
                ]
                white_locations = [
                    (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                    (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)
                ]
                black_pieces = [
                    'rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn'
                ]
                black_locations = [
                    (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                    (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)
                ]
                captured_pieces_white = []
                captured_pieces_black = []
                turn_step = 0
                selection = 100
                valid_moves = []
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')

    if winner != '':
        game_over = True
        draw_game_over()

    pygame.display.flip()

pygame.quit()