"""Recreation of the Pong arcade game by David Adams"""
from random import randint

# Dimensions of canvas
w = 720
h = 480

# Each block component of paddles and balls is 15x15
block_size = 15

class Paddle():
    """Represents a paddle that can move and hit the ball"""
    def __init__(self, side):
        global w, h
        self.side = side
        self.direction = 'none'
        
        # Based on the side it is on, it gets a different x-value
        if side == 'left':
            self.x = block_size
        elif side == 'right':
            self.x = w - 2 * block_size
                    
        # y is initiated at midpoint of y-axis   
        self.leng = 5
        
        # y-value is based on the middle of the paddle
        self.y = h / 2
        self.frames_since_change = 0
    
    def show(self):
        """Draws the paddle onto the screen"""
        rect(self.x, self.y - (self.leng * block_size) / 2, block_size, self.leng * block_size)
    
    def move(self):
        """Moves the paddle based on user-entered direction"""
        if self.direction == 'up' and self.y - (self.leng * block_size / 2) > 0:
            self.y -= 9
        elif self.direction == 'down' and self.y + (self.leng * block_size / 2) < h:
            self.y += 9


class Ball():
    """Represents the ball being hit"""
    def __init__(self, x_speed, y_speed):
        global w, h, block_size
        self.x = w / 2
        self.y = h / 2
        self.x_speed = x_speed
        self.y_speed = y_speed
    
    def show(self):
        """Draws the ball onto the screen"""
        rect(self.x, self.y, block_size, block_size)
    
    def move(self, paddles):
        """Moves the ball and bounces it if it hits an object"""
        # Collision detection with walls
        if self.y <= 0 or self.y >= h - block_size:
            self.y_speed = -self.y_speed
        
        def intersect_x_axis(paddle):
            if paddle.side == 'left':
                if self.x <= paddle.x + block_size and self.x >= paddle.x:
                    return True
            elif paddle.side == 'right':
                if self.x + block_size >= paddle.x and self.x + block_size <= paddle.x + block_size:
                    return True
            else:
                return False
        
        def intersect_y_axis(paddle):
            d_from_center = (paddle.leng * block_size) / 2
            if self.y <= paddle.y + d_from_center and self.y + block_size >= paddle.y - d_from_center:
                return True
            else:
                return False
        
        # Collision detection with paddles
        for paddle in paddles:
             if intersect_x_axis(paddle) and intersect_y_axis(paddle):
                 self.x_speed = -self.x_speed
                 mid_ball = self.y + (block_size / 2)
                 self.y_speed = (mid_ball - paddle.y) * .35
        
        self.x += self.x_speed
        if self.y <= 0 or self.y >= h:
            self.y += 2 * self.y_speed
        else:
            self.y += self.y_speed



def move_cpu_paddle(paddle, ball):
    """Moves cpu paddle based on position of the ball.
    Challenging but not too difficult for user to beat."""
    if paddle.frames_since_change >= 4:
        mid_ball = ball.y + (block_size / 2)
        if mid_ball - paddle.y > 15:
            paddle.direction = 'down'
        elif mid_ball - paddle.y < 15:
            paddle.direction = 'up'
        else:
            paddle.direction = 'none'
        paddle.frames_since_change = 0
    else:
        paddle.frames_since_change += 1

# Beginning of main
def setup():
    global w, h, grid_size
    frameRate(30)
    size(w, h)
    background(0)
    stroke(255)
    fill(255)
    textSize(25)
    textAlign(CENTER, LEFT)
    
ball = Ball(12, 0)
paddles = [Paddle('left'), Paddle('right')]
scores = [0, 0]

def keyPressed():
    """Moves the user's paddle up and down 
    when the arrow keys are pressed"""
    # Up Arrow
    if keyCode == 38:
        paddles[0].direction = 'up'
    # Down Arrow
    elif keyCode == 40:
        paddles[0].direction = 'down'

def keyReleased():
    """Resets direction of paddle to 'none' when key is released"""
    paddles[0].direction = 'none'

def draw():
    global ball
    background(0)
    line(w / 2, 0, w / 2, h)
    move_cpu_paddle(paddles[1], ball)
    for paddle in paddles:
        paddle.move()
        paddle.show()
    ball.move(paddles)
    ball.show()
    
    # Generates a new ball and increments score when the ball goes out
    if ball.x < 0:
        ball = Ball(12, randint(0, 4))
        scores[1] += 1
    if ball.x > w :
        ball = Ball(-12, randint(0, 4))
        scores[0] += 1
    
    text(scores[0], (w / 2) - 50, 50)
    text(scores[1], (w / 2) + 50, 50)
    