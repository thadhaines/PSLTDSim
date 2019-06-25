def findArea(mirror, area):
    """simple finding of area in mirror"""
    # NOTE: can be improved

    areaNum = float(area)
    for cArea in mirror.Area:
        if cArea.Area == areaNum:
            return cArea

    print("*** Area %s Not Found")
    return None