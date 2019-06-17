from PIL import Image, ImageDraw
import numpy as np


def get_mask(colored, color):
    mask = np.ones(colored.shape, np.uint8)
    i, j = np.where(np.all(colored[0] == color, axis=-1))
    mask[0, i, j] = 0
    return mask


def image_to_array(image):
    array = np.asarray(image)
    return np.array(array / 255.0)


def region_by_mask(mask):
    i, j = np.where(np.all(mask[0], axis=-1) == 0)
    if len(i) == 0:
        return []
    coords = [coord for coord in zip(j, i)]
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

# find strongly connected components with the mask color


def find_regions(image, mask_color):
    pixel = image.load()
    neighbors = dict()
    width, height = image.size
    for x in range(width):
        for y in range(height):
            if is_right_color(pixel[x,y], *mask_color):
                neighbors[x, y] = {(x,y)}
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
    regions.sort(key = len, reverse = True)
    return regions


def find_color_regions(image, target_color=(0, 0, 0), threshhold=(1, 1)):
    target_color = np.array(target_color) * 255.0
    # print(target_color)
    low_t = (target_color[0] - threshhold[0], target_color[1] - threshhold[0], target_color[2] - threshhold[0])
    high_t = (target_color[0] + threshhold[1], target_color[1] + threshhold[1], target_color[2] + threshhold[1])
    # print(low_t, high_t)
    pixel = image.load()
    neighbors = dict()
    width, height = image.size
    for x in range(width):
        for y in range(height):
            r, g, b = pixel[x, y]
            if low_t[0] <= r and r <= high_t[0] and \
               low_t[1] <= g and g <= high_t[1] and \
               low_t[2] <= b and b <= high_t[2]:
                neighbors[x, y] = {(x, y)}
    for x, y in neighbors:
        candidates = []
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


def expand_bounding_mk2(img, region, expand_factor=1.50, min_size=256, max_size=512):
    # expand bounding box to capture more context
    if not isinstance(region, set) and len(region) == 4:
        min_x, min_y, max_x, max_y = region[0], region[1], region[2], region[3]
    else:
        x, y = zip(*region)
        min_x, min_y, max_x, max_y = min(x), min(y), max(x), max(y)

    # print("MinX {}, MinY {}, MaxX {}, MaxY, {}".format(min_x, min_y, max_x, max_y))

    width, height = img.size
    bb_width = max_x - min_x
    bb_height = max_y - min_y
    x_center = (min_x + max_x)//2
    y_center = (min_y + max_y)//2
    current_size = max(bb_width, bb_height)
    current_size = int(current_size * expand_factor)
    bb_width = int(bb_width * expand_factor)
    bb_height = int(bb_height * expand_factor)
    if bb_width > max_size:
        bb_width = max_size
    if bb_width < min_size:
        bb_width = min_size

    if bb_height > max_size:
        bb_height = max_size
    if bb_height < min_size:
        bb_height = min_size

    x1 = x_center - bb_width//2
    x2 = x_center + bb_width//2
    y1 = y_center - bb_height//2
    y2 = y_center + bb_height//2
    x1_square = x1
    y1_square = y1
    x2_square = x2
    y2_square = y2

    if (y1_square < 0 or y2_square > (height - 1)) and (x1_square < 0 or x2_square > (width - 1)):
        # conservative square region
        if x1_square < 0 and y1_square < 0:
            x1_square = 0
            y1_square = 0
            x2_square = bb_width
            y2_square = bb_height
        elif x2_square > (width - 1) and y1_square < 0:
            x1_square = width - bb_width - 1
            y1_square = 0
            x2_square = width - 1
            y2_square = bb_height
        elif x1_square < 0 and y2_square > (height - 1):
            x1_square = 0
            y1_square = height - bb_height - 1
            x2_square = bb_width
            y2_square = height - 1
        elif x2_square > (width - 1) and y2_square > (height - 1):
            x1_square = width - bb_width - 1
            y1_square = height - bb_height - 1
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

    if x2_square > width or y2_square > height:
        print("bounding box out of bounds!")
        print(x1_square, y1_square, x2_square, y2_square)
        x1_square, y1_square, x2_square, y2_square = min_x, min_y, max_x, max_y
    return int(x1_square), int(y1_square), int(x2_square), int(y2_square)


