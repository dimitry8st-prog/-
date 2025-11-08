import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm


def extract_all_wisdom():
    """
    Функция для извлечения всех цитат со ВСЕХ страниц мудрости
    """

    base_url = "http://quotes.toscrape.com"
    current_url = base_url

    print("🧘 НАЧИНАЮ ВЕЛИКИЙ СБОР МУДРОСТИ СО ВСЕХ СТРАНИЦ")
    print("=" * 60)

    all_quotes_data = []
    page_number = 1

    try:
        # Создаем прогресс-бар для общего процесса
        with tqdm(desc="📖 Сбор мудрости", unit="стр") as pbar:
            while current_url:
                print(f"\n🌐 Обрабатываю страницу {page_number}: {current_url}")

                # Отправляем запрос к источнику мудрости
                response = requests.get(current_url)

                # Проверяем, открылись ли врата мудрости
                if response.status_code != 200:
                    print(f"❌ Врата мудрости закрыты на странице {page_number}! Код: {response.status_code}")
                    break

                # Создаем объект BeautifulSoup для чтения священного свитка
                soup = BeautifulSoup(response.text, 'html.parser')

                # 1. НАХОДИМ ВСЕ ЭЛЕМЕНТЫ С ЦИТАТАМИ НА ТЕКУЩЕЙ СТРАНИЦЕ
                quote_containers = soup.find_all('div', class_='quote')

                print(f"📚 Найдено цитат на странице {page_number}: {len(quote_containers)}")

                # Если цитат не найдено, проверяем следующую страницу
                if not quote_containers:
                    print(f"💔 Не найдено цитат на странице {page_number}...")

                # 2. ИЗВЛЕКАЕМ МУДРОСТЬ ИЗ КАЖДОГО СОСУДА НА ТЕКУЩЕЙ СТРАНИЦЕ
                page_quotes_count = 0

                for quote_container in quote_containers:
                    # ИЗВЛЕКАЕМ ТЕКСТ ЦИТАТЫ
                    quote_text_element = quote_container.find('span', class_='text')
                    quote_text = quote_text_element.get_text() if quote_text_element else "Текст мудрости утерян"

                    # ИЗВЛЕКАЕМ АВТОРА
                    author_element = quote_container.find('small', class_='author')
                    author = author_element.get_text() if author_element else "Автор неизвестен"

                    # ИЗВЛЕКАЕМ ТЕГИ
                    tag_elements = quote_container.find_all('a', class_='tag')
                    tags = [tag.get_text() for tag in tag_elements] if tag_elements else []

                    # Проверяем уникальность цитаты перед добавлением
                    if not is_duplicate_quote(all_quotes_data, quote_text, author):
                        quote_data = {
                            'text': quote_text,
                            'author': author,
                            'tags': tags,
                            'page': page_number
                        }
                        all_quotes_data.append(quote_data)
                        page_quotes_count += 1
                    else:
                        print(f"⚠️  Пропущена дублирующая цитата: {quote_text[:50]}...")

                print(f"✅ Добавлено уникальных цитат со страницы {page_number}: {page_quotes_count}")

                # 3. ПРОВЕРЯЕМ НАЛИЧИЕ СЛЕДУЮЩЕЙ СТРАНИЦЫ
                next_button = soup.find('li', class_='next')

                if next_button:
                    next_link = next_button.find('a')
                    if next_link and next_link.get('href'):
                        current_url = base_url + next_link['href']
                        page_number += 1

                        # Добавляем задержку между запросами
                        print("⏳ Задержка перед следующим запросом...")
                        time.sleep(1)  # Задержка 1 секунда между страницами
                    else:
                        current_url = None
                else:
                    current_url = None
                    print("🎯 Достигнута последняя страница!")

                # Обновляем прогресс-бар
                pbar.update(1)
                pbar.set_postfix({
                    'страниц': page_number,
                    'цитат': len(all_quotes_data)
                })

        # 4. СОХРАНЯЕМ ВСЕ ДАННЫЕ В ФАЙЛ
        if all_quotes_data:
            save_quotes_to_file(all_quotes_data)
        else:
            print("💔 Не собрано ни одной цитаты для сохранения.")

        print("=" * 60)
        print(f"🎉 ВЕЛИКИЙ СБОР ЗАВЕРШЕН!")
        print(f"📖 Всего обработано страниц: {page_number}")
        print(f"📚 Всего собрано уникальных цитат: {len(all_quotes_data)}")

    except requests.exceptions.RequestException as e:
        print(f"🌐 Ошибка сети: {e}")
    except Exception as e:
        print(f"💥 На пути возникла преграда: {e}")


