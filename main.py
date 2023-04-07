import pygame
import random
import time

# 初始化 Pygame
pygame.init()

# 定義遊戲視窗大小
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

# 設置視窗
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 設置字型和字型大小
font = pygame.font.Font(None, 36)

# 定義牌的數量和大小
card_width = 70
card_height = 100
cards = []
for i in range(4):
    for j in range(1, 14):
        cards.append((i, j))

# 初始化遊戲狀態
game_over = False
result_text = ""

# 定義翻牌流程變數
is_hole_card = True
card1 = None
card2 = None
card3 = None

# 定義下注金額
bet = 10

# 創建字典儲存每個玩家的籌碼數量
num_players = 0
player_chips = {}
current_player = 1

screen.fill((255, 255, 255))
pygame.display.update()


def choosePlayer(num_players):
    # 選擇玩家數量
    confirm = False
    while not confirm:
        # 事件處理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if up_button.collidepoint(pygame.mouse.get_pos()):
                    num_players += 1
                elif down_button.collidepoint(pygame.mouse.get_pos()):
                    if num_players > 0:
                        num_players -= 1
                elif confirm_button.collidepoint(pygame.mouse.get_pos()):
                    confirm = True
                    break
        # 繪製界面
        screen.fill((255, 255, 255))
        num_players_text = font.render("Choose the number of players:", True, (0, 0, 0))
        screen.blit(num_players_text, (WINDOW_WIDTH // 2 - num_players_text.get_width() // 2, 100))

        up_button = pygame.Rect(WINDOW_WIDTH // 2 + 50, 200, 50, 50)
        up_text = font.render("up", True, (0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), up_button)
        screen.blit(up_text,
                    (up_button.centerx - up_text.get_width() // 2, up_button.centery - up_text.get_height() // 2))
        if up_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (200, 200, 200), up_button)

        num_players_text = font.render(str(num_players), True, (0, 0, 0))
        screen.blit(num_players_text, (WINDOW_WIDTH // 2 - num_players_text.get_width() // 2, 210))

        down_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, 200, 50, 50)
        down_text = font.render("down", True, (0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), down_button)
        screen.blit(down_text, (down_button.centerx - down_text.get_width() // 2,
                                down_button.centery - down_text.get_height() // 2))
        if down_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (200, 200, 200), down_button)

        confirm_button = pygame.Rect(WINDOW_WIDTH // 2 - 75, 300, 150, 50)
        confirm_text = font.render("Confirm", True, (0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), confirm_button)
        screen.blit(confirm_text, (confirm_button.centerx - confirm_text.get_width() // 2,
                                   confirm_button.centery - confirm_text.get_height() // 2))
        if confirm_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (200, 200, 200), confirm_button)

        pygame.display.update()
    # 為每個玩家初始化籌碼數量
    for i in range(num_players):
        player_chips[f"Player {i + 1}"] = -10
    screen.fill((255, 255, 255))
    pygame.display.update()
    pool = bet * num_players
    # 返回玩家數量和每個玩家的籌碼數量
    return num_players, player_chips, pool


def bet_choose(pool, card1, card2):
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)

    # 定義滑塊位置和大小
    slider_x = WINDOW_WIDTH // 2 - 100
    slider_y = 275
    slider_width = 200
    slider_height = 15

    # 定義滑塊範圍
    slider_min = 10
    slider_max = pool
    slider_value = slider_min

    up_down = 0

    dragging = False
    confirm = False
    while not confirm:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # 如果鼠雕點擊在滑塊上，就開始拖動滑塊
                if slider_x <= mouse_x <= slider_x + slider_width and slider_y <= mouse_y <= slider_y + slider_height:
                    dragging = True
                elif confirm_button.collidepoint(pygame.mouse.get_pos()):
                    if card1[1] == card2[1] and up_down == 0:
                        confirm = False
                    else:
                        confirm = True
                    break
                if up_button.collidepoint(pygame.mouse.get_pos()):
                    up_down = 1
                elif down_button.collidepoint(pygame.mouse.get_pos()):
                    up_down = 2
            elif event.type == pygame.MOUSEBUTTONUP:
                # 如果鼠標松开，就停止拖動滑塊
                dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                # 如果鼠標移動並且正在拖動滑塊，就更新滑塊的值
                mouse_x, mouse_y = event.pos
                # 限制滑塊只能在水平方向移動
                if mouse_x < slider_x:
                    slider_value = slider_min
                elif mouse_x > slider_x + slider_width:
                    slider_value = slider_max
                else:
                    # 將滑塊位置映射到滑塊值上
                    slider_value = int(
                        (mouse_x - slider_x) / slider_width * (slider_max - slider_min) + slider_min) // 10 * 10

        screen.fill((255, 255, 255))
        screen.blit(card1_img, (50, 50))
        screen.blit(card2_img, (200, 50))
        pool_surface = font.render(f"Pool: {pool}", True, (0, 0, 0))
        screen.blit(pool_surface, (WINDOW_WIDTH // 2 - pool_surface.get_width() // 2, 250))

        up_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, 315, 50, 50)
        up_text = font.render("up", True, (0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), up_button)

        down_button = pygame.Rect(WINDOW_WIDTH // 2 + 50, 315, 50, 50)
        down_text = font.render("down", True, (0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), down_button)

        if card1[1] == card2[1]:
            screen.blit(up_text, (up_button.centerx - up_text.get_width() // 2,
                                  up_button.centery - up_text.get_height() // 2))
            if up_button.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (200, 200, 200), up_button)
            screen.blit(down_text, (down_button.centerx - down_text.get_width() // 2,
                                    down_button.centery - down_text.get_height() // 2))
            if down_button.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (200, 200, 200), down_button)

        if up_down == 1:
            pygame.draw.rect(screen, (200, 200, 200), up_button)
        elif up_down == 2:
            pygame.draw.rect(screen, (200, 200, 200), down_button)
        confirm_button = pygame.Rect(WINDOW_WIDTH // 2 - 75, 375, 150, 50)
        confirm_text = font.render("Confirm", True, (0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), confirm_button)
        screen.blit(confirm_text, (confirm_button.centerx - confirm_text.get_width() // 2,
                                   confirm_button.centery - confirm_text.get_height() // 2))
        if confirm_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (200, 200, 200), confirm_button)
        # 顯示玩家的籌碼數量
        player_chips_surface = font.render(f"Player {current_player}: {player_chips[f'Player {current_player}']}",
                                           True,
                                           (0, 0, 0))
        screen.blit(player_chips_surface,
                    (WINDOW_WIDTH // 2 - player_chips_surface.get_width() // 2, 450))
        # 繪製滑塊
        pygame.draw.rect(screen, BLACK, [slider_x, slider_y, slider_width, slider_height])
        if pool <= 10:
            slider_pos = 10 * slider_width + slider_x
        else:
            slider_pos = (slider_value - slider_min) / (slider_max - slider_min) * slider_width + slider_x
        pygame.draw.circle(screen, GRAY, (int(slider_pos), slider_y + slider_height // 2), slider_height // 2)

        # 顯示當前值
        text = font.render(str(slider_value), True, BLACK)
        screen.blit(text, (slider_x + slider_width + 10, slider_y - 10))

        # 刷新
        pygame.display.update()
    return slider_value, up_down


# 初始玩家人數、籌碼
num_players, player_chips, pool = choosePlayer(num_players)

while True:
    # 限制偵率
    pygame.time.Clock().tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # 退出遊戲
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
            # 點擊鼠標，進行下一回合
            game_over = False
            result_text = ""
            is_hole_card = True
            # 清除畫面
            screen.fill((255, 255, 255))
            pool_surface = font.render(f"Pool: {pool}", True, (0, 0, 0))
            screen.blit(pool_surface, (WINDOW_WIDTH // 2 - pool_surface.get_width() // 2, 250))
            pygame.display.update()

        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            screen.fill((255, 255, 255))
            pool_surface = font.render(f"Pool: {pool}", True, (0, 0, 0))
            screen.blit(pool_surface, (WINDOW_WIDTH // 2 - pool_surface.get_width() // 2, 250))
            # 顯示玩家的籌碼數量
            player_chips_surface = font.render(f"Player {current_player}: {player_chips[f'Player {current_player}']}",
                                               True,
                                               (0, 0, 0))
            screen.blit(player_chips_surface,
                        (WINDOW_WIDTH // 2 - player_chips_surface.get_width() // 2, 450))
            pygame.display.update()
            if is_hole_card:
                # 翻開第一張牌
                random.shuffle(cards)
                card1 = cards[0]
                card1_img = pygame.image.load(f'cards/{card1[0]}_{card1[1]}.jpg')
                screen.blit(card1_img, (50, 50))
                is_hole_card = False
                # 翻開第二張牌，比較大小
                card2 = cards[1]
                card2_img = pygame.image.load(f'cards/{card2[0]}_{card2[1]}.jpg')
                screen.blit(card2_img, (200, 50))
                pygame.display.update()
            # 第三張牌
            else:
                # 清除重整畫面
                screen.fill((255, 255, 255))
                screen.blit(card1_img, (50, 50))
                screen.blit(card2_img, (200, 50))

                bet, up_down = bet_choose(pool, card1, card2)
                # 翻開第三張牌，比較大小
                # 玩家下注
                # 清除重整畫面
                screen.fill((255, 255, 255))
                screen.blit(card1_img, (50, 50))
                screen.blit(card2_img, (200, 50))

                card3 = cards[2]
                card3_img = pygame.image.load(f'cards/{card3[0]}_{card3[1]}.jpg')
                screen.blit(card3_img, (350, 50))
                pygame.display.update()

                if card1[1] == card2[1]:
                    if (up_down == 1 or up_down == 2) and card1[1] == card3[1]:
                        result_text = 'LOSE Triple'
                        player_chips[f"Player {current_player}"] -= 3 * bet
                        pool += 3 * bet
                    # 選上
                    elif up_down == 1:
                        if card1[1] < card3[1]:
                            result_text = 'WIN'
                            # 獲得底池中的金額
                            player_chips[f"Player {current_player}"] += bet
                            pool -= bet
                        else:
                            result_text = 'LOSE'
                            # 投入金額到底池中
                            player_chips[f"Player {current_player}"] -= bet
                            pool += bet
                    else:
                        if card1[1] > card3[1]:
                            result_text = 'WIN'
                            # 獲得底池中的金額
                            player_chips[f"Player {current_player}"] += bet
                            pool -= bet
                        else:
                            result_text = 'LOSE'
                            # 投入金額到底池中
                            player_chips[f"Player {current_player}"] -= bet
                            pool += bet

                else:
                    if card1[1] == card3[1] or card2[1] == card3[1]:
                        result_text = 'LOSE Double'
                        player_chips[f"Player {current_player}"] -= 2 * bet
                        pool += 2 * bet
                    elif (card1[1] < card3[1] < card2[1]) or (card2[1] < card3[1] < card1[1]):
                        result_text = 'WIN'
                        # 獲得底池中的金額
                        player_chips[f"Player {current_player}"] += bet
                        pool -= bet
                    else:
                        result_text = 'LOSE'
                        # 投入金額到底池中
                        player_chips[f"Player {current_player}"] -= bet
                        pool += bet


                if pool <= 0:
                    for i in range(num_players):
                        player_chips[f"Player {i + 1}"] -= 10
                    pool = 10 * num_players
                is_hole_card = True
                # 標記遊戲結束
                game_over = True

            if game_over:
                # 顯示勝負結果
                result_surface = font.render(result_text, True, (0, 0, 0))
                screen.blit(result_surface, (WINDOW_WIDTH // 2 - result_surface.get_width() // 2, 200))

                # 顯示玩家的籌碼數量
                player_chips_surface = font.render(
                    f"Player {current_player}: {player_chips[f'Player {current_player}']}", True,
                    (0, 0, 0))
                screen.blit(player_chips_surface,
                            (WINDOW_WIDTH // 2 - player_chips_surface.get_width() // 2, 450))
                pool_surface = font.render(f"Pool: {pool}", True, (0, 0, 0))
                screen.blit(pool_surface, (WINDOW_WIDTH // 2 - pool_surface.get_width() // 2, 250))
                print(pool)
                print(player_chips)

                if current_player < num_players:
                    current_player += 1
                else:
                    current_player = 1

            pygame.display.update()
pygame.quit()
