from flask import request, jsonify, current_app as app
from .models import db, Restaurant
from sqlalchemy import text
import inspect

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    """
    Obtiene la lista de todos los restaurantes.

    Esta función devuelve una lista de todos los restaurantes disponibles.
    """
    restaurants = Restaurant.query.all()
    return jsonify([restaurant.serialize() for restaurant in restaurants])

@app.route('/restaurants/<id>', methods=['GET'])
def get_restaurant(id):
    """
    Obtiene la informacion de un restaurante.

    Esta función devuelve una lista de un restaurante especifico cuyo ID fue dado en los parametros.
    """
    restaurant = Restaurant.query.get_or_404(id)
    return jsonify(restaurant.serialize())

@app.route('/restaurants', methods=['POST'])
def create_restaurant():
    """
    Crea un nuevo restaurante

    Esta función crea un nuevo restaurante, los datos se pasan en el body.
    Error 500 si no se agrega un rating valido o url valida
    """
    data = request.json
    new_restaurant = Restaurant(**data)
    db.session.add(new_restaurant)
    db.session.commit()
    return jsonify({"message": "Restaurant created successfully!"}), 201

@app.route('/restaurants/<id>', methods=['PUT'])
def update_restaurant(id):
    """
    Actualiza un restaurante existente

    Esta función actualiza el restaurante existente que se indique en el request con el id
    Error 500 si no se agrega un rating valido o url valida
    """
    restaurant = Restaurant.query.get_or_404(id)
    data = request.json
    for key, value in data.items():
        setattr(restaurant, key, value)
    db.session.commit()
    return jsonify({"message": "Restaurant updated successfully!"})

@app.route('/restaurants/<id>', methods=['DELETE'])
def delete_restaurant(id):
    """
    Elimina un restaurante existente

    Esta función elimina el restaurante que se indique en el request con el id
    """
    restaurant = Restaurant.query.get_or_404(id)
    db.session.delete(restaurant)
    db.session.commit()
    return jsonify({"message": "Restaurant deleted successfully!"})




@app.route('/restaurants/statistics', methods=['GET'])
def get_statistics():
    """
    Obtiene estadisticas de los restaurantes

    Esta función obtiene el AVG, Standard Deviation y el Count
    de los restaurantes de que esten dentro de un radio dado en metros
    el punto central es dado por longitud y latitud
    """
    latitude = float(request.args.get('latitude'))
    longitude = float(request.args.get('longitude'))
    radius = float(request.args.get('radius'))
        
    query = text ("""
        WITH punto AS (
            SELECT ST_SetSRID(ST_MakePoint(:longitude,:latitude), 4326) AS punto_interes
        ),
        restaurantes_cercanos AS (
            SELECT *
            FROM restaurant
            WHERE ST_DWithin(
                ST_SetSRID(ST_MakePoint(restaurant.lng, restaurant.lat), 4326),
                (SELECT punto_interes FROM punto), 
                :radius
            )
        )
        , cuenta_restaurantes AS (
            SELECT COUNT(*) AS cantidad_restaurantes
            FROM restaurantes_cercanos
        )
        SELECT 
            AVG(rating) AS avgr,
            STDDEV_POP(rating) AS stdr,
            (SELECT cantidad_restaurantes FROM cuenta_restaurantes) AS countr
        FROM restaurantes_cercanos;
    """
    )
    result = db.session.execute(query, {'latitude': latitude, 'longitude': longitude, 'radius': radius}).fetchone()
        
    return jsonify({"count": result.countr, "avg": result.avgr, "std": result.stdr}), 200

def generate_openapi_spec(app):
    spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "Ejemplo de API con Flask y OpenAPI/Swagger",
            "version": "1.0.0",
            "description": "Especificación de la API generada automáticamente desde Flask."
        },
        "paths": {}
    }
    url_map = app.url_map
    for rule in app.url_map.iter_rules():
        endpoint = app.view_functions[rule.endpoint]
        docstring = inspect.getdoc(endpoint)
        methods = [m for m in rule.methods if m not in ['HEAD', 'OPTIONS']]

        if docstring:
            print(docstring)
            spec["paths"][rule.rule] = {}
            for method in methods:
                spec["paths"][rule.rule][method.lower()] = {
                    "summary": docstring.split("\n")[0],
                    "description": docstring.strip(),
                    "responses": {
                        "200": {"description": "Success"},
                        "404": {"description": "Not Found"}
                    }
                }
    return spec
