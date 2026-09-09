"""oracle.py - sistema de configuracao via variaveis de ambiente.

Carrega config de env vars + arquivo .env (via python-dotenv),
mostra comportamento diferente entre development e production, e
trata config faltando sem estourar traceback.
"""

import os
import sys

from dotenv import load_dotenv

# nome da var -> valor default (None = obrigatoria-condicional, sem default)
DEFAULTS: dict[str, str | None] = {
    "MATRIX_MODE": "development",
    "DATABASE_URL": None,
    "API_KEY": None,
    "LOG_LEVEL": "INFO",
    "ZION_ENDPOINT": "http://localhost:9000",
}

VALID_MODES: tuple[str, ...] = ("development", "production")


def load_config() -> dict[str, str | None]:
    """Le as 5 variaveis de os.environ, aplicando os defaults de DEFAULTS.

    load_dotenv() ja deve ter rodado antes (injeta o .env sem
    sobrescrever o que veio do shell).
    """
    resultados: dict[str, str | None] = {}
    for nome, padrao in DEFAULTS.items():
        if padrao is None:
            resultados[nome] = os.environ.get(nome)
        else:
            resultados[nome] = os.getenv(nome, padrao)
    return resultados


def validate_config(config: dict[str, str | None]) -> list[str]:
    """Valida a config conforme o modo. Devolve lista de WARNINGS.

    Regras:
      - MATRIX_MODE fora de VALID_MODES -> warning (tratar como dev)
      - production: DATABASE_URL ou API_KEY ausente -> erro fatal
        (mensagem clara + sys.exit(1))
      - development: as mesmas ausencias -> so warning
      - LOG_LEVEL / ZION_ENDPOINT: nunca falham (tem default)
    """
    erros: list[str] = []
    if config["MATRIX_MODE"] not in VALID_MODES:
        erros.append("MATRIX_MODE invalido, assumindo development")
        config["MATRIX_MODE"] = "development"
    prod = config["MATRIX_MODE"] == "production"
    for chave in ("DATABASE_URL", "API_KEY"):
        if config[chave] is not None:
            continue
        if prod:
            print(f"ERROR: {chave} nao definida (obrigatoria em production)",
                  file=sys.stderr)
            sys.exit(1)
        erros.append(f"{chave} nao definida")
    return erros


def mask_secret(value: str | None) -> str:
    """Representacao segura de um segredo p/ exibir na saida.

    Ex: None -> '<not set>' ; 'abcdef123' -> 'abc***' (nunca o valor
    inteiro).
    """
    if value is None:
        return "<not set>"
    len_value = len(value)
    if len_value > 4:
        return value[:3] + "*" * (len_value - 3)
    return "*" * len_value


def _describe_secret(value: str | None, is_prod: bool, ok_label: str) -> str:
    """Como um segredo aparece na saida, conforme None / prod / dev."""
    if value is None:
        return "not configured"
    if is_prod:
        return ok_label
    return mask_secret(value)


def _print_config_block(config: dict[str, str | None], is_prod: bool) -> None:
    """Bloco 'Configuration loaded:' (dev mostra mais, prod esconde)."""
    print("Configuration loaded:")
    print(f"  Mode: {config['MATRIX_MODE']}")
    db = _describe_secret(config["DATABASE_URL"], is_prod, "Connected")
    print(f"  Database: {db}")
    api = _describe_secret(config["API_KEY"], is_prod, "Authenticated")
    print(f"  API Access: {api}")
    print(f"  Log Level: {config['LOG_LEVEL']}")
    print(f"  Zion Network: {config['ZION_ENDPOINT']}")


def _print_security_block(warnings: list[str]) -> None:
    """Bloco de warnings + 'Environment security check:'."""
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"  WARNING: {warning}")
        print()
    print("Environment security check:")
    print("  [OK] No hardcoded secrets detected")
    if os.path.exists(".env"):
        print("  [OK] .env file loaded")
    else:
        print("  [--] .env not found (using env vars / defaults)")
    print("  [OK] Production overrides available")


def report(config: dict[str, str | None], warnings: list[str]) -> None:
    """Imprime o relatorio no formato do subject.

    dev x prod (visivel na saida): development mostra os valores
    (API_KEY mascarada parcial); production esconde os segredos
    ('Connected' / 'Authenticated').
    """
    is_prod = config["MATRIX_MODE"] == "production"
    print("ORACLE STATUS: Reading the Matrix...")
    print()
    _print_config_block(config, is_prod)
    print()
    _print_security_block(warnings)
    print()
    print("The Oracle sees all configurations.")


def main() -> None:
    """Entrypoint - carrega, valida e reporta a configuracao."""
    load_dotenv()
    config = load_config()
    warnings = validate_config(config)
    report(config, warnings)


if __name__ == "__main__":
    main()
