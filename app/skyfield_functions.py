from typing import Optional
from skyfield.api import Star, load,  load_constellation_names
from skyfield.data import hipparcos, stellarium
from skyfield.named_stars import named_star_dict
import pandas as pd

with load.open(hipparcos.URL) as f:
    hipparcos.load_dataframe(f)
    dfg = hipparcos.load_dataframe(f)

barnards_star = Star.from_dataframe(dfg.loc[87937])
planets = load('de421.bsp')
earth = planets['earth']

hip_to_name = {v: k for k, v in named_star_dict.items()}

def add_color_index() -> None:
    hipparcos_df = pd.read_csv('hip_main.dat', sep='|', header=None, usecols=[37], names=['color_index'])
    dfg['color_index'] = hipparcos_df['color_index']
    
add_color_index()

def  get_star_name(hip):
    return hip_to_name.get(hip, f"HIP{hip}")

dfg["name"] = dfg.index.map(get_star_name)

def get_stars_by_magnitude(max_magnitude: Optional[float], min_magnitude: Optional[float]) -> list:

    df = dfg[(dfg['magnitude'] <= max_magnitude) & (dfg['magnitude'] >= min_magnitude)]
    stars = Star.from_dataframe(df)
    ts = load.timescale()
    t = ts.now()
    astrometric = earth.at(t).observe(stars)

    ra, dec, distance = astrometric.radec()
    response = []
    for i in range(len(df)): 
        try:
            
            color_index = float(df['color_index'].__array__()[i])
        except Exception as e:
            print(e)
            color_index = 0
        response.append({
            "name": df['name'].__array__()[i],
            "right_ascension": ra.hours[i],
            "declination": dec.degrees[i],
            "distance": distance.au[i],
            "magnitude": df['magnitude'].__array__()[i],
            "color": get_color(color_index),
            "color_index": color_index
        })


    return response

def get_star(index: int) -> dict:
    try:
        star = dfg.iloc[index]
        starObject = Star.from_dataframe(star)
        t = load.timescale().now()
        astrometric = earth.at(t).observe(starObject)
        ra, dec, distance = astrometric.radec()
        print(ra.hours)
        print(star['ra_hours'].item())
        return {
            "name": star['name'],
            "right_ascension": ra.hours,
            "declination": dec.degrees,
            "magnitude": star['magnitude'].item(),
            "color_index": float(star['color_index']),
            "color": get_color(float(star['color_index']))
        }
    except Exception as e:
        print(e)
        print(f"index {index} not found")
        return {}

def get_constellations() -> list:

    url = ('https://raw.githubusercontent.com/Stellarium/stellarium/master'
       '/skycultures/modern_st/constellationship.fab')
    with load.open(url) as f:
        constellations = stellarium.parse_constellations(f)
        
    d = dict(load_constellation_names())
        
    constellation_list = []
    for constellation in constellations:
        edges = []
        for edge in constellation[1]:
            edges.append([
                get_star(edge[0]),
                get_star(edge[1])
            ])
        constellation_list.append({
            "name": d[constellation[0]],
            "edges": edges
        })
    
    return constellation_list


def get_color(color_index: float) -> str:
    if color_index <= -0.33:
        return '#94B6FF'
    if color_index <= -0.30:
        return '#99B9FF'
    if color_index <= -0.02:
        return '#C9D9FF'
    if color_index <= 0.30:
        return '#ECEEFF'
    if color_index <= 0.58:
        return '#FFF2EE'
    if color_index <= 0.81:
        return '#FFE7D2'
    else:
        return '#FFCC98'
    