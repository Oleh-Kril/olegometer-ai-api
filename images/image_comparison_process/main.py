import time
from io import BytesIO
import skimage.io

from .segmentation import split_image_to_ui_elements
from .finding_pairs import find_pairs
from .analysis import analyze_pairs

def process_images(image1, image2):
    print("Starting process pipeline")
    # Segmentation
    start_time = time.time()

    image_1_np = skimage.io.imread(BytesIO(image1))
    ui_elements_1 = split_image_to_ui_elements(image_1_np, "design")
    print("Split finished for image 1 (design)")

    image_2_np = skimage.io.imread(BytesIO(image2))
    ui_elements_2 = split_image_to_ui_elements(image_2_np, "website")
    print("Split finished for image 2 (website)")

    segmentation_time = time.time() - start_time

    # Find pairs
    print("Starting find_pairs phase")
    start_time = time.time()

    ui_elements_pairs = find_pairs(ui_elements_1, ui_elements_2)
    pairs_found = len([x for x in ui_elements_pairs if x[1] is not None and x[0] is not None])
    pairs_missing = len(ui_elements_pairs) - pairs_found

    finding_pairs_time = time.time() - start_time
    print("Finished find_pairs phase")

    # Analysis
    print("Starting analyze_pairs phase")
    start_time = time.time()

    insights = analyze_pairs(ui_elements_pairs)

    analysis_time = time.time() - start_time
    print("Finished analyze_pairs phase")

    return {
        "designElementsCount": len(ui_elements_1),
        "websiteElementsCount": len(ui_elements_2),
        "pairsFound": pairs_found,
        "pairsMissing": pairs_missing,
        "insights": insights,
        "segmentationTime": segmentation_time,
        "findingPairsTime": finding_pairs_time,
        "analysisTime": analysis_time,
        "totalTime": segmentation_time + finding_pairs_time + analysis_time,
    }