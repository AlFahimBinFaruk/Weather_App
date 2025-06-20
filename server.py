from flask import Flask, render_template, request
import os
from src.weather_fetcher import fetch_weather, save_local
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    error = None
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            try:
                data = fetch_weather(city)
                save_local(city, data)
                weather = {
                    'city': city,
                    'temp': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    # Extend as needed
                }
            except Exception as e:
                error = f"Error fetching data for {city}: {e}"
    return render_template('index.html', weather=weather, error=error)

if __name__ == '__main__':
    app.run(debug=True)
