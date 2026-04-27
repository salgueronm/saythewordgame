import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Say the Word!")

clock = pygame.time.Clock()

WHITE = (250, 246, 238)
BLACK = (20, 20, 35)
TEAL = (42, 169, 160)
RED = (230, 70, 70)
GREEN = (80, 200, 120)
GRAY = (230, 230, 230)
YELLOW = (255, 210, 60)

font_big = pygame.font.SysFont("arialblack", 52)
font_med = pygame.font.SysFont("arialblack", 28)
font_small = pygame.font.SysFont("arial", 22)
font_tiny = pygame.font.SysFont("arial", 18)

words = [
    ("🎩", "Hat"),
    ("🐱", "Cat"),
    ("🐶", "Dog"),
    ("⭐", "Star"),
    ("🍎", "Apple"),
    ("🚗", "Car"),
    ("🌙", "Moon"),
    ("🔥", "Fire")
]

round_num = 1
max_rounds = 5
score = 0
player_name = ""
name_active = True
game_started = False
show_sequence = False
current_input = ""
message = "Enter your name, pick a level, then click START"
difficulty = 1
sequence = []
flash_index = 0
flash_timer = 0
waiting_for_answer = False
answer_index = 0

leaderboard = []


def draw_button(rect, text, color):
    pygame.draw.rect(screen, color, rect, border_radius=12)
    pygame.draw.rect(screen, BLACK, rect, 4, border_radius=12)
    label = font_med.render(text, True, WHITE)
    screen.blit(label, label.get_rect(center=rect.center))


def draw_text(text, font, color, x, y, center=False):
    label = font.render(text, True, color)
    rect = label.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(label, rect)


def new_round():
    global sequence, flash_index, flash_timer, show_sequence, waiting_for_answer
    global answer_index, current_input, message

    card_count = 4 + difficulty * 2
    sequence = [random.choice(words) for _ in range(card_count)]
    flash_index = 0
    flash_timer = pygame.time.get_ticks()
    show_sequence = True
    waiting_for_answer = False
    answer_index = 0
    current_input = ""
    message = "Memorize the words as they light up!"


def finish_game():
    global game_started, message, leaderboard, player_name, score
    leaderboard.append((player_name if player_name else "Player", score))
    leaderboard = sorted(leaderboard, key=lambda x: x[1], reverse=True)[:5]
    game_started = False
    message = "Game finished! Your score was added to the leaderboard."


start_button = pygame.Rect(380, 560, 140, 55)
name_box = pygame.Rect(200, 170, 420, 45)

level_buttons = [
    (pygame.Rect(150, 230, 140, 40), 1, "LVL 1 - EASY"),
    (pygame.Rect(310, 230, 170, 40), 2, "LVL 2 - MEDIUM"),
    (pygame.Rect(500, 230, 150, 40), 3, "LVL 3 - HARD"),
    (pygame.Rect(670, 230, 170, 40), 4, "LVL 4 - EXTREME")
]

