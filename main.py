import cv2
from find_start_end_targets import find_start_end_nodes
from find_start_end_targets import find_start_end_nodes
from breadth_first_search import find_connectivity_path

IMAGE_PATH = 'gfap-1.png'
START_END_NODES = find_start_end_nodes(IMAGE_PATH)
PATH_COLOR = (255, 0, 255)
IMAGE = cv2.imread(IMAGE_PATH)


def main():
    print(find_connectivity_path(START_END_NODES[0], START_END_NODES[1], image_object=IMAGE, line_color=PATH_COLOR))


if __name__ == "__main__":
    main()
