import numpy as np
import pygame as pg
import random
from pygame import *
from tkManager import TkinterManager
from datetime import datetime,timedelta

# Grid setup
X = 1000
Y = 1000
CELL_SIZE = 20

# Game parameters
size_modifier = 1
speed_range_modifier = 3
sense_range_modifier = 1


# Sprites
background_map = pg.image.load("map.png")
background_map = pg.transform.scale(background_map, (X,Y))
food_image = pg.image.load("image.png")
food_image = pg.transform.scale(food_image, (CELL_SIZE,CELL_SIZE))
prey_image = pg.image.load("prey.png")
prey_image = pg.transform.scale(prey_image, (CELL_SIZE,CELL_SIZE))
predator_image = pg.image.load("predator.png")
predator_image = pg.transform.scale(predator_image, (CELL_SIZE,CELL_SIZE))

class Grid():
    def __init__(self, width, height, cell_size):
        self.columns = width // cell_size
        self.rows = height // cell_size
        self.cell_size = cell_size
        self.occupied_positions = set()
        self.prey_positions = set()  # Allows predators to step on prey
        self.predator_positions = set()  # Prevents predators from stacking
        self.cells = [[pg.Rect(col * cell_size, row * cell_size, cell_size, cell_size) for col in range(self.columns)] for row in range(self.rows)] 
           
    def draw(self, surface):
        grid_colour = (220,220,220)
        for row in self.cells:
            for cell in row:
                pg.draw.rect(surface, grid_colour, cell, 1)

class Food(pg.sprite.Sprite):
    def __init__(self,grid):
        pg.sprite.Sprite.__init__(self)
        self.energy = 20
        self.image = food_image
        self.rect= self.image.get_rect()
        
        while True:  # Ensure food does not spawn on occupied cells
            row = np.random.randint(0, grid.rows)
            col = np.random.randint(0, grid.columns)
            if (row, col) not in grid.occupied_positions:
                break
            
        self.pos = np.array([row,col], dtype = int)
        self.rect.topleft = (col * grid.cell_size, row * grid.cell_size)
        
class Creature(pg.sprite.Sprite):
    def __init__(self, behavior,grid):
        pg.sprite.Sprite.__init__(self)
        self.size = CELL_SIZE
        self.speed_range = CELL_SIZE
        self.sense_range = CELL_SIZE * 5
        self.energy = 100
        self.grid = grid
        self.behavior = behavior  # "random", "seeking"
        row = np.random.randint(0, grid.rows)
        col = np.random.randint(0, grid.columns)
        self.pos = np.array([row * grid.cell_size, col * grid.cell_size], dtype=float)

    def move(self):
        self.pos += np.array(np.random.choice([-CELL_SIZE, 0, CELL_SIZE], size=2), dtype=float)
        self.rect.topleft = tuple(self.pos.astype(int))  # Ensures integer coordinates
    
    def eat(self):
        pass
            
    def check_dead(self):
        if self.energy == 0:
            self.grid.occupied_positions.discard(tuple(self.pos.astype(int)))
            self.kill()
            

