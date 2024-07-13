from skimage.transform import resize
from .similarity import get_similarity
import copy

MAX_PAIR_DIMENSIONS_DIFFERENCE = 2

def resize_and_check_ratio(image1, image2):
    height1, width1 = image1.shape[:2]
    height2, width2 = image2.shape[:2]

    if width1 > width2:
        ratio = width1 / width2
    else:
        ratio = width2 / width1

    if ratio > MAX_PAIR_DIMENSIONS_DIFFERENCE:
        return None, None

    if height1 > height2:
        ratio = max(ratio, height1 / height2)
    else:
        ratio = max(ratio, height2 / height1)

    if ratio > MAX_PAIR_DIMENSIONS_DIFFERENCE:
        return None, None

    # Resize the images
    max_height = max(height1, height2, 100)
    max_width = max(width1, width2, 100)

    image1 = resize(image1, (max_height, max_width), mode='constant', anti_aliasing=True)
    image2 = resize(image2, (max_height, max_width), mode='constant', anti_aliasing=True)

    return image1, image2

def find_pairs(ui_elements_1, ui_elements_2):
    i = 0
    pairs = []
    ui_elements_2_copy = copy.deepcopy(ui_elements_2)
    for image1, bbox1 in ui_elements_1:
        j = 0
        index_to_remove = None
        max_similarity = float('-inf')
        max_similarity_pair = ((image1, bbox1), None)

        for image2, bbox2 in ui_elements_2_copy:
            image1_r, image2_r = resize_and_check_ratio(image1, image2)
            if image1_r is None or image2_r is None:
                continue

            similarity_score = get_similarity(image1_r, image2_r)

            if similarity_score > max_similarity:
                max_similarity = similarity_score
                max_similarity_pair = ((image1, bbox1), (image2, bbox2))
                index_to_remove = j
            j += 1

        pairs.append(max_similarity_pair)
        if index_to_remove is not None:
            del ui_elements_2_copy[index_to_remove]
        i += 1

    if len(ui_elements_2_copy) > 0:
        pairs.extend([(None, (image, bbox)) for (image, bbox) in ui_elements_2_copy])

    return pairs