from engine.libs.Services import Service
import pygame, json, os, sys

import engine.libs.Utils as utils



class EntityService(Service):
    """
    Stores all entities to keep them loaded in RAM and update them.
    Entities that aren't currently active are sent to a different stack within the same class.
    """
    active_entities = []
    idle_entities = []

    @classmethod
    def add_entity(cls, entity):
        print("Entity Added to service ")
        cls.active_entities.append(entity)

    @classmethod
    def delete_entity(cls, entity):
        if entity in cls.active_entities:
            cls.active_entities.remove(entity)
            del entity
            return True
        elif entity in cls.idle_entities:
            cls.idle_entities.remove(entity)
            del entity
            return True
        else:
            return False

    @classmethod
    def unload_entity(cls, entity):
        if entity in cls.active_entities:
            cls.idle_entities.append(cls.active_entities.pop(cls.active_entities.index(entity)))
            return True
        else:
            return False

    @classmethod
    def load_entity(cls, entity):
        if entity in cls.idle_entities:
            cls.active_entities.append(cls.idle_entities.pop(cls.idle_entities.index(entity)))
            return True
        else:
            return False

    @classmethod
    def is_entity(cls, entity):
        return entity in cls.active_entities or entity in cls.idle_entities

    @classmethod
    def clear_active_entities(cls):
        cls.active_entities = []

    @classmethod
    def clear_idle_entities(cls):
        cls.idle_entities = []

    @classmethod
    def clear_all_entities(cls):
        cls.active_entities = []
        cls.idle_entities = []

    @classmethod
    def update(cls):
        for entity in cls.active_entities:
            entity.update()
            entity.events()
            entity.draw()


class Entity:
    def __init__(self):
        EntityService.add_entity(self)

    def update(self):
        pass

    def events(self):
        pass

    def draw(self):
        pass


        