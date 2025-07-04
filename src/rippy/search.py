import requests

API_KEY = ""

def find_movies(title: str):
    url = f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}&include_adult=false&language=en-US&page=1'

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    response = requests.get(url, headers=headers)

    data = response.json()
    return sorted(data['results'], key=lambda m: m["popularity"], reverse=True)
