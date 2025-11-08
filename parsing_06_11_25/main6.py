import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
import os


def extract_all_wisdom():
    """
    Функция для извлечения всех цитат со ВСЕХ страниц мудрости
    и сохранения в красивый HTML файл
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

        # 4. СОХРАНЯЕМ ВСЕ ДАННЫЕ В КРАСИВЫЙ HTML ФАЙЛ
        if all_quotes_data:
            save_quotes_to_html(all_quotes_data)
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
    """
    for quote in existing_quotes:
        if quote['text'] == new_quote_text and quote['author'] == new_author:
            return True
    return False


def save_quotes_to_html(quotes_data):
    """
    Сохраняет все собранные цитаты в красивый HTML файл

    Args:
        quotes_data (list): Список словарей с данными цитат
    """
    filename = 'wisdom_collection.html'

    print(f"\n💾 Создаю красивую HTML страницу '{filename}'...")

    try:
        with open(filename, 'w', encoding='utf-8') as file:
            # Начало HTML документа
            file.write("""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📚 Великий Архив Мудрости</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            background: rgba(255, 255, 255, 0.95);
            padding: 40px;
            border-radius: 20px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            backdrop-filter: blur(10px);
        }

        .header h1 {
            font-size: 3em;
            color: #4a5568;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .header .subtitle {
            font-size: 1.2em;
            color: #718096;
            margin-bottom: 20px;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }

        .stat-card {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }

        .stat-number {
            font-size: 2em;
            font-weight: bold;
            display: block;
        }

        .quotes-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }

        .quote-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border-left: 5px solid #667eea;
            position: relative;
            overflow: hidden;
        }

        .quote-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
        }

        .quote-card::before {
            content: '"';
            font-size: 6em;
            color: #667eea;
            opacity: 0.1;
            position: absolute;
            top: -20px;
            left: 10px;
            font-family: Georgia, serif;
        }

        .quote-text {
            font-size: 1.1em;
            line-height: 1.6;
            color: #4a5568;
            margin-bottom: 20px;
            font-style: italic;
            position: relative;
            z-index: 1;
        }

        .quote-author {
            font-weight: bold;
            color: #667eea;
            text-align: right;
            font-size: 1em;
            margin-bottom: 15px;
            position: relative;
            z-index: 1;
        }

        .quote-author::before {
            content: "— ";
        }

        .quote-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            position: relative;
            z-index: 1;
        }

        .tag {
            background: linear-gradient(135deg, #90cdf4, #63b3ed);
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 500;
        }

        .quote-meta {
            font-size: 0.8em;
            color: #a0aec0;
            text-align: right;
            margin-top: 10px;
            position: relative;
            z-index: 1;
        }

        .footer {
            text-align: center;
            background: rgba(255, 255, 255, 0.9);
            padding: 20px;
            border-radius: 15px;
            margin-top: 40px;
            color: #718096;
        }

        @media (max-width: 768px) {
            .quotes-grid {
                grid-template-columns: 1fr;
            }

            .header h1 {
                font-size: 2em;
            }

            .stats {
                grid-template-columns: 1fr;
            }
        }

        .loading {
            text-align: center;
            padding: 40px;
            color: white;
        }

        .pulse {
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 Великий Архив Мудрости</h1>
            <div class="subtitle">Собрано с quotes.toscrape.com</div>
            <div class="stats">
""")

            # Статистика
            total_quotes = len(quotes_data)
            unique_authors = len(set(quote['author'] for quote in quotes_data))
            all_tags = [tag for quote in quotes_data for tag in quote['tags']]
            unique_tags = len(set(all_tags))
            total_pages = max(quote['page'] for quote in quotes_data)

            file.write(f"""
                <div class="stat-card">
                    <span class="stat-number">{total_quotes}</span>
                    <span>Всего цитат</span>
                </div>
                <div class="stat-card">
                    <span class="stat-number">{unique_authors}</span>
                    <span>Авторов</span>
                </div>
                <div class="stat-card">
                    <span class="stat-number">{unique_tags}</span>
                    <span>Уникальных тегов</span>
                </div>
                <div class="stat-card">
                    <span class="stat-number">{total_pages}</span>
                    <span>Страниц обработано</span>
                </div>
            </div>
            <div class="quote-meta" style="margin-top: 20px; text-align: center;">
                Собрано: {time.strftime('%d.%m.%Y %H:%M:%S')}
            </div>
        </div>

        <div class="quotes-grid">
""")

            # Создаем прогресс-бар для записи цитат
            with tqdm(quotes_data, desc="💾 Запись цитат в HTML", unit="цитат") as pbar:
                for i, quote in enumerate(pbar, 1):
                    # Записываем карточку цитаты
                    file.write(f"""
            <div class="quote-card">
                <div class="quote-text">{quote['text']}</div>
                <div class="quote-author">{quote['author']}</div>
                <div class="quote-tags">
    """)

                    # Записываем теги
                    if quote['tags']:
                        for tag in quote['tags']:
                            file.write(f'<span class="tag">{tag}</span>')
                    else:
                        file.write('<span class="tag">без тегов</span>')

                    # Мета-информация
                    file.write(f"""
                </div>
                <div class="quote-meta">Цитата #{i} • Страница {quote['page']}</div>
            </div>
    """)

                    pbar.set_postfix({'текущая': i})

            # Закрываем основную структуру
            file.write("""
        </div>

        <div class="footer">
            <p>✨ Собрано с любовью к мудрости и знаниям</p>
            <p>📅 "Время, проведенное в чтении мудрых мыслей, есть время, приобретенное для жизни"</p>
        </div>
    </div>

    <script>
        // Добавляем анимацию появления карточек
        document.addEventListener('DOMContentLoaded', function() {
            const cards = document.querySelectorAll('.quote-card');
            cards.forEach((card, index) => {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';

                setTimeout(() => {
                    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }, index * 100);
            });
        });
    </script>
</body>
</html>
""")

        print(f"✅ Красивая HTML страница создана: '{filename}'!")
        print(f"📊 Итоговая статистика:")
        print(f"   • Цитат: {total_quotes}")
        print(f"   • Авторов: {unique_authors}")
        print(f"   • Тегов: {unique_tags}")
        print(f"   • Страниц: {total_pages}")

        # Показываем путь к файлу
        file_path = os.path.abspath(filename)
        print(f"📁 Файл сохранен: {file_path}")

    except IOError as e:
        print(f"❌ Ошибка при записи в файл '{filename}': {e}")
    except Exception as e:
        print(f"❌ Неожиданная ошибка при создании HTML: {e}")


