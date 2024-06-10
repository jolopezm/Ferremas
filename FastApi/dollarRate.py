from fastapi import HTTPException
from datetime import datetime, timedelta
import requests

def get_dollar_rate():
    # Obtener la fecha actual en el formato YYYY-MM-DD
    today = datetime.today()
    today_str = today.strftime('%Y-%m-%d')
    
    yesterday = today - timedelta(days=1)
    yesterday_str = yesterday.strftime('%Y-%m-%d')

    tomorrow = today + timedelta(days=1)
    tomorrow_str = tomorrow.strftime('%Y-%m-%d')

    # Credenciales de usuario y código de serie
    user = "joselopezmignone7@gmail.com"
    password = "bCentral**11"
    timeseries = "F073.TCO.PRE.Z.D"  # Código de serie del dólar
    url_2 = 'https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=joselopezmignone7@gmail.com&pass=bCentral**11&function=GetSeries&timeseries=F073.TCO.PRE.Z.D&firstdate=2024-06-08&lastdate=2024-06-08'
    # URL de la API
    url = f"https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user={user}&pass={password}&function=GetSeries&timeseries={timeseries}&firstdate={tomorrow_str}&lastdate={tomorrow_str}"

    try:
        # Realizar la solicitud
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            print("Response JSON:", data)  # Debug print para verificar la estructura de la respuesta
            
            # Obtener los datos de la serie
            series = data.get('Series', [])
            tipo_de_cambio = float(data["Series"]["Obs"][0]["value"])
            return tipo_de_cambio
        else:
            raise HTTPException(status_code=response.status_code, detail="Error from Banco Central API")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))