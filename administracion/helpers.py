import requests
import json
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from usuarios.models import MUNICIPIOS


class Coordenadas:
    def __init__(self, latitud, longitud):
        self.latitud = latitud
        self.longitud = longitud

def enviar_correo_respuesta_solicitud_ingreso(subject, message, remitentes, respuesta, usuario, sitio):
    template = get_template("correo_solicitud_ingreso.html")
    contenido = template.render({"usuario":usuario, "respuesta": respuesta, "sitio": sitio})
    correo = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=remitentes)
    correo.attach_alternative(contenido, "text/html")
    try:
        correo.send()
        return True
    except Exception:
        return False

def obtener_coordenadas(cleaned_data):
    return Coordenadas(0.0, 0.0)
    # codigo_postal = cleaned_data['codigo_postal']
    # municipio = MUNICIPIOS[cleaned_data['municipio']][1]
    # # colonia = cleaned_data['colonia']
    # calle = cleaned_data['calle']
    # numero_exterior = cleaned_data['numero_exterior']

    # headers = {
    #     'User-agent': 'Script de consulta de ubicacion'
    # }
    # payload = {
    #     "street": f"{numero_exterior} {calle}",
    #     "city": municipio,
    #     "country": "Mexico",
    #     "state": "Zacatecas",
    #     "postalcode": codigo_postal,
    #     # "county": colonia,
    #     "format": "json"
    # }
    # r = requests.get(
    #     "https://nominatim.openstreetmap.org/search",
    #     params=payload,
    #     headers=headers)

    # if r.status_code != 200:
    #     return None

    # data = json.loads(r.text)

    # if len(data) == 0:
    #     return None

    # data = data[0]

    # if "lat" not in data or "lon" not in data:
    #     return None

    # return Coordenadas(float(data["lat"]), float(data["lon"]))
