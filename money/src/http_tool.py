from fastapi import HTTPException, status
import requests


def fetch_data(url, params=None):
    try:
        res = requests.get(url, params=params)
        if res.status_code != status.HTTP_200_OK:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erreur API externe")
        return res.json()
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erreur API externe")
