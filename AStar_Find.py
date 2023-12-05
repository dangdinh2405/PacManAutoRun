import numpy as np
import copy
import heapq
import AStar
import convert


class AStarFind:
    converter = convert.MatrixConverter()
    grid = converter.convertCoordinates()
    cd_array = copy.deepcopy(grid)
    matrix = np.array(converter.convertOneZero())  # Convert to NumPy array

    def __init__(self):
        self.visited = set()
        self.path = []
        self.steps = 0
        self.goal = (self.matrix.shape[0] // 2, self.matrix.shape[1] // 2)

    def heuristic(self, current, goal):
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

    def get_neighbors(self, position):
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        result = []
        for dx, dy in neighbors:
            new_x, new_y = position[0] + dx, position[1] + dy
            if 0 <= new_x < self.matrix.shape[0] and 0 <= new_y < self.matrix.shape[1]:
                result.append((new_x, new_y))
        return result

    def astar(self, start):
        priority_queue = [(0, start)]
        cost_so_far = {start: 0}

        while priority_queue:
            current_cost, current_vertex = heapq.heappop(priority_queue)

            if current_vertex == self.goal:
                break

            if current_vertex not in self.visited and self.matrix[current_vertex[0]][current_vertex[1]] == 0:
                self.path.append(current_vertex)
                self.visited.add(current_vertex)
                self.steps += 1

                neighbors = self.get_neighbors(current_vertex)
                for neighbor in neighbors:
                    if self.matrix[neighbor[0]][neighbor[1]] == 1:  # Check if it's a wall
                        continue

                    new_cost = cost_so_far[current_vertex] + 1  # Assuming a cost of 1 to move to a neighboring cell

                    if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                        cost_so_far[neighbor] = new_cost
                        priority = new_cost + self.heuristic(neighbor, self.goal)
                        heapq.heappush(priority_queue, (priority, neighbor))

        return self.path, self.steps

    def optimal(self,location):
        a_star = AStarFind()
        path, total_steps = a_star.astar(location)
        i = 0
        long = len(path)
        while i < long - 1:
            if not (abs(path[i][0] - path[i + 1][0]) + abs(path[i][1] - path[i + 1][1]) == 1):
                solver = AStar.AStar(path[i], path[i + 1])
                path1, sleps = solver.astar()
                path1.pop(0)
                path1.pop(-1)
                path = path[:i + 1] + path1 + path[i + 1:]
                i = i - 1
                long = len(path)
            i = i + 1
        return path, total_steps + sleps


# # Example usage:
# a_star = AStarFind()
# path, steps = a_star.optimal((2, 2))
# print(path)
# print(steps)
