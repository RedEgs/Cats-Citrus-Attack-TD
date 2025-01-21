import pygame, pytweening

class TweenManager():
    tweens = []
    active_tweens = []

    @classmethod
    def add_tween(cls, tween):
        if not tween in cls.tweens:
            cls.tweens.append(tween)

    @classmethod
    def start_tween(cls, tween):
        if not tween in cls.active_tweens:
            cls.active_tweens.append(tween)

    @classmethod
    def stop_tween(cls, tween):
        cls.active_tweens.remove(tween)

    @classmethod
    def kill_tween(cls, tween):
        try:
            cls.active_tweens.remove(tween)
        except: pass
        try:
            cls.tweens.remove(tween)
        except: pass
        del tween

    @classmethod
    def update(cls, delta_time):
        active_tween = [tween.update(delta_time) for tween in cls.active_tweens]

class Tween():
    from typing import Callable, Union

    def __init__(self, pos_1: Union[int, pygame.Vector2],
                 pos_2: Union[int, pygame.Vector2],
                 time: float = 1,
                 easing_type: Callable[[float], float] = pytweening.linear,
                 **settings):

        self.pos_1 = pos_1
        self.pos_2 = pos_2

        self.time = time
        self.easing_type = easing_type

        self.t_settings = settings

        self.progress = 0.0
        self._finished = False
        self._started = False
        self._tween_factor = 0

        self.load_settings()

        if type(self.pos_1) is pygame.Vector2 and type(self.pos_2) is pygame.Vector2:
            self.output_pos = pytweening.getPointOnLine(self.pos_1[0], self.pos_1[1],
                                                        self.pos_2[0], self.pos_2[1],
                                                        self._tween_factor)
        if type(self.pos_1) is int and type(self.pos_2) is int:
            self.output_pos = pytweening.getPointOnLine(self.pos_1, self.pos_1,
                                                        self.pos_2, self.pos_2,
                                                        self._tween_factor)

        TweenManager.add_tween(self)

    def load_settings(self):
        """
        1 - On start callback
        2 - On stop callback
        3 - Start delay
        4 - Reverse on finish
        """
        self.callback_1 = None
        self.callback_2 = None
        self.delay = 0
        self.reverse_on_finish = False

        self.reverse_once = False
        self._finished_reverse = False

        print(self.t_settings)
        for setting, value in self.t_settings.items():
            if setting == "on_start":
                self.callback_1 = value
            elif setting == "on_stop":
                self.callback_2 = value
            elif setting == "delay":
                self.delay = value
            elif setting == "reverse":
                self.reverse_on_finish = True
            elif setting == "reverse_once":
                self.reverse_once = True

    def start(self):
        self.on_start()

        self._start_time = pygame.time.get_ticks()
        self._started = True

        if type(self.pos_1) is pygame.Vector2 and type(self.pos_2) is pygame.Vector2:
            self.output_pos = pytweening.getPointOnLine(self.pos_1[0], self.pos_1[1],
                                                        self.pos_2[0], self.pos_2[1],
                                                        self._tween_factor)
        if type(self.pos_1) is int and type(self.pos_2) is int:
            self.output_pos = pytweening.getPointOnLine(self.pos_1, self.pos_1,
                                                        self.pos_2, self.pos_2,
                                                        self._tween_factor)

        TweenManager.start_tween(self)

    def stop(self):
        self._started = False
        self._finished = True


        if self.reverse_on_finish:
            if self.reverse_once and not self._finished_reverse:
                self.reverse()
                self._finished_reverse = True

            self.reverse()



        TweenManager.stop_tween(self)
        self.on_stop()



    def reverse(self):
        self.progress = 0
        self._finished = False
        self._started = False
        self._tween_factor = 0

        temp_pos = self.pos_1
        self.pos_1 = self.pos_2
        self.pos_2 = temp_pos

        self.start()


    def kill(self):
        TweenManager.kill_tween(self)

    def update(self, delta_time):
        if self._start_time + (self.delay * 1000) <= pygame.time.get_ticks():
            if self._started and self.progress <= 1.0:
                self.progress += delta_time / self.time
                self._tween_factor = self.easing_type(self.progress)

                if type(self.pos_1) is pygame.Vector2 and type(self.pos_2) is pygame.Vector2:
                    self.output_pos = pytweening.getPointOnLine(self.pos_1[0], self.pos_1[1],
                                                                self.pos_2[0], self.pos_2[1],
                                                                self._tween_factor)
                if type(self.pos_1) is int and type(self.pos_2) is int:
                    self.output_pos = pytweening.getPointOnLine(self.pos_1, self.pos_1,
                                                                self.pos_2, self.pos_2,
                                                                self._tween_factor)

            if self.progress >= 1.0 and not self._finished:
                self.stop()


    def on_start(self):
        if self.callback_1 is not None and not self._started:
            self.callback_1()

    def on_stop(self):
        if self.callback_2 is not None:

            self.callback_2()

    def check_finished(self):
        return self._finished

    def check_started(self):
        return self._started

    def get_start_time(self):
        return self._start_time

    def get_progress(self):
        return self.progress

    def get_output(self):
        if  type(self.pos_1) is pygame.Vector2 and type(self.pos_2) is pygame.Vector2:
            return pygame.Vector2(self.output_pos)
        if type(self.pos_1) is int and type(self.pos_2) is int:
            return self.output_pos[0]


