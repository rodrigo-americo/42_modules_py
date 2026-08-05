# 42 Python Modules — Study Kit

Estudo pessoal dos Python Modules da 42 (piscine), por hobby. **Não é entregue
para pares** — os exercícios aqui não seguem o fluxo oficial de correção da 42.

## Ambiente

- Python 3.10+ (fixado via [uv](https://docs.astral.sh/uv/) — ver `.python-version`)
- Lint: [flake8](https://flake8.pycqa.org/), config em `.flake8`

```bash
uv sync              # cria .venv e instala dependências de dev
uv run flake8 .      # roda o lint no projeto inteiro
uv run flake8 module00/ex0/  # roda o lint num exercício específico
```

## Estrutura

```
module00/
  py0.pdf        # subject original (nunca versionado — ver .gitignore)
  mainpy0.py     # helper de teste fornecido pela 42, específico deste module
  exN/
    ft_*.py      # solução de cada exercício
```

Cada module novo segue o mesmo padrão: subject em PDF (ignorado pelo git),
exercícios em pastas `exN/`, um arquivo por função pedida.

## Assistência de IA

As regras de como a IA deve me ajudar a estudar (nunca gerar solução completa
de exercício avaliativo, sempre ler o subject de verdade antes de explicar,
etc.) estão em [`CLAUDE.md`](CLAUDE.md) e `.claude/`. Isso é o meu próprio
protocolo de estudo — o subject oficial da 42 também tem uma seção "AI
Instructions" (ver `py0.pdf`) que resume o espírito: usar IA para reduzir
tarefas repetitivas e aprender a fazer prompts melhores, nunca para gerar
código que eu não conseguiria explicar sozinho.

## Glossário

Termos recorrentes entre módulos: [`.claude/GLOSSARY.md`](.claude/GLOSSARY.md).
