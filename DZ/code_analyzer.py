import ast
import os
import subprocess
from datetime import datetime
from typing import Dict, List, Any


class CodeDocumentationGenerator:
    """Генератор документации для Python проектов"""
    
    def __init__(self, project_path: str):
        self.project_path = os.path.abspath(project_path)
        self.structure = {
            'project_info': {
                'name': os.path.basename(self.project_path),
                'analysis_date': datetime.now().isoformat(),
                'total_files': 0
            },
            'modules': [],
            'functions': [],
            'classes': [],
            'imports': {},
            'dependencies': set()
        }
    
    def analyze_project(self) -> None:
        """Основной метод анализа проекта"""
        print(f"🔍 Анализ проекта: {self.project_path}")
        
        self._extract_git_info()
        self._walk_directory()
        self._generate_dependencies()
        
        self.structure['project_info']['total_files'] = len(self.structure['modules'])
        print(f"✅ Проанализировано {len(self.structure['modules'])} файлов")
    
    def _extract_git_info(self) -> None:
        """Извлечение информации из git истории"""
        try:
            result = subprocess.run(
                ['git', 'log', '--oneline', '-10'],
                capture_output=True, text=True, cwd=self.project_path,
                timeout=30
            )
            if result.returncode == 0:
                self.structure['git_history'] = [
                    line for line in result.stdout.split('\n') if line.strip()
                ]
            else:
                self.structure['git_history'] = []
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            self.structure['git_history'] = ["Git история недоступна"]
    
    def _walk_directory(self) -> None:
        """Рекурсивный обход директории проекта"""
        for root, dirs, files in os.walk(self.project_path):
            # Игнорируем служебные директории
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in [
                '__pycache__', 'venv', 'env', '.env', 'node_modules', 'dist', 'build'
            ]]
            
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    file_path = os.path.join(root, file)
                    self._analyze_python_file(file_path)
    
    def _analyze_python_file(self, file_path: str) -> None:
        """Анализ отдельного Python файла"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            relative_path = os.path.relpath(file_path, self.project_path)
            
            module_info = {
                'file_path': relative_path,
                'functions': [],
                'classes': [],
                'imports': [],
                'lines_of_code': len(content.splitlines())
            }
            
            # Анализ AST дерева
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_info = self._extract_function_info(node)
                    module_info['functions'].append(func_info)
                    self.structure['functions'].append({
                        **func_info,
                        'module': relative_path
                    })
                
                elif isinstance(node, ast.ClassDef):
                    class_info = self._extract_class_info(node)
                    module_info['classes'].append(class_info)
                    self.structure['classes'].append({
                        **class_info,
                        'module': relative_path
                    })
                
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    import_info = self._extract_import_info(node)
                    module_info['imports'].extend(import_info)
            
            self.structure['modules'].append(module_info)
            
        except SyntaxError as e:
            print(f"⚠️  Синтаксическая ошибка в файле {file_path}: {e}")
        except Exception as e:
            print(f"❌ Ошибка при анализе файла {file_path}: {e}")
    
    def _extract_function_info(self, node: ast.FunctionDef) -> Dict[str, Any]:
        """Извлечение информации о функции"""
        args = []
        for arg in node.args.args:
            args.append(arg.arg)
        
        # Обработка аргументов со значениями по умолчанию
        defaults = len(node.args.defaults) if node.args.defaults else 0
        
        # Извлечение docstring
        docstring = ast.get_docstring(node)
        
        # Извлечение декораторов
        decorators = []
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name):
                decorators.append(decorator.id)
            elif isinstance(decorator, ast.Attribute):
                decorators.append(decorator.attr)
            elif isinstance(decorator, ast.Call):
                if isinstance(decorator.func, ast.Name):
                    decorators.append(decorator.func.id)
        
        return {
            'name': node.name,
            'args': args,
            'defaults_count': defaults,
            'docstring': docstring,
            'lineno': node.lineno,
            'decorators': decorators
        }
    
    def _extract_class_info(self, node: ast.ClassDef) -> Dict[str, Any]:
        """Извлечение информации о классе"""
        methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                methods.append(self._extract_function_info(item))
        
        docstring = ast.get_docstring(node)
        
        # Обработка базовых классов
        bases = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                bases.append(base.attr)
        
        return {
            'name': node.name,
            'methods': methods,
            'docstring': docstring,
            'lineno': node.lineno,
            'bases': bases
        }
    
    def _extract_import_info(self, node) -> List[str]:
        """Извлечение информации об импортах"""
        imports = []
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
                self.structure['dependencies'].add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            module = node.module
            if module:
                self.structure['dependencies'].add(module.split('.')[0])
                for alias in node.names:
                    full_name = f"{module}.{alias.name}" if module != '.' else alias.name
                    imports.append(full_name)
        
        return imports
    
    def _generate_dependencies(self) -> None:
        """Генерация списка зависимостей"""
        # Фильтрация стандартных библиотек
        stdlib = {
            'os', 'sys', 'json', 'datetime', 'typing', 'ast', 'subprocess', 
            'inspect', 'logging', 'argparse', 'asyncio', 'pathlib'
        }
        self.structure['dependencies'] = list(self.structure['dependencies'] - stdlib)
    
    def generate_markdown_docs(self, output_dir: str) -> None:
        """Генерация Markdown документации"""
        os.makedirs(output_dir, exist_ok=True)
        
        self._generate_readme(output_dir)
        self._generate_api_reference(output_dir)
        self._generate_changelog(output_dir)
        self._generate_requirements(output_dir)
        
        print(f"📄 Markdown документация создана в {output_dir}/")
    
    def _generate_readme(self, output_dir: str) -> None:
        """Генерация README.md"""
        project_name = self.structure['project_info']['name']
        
        total_lines = sum(m.get('lines_of_code', 0) for m in self.structure['modules'])
        
        readme_content = f"{project_name.title()}"