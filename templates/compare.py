from geopy.geocoders import Nominatim
from templates.condition import *
from templates.normalize import *
import random

class Location: 
    def __init__(self,add,thresh_pop_dens,radius,bank_loc):
        #self.name = name
        self.add = add
        self.thresh_pop_dens = int(thresh_pop_dens)
        self.radius = radius
        print("1....")
        geolocator = Nominatim(user_agent="atm_locator")
        print("2....")
        location = geolocator.geocode(self.add)
        print("3....")
        if location is None:
            print("Invalid address.")
            return None
        latitude = location.latitude
        longitude = location.longitude
        print(latitude,longitude)
        
        self.existing_atms = check_existing_atms(latitude,longitude,self.radius)
        self.existing_others = check_others(self.add,self.radius)
        self.distance_bank = calculate_distance(self.add,bank_loc)
        self.pop_dens = random.randint(0,self.thresh_pop_dens)
        print("POPULATION DENSITY: ",self.pop_dens)
        self.pop_dens = check_population_density(self.pop_dens,self.thresh_pop_dens)

class Priority:
    def __init__(self,map,name,locations):
        print("Priority class")
        self.map = map
        self.name = name
        self.norm_table = normalize(locations)
        print(self.norm_table)

    def compute(self,scale,normval):
        return scale * normval

    def prioritize(self):

        colors = [("RED","LOW"),("BLUE","AVERAGE"),("GREEN","HIGH")]
        score_board = []

        for loc,data in self.norm_table.items():
            score = 0
            for metrics,val in data.items():
                score += self.compute(scale_metrics()[metrics],val)
            score_board.append((loc,score))
        score_board = sorted(score_board,key=lambda x:x[1])
        self.size = len(score_board)

        pri_list = []
        while self.size != 0:
            pri_list.append((score_board[self.size-1][0].add,colors[self.size-1]))
            self.size -= 1

        print("------------>",pri_list)
        return pri_list

def find_loc(bankname,bank_location,location1,location2,location3,pop_dens,radius):
    locations = {}
    neighbours = {}
    map = {bankname:[]}
    
    locations[location1] = Location(location1,pop_dens,radius,bank_location)
    neighbours[locations[location1]] = "RED"
    
    locations[location2] = Location(location2,pop_dens,radius,bank_location)
    neighbours[locations[location2]] = "RED"
    
    locations[location3] = Location(location3,pop_dens,radius,bank_location)
    neighbours[locations[location3]] = "RED"
        

    map[bankname] = neighbours


    p = Priority(map,bankname,locations)
    return p.prioritize()   




    
    
        





if __name__ == "__main__":
    name = input("Enter Bank Name: ")
    bank_location = input("Enter Bank Location: ")
    pop_dens = input("Enter Population Density: ")
    radius = input("Enter Radius: ")
    locations = {}
    neighbours = {}
    map = {name:[]}
    for i in range(3):
        loc = (input("Enter Location: "))
        locations[loc] = Location(loc,pop_dens,radius,bank_location)
        neighbours[locations[loc]] = "RED"

    map[name] = neighbours


    p = Priority(map,name,locations)
    p.prioritize()


