from math import radians,cos,sin,asin,sqrt

def calculate_distance_km(lat1,lon1,lat2,lon2):
    """
    Haversine formula to calculate distance between two coordinates
    """
    lat1,lon1,lat2,lon2=map(radians,[lat1,lon1,lat2,lon2])

    dlat=lat2-lat1
    dlon=lon2-lon1

    a=sin(dlat/2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon/2) ** 2
    c=2*asin(sqrt(a))

    return round(6371 * c, 2)