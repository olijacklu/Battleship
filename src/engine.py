import random

#AI for the computer to find the optimal square to shoot at

#Fonction that calculates probability of a certain tile containing a boat
def cellprob(cell, grid):

	#If the cell is already occupied than it has 0 probability
	if cell.get_value() != 0 and cell.get_value() != 2:
		return 0

	#All boats that the computer still needs to find
	boat_sizes = grid.unsunk_boats

	total_prob = 0

	x = cell.x
	y = cell.y

	#See how many different boats can be placed in that square, which will be the score for that tile
	for size in boat_sizes:
		#Vertical possibilities
		for i in range(size):
			boat = Boat(x, x, y - i, y - i + size -1, grid.get_grid(), placement=False)
			if (not boat.get_invalid()) and grid.place_boat(boat, placement=False):
				total_prob += 1

		#Horizontal possibilities
		for i in range(size):
			boat = Boat(x-i, x -i + size -1, y, y, grid.get_grid(), placement=False)
			if (not boat.get_invalid()) and grid.place_boat(boat, placement=False):
				total_prob += 1

	return total_prob

'''Algorithm to decide which will be the next square the computer will shoot at. 'Misses' is a optional parameter
that allows the program to shoot randomly from time to time, if necessary

There are three different game modes:

EASY: computer just shoots randomly

MEDIUM: computer shoots randomly until it hits a boat, then it shoots around the boat (analysing all shot squares to decide if 
it is smarter to shoot horizontally or vertically) until the boats sinks

HARD: computer analysis probabilities for each square to determine what is the optimal square to shoot at. When hitting a boat, follow the
same algorithm as MEDIUM to sink the ship.

The parameter 'level' indicates which game difficulty is currently being considered
'''

def next_square(grid, misses=5, level=0):
	#Last squares the computer shot at
	last_cells = [cell.value for cell in grid.shot_cells[-misses:]] 

	#Shoot around a hit square
	if level != 0 and len(grid.high_priority) > 0:
		
		neighbouring_hits = {}

		#Check if it is better to shoot horizontally or vertically
		for cell1 in grid.high_priority:
			for cell2 in grid.high_priority:
				if cell1 in grid.high_priority[cell2]:
					if cell1.x == cell2.x:
						if (cell2, cell1) not in neighbouring_hits:
							neighbouring_hits[(cell1, cell2)] = 1
					else:
						if (cell2, cell1) not in neighbouring_hits:
							neighbouring_hits[(cell1, cell2)] = 0
		#Cells that should be prioritized because they are neighbours of a hit square
		high_priority_list = []


		#See which high priority cell we should shoot at
		if neighbouring_hits != {}:
			for (cell1, cell2) in neighbouring_hits:
				if neighbouring_hits[(cell1, cell2)] == 0:
					if min(cell1.x, cell2.x) > 0:
						cell = grid.grid[cell1.y][min(cell1.x, cell2.x)-1]
						if cell.get_value() == 0 or cell.get_value() == 2:
							high_priority_list.append(cell)
					if max(cell1.x, cell2.x) < grid.size-1:
						cell = grid.grid[cell1.y][max(cell1.x, cell2.x)+1]
						if cell.get_value() == 0 or cell.get_value() == 2:
							high_priority_list.append(cell)
				else:
					if min(cell1.y, cell2.y) > 0:
						cell = grid.grid[min(cell1.y, cell2.y)-1][cell1.x]
						if cell.get_value() == 0 or cell.get_value() == 2:
							high_priority_list.append(cell)
					if max(cell1.y, cell2.y) < grid.size-1:
						cell = grid.grid[max(cell1.y, cell2.y)+1][cell1.x]
						if cell.get_value() == 0 or cell.get_value() == 2:
							high_priority_list.append(cell)

		#If none of the all priority list cells are unavailable, just take one of the neighbours of the shot cell
		if len(high_priority_list) == 0:
			for l in grid.high_priority.values():
				high_priority_list += l		
		maxi = 0
		maxi_cells = []

		#Get the maximum element of the high priority list	

		for cell in high_priority_list:
			current = cellprob(cell, grid)

			if current > maxi:
				maxi = current
				maxi_cells = [cell]

			elif current == maxi:
				maxi_cells.append(cell)

		#Choose randomly between all squares of same probability
		maxi_cell = random.choice(maxi_cells)

		return (maxi_cell.y, maxi_cell.x)

	elif (len(grid.shot_cells) >= misses and not ( (3 in last_cells) or (4 in last_cells))) or level != 2:
		return grid.random_tile()
	#Find cell with highest probability
	maxi = 0
	maxi_cells = []
	for cell in grid.unshot_cells:

		current = cellprob(cell, grid)
		if current > maxi:
			maxi = current
			maxi_cells = [cell]

		elif current == maxi:
			maxi_cells.append(cell)

	maxi_cell = random.choice(maxi_cells)

	return (maxi_cell.y, maxi_cell.x)

