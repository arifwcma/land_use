from report_land_use import report

local_areas = [
    "West Wimmera",
    "Hindmarsh",
    "Yarriambiack and Buloke",
    "Horsham",
    "Upper Catchment"
]

def report_by_type(map, report_type):
    for area in local_areas:
        report(map, area, report_type)