while True:
    screen.fill(WHITE)

    draw_text("SAY THE WORD!", font_big, BLACK, WIDTH // 2, 45, True)
    draw_text("ON THE BEAT CHALLENGE", font_small, RED, WIDTH // 2, 90, True)

    pygame.draw.rect(screen, WHITE, (60, 120, 600, 50), border_radius=10)
    pygame.draw.rect(screen, BLACK, (60, 120, 600, 50), 4, border_radius=10)
    draw_text("🎤  " + message, font_small, BLACK, 80, 135)

    pygame.draw.rect(screen, BLACK, (60, 178, 600, 35), border_radius=8)
    draw_text("MIC DEBUG: waiting for input...", font_tiny, TEAL, 80, 185)

    draw_text("Your Name:", font_small, BLACK, 70, 180)
    pygame.draw.rect(screen, WHITE, name_box, border_radius=8)
    pygame.draw.rect(screen, BLACK, name_box, 3, border_radius=8)
    draw_text(player_name if player_name else "Enter name...", font_small, BLACK, 215, 182)

    for rect, lvl, text in level_buttons:
        color = TEAL if difficulty == lvl else WHITE
        pygame.draw.rect(screen, color, rect, border_radius=20)
        pygame.draw.rect(screen, BLACK, rect, 3, border_radius=20)
        draw_text(text, font_tiny, BLACK if difficulty != lvl else WHITE, rect.centerx, rect.centery, True)

    pygame.draw.rect(screen, WHITE, (70, 290, 600, 240), border_radius=15)
    pygame.draw.rect(screen, BLACK, (70, 290, 600, 240), 4, border_radius=15)

    draw_text(f"ROUND {round_num} / {max_rounds}", font_med, BLACK, 90, 305)
    draw_text(f"⭐ {score}", font_med, BLACK, 570, 305)

    if not game_started:
        draw_text("Get ready — memorize these words!", font_small, BLACK, 260, 355, True)

        sample = sequence if sequence else [words[0], words[1], words[0], words[1]]
        x_start = 110
        for i in range(4):
            rect = pygame.Rect(x_start + i * 130, 390, 110, 90)
            pygame.draw.rect(screen, WHITE, rect, border_radius=8)
            pygame.draw.rect(screen, BLACK, rect, 3, border_radius=8)
            draw_text(sample[i][0], font_med, BLACK, rect.centerx, rect.centery - 10, True)
            draw_text(sample[i][1], font_tiny, BLACK, rect.centerx, rect.centery + 25, True)

        draw_button(start_button, "▶ START", TEAL)

    else:
        if show_sequence:
            now = pygame.time.get_ticks()
            if now - flash_timer > 1000:
                flash_index += 1
                flash_timer = now
                if flash_index >= len(sequence):
                    show_sequence = False
                    waiting_for_answer = True
                    message = "Type each word in order and press ENTER"

            for i, item in enumerate(sequence[:8]):
                row = i // 4
                col = i % 4
                rect = pygame.Rect(110 + col * 130, 370 + row * 85, 110, 70)
                color = GREEN if i == flash_index else WHITE
                pygame.draw.rect(screen, color, rect, border_radius=8)
                pygame.draw.rect(screen, BLACK, rect, 3, border_radius=8)
                draw_text(item[0], font_med, BLACK, rect.centerx, rect.centery - 8, True)
                draw_text(item[1], font_tiny, BLACK, rect.centerx, rect.centery + 22, True)

        elif waiting_for_answer:
            draw_text(f"Word {answer_index + 1} of {len(sequence)}", font_med, BLACK, WIDTH // 2 - 100, 360, True)
            draw_text("Type the word you remember:", font_small, BLACK, WIDTH // 2 - 100, 410, True)

            input_rect = pygame.Rect(230, 440, 300, 45)
            pygame.draw.rect(screen, GRAY, input_rect, border_radius=8)
            pygame.draw.rect(screen, BLACK, input_rect, 3, border_radius=8)
            draw_text(current_input, font_small, BLACK, 245, 452)

    pygame.draw.rect(screen, WHITE, (700, 120, 160, 210), border_radius=15)
    pygame.draw.rect(screen, BLACK, (700, 120, 160, 210), 4, border_radius=15)
    draw_text("🏆 LEADERBOARD", font_small, BLACK, 780, 145, True)

    if leaderboard:
        y = 185
        for i, (name, pts) in enumerate(leaderboard, 1):
            draw_text(f"{i}. {name}: {pts}", font_tiny, BLACK, 720, y)
            y += 30
    else:
        draw_text("No scores yet!", font_tiny, BLACK, 780, 210, True)

    pygame.draw.rect(screen, WHITE, (70, 545, 600, 80), border_radius=12)
    pygame.draw.rect(screen, BLACK, (70, 545, 600, 80), 3, border_radius=12)
    draw_text("HOW TO PLAY", font_tiny, RED, 90, 555)
    draw_text("1. Enter your name and pick a level.", font_tiny, BLACK, 90, 580)
    draw_text("2. Press START and memorize the flashing words.", font_tiny, BLACK, 90, 600)
    draw_text("3. Type each word in order to score points.", font_tiny, BLACK, 90, 620)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if name_box.collidepoint(event.pos):
                name_active = True

            for rect, lvl, text in level_buttons:
                if rect.collidepoint(event.pos):
                    difficulty = lvl

            if start_button.collidepoint(event.pos) and not game_started:
                round_num = 1
                score = 0
                game_started = True
                new_round()

        if event.type == pygame.KEYDOWN:
            if name_active and not game_started:
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.key != pygame.K_RETURN:
                    player_name += event.unicode

            elif waiting_for_answer:
                if event.key == pygame.K_BACKSPACE:
                    current_input = current_input[:-1]
                elif event.key == pygame.K_RETURN:
                    correct_word = sequence[answer_index][1].lower()

                    if current_input.strip().lower() == correct_word:
                        score += 10

                    current_input = ""
                    answer_index += 1

                    if answer_index >= len(sequence):
                        round_num += 1
                        if round_num > max_rounds:
                            finish_game()
                        else:
                            new_round()
                else:
                    current_input += event.unicode

    pygame.display.flip()
    clock.tick(60)
