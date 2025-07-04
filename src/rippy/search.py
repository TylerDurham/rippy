import requests

def find_movies(title: str):
    url = f'https://api.themoviedb.org/3/search/movie?api_key=e348303428642e6ad644b72834e2c56c&query={title}&include_adult=false&language=en-US&page=1'

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer e348303428642e6ad644b72834e2c56c"
    }

    response = requests.get(url, headers=headers)

    data = response.json()
    return sorted(data['results'], key=lambda m: m["popularity"], reverse=True)
