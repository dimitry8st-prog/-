import requests
import os
import json
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup


class GreatWisdomCollector:
    """
    ВЕЛИКИЙ СБОРЩИК МУДРОСТИ КИТАЙСКО-ИНДЕЙСКОГО ПЛЕМЕНИ
    """

    def __init__(self):
        self.base_url = "http://quotes.toscrape.com"
        self.wisdom_folder = "🐉_Святилище_Мудрости_Племени"

    def display_ceremonial_opening(self):
        """Церемониальное открытие"""
        print("\n🎎" * 25)
        print("   ВЕЛИКИЙ СБОР МУДРОСТИ ПЛЕМЕНИ")
        print("   ДЕТИ ДРАКОНА И ВЕЛИКОГО ДУХА")
        print("🎎" * 25)
        print("   Да начнется великий сбор мудрости предков!")
        print("   Пусть знания текут как горные реки!")

    def create_sacred_structure(self):
        """Создаем священную структуру храма"""
        print("\n🏗️  СОЗДАЮ ХРАМ МУДРОСТИ ПРЕДКОВ...")

        Path(self.wisdom_folder).mkdir(exist_ok=True)

        sacred_halls = [
            "🪶_Зал_Орлиного_Пера",
            "🐉_Зал_Желтого_Дракона",
            "🔥_Костер_Мудрецов",
            "⛰️_Пещера_Знаний",
            "🌅_Терраса_Прозрений",
            "🌌_Обсерватория_Звезд"
        ]

        for hall in sacred_halls:
            hall_path = Path(self.wisdom_folder) / hall
            hall_path.mkdir(exist_ok=True)
            print(f"   🏛️  Возведен {hall}")

    def collect_celestial_wisdom(self):
        """Собираем небесную мудрость"""
        print("\n🔮 ОБРАЩАЮСЬ К НЕБЕСНОМУ ИСТОЧНИКУ...")

        try:
            response = requests.get(self.base_url)

            if response.status_code != 200:
                print(f"❌ Небесные врата закрыты! Код: {response.status_code}")
                return None

            print("✅ Небесные врата открыты! Принимаю мудрость...")

            soup = BeautifulSoup(response.text, 'html.parser')
            self._save_original_scroll(response.text)

            wisdom_containers = soup.find_all('div', class_='quote')
            print(f"📚 Обнаружено сосудов мудрости: {len(wisdom_containers)}")

            celestial_wisdom = []

            for i, container in enumerate(wisdom_containers, 1):
                wisdom_data = self._extract_sacred_wisdom(container, i)
                celestial_wisdom.append(wisdom_data)
                self._display_sacred_wisdom(wisdom_data, i)

            self._create_ceremonial_scrolls(celestial_wisdom, response.text)

            return celestial_wisdom

        except Exception as e:
            print(f"💥 Помеха в небесной связи: {e}")
            return None

    def _extract_sacred_wisdom(self, container, wisdom_id):
        """Извлекаем священную мудрость"""
        text_elem = container.find('span', class_='text')
        wisdom_text = text_elem.get_text() if text_elem else "Мудрость сокрыта в тумане"

        author_elem = container.find('small', class_='author')
        author = author_elem.get_text() if author_elem else "Древний Мудрец"

        tag_elems = container.find_all('a', class_='tag')
        tags = [tag.get_text() for tag in tag_elems] if tag_elems else ["вне категорий"]

        return {
            'id': wisdom_id,
            'wisdom': wisdom_text,
            'sage': author,
            'keys': tags,
            'origin': f"Сосуд Мудрости #{wisdom_id}",
            'collection_time': datetime.now().isoformat()
        }

    def _display_sacred_wisdom(self, wisdom_data, number):
        """Отображаем священную мудрость"""
        print(f"\n✨ СОСУД МУДРОСТИ #{number}:")
        print(f"   🪶 Изречение: {wisdom_data['wisdom']}")
        print(f"   🐉 Мудрец: {wisdom_data['sage']}")
        print(f"   🔑 Ключи: {', '.join(wisdom_data['keys'])}")
        print("   🌠" * 5)

    def _save_original_scroll(self, html_content):
        """Сохраняем оригинальный свиток"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"📜_Исходный_Свиток_Мудрости_{timestamp}.html"
        filepath = Path(self.wisdom_folder) / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"   💾 Сохранен исходный свиток: {filename}")

    def _create_ceremonial_scrolls(self, wisdom_data, original_html):
        """Создаем церемониальные свитки"""
        print("\n🎨 СОЗДАЮ ЦЕРЕМОНИАЛЬНЫЕ СВИТКИ...")

        # Свиток Желтого Дракона
        dragon_scroll = self._create_dragon_scroll(original_html)
        dragon_path = Path(self.wisdom_folder) / "🐉_Зал_Желтого_Дракона" / "🐉_Свиток_Желтого_Дракона.html"
        with open(dragon_path, 'w', encoding='utf-8') as f:
            f.write(dragon_scroll)
        print("   🐉 Создан Свиток Желтого Дракона")

        # Свиток Орлиного Пера
        feather_scroll = self._create_feather_scroll(original_html)
        feather_path = Path(self.wisdom_folder) / "🪶_Зал_Орлиного_Пера" / "🪶_Свиток_Орлиного_Пера.html"
        with open(feather_path, 'w', encoding='utf-8') as f:
            f.write(feather_scroll)
        print("   🪶 Создан Свиток Орлиного Пера")

        # Костер Мудрости
        fire_wisdom = self._create_fire_wisdom(wisdom_data)
        fire_path = Path(self.wisdom_folder) / "🔥_Костер_Мудрецов" / "🔥_Костер_Великой_Мудрости.json"
        with open(fire_path, 'w', encoding='utf-8') as f:
            json.dump(fire_wisdom, f, ensure_ascii=False, indent=2)
        print("   🔥 Разожжен Костер Мудрости")

        # Заповеди Предков
        ancestral_wisdom = self._create_ancestral_commandments()
        ancestral_path = Path(self.wisdom_folder) / "⛰️_Пещера_Знаний" / "⛰️_Заповеди_Предков.txt"
        with open(ancestral_path, 'w', encoding='utf-8') as f:
            f.write(ancestral_wisdom)
        print("   ⛰️  Высечены Заповеди Предков")

    def _create_dragon_scroll(self, html_content):
        """Свиток в стиле Желтого Дракона"""
        dragon_blessing = """