def is_duplicate_quote(existing_quotes, new_quote_text, new_author):
    """
    Проверяет, является ли цитата дубликатом

    Args:
        existing_quotes (list): Список уже собранных цитат
        new_quote_text (str): Текст новой цитаты
        new_author (str): Автор новой цитаты

    Returns:
        bool: True если цитата дублируется, False если уникальна
    """
    for quote in existing_quotes:
        if quote['text'] == new_quote_text and quote['author'] == new_author:
            return True
    return False


def save_quotes_to_file(quotes_data):
    """
    Сохраняет все собранные цитаты в текстовый файл

    Args:
        quotes_data (list): Список словарей с данными цитат
    """
    filename = 'all_quotes.txt'

    print(f"\n💾 Начинаю сохранение всей мудрости в файл '{filename}'...")

    try:
        with open(filename, 'w', encoding='utf-8') as file:
            # Записываем заголовок с общей статистикой
            file.write("=" * 60 + "\n")
            file.write(f"📚 ВЕЛИКИЙ АРХИВ МУДРОСТИ\n")
            file.write(f"📖 Всего цитат: {len(quotes_data)}\n")
            file.write(f"📅 Собрано: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write("=" * 60 + "\n\n")

            # Создаем прогресс-бар для записи в файл
            with tqdm(quotes_data, desc="💾 Сохранение в файл", unit="цитат") as pbar:
                for i, quote in enumerate(pbar, 1):
                    # Записываем разделитель для цитаты
                    file.write(f"{'=' * 7} ЦИТАТА {i} (Страница {quote['page']}) {'=' * 7}\n\n")

                    # Записываем текст цитаты
                    file.write(f"Текст: {quote['text']}\n\n")

                    # Записываем автора
                    file.write(f"Автор: {quote['author']}\n\n")

                    # Записываем теги
                    tags_str = ", ".join(quote['tags']) if quote['tags'] else "нет тегов"
                    file.write(f"Теги: {tags_str}\n\n")

                    # Обновляем прогресс-бар
                    pbar.set_postfix({'текущая': i})

            # Добавляем итоговую статистику
            file.write("=" * 60 + "\n")
            file.write("📊 СТАТИСТИКА СОБРАННОЙ МУДРОСТИ:\n")
            file.write(f"• Всего цитат: {len(quotes_data)}\n")

            # Статистика по авторам
            authors = [quote['author'] for quote in quotes_data]
            unique_authors = set(authors)
            file.write(f"• Уникальных авторов: {len(unique_authors)}\n")

            # Статистика по тегам
            all_tags = []
            for quote in quotes_data:
                all_tags.extend(quote['tags'])
            file.write(f"• Всего тегов: {len(all_tags)}\n")
            file.write(f"• Уникальных тегов: {len(set(all_tags))}\n")
            file.write("=" * 60 + "\n")

        print(f"✅ Вся мудрость успешно сохранена в файл '{filename}'!")
        print(f"📊 Итоговая статистика:")
        print(f"   • Цитат: {len(quotes_data)}")
        print(f"   • Авторов: {len(set([q['author'] for q in quotes_data]))}")
        print(f"   • Страниц обработано: {max([q['page'] for q in quotes_data])}")

    except IOError as e:
        print(f"❌ Ошибка при записи в файл '{filename}': {e}")
    except Exception as e:
        print(f"❌ Неожиданная ошибка при сохранении файла: {e}")


def demonstrate_pagination():
    """
    Демонстрация работы с пагинацией
    """
    print("\n" + "🔗" * 30)
    print("РАЗЪЯСНЕНИЕ ПАГИНАЦИИ")
    print("🔗" * 30)

    print("""
📖 САЙТ quotes.toscrape.com ИСПОЛЬЗУЕТ ПАГИНАЦИЮ:

Структура навигации:
<nav>
  <ul class="pager">
    <li class="next">
      <a href="/page/2/">Next →</a>
    </li>
  </ul>
</nav>

🎯 АЛГОРИТМ ОБХОДА ВСЕХ СТРАНИЦ:
1. Начинаем с главной страницы
2. Ищем элемент <li class="next">
3. Если находим - извлекаем ссылку на следующую страницу
4. Повторяем процесс для каждой следующей страницы
5. Когда <li class="next"> отсутствует - мы на последней странице

⚡ ОСОБЕННОСТИ РЕАЛИЗАЦИИ:
• Задержка 1 секунда между запросами
• Проверка уникальности цитат
• Прогресс-бар для визуализации
• Обработка всех возможных ошибок
    """)


# Запускаем наш усовершенствованный сборщик
if __name__ == "__main__":
    # Демонстрируем работу с пагинацией
    demonstrate_pagination()

    print("\n" + "🚀" * 30)
    print("ПЕРЕХОДИМ К ПОЛНОМУ СБОРУ МУДРОСТИ")
    print("🚀" * 30)

    # Запускаем сбор всех цитат
    extract_all_wisdom()