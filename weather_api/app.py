import sys
import os
from flask import Flask
from flasgger import Swagger

# Adiciona o diretório pai ao sys.path para que o Python possa encontrar o pacote weather_api
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from weather_api import create_app

app = create_app()

swagger = Swagger(app)

if __name__ == '__main__':
    app.run(debug=True)