#Boat class, implements basic boat behaviour
class Boat:
	#Check if a boat is valid (e.g, size matches x, y coordinates, boatg fits on grid, etc)
	def check_valid(self):
			#NOT a valid boat: gets off the grid
			if not (0<=self.begin_x<len(self.grid) and 0<=self.begin_y<len(self.grid) and 0<=self.end_x<len(self.grid) and 0<=self.end_y<len(self.grid)):
				self.invalid = True
				return False
			#NOT a valid boat: size doesn't match coordinates (vertical boat)
			elif(self.end_x == self.begin_x and abs(self.end_y - self.begin_y) == (self.size-1)):
				return True
			#NOT a valid boat: size doesn't match coordinates (horizontal boat)
			elif(self.end_y == self.begin_y and abs(self.end_x - self.begin_x) == (self.size-1)):
				return True

			#Marks boat as invalid
			self.invalid = True
			return False
	
	#Constructor - placement is an optional parameter that determines if we are really placing the boat or only simulating
	def __init__(self, begin_x, end_x, begin_y, end_y, grid, placement=True, size=None):
		self.direction = 0
		self.size = size
		self.grid = grid
		#Is size not given just calculate it given coordinates
		if size is None:
			self.size = max(abs(begin_x - end_x), abs(begin_y - end_y)) + 1
		
		
		self.pos = []
		self.begin_x = begin_x
		self.begin_y = begin_y
		self.end_x = end_x
		self.end_y = end_y
		self.sunk = False
		self.invalid = False

		#If the boat isn't valid just return
		if not self.check_valid(): 
			return
		
		#Check if there isn't some one boat where we want to place it
		if(begin_y == end_y):
			for i in range(min(begin_x, end_x), max(begin_x, end_x)+1):
				if(grid[begin_y][i].get_value() != 0):
					if(placement is False and (grid[begin_y][i].get_value() == 2 or grid[begin_y][i].get_value() == 3)):
						continue
					self.invalid = True
					return
				self.pos.append((begin_y, i))
		else:
			self.direction = 1
			for i in range(min(begin_y, end_y), max(begin_y, end_y)+1):
				if(grid[i][begin_x].get_value() != 0):
					if(placement is False and (grid[i][begin_x].get_value() == 2 or grid[i][begin_x].get_value() == 3)):
						continue
					self.invalid = True
					return
				self.pos.append((i, begin_x))
		
		self.sink_track = {}

		for p in self.pos:
			self.sink_track[p] = 0
	
	def get_sunk(self):
		return self.sunk

	def set_sunk(self, sunk):
		self.sunk = sunk

	def get_pos(self):
		
		return self.pos
	
	def hit(self, pos):
		self.sink_track[pos] = 1

	def get_invalid(self):
		return self.invalid

#Cell class, determines the behaviour of each of the grid's squares

class Cell:
	#Constructor
	def __init__(self, x, y, value=0):
		self.hit = False
		self.x = x
		self.y = y
		self.neighbours = []
		self.value = value
		self.boat = None

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y
	
	def get_value(self):
		return self.value

	def set_value(self, value):
		self.value = value
	
	def set_boat(self, boat):
		self.boat = boat
	
	def get_boat(self):
		return self.boat
		
#Grid class, generic class that rules behaviour of grids (place where we place the boats)
 
