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
substeps = 4


#track pos
mouse_trajectory = []



class QuadTree:
    def __init__(self, boundary, capacity = 4):
        self.boundary = boundary
        self.capacity = capacity
        self.balls = []
        self.divided = False
        self.nw = self.ne = self.sw = self. se = None
    
    def contains(self, ball):
        x, y, w, h = self.boundary
        return (ball.x_pos >= x and ball.x_pos < x + w and ball.y_pos >= y and ball.y_pos < y + h)

    
    def subdivide(self):
        x, y, w, h = self.boundary
        hw = w/2 
        hh = h/2
        self.nw = QuadTree((x, y, hw, hh), self.capacity)
        self.ne = QuadTree((x + hw, y, hw, hh), self.capacity)
        self.sw = QuadTree((x, y + hh, hw, hh), self.capacity)
        self.se = QuadTree((x + hw, y + hh, hw, hh), self.capacity)
        self.divided = True
    
    def intersects(self, area):
        x, y, w, h = self.boundary
        rx, ry, rw, rh = area
        return not (
            rx > x + w or 
            rx + rw < x or
            ry > y + h or
            ry + rh < y
        )
    def query(self, area, found=None):
        if found is None:
            found = []
        if not self.intersects(area):
            return found
        
        rx, ry, rw, rh = area
        for ball in self.balls:
            if rx <= ball.x_pos <= rx + rw and ry <= ball.y_pos <= ry + rh:
                found.append(ball)
        if self.divided:
            self.nw.query(area, found)
            self.ne.query(area, found)
            self.sw.query(area,found)
            self.se.query(area,found)
        return found

    def insert(self, ball):
        #not within region
        if not self.contains(ball):
            return False
        
        #base
        if len(self.balls) < self.capacity:
            self.balls.append(ball)
            return True
        
        #full
        if not self.divided:
            self.subdivide()

        return (self.nw.insert(ball) or self.ne.insert(ball) or self.se.insert(ball) or self.sw.insert(ball))
        
    


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
    
    def updatePos(self, mouse, substeps=1):
        if not self.selected:
            self.y_pos += self.y_speed / substeps
            self.x_pos += self.x_speed / substeps
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
def resolve_collision(a,b):
    # collision normal
    dx = b.x_pos - a.x_pos
    dy = b.y_pos - a.y_pos
    dist = (dx**2 + dy**2) ** 0.5
    if dist == 0:
        return
    #normalize
    nx, ny = dx / dist, dy/dist
    #dot product
    aNormal = a.x_speed * nx + a.y_speed * ny
    bNormal = b.x_speed * nx + b.y_speed * ny

    
    da = bNormal - aNormal
    if da > 0:
        return
    m1, m2 = a.mass, b.mass
    impulse = (2 * da) / (m1+m2)
    a.x_speed += impulse * m2 * nx
    a.y_speed += impulse * m2 * ny
    b.x_speed -= impulse * m1 * nx
    b.y_speed -= impulse * m1 * ny

    #pushing balls apart so no overlap occurs
    overlap = (a.radius + b.radius) - dist
    if overlap > 0:
        m1, m2 = a.mass, b.mass
        total = m1 + m2
        a.x_pos -= overlap * (m2 / total) * nx
        a.y_pos -= overlap * (m2 / total) * ny
        b.x_pos += overlap * (m1/total) * nx
        b.y_pos += overlap * (m1 / total) * ny

    for obj in (a, b):
        obj.x_pos = max(obj.radius + wall_thickness/2, min(Width - obj.radius - wall_thickness/2, obj.x_pos))
        obj.y_pos = max(obj.radius + wall_thickness/2, min(Height - obj.radius - wall_thickness/2, obj.y_pos))

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
    drawWalls()
    for ball in balls:
        ball.draw()
    for ball in balls:
        ball.y_speed = ball.checkGravity()
    for _ in range(substeps):
        for ball in balls:
            ball.updatePos(mouse_coords, substeps)
        qt = QuadTree((0,0,Width, Height))
        for ball in balls:
            qt.insert(ball)
        checked = set()
        for ball in balls:
            r = ball.radius
            area = (ball.x_pos - 2*r, ball.y_pos - 2*r, 4*r, 4*r)
            near = qt.query(area)
            for other in near:
                if other is ball:
                    continue
                pair = (min(ball.id, other.id), max(ball.id, other.id))
                if pair in checked:
                    continue
                checked.add(pair)
                dx = other.x_pos - ball.x_pos
                dy = other.y_pos - ball.y_pos
                dist = (dx**2 + dy**2) ** 0.5

                if dist < ball.radius + other.radius:
                    resolve_collision(ball, other)







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

