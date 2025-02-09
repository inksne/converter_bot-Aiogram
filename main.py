from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.utils import markdown
from aiogram.enums.parse_mode import ParseMode
from aiogram.enums.chat_action import ChatAction

from fastapi import FastAPI
import uvicorn

import logging
import asyncio

from config import BOT_TOKEN
from converters.jpg_and_png_to_ico import image_to_ico, ico_to_image
from converters.json_to_xml import json_to_xml, xml_to_json
from converters.png_to_jpeg import convert_image
from converters.jpg_and_png_to_gif import convert_gif_to_image, convert_image_to_gif
from converters.zip_to_tar import convert_tar_gz_to_zip, convert_zip_to_tar_gz


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
app = FastAPI()


@dp.message(CommandStart())
async def handle_start(message: types.Message):
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    text = markdown.text(
        f'Приветствую, {markdown.hbold(message.from_user.full_name)}!',
        markdown.text('Я -', markdown.hbold('бот конвертатор')),
        'Ознакомиться со списком конвертируемых файлов можно по команде /help',
        sep='\n'
    )
    await message.answer(text=text, parse_mode=ParseMode.HTML)


@dp.message(Command('help'))
async def handle_comands(message: types.Message):
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    text = markdown.text(
        markdown.hbold('Список всех команд:'),
        '',
        '/start  -  Запуск бота',
        '/help  -  Справка',
        '',
        '/image_to_ico  -  Изображение в иконку',
        '/ico_to_image  -  Иконка в изображение',
        '/image_to_gif  -  Изображение в GIF',
        '/gif_to_image  -  GIF в изображение',
        '/png_to_jpeg  -  PNG в JPG/JPEG',
        '/jpg_to_png  -  JPG/JPEG в PNG',
        '/json_to_xml  -  JSON в XML',
        '/xml_to_json  -  XML в JSON',
        '/zip_to_tar  -  ZIP в tar.gz',
        '/tar_to_zip  -  tar.gz в ZIP',
        '',
        markdown.hitalic('Прикрепляйте файл вместе с командой!'),
        sep='\n'
    )
    await message.answer(text=text, parse_mode=ParseMode.HTML)


@dp.message(Command('image_to_ico'))
async def handle_image_to_ico(message: types.Message):
    if message.photo:
        await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_DOCUMENT)
        photo = message.photo[-1]
        file_info = await bot.get_file(photo.file_id)
        photo_bytes = await bot.download_file(file_info.file_path)
        
        photo_bytes_data = photo_bytes.getvalue()

        ico_data = await image_to_ico(photo_bytes_data)

        await message.answer_document(types.BufferedInputFile(ico_data, filename='icon.ico'), caption="Вот ваш файл .ico")
    else:
        await message.answer("Пожалуйста, отправьте изображение с командой /image_to_ico.")


@dp.message(Command('ico_to_image'))
async def handle_ico_to_image(message: types.Message):
    if message.document:
        if message.document.file_name.lower().endswith('.ico'):
            await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_DOCUMENT)
            file_info = await bot.get_file(message.document.file_id)
            ico_bytes = await bot.download_file(file_info.file_path)
            ico_bytes_data = ico_bytes.getvalue()

            image_data = await ico_to_image(ico_bytes_data)

            await message.answer_document(types.BufferedInputFile(image_data, filename='image.png'), caption="Вот ваш файл .ico")
        else:
            await message.answer("Пожалуйста, отправьте файл формата .ico.")
    else:
        await message.answer("Пожалуйста, отправьте файл с командой /ico_to_image.")


@dp.message(Command('json_to_xml'))
async def handle_json_to_xml(message: types.Message):
    if message.document:
        file_name = message.document.file_name
        if file_name.lower().endswith('.json'):
            await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

            file_info = await bot.get_file(message.document.file_id)
            file_bytes = await bot.download_file(file_info.file_path)
            json_data = file_bytes.getvalue().decode('utf-8')

            xml_result = json_to_xml(json_data)
            print(xml_result)
            text = markdown.text(
                'Конвертированный JSON:',
                markdown.hpre(xml_result),
                sep='\n'
            )
            await message.answer(text=text, parse_mode=ParseMode.HTML)
        else:
            await message.answer("Пожалуйста, отправьте файл формата .json.")
    else:
        await message.answer("Пожалуйста, отправьте файл с командой /json_to_xml.")


@dp.message(Command('xml_to_json'))
async def handle_xml_to_json(message: types.Message):
    if message.document:
        file_name = message.document.file_name
        if file_name.lower().endswith('.xml'):
            await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

            file_info = await bot.get_file(message.document.file_id)
            file_bytes = await bot.download_file(file_info.file_path)
            xml_data = file_bytes.getvalue().decode('utf-8')

            json_result = xml_to_json(xml_data)
            text = markdown.text(
                'Конвертированный JSON:',
                markdown.hpre(json_result),
                sep='\n'
            )
            await message.answer(text=text, parse_mode=ParseMode.HTML)
        else:
            await message.answer("Пожалуйста, отправьте файл формата .xml.")
    else:
        await message.answer("Пожалуйста, отправьте файл с командой /xml_to_json.")


