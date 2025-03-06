from fastapi import FastAPI
from pydantic import BaseModel
import os
import uvicorn
import string

# Crear la aplicación FastAPI
app = FastAPI()

# Definir los caracteres permitidos en el cifrado
ALFABETO = string.ascii_lowercase + string.ascii_uppercase + string.digits  # Minúsculas, mayúsculas y números

class CifradoRequest(BaseModel):
    texto_cifrado: str
    clave_descifrado: int
    direccion: str  # "derecha" o "izquierda"

def algoritmo_descifrado(texto_cifrado: str, clave_descifrado: int, direccion: str) -> str:
    texto_plano = ""

    for caracter in texto_cifrado:
        if caracter in ALFABETO:
            indice = ALFABETO.index(caracter)

            if direccion == "izquierda":
                nuevo_indice = (indice - clave_descifrado) % len(ALFABETO)
            elif direccion == "derecha":
                nuevo_indice = (indice + clave_descifrado) % len(ALFABETO)
            else:
                return "Error: Dirección inválida. Usa 'izquierda' o 'derecha'."

            texto_plano += ALFABETO[nuevo_indice]
        else:
            texto_plano += caracter  # Mantiene espacios y caracteres especiales

    return texto_plano

@app.post("/descifrar")
async def descifrar(request: CifradoRequest):
    resultado = algoritmo_descifrado(request.texto_cifrado, request.clave_descifrado, request.direccion)
    return {"texto_plano": resultado}

# Configuración para Render: Usar el puerto asignado dinámicamente
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