def demonstrate_features():
    """
    Демонстрация возможностей HTML страницы
    """
    print("\n" + "🎨" * 30)
    print("ВОЗМОЖНОСТИ HTML СТРАНИЦЫ")
    print("🎨" * 30)

    print("""
✨ ОСОБЕННОСТИ СОЗДАННОЙ СТРАНИЦЫ:

🎯 ДИЗАЙН:
• Современный градиентный фон
• Адаптивная сетка карточек
• Плавные анимации и переходы
• Стеклянный эффект (glassmorphism)
• Полная поддержка мобильных устройств

📊 СТАТИСТИКА:
• Красивые карточки с показателями
• Общая информация о сборе
• Подсчет уникальных авторов и тегов

🎪 КАРТОЧКИ ЦИТАТ:
• Ховер-эффекты с подъемом
• Красивые градиенты для тегов
• Номера цитат и страниц
• Элегантная типографика

⚡ ИНТЕРАКТИВНОСТЬ:
• Плавное появление карточек
• Анимация при наведении
• Адаптивный дизайн
• JavaScript анимации

📱 ДОСТУПНОСТЬ:
• Полная адаптивность
• Оптимизация для мобильных
• Читаемые шрифты
• Правильные контрасты
    """)


# Запускаем сборщик
if __name__ == "__main__":
    # Демонстрируем возможности
    demonstrate_features()

    print("\n" + "🚀" * 30)
    print("НАЧИНАЕМ СОЗДАНИЕ КРАСИВОЙ СТРАНИЦЫ")
    print("🚀" * 30)

    # Запускаем сбор всех цитат
    extract_all_wisdom()