import random

from django.http import HttpRequest
from django.shortcuts import render
import requests
import datetime
import re
import os
import environ
from weatherapp.forms import CityForm


env = environ.Env()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

def home(request: HttpRequest):
    if request.POST:
        form = CityForm(request.POST)
        if form.is_valid():
            s = form.cleaned_data['city'].title()
            city = re.sub(r'[^\w]', ' ', s).strip()
    else:
        form = CityForm()
        city = "Almaty"

    # API settings
    key = env('key')
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}'
    PARAMS = {'units': 'metric'}
    API_KEY = env('API_KEY')
    SEARCH_ENGINE_ID = env('SEARCH_ENGINE_ID')

    try:
        response = requests.get(url, PARAMS)
        data = response.json()

        if response.status_code != 200 or data.get('cod') != 200:
            raise ValueError("City not found!")

        # Getting info from API
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = round(data['main']['temp'], 1)
        day = datetime.date.today()

        # Getting city photo from API
        query = city + f" фото города"
        page = 1
        start = (page - 1) * 10 + 1
        search_type = 'image'
        city_url = f'https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={search_type}&imgSize=xlarge'

        data = requests.get(city_url).json()
        search_items = data.get("items")
        n = random.randint(1, 5)
        image_url = search_items[n]['link']

        context = {
            'form': form,
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'image_url': image_url,
        }

    except Exception as e:
        error = str(e).title()
        context = {
            'form': form,
            'error': error,
            'icon': "04d",
            'temp': "?",
            'day': datetime.date.today(),
        }
    return render(request, "weatherapp/index.html", context)
