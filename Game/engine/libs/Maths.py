
def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    
    z1 = x2 - x1
    z2 = y2 - y1
    
    return (z1, z2)

def midpoint(point1, point2):
    """Calculate the midpoint of a segment defined by two points."""
    x1, y1 = point1
    x2, y2 = point2
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    return (mid_x, mid_y)

def get_center(x, y):
    return x // 2, y //2   