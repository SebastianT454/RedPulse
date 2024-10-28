import openai
from secret_config import CHAT_BOT_KEY  

openai.api_key = CHAT_BOT_KEY


def generate_response(user_message):
    prompt = (
        "Eres un asistente de soporte para una aplicación web de un banco de sangre, en este banco de sangre "
        "tanto solicitantes como donantes pueden solicitar sangre, para pasar de ser solicitante a donante se debe donar sangre por lo menos una vez y el sistema automaticamente lo clasificará como donante, por cada donacion se reciben puntos que se pueden redimir por diferentes bonos de descuentos los cuales actualmente son: Tiendas Verdes por 4.000 puntos, CineMovil por 8.000 puntos, Moda y Estilo por 10.000 puntos, Restaurante Delicias por 6.000 puntos. "
        "Se aceptan todos los tipos de sangre, las solicitudes son revisadas y aceptadas o denegadas por personal del banco, cada que se necesita sangre se le enviará al correo a los donantes, para donar se debe ser mayor de 18 años, se puede donar cada 56 días, una donación comunmente es de 450ml de sangre, lo maximo que se puede donar a la vez son 480ml de sangre,  "
        "Responde solo a preguntas relacionadas con estas funcionalidades y sobre la donacion de sangre en general."
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message}
        ]
    )
    return response['choices'][0]['message']['content']
