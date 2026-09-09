"""construct.py - diagnostico de virtual environment.

Responde "estou dentro ou fora de um venv?" e imprime saidas
diferentes para cada caso.
"""

import os
import site
import sys


def in_virtualenv() -> bool:
    """True se o interpretador atual roda dentro de um virtual environment."""
    return sys.prefix != sys.base_prefix or hasattr(sys, "real_prefix")


def python_version() -> str:
    """Versao curta do Python em uso, ex: '3.13'."""
    return f"{sys.version_info.major}.{sys.version_info.minor}"


def site_packages_path() -> str:
    """Diretorio onde 'pip install' colocaria pacotes neste ambiente."""
    return site.getsitepackages()[-1]


def report_outside() -> None:
    """Saida quando NAO ha venv: aviso + instrucoes de criacao/ativacao."""
    text: str = (
        "MATRIX STATUS: You're still plugged in\n"
        "\n"
        f"Current Python: {sys.executable}\n"
        "Virtual Environment: None detected\n"
        "\n"
        "WARNING: You're in the global environment!\n"
        "The machines can see everything you install.\n"
        "\n"
        "To enter the construct, run:\n"
        "python -m venv matrix_env\n"
        "source matrix_env/bin/activate # On Unix\n"
        "matrix_env\\Scripts\\activate # On Windows\n"
        "\n"
        "Then run this program again.\n"
        "\n"
        f"Global packages would go to: {site_packages_path()}"
    )
    print(text)


def report_inside() -> None:
    """Saida quando HA venv: detalhes do ambiente isolado."""
    text: str = (
        "MATRIX STATUS: Welcome to the construct\n"
        "\n"
        f"Current Python: {sys.executable}\n"
        f"Virtual Environment: {os.path.basename(sys.prefix)}\n"
        f"Environment Path: {sys.prefix}\n"
        "\n"
        "SUCCESS: You're in an isolated environment!\n"
        "Safe to install packages without affecting\n"
        "the global system.\n"
        "\n"
        "Package installation path:\n"
        f"{site_packages_path()}\n"
        "\n"
        f"(Global would instead be under: {sys.base_prefix})"
    )
    print(text)


def main() -> None:
    """Decide qual relatorio imprimir com base na deteccao de venv."""
    if in_virtualenv():
        report_inside()
    else:
        report_outside()


if __name__ == "__main__":
    main()
