#dfs
graph={
    "kudal":["kankavli","malvan","vengurla","sawantwadi"],
    "kankavli":["vaibhavwadi","kudal","devgad","malvan"],
    "sawantwadi":["kudal","dodamarg","vengurla"],
    "malvan":["devgad","kankavli","kudal","vengurla"],
    "vengurla":["malvan","kudal","sawantwadi"],
    "devgad":["kankavli","malvan"],
    "dodamarg":["sawantwadi"],
    "vaibhavwadi":["kankavli"]
}
visited=[]
def dfs(node,visited,graph):
    if node not in visited:
        print(node)
        visited.append(node)
        for i in graph[node]:
            dfs(i,visited,graph)

dfs('kudal',visited,graph)


#bfs
graph={
    "kudal":["kankavli","malvan","vengurla","sawantwadi"],
    "kankavli":["vaibhavwadi","kudal","devgad","malvan"],
    "sawantwadi":["kudal","dodamarg","vengurla"],
    "malvan":["devgad","kankavli","kudal","vengurla"],
    "vengurla":["malvan","kudal","sawantwadi"],
    "devgad":["kankavli","malvan"],
    "dodamarg":["sawantwadi"],
    "vaibhavwadi":["kankavli"]
}
visited=[]
queue=[]
def bfs(node,visited,graph):
    visited.append(node)
    queue.append(node)
    while queue:
        m=queue.pop(0)
        print(m,end=' ')
        for i in graph[m]:
            if i not in visited:
                visited.append(i)
                queue.append(i)

bfs('kudal',visited,graph)








#nqueen
N=int(input("Enter the size of chessBoard : "))
def solveNQueens(board, col):
	if col == N:
		print(board)
		return True
	for i in range(N):
		if isSafe(board, i, col):
			board[i][col] = 1
			if solveNQueens(board, col + 1):
				return True
			board[i][col] = 0
	return False

def isSafe(board, row, col):
	for x in range(col):
		if board[row][x] == 1:
			return False
	for x, y in zip(range(row, -1, -1), range(col, -1, -1)):
		if board[x][y] == 1:
			return False
	for x, y in zip(range(row, N, 1), range(col, -1, -1)):
		if board[x][y] == 1:
			return False
	return True

board = [[0 for x in range(N)] for y in range(N)]
if not solveNQueens(board, 0):
	print("No solution found")



#tower of hanoi
def TOH(n,s,d,a):
	if n==1:
		print ("Move disk 1 from source",s,"to destination",d)
		return
	TOH(n-1,s,a,d)
	print ("Move disk",n,"from source",s,"to destination",d)
	TOH(n-1,a,d,s)
		
n = 3
TOH(n,'A','B','C') 




#alpha beta
def minimax(depth,nodeIndex,maximizingPlayer,values,alpha,beta):
    if depth==3:
        return values[nodeIndex]
    
    if maximizingPlayer:
        maxEval=float('-inf')
        for i in range(2):
            eval=minimax(depth+1,nodeIndex * 2 + i,False,values,alpha,beta)
            maxEval=max(maxEval,eval)
            alpha=max(alpha,eval)
            if beta <= alpha:
                break
        return maxEval

    else:
        minEval=float('inf')
        for i in range(2):
            eval=minimax(depth+1,nodeIndex * 2 + i,True,values,alpha,beta)
            minEval=min(minEval,eval)
            beta=min(beta,eval)
            if beta <= alpha:
                break
        return minEval
    

if __name__ == "__main__":
        values=[3,5,6,9,1,2,0,-1]
        optimal_value=minimax(0,0,True,values,float('-inf'),float('inf'))
        print("The optimal value is :",optimal_value)



#hill climb racing
import random
def objective_function(x):
    return -x**2 + 4*x

def generate_neighbor(current_x,step_size):
    return current_x+random.uniform(-step_size,step_size)

def hill_climbing(starting_point,step_size,max_iterations):
    current_x=starting_point
    current_value=objective_function(current_x)

    for _ in range(max_iterations):
        neighbor_x=generate_neighbor(current_x,step_size)
        neighbor_value=objective_function(neighbor_x)

        if neighbor_value>current_value:
            current_x=neighbor_x
            current_value=neighbor_value

    return current_x,current_value

starting_point=random.uniform(0,4)
step_size=0.1
max_iterations=100

best_x,best_value=hill_climbing(starting_point,step_size,max_iterations)

print(f"Best x:{best_x},Best value: {best_value}")


