import numpy as np
import pygame as pg
from pygame import *
from datetime import datetime, timedelta

# Window setup
X, Y = 1000, 1000
CELL_SIZE = 50

# Colors
WHITE = (255, 255, 255)


# Main function
def main():
    pg.init()
    screen = pg.display.set_mode((X, Y))
    clock = pg.time.Clock()
    
    def load_image(path, size):
        image = pg.image.load(path).convert_alpha()  # Ensure transparency is preserved
        return pg.transform.scale(image, size)  # Scale correctly
    
    background_map = load_image("map.png", (X, Y))
    food_image = load_image("food.png", (CELL_SIZE, CELL_SIZE))
    prey_image = load_image("prey.png", (CELL_SIZE, CELL_SIZE))
    predator_image = load_image("predator.png", (CELL_SIZE, CELL_SIZE))

    class Food(pg.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = food_image
            self.rect = self.image.get_rect()
            self.pos = pg.Vector2(np.random.randint(0, X), np.random.randint(0, Y))
            self.rect.center = self.pos

    class Creature(pg.sprite.Sprite):
        def __init__(self, image, speed):
            super().__init__()
            self.image = image
            self.rect = self.image.get_rect()
            self.pos = pg.Vector2(np.random.randint(0, X), np.random.randint(0, Y))
            self.speed = speed
            self.rect.center = self.pos
            self.energy = 100  # Each creature starts with 100 energy

        def move_towards(self, target_pos):
            direction = target_pos - self.pos
            if direction.length() > 0:
                direction = direction.normalize() * self.speed
                self.pos += direction
                self.rect.center = self.pos

        def check_dead(self):
            if self.energy <= 0:
                self.kill()

    class Prey(Creature):
        def __init__(self):
            super().__init__(prey_image, speed=2)

        def move(self, food_list):
            if food_list:
                closest_food = min(food_list, key=lambda f: self.pos.distance_to(f.pos))
                self.move_towards(closest_food.pos)
                self.eat(food_list)  # Try to eat food while moving
            else:
                self.pos += pg.Vector2(np.random.uniform(-1, 1), np.random.uniform(-1, 1)).normalize() * self.speed
            self.rect.center = self.pos

        def eat(self, food_list):
            # Eat the closest food if close enough
            for food in food_list:
                if self.pos.distance_to(food.pos) < CELL_SIZE:  # Close enough to eat
                    self.energy += 20  # Gain energy from food
                    food.kill()  # Remove food from the game
                    break  # Stop after eating one food

    class Predator(Creature):
        def __init__(self):
            super().__init__(predator_image, speed=3)

        def move(self, prey_list):
            if prey_list:
                closest_prey = min(prey_list, key=lambda p: self.pos.distance_to(p.pos))
                self.move_towards(closest_prey.pos)
                self.eat(prey_list)  # Try to eat prey while moving
            self.rect.center = self.pos

        def eat(self, prey_list):
            # Eat the closest prey if close enough
            for prey in prey_list:
                if self.pos.distance_to(prey.pos) < CELL_SIZE:  # Close enough to eat
                    self.energy += 30  # Gain energy from prey
                    prey.kill()  # Remove prey from the game
                    break  # Stop after eating one prey

    
    prey_group = pg.sprite.Group([Prey() for _ in range(10)])
    predator_group = pg.sprite.Group([Predator() for _ in range(5)])
    food_group = pg.sprite.Group([Food() for _ in range(20)])
    
    running = True
    start_time = datetime.now()
    while running and datetime.now() < start_time + timedelta(minutes=1):
        screen.blit(background_map, (0, 0))
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        
        # Update prey and predator movement and eating
        for prey in prey_group:
            prey.move(food_group.sprites())
            prey.check_dead()  # Check if the prey is dead due to energy depletion

        for predator in predator_group:
            predator.move(prey_group.sprites())
            predator.check_dead()  # Check if the predator is dead due to energy depletion
        
        food_group.draw(screen)
        prey_group.draw(screen)
        predator_group.draw(screen)
        
        pg.display.flip()
        clock.tick(30)
    
    pg.quit()

if __name__ == "__main__":
    main()
