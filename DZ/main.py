"""
Основной скрипт для браузерной автоматизации и анализа кода
"""

import asyncio
import argparse
from DZ.habr_automation import HabrAutomation
from DZ.code_analyzer import CodeDocumentationGenerator


async def run_habr_automation(args):
    """Запуск автоматизации Habr"""
    print("🚀 Запуск автоматизации Habr...")

    automation = HabrAutomation()

    try:
        # Настройка браузера
        await automation.setup_browser(headless=args.headless)

        # Переход на сайт
        title = await automation.navigate_to_site(args.url)

        # Создание скриншота
        if args.screenshot:
            screenshot_path = await automation.take_screenshot(args.url)

        # Извлечение данных
        articles_data = await automation.extract_articles_data(args.keywords)

        # Сохранение и вывод статистики
        if articles_data['articles']:
            json_file = await automation.save_to_json(articles_data)
            automation.print_statistics(articles_data)

    except KeyboardInterrupt:
        automation.logger.info("Скрипт прерван пользователем")
    except Exception as e:
        automation.logger.error(f"Ошибка в основном потоке: {e}")
    finally:
        await automation.close()


def run_code_analysis(args):
    """Запуск анализа кода и генерации документации"""
    print("🔍 Запуск анализа кода...")

    generator = CodeDocumentationGenerator(args.project_path)
    generator.analyze_project()

    output_dir = args.output_dir
    generator.generate_markdown_docs(output_dir)
    generator.generate_json_structure(output_dir)
    generator.generate_uml_diagram(output_dir)

    print("✅ Документация успешно сгенерирована!")
    print(f"📁 Файлы сохранены в: {output_dir}/")


def main():
    """Основная функция"""
    parser = argparse.ArgumentParser(description='Browser Automation and Code Analysis Toolkit')
    subparsers = parser.add_subparsers(dest='command', help='Доступные команды')

    # Парсер для Habr автоматизации
    habr_parser = subparsers.add_parser('habr', help='Автоматизация Habr')
    habr_parser.add_argument('--url', default='https://habr.com', help='URL для перехода')
    habr_parser.add_argument('--headless', action='store_true', default=True, help='Headless режим')
    habr_parser.add_argument('--keywords', nargs='+', help='Ключевые слова для фильтрации')
    habr_parser.add_argument('--screenshot', action='store_true', default=True, help='Создавать скриншот')

    # Парсер для анализа кода
    code_parser = subparsers.add_parser('analyze', help='Анализ кода и генерация документации')
    code_parser.add_argument('--project-path', default='.', help='Путь к проекту')
    code_parser.add_argument('--output-dir', default='docs', help='Директория для документации')

    args = parser.parse_args()

    if args.command == 'habr':
        asyncio.run(run_habr_automation(args))
    elif args.command == 'analyze':
        run_code_analysis(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()