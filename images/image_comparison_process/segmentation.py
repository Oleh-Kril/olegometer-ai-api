import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from skimage.feature import canny
from skimage.color import rgb2gray
import scipy.ndimage as nd
from skimage.measure import regionprops, label
from skimage.morphology import disk
plt.rcParams["figure.figsize"] = (12, 8)

EDGE_DETECTION_SIGMA = 2.0
DILATION_DISK_SIZE = 4
STANDART_WIDTH = 1600
LABEL_CONNECTIVITY = 2

def split_image_to_ui_elements(image, image_id):
    labeled_image, image, edges = edge_segmentation(image)
    save_groups_in_file(image, labeled_image, image_id)
    regions = regionprops(labeled_image)
    ui_elements = []
    for i, region in enumerate(regions):
        bbox = region.bbox
        ui_element = image[bbox[0]:bbox[2], bbox[1]:bbox[3], :]
        ui_elements.append((ui_element, bbox))
    return ui_elements

def edge_segmentation(image):
    # plt.imshow(image)
    # plt.title('image without alpha channel')
    # plt.show()

    # Check if it has an alpha channel
    if image.shape[-1] == 4:
        image = image[..., :3]

    image_wh = rgb2gray(image)

    edges = canny(image_wh, sigma=EDGE_DETECTION_SIGMA)
    # plt.imshow(edges, interpolation='gaussian')
    # plt.title('Canny detector')
    # plt.show()

    disk_size = get_dilation_disk_size(image_wh)
    print(image_wh.shape, disk_size)
    dilated_edges = nd.binary_dilation(edges, disk(DILATION_DISK_SIZE))

    # plt.imshow(dilated_edges, interpolation='gaussian')
    # plt.title('Combined edges')
    # plt.show()

    fill_im = nd.binary_fill_holes(dilated_edges)
    # plt.imshow(fill_im)
    # plt.title('Region Filling')
    # plt.show()

    # Label connected components
    labeled_image = label(fill_im, connectivity=LABEL_CONNECTIVITY, background=calculate_background_value(image_wh))

    return labeled_image, image, edges

def save_groups_in_file(image, labeled_image, image_id):
    # Create a color map for visualization
    num_labels = np.max(labeled_image)
    print("Number of labels for " + image_id + " is", num_labels)
    colors = plt.cm.jet(np.linspace(0, 1, num_labels + 1))

    # Visualize the labeled regions in different colors
    fig, ax = plt.subplots()
    ax.imshow(image, cmap=plt.cm.gray)

    for region in regionprops(labeled_image):
        # Draw rectangle around segmented region
        minr, minc, maxr, maxc = region.bbox
        # print(region.bbox)
        rect = plt.Rectangle((minc, minr), maxc - minc, maxr - minr,
                             fill=False, edgecolor=colors[region.label], linewidth=2)
        ax.add_patch(rect)

    plt.savefig(f"segmented-groups-{image_id}.png", format='png')
    plt.close(fig)
def calculate_background_value(image_gray):
    flat_image = image_gray.flatten()

    hist, bin_edges = np.histogram(flat_image, bins=256, range=(0, 1))

    # Find the bin with the maximum count, assuming the background is the most common value
    background_value = bin_edges[np.argmax(hist)]

    return background_value

def get_dilation_disk_size(image, default_disk_size=DILATION_DISK_SIZE, reference_width=STANDART_WIDTH):
    image_width = image.shape[1]
    adjusted_disk_size = int(default_disk_size * (image_width / reference_width))
    return adjusted_disk_size

if __name__ == '__main__':
    labeled_image, image, edges = edge_segmentation("amazon.png")
    save_groups_in_file(image, labeled_image)
