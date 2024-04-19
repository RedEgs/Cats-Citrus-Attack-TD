import pygame
import moderngl
from array import array
import os

path = os.getcwd()

run = True
#pygame related stuff
resolution = (1000, 1000)

window = pygame.display.set_mode(resolution, pygame.OPENGL | pygame.DOUBLEBUF)

#GL related stuff
ctx = moderngl.create_context()

program = ctx.program(vertex_shader='''
#version 330 core

in vec2 vert;
in vec2 texcoord;
out vec2 uvs;

uniform float time = 0;

void main() {
    uvs = texcoord;
    gl_Position = vec4(vert, 0.0, 1.0);

}
''', fragment_shader='''
#version 330 core
uniform sampler2D tex;

in vec2 uvs;
out vec4 f_color;

void main()
{
    f_color = texture(tex, uvs);
}
''')

clock = pygame.time.Clock()

def relative_pos(rect, ctx, top_offset = 0, bottom_offset = 0, return_rect = None, return_list = None, rotate = 0, x_mul = 1):
    win_w, win_h = resolution
    l, t, r, b = rect
    r_w_w = 1 / win_w
    r_w_h = 1 / win_h
    no_t = (t * r_w_h) * -2 + 1
    no_b = ((t + b) * r_w_h) * -2 + 1
    no_l = (l * r_w_w) * 2 - 1
    no_r = ((r + l) * r_w_w) * 2 - 1 

    buffer = [
            # position (x, y), uv coords (x, y)
            no_l + top_offset, no_t, 0, 0,  # topleft
            no_r + top_offset, no_t, 1, 0,  # topright
            no_l + bottom_offset, no_b, 0, 1,  # bottomleft
            no_r + bottom_offset, no_b, 1, 1,  # bottomright
        ]

    if not return_rect:
        quad_buffer = ctx.buffer(data=array('f', buffer))

    return (quad_buffer if not return_list else buffer) if not return_rect else (no_l, no_t, no_r, no_b)

rect1 = pygame.Rect(100, 100, 100, 100)

img = pygame.image.load("player.png")

tex = ctx.texture(img.get_size(), 4, pygame.image.tobytes(img, 'RGBA'))

tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
tex.repeat_x, tex.repeat_y = False, False

ctx.enable(moderngl.BLEND)

ctx.screen.use()

while run:
    dt = clock.tick(100000) * 0.001

    for event in pygame.event.get():
        print(clock.get_fps())
        if event.type == pygame.QUIT:
           
            run = False

    tex.use()
    
    buffer = relative_pos(rect1, ctx)
    vao = ctx.vertex_array(program, [(buffer, '2f 2f', 'vert', 'texcoord')])

    vao.render(mode=moderngl.TRIANGLE_STRIP)

    pygame.display.flip()

    buffer.release()
    vao.release()

#pygame.quit()