class Prey(Creature):
    
    def __init__(self, behavior, grid):
        super().__init__(behavior, grid)
        self.size = CELL_SIZE * size_modifier
        self.speed_range = CELL_SIZE * speed_range_modifier
        self.speed_range = round(self.speed_range / CELL_SIZE) * CELL_SIZE
        self.sense_range = 50 * sense_range_modifier
        self.image = pg.transform.scale(prey_image, (self.size,self.size))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos.copy()
        
    def eat(self, food_list):
        for food in food_list:
            # Get position of food (rounded to nearest grid cell)
            food_pos = np.array(food.rect.topleft)
            food_pos = np.round(food_pos / CELL_SIZE) * CELL_SIZE  # Align to grid
            if np.linalg.norm(self.pos - food_pos) < CELL_SIZE:
                self.energy += food.energy  # Regain energy
                food.kill()  # Remove food from the game
                pg.display.update()
                break  # Stop after eating one food item
            
    def move(self, food_list):
        old_pos = tuple(self.pos.astype(int))
        
        possible_moves = []
        for i in range(self.speed_range):
            possible_moves.append(self.pos + np.array([-(i+1), 0]))  # Left
            possible_moves.append(self.pos + np.array([i+1, 0]))   # Right
            possible_moves.append(self.pos + np.array([0, -(i+1)]))  # Up
            possible_moves.append(self.pos + np.array([0, i+1]))   # Down
            possible_moves.append(self.pos + np.array([-(i+1), -(i+1)]))  # Top-left
            possible_moves.append(self.pos + np.array([-(i+1), i+1]))  # Bottom-left
            possible_moves.append(self.pos + np.array([i+1, -(i+1)]))  # Top-right
            possible_moves.append(self.pos + np.array([i+1, i+1]))  # Bottom-right


        # Filter valid moves (inside grid & not occupied by another prey)
        valid_moves = [
            move for move in possible_moves
            if 0 <= move[0] < self.grid.rows * CELL_SIZE and 
            0 <= move[1] < self.grid.columns * CELL_SIZE and 
            tuple(move.astype(int)) not in self.grid.prey_positions
        ]

        new_pos = self.pos.copy()

        if self.behavior == "random":
            if valid_moves:
                new_pos = random.choice(valid_moves)

        elif self.behavior == "seeking" and food_list:
            target_positions = np.array([food.rect.topleft for food in food_list])
            distances = np.sum((target_positions - self.pos) ** 2, axis=1)
            closest_target_index = np.argmin(distances)
            target_pos = target_positions[closest_target_index]

            direction = target_pos - self.pos
            norm = np.linalg.norm(direction)

            if norm != 0:
                move_attempt = self.pos + (direction / norm) * self.speed_range
                move_attempt = np.round(move_attempt / CELL_SIZE) * CELL_SIZE  # Snap to grid

                if tuple(move_attempt.astype(int)) in [tuple(move.astype(int)) for move in valid_moves]:
                    new_pos = move_attempt
                elif valid_moves:
                    new_pos = random.choice(valid_moves)  # Pick a random valid move if preferred move is blocked

        # FINAL CHECK: If still no valid move, stay in place
        if tuple(new_pos.astype(int)) in self.grid.occupied_positions:
            new_pos = self.pos  
            
        print(f"Old Pos: {self.pos}, New Pos: {new_pos}, Speed Range: {self.speed_range}")

        # Remove old position from tracking sets
        self.grid.occupied_positions.discard(old_pos)
        self.grid.prey_positions.discard(old_pos)

        self.pos = new_pos
        self.rect.topleft = tuple(self.pos.astype(int))

        # Update tracking sets with new position
        self.grid.prey_positions.add(tuple(self.pos.astype(int)))
        self.grid.occupied_positions.add(tuple(self.pos.astype(int)))

        # Reduce energy
        self.energy -= 2

        

