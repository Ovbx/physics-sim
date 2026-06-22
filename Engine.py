import pygame

pygame.init()

Width = 1000
Height = 800
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Pygame Window")

fps = 60
timer = pygame.time.Clock()

#game variables
wall_thickness = 10
gravity = 0.5
bounce_stop = 0.3


#track pos
mouse_trajectory = []


#without charge
class QuadTree:
    def __init__(self, boundary, capacity = 4):
        self.boundary = boundary
        self.capacity = capacity
        self.balls = []
        self.divided = False
        self.nw = self.ne = self.sw = self. se = None
    


class Ball:
    def __init__(self, x_pos, y_pos, radius, color, mass, retention, y_speed, x_speed, id, friction):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius
        self.color = color
        self.mass = mass
        self.retention = retention
        self.y_speed = y_speed
        self.x_speed = x_speed
        self.id = id
        self.circle = ''
        self.selected = False
        self.friction = friction

    def draw(self):
        self.circle = pygame.draw.circle(screen, self.color, (self.x_pos, self.y_pos), self.radius)

    def checkGravity(self):
        if not self.selected:
            if self.y_pos < Height - self.radius - (wall_thickness / 2):
                self.y_speed += gravity
            else:
                if self.y_speed > bounce_stop:
                    self.y_speed = self.y_speed * -1 * self.retention
                else:
                    if abs(self.y_speed) <= bounce_stop:
                        self.y_speed = 0
            if (self.x_pos < self.radius + (wall_thickness/2) and self.x_speed < 0) or \
                    (self.x_pos > Width - self.radius - (wall_thickness /2 ) and self.x_speed > 0):
                self.x_speed *= -1 * self.retention
                if abs(self.x_speed) < bounce_stop:
                    self.x_speed = 0
            if self.y_speed == 0 and self.x_speed != 0:
                if self.x_speed > 0:
                    self.x_speed -= self.friction
                elif self.x_speed < 0:
                    self.x_speed += self.friction


        else:
            self.x_speed = x_push
            self.y_speed = y_push
        return self.y_speed
    
    def updatePos(self, mouse):
        if not self.selected:
            self.y_pos += self.y_speed
            self.x_pos += self.x_speed
        else:
            self.x_pos = mouse[0]
            self.y_pos = mouse[1]
    

    def check_select(self, pos):
    
        self.selected = False
        if self.circle.collidepoint(pos):
            self.selected = True
        return self.selected

    


def drawWalls():
    left = pygame.draw.line(screen, 'white', (0,0), (0, Height), wall_thickness)
    right = pygame.draw.line(screen, 'white', (Width,0), (Width, Height), wall_thickness)
    top = pygame.draw.line(screen, 'white', (0,0), (Width, 0), wall_thickness)
    bottom = pygame.draw.line(screen, 'white', (0,Height), (Width, Height), wall_thickness)

def calc_motion_vector():
    x_speed = 0
    y_speed = 0
    if len(mouse_trajectory) > 10:
        x_speed = (mouse_trajectory[-1][0] - mouse_trajectory[0][0]) / len(mouse_trajectory)
        y_speed = (mouse_trajectory[-1][1] - mouse_trajectory[0][1]) / len(mouse_trajectory)
    return x_speed, y_speed


ball1 = Ball(50, 50, 30, 'blue', 100, .9, 0,0, 1, 0.02)
ball2 = Ball(500, 500, 50, 'red', 300, .9, 0,0,2, 0.03)
ball3 = Ball(200,200,40,'purple', 200, .9, 0,0,3, 0.04)
ball4 = Ball(300,200,30, 'green', 200, .9, 0,0,4, 0.02)

balls = [ball1, ball2, ball3, ball4]

#main loop
run = True
while run:
    timer.tick(fps)
    screen.fill('black')
    mouse_coords = pygame.mouse.get_pos()
    mouse_trajectory.append(mouse_coords)
    if len(mouse_trajectory) > 20:
        mouse_trajectory.pop(0)
    x_push, y_push = calc_motion_vector()


    walls = drawWalls()
    ball1.draw()
    ball2.draw()
    ball3.draw()
    ball4.draw()
    ball1.updatePos(mouse_coords)
    ball2.updatePos(mouse_coords)
    ball3.updatePos(mouse_coords)
    ball4.updatePos(mouse_coords)

    ball1.y_speed = ball1.checkGravity()
    ball2.y_speed = ball2.checkGravity()
    ball3.y_speed = ball3.checkGravity()
    ball4.y_speed = ball4.checkGravity()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if ball1.check_select(event.pos) or ball2.check_select(event.pos) or ball3.check_select(event.pos) or ball4.check_select(event.pos):
                active_select = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                active_select = False
                for i in range(len(balls)):
                    balls[i].check_select((-1000,-1000))



    pygame.display.flip()

pygame.quit()

