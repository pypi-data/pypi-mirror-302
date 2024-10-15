import os
import sys
import pyperclip
import argparse
from io import StringIO
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLabel, QFileDialog, QMessageBox, QCheckBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import yaml
from yaml import SafeDumper
from yaml.representer import SafeRepresenter

# Configuração para lidar com multiline strings no YAML
class LiteralScalarString(str):
    pass

def represent_literal(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')

SafeDumper.add_representer(LiteralScalarString, represent_literal)

def makeFastCodePrompts(root_path):
    """
    Recursively traverses all directories starting from root_path,
    collects .py files, and constructs a nested YAML structure where
    keys are directories and files, and values are the contents of the .py files.

    Args:
        root_path (str): Root path to start the search.

    Returns:
        str: String representation of the generated YAML.
    """
    yaml_structure = {}

    for current_dir, dirs, files in os.walk(root_path):
        # Determine the relative part of the current directory with respect to root_path
        relative_dir = os.path.relpath(current_dir, root_path)
        if relative_dir == ".":
            relative_dir = ""

        # Navigate the dictionary structure to insert files
        current_level = yaml_structure
        if relative_dir:
            for part in relative_dir.split(os.sep):
                current_level = current_level.setdefault(part, {})

        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(current_dir, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                except Exception as e:
                    print(f"⚠️ Erro ao ler {file_path}: {e}")
                    content = ""

                # Use the filename without extension as the key
                file_key = os.path.splitext(file)[0]

                # Wrap content with LiteralScalarString for block style
                current_level[file_key] = LiteralScalarString(content)
    yaml_output = StringIO()
    yaml.dump(yaml_structure, yaml_output, Dumper=SafeDumper, default_flow_style=False, allow_unicode=True)
    return yaml_output.getvalue()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gerador de Prompts de Código Rápido")
        self.setGeometry(100, 100, 800, 600)  # x, y, width, height
        self.setWindowIcon(QIcon())  # Você pode definir um ícone se desejar

        self.current_theme = "light"  # Tema padrão

        self.init_ui()
        self.apply_system_theme()

    def init_ui(self):
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Layout de seleção de diretório
        dir_layout = QHBoxLayout()
        self.dir_label = QLabel("Diretório Raiz:")
        self.dir_path = QTextEdit()
        self.dir_path.setFixedHeight(30)
        self.dir_path.setPlaceholderText("Selecione o diretório raiz contendo seus arquivos...")
        self.dir_path.setReadOnly(True)
        self.browse_button = QPushButton("Procurar")
        self.browse_button.clicked.connect(self.browse_directory)

        dir_layout.addWidget(self.dir_label)
        dir_layout.addWidget(self.dir_path)
        dir_layout.addWidget(self.browse_button)

        main_layout.addLayout(dir_layout)

        # Layout para comandos do usuário
        command_layout = QHBoxLayout()
        self.command_label = QLabel("Comandos do Usuário:")
        self.command_input = QTextEdit()
        self.command_input.setFixedHeight(100)
        self.command_input.setPlaceholderText("Insira seus comandos aqui...")

        command_layout.addWidget(self.command_label)
        command_layout.addWidget(self.command_input)

        main_layout.addLayout(command_layout)

        # Botão de execução
        self.execute_button = QPushButton("Gerar Prompt")
        self.execute_button.clicked.connect(self.generate_prompt)
        main_layout.addWidget(self.execute_button)

        # Exibição do prompt
        self.prompt_display = QTextEdit()
        self.prompt_display.setReadOnly(True)
        main_layout.addWidget(self.prompt_display)

        # Layout inferior para temas e copiar
        bottom_layout = QHBoxLayout()

        # Toggle de tema
        self.theme_toggle = QCheckBox("Modo Escuro")
        self.theme_toggle.stateChanged.connect(self.toggle_theme)
        bottom_layout.addWidget(self.theme_toggle)

        # Espaçador
        bottom_layout.addStretch()

        # Botão para copiar para a área de transferência
        self.copy_button = QPushButton("Copiar para Área de Transferência")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        bottom_layout.addWidget(self.copy_button)

        main_layout.addLayout(bottom_layout)

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Selecionar Diretório Raiz", os.getcwd())
        if directory:
            self.dir_path.setText(directory)

    def generate_prompt(self):
        root_directory = self.dir_path.toPlainText().strip()
        if not root_directory:
            QMessageBox.warning(self, "Erro de Entrada", "Por favor, selecione um diretório raiz.")
            return

        if not os.path.isdir(root_directory):
            QMessageBox.warning(self, "Erro de Entrada", "O caminho selecionado não é um diretório válido.")
            return

        user_commands = self.command_input.toPlainText().strip()
        if not user_commands:
            QMessageBox.warning(self, "Erro de Entrada", "Por favor, insira os comandos do usuário.")
            return

        try:
            yaml_result = makeFastCodePrompts(root_directory)

            prompt = f"CONTEXTO DO MEU CÓDIGO:\n\n{yaml_result}\n\n\nPROMPT:\n\n" + user_commands
            self.prompt_display.setPlainText(prompt)

            # Copiar para a área de transferência
            try:
                pyperclip.copy(prompt)
                QMessageBox.information(self, "Sucesso", "✅ Prompt copiado para a área de transferência! 🎉")
            except pyperclip.PyperclipException as e:
                QMessageBox.warning(self, "Erro de Área de Transferência", f"⚠️ Não foi possível copiar o prompt: {e}")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro: {e}")

    def toggle_theme(self, state):
        if state == Qt.Checked:
            self.apply_dark_theme()
            self.current_theme = "dark"
        else:
            self.apply_light_theme()
            self.current_theme = "light"

    def apply_dark_theme(self):
        dark_stylesheet = """
            QWidget {
                background-color: #2e2e2e;
                color: #f0f0f0;
            }
            QPushButton {
                background-color: #444444;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
            QTextEdit, QLineEdit {
                background-color: #3e3e3e;
                color: #f0f0f0;
            }
            QLabel {
                color: #f0f0f0;
            }
            QCheckBox {
                color: #f0f0f0;
            }
        """
        self.setStyleSheet(dark_stylesheet)

    def apply_light_theme(self):
        light_stylesheet = """
            QWidget {
                background-color: #f0f0f0;
                color: #2e2e2e;
            }
            QPushButton {
                background-color: #e0e0e0;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            QTextEdit, QLineEdit {
                background-color: #ffffff;
                color: #2e2e2e;
            }
            QLabel {
                color: #2e2e2e;
            }
            QCheckBox {
                color: #2e2e2e;
            }
        """
        self.setStyleSheet(light_stylesheet)

    def apply_system_theme(self):
        # Tentativa de detectar o tema do sistema (claro/escuro)
        if sys.platform == "win32":
            try:
                import winreg

                registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
                key_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
                key = winreg.OpenKey(registry, key_path)
                # 0 = Dark mode, 1 = Light mode
                value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                if value == 0:
                    self.apply_dark_theme()
                    self.current_theme = "dark"
                else:
                    self.apply_light_theme()
                    self.current_theme = "light"
                winreg.CloseKey(key)
            except Exception as e:
                print(f"⚠️ Não foi possível detectar o tema do sistema: {e}")
                self.apply_light_theme()
        else:
            # Para outros sistemas operacionais, padrão para tema claro
            self.apply_light_theme()

    def copy_to_clipboard(self):
        prompt_text = self.prompt_display.toPlainText()
        if prompt_text:
            QApplication.clipboard().setText(prompt_text)
            QMessageBox.information(self, "Copiado", "✅ Prompt copiado para a área de transferência!")
        else:
            QMessageBox.warning(self, "Sem Conteúdo", "⚠️ Não há nenhum prompt para copiar.")


def run_cli_mode():
    """
    Executa a lógica da aplicação via linha de comando de forma interativa.
    """
    parser = argparse.ArgumentParser(description="Gerador de Prompts de Código Rápido - Modo CLI")
    parser.add_argument('--root', type=str, help='Caminho do diretório raiz contendo arquivos Python')
    parser.add_argument('--commands', type=str, help='Comandos do usuário a serem incluídos no prompt')

    args = parser.parse_args()

    # Inicializar root_directory
    root_directory = args.root.strip() if args.root else None

    # Validar root_directory se fornecido via argumento
    if root_directory:
        if not os.path.isdir(root_directory):
            print("⚠️ Erro: O caminho fornecido não é um diretório válido.")
            sys.exit(1)
    else:
        # Solicitar diretório raiz
        while True:
            root_directory = input("Digite o caminho do diretório raiz contendo seus arquivos Python: ").strip()
            if not root_directory:
                print("⚠️ Erro: Diretório raiz não fornecido.")
                continue
            if not os.path.isdir(root_directory):
                print("⚠️ Erro: O caminho fornecido não é um diretório válido.")
                continue
            break

    while True:
        # Obter comandos do usuário
        if args.commands:
            user_commands = args.commands.strip()
        else:
            print("Digite seus comandos do usuário (pressione Enter duas vezes para finalizar):")
            user_commands_lines = []
            while True:
                line = input()
                if line == "":
                    break
                user_commands_lines.append(line)
            user_commands = "\n".join(user_commands_lines).strip()

        if not user_commands:
            print("⚠️ Erro: Comandos do usuário não fornecidos.")
            if args.commands:
                sys.exit(1)
            else:
                continue

        try:
            yaml_result = makeFastCodePrompts(root_directory)
            prompt = f"CONTEXTO DO MEU CÓDIGO:\n\n{yaml_result}\n\n\nPROMPT:\n\n" + user_commands

            # Copiar para a área de transferência
            try:
                pyperclip.copy(prompt)
                print("✅ Prompt copiado para a área de transferência! 🎉")
            except pyperclip.PyperclipException as e:
                print(f"⚠️ Não foi possível copiar o prompt para a área de transferência: {e}")

            # Perguntar ao usuário se deseja gerar outro prompt
            while True:
                choice = input("Deseja gerar outro prompt? (s/n): ").strip().lower()
                if choice == 's':
                    # Perguntar se deseja alterar o diretório raiz
                    change_dir = input("Deseja alterar o diretório raiz? (s/n): ").strip().lower()
                    if change_dir == 's':
                        while True:
                            new_root = input("Digite o novo caminho do diretório raiz contendo seus arquivos Python: ").strip()
                            if not new_root:
                                print("⚠️ Erro: Diretório raiz não fornecido.")
                                continue
                            if not os.path.isdir(new_root):
                                print("⚠️ Erro: O caminho fornecido não é um diretório válido.")
                                continue
                            root_directory = new_root
                            break
                    # Resetar comandos se não forem fornecidos via argumentos
                    if not args.commands:
                        args.commands = None
                    break
                elif choice == 'n':
                    print("Encerrando a aplicação. Até mais! 👋")
                    sys.exit(0)
                else:
                    print("Por favor, responda com 's' para sim ou 'n' para não.")

        except Exception as e:
            print(f"⚠️ Ocorreu um erro: {e}")
            sys.exit(1)


def run_gui_mode():
    """
    Executa a aplicação no modo UI.
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


class GetContext:
    def __init__(self, ui=False):
        if ui:
            # Modo UI
            run_gui_mode()
        else:
            # Modo CLI
            run_cli_mode()



