
import asyncio

from openpyxl import load_workbook
import requests
import time
import random
import os
import json
from aiohttp import ClientSession


async def download_file(file: str):
    wb = load_workbook(filename=file)
    sheet_ranges = wb['eBook list']

    async with ClientSession() as session:
        for i, row in enumerate(sheet_ranges):
            if i == 0:
                continue
            book_title = row[0].value
            isbn = row[7].value
            pdf_url = f'https://link.springer.com/content/pdf/10.1007%2F{isbn}.pdf'
            epub_url = f'https://link.springer.com/download/epub/10.1007%2F{isbn}.epub'

            urls = [pdf_url, epub_url]
            extensions = ['pdf', 'epub']

            for url, extension in zip(urls, extensions):

                file_name = f'{isbn}.{extension}'
                if os.path.isfile(file_name):
                    print(f'{file_name} exists')
                    continue
                await download(session, url, file_name)


async def download(session: ClientSession, url: str, file_name: str):
    async with session.get(url) as response:
        if response.status == 200:
            with open(file_name, 'wb') as file:
                file.write(await response.read())
            await asyncio.sleep(random.uniform(1, 3))
            print(f'Downloaded {file_name}')


if __name__ == '__main__':
    with open("config.json") as file:
        config = json.load(file)

    loop = asyncio.get_event_loop()

    tasks = []
    for file in config['files']:
        task = asyncio.ensure_future(download_file(file))
        tasks.append(task)
    loop.run_until_complete(asyncio.wait(tasks))
