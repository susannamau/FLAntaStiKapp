from app import create_app
import json

with open('/Users/susannamau/Dev/BPER/Python/webapp/config.json', 'r') as config_file:
    config = json.load(config_file)

app = create_app()

if __name__ == '__main__':
    app.secret_key = config["SECRET_KEY"]
    app.run(use_reloader=True)