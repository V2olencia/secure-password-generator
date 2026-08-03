import math
import secrets
import string
import subprocess
import sys
from datetime import datetime
from pathlib import Path


VERSION = "2.0"
DEFAULT_OUTPUT_FILE = "senhas_geradas.txt"
CONFUSING_CHARACTERS = set("O0Il")


settings = {
    "length": 12,
    "include_symbols": True,
    "exclude_confusing": True,
    "quantity": 1,
    "auto_copy": False,
    "output_file": DEFAULT_OUTPUT_FILE,
}

history = []


def clear_screen():
    print("\n" * 2)


def pause():
    input("\nPressione Enter para continuar...")


def show_header():
    print("=" * 35)
    print(f" Password Generator v{VERSION}")
    print("=" * 35)


def show_menu():
    clear_screen()
    show_header()
    print("1 - Gerar senha")
    print("2 - Salvar em arquivo")
    print("3 - Ver historico")
    print("4 - Copiar para area de transferencia")
    print("5 - Configuracoes")
    print("0 - Sair")


def build_character_pool():
    characters = string.ascii_letters + string.digits

    if settings["include_symbols"]:
        characters += "!@#$%^&*()-_=+[]{};:,.<>?/"

    if settings["exclude_confusing"]:
        characters = "".join(
            character for character in characters if character not in CONFUSING_CHARACTERS
        )

    return characters


def get_required_groups():
    groups = [string.ascii_lowercase, string.ascii_uppercase, string.digits]

    if settings["include_symbols"]:
        groups.append("!@#$%^&*()-_=+[]{};:,.<>?/")

    if settings["exclude_confusing"]:
        groups = [
            "".join(character for character in group if character not in CONFUSING_CHARACTERS)
            for group in groups
        ]

    return [group for group in groups if group]


def generate_password():
    characters = build_character_pool()
    groups = get_required_groups()
    length = max(settings["length"], len(groups))

    password_characters = [secrets.choice(group) for group in groups]

    while len(password_characters) < length:
        password_characters.append(secrets.choice(characters))

    secrets.SystemRandom().shuffle(password_characters)
    return "".join(password_characters)


def calculate_strength(password):
    pool_size = 0

    if any(character.islower() for character in password):
        pool_size += 26
    if any(character.isupper() for character in password):
        pool_size += 26
    if any(character.isdigit() for character in password):
        pool_size += 10
    if any(character in string.punctuation for character in password):
        pool_size += len(string.punctuation)

    entropy = len(password) * math.log2(pool_size) if pool_size else 0

    if entropy >= 90:
        return "Muito forte", entropy
    if entropy >= 70:
        return "Forte", entropy
    if entropy >= 50:
        return "Media", entropy
    return "Fraca", entropy


