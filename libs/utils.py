from PIL import Image, ImageDraw
import numpy as np

# Return a mask based off the specified color
# Color should have a shape of (r, g, b) and a float value from 0.0 to 1.0
# Colored should be the image in array form, with expanded dimensions of axis=0,
# and the array has values from 0.0 to 1.0, same as color array.
def get_mask(colored, color):
    mask = np.ones(colored.shape, np.uint8)
    i, j = np.where(np.all(colored[0] == color, axis=-1))
    mask[0, i, j] = 0
    return mask


def image_to_array(image):
    array = np.asarray(image)
    return np.array(array / 255.0)

# Find all the regions of the masked picture
# All marked regions should have the value 0, all else should be 1
def find_regions(mask):
    # Gets all of the coordinates where the mask exists
    i, j = np.where(np.all(mask[0], axis=-1) == 0)
    if len(i) == 0:
        return []
    # Creates a tuple of the coordinates
    coords = [coord for coord in zip(j, i)]

    # Creates a dictionary with the coordinates as both key and value.
    neighbors = dict((y, {y}) for y in coords)

    for x, y in neighbors:
        candidates = (x + 1, y), (x, y + 1)
        for candidate in candidates:
            if candidate in neighbors:
                neighbors[x, y].add(candidate)
                neighbors[candidate].add((x, y))

    closed_list = set()

    def connected_component(pixel):
        region = set()
        open_list = {pixel}
        while open_list:
            pixel = open_list.pop()
            closed_list.add(pixel)
            open_list |= neighbors[pixel] - closed_list
            region.add(pixel)
        return region

    regions = []
    for pixel in neighbors:
        if pixel not in closed_list:
            regions.append(connected_component(pixel))
    regions.sort(key=len, reverse=True)
    return regions

# risk of box being bigger than the image
def expand_bounding(img, region, expand_factor=1.5, min_size = 256):
    #expand bounding box to capture more context
    x, y = zip(*region)
    min_x, min_y, max_x, max_y = min(x), min(y), max(x), max(y)
    width, height = img.size
    width_center = width//2
    height_center = height//2
    bb_width = max_x - min_x
    bb_height = max_y - min_y
    x_center = (min_x + max_x)//2
    y_center = (min_y + max_y)//2
    current_size = max(bb_width, bb_height)
    current_size  = int(current_size * expand_factor)
    max_size = min(width, height)
    if current_size > max_size:
        current_size = max_size
    elif current_size < min_size:
        current_size = min_size
    x1 = x_center - current_size//2
    x2 = x_center + current_size//2
    y1 = y_center - current_size//2
    y2 = y_center + current_size//2
    x1_square = x1
    y1_square = y1
    x2_square = x2
    y2_square = y2
    #move bounding boxes that are partially outside of the image inside the image
    if (y1_square < 0 or y2_square > (height - 1)) and (x1_square < 0 or x2_square > (width - 1)):
        #conservative square region
        if x1_square < 0 and y1_square < 0:
            x1_square = 0
            y1_square = 0
            x2_square = current_size
            y2_square = current_size
        elif x2_square > (width - 1) and y1_square < 0:
            x1_square = width - current_size - 1
            y1_square = 0
            x2_square = width - 1
            y2_square = current_size
        elif x1_square < 0 and y2_square > (height - 1):
            x1_square = 0
            y1_square = height - current_size - 1
            x2_square = current_size
            y2_square = height - 1
        elif x2_square > (width - 1) and y2_square > (height - 1):
            x1_square = width - current_size - 1
            y1_square = height - current_size - 1
            x2_square = width - 1
            y2_square = height - 1
        else:
            x1_square = x1
            y1_square = y1
            x2_square = x2
            y2_square = y2
    else:
        if x1_square < 0:
            difference = x1_square
            x1_square -= difference
            x2_square -= difference
        if x2_square > (width - 1):
            difference = x2_square - width + 1
            x1_square -= difference
            x2_square -= difference
        if y1_square < 0:
            difference = y1_square
            y1_square -= difference
            y2_square -= difference
        if y2_square > (height - 1):
            difference = y2_square - height + 1
            y1_square -= difference
            y2_square -= difference
    # if y1_square < 0 or y2_square > (height - 1):

    #if bounding box goes outside of the image for some reason, set bounds to original, unexpanded values
    #print(width, height)
    if x2_square > width or y2_square > height:
        print("bounding box out of bounds!")
        print(x1_square, y1_square, x2_square, y2_square)
        x1_square, y1_square, x2_square, y2_square = min_x, min_y, max_x, max_y
    return x1_square, y1_square, x2_square, y2_square

def is_right_color(pixel, r2, g2, b2):
    r1, g1, b1 = pixel
    return r1 == r2 and g1 == g2 and b1 == b2

# Draws boxes around the found censor regions.
if __name__ == '__main__':
    image = Image.open(r'D:\VirtualPython\venv\DeepCreamPy\decensor_input\mermaid_censored.png')
    no_alpha_image = image.convert('RGB')
    draw = ImageDraw.Draw(no_alpha_image)
    
    ### Original
    # for region in find_regions(no_alpha_image, [0, 255, 0]):
    #     draw.rectangle(expand_bounding(no_alpha_image, region), outline=(0, 255, 0))
    # no_alpha_image.show()
    ### END OF ORIGINAL

    ### With new mask region finder
    ori_array = np.asarray(no_alpha_image)
    ori_array = np.array(ori_array / 255.0)
    ori_array = np.expand_dims(ori_array, axis=0)
    mask = get_mask(ori_array, [0.0, 1.0, 0.0])
    regions = find_regions(mask)
    for region in regions:
        draw.rectangle(expand_bounding(no_alpha_image, region), outline=(0, 255, 0))
    no_alpha_image.show()
    ### END OF NEW MASK REGION FINDER
