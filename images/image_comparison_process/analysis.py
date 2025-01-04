MAX_OK_DIFFERENCE = 0.1

def bbox_diff(bbox1, bbox2, threshold=MAX_OK_DIFFERENCE):
    width1, height1 = bbox1[2] - bbox1[0], bbox1[3] - bbox1[1]
    width2, height2 = bbox2[2] - bbox2[0], bbox2[3] - bbox2[1]
    absolute_width_diff = abs(width1 - width2)
    absolute_height_diff = abs(height1 - height2)

    width_diff = absolute_width_diff / width1
    height_diff = absolute_height_diff / height1

    width_diff_sign = "+" if width2 > width1 else "-"
    height_diff_sign = "+" if height2 > height1 else "-"

    if width_diff > threshold or height_diff > threshold:
        return absolute_width_diff, absolute_height_diff, width_diff, height_diff, width_diff_sign, height_diff_sign
    return None

def analyze_pairs(ui_elements_pairs):
    pairs_found = [x for x in ui_elements_pairs if x[1] is not None and x[0] is not None]
    pairs_missing_on_2 = [x for x in ui_elements_pairs if x[0] is not None and x[1] is None]
    pairs_missing_on_1 = [x for x in ui_elements_pairs if x[0] is None and x[1] is not None]

    insights = {}

    for pair in pairs_found:
        bbox1 = pair[0][1]
        bbox2 = pair[1][1]
        diff = bbox_diff(bbox1, bbox2)
        if diff is not None:
            bbox2_key = f"{bbox2}-website"
            if bbox2_key not in insights:
                insights[bbox2_key] = []
            insights[bbox2_key].append({
                "message": f'Bounding box differs from design by more than {int(MAX_OK_DIFFERENCE*100)}%',
                "type": "size",
                "width_diff_sign": diff[4],
                "height_diff_sign": diff[5],
                "absoluteDiffWidth": diff[0],
                "absoluteDiffHeight": diff[1],
                "diffWidthInPercents": round(diff[2] * 100, 1),
                "diffHeightInPercents": round(diff[3] * 100, 1),
            })

    for pair in pairs_missing_on_2:
        bbox1 = pair[0][1]
        bbox1_key = f"{bbox1}-design"
        if bbox1_key not in insights:
            insights[bbox1_key] = []
        insights[bbox1_key].append({
            "message": 'Element is missing in the implementation',
            "type": "missing"
        })

    for pair in pairs_missing_on_1:
        bbox2 = pair[1][1]
        bbox2_key = f"{bbox2}-website"
        if bbox2_key not in insights:
            insights[bbox2_key] = []
        insights[bbox2_key].append({
            "message": 'Element is missing in the design mockups',
            "type": "missing"
        })

    return insights