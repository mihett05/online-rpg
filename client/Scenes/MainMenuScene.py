import pygame
import pygame_gui
import os
import sys
from client.Scene import Scene
from client.Scenes.SettingsScene import SettingsScene
from client.Scenes import CharsScene


class MainMenuScene(Scene):
    def __init__(self):
        self.bg = pygame.sprite.Sprite()
        Scene.__init__(self)
        self.sprites = pygame.sprite.Group()

        self.login, self.password, self.login_button, self.status = None, None, None, None
        self.init_ui()

    @staticmethod
    def load_image_ins(name):
        try:
            return pygame.image.load(os.path.join('data', name))
        except pygame.error:
            print("Can't load image data/{}".format(name))
            return pygame.image.load(os.path.join("data", "default.png")).convert()

    def init_ui(self):
        self.bg.image = pygame.transform.scale(self.load_image_ins('greenback4.jpg'),
                                          (self.size[0], self.size[1]))
        self.bg.rect = self.bg.image.get_rect()
        self.bg.rect.x = 0
        self.bg.rect.y = 0
        self.sprites.add(self.bg)

        self.status = None
        self.quit_button = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 2 - 120, self.size[1] / 2 - self.size[1] / 9 + 140, 240, 50), manager=self.ui,
            text="Выйти из игры"
        ))
        self.play_button = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 2 - 120, self.size[1] / 2 - self.size[1] / 9, 240, 50), manager=self.ui,
            text="Играть"
        ))
        self.settings_button = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 2 - 120, self.size[1] / 2 - self.size[1] / 9 + 70, 240, 50),
            manager=self.ui,
            text="Настройки"
        ))
        self.font = pygame.font.Font('data/AtariRevue.ttf', 26)
        self.logined_account = self.font.render("Аккаунт: {}".format(self.account["login"]), False, (0, 0, 0))

    def draw(self):
        self.sprites.draw(self.screen)
        self.screen.blit(self.logined_account, (self.size[0] / 40, self.size[1] - self.size[1] / 29))
        for sprite in self.sprites.spritedict.keys():
            sprite.update()

    def process_events(self, event):
        if self.scene_manager.name == "MainMenu":
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.play_button:
                        self.scene_manager.change("CharsScene", CharsScene)
                    elif event.ui_element == self.settings_button:
                        self.scene_manager.change("Settings", SettingsScene)
                    elif event.ui_element == self.quit_button:
                        self.data["close"]()
