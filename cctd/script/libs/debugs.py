import pygame
import pygame_gui as pygui
import sys


class FPSCounter:
    def __init__(self, manager, clock):
        self.visible = True

        self.clock = clock
        self.fps = None

        self.Label = pygui.elements.UILabel(
            relative_rect=pygame.Rect(0, 0, -1, 50),
            text="FPS",
            manager=manager

        )

    def update(self):
        self.fps = f"FPS: {str(int(self.clock.get_fps()))}"

        if self.visible == True:
            self.Label.set_text(self.fps)
        else:
            self.Label.set_text_alpha(0)

    def show(self):
        self.visible = True
        self.Label.set_text_alpha(255)

        # self.counter.set_active_effect(
        # pygui.TEXT_EFFECT_FADE_IN)

    def hide(self):
        self.visible = False
        self.Label.set_text_alpha(0)

        # self.counter.set_active_effect(
        # pygui.TEXT_EFFECT_FADE_OUT)


class GridResOverlay:
    def __init__(self, manager, res):
        self.visible = True

        self.res = res

        self.Label = pygui.elements.UILabel(
            relative_rect=pygame.Rect(0, 0, -1, 80),
            text="Grid Res: ",
            manager=manager

        )

    def update(self):
        self.Label.set_text(f"Grid Res: {self.res}")

    def show(self):
        self.visible = True
        self.Label.set_text_alpha(255)

        # self.counter.set_active_effect(
        # pygui.TEXT_EFFECT_FADE_IN)

    def hide(self):
        self.visible = False
        self.Label.set_text_alpha(0)


class EnemyOverlay:
    def __init__(self, manager, enemy):
        self.visible = True

        self.enemy = enemy
        self.Label = pygui.elements.UILabel(
            relative_rect=pygame.Rect(0, 0, -1, 110),
            text="Enemies Alive: ",
            manager=manager

        )

    def update(self, enemyCount):
        if self.visible == True:
            self.Label.set_text(f"Enemies Alive: {enemyCount}")
        else:
            self.Label.set_text_alpha(0)

    def show(self):
        self.visible = True
        self.Label.set_text_alpha(255)

        # self.counter.set_active_effect(
        # pygui.TEXT_EFFECT_FADE_IN)

    def hide(self):
        self.visible = False
        self.Label.set_text_alpha(0)


class EditorModeOverlay:
    def __init__(self, manager, editorMode):
        self.visible = True

        self.editorStatus = editorMode
        self.Label = pygui.elements.UILabel(
            relative_rect=pygame.Rect(0, 0, -1, 140),
            text="Editor: True",
            manager=manager
        )

    def update(self, editorMode):
        self.Label.set_text(f"Editor: {str(editorMode)}")

    def show(self):
        self.visible = True
        self.Label.set_text_alpha(255)

        # self.counter.set_active_effect(
        # pygui.TEXT_EFFECT_FADE_IN)

    def hide(self):
        self.visible = False
        self.Label.set_text_alpha(0)


class MousePreviewOverlay(pygame.sprite.Sprite):
    def __init__(self, rect_size, image_path, alpha):
        pygame.sprite.Sprite.__init__(self)

        self.width, self.height = rect_size
        self.alpha = alpha

        # Create a rect attribute
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect_x = 0
        self.rect_y = 0

        # Load the image
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))

        # Set the rect position based on the initial values
        self.rect.topleft = (self.rect_x, self.rect_y)

    def update_position(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.rect_x, self.rect_y = mouse_x - self.width / 2, mouse_y - self.height / 2

        # Update the rect's position
        self.rect.topleft = (self.rect_x, self.rect_y)

    def check_bounds(self):
        if pygame.mouse.get_pos()[0] <= 600 and pygame.mouse.get_pos()[1] <= 600:
            return True

        return False

    def check_conditions(self, tower_group, mask):
        default_color = (255, 0, 0)

        # Create a copy of the image to avoid modifying the original
        tinted_image = self.image.copy()

        # Check collision with other towers
        if not pygame.sprite.spritecollideany(self, tower_group):

            # Get the rect of the preview tower
            preview_rect = self.get_rect()

            # Create a mask for the preview tower
            preview_mask = pygame.mask.from_surface(self.image)

            # Check collision with the mask
            if mask.overlap(preview_mask, (int(preview_rect.x), int(preview_rect.y))) is None:
                # Check if the tower position exceeds the specified limits
                if pygame.mouse.get_pos()[0] <= 600 and pygame.mouse.get_pos()[1] <= 600:
                    default_color = (0, 255, 0)

                    tinted_image.fill((*default_color, self.alpha),
                                      special_flags=pygame.BLEND_RGBA_MULT)

        tinted_image.fill((*default_color, self.alpha),
                          special_flags=pygame.BLEND_RGBA_MULT)

        return tinted_image

    def draw(self, screen, tower_group, mask):
        if self.check_bounds():
            tinted_image = self.check_conditions(tower_group, mask)
            screen.blit(tinted_image, self.rect.topleft)

    def get_rect(self):
        return self.rect


class GridOverlay:
    def __init__(self, grid):
        self.grid = grid
        self.overlay_surface = pygame.Surface(
            (self.grid.render_width * self.grid.cell_size, self.grid.render_height * self.grid.cell_size), pygame.SRCALPHA)
        self.overlay_alpha = 100  # Adjust the alpha value as needed

    def draw(self, screen):
        GridColor = (255, 255, 255, self.overlay_alpha)

        for x in range(0, self.grid.render_width * self.grid.cell_size, self.grid.cell_size):
            pygame.draw.line(self.overlay_surface, GridColor, (x, 0),
                             (x, self.grid.render_height * self.grid.cell_size), 1)
        for y in range(0, self.grid.render_height * self.grid.cell_size, self.grid.cell_size):
            pygame.draw.line(self.overlay_surface, GridColor, (0, y),
                             (self.grid.render_width * self.grid.cell_size, y), 1)

        screen.blit(self.overlay_surface, (0, 0))


class PathOverlay:
    def __init__(self, waypoints):
        self.waypoints = waypoints
        print(waypoints)

    def draw(self, screen):
        # Check if there are at least two points
        if len(self.waypoints) >= 2:
            # Draw the line connecting waypoints
            pygame.draw.lines(screen, "red", False, self.waypoints)

            # Highlight the first waypoint in green
            pygame.draw.circle(screen, "green", self.waypoints[0], 10)

            # Highlight the last waypoint in blue
            pygame.draw.circle(screen, "blue", self.waypoints[-1], 10)

            # Draw red circles for points in between
            for point in self.waypoints[1:-1]:
                pygame.draw.circle(screen, "red", point, 5)

        pygame.draw.lines(screen, "red", False, self.waypoints)
