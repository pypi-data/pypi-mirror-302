def process_azimuth(azimuth_angle):
    if isinstance(azimuth_angle, str):
        azimuth_angle = {
            'N' : 0,
            'E': 90,
            'S' : 180,
            'W': 270
        }[azimuth_angle]
    return azimuth_angle