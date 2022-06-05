import cv2
from find_start_end_targets import find_start_end_nodes
from find_start_end_targets import find_start_end_nodes
from breadth_first_search import find_connectivity_path

IMAGE_PATH = 'gfap_single_pixel_dots.png'
START_END_NODES = find_start_end_nodes(IMAGE_PATH)
PATH_COLOR = (255, 0, 120)
IMAGE = cv2.imread(IMAGE_PATH)


def flood(node_1, node_2, image_object, valid_path_rgb, fill_color, display_plot, have_end_node):
    """Flood Fills the image until it finds the target node. Colors the image and displays it if display_plot is True.
    node1 and node2 are (x, y) coordinates for the start and end points, valid_path_rgb is an RGB tuple for the color
    that the algorithm should follow for the fill, and fill_color is an RGB tuple for the fill color. If you want the
    flood fill to end once a target node is found, have_end_node should be True. If you want to fill the entire
    connected space, have_end_node is False."""

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
            if tuple(px_val) == valid_path_rgb:
                valid_pixels_for_path.append((g, h))

    # start node
    # check neighbors
    # if neighbor not in pixels
    # if white switch to black and add to list of visited

    current_pixel = node_1
    found_target = False
    visited_px = [node_1]
    while not found_target:
        neighbors = find_neighbors(current_pixel)
        for n in neighbors:
            if n == node_2 and have_end_node:
                found_target = True
                if display_plot:
                    cv2.imshow('image', image)
                    cv2.waitKey()
                    cv2.destroyAllWindows()
                cv2.imwrite('Flood_Filled.png', image_object)
                return True
            if n not in visited_px and tuple(image[n[1], n[0]]) == valid_path_rgb:
                visited_px.append(n)
                image[n[1], n[0]] = fill_color
                visited_px.append(n)
        try:
            current_pixel = visited_px[0]
            visited_px.remove(visited_px[0])
        except IndexError:
            break

    if not have_end_node:
        if display_plot:
            cv2.imshow('image', image)
            cv2.waitKey()
            cv2.destroyAllWindows()
        cv2.imwrite('Flood_Filled.png', image_object)


print(flood(START_END_NODES[0], START_END_NODES[1], image_object=IMAGE, fill_color=PATH_COLOR,
            display_plot=True, valid_path_rgb=(0, 0, 0), have_end_node=False))
