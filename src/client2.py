import requests

BASE = "http://127.0.0.1:8000/movies"

def get_all():
    r = requests.get(BASE)
    print("GET ALL:", r.json())

def get_one(movie_id):
    r = requests.get(f"{BASE}/{movie_id}")
    print("GET ONE:", r.json())

def add_movie(name, year):
    data = {
        "name": name,
        "year": year
    }
    r = requests.post(BASE, json=data)
    print("POST:", r.json())

def update_movie(movie_id, name, year):
    data = {
        "name": name
        "year": year
     }

        
       
    
    r = requests.put(f"{BASE}/{movie_id},", json=data)
    print("PUT": r.json())

def delete_movie(movie_id):
    r = requests.delete(f"{BASE}/{movie_id}")
    print("DELETE", r.json())

add_movie("redded", 2010)
add_movie("fight club", 2014)

#get_all()

#get_one(1)
#update_movie(1, "Batman", 2005)
#get_all()

#delete_movie(2)
#get_all()
   

                           