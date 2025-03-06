from fastapi import FastAPI
from pydantic import BaseModel
import string

app = FastAPI()
ALFABETO = string.ascii_lowercase  # "abcdefghijklmnopqrstuvwxyz"

class DescifradoRequest(BaseModel):
    texto_cifrado: str
    clave_descifrado: int
    direccion: str  # "derecha" o "izquierda"

def algoritmo_descifrado(texto_cifrado: str, clave_descifrado: int, direccion: str) -> str:
    texto_plano = ""
    
    if direccion.lower() == "derecha":
        clave_descifrado = -clave_descifrado  # Si es derecha, invierte el desplazamiento

    for letra in texto_cifrado:
        if letra not in ALFABETO:
            texto_plano += letra
        else:
            indice_letra_cifrada = ALFABETO.index(letra)
            indice_letra_descifrada = (indice_letra_cifrada + clave_descifrado) % len(ALFABETO)
            texto_plano += ALFABETO[indice_letra_descifrada]

    return texto_plano

@app.post("/descifrar")
def descifrar_texto(request: DescifradoRequest):
    texto_descifrado = algoritmo_descifrado(request.texto_cifrado, request.clave_descifrado, request.direccion)
    return {"texto_plano": texto_descifrado}
