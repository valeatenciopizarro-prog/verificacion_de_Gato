import os

os.environ["TF_USE_LEGACY_KERAS"] = "1"

import discord
from discord.ext import commands
import random
from model import get_class

# Permisos para leer mensajes
intents = discord.Intents.default()
intents.message_content = True

# Crear el bot con prefix $
bot = commands.Bot(command_prefix='$', intents=intents)

# Evento cuando el bot inicia
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

# Comando hello
@bot.command()
async def hello(ctx):
    await ctx.send("Hola estudiantes!")

# Comando dado
@bot.command()
async def dado(ctx):
    numero = random.randint(1,6)
    await ctx.send(f"🎲 Salió: {numero}")


@bot.command()
async def check(ctx):
    if ctx.message.attachments:

        for attachment in ctx.message.attachments:

            file_name = attachment.filename

            # Guardar imagen
            await attachment.save(f"./{file_name}")

            # Clasificar imagen
            resultado = get_class(
                model_path="./keras_model.h5",
                labels_path="labels.txt",
                image_path=f"./{file_name}"
            )

            # Responder
            await ctx.send(
                f"🍌 Resultado: {resultado}"
            )

    else:
        await ctx.send(
            "❌ Olvidaste subir la imagen :("
        )


# Ejecutar bot
bot.run("TU_TOKEN_AQUI")