def bounding_box_check_mk2(size, box1, box2, target_size=(512, 512)):
    # expand bounding box to capture more context
    #    print("Creating new box for box1: {b1}, and box2: {b2}".format(b1=box1, b2=box2))
    inside = True
    minX = min(box1[0], box1[2], box2[0], box2[2])
    maxX = max(box1[0], box1[2], box2[0], box2[2])
    minY = min(box1[1], box1[3], box2[1], box2[3])
    maxY = max(box1[1], box1[3], box2[1], box2[3])

#    print("BEFORE -- MaxX: {maxx}, MinX: {minx}, MaxY: {maxy}, MinY: {miny}".format(maxx=maxX, minx=minX, maxy=maxY, miny=minY))

    b_width = maxX - minX
    if b_width <= target_size[0]:
        dist_left = target_size[0] - b_width
        if dist_left != 0:
            minX = round(minX - dist_left/2)
            maxX = round(maxX + dist_left/2)
    else:
        inside = False
#        print(b_width)

    b_height = maxY - minY
    if b_height <= target_size[1]:
        dist_left = target_size[1] - b_height
        if dist_left != 0:
            minY = round(minY - dist_left/2)
            maxY = round(maxY + dist_left/2)
    else:
        inside = False

    minX, minY = shift(size, minX, minY)

#    print("MaxX: {maxx}, MinX: {minx}, MaxY: {maxy}, MinY: {miny}".format(maxx=maxX, minx=minX, maxy=maxY, miny=minY))

    if (minX < 0 or minX + target_size[0] > size[0]):
        print("No possible box of size 512,512 possible")
        maxX = size[0]
    else:
        maxX = minX + target_size[0]

    if (minY < 0 or minY + target_size[1] > size[1]):
        maxY = size[0]
    else:
        maxY = minY + target_size[1]

    return [inside, (minX, minY, maxX, maxY)]


def big_bound_check_mk2(size, big_box, box1, boxes, target_size=(512, 512)):
    inside = True

    maxX = max(box1[0], box1[2])
    maxY = max(box1[1], box1[3])

    minX = min(box1[0], box1[2])
    minY = min(box1[1], box1[3])

    for box in boxes:
        maxX = max(maxX, box[0], box[2])
        maxY = max(maxY, box[1], box[3])

        minX = min(minX, box[0], box[2])
        minY = min(minY, box[1], box[3])

    b_width = maxX - minX
    if b_width <= target_size[0]:
        dist_left = target_size[0] - b_width
        if dist_left != 0:
            minX = round(minX - dist_left/2)
            maxX = round(maxX + dist_left/2)
    else:
        inside = False

    b_height = maxY - minY
    if b_height <= target_size[1]:
        dist_left = target_size[1] - b_height
        if dist_left != 0:
            minY = round(minY - dist_left/2)
            maxY = round(maxY + dist_left/2)
    else:
        inside = False

    minX, minY = shift(size, minX, minY)

    # print("MaxX: {maxx}, MinX: {minx}, MaxY: {maxy}, MinY: {miny}".format(maxx=maxX, minx=minX, maxy=maxY, miny=minY))

    if (minX < 0 or minX + target_size[0] > size[0]):
        print("No possible box of size 512,512 possible")
        maxX = size[0]
        minX = size[0] - target_size[0]
        if target_size[0] >= size[0]:
            minX = 0
    else:
        maxX = minX + target_size[0]

    if (minY < 0 or minY + target_size[1] > size[1]):
        maxY = size[1]
        minY = size[1] - target_size[1]
        if target_size[1] >= size[1]:
            minY = 0
    else:
        maxY = minY + target_size[1]

    return [inside, (minX, minY, maxX, maxY)]


def shift(size, x, y, target_size=(512, 512)):

    if x < 0:
        x = 0
    if (x + target_size[0]) > size[0]:
        x = size[0] - target_size[0]

    if y < 0:
        y = 0
    if (y + target_size[1]) > size[1]:
        y = size[1] - target_size[1]

    return x, y


