import os
import zipfile
import json
import pygame
from client.SpriteFactory import SpriteFactory
from client.AppData import AppData


class Map:
    def __init__(self, maps_path):
        self.data = AppData()
        self.path = os.path.join("data", "maps", maps_path)
        self.map_name = "".join(maps_path.split(".")[:-1])
        self.cache_path = os.path.join("cache", self.map_name)
        self.map = None
        self.view = None
        self.sprites = pygame.sprite.Group()
        self.blocks = {}
        self.blockers = pygame.sprite.Group()
        self.teleports = pygame.sprite.Group()
        self.windows = pygame.sprite.Group()
        self.is_active = True
        self.spawn_point = (0, 0)
        self.width = self.data["screen"].get_width() // 25
        self.height = self.data["screen"].get_height() // 14

        if zipfile.is_zipfile(self.path):
            self.load()
        else:
            print(f"Can't load {maps_path}")

    def load_sprite(self, map_name, name, color_key=None):
        try:
            image = pygame.image.load(os.path.join("cache", map_name, "sprites", name))
            if not color_key:
                color_key = image.get_at((0, 0))
            if color_key != 'NO':
                image.set_colorkey(color_key)
            return pygame.transform.scale(image, (
                self.width,
                self.height)
            )
        except pygame.error:
            print("Can't load image cache/{}/sprites/{}".format(map_name, name))
            return pygame.image.load(os.path.join("data", "default.png")).convert()

    def load(self):
        teleport = False
        window = False
        if not os.path.exists("cache"):
            os.makedirs("cache")
        with zipfile.ZipFile(self.path, "r") as archive:
            archive.extract("map.txt", self.cache_path)
            archive.extract("view.json", self.cache_path)
            with open(os.path.join(self.cache_path, "map.txt"), "r") as m:
                self.map = list(map(lambda x: x.strip(), m.readlines()))
            with open(os.path.join(self.cache_path, "view.json"), "r") as v:
                self.view = json.loads(v.read())
                for name in self.view["sprites"].values():
                    archive.extract("sprites/" + name, self.cache_path)
                for key in self.view["sprites"]:
                    groups = [self.sprites]
                    if key in self.view["blocks_blockers"]:
                        groups.append(self.blockers)
                    if key in self.view["teleports"]:
                        teleport = True
                        groups.append(self.teleports)
                    if key in self.view["windows"]:
                        window = True
                        groups.append(self.windows)
                    self.blocks[key] = SpriteFactory(
                        groups.copy(),
                        self.load_sprite(self.map_name, self.view["sprites"][key], 255)
                    )
                    if teleport:
                        self.blocks[key].set_teleport(self.view["teleports"][key])
                        teleport = False
                    if window:
                        self.blocks[key].set_window(self.view["windows"][key])
                        window = False
                self.spawn_point = tuple(self.view["spawn"])

    def draw(self):
        if self.is_active:
            self.teleports.empty()
            self.blockers.empty()

            self.sprites.empty()
            for h, line in enumerate(self.map):
                for w, char in enumerate(line):
                    self.blocks[char].create(
                        x=w * self.width,
                        y=h * self.height
                    )
            self.sprites.draw(self.data["screen"])

    def clear(self):
        self.teleports.empty()
        self.blockers.empty()
        self.sprites.empty()
        self.is_active = False
                

