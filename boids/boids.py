import pygame
import math 
import random
from reward import Reward
from slider import Slider
import csv

# Constants
WIDTH, HEIGHT = 1000, 900
NUM_BOIDS = 15
MAX_VELOCITY = 2
BOID_RADIUS = 4
NEIGHBOR_RADIUS = 50
AVOID_RADIUS = 15
ATTRACT_RADIUS = 150
PADDING = 40
SEPARATION_COEFF = 0.01

# Colors
WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

# Pygame Init
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Boids Simulation')

clock = pygame.time.Clock()

# anyone can access this
def distance( b1, b2):
    return math.sqrt((b1.x - b2.x) ** 2 + (b1.y - b2.y) ** 2)

class Boid:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.velocity_x = random.uniform(-1,1) * MAX_VELOCITY
        self.velocity_y = random.uniform(-1,1) * MAX_VELOCITY

    def move(self):
        # Boundary conditions
        if self.x >= WIDTH - PADDING:
            self.x = WIDTH - PADDING - 10
            self.velocity_x = -self.velocity_x
        elif self.x <= PADDING:
            self.velocity_x = -self.velocity_x
            self.x = PADDING + 10
        if self.y >= HEIGHT - PADDING:
            self.velocity_y = -self.velocity_y
            self.y = HEIGHT - PADDING - 10
        elif self.y <= PADDING:
            self.y = PADDING + 10
            self.velocity_y = -self.velocity_y

         # update pos with vel
        self.x += self.velocity_x
        self.y += self.velocity_y

    def align(self, boids):
        avg_vel_x, avg_vel_y = 0,0
        total = 0
        for boid in boids:
            if distance(self, boid) <  NEIGHBOR_RADIUS:
                avg_vel_x += boid.velocity_x
                avg_vel_y += boid.velocity_y
                total += 1
        if total > 0:
            avg_vel_x /= total
            avg_vel_y /= total

            # set velocity towards avg
            self.velocity_x += (avg_vel_x - self.velocity_x) * ALIGN_COEFF
            self.velocity_y += (avg_vel_y - self.velocity_y) * ALIGN_COEFF

    def cohesion(self, boids):
        center_x, center_y = 0,0
        total = 0
        for boid in boids:
            if distance(self, boid) < NEIGHBOR_RADIUS:
                center_x += boid.x
                center_y += boid.y
                total += 1
        if total > 0:
            center_x /= total
            center_y /= total

            #move towards center
            self.velocity_x += (center_x - self.x) * COHESION_COEFF
            self.velocity_y += (center_y - self.y) * COHESION_COEFF
    
    def separation(self, boids):
        move_x, move_y = 0,0
        for boid in boids:
            if distance(self , boid) < AVOID_RADIUS:
                move_x += self.x - boid.x
                move_y += self.y - boid.y
        self.velocity_x += move_x * SEPARATION_COEFF
        self.velocity_y += move_y * SEPARATION_COEFF

    def attract(self, reward):
        if reward:
            if distance(self, reward) < ATTRACT_RADIUS:
                self.velocity_x += (reward.x - self.x) * REWARD_COEFF
                self.velocity_y += (reward.y - self.y) * REWARD_COEFF
    
    def update(self, boids, reward):
        self.align(boids)
        self.cohesion(boids)
        self.separation(boids)
        self.attract(reward)
        self.check_vel()
        self.move()

    def check_vel(self):
        speed = math.sqrt(self.velocity_x ** 2 + self.velocity_y ** 2)
        if speed > MAX_VELOCITY:
            ratio = MAX_VELOCITY / speed
            self.velocity_x *= ratio
            self.velocity_y *= ratio

    def draw(self, screen):
        pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), BOID_RADIUS) # draw the boid 
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), AVOID_RADIUS, width=1) # draw the avoid radius
        pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), NEIGHBOR_RADIUS, width=1) # draw neighbor radius
        pygame.draw.line(screen, WHITE, (int(self.x), int(self.y)), (int(self.x + 10*self.velocity_x), int(self.y + 10*self.velocity_y)), width=2)

# Drawing text onto the screen
def draw_text(screen, text, position, size=30, color=WHITE, font_name = "Monospace"):
    font = pygame.font.SysFont(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = position
    screen.blit(text_surface, text_rect)

# Main function
def main():
    global ALIGN_COEFF, COHESION_COEFF, REWARD_COEFF, ATTRACT_RADIUS, AVOID_RADIUS, NEIGHBOR_RADIUS, BOID_RADIUS, SEPARATION_COEFF
    counter = 0
    boids = [Boid(random.randint(0,WIDTH-PADDING), random.randint(0, HEIGHT-PADDING)) for _ in range(NUM_BOIDS)]

    # states of the game
    running = True
    paused = False
    reward = None
    spacing = 30
    # create slider instances
    sliders = [
        Slider(50, HEIGHT - 8 * spacing, 200, 20, 0.00, 0.25, 0.01, "Alignment"),
        Slider(50, HEIGHT - 7 * spacing, 200, 20, 0.00, 0.25, 0.01, "Cohesion"),
        Slider(50, HEIGHT - 6 * spacing, 200, 20, 0.00, 0.10, 0.01, "Reward Attraction"),
        Slider(50, HEIGHT - 5 * spacing, 200, 20, 10, 500, 150, "Reward Radius"),
        Slider(50, HEIGHT - 4 * spacing, 200, 20, 0, 50, 15, "Avoid Radius"),
        Slider(50, HEIGHT - 3 * spacing, 200, 20, 0, 150, 30, "Neighbor Radius"),
        Slider(50, HEIGHT - 2 *  spacing, 200, 20, 1, 20, 4, "Boid Radius"),
        Slider(50, HEIGHT - 1 * spacing, 200, 20, 0.00, 0.2, 0.05, "Separation"),
    ]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused # toggle pause state
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not any(slider.is_over(event.pos) for slider in sliders):
                    mx, my = pygame.mouse.get_pos()
                    reward = Reward(mx,my,ATTRACT_RADIUS)
                    print(f"Reward coords: ({mx}, {my})")
            slider_handling = any(slider.handle_event(event) for slider in sliders)
        
        ALIGN_COEFF = sliders[0].val
        COHESION_COEFF = sliders[1].val
        REWARD_COEFF = sliders[2].val
        ATTRACT_RADIUS = sliders[3].val
        AVOID_RADIUS = sliders[4].val
        NEIGHBOR_RADIUS = sliders[5].val
        BOID_RADIUS = sliders[6].val
        SEPARATION_COEFF = sliders[7].val
        
        screen.fill(BLACK)
        
        # Draw the reward
        if reward:
            reward.draw(screen)
        # event loop to update all boids
        for boid in boids:
            if not paused:
                boid.update(boids, reward)
            boid.draw(screen)
        # draw sliders
        for slider in sliders:
            slider.draw(screen)

        # pausing mechanics
        if not paused:
            counter += 1
        if paused:
            draw_text(screen, "Paused", (WIDTH // 2, 50), color=YELLOW)
        
        # Print counter on screen
        draw_text(screen,f"Iteration:{str(counter)}", (100, 30), size= 20, font_name="Arial")

        # draw title
        draw_text(screen, "Boid Simulation", (WIDTH // 2, 20))
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()


