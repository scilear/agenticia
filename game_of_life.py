import numpy as np
import matplotlib.pyplot as plt
import imageio

def initialize_grid(size):
    return np.random.choice([0, 1], size=size*size, p=[0.3, 0.7]).reshape(size, size)

def update_grid(grid):
    new_grid = grid.copy()
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            live_neighbors = np.sum(grid[i-1:i+2, j-1:j+2]) - grid[i, j]
            if grid[i, j] == 1 and (live_neighbors < 2 or live_neighbors > 3):
                new_grid[i, j] = 0
            elif grid[i, j] == 0 and live_neighbors == 3:
                new_grid[i, j] = 1
    return new_grid

size = 200
steps = 1000
fps = 6
filename = 'game_of_life.gif'

grid = initialize_grid(size)
images = []

for _ in range(steps):
    grid = update_grid(grid)
    plt.figure(figsize=(10, 10))
    plt.imshow(grid, cmap='binary')
    plt.axis('off')
    plt.savefig('temp.png', bbox_inches='tight', pad_inches=0.0)
    plt.close()
    images.append(imageio.imread('temp.png'))

imageio.mimsave(filename, images, fps=fps)

print('GIF saved as', filename)