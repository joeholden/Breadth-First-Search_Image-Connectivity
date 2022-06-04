import cv2


def find_start_end_nodes(img_path):
    image = cv2.imread(img_path)
    dims = image.shape

    width = dims[1]
    height = dims[0]
    pxlz = []

    for x in range(width):
        for y in range(height):
            px_val = image[y, x]
            pxlz.append(tuple(px_val))

    pixel_set = set(pxlz)
    non_bw_rgb = None
    for rgb in pixel_set:
        if rgb != (0, 0, 0) and rgb != (255, 255, 255):
            non_bw_rgb = rgb

    nodes = []
    for x in range(width):
        for y in range(height):
            px_val = image[y, x]
            if tuple(px_val) == non_bw_rgb:
                nodes.append((x, y))

    return nodes


