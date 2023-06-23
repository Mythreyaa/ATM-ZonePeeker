
def scale_metrics():
    scaledmetric = {"Population Density":10,"Existing Others":-5,"Existing ATM":-5,"Distance Bank":3}
    return scaledmetric


def normalize(locations):
    pop_dens = []
    existing_atms = []
    existing_others = []
    distance_bank = []

    for value in locations.values():
        pop_dens.append(value.pop_dens)
        existing_atms.append(value.existing_atms)
        existing_others.append(value.existing_others)
        distance_bank.append(value.distance_bank)

    minp,maxp = min(pop_dens),max(pop_dens)
    minatm,maxatm = min(existing_atms),max(existing_atms)
    minothers,maxothers = min(existing_others),max(existing_others)
    mindist,maxdist = min(distance_bank),max(distance_bank)

    normalized = {}
   
    for key,val in locations.items():
        normp = (val.pop_dens - minp) / (maxp - minp)
        normartm = (val.existing_atms - minatm) / (maxatm - minatm)
        normothers = (val.existing_others - minothers) / (maxothers - minothers)
        normdist = (val.distance_bank - mindist) / (maxdist - mindist)
        normalized[val] = {"Population Density":normp,"Existing Others":normothers,"Existing ATM":normartm,"Distance Bank":normdist}

    return normalized




