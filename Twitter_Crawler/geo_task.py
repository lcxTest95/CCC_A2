import shapefile
from shapely.geometry import Polygon, Point

## Set the SA4 coordinates polygon
"""
    This SA2 file contains both SA4 and SA2 location. 
    Some Tweets only have user profile location, and the name is match with SA2 name. 
    Therefore, for this kind of situation, we match it with SA2 first, then match it with SA4.
 
 """
sf = shapefile.Reader("sa2_2016_aust_shape/SA2_2016_AUST")
records = sf.records()
shapes = sf.shapes()

polygons_list = []
for ind, shape in enumerate(shapes):
    polys = Polygon(shape.points)
    polygons_list.append(polys)

SA2_list = []
for ind, rec in enumerate(records):
    info = rec.as_dict()
    info['polygon'] = polygons_list[ind]
    SA2_list.append(info)

SA2_name = []
for i in SA2_list:
    SA2_name.append(i['SA2_NAME16'])

SA2_name_lower = []
for i in SA2_name:
    i = i.lower()
    SA2_name_lower.append(i)

# Add SA4_code, SA4_NAME, STATE_CODE, STATE_Name to the original tweets.
def addKey(tweet_data, area, flag):
    if flag:
        tweet_data['SA4_CODE'] = area['SA4_CODE16']
        tweet_data['SA4_NAME'] = area['SA4_NAME16']
        tweet_data['STATE_CODE'] = area['STE_CODE16']
        tweet_data['STATE_NAME'] = area['STE_NAME16']
    else:
        tweet_data['SA4_CODE'] = "no_values"
        tweet_data['SA4_NAME'] = "no_values"
        tweet_data['STATE_CODE'] = "no_values"
        tweet_data['STATE_NAME'] = "no_values"
    return tweet_data


def geo_processing(tweet_data):
    flag = True
    if tweet_data['geo'] != None: ## First, check if there is location information in 'geo'.
        point = Point(tweet_data['geo']['coordinates'][1], tweet_data['geo']['coordinates'][0])
        for area in SA2_list:
            if point.within(area['polygon']):
                addKey(tweet_data,area,flag)
                break
        else:
            flag = False
            addKey(tweet_data, None, flag)
    elif tweet_data['place'] != None: ##Second, check if there is location in 'place'.
        box = tweet_data['place']['bounding_box']['coordinates'][0]
        ctr = Polygon(box).centroid
        for area in SA2_list:
            if ctr.within(area['polygon']):
                addKey(tweet_data,area,flag)
                break
        else:
            flag = False
            addKey(tweet_data, None, flag)
    elif tweet_data['user']['location'] != '': ## Third, check if there is location in user profile.
        try:
            loc = tweet_data['user']['location'].split()[0].rstrip(',').lower()
            for i, name in enumerate(SA2_name_lower):
                if loc in name:
                    addKey(tweet_data, SA2_list[i], flag)
                    break
            else:
                flag = False
                addKey(tweet_data, None, flag)
        except IndexError as I:
            flag = False
            addKey(tweet_data, None, flag)
    elif tweet_data['user']['location'] == '': ## Fourth, check if there is location in original user profile if this is retweeted.
        try:
            loc = tweet_data['retweeted_status']['user']['location'].split()[0].rstrip(',').lower()
            for i, name in enumerate(SA2_name_lower):
                if loc in name:
                    addKey(tweet_data, SA2_list[i], flag)
                    break
            else:
                flag = False
                addKey(tweet_data, None, flag)
        except IndexError as I:
            flag = False
            addKey(tweet_data, None, flag)
        except KeyError as K:
            flag = False
            addKey(tweet_data,None,flag)
    return tweet_data
