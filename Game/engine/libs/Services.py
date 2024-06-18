import logging, random, pygame, json, os, sys
#from colorama import Fore, Back, Style



class Service():
    def __init__(self, app):
        #self._service_name = name
        self.name = self.__class__.__name__
        self._service_registry = app.service_registry # Get the list
        self._service_registry.append(self) # Append self to it