def center(size, X, Y, target_size=(512, 512)):
    centerX = X / 2
    centerY = Y / 2

    if (centerX + 256 > size[0]):
        centerX = size[0] - target_size[0]/2
    if (centerX - 256 < 0):
        centerX = size[0] + target_size[0]/2

    if (centerY + 256 > size[1]):
        centerY = size[1] - target_size[1]/2
    if (centerY - 256 < 0):
        centerY = size[1] + target_size[1]/2

    return round(centerX), round(centerY)


def is_green(pixel):
    r, g, b = pixel
    return r == 0 and g == 255 and b == 0

def is_right_color(pixel, r2, g2, b2):
    r1, g1, b1 = pixel
    return r1 == r2 and g1 == g2 and b1 == b2

if __name__ == '__main__':
    image = Image.open('')
    no_alpha_image = image.convert('RGB')
    draw = ImageDraw.Draw(no_alpha_image)
    
    ### Original
    # for region in find_regions(no_alpha_image, [0, 255, 0]):
    #     draw.rectangle(expand_bounding_mk2(no_alpha_image, region), outline=(0, 255, 0))
    # no_alpha_image.show()
    ### END OF ORIGINAL

    ### With new mask region finder
    ori_array = np.asarray(no_alpha_image)
    ori_array = np.array(ori_array / 255.0)
    ori_array = np.expand_dims(ori_array, axis=0)
    mask = get_mask(ori_array, [0.0, 1.0, 0.0])
    regions = region_by_mask(mask)
    for region in regions:
        draw.rectangle(expand_bounding_mk2(no_alpha_image, region), outline=(0, 255, 0))
    no_alpha_image.show()
    ### END OF NEW MASK REGION FINDER

    ### Using big boxes and new region finder
    # width, height = no_alpha_image.size
    # ori_array = np.asarray(no_alpha_image)
    # ori_array = np.array(ori_array / 255.0)
    # ori_array = np.expand_dims(ori_array, axis=0)

    # mask = get_mask(ori_array, [0.0, 1.0, 0.0])

    # regions = region_by_mask(mask)

    # box_bounds = []
    # # Group boxes into a bigger box that has size 512x512
    # for region_counter, region in enumerate(regions, 1):
    #     bounding_box = expand_bounding_mk2(no_alpha_image, region, expand_factor=1.25, min_size=64)

    #     if (len(box_bounds) == 0):
    #         boxCheck = bounding_box_check_mk2((width, height), bounding_box, bounding_box, target_size=(512, 512))
    #         if (boxCheck[0]):
    #             box_bounds.append([boxCheck[1], [bounding_box], [region]])
    #             continue
    #         else:
    #             print("Could not create bounding box for censored area. Aborting.")
    #             break
    #     for i in range(len(box_bounds)):
    #         boxCheck = big_bound_check_mk2((width, height), box_bounds[i][0], bounding_box, box_bounds[i][1], (512, 512))
    #         if (boxCheck[0]):
    #             box_bounds[i][0] = boxCheck[1]
    #             box_bounds[i][1].append(bounding_box)
    #             box_bounds[i][2].append(region)
    #             break
    #         else:
    #             if (i == len(box_bounds) - 1):
    #                 boxCheck = bounding_box_check_mk2((width, height), bounding_box, bounding_box, target_size=(512, 512))
    #                 if (boxCheck[0]):
    #                     box_bounds.append([boxCheck[1], [bounding_box], [region]])
    #                 else:
    #                     print("Could not create bounding box for censored area. Aborting.")
    #                     break

    # for indx, region in enumerate(box_bounds):
    #     # Alternate colors
    #     c = (255 * (0 if (indx) % 3 == 0 else 1), 255 * (0 if (indx + 1) % 3 == 0 else 1), 255 * (0 if (indx + 2) % 3 == 0 else 1))
    #     # print(indx, c)

    #     # Display the big box
    #     draw.rectangle(region[0], outline=c, width=5)

    #     # Display all the boxes that are grouped in the big box, uncomment to show
    #     # for box in region[1]:
    #         # draw.rectangle(expand_bounding_mk2(no_alpha_image, box, expand_factor=1.25), outline=c, width=3)
    # no_alpha_image.show()
    ### END OF BIG BOXES + REGION FINDER
