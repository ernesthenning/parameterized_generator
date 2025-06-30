import re
import sys
from collections import deque


def replace_datetime(input_data, old_datetime, new_datetime):
    # Кодируем новую дату-время в ascii
    new_datetime_bytes = new_datetime.encode('ascii')

    return input_data.replace(old_datetime.encode('ascii'), new_datetime_bytes)


def find_dates_in_binary(file_path):
    pattern = re.compile(
        rb'(?<!\d)'  # Проверка, что перед датой нет цифры
        rb'(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-(\d{4}) '  # DD-MM-YYYY
        rb'([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])'  # HH:MM:SS
        rb'(?!\d)'  # Проверка, что после даты нет цифры
    )

    unique_dates = set()
    buffer = bytearray()
    chunk_size = 4096  # Размер блока чтения

    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break

            buffer.extend(chunk)
            # Обрабатываем буфер, находя совпадения
            matches = list(pattern.finditer(buffer))

            if matches:
                for match in matches:
                    date_bytes = match.group(0)
                    try:
                        date_str = date_bytes.decode('ascii')
                        unique_dates.add(date_str)
                    except UnicodeDecodeError:
                        continue

                # Сохраняем необработанный "хвост" (20 байт после последней даты)
                last_end = matches[-1].end()
                buffer = bytearray(buffer[last_end - 20:])

    # Проверяем остаток буфера после чтения файла
    final_matches = pattern.finditer(buffer)
    for match in final_matches:
        date_bytes = match.group(0)
        try:
            date_str = date_bytes.decode('ascii')
            unique_dates.add(date_str)
        except UnicodeDecodeError:
            continue

    return sorted(unique_dates)


if __name__ == "__main__":
    dates = find_dates_in_binary('_2024-12-26_09-03.CHW')
    with open('_2024-12-26_09-03.CHW', 'rb') as f:
        data = f.read()

    for date in dates:
        print(date)

    try:
        data_2 = replace_datetime(data, dates[2], '25-03-2025 11:11:11')
        data_3 = replace_datetime(data_2, dates[3], '25-03-2025 11:12:11')
        data_4 = replace_datetime(data_3, dates[4], dates[4])
        data_5 = replace_datetime(data_4, '_2024-12-26_09-03', '_2025-03-25_09-11')
        with open('_2025-03-25_09-11.CHW', 'wb') as f:
            f.write(data_5)
        print(f"Даты и время успешно заменены. Результат сохранен в: {'_2024-12-26_09-03_rep.CHW'}")
    except Exception as e:
        print(f"Ошибка: {str(e)}")
        sys.exit(1)
