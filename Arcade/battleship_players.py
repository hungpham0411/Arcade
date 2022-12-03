import random

class Ship:
    def __init__(self, size):
        self.row = random.randrange(0, 9)
        self.column = random.randrange(0, 9)
        self.size = size
        self.orientation = random.choice(["h", "v"]) # Horizontal or vertical ship choice
        self.indexes = self.compute_indexes()   # List of the ship indexes on the grid that represents the position of the ship
        
    def compute_indexes(self):
        start_index = self.row * 10 + self.column
        if self.orientation == "h":
            return [start_index + i for i in range(self.size)]
        elif self.orientation == "v":
            return [start_index + i*10 for i in range(self.size)]

class Player:
    def __init__(self):
        self.ships = []
        self.search = ["U"] * 100 # "U" is for unknown ships
        self.place_ships(sizes = [5, 4, 3, 3, 2]) # Ship sizes are the following
        list_of_lists = [ship.indexes for ship in self.ships]
        self.indexes = [index for sublist in list_of_lists for index in sublist]
    
    def place_ships(self, sizes):
        for size in sizes:
            placed = False
            while not placed:
                # Create new ship
                ship = Ship(size)
                
                # Check if placement is possible
                possible = True
                for index in ship.indexes:
                    
                    # Indexes must be less than 100
                    if index >= 100:
                        possible = False
                        break
                    
                    # Ships must stay in boundary
                    new_row = index // 10
                    new_col = index % 10
                    if new_row != ship.row and new_col != ship.column:
                        possible = False
                        break
                        
                    # Ships cannot intersect
                    for other_ship in self.ships:
                        if index in other_ship.indexes:
                            possible = False
                            break
                            
                # Place the ship
                if possible == True:
                    self.ships.append(ship)
                    placed = True

    # If needed for debugging you can run this and a graph will show (NOT THE ACTUAL GAME!)
    def show_ships(self):
        indexes = ["-" if i not in self.indexes else "X" for i in range(100)] # "-" represenets water while "X" represents a ship placement
        for row in range(10):
            print(" ".join(indexes[(row - 1)*10:row * 10]))
        