class Grid:

	def __init__(self, size, level=2, misses=500):
		self.size = size

		self.grid = []

		self.misses = misses

		self.level = level

		self.boat_list = []

		self.shot_cells = []

		self.unshot_cells = []

		self.unsunk_boats = []

		self.high_priority = {}

		self.boat_size_list = [2,2,3,3,4,4,5,7]
		
		self.unsunk_boats = self.boat_size_list

		
		self.boat_size_list.reverse()

		for i in range(size):
			row = []
			for j in range(size):
				new_cell = Cell(j, i)
				row.append(new_cell)
				self.unshot_cells.append(new_cell)
			self.grid.append(row)
		#0 if square was never shot at, 1 if it is water, 2 if there's a ship there, 3 if there's a hit boat there, 4 if there's 
		#a sunk boat there
		self.hit_dic = {0:'.', 1:'o', 2:'S', 3:'x', 4:'*'}

		#Find all neighbours of each cell
		for i in range(size):
			for j in range(size):
				if(i != 0):
					self.grid[i][j].neighbours.append(self.grid[i-1][j])
				if(i != size-1):
					self.grid[i][j].neighbours.append(self.grid[i+1][j])
				if(j != 0):
					self.grid[i][j].neighbours.append(self.grid[i][j-1])
				if(j != size-1):
					self.grid[i][j].neighbours.append(self.grid[i][j+1])
						
	#Print a grid
	def print_grid(self):
		print("    ", end="")
		for n in range(self.size):
			print(f" {n} ", end="")
		print("")
		for i, row in enumerate(self.grid):
			print(f"{i} - ", end="")
			for e in row:
				print(f" {self.hit_dic[e.get_value()]} ", end='')
			print("")
		
		print("")

	#Test if neighbours are correct (test purposes only)
	def test_neighbours(self):
		for row in self.grid:
			for cell in row:
				print(f"----({cell.x}, {cell.y})-------")
				for n in cell.neighbours:
					print(f"- {n.x}, {n.y}")

	def get_grid(self):
		return self.grid

	#Places a boat on the grid
	def place_boat(self, boat, placement=True):
		#First analysis if boat can be placed
		changes = []
		for (y,x) in boat.get_pos():
			if(self.grid[y][x].get_value() == 0):
				changes.append((y,x))
			else:
				if((self.grid[y][x].get_value() == 2 or self.grid[y][x].get_value() == 3) and placement is False):
					continue

				return False
		
		if placement is False:
			return True
		
		for (y,x) in changes:
			self.grid[y][x].set_value(2)
			self.grid[y][x].set_boat(boat)
		self.boat_list.append(boat)

		return True
	#Check if a boat has been sunk
	def check_sunk(self, boat):
		pos = boat.get_pos()

		for (y,x) in pos:
			if self.grid[y][x].get_value() != 3:
				return False
		for (y,x) in pos:
			self.grid[y][x].set_value(4)
		boat.set_sunk(True)

		
		for cell in list(self.high_priority):
			if cell.boat == boat:
				self.high_priority.pop(cell)
		
		self.unsunk_boats.remove(boat.size)

		return True

	#Shoots at a square on the grid
	def shoot(self, pos):
		y,x = pos
		if self.grid[y][x].get_value() == 0:
			self.grid[y][x].set_value(1)
		
		elif self.grid[y][x].get_value() == 1 or self.grid[y][x].get_value() == 3 or self.grid[y][x].get_value() == 4 :
			return False

		elif self.grid[y][x].get_value() == 2:
			self.grid[y][x].set_value(3)
			#Adding neighbours to high priority list so algorithm knows where it is best to shoot next time
			self.high_priority[self.grid[y][x]] =  self.grid[y][x].neighbours
			self.check_sunk(self.grid[y][x].get_boat())
		self.shot_cells.append(self.grid[y][x])
		self.unshot_cells.remove(self.grid[y][x])
		return True

	#Fonction used to place all boats on the map via terminal
	def place_all_boats(self):
		for s in self.boat_size_list:
			print("====================")
			print(f"Place a boat of size: {s}")
			while(1):
				x_ini = int(input("Boat's x START coordinate: "))
				x_end = int(input("Boat's x END coordinate: "))
				y_ini = int(input("Boat's y START coordinate: "))
				y_end = int(input("Boat's y END coordinate: "))
				boat = Boat(x_ini, x_end, y_ini, y_end, self.grid, True, s)
				if not boat.get_invalid() and self.place_boat(boat):
					break
				
				print("Invalid boat coordinates given demanded size!")
			self.print_grid()

	#Place all the boats randomly
	def place_all_boats_random(self):
		
		for s in self.boat_size_list:
			
			while(1):
				
				direction = random.randint(0,1)
				
				x_b = 0
				x_e = 0
				y_b = 0
				y_e = 0

				if(direction == 0):	
					x_b = random.randint(0, 9)
					x_e = x_b+random.choice([-1,1])*(s-1)
					y_b = random.randint(0,9)
					y_e = y_b
				else:
					y_b = random.randint(0, 9)
					y_e = y_b+random.choice([-1,1])*(s-1)
					x_b = random.randint(0,9)
					x_e = x_b

				boat = Boat(x_b, x_e, y_b, y_e, self.grid, True, s)
				
				if (not boat.get_invalid()) and self.place_boat(boat):
					break

	def get_boat_size_list(self):
		return self.boat_size_list

	def check_victory(self):
		for boat in self.boat_list:
			if not boat.get_sunk():
				return False
		
		return True
	
	#Prints the probabiblity matrix for the entire grid
	def prob_matrix(self):

		for row in self.grid:
			for cell in row:
				print(cellprob(cell, self), end = " ")
			print("")
	

#Inherits Grid class, specific behaviour for the player's grid
class GridPlayer(Grid):
		
	def __init__(self, size, level=2, misses=500):
		
		super().__init__(size, level, misses)

	#Finds a random tile in the grid
	def random_tile(self):
		cell = random.choice(self.unshot_cells)
		y = cell.get_y()
		x = cell.get_x()

		return (y, x)

	#Allows the machine to shoot randomly
	def shoot_random(self):
		y,x = self.random_tile()
		self.shoot((y,x))
	
	#AI's shot
	def shoot_pc(self):
		(y,x) = next_square(self, self.misses, self.level)
		
		self.shoot((y,x))

#Inherits Grid class, specific behaviour for the enemy grid
class GridPC(Grid):
	
	def __init__(self, size):
		super().__init__(size)
	
	def turn(self):
		pos = str(input("Choose a cell to shoot at: "))
		y = int(pos[0])
		x = int(pos[1])
		print(f"Entry: x:{x} , y:{y}")
		self.shoot((y,x))
		print("=========================")
		self.print_grid()
	
#Test the probabilities by printing the initial matrix
if __name__ == "__main__":

	grid = GridPC(10)
	for row in grid.get_grid():
		for cell in row:
			print(cellprob(cell, grid), end=" ")
		print("")
