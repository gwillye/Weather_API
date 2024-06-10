from flask import Blueprint, request, jsonify
import requests
from .models import db, WeatherData
from flasgger import swag_from

api = Blueprint('api', __name__)

@api.route('/weather', methods=['POST'])
@swag_from({
    'responses': {
        201: {
            'description': 'Dados meteorológicos coletados com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'city': {'type': 'string'},
                    'lon': {'type': 'number'},
                    'lat': {'type': 'number'},
                    'description': {'type': 'string'},
                    'temp': {'type': 'number'},
                    'feels_like': {'type': 'number'},
                    'temp_min': {'type': 'number'},
                    'temp_max': {'type': 'number'},
                    'pressure': {'type': 'integer'},
                    'humidity': {'type': 'integer'},
                    'visibility': {'type': 'integer'},
                    'wind_speed': {'type': 'number'},
                    'wind_deg': {'type': 'integer'},
                    'clouds_all': {'type': 'integer'},
                    'sunrise': {'type': 'integer'},
                    'sunset': {'type': 'integer'}
                }
            }
        },
        500: {
            'description': 'Erro ao buscar dados da API OpenWeatherMap'
        }
    },
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'city': {'type': 'string'},
                    'lat': {'type': 'number'},
                    'lon': {'type': 'number'}
                }
            }
        }
    ],
    'tags': ['weather']
})
def collect_weather_data():
    data = request.get_json()
    lat = data.get('lat')
    lon = data.get('lon')
    city = data.get('city')
    api_key = "obviamente eu removi minha api key daqui né, não ia upar ela no GitHub"

    if city:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang=pt_br"
    else:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&lang=pt_br"

    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({'error': 'Could not fetch data from OpenWeatherMap API'}), 500

    weather_data = response.json()
    description = weather_data['weather'][0]['main']
    temp = weather_data['main']['temp'] - 273.15
    feels_like = weather_data['main']['feels_like'] - 273.15
    temp_min = weather_data['main']['temp_min'] - 273.15
    temp_max = weather_data['main']['temp_max'] - 273.15
    pressure = weather_data['main']['pressure']
    humidity = weather_data['main']['humidity']
    visibility = weather_data['visibility']
    wind_speed = weather_data['wind']['speed']
    wind_deg = weather_data['wind']['deg']
    clouds_all = weather_data['clouds']['all']
    sunrise = weather_data['sys']['sunrise']
    sunset = weather_data['sys']['sunset']

    weather_entry = WeatherData(
        city=city,
        lon=lon,
        lat=lat,
        description=description,
        temp=temp,
        feels_like=feels_like,
        temp_min=temp_min,
        temp_max=temp_max,
        pressure=pressure,
        humidity=humidity,
        visibility=visibility,
        wind_speed=wind_speed,
        wind_deg=wind_deg,
        clouds_all=clouds_all,
        sunrise=sunrise,
        sunset=sunset
    )
    db.session.add(weather_entry)
    db.session.commit()

    return jsonify(weather_entry.to_dict()), 201

@api.route('/weather', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'Lista de dados meteorológicos',
            'schema': {
                'type': 'object',
                'properties': {
                    'items': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'city': {'type': 'string'},
                                'lon': {'type': 'number'},
                                'lat': {'type': 'number'},
                                'description': {'type': 'string'},
                                'temp': {'type': 'number'},
                                'feels_like': {'type': 'number'},
                                'temp_min': {'type': 'number'},
                                'temp_max': {'type': 'number'},
                                'pressure': {'type': 'integer'},
                                'humidity': {'type': 'integer'},
                                'visibility': {'type': 'integer'},
                                'wind_speed': {'type': 'number'},
                                'wind_deg': {'type': 'integer'},
                                'clouds_all': {'type': 'integer'},
                                'sunrise': {'type': 'integer'},
                                'sunset': {'type': 'integer'}
                            }
                        }
                    },
                    'total': {'type': 'integer'},
                    'pages': {'type': 'integer'},
                    'current_page': {'type': 'integer'}
                }
            }
        }
    },
    'parameters': [
        {
            'name': 'page',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'default': 1
        },
        {
            'name': 'per_page',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'default': 10
        }
    ],
    'tags': ['weather']
})
def list_weather_data():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    weather_entries = WeatherData.query.paginate(page, per_page, error_out=False)

    data = {
        'items': [entry.to_dict() for entry in weather_entries.items],
        'total': weather_entries.total,
        'pages': weather_entries.pages,
        'current_page': weather_entries.page
    }

    return jsonify(data)
