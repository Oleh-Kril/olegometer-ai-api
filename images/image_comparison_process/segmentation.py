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

def split_image_to_ui_elements(image):
    labeled_image, image, edges = edge_segmentation(image)
    # save_groups_in_file(image, labeled_image)
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

    image_wh = rgb2gray(image)

    edges = canny(image_wh)
    # plt.imshow(edges, interpolation='gaussian')
    # plt.title('Canny detector')
    # plt.show()

    dilated_edges = nd.binary_dilation(edges, disk(7))

    # plt.imshow(dilated_edges, interpolation='gaussian')
    # plt.title('Combined edges')
    # plt.show()

    fill_im = nd.binary_fill_holes(dilated_edges)
    # plt.imshow(fill_im)
    # plt.title('Region Filling')
    # plt.show()

    # Label connected components
    labeled_image = label(fill_im, connectivity=2, background=0)

    return labeled_image, image, edges

def save_groups_in_file(image, labeled_image):
    # Create a color map for visualization
    num_labels = np.max(labeled_image)
    print(num_labels)
    colors = plt.cm.jet(np.linspace(0, 1, num_labels + 1))

    # Visualize the labeled regions in different colors
    fig, ax = plt.subplots()
    ax.imshow(image, cmap=plt.cm.gray)

    for region in regionprops(labeled_image):
        # Draw rectangle around segmented region
        minr, minc, maxr, maxc = region.bbox
        print(region.bbox)
        rect = plt.Rectangle((minc, minr), maxc - minc, maxr - minr,
                             fill=False, edgecolor=colors[region.label], linewidth=2)
        ax.add_patch(rect)

    plt.title('Region Filling with Color-Coded Groups')
    plt.savefig("segmented-groups.png", format='png')
    plt.close(fig)

if __name__ == '__main__':
    labeled_image, image, edges = edge_segmentation("amazon.png")
    save_groups_in_file(image, labeled_image)
