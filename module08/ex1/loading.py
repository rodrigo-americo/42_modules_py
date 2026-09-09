import importlib.metadata
import sys

try:
    import numpy
except ImportError:
    numpy = None  # type: ignore[assignment]

try:
    import pandas
except ImportError:
    pandas = None  # type: ignore[assignment]

try:
    import matplotlib
    matplotlib.use("Agg")
except ImportError:
    matplotlib = None  # type: ignore[assignment]


# pacote -> (modulo importado ou None, descricao curta p/ a saida)
DEPENDENCIES: dict[str, tuple[object, str]] = {
    "numpy": (numpy, "Numerical computation"),
    "pandas": (pandas, "Data manipulation"),
    "matplotlib": (matplotlib, "Visualization"),
}

OUTPUT_IMAGE: str = "matrix_analysis.png"
N_POINTS: int = 1000


def package_version(name: str) -> str:
    """Versao instalada de `name`, ou '?' se nao encontrada."""
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return "?"


def check_dependencies() -> list[str]:
    """Imprime o status de cada dependencia e devolve a lista das ausentes.

    Formato por linha (ver subject):
      [OK] numpy (2.4.2) - Numerical computation ready
      [MISSING] matplotlib - run: pip install -r requirements.txt
    """
    missing: list[str] = []
    for name, (module, description) in DEPENDENCIES.items():
        if module is not None:
            version = package_version(name)
            print(f"[OK] {name} ({version}) - {description} ready")
        else:
            print(f"[MISSING] {name} - run: pip install -r requirements.txt")
            missing.append(name)
    return missing


def print_install_help() -> None:
    """Instrucoes de instalacao pelos dois caminhos (pip e Poetry)."""
    print("Missing dependencies. Install with one of:")
    print("  pip:    pip install -r requirements.txt")
    print("  Poetry: poetry install  (then: poetry run python loading.py)")


def generate_matrix_data() -> object:
    """Gera o dataset simulado da Matrix (fonte = numpy) como DataFrame.

    Regra do subject: os dados TEM que vir de numpy - nada de listas
    hardcoded nem range().
    """
    rng = numpy.random.default_rng(2)
    time_axis = numpy.linspace(0.0, 10.0, N_POINTS)
    signal = numpy.sin(time_axis) + rng.normal(0.0, 0.2, N_POINTS)
    return pandas.DataFrame({"time": time_axis, "signal": signal})


def analyze(df: object) -> object:
    """Roda uma analise real sobre o DataFrame e devolve o resultado.

    Ex: describe(), media movel (rolling), ou groupby por faixa.
    """
    df["rolling_mean"] = df["signal"].rolling(window=50).mean()
    df["rolling_std"] = df["signal"].rolling(window=50).std()
    return df


def make_visualization(df: object, path: str = OUTPUT_IMAGE) -> None:
    """Plota o DataFrame e salva em `path` (backend nao-interativo)."""
    from matplotlib import pyplot as plt
    plt.figure(figsize=(8, 5))
    plt.plot(df["time"], df["signal"], alpha=0.4, label="signal")
    plt.plot(df["time"], df["rolling_mean"], label="rolling_mean")
    plt.xlabel("time")
    plt.ylabel("signal")
    plt.title("Matrix Data Analysis")
    plt.legend()
    plt.savefig(path)
    plt.close()


def print_pip_vs_poetry() -> None:
    """Mostra na saida a diferenca entre pip e Poetry."""
    print("pip vs Poetry (mesmas libs, ferramentas diferentes):")
    print("  pip    -> le requirements.txt; lista 'flat' de pacotes;")
    print("            sem lockfile proprio das deps transitivas;")
    print("            instala no ambiente ativo (voce gere o venv).")
    print("  Poetry -> le pyproject.toml; grava poetry.lock com TODA")
    print("            a arvore transitiva travada por hash;")
    print("            cria e gerencia o venv do projeto sozinho.")
    print("  Neste ex: requirements.txt e pyproject.toml declaram")
    print("  exatamente as MESMAS libs, so em formatos distintos.")


def main() -> None:
    """Entrypoint - orquestra checagem, analise e visualizacao."""
    print("LOADING STATUS: Loading programs...")
    print()
    print("Checking dependencies:")
    missing = check_dependencies()
    if missing:
        print()
        print_install_help()
        sys.exit(1)

    print()
    print_pip_vs_poetry()

    print()
    print("Analyzing Matrix data...")
    data = generate_matrix_data()
    print(f"Processing {N_POINTS} data points...")
    analyze(data)

    print("Generating visualization...")
    make_visualization(data)

    print()
    print("Analysis complete!")
    print(f"Results saved to: {OUTPUT_IMAGE}")


if __name__ == "__main__":
    main()
