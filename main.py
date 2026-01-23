import pygame
import sys
from assets_loading_system import AssetManager
from your_ship import Player
from assembly import AssemblyScene
from gacha import spin_gacha


class GameMaster:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("艦隊RPG：リファイン版")
        self.clock = pygame.time.Clock()
        self.assets = AssetManager()
        self.player = Player()
        self.assembly = AssemblyScene(self.player)

        self.state = "MENU"
        self.options = ["ガチャを引く", "編成ドック", "出撃", "終了"]
        self.idx = 0
        self.font = pygame.font.SysFont("msgothic", 30)

    def run(self):
        while True:
            self.screen.fill((20, 20, 25))
            self.handle_input()

            if self.state == "MENU":
                self.draw_menu()
            elif self.state == "ASSEMBLY":
                self.assembly.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(30)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.state == "ASSEMBLY":
                if self.assembly.handle_event(event) == "MENU":
                    self.state = "MENU"

            elif self.state == "MENU" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.idx = (self.idx - 1) % len(self.options)
                if event.key == pygame.K_DOWN:
                    self.idx = (self.idx + 1) % len(self.options)
                if event.key == pygame.K_RETURN:
                    self.execute_menu()

    def execute_menu(self):
        if self.idx == 0:  # ガチャを引く
            new_items = spin_gacha(1)
            for item in new_items:
                # ここで Player の inventory に追加！
                self.player.add_to_inventory(item)
                print(f"【獲得】: {item['name']} (レア度: {item['rarity']})")

        elif self.idx == 1:  # 編成画面へ
            self.state = "ASSEMBLY"

    def draw_menu(self):
        for i, opt in enumerate(self.options):
            color = (0, 255, 100) if i == self.idx else (255, 255, 255)
            txt = self.font.render(opt, True, color)
            self.screen.blit(txt, (300, 200 + i * 60))


if __name__ == "__main__":
    GameMaster().run()
