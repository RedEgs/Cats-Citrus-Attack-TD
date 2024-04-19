import pygame, json, os, sys

from engine.app import *
from engine.libs import SceneService as SceneService
import cProfile, asyncio

"""import scenes.main_menu as main_menu
import scenes.difficulty_select as d_select
import scenes.map_select as m_select
import scenes.tower_select as t_select
import scenes.main_game as main_game
import scenes.map_editor as map_editor
import scenes.user_login as user_login
import scenes.network_test as network_test"""
import scenes.example_scene as example_scene
import scenes.example_scene_2 as example_scene_2


class Main(App):
    def __init__(self):
        super().__init__()

    def set_user(self, user):
        self.user = user

    def load_scenes(self):
        self.scene_service.load_scenes([example_scene_2.Example_Scene("example_scene_2", self)])
        self.scene_service.load_scenes([example_scene.Example_Scene("example_scene", self)])
       
        self.scene_service.set_scene("example_scene")


"""network_test.Network_Test("network_test", self),
                                 map_editor.Map_Editor("map_editor", self),
                                 main_game.Main_Game("main_game", self),
                                 t_select.Tower_Select("tower_select", self),
                                 m_select.Map_Select("map_select", self),
                                 d_select.Difficulty_Select("difficulty_select", self),
                                 main_menu.Menu("main_menu", self),
                                 user_login.User_Login("user_login", self),"""


if __name__ == "__main__":

    
    main = Main()
    #cProfile.run("main.run()", sort="ncalls")
    #asyncio.run(main.run())
    main.run()