#a*
import heapq
def a_star(graph,heuristics,start,goal):
    open_list=[]
    heapq.heappush(open_list,(heuristics.get(start),0,start,[]))
    came_from={}
    cost_so_far={start:0}

    while open_list:
        f,current_cost,current_node,path=heapq.heappop(open_list)

        if current_node==goal:
             return path + [current_node]

        for neighbor,cost in graph.get(current_node,{}).items():
            new_cost=current_cost+cost
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor]=new_cost

                priority=new_cost+heuristics.get(neighbor)
                heapq.heappush(open_list,(priority,new_cost,neighbor,path + [current_node]))
                came_from[neighbor]=current_node

    return None

graph={
     'A':{'B':1,'C':4},
     'B':{'C':2,'D':5},
     'C':{'D':1},
     'D':{}
}

heuristics={
     'A':7,
     'B':6,
     'C':2,
     'D':0
}

start_node='A'
goal_node='D'
path=a_star(graph,heuristics,start_node,goal_node)

if path:
    print("Path found : ",path)
else:
    print("No path found")


#water jug
from collections import deque

def water_jug_fill_any_jug(m,n,d):
    queue=deque()
    queue.append((0,0,[]))

    visited=set()
    visited.add((0,0))

    while queue:
        a,b,path=queue.popleft()
        if a == d or b == d:
           
            return path
        possible_states=[
        (m,b,path +[(m,b)]),
        (a,n,path +[(a,n)]),
        (0,b,path +[(0,b)]),
        (a,0,path +[(a,0)]),
        (min(a+b,m),b-(min(a+b,m)-a),path+[
             (min(a+b,m),b-(min(a+b,m)-a))]),
        (a-(min(a+b,n)-b),min(a+b,n),path+[
            (a-(min(a+b,n)-b),min(a+b,n))])
         ]

        for state in possible_states:
            state_ab=(state[0],state[1])
            if state_ab not in visited:
               visited.add(state_ab)
               queue.append(state)
    return None
m=5
n=6
d=2

steps=water_jug_fill_any_jug(m,n,d)
if steps:
    print(f"it is  possible to measure exactely {d} liters in either jug. steps:")
    for i,step in enumerate(steps):
        print(f"step {i+1}: Jug 1= {step[0]} liters ,jug 2= {step[1]} liters ")
else:
    print(f"it is not possible to measure exactely {d} liters in either jug.")


#tic tac toe

# Initialize the board
board = ['' for _ in range(9)]

# Function to print the board
def print_board(board):
    for row in [board[i*3:(i+1)*3] for i in range(3)]:
        print('|'.join(cell if cell != '' else ' ' for cell in row))
        print('-'*5)

# Function to check for a win
def check_win(board, player):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
                      (0, 4, 8), (2, 4, 6)]  # diagonals
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
    return False

# Minimax algorithm
def minimax(board, depth, is_maximizing):
    if check_win(board, 'X'):
        return 1
    elif check_win(board, 'O'):
        return -1
    elif '' not in board:
        return 0

    if is_maximizing:
        best_score = -float('inf')  
        for i in range(9):
            if board[i] == '':
                board[i] = 'X'
                score = minimax(board, depth + 1, False)
                board[i] = ''
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == '':
                board[i] = 'O'
                score = minimax(board, depth + 1, True)
                board[i] = ''
                best_score = min(score, best_score)
        return best_score

# AI move using Minimax algorithm
def ai_move(board):
    best_score = -float('inf')
    move = None
    for i in range(9):
        if board[i] == '':
            board[i] = 'X'
            score = minimax(board, 0, False)
            board[i] = ''
            if score > best_score:
                best_score = score
                move = i
    if move is not None:       
        board[move] = 'X'

# Function to play the game
def play_game():
    while True:
        print_board(board)
        if check_win(board, 'X'):
            print("X wins!")
            break
        elif check_win(board, 'O'):
            print("O wins!")
            break
        elif '' not in board:
            print("It's a tie!")
            break

        # Player move
        try:
            move = int(input("Enter your move (1-9): ")) - 1
            if 0 <= move < 9 and board[move] == '':
                board[move] = 'O'
            else:
                print("Invalid move. Try again.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 9.")
            continue

        # AI move
        ai_move(board)

# Start the game
play_game()




#shuffle deck

import random
a=["Heart ","Diamond ","Club ","Spade "]
b=['Ace','2','3','4','5','6','7','8','9','10','Jack','Queen','King']
deck=[]
for i in a:
    for j in b:
        deck.append(i+j)
random.shuffle(deck)
print(deck)




#constraint
import constraint
import matplotlib.pyplot as plt
import networkx as nx

#Create a new problem instance
problem = constraint.Problem()

