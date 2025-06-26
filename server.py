from flask import Flask, render_template, request
import os,logging
from src.weather_fetcher import fetch_weather, save_to_db
from dotenv import load_dotenv
from models.weatherHistory import db

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
DB_URL=os.getenv("DATABASE_URL")
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)



@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    error = None
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            try:
                data = fetch_weather(city)
                save_to_db(city, data)
                weather = {
                    'city': city,
                    'temp': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                }
            except Exception as e:
                error = f"Error fetching data for {city}: {e}"
    return render_template('index.html', weather=weather, error=error)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,host="0.0.0.0",port=5000)
