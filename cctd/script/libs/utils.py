import pytweening, pygame, sys, os

current_dir = os.path.dirname(os.path.realpath(__file__))
resources_dir = os.path.join(current_dir, '..', '..', 'resources')



#SECTION - Python Miscs

def is_in_list(item, list):
    try:
        list.index(item)
        return True
    except ValueError:
        return False
        
    
    
    


#!SECTION


#SECTION - Pygames Specifics
def rect_to_surface(rect):
    # Create a Surface with the dimensions of the Rect
    surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

    # Return the created Surface
    return surface

def load_image(image_path):
    return pygame.image.load(image_path).convert_alpha()

def callback():
    print("Callbacked")

#!SECTION


#SECTION - Maths Based
def distance_squared(point1, point2):
    return (point1[0] - point2[0])**2 + (point1[1] - point2[1])**2

def calculate_index_spacing(i, starting_pos_x, starting_pos_y, image_width, image_height, h_spacing, v_spacing, v_limit):
    if v_limit <= i:
        y = starting_pos_y + (image_height + v_spacing) * (i-v_limit + 1)
        x = starting_pos_x+(image_width+h_spacing)*(i-v_limit)
        
        spacing = (x, y)
        return spacing
    else:
        y = starting_pos_y
        x = starting_pos_x+(image_width+h_spacing)*(i)
        
        
        spacing = (x, y)
        return spacing
    
def calculate_index_spacing_out(i, starting_pos_x, starting_pos_y, image_width, image_height, h_spacing, v_spacing, v_limit):
    if v_limit <= i:
        y = starting_pos_y + (image_height + v_spacing) * (i-v_limit + 1)
        x = starting_pos_x+(image_width+h_spacing)*(i-v_limit)
        
        spacing = (x, y)
        return spacing[0], spacing[1]
    else:
        y = starting_pos_y
        x = starting_pos_x+(image_width+h_spacing)*(i)
        
        
        spacing = (x, y)
        return spacing[0], spacing[1]




#!SECTION



#SECTION - Game Specific
def check_rarity(rarity):
    if rarity == 1:
        return "uncommon"
       # img_path = os.path.join(current_dir, '..', '..', 'resources', 'lobby', 'tower_select_green.png')
    elif rarity == 2:
        return "rare"
        # img_path = os.path.join(current_dir, '..', '..', 'resources', 'lobby', 'tower_select_blue.png')
    elif rarity == 3:
        return "epic"
        #img_path = os.path.join(current_dir, '..', '..', 'resources', 'lobby', 'tower_select_purple.png')
    elif rarity == 4:
        return "hero"
        #img_path = os.path.join(current_dir, '..', '..', 'resources', 'lobby', 'tower_select_red.png')
    else:
        return False

def check_rarity_color(rarity):
    if rarity == 1:
        return "green"
       # img_path = os.path.join(current_dir, '..', '..', 'resources', 'lobby', 'tower_select_green.png')
    elif rarity == 2:
        return "blue"
        # img_path = os.path.join(current_dir, '..', '..', 'resources', 'lobby', 'tower_select_blue.png')
    elif rarity == 3:
        return "purple"
        #img_path = os.path.join(current_dir, '..', '..', 'resources', 'lobby', 'tower_select_purple.png')
    elif rarity == 4:
        return "red"
        #img_path = os.path.join(current_dir, '..', '..', 'resources', 'lobby', 'tower_select_red.png')
    else:
        return False

    
def quitGame():
        pygame.quit()
        sys.exit()
    






#!SECTION


class TweenSprite:
    def __init__(self, start_pos, end_pos, image, duration, easing_function, delay=0):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.image = image
        self.duration = duration
        self.easing_function = easing_function
        self.delay = delay
        self.start_time = None  # Initialize start_time as None

    def update(self):
        if self.start_time is None:
            self.start_time = pygame.time.get_ticks() + int(self.delay * 1000)

        current_time = pygame.time.get_ticks()
        if current_time < self.start_time:
            return  # Delaying the start of the tween

        elapsed_time = current_time - self.start_time
        progress = min(elapsed_time / (self.duration * 1000), 1.0)

        # Use the provided easing function to calculate the interpolated position
        self.current_pos = (
            self.start_pos[0] + self.easing_function(
                progress) * (self.end_pos[0] - self.start_pos[0]),
            self.start_pos[1] + self.easing_function(
                progress) * (self.end_pos[1] - self.start_pos[1]),
        )

    def draw(self, screen):
        screen.blit(self.image, self.current_pos)


class TweenOpacity:
    def __init__(self, start_alpha, end_alpha, image, duration, easing_function, delay=0):
        self.start_alpha = start_alpha
        self.end_alpha = end_alpha
        self.image = image
        self.duration = duration
        self.easing_function = easing_function
        self.delay = delay
        self.start_time = None  # Initialize start_time as None

        # Set the initial alpha value to 0
        self.current_alpha = 0
        self.image.set_alpha(self.current_alpha)

    def start(self):
        # Start the tween by setting the start_time to the current time
        self.start_time = pygame.time.get_ticks() + int(self.delay * 1000)

    def update(self):
        if self.start_time is None:
            return  # The tween has not started yet

        current_time = pygame.time.get_ticks()
        if current_time < self.start_time:
            return  # Delaying the start of the tween

        elapsed_time = current_time - self.start_time
        progress = min(elapsed_time / (self.duration * 1000), 1.0)

        # Use the provided easing function to calculate the interpolated alpha
        self.current_alpha = int(
            self.start_alpha + self.easing_function(progress) * (self.end_alpha - self.start_alpha))
        self.image.set_alpha(self.current_alpha)

    def draw(self, screen):
        screen.blit(self.image, (0, 0))

    def kill(self):
        del self



