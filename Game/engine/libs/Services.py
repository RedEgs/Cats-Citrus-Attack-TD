import logging, random, pygame, json, os, sys
#from colorama import Fore, Back, Style



class Service():
    def __init__(self, app):
        #self._service_name = name

        self._engine_logger = app.engine_logger
        self._service_registry = app.service_registry # Get the list
        self._service_registry.append(self) # Append self to it

        self._engine_logger.debug(f"Initialised Service: {self._service_registry.index(self)}")




        