def generate_passwords():
    passwords = []

    for _ in range(settings["quantity"]):
        password = generate_password()
        strength, entropy = calculate_strength(password)
        passwords.append(
            {
                "password": password,
                "strength": strength,
                "entropy": entropy,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    history.extend(passwords)
    return passwords


def show_generated_passwords(passwords):
    print("\nSenhas geradas:\n")

    for index, item in enumerate(passwords, start=1):
        print(
            f"{index}. {item['password']} "
            f"({item['strength']} - {item['entropy']:.1f} bits)"
        )


def option_generate_passwords():
    passwords = generate_passwords()
    show_generated_passwords(passwords)

    if settings["auto_copy"]:
        copied = copy_text_to_clipboard(passwords[-1]["password"])
        if copied:
            print("\nUltima senha copiada automaticamente.")
        else:
            print("\nNao foi possivel copiar automaticamente neste sistema.")

    pause()


def save_passwords_to_file(passwords):
    if not passwords:
        return False

    output_path = Path(settings["output_file"])

    with output_path.open("a", encoding="utf-8") as file:
        file.write(f"\n--- Senhas geradas em {datetime.now():%Y-%m-%d %H:%M:%S} ---\n")

        for item in passwords:
            file.write(
                f"{item['password']} | Forca: {item['strength']} "
                f"| Entropia: {item['entropy']:.1f} bits\n"
            )

    return True


def option_save_to_file():
    if not history:
        print("\nNenhuma senha foi gerada ainda.")
        pause()
        return

    if save_passwords_to_file(history):
        print(f"\nHistorico salvo em: {Path(settings['output_file']).resolve()}")
    else:
        print("\nNao ha senhas para salvar.")

    pause()


def option_show_history():
    if not history:
        print("\nHistorico vazio.")
        pause()
        return

    print("\nHistorico:\n")

    for index, item in enumerate(history, start=1):
        print(
            f"{index}. {item['password']} | {item['strength']} "
            f"| {item['entropy']:.1f} bits | {item['created_at']}"
        )

    pause()


def copy_text_to_clipboard(text):
    commands = []

    if sys.platform == "darwin":
        commands.append(["pbcopy"])
    elif sys.platform.startswith("win"):
        commands.append(["clip"])
    else:
        commands.extend([["xclip", "-selection", "clipboard"], ["xsel", "--clipboard"]])

    for command in commands:
        try:
            subprocess.run(
                command,
                input=text,
                text=True,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            continue

    return False


def option_copy_to_clipboard():
    if not history:
        print("\nNenhuma senha foi gerada ainda.")
        pause()
        return

    latest_password = history[-1]["password"]

    if copy_text_to_clipboard(latest_password):
        print("\nUltima senha copiada para a area de transferencia.")
    else:
        print("\nNao foi possivel copiar neste sistema.")

    pause()


def ask_integer(prompt, minimum, maximum=None):
    while True:
        value = input(prompt).strip()

        try:
            number = int(value)
        except ValueError:
            print("Digite um numero valido.")
            continue

        if number < minimum:
            print(f"Digite um numero maior ou igual a {minimum}.")
            continue

        if maximum is not None and number > maximum:
            print(f"Digite um numero menor ou igual a {maximum}.")
            continue

        return number


def ask_yes_or_no(prompt):
    while True:
        value = input(f"{prompt} (s/n): ").strip().lower()

        if value in ("s", "sim"):
            return True
        if value in ("n", "nao", "não"):
            return False

        print("Responda com s ou n.")


def option_settings():
    clear_screen()
    show_header()
    print("Configuracoes atuais:\n")
    print(f"Tamanho da senha: {settings['length']}")
    print(f"Quantidade por vez: {settings['quantity']}")
    print(f"Incluir simbolos: {'sim' if settings['include_symbols'] else 'nao'}")
    print(
        "Excluir caracteres confusos: "
        f"{'sim' if settings['exclude_confusing'] else 'nao'}"
    )
    print(f"Copiar automaticamente: {'sim' if settings['auto_copy'] else 'nao'}")
    print(f"Arquivo de saida: {settings['output_file']}")
    print()

    settings["length"] = ask_integer("Novo tamanho da senha (minimo 4): ", 4, 128)
    settings["quantity"] = ask_integer("Quantas senhas gerar por vez (1 a 100): ", 1, 100)
    settings["include_symbols"] = ask_yes_or_no("Incluir simbolos")
    settings["exclude_confusing"] = ask_yes_or_no("Excluir O, 0, I, l")
    settings["auto_copy"] = ask_yes_or_no("Copiar automaticamente a ultima senha")

    output_file = input(
        f"Arquivo para salvar senhas [{settings['output_file']}]: "
    ).strip()

    if output_file:
        settings["output_file"] = output_file

    print("\nConfiguracoes atualizadas.")
    pause()


def main():
    while True:
        show_menu()
        option = input("\nEscolha uma opcao: ").strip()

        if option == "1":
            option_generate_passwords()
        elif option == "2":
            option_save_to_file()
        elif option == "3":
            option_show_history()
        elif option == "4":
            option_copy_to_clipboard()
        elif option == "5":
            option_settings()
        elif option == "0":
            print("\nAte logo!")
            break
        else:
            print("\nOpcao invalida.")
            pause()


if __name__ == "__main__":
    main()
