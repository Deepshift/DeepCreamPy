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
def region_by_mask(mask):
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

# Expand the box surrounding the region area.
def expand_bounding_mk2(img, region, expand_factor=1.50, min_size=256, max_size=512):
    # expand bounding box to capture more context
    if not isinstance(region, set) and len(region) == 4:
        min_x, min_y, max_x, max_y = region[0], region[1], region[2], region[3]
    else:
        x, y = zip(*region)
        min_x, min_y, max_x, max_y = min(x), min(y), max(x), max(y)

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

    # If the box is out of bounds, return to the original coordinates
    if x2_square > width or y2_square > height:
        print("bounding box out of bounds!")
        print(x1_square, y1_square, x2_square, y2_square)
        x1_square, y1_square, x2_square, y2_square = min_x, min_y, max_x, max_y
    return int(x1_square), int(y1_square), int(x2_square), int(y2_square)

# Creates a new big box around the specified box. 
# Size is the size of the picture, and not the box, which is meant to limit the coordinates of the box
# as to not go outside of the picture.
# Index 0 of the return array is a boolean mentioning if the box is too big to fit in the picture (False if too big).
def bounding_box_check_mk2(size, box, target_size=(512, 512)):
    inside = True
    # Get the boundaries of the box
    minX = min(box[0], box[2])
    maxX = max(box[0], box[2])
    minY = min(box[1], box[3])
    maxY = max(box[1], box[3])

    # If the box has a width less than or equal to the target size (512, 512)
    # a bigger box is created, centered around it
    b_width = maxX - minX
    if b_width <= target_size[0]:
        dist_left = target_size[0] - b_width
        if dist_left != 0:
            minX = round(minX - dist_left/2)
            maxX = round(maxX + dist_left/2)
    else:
        print('Censor region is too big')
        inside = False

    b_height = maxY - minY
    if b_height <= target_size[1]:
        dist_left = target_size[1] - b_height
        if dist_left != 0:
            minY = round(minY - dist_left/2)
            maxY = round(maxY + dist_left/2)
    else:
        print('Censor region is too big')
        inside = False

    # This shifts the box so that it does not go outside of the picture
    minX, minY = shift(size, minX, minY)

    # Shrink/move the box horizontally if it is bigger than the picture
    if (minX < 0 or minX + target_size[0] > size[0]):
        print("No possible box of size 512,512 possible")
        maxX = size[0]
    else:
        maxX = minX + target_size[0]

    minX = max(0, minX)

    # Shrink/move the box vertically if it is bigger than the picture
    if (minY < 0 or minY + target_size[1] > size[1]):
        maxY = size[1]
    else:
        maxY = minY + target_size[1]

    minY = max(0, minY)

    return [inside, (minX, minY, maxX, maxY)]

# Check if box1 fits into big_box by checking if it is within range of all other boxes.
# Size is the size of the picture and not the size of the box.
def big_bound_check_mk2(size, big_box, box1, boxes, target_size=(512, 512)):
    inside = True

    # Initialize maxX,maxY,minX,minY
    maxX = max(box1[0], box1[2])
    maxY = max(box1[1], box1[3])

    minX = min(box1[0], box1[2])
    minY = min(box1[1], box1[3])

    # Check all the boxes for the correct min/max values
    for box in boxes:
        maxX = max(maxX, box[0], box[2])
        maxY = max(maxY, box[1], box[3])

        minX = min(minX, box[0], box[2])
        minY = min(minY, box[1], box[3])

    # Get the total width of the new big box
    b_width = maxX - minX

    # If the new big box has a width less than or equal to the target size (512, 512)
    # the new box fits into the group, and the big box can be moved accordingly
    if b_width <= target_size[0]:
        dist_left = target_size[0] - b_width
        if dist_left != 0:
            minX = round(minX - dist_left/2)
            maxX = round(maxX + dist_left/2)
    else:
        inside = False

    # Same deal for the height as for the width above
    b_height = maxY - minY
    if b_height <= target_size[1]:
        dist_left = target_size[1] - b_height
        if dist_left != 0:
            minY = round(minY - dist_left/2)
            maxY = round(maxY + dist_left/2)
    else:
        inside = False

    # Shift the box if it's close to the edge
    minX, minY = shift(size, minX, minY)

    # print("MaxX: {maxx}, MinX: {minx}, MaxY: {maxy}, MinY: {miny}".format(maxx=maxX, minx=minX, maxy=maxY, miny=minY))

    # Shrink/move the box horizontally if it is bigger than the picture
    if (minX < 0 or minX + target_size[0] > size[0]):
        print("No possible box of size 512,512 possible")
        maxX = size[0]
        minX = size[0] - target_size[0]
        if target_size[0] >= size[0]:
            minX = 0
    else:
        maxX = minX + target_size[0]

    # Shrink/move the box vertically if it is bigger than the picture
    if (minY < 0 or minY + target_size[1] > size[1]):
        maxY = size[1]
        minY = size[1] - target_size[1]
        if target_size[1] >= size[1]:
            minY = 0
    else:
        maxY = minY + target_size[1]

    return [inside, (minX, minY, maxX, maxY)]

