def draw():
    # Draw Code Goes Here
    print("Drawing")

draw_count = 0

def wrapped_draw():
    draw()
    draw_count += 1


