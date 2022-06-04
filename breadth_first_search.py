import cv2
from queue import Queue


def find_connectivity_path(node_1, node_2, image_object, line_color):
    """Takes in a starting point and an end point (colored pixels on a binary image) and uses breadth first search
    algorithm to find a path to the points if it exists. Black pixels are taken as valid pixels for path tracing.
    An image with the path overlay is saved. The function returns a list of the path pixels and True if a path is found
    and False if no path exists. Nodes are (x, y) tuples, image object is the cv2 image, and line_color is RGB tuple
    (R, G, B)."""
    image = image_object
    width = image.shape[1]
    height = image.shape[0]
    valid_pixels_for_path = []

    def find_neighbors(px):
        x = px[0]
        y = px[1]
        neighbors = [
            (x - 1, y - 1),
            (x, y - 1),
            (x + 1, y - 1),
            (x - 1, y),
            (x + 1, y),
            (x - 1, y + 1),
            (x, y + 1),
            (x + 1, y + 1)
        ]
        neighbors = [(i, j) for (i, j) in neighbors if 0 <= i < width and 0 <= j < height]
        # neighbors = [e for e in neighbors if e in black_pixels]
        return neighbors

    # Find the black points in the image (valid path pixels)
    for g in range(width):
        for h in range(height):
            px_val = image[h, g]
            if tuple(px_val) == (0, 0, 0):
                valid_pixels_for_path.append((g, h))

    # Adds the start and end point to valid path pixels
    valid_pixels_for_path.append(node_1)
    valid_pixels_for_path.append(node_2)

    # Creates a dictionary with each pixel as a key and valid surrounding pixels or child nodes
    children = dict()
    for w in range(width):
        for h in range(height):
            pixel = (w, h)
            neighboring_pixels = find_neighbors((w, h))
            children[pixel] = neighboring_pixels

    def breadth_first_search(start_node, target_node):
        # make a list of visited nodes to save computation time
        visited_nodes = set()
        queue = Queue()

        # Add the start_node to the queue and visited list
        queue.put(start_node)
        visited_nodes.add(start_node)

        # start_node has no parents
        parent_nodes = dict()
        parent_nodes[start_node] = None

        # algorithm
        path_found = False
        while not queue.empty():
            # FIFO, first in first out.
            # Remove and return an item from the queue
            current_node = queue.get()
            if current_node == target_node:
                path_found = True
                break

            for next_node in children[current_node]:
                if (next_node not in visited_nodes) and (next_node in valid_pixels_for_path):
                    queue.put(next_node)
                    parent_nodes[next_node] = current_node
                    visited_nodes.add(next_node)

        # Determine the path by retracing tree by parents tag
        path = []
        if path_found:
            path.append(target_node)
            while parent_nodes[target_node] is not None:
                path.append(parent_nodes[target_node])
                target_node = parent_nodes[target_node]
            path.reverse()
        return path

    bfs_path_pixels = breadth_first_search(node_1, node_2)
    # color the path in the original image
    for p in bfs_path_pixels:
        image[p[1], p[0]] = line_color

    cv2.imshow('test', image)
    cv2.waitKey()
    cv2.destroyAllWindows()
    cv2.imwrite('BFS_Output.png', image)

    if bfs_path_pixels:
        return True, bfs_path_pixels
    else:
        return False, bfs_path_pixels