class Predator(Creature):
    def __init__(self, behavior, grid):
        super().__init__(behavior, grid)
        self.image = predator_image
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos.copy()
        self.speed = CELL_SIZE * 2
        self.known_prey_locations = []
    
    def communicate(self, predators):
        all_prey_locations = set(self.known_prey_locations)
        for predator in predators:
            all_prey_locations.update(predator.known_prey_locations)
        self.known_prey_locations = list(all_prey_locations)
        
    def move(self, prey_list, predators):
        old_pos = tuple(self.pos.astype(int))

        # Share knowledge with other predators
        self.communicate(predators)

        # If prey exists, track it
        if prey_list:
            target_positions = np.array([prey.rect.topleft for prey in prey_list])
            distances = np.sum((target_positions - self.pos) ** 2, axis=1)
            closest_target_index = np.argmin(distances)
            target_pos = target_positions[closest_target_index]
            self.known_prey_locations.append(tuple(target_pos))

        # If no prey is in sight, rely on known locations from communication
        elif self.known_prey_locations:
            target_pos = np.array(self.known_prey_locations[-1])  # Use last known location

        else:
            return  # No prey seen, stay still

        # Move toward the best step (as previously implemented)
        move_options = [
            (self.pos + np.array([-CELL_SIZE, 0])),   # Left 1-step
            (self.pos + np.array([CELL_SIZE, 0])),    # Right 1-step
            (self.pos + np.array([0, -CELL_SIZE])),   # Up 1-step
            (self.pos + np.array([0, CELL_SIZE])),    # Down 1-step
            (self.pos + np.array([-2 * CELL_SIZE, 0])),  # Left 2-step
            (self.pos + np.array([2 * CELL_SIZE, 0])),   # Right 2-step
            (self.pos + np.array([0, -2 * CELL_SIZE])),  # Up 2-step
            (self.pos + np.array([0, 2 * CELL_SIZE]))    # Down 2-step
        ]

        valid_moves = [
            move for move in move_options
            if 0 <= move[0] < self.grid.rows * CELL_SIZE and 
            0 <= move[1] < self.grid.columns * CELL_SIZE and 
            tuple(move.astype(int)) not in self.grid.predator_positions
        ]

        if valid_moves:
            best_move = min(valid_moves, key=lambda move: np.linalg.norm(target_pos - move))
            new_pos = best_move
        else:
            new_pos = self.pos

        self.grid.occupied_positions.discard(old_pos)
        self.grid.predator_positions.discard(old_pos)
        self.pos = new_pos
        self.grid.predator_positions.add(tuple(self.pos.astype(int)))
        self.grid.occupied_positions.add(tuple(self.pos.astype(int)))
        self.rect.topleft = tuple(self.pos.astype(int))
        self.energy -= 2
            
    def eat(self, prey_list):
        for prey in prey_list:
            prey_pos = np.array(prey.rect.topleft)
            prey_pos = np.round(prey_pos / CELL_SIZE) * CELL_SIZE
            if tuple(self.pos.astype(int)) == tuple(prey_pos.astype(int)):
                self.energy += 0.8 * prey.energy
                prey.kill()
                break

    def check_dead(self):
        if self.energy <= 0:
            self.grid.occupied_positions.discard(tuple(self.pos.astype(int)))
            self.kill()

def main():
    
    tkinter_manager = TkinterManager()
    if tkinter_manager.get_verified() == True and tkinter_manager.get_settings_confirmed() == True and True:
        pg.init()
        display_surface = pg.display.set_mode((X, Y ))
        display_surface.fill("white")
        display_surface.blit(background_map, (0,0))
        pg.display.set_caption('Simulation') 
        clock = pg.time.Clock()
        
        grid = Grid(X,Y,CELL_SIZE)
        
        prey_sprites = pg.sprite.Group()
        predator_sprites = pg.sprite.Group()
        for _ in range(tkinter_manager.get_preynum()):
            prey_sprites.add(Prey(np.random.choice(["random", "seeking"]),grid))
        
        for _ in range(tkinter_manager.get_predatornum()):
            predator_sprites.add(Predator(np.random.choice(["random", "seeking"]),grid))

        food_sprites = pg.sprite.Group()
        for _ in range(tkinter_manager.get_foodnum()):
            food_sprites.add(Food(grid))

        simulationOn = True
        start_time = datetime.now()
        now_time = datetime.now()
        while simulationOn and now_time < start_time + timedelta(minutes= 1):
            pg.display.flip()
            if len(food_sprites) == 0 or len(prey_sprites) == 0:
                simulationOn = False
            for event in pg.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_BACKSPACE:
                        simulationOn = False
                elif event.type == pg.QUIT:
                    simulationOn = False

            # Draw food
            display_surface.blit(background_map, (0, 0))
            grid.draw(display_surface)
            food_sprites.draw(display_surface)

            # Update creatures
            for prey in prey_sprites:
                prey.move(food_sprites.sprites())
                prey.eat(food_sprites.sprites())
                prey.check_dead()
                prey_sprites.draw(display_surface)
                
            for predator in predator_sprites:
                predator.move(prey_sprites.sprites(), predator_sprites.sprites())
                predator.eat(prey_sprites.sprites())
                predator.check_dead()
                predator_sprites.draw(display_surface)
            
            pg.display.flip()
            clock.tick(tkinter_manager.get_speed())

        pg.QUIT


if __name__ == "__main__":
    main()
