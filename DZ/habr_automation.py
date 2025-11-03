import asyncio
import os
import json
import logging
import argparse
import sys
from datetime import datetime
from typing import List, Dict, Optional
from playwright.async_api import async_playwright


class HabrAutomation:
    """Класс для автоматизации действий на сайте Habr"""

    def __init__(self):
        self.setup_logging()
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def setup_logging(self) -> None:
        """Настройка системы логирования"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('habr_automation.log', encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    async def setup_browser(self, headless: bool = True) -> None:
        """
        Настройка и запуск браузера
        """
        try:
            self.logger.info("Инициализация Playwright...")
            self.playwright = await async_playwright().start()

            self.logger.info(f"Запуск браузера (headless={headless})...")
            self.browser = await self.playwright.chromium.launch(
                headless=headless,
                args=[
                    '--window-size=1280,720',
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled',
                    '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                ],
                timeout=60000
            )

            self.context = await self.browser.new_context(
                viewport={'width': 1280, 'height': 720},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            )

            self.page = await self.context.new_page()

            # Устанавливаем таймауты
            self.page.set_default_timeout(30000)
            self.page.set_default_navigation_timeout(40000)

            self.logger.info("Браузер успешно запущен")

        except Exception as e:
            self.logger.error(f"Ошибка при запуске браузера: {e}")
            raise

    async def navigate_to_site(self, url: str = "https://habr.com") -> str:
        """
        Переход на указанный URL и ожидание загрузки
        """
        try:
            self.logger.info(f"Переход на сайт: {url}")

            # Пробуем разные стратегии загрузки
            try:
                await self.page.goto(url, wait_until='networkidle', timeout=40000)
            except Exception as network_idle_error:
                self.logger.warning(f"Networkidle timeout, trying domcontentloaded: {network_idle_error}")
                await self.page.goto(url, wait_until='domcontentloaded', timeout=40000)

            # Ожидание загрузки основных элементов с разными селекторами
            selectors_to_wait = [
                'article',
                '.tm-articles-list',
                '.tm-article-snippet',
                '[class*="article"]',
                '.post__title'
            ]

            for selector in selectors_to_wait:
                try:
                    await self.page.wait_for_selector(selector, timeout=10000)
                    self.logger.info(f"Найден селектор: {selector}")
                    break
                except Exception:
                    continue
            else:
                self.logger.warning("Не удалось найти ожидаемые элементы на странице")

            self.logger.info("Страница успешно загружена")

            # Получаем заголовок страницы
            title = await self.page.title()
            print(f"📄 Заголовок страницы: {title}")

            return title

        except Exception as e:
            self.logger.error(f"Ошибка при загрузке страницы: {e}")

            # Пробуем альтернативный URL
            if "habr.com" in url:
                self.logger.info("Пробуем альтернативный URL...")
                try:
                    alternative_url = "https://habr.com/ru/articles/"
                    await self.page.goto(alternative_url, wait_until='domcontentloaded', timeout=30000)
                    title = await self.page.title()
                    print(f"📄 Заголовок страницы (альтернативный URL): {title}")
                    return title
                except Exception as alt_error:
                    self.logger.error(f"Ошибка при загрузке альтернативного URL: {alt_error}")

            raise

    async def take_screenshot(self, url: str) -> str:
        """
        Создание скриншота всей страницы
        """
        try:
            # Создаем папку для скриншотов
            screenshots_dir = "screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)

            # Генерируем имя файла
            domain = url.split('//')[-1].split('/')[0].replace('.', '_')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{screenshots_dir}/{domain}_{timestamp}.png"

            # Делаем скриншот
            await self.page.screenshot(path=filename, full_page=True)
            self.logger.info(f"Скриншот сохранен: {filename}")
            print(f"📸 Путь к скриншоту: {filename}")

            return filename

        except Exception as e:
            self.logger.error(f"Ошибка при создании скриншота: {e}")
            raise

    async def check_connection(self) -> bool:
        """
        Проверка подключения к интернету
        """
        try:
            # Пробуем загрузить простую страницу для проверки соединения
            test_page = await self.context.new_page()
            await test_page.goto('https://www.google.com', wait_until='domcontentloaded', timeout=15000)
            await test_page.close()
            self.logger.info("Проверка подключения: OK")
            return True
        except Exception as e:
            self.logger.error(f"Проверка подключения: FAILED - {e}")
            return False

    async def close(self) -> None:
        """Корректное закрытие браузера и освобождение ресурсов"""
        try:
            if hasattr(self, 'browser') and self.browser:
                await self.browser.close()
                self.logger.info("Браузер закрыт")

            if hasattr(self, 'playwright') and self.playwright:
                await self.playwright.stop()
                self.logger.info("Playwright остановлен")

        except Exception as e:
            self.logger.error(f"Ошибка при закрытии браузера: {e}")


async def run_standalone():
    """Запуск автономной версии скрипта"""
    parser = argparse.ArgumentParser(description='Habr Automation Script')
    parser.add_argument('--url', default='https://habr.com', help='URL для перехода')
    parser.add_argument('--headless', action='store_true', default=True, help='Headless режим')
    parser.add_argument('--screenshot', action='store_true', default=True, help='Создавать скриншот')
    parser.add_argument('--timeout', type=int, default=40000, help='Таймаут в миллисекундах')

    args = parser.parse_args()

    automation = HabrAutomation()

    try:
        # Настройка браузера
        await automation.setup_browser(headless=args.headless)

        # Проверка подключения
        if not await automation.check_connection():
            print("❌ Нет подключения к интернету")
            return

        # Переход на сайт
        title = await automation.navigate_to_site(args.url)

        # Создание скриншота
        if args.screenshot:
            screenshot_path = await automation.take_screenshot(args.url)

        print("✅ Скрипт успешно выполнен")

    except KeyboardInterrupt:
        automation.logger.info("Скрипт прерван пользователем")
        print("\n⚠️  Скрипт прерван пользователем")
    except Exception as e:
        automation.logger.error(f"Ошибка в основном потоке: {e}")
        print(f"❌ Произошла ошибка: {e}")

        # Сохраняем скриншот ошибки
        try:
            error_screenshot = f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            await automation.page.screenshot(path=error_screenshot, full_page=True)
            print(f"📸 Скриншот ошибки сохранен: {error_screenshot}")
        except:
            pass

    finally:
        await automation.close()


if __name__ == "__main__":
    asyncio.run(run_standalone())