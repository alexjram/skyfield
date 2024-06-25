from typing import Optional
from skyfield.api import Star, load
from skyfield.data import hipparcos
from skyfield.named_stars import named_star_dict

with load.open(hipparcos.URL) as f:
    dfg = hipparcos.load_dataframe(f)

barnards_star = Star.from_dataframe(dfg.loc[87937])
planets = load('de421.bsp')
earth = planets['earth']

hip_to_name = {v: k for k, v in named_star_dict.items()}

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
        response.append({
            "name": df['name'].__array__()[i],
            "right_ascension": ra.hours[i],
            "declination": dec.degrees[i],
            "distance": distance.au[i],
            "magnitude": df['magnitude'].__array__()[i]
        })


    return response