# Define the regions and their respective domains (colors)
regions = ['Kudal', 'Sawantwadi', 'Kankavli', 'Devgad', 'Malvan', 'Vengurla', 'Dodamarg','Vaibhavwadi']
colors = ['Red', 'Green', 'Blue','Pink','Black','Grey','Purple']
# Add variables to the problem
for region in regions:
    problem.addVariable(region, colors)
#Define the constraints
neighbors = {"Kudal":["Sawantwadi","Kankavli","Vengurla","Malvan"],
         "Sawantwadi":["Vengurla","Dodamarg","Kudal"],
         "Kankavli":["Malvan","Devgad","Kudal","Vaibhavwadi"],------
         "Devgad":["Kankavli","Malvan","Vaibhavwadi"],
         "Malvan":["Kankavli","Kudal","Devgad","Vengurla"],
         "Vengurla":["Sawantwadi","Kudal","Malvan"],
         "Dodamarg":["Sawantwadi"],
         "Vaibhavwadi":["Kankavli"] 
    }

for region, adjacent in neighbors.items():
    for neighbor in adjacent:
        problem.addConstraint(lambda region, neighbor: region != neighbor,(region,neighbor))
solution=problem.getSolution()
print(solution)

grp=nx.Graph(neighbors)
nx.draw(grp,with_labels=True,node_color="white",font_color="black")
plt.show()






#associative

a.Derive the expressions based on Associative Law. 
Code:
def assoc(a,b,c):
    left=a+(b+c)
    right=(a+b)+c
    if(left==right):
        print("a+(b+c)=(a+b)+c")
        print("Associative Law proved for addition")
    else:
        print("Associative Law Not proved for addition")
    print("\n")
    l=a*(b*c)
    r=(a*b)*c
    if(l==r):
        print("a*(b*c)=(a*b)*c")
        print("Associative Law proved for multiplication")
    else:
        print("Associative Law Not proved for multiplication")

a=int(input("Enter a : "))
b=int(input("Enter b : "))
c=int(input("Enter c : "))
assoc(a,b,c)



#distributive
def distri(a,b,c):
    left= a*(b + c)
    right= (a*b)+(a*c)
    if(left==right):
        print("a(b+c)=ab+ac")
        print("Distributive law proved(for Addition)")
    else:
        print("Distributive law Not proved")

    print("\n")
    
    le= a*(b-c)
    ri= (a*b)-(a*c)
    if(le==ri):
        print("a(b-c)=ab-ac")
        print("Distributive law proved(for Subtraction)")
    else:
        print("Distributive law Not proved")
a=int(input("Enter a : "))
b=int(input("Enter b : "))
c=int(input("Enter c : "))
distri(a,b,c)


#family

from graphviz import Digraph
class Person:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
        self.parents = []
        self.children = []  # Add a children list

    def add_parent(self, parent):
        self.parents.append(parent)
        parent.children.append(self)  # Automatically add this instance to the parent's children

# Create instances
john = Person("John", "male")
susan = Person("Susan", "female")
peter = Person("Peter", "male")
lisa = Person("Lisa", "female")
michael = Person("Michael", "male")
mary = Person("Mary", "female")
james = Person("James", "male")
anna = Person("Anna", "female")

# Establish relationships
peter.add_parent(john)
peter.add_parent(susan)
lisa.add_parent(john)
lisa.add_parent(susan)
michael.add_parent(peter)
michael.add_parent(mary)
anna.add_parent(james)
anna.add_parent(lisa)

def father(child):
    for parent in child.parents:
        if parent.gender == "male":
            return parent  # Return the parent object
    return None

def mother(child):
    for parent in child.parents:
        if parent.gender == "female":
            return parent  # Return the parent object
    return None

def grandfather(child):
    dad = father(child)
    if dad:  # Ensure dad is a Person object
        return father(dad)
    return None

def grandmother(child):
    mom = mother(child)
    if mom:  # Ensure mom is a Person object
        return mother(mom)
    return None

def siblings(person):
    result = []
    for parent in person.parents:
        for sibling in parent.children:
            if sibling != person and sibling not in result:
                result.append(sibling)
    return result

def brother(person):
    return [sibling.name for sibling in siblings(person) if sibling.gender == "male"]

def sister(person):
    return [sibling.name for sibling in siblings(person) if sibling.gender == "female"]

def uncle(child):
    for parent in child.parents:
        for sibling in siblings(parent):
            if sibling.gender == "male":
                return sibling.name
    return None

def aunt(child):
    for parent in child.parents:
        for sibling in siblings(parent):
            if sibling.gender == "female":
                return sibling.name
    return None

