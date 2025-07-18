

def estimate_weight_from_pixels(length_px, px_per_cm=25):
    """
    Estimate fish length in centimeters and weight in grams from pixel length.

    Args:
        length_px (float): Length of the fish in pixels (from image).
        px_per_cm (float): Calibration value, number of pixels per centimeter.
            This should be determined for your camera setup using a reference object of known length.

    Returns:
        tuple: (length_cm, weight) where length_cm is the fish length in centimeters,
               and weight is the estimated fish weight in grams.
    """
    # Calibration: px_per_cm converts pixel measurements to centimeters
    length_cm = length_px / px_per_cm
    weight = 0.0196 * (length_cm ** 2.9868)
    return round(weight, 2)
