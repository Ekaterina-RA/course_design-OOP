import os
from pathlib import Path


ROOT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(ROOT_DIR, 'data')
file_path = os.path.join(DATA_DIR, 'vacancies.json')

# Проверяем существование файла
if not os.path.exists(file_path):
    raise FileNotFoundError(f"Файл не найден: {file_path}")

BASE_DIR = Path(__file__).resolve().parent

JSON_PATH = BASE_DIR.joinpath('vacancies.json')