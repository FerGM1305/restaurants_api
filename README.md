# RESTAURANT API
***
This proyect is an API  that will provide useful information about restaurants to users.
It implements CRUD operations
It also implements a endpoint that given the latitud, longitud and a radius in meters shows the Average rating,Standard deviation and the count of the restaurants that are in te radius from the point(lat,lng)

## Important Technologies
***
A list of technologies used within the project:
* [Python](https://www.python.org/): Version 3.12
* [Flask](https://flask.palletsprojects.com/en/3.0.x/): Version 3.0.3

## Deployment
For the deployment I used render, in render you can deploy your web services and also a sqldb
* [render](https://render.com/)


## Usage
***
To try the API You can go to: 
https://restaurants-api-pz1e.onrender.com/restaurants


### Important endpoints
The endpoints are
To see all restaurants: https://restaurants-api-pz1e.onrender.com/restaurants
To find an existing restaurant by id: https://restaurants-api-pz1e.onrender.com/restaurants/id
Example To see the statistics(AVG, STD, COUNT): https://restaurants-api-pz1e.onrender.com/restaurants/statistics?latitude=40.7128&longitude=-74.0060&radius=1000

