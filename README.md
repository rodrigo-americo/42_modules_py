# 42 Python Modules — Study Kit

Estudo pessoal dos Python Modules da 42, por hobby. **Não é entregue para
pares** — os exercícios aqui não seguem o fluxo oficial de correção da 42.

## Ambiente

- Python 3.10+ (fixado via [uv](https://docs.astral.sh/uv/) — ver `.python-version`)
- Lint: [flake8](https://flake8.pycqa.org/), config em `.flake8`
- Type checking: [mypy](https://mypy-lang.org/) (exigido a partir do módulo00
  ex7, que introduz type hints obrigatórios)

```bash
uv sync              # cria .venv e instala dependências de dev
uv run flake8 .      # roda o lint no projeto inteiro
uv run flake8 module00/ex0/  # roda o lint num exercício específico
uv run mypy module00/ex7/    # checa tipagem de um exercício específico
```

## Módulos

| Módulo | Tema | Material de estudo |
|--------|------|---------------------|
| [module00](module00/) | Growing Code — fundamentos de Python | [concept.md](module00/concept.md) |
| [module01](module01/) | Code Cultivation — POO: classes, herança, encapsulamento | [concept.md](module01/concept.md) |
| [module02](module02/) | Garden Guardian — tratamento de exceções | [concept.md](module02/concept.md) |
| [module03](module03/) | Data Quest — coleções (list, tuple, set, dict, generators) | [concept.md](module03/concept.md) |
| [module04](module04/) | Data Archivist — arquivos, serialização, preservação digital | [concept.md](module04/concept.md) |
| [module05](module05/) | Code Nexus — polimorfismo, `ABC`, `Protocol` | [concept.md](module05/concept.md) |
| [module06](module06/) | The Codex — sistema de import do Python, pacotes | [concept.md](module06/concept.md) |
| [module07](module07/) | DataDeck — herança múltipla, arquitetura abstrata | [concept.md](module07/concept.md) |
| [module08](module08/) | The Matrix — venvs, dependências, config por variáveis de ambiente | [concept.md](module08/concept.md) |
| [module09](module09/) | Cosmic Data — Pydantic v2, validação de modelos | [concept.md](module09/concept.md) |
| [module10](module10/) | FuncMage — programação funcional: lambdas, closures, `functools`, decorators | [concept.md](module10/concept.md) |

Cada module tem seu próprio `README.md` com a tabela de exercícios e comandos
de execução, e um `concept.md` com o material de estudo (TL;DR + aprofundamento
por conceito).

## Estrutura

```
module00/
  mainpy0.py     # helper de teste fornecido pela 42, específico deste module
  exN/
    ft_*.py      # solução de cada exercício
```

Cada module segue o mesmo padrão: subject original em PDF (nunca versionado —
ver `.gitignore`), exercícios em pastas `exN/`, um arquivo por função pedida.

## Assistência de IA

As regras de como a IA deve me ajudar a estudar (nunca gerar solução completa
de exercício avaliativo, sempre ler o subject de verdade antes de explicar,
etc.) estão em [`CLAUDE.md`](CLAUDE.md) e `.claude/`. Isso é o meu próprio
protocolo de estudo — o subject oficial da 42 também tem uma seção "AI
Instructions" que resume o espírito: usar IA para reduzir tarefas repetitivas
e aprender a fazer prompts melhores, nunca para gerar código que eu não
conseguiria explicar sozinho.

## Glossário

Termos recorrentes entre módulos: [`.claude/GLOSSARY.md`](.claude/GLOSSARY.md).