@dp.message(Command('png_to_jpeg'))
async def handle_png_to_jpg(message: types.Message):
    if message.photo:
        await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_DOCUMENT)

        photo = message.photo[-1]
        file_info = await bot.get_file(photo.file_id)
        photo_bytes = await bot.download_file(file_info.file_path)

        converted_image = convert_image(photo_bytes.getvalue(), 'JPEG')

        await message.answer_document(
            types.BufferedInputFile(converted_image, filename='image.jpeg'),
            caption="Вот ваш файл .jpeg"
        )
    else:
        await message.answer("Пожалуйста, отправьте фото с командой/png_to_jpeg.")


@dp.message(Command('jpg_to_png'))
async def handle_jpg_to_png(message: types.Message):
    if message.photo:
        await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_DOCUMENT)

        photo = message.photo[-1]
        file_info = await bot.get_file(photo.file_id)
        photo_bytes = await bot.download_file(file_info.file_path)

        converted_image = convert_image(photo_bytes.getvalue(), 'PNG')

        await message.answer_document(
            types.BufferedInputFile(converted_image, filename='image.png'),
            caption="Вот ваш файл .png"
        )
    else:
        await message.answer("Пожалуйста, отправьте фото с командой /jpg_to_png.")


@dp.message(Command('image_to_gif'))
async def handle_image_to_gif(message: types.Message):
    if message.photo:
        await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_DOCUMENT)

        photo = message.photo[-1]
        file_info = await bot.get_file(photo.file_id)
        photo_bytes = await bot.download_file(file_info.file_path)

        converted_image = convert_image_to_gif(photo_bytes.getvalue())

        await message.answer_document(
            types.BufferedInputFile(converted_image, filename='gif.gif'),
            caption="Вот ваш файл .gif"
        )
    else:
        await message.answer("Пожалуйста, отправьте фото с командой /image_to_gif.")


@dp.message(Command('gif_to_image'))
async def handle_gif_to_image(message: types.Message):
    if message.document:
        file_name = message.document.file_name
        if file_name.lower().endswith('.gif'):
            await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_DOCUMENT)

            file_info = await bot.get_file(message.document.file_id)
            gif_bytes = await bot.download_file(file_info.file_path)

            converted_image = convert_gif_to_image(gif_bytes.getvalue(), 'PNG')

            await message.answer_document(
                types.BufferedInputFile(converted_image, filename='image.png'),
                caption="Вот ваш файл .png"
            )
        else:
            await message.answer("Пожалуйста, отправьте файл формата .gif.")
    else:
        await message.answer("Пожалуйста, отправьте файл с командой /gif_to_image.")


@dp.message(Command('zip_to_tar'))
async def handle_zip_to_tar(message: types.Message):
    if message.document:
        file_name = message.document.file_name
        if file_name.lower().endswith('.zip'):
            await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_DOCUMENT)

            file_info = await bot.get_file(message.document.file_id)
            zip_bytes = await bot.download_file(file_info.file_path)

            converted_data = convert_zip_to_tar_gz(zip_bytes.getvalue())

            await message.answer_document(
                types.BufferedInputFile(converted_data, filename='tar.tar.gz'),
                caption="Вот ваш файл .tar.gz"
            )
        else:
            await message.answer("Пожалуйста, отправьте файл формата .zip.")
    else:
        await message.answer("Пожалуйста, отправьте файл с командой /zip_to_tar.")


@dp.message(Command('tar_to_zip'))
async def handle_tar_to_zip(message: types.Message):
    if message.document:
        file_name = message.document.file_name
        if file_name.lower().endswith('.tar.gz'):
            await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_DOCUMENT)

            file_info = await bot.get_file(message.document.file_id)
            tar_gz_bytes = await bot.download_file(file_info.file_path)

            converted_data = convert_tar_gz_to_zip(tar_gz_bytes.getvalue())

            await message.answer_document(
                types.BufferedInputFile(converted_data, filename='zip.zip'),
                caption="Вот ваш файл .zip"
            )
        else:
            await message.answer("Пожалуйста, отправьте файл формата .tar.gz.")
    else:
        await message.answer("Пожалуйста, отправьте файл с командой /tar_to_zip.")


async def start_bot():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


async def main():
    uvicorn_config = uvicorn.Config("main:app", host="0.0.0.0", port=10000)
    server = uvicorn.Server(uvicorn_config)
    
    await asyncio.gather(
        start_bot(),
        server.serve()
    )


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        exit(0)