from fastapi import HTTPException
import requests


def fetch_data(url, params=None):
    try:
        res = requests.get(url, params=params)
        if res.status_code != 200:
            raise HTTPException(status_code=500, detail="Erreur API externe")
        return res.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur API externe")
