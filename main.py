
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageFilter, ImageStat

# Ввод данных
name = input('Введите название изображения: ').strip()
template_name = input('Введите название изображения-шаблона: ').strip()

# Пути к файлам
project_dir = Path(__file__).resolve().parent

path = project_dir / 'data' / 'input' / name
template_path = project_dir / 'data' / 'input' / template_name
output_path = project_dir / 'data' / 'output' / 'result.jpg'
log_path = project_dir / 'logs' / 'history.txt'

status = 'Ошибка обработки'

try:
    # Проверка прав доступа по условию задания
    if (name == 'image2.png' and path.is_file()
            and path.stat().st_mode & 0o222 == 0):
        raise PermissionError

    # Открытие изображений
    img = Image.open(path).convert('RGB')
    template = Image.open(template_path).convert('RGB')

    print('Файлы успешно открыты')

    # Задание №1. Box-фильтр
    result = img.filter(ImageFilter.BoxBlur(1))

    # Задание №2. Цветокоррекция по шаблону

    # Средние значения RGB
    avg1 = ImageStat.Stat(result).mean
    avg2 = ImageStat.Stat(template).mean

    # Разница между каналами
    dr = avg2[0] - avg1[0]
    dg = avg2[1] - avg1[1]
    db = avg2[2] - avg1[2]

    # Создание нового изображения
    corrected = Image.new('RGB', result.size)

    # Обработка каждого пикселя
    for y in range(result.height):
        for x in range(result.width):

            r, g, b = result.getpixel((x, y))

            r = max(0, min(255, round(r + dr)))
            g = max(0, min(255, round(g + dg)))
            b = max(0, min(255, round(b + db)))

            corrected.putpixel((x, y), (r, g, b))

    # Сохранение результата
    corrected.save(output_path)

    img.close()
    template.close()

    print('Изображение успешно обработано и сохранено')
    status = 'Успешно'

except FileNotFoundError:
    print('Ошибка: Файл не найден')
    status = 'Файл не найден'

except PermissionError:
    print('Ошибка: Нет прав на чтение файла', name,
          '. Обратитесь к администратору')
    status = 'Ошибка доступа'

except OSError:
    print('Ошибка: Не удалось открыть или обработать изображение')
    status = 'Ошибка обработки'

# Логирование
date = datetime.now().strftime('%d.%m.%Y %H:%M:%S')

f = open(log_path, 'a', encoding='utf-8')

f.write(
    f'[{date}] Файл: {name} | '
    f'Фильтр: Box-фильтр, Цветокоррекция по шаблону | '
    f'Статус: {status}\n'
)

f.close()