class Text():
    def __init__(self, text, size, position):
        self.text = text
        self.size = size
        self.pos = position
        self.content = self.text
        self.color = (255, 255, 255)
        self.created_time = pygame.time.get_ticks()

        self.default_font = pygame.font.Font("font.ttf", self.size)
        self.image = self.default_font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(topleft=self.pos)

    def handle_events(self, event, mouse_pos):
        pass

    def update_text(self, text=None):
        self.text = text
        self.image = self.default_font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(topleft=self.pos)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

class Button:
    def __init__(self, pos, size, image = None, color = (0,0,0), text = None):
        self.pos = pos
        self.text = text

        if image == None:
            self.image = pygame.Surface(size)
            if color != None:
                self.image.fill(color)
        else:
            self.image = image

        if text != None:
            self.text.rect.center = pos
            self.text.pos = self.text.rect.center

        self.rect = self.image.get_rect(center=pos)

    def handle_events(self, event, mouse_pos):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.text != None: self.text.draw(screen)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def get_image(self) -> pygame.Surface:
        return self.image

    def get_drawable(self):
        return self.image, self.rect


class DraggablePanel:
    def __init__(self, pos, size, color = (0, 0, 0)):
        self.pos = pos
        self.color = color
        self.size = size
        self.resizable = False

        self.resizing_rect = False
        self.dragging_rect = False

        self.can_change_mouse = True

        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.color)
        self.surface.set_alpha(200)

        self.rect = self.surface.get_rect(center=self.pos)


    def update_position(self):
        self.pos = self.rect.center

    def handle_events(self, event, mouse_pos):

        if event.type == pygame.MOUSEBUTTONUP:
            print("stop draggin")
            self.dragging_rect = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(mouse_pos):  # Dragging Header
                self.dragging_rect = True
                print("start dragging")


        if self.dragging_rect:
            if event.type == pygame.MOUSEMOTION:
                self.rect.move_ip(event.rel[0], event.rel[1])
                self.update_position()
                print(self.pos)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.surface, self.rect)



class Panel:
    def __init__(self, pos, size, color = (0, 0, 0)):
        self.pos = pos
        self.color = color
        self.size = size

        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.color)
        self.surface.set_alpha(200)

        self.rect = self.surface.get_rect(center=self.pos)


    def update_position(self):
        self.pos = self.rect.center

    def handle_events(self, event, mouse_pos):
        pass

    def draw(self, screen: pygame.Surface):
        screen.blit(self.surface, self.rect)
