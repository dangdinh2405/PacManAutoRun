import copy
from collections import deque

import AStar
import convert


class PathFinder:
    converter = convert.MatrixConverter()
    grid = converter.convertCoordinates()
    cd_array = copy.deepcopy(grid)
    matrix = converter.convertOneZero()

    def __init__(self):

        self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def bfs(self, matrix, start):
        rows, cols = len(matrix), len(matrix[0])

        queue = deque([start])
        visited = set([start])
        path = []

        while queue:
            current_row, current_col = queue.popleft()
            path.append((current_row, current_col))

            for dr, dc in self.directions:
                new_row, new_col = current_row + dr, current_col + dc

                if 0 <= new_row < rows and 0 <= new_col < cols and matrix[new_row][new_col] == 0 and (
                new_row, new_col) not in visited:
                    queue.append((new_row, new_col))
                    visited.add((new_row, new_col))
                    matrix[new_row][new_col] = 2  # Đánh dấu điểm đã được thăm

        return path

    def find_paths(self, matrix):
        rows, cols = len(matrix), len(matrix[0])
        paths = []

        for i in range(rows):
            for j in range(cols):
                if matrix[i][j] == 0:
                    path = self.bfs(matrix, (i, j))
                    paths.append(path)

        return paths

    def process_matrix(self):
        matrix = self.converter.convertOneZero()
        paths = self.find_paths(matrix)

        # Flatten the list of paths to a one-dimensional list
        flattened_path = [point for path in paths for point in path]

        return flattened_path

    def optimal(self):
        bfs = PathFinder()
        path = bfs.process_matrix()
        i = 0
        long = len(path)
        while i < long - 1:
            if not (abs(path[i][0] - path[i + 1][0]) + abs(path[i][1] - path[i + 1][1]) == 1):
                solver = AStar.AStar(path[i], path[i + 1])
                path1 = solver.astar()
                path1.pop(0)  # xóa phần tử đầu tiên
                path1.pop(-1)  # xóa phần tử cuối cùng
                path = path[:i + 1] + path1 + path[i + 1:]
                i = i - 1
                long = len(path)
            i = i + 1
        return path



path_finder = PathFinder()
result_path = path_finder.optimal()
print(result_path)
