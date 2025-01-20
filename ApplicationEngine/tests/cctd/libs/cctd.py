import pygame, math, os, sys, ast, time

class Scene():
    def __init__(self, display: pygame.Surface):
        pass

    def on_enter(self):
        pass

    def handle_events(self, event: pygame.event.Event, mouse_pos: list | tuple):
        pass

    def update(self):
        pass

    def draw(self):
        pass


class GameMap:
    def __init__(self, folder_path):
        self.folder_path = folder_path

        self._texture_path = os.path.join(self.folder_path, "map.png")
        self._mask_path = os.path.join(self.folder_path, "mask.png")

        self.map_texture = pygame.image.load(self._texture_path).convert_alpha()
        self.mask_texture = pygame.image.load(self._mask_path).convert_alpha()
        self.path_mask = pygame.mask.from_surface(self.mask_texture)

        with open(os.path.join(self.folder_path, "waypoints.txt"), "r") as f:
            self.waypoints = f.read()
            self.waypoints = ast.literal_eval(self.waypoints)


    def draw_points(self, screen):
        pygame.draw.lines(screen, (255, 255, 0), False, self.waypoints)

    def get_points(self):
        return self.waypoints

    def get_mask(self):
        return self.path_mask

    def get_surface(self):
        return self.map_texture

class Enemy():
    def __init__(self, waypoints, parent, speed = 1, health = 20):
        self.waypoints = waypoints
        self.speed = speed
        self.pos =self.waypoints[0]
        self.parent = parent

        self.targetPoint = 1

        self.originalImage = pygame.image.load(
            "enemy.png").convert_alpha()
        self.image = pygame.image.load(
            "enemy.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.health = health
        self.max_health = self.health

        self.strength = (speed * health) / 10


    def move(self):
        if self.targetPoint < len(self.waypoints):
            self.target = self.waypoints[self.targetPoint]
            self.path = pygame.Vector2(self.target) - pygame.Vector2(self.pos)
        else:
            self.parent.remove(self)
            return True

        distance = self.path.length()
        if distance >= self.speed:
            self.pos += self.path.normalize() * self.speed
        else:
            if distance != 0:
                self.pos += self.path.normalize() * distance
            self.targetPoint += 1

    def rotate(self):
        distance = self.target - self.pos

        self.angle = math.degrees(math.atan2(-distance[1], distance[0]))
        self.image = pygame.transform.rotate(self.originalImage, self.angle)
        self.rect.center = self.pos

    def update(self):
        if self.move() == True: return True
        self.rotate()

        if self.health <= 0:
            self.parent.remove(self)

    def draw(self, surf: pygame.Surface):
        surf.blit(self.image, self.pos)

class Tower():
    def __init__(self, position, parent) -> None:
        self.pos = position
        self.parent = parent
        self.tower_name = "Citrus Cat"

        self.image = pygame.image.load("towers/sprite.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.panel = None

        self.rect.center = self.pos

        self.range = 150
        self.last_shot_time = 0
        self.fire_rate = 0.001
        self.target = None
        self.damage = 10

    def check_overlap(self, mask, mask_pos):

        # Create masks from surfaces
        image_mask = pygame.mask.from_surface(self.image)
        mask_mask = mask

        # Calculate the offset between the image and mask
        offset_x = mask_pos[0] - self.pos[0]
        offset_y = mask_pos[1] - self.pos[1]
        offset = (offset_x, offset_y)

        # Check for overlap
        overlap = image_mask.overlap(mask_mask, offset)

        return overlap is not None

    def distance_to(self, enemy_rect):
        # Calculate the distance between the centers of two pygame.Rects
        tower_center = self.rect.center
        enemy_center = enemy_rect.center
        return math.sqrt((enemy_center[0] - tower_center[0])**2 + (enemy_center[1] - tower_center[1])**2)

    def find_target(self, enemies):
        target = None
        min_distance = float('inf')
        for enemy in enemies:
            dist = self.distance_to(enemy.rect)
            if dist <= self.range and dist < min_distance:
                target = enemy
                min_distance = dist
        return target

    def shoot(self, enemy, game):
        self.target = enemy

        if game.current_time - self.last_shot_time >= 1 / self.fire_rate:
            self.target.health -= self.damage
            game.on_tower_damage(self.target, self.damage)
            self.last_shot_time = game.current_time


    def update(self, enemies, game):
        target = self.find_target(enemies)
        if target:
            self.shoot(target, game)
        else: self.target = None

    def draw(self, surf: pygame.Surface):
        surf.blit(self.image, self.rect)

        if self.target != None:
            pygame.draw.line(surf, (255, 0, 255), self.pos, self.target.pos)

class RoundManager():
    def __init__(self, RoundCount, MoneyCount, GameMap, EnemyList: list) -> None:
        self.GameMap = GameMap

        self.RoundCount = RoundCount
        self.MoneyCount = MoneyCount
        self.MidRound = False
        self.current_time = 0
        self.spawn_amount = 3

        self.spawn_times = []
        self.enemy_list = EnemyList

    def spawn_enemies(self):
        base_time = pygame.time.get_ticks()
        for i in range(self.spawn_amount * self.RoundCount):
            self.spawn_times.append(base_time + i * 500)

    def update(self, current_time, roundtext, cashtext):
        self.current_time = current_time
        for spawn_time in self.spawn_times[:]:
            if self.current_time >= spawn_time:
                # Spawn an enemy at a random position
                enemy = Enemy(self.GameMap.waypoints, self.enemy_list, 1+(self.RoundCount * 0.8), 20)
                self.enemy_list.append(enemy)
                self.spawn_times.remove(spawn_time)

        if len(self.enemy_list) == 0 and self.MidRound:
            self.end_round(roundtext, cashtext)


    def spend_money(self, amount, cashtext):
        self.MoneyCount -= amount
        cashtext.update_text(f"Cash: ${self.MoneyCount}")

    def give_money(self, amount, cashtext):
        self.MoneyCount += amount
        cashtext.update_text(f"Cash: ${self.MoneyCount}")


    def start_round(self):
        if self.MidRound: return

        self.spawn_enemies()
        self.MidRound = True


    def end_round(self, roundtext, cashtext):
        if not self.MidRound: return
        self.RoundCount += 1
        self.MidRound = False

        self.give_money(15*(self.RoundCount*0.8), cashtext)
        roundtext.update_text(f"Round: {self.RoundCount}/100")