# Shifts the x and y if it's too close to the edge for target_size not to be applicable
# Does not reshape the box if the target_size is greater than size of the picture
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

# Draws boxes around the found censor regions.
if __name__ == '__main__':
    image = Image.open(r'')
    no_alpha_image = image.convert('RGB')
    draw = ImageDraw.Draw(no_alpha_image)
    
    ### Original
    # for region in find_regions(no_alpha_image, [0, 255, 0]):
    #     draw.rectangle(expand_bounding_mk2(no_alpha_image, region), outline=(0, 255, 0))
    # no_alpha_image.show()
    ### END OF ORIGINAL

    ### With new mask region finder
    # ori_array = np.asarray(no_alpha_image)
    # ori_array = np.array(ori_array / 255.0)
    # ori_array = np.expand_dims(ori_array, axis=0)
    # mask = get_mask(ori_array, [0.0, 1.0, 0.0])
    # regions = region_by_mask(mask)
    # for region in regions:
    #     draw.rectangle(expand_bounding_mk2(no_alpha_image, region), outline=(0, 255, 0))
    # no_alpha_image.show()
    ### END OF NEW MASK REGION FINDER

    ### Using big boxes and new region finder
    width, height = no_alpha_image.size
    ori_array = np.asarray(no_alpha_image)
    ori_array = np.array(ori_array / 255.0)
    ori_array = np.expand_dims(ori_array, axis=0)

    mask = get_mask(ori_array, [0.0, 1.0, 0.0])

    # Find all the masked regions
    regions = region_by_mask(mask)

    box_bounds = []
    # Group boxes into a bigger box that has size target_size (default: 512x512)
    for region_counter, region in enumerate(regions, 1):
        bounding_box = expand_bounding_mk2(no_alpha_image, region, expand_factor=1.25, min_size=64)

        if (len(box_bounds) == 0):
            boxCheck = bounding_box_check_mk2((width, height), bounding_box, target_size=(512, 512))
            if (boxCheck[0]):
                box_bounds.append([boxCheck[1], [bounding_box], [region]])
            else:
                print("Censor region exceeds boundary: {}".format(bounding_box))
            continue    
        for i in range(len(box_bounds)):
            boxCheck = big_bound_check_mk2((width, height), box_bounds[i][0], bounding_box, box_bounds[i][1], (512, 512))
            if (boxCheck[0]):
                box_bounds[i][0] = boxCheck[1]
                box_bounds[i][1].append(bounding_box)
                box_bounds[i][2].append(region)
                break
            else:
                if (i == len(box_bounds) - 1):
                    boxCheck = bounding_box_check_mk2((width, height), bounding_box, target_size=(512, 512))
                    if (boxCheck[0]):
                        box_bounds.append([boxCheck[1], [bounding_box], [region]])
                    else:
                        print("Censor region exceeds boundary: {}".format(bounding_box))

    # Iterate over the big boxes and draw them to the picture
    for indx, region in enumerate(box_bounds):
        # Alternate colors
        c = (255 * (0 if (indx) % 3 == 0 else 1), 255 * (0 if (indx + 1) % 3 == 0 else 1), 255 * (0 if (indx + 2) % 3 == 0 else 1))
        # print(indx, c)

        # Display the big box
        draw.rectangle(region[0], outline=c, width=5)

        # Display all the boxes that are grouped in the big box, uncomment to show
        for box in region[1]:
            draw.rectangle(expand_bounding_mk2(no_alpha_image, box, expand_factor=1.25), outline=c, width=3)
    no_alpha_image.show()
    ### END OF BIG BOXES + REGION FINDER