def cousin(person):
    cousins = []
    for parent in person.parents:
        for sibling in siblings(parent):
            cousins.extend(cousin.name for cousin in sibling.children)
    return cousins

def draw_family_tree():
    tree = Digraph(comment='Family Tree')
    
    # Define nodes
    tree.node('J', 'John')
    tree.node('S', 'Susan')
    tree.node('P', 'Peter')
    tree.node('L', 'Lisa')
    tree.node('M', 'Michael')
    tree.node('Mary', 'Mary')
    tree.node('James', 'James')
    tree.node('A', 'Anna')
    
    # Define edges (relationships)
    tree.edge('J', 'P', label='father')
    tree.edge('S', 'P', label='mother')
    tree.edge('J', 'L', label='father')
    tree.edge('S', 'L', label='mother')
    tree.edge('P', 'M', label='father')
    tree.edge('Mary', 'M', label='mother')
    tree.edge('James', 'A', label='father')
    tree.edge('L', 'A', label='mother')
    
    # Render tree
    tree.render('family_tree', view=True, format='png') 

# Print relationships
print("Father of Peter:", father(peter).name if father(peter) else None)
print("Mother of Peter:", mother(peter).name if mother(peter) else None)
print("Grandfather of Michael:", grandfather(michael).name if grandfather(michael) else None)
print("Grandmother of Michael:", grandmother(michael).name if grandmother(michael) else None)
print("Brother of Lisa:", brother(lisa))
print("Sister of Peter:", sister(peter))
print("Uncle of Michael:", uncle(michael))
print("Aunt of Anna:", aunt(anna))
print("Cousins of Michael:", cousin(michael))

draw_family_tree()
#derivative
import spacy

# Load the spaCy English model
nlp = spacy.load('en_core_web_sm')

def extract_predicates(sentence): 
    doc = nlp(sentence)
    predicates = []
    
    for token in doc:
        # Extract attributes and adjectival complements
        if token.dep_ in ['attr', 'acomp']:
            predicates.append(token.text)
        
        # Extract verbs excluding auxiliaries
        if token.pos_ == 'VERB' and token.dep_ != 'aux':
            predicates.append(token.lemma_)
    
    return sorted(set(predicates))

# Sample sentences
sentences = [
    "Sanchin is a cricketer.",
    "Sanchin is a cricketer and plays cricket.",
    "Some boys are intelligent."
]

# Extract and print predicates for each sentence
for sentence in sentences:
    predicates = extract_predicates(sentence)
    print(f"Predicates in the sentence '{sentence}': {predicates}")


#number puzzle
import numpy as np
import heapq

class PuzzleState:
    def __init__(self, board, zero_pos, moves=0, previous=None):
        self.board = board
        self.zero_pos = zero_pos
        self.moves = moves
        self.previous = previous
        self.cost = self.moves + self.heuristic()
    def heuristic(self):
        distance = 0
        for i in range(3):
            for j in range(3):
                value = self.board[i][j]
                if value != 0:  # Ignore the blank tile
                    target_x, target_y = divmod(value - 1, 3)
                    distance += abs(i - target_x) + abs(j - target_y)
        return distance
    def get_neighbors(self):
        neighbors = []
        x, y = self.zero_pos
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Down, Up, Right, Left
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                new_board = np.copy(self.board)
                new_board[x][y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[x][y]
                neighbors.append(PuzzleState(new_board, (new_x, new_y), self.moves + 1, self))
        return neighbors
    def __lt__(self, other):
        return self.cost < other.cost
def a_star(initial_board):
    initial_zero_pos = tuple(np.argwhere(initial_board == 0)[0])  # Get the first matching position
    initial_state = PuzzleState(initial_board, initial_zero_pos)
    goal_state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    priority_queue = []
    visited = set()
    heapq.heappush(priority_queue, initial_state)
    while priority_queue:
        current_state = heapq.heappop(priority_queue)
        if np.array_equal(current_state.board, goal_state):
            return current_state
        visited.add(tuple(map(tuple, current_state.board)))
        for neighbor in current_state.get_neighbors():
            if tuple(map(tuple, neighbor.board)) not in visited:
                heapq.heappush(priority_queue, neighbor)
    return None
def print_solution(solution):
    path = []
    while solution:
        path.append(solution.board)
        solution = solution.previous
    for step in reversed(path):
        print(step,"\n")


if __name__ == "__main__":
    initial_board = np.array([[1, 2, 3],
                              [5, 7, 8],
                              [6, 0, 4]])
    solution = a_star(initial_board)
    if solution:
        print("\nSolution found in {} moves:".format(solution.moves))
        
        print_solution(solution)

    else:
        print("No solution found.")