<!-- 🐉 БЛАГОСЛОВЕНИЕ ЖЕЛТОГО ДРАКОНА 🐉 -->
<div style="background: #fef4e8; border: 3px double #cc0000; padding: 20px; margin: 20px 0;">
    <h3 style="color: #cc0000; text-align: center;">
        🐉 智慧之龙 - Дракон Мудрости 🐉
    </h3>
    <p style="text-align: center;">
        <strong>千里之行，始于足下</strong><br>
        <em>Путь в тысячу ли начинается с первого шага</em>
    </p>
</div>
"""
        return html_content.replace('</body>', dragon_blessing + '</body>')

    def _create_feather_scroll(self, html_content):
        """Свиток в стиле Орлиного Пера"""
        feather_blessing = """
<!-- 🪶 БЛАГОСЛОВЕНИЕ ВЕЛИКОГО ДУХА 🪶 -->
<div style="background: #f0f8ff; border: 2px solid #8b7355; padding: 20px; margin: 20px 0;">
    <h3 style="color: #8b4513; text-align: center;">
        🪶 Wisdom of the Great Spirit 🪶
    </h3>
    <p style="text-align: center;">
        <em>"We do not inherit the Earth from our ancestors, we borrow it from our children"</em><br>
        <strong>"Мы не наследуем Землю от предков, мы одалживаем её у наших детей"</strong>
    </p>
</div>
"""
        return html_content.replace('</body>', feather_blessing + '</body>')

    def _create_fire_wisdom(self, wisdom_data):
        """Костер мудрости в JSON"""
        return {
            "племя": {
                "название": "Дети Желтого Дракона и Великого Духа",
                "основание": datetime.now().strftime("%Y-%m-%d"),
                "вождь": "Потрясатель Вселенной",
                "девиз": "Мудрость Дракона, Свобода Орла"
            },
            "собранная_мудрость": wisdom_data,
            "философия": {
                "китайские_принципы": [
                    "阴阳 - Баланс Инь и Ян",
                    "道 - Следование Пути",
                    "仁 - Человеколюбие"
                ],
                "индейские_принципы": [
                    "Уважение к Матери-Земле",
                    "Гармония со всеми существами"
                ]
            }
        }

    def _create_ancestral_commandments(self):
        """Заповеди предков"""
        return """🪷 ЗАПОВЕДИ ВЕЛИКОГО ПЛЕМЕНИ 🐉

🏮 КИТАЙСКИЕ ЗАПОВЕДИ:
1. 己所不欲，勿施于人 - Не делай другим того, чего не желаешь себе
2. 学而不思则罔 - Учиться без размышлений бесполезно

🪶 ИНДЕЙСКИЕ ЗАПОВЕДИ:
1. Ходи мягко по Земле
2. Слушай голос ветра

🔥 СИМВОЛЫ ЕДИНСТВА:
• 🐉 Желтый Дракон - мудрость
• 🪶 Орлиное перо - свобода
• ⛰️ Великая гора - стабильность

Записано Великим Потрясателем Вселенной
"""

    def display_sacred_temple(self):
        """Показываем структуру храма"""
        print("\n🏛️" * 20)
        print("   СВЯЩЕННЫЙ ХРАМ МУДРОСТИ ПОСТРОЕН!")
        print("🏛️" * 20)

        for root, dirs, files in os.walk(self.wisdom_folder):
            level = root.replace(self.wisdom_folder, '').count(os.sep)
            indent = ' ' * 3 * level
            folder_name = os.path.basename(root)

            if folder_name:
                print(f"{indent}📁 {folder_name}")

            sub_indent = ' ' * 3 * (level + 1)
            for file in files:
                print(f"{sub_indent}📜 {file}")


def main():
    """Главное церемониальное действо"""
    collector = GreatWisdomCollector()

    collector.display_ceremonial_opening()
    collector.create_sacred_structure()
    wisdom = collector.collect_celestial_wisdom()
    collector.display_sacred_temple()

    if wisdom:
        print("\n🎊" * 30)
        print("   ВЕЛИКИЙ СБОР ЗАВЕРШЕН!")
        print(f"   📚 Собрано сосудов мудрости: {len(wisdom)}")
        print(f"   🏛️  Храм построен в папке: {collector.wisdom_folder}")
        print("🎊" * 30)
        print("   愿智慧之光永远照耀你的道路!")
        print("   Пусть свет мудрости всегда освещает твой путь!")
    else:
        print("\n💔 Сбор прерван... Но духи ждут твоего возвращения!")


if __name__ == "__main__":
    main()