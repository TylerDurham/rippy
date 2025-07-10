import requests

def search_movies(title: str, api_key: str, max_records: int = 5):
    url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={title}&include_adult=false&language=en-US&page=1'

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    response = requests.get(url, headers=headers)

    data = response.json()
    return sorted(data['results'], key=lambda m: m["popularity"], reverse=True)[0:max_records]

def get_movie(id: str, api_key: str):

    url = f"https://api.themoviedb.org/3/movie/{id}?api_key={api_key}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    response = requests.get(url, headers=headers)

    return response.json()


    
