from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

curp_validador = RegexValidator(
    regex=(
        r'^([A-Z][AEIOUX][A-Z]{2}\d{2}(?:0[1-9]|1[0-2])' +
        r'(?:0[1-9]|[12]\d|3[01])[HM](?:AS|B[CS]|C[CLMSH]' +
        r'|D[FG]|G[TR]|HG|JC|M[CNS]|N[ETL]|OC|PL|Q[TR]|S[PLR]' +
        r'|T[CSL]|VZ|YN|ZS)[B-DF-HJ-NP-TV-Z]{3}[A-Z\d])(\d)$'),
    message='El CURP no tiene un formato válido',
    code='curp_invalido'
)

google_scholar_link_valdador = RegexValidator(
    regex=r"^https://scholar.google.[a-zA-Z.]+/citations",
    message="Link de Google Scholar inválido. Un link válido tiene la siguiente estructura: https://scholar.google.com/citations?user=",
    code="link_google_scholar_invalido"
)

def limiteTamanioArchivo(archivo):
    limite = 4e6
    if archivo.size > limite:
        raise ValidationError('Archivo demasiado grande. El tamaño del archivo no debería exceder de 2 MB.')
    
def limite10MbArchivo(archivo):
    limit = 10.0
    if archivo.size > limit*1024*1024:
        raise ValidationError('Archivo demasiado grande. El tamaño del archivo no deberia exceder de %sMB' %str(limit))