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
    
def get_item_list(item, list):
    try:
        return list.index(item)
    except ValueError:
        return False

def get_last_index(list):
    try:
        return len(list)-1
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

def get_center_pos(surface):
    return (surface.width //2, surface.height // 2)

def callback():
    print("Callbacked")

def script_wait(seconds):
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    seconds = seconds * 1000

    while pygame.time.get_ticks() - start_time < seconds:
        clock.tick(120)  # Adjust the frame rate as needed (e.g., 60 frames per second)
        
    return True
    




#!SECTION


#SECTION - Maths Based
def distance_squared(point1, point2):
    return (point1[0] - point2[0])**2 + (point1[1] - point2[1])**2

def calculate_index_spacing(i, starting_pos_x, starting_pos_y, image_width, image_height, h_spacing, v_spacing, v_limit):
    if v_limit <= i:
        if i-v_limit == 0:
            y = starting_pos_y + (image_height + v_spacing) * (i-v_limit+1)
        else:
            y = starting_pos_y + (image_height + v_spacing) * (i-v_limit)

        x = starting_pos_x+(image_width+h_spacing)*(i-v_limit)
        
        spacing = (x, y)
        return spacing
    else:
        y = starting_pos_y
        x = starting_pos_x+(image_width+h_spacing)*(i)
        
        
        spacing = (x, y)
        return spacing



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


