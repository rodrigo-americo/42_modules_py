# module04 — Data Archivist: Digital Preservation in the Cyber Archives

Material de estudo (TL;DR + aprofundamento por conceito): [`concept.md`](concept.md).

## Exercícios

| Dir  | Função                    | Conceito principal                                              |
|------|---------------------------|-------------------------------------------------------------------|
| ex0  | `ft_ancient_text`         | `open()`, leitura de arquivo, `try`/`except OSError`               |
| ex1  | `ft_archive_creation`     | escrita de arquivo, transformar conteúdo, `input()`                |
| ex2  | `ft_stream_management`    | `sys.stdin`/`sys.stdout`/`sys.stderr` em vez de `input()`/`print()` |
| ex3  | `ft_vault_security`       | `with` (context manager), função `secure_archive()`                |

Cada exercício é um arquivo independente (só ele é submetido) — por isso
`ex1` retoma o código do `ex0`, `ex2` retoma o de `ex1`, e assim por diante,
cada um copiado e adaptado dentro do próprio arquivo, não importado entre
pastas.

## Restrição do subject: `with` só a partir do ex3

O subject proíbe explicitamente o uso do `with` statement antes do
exercício 3 — `ex0`, `ex1` e `ex2` devem abrir e fechar arquivos manualmente
(`f = open(...)` seguido de `f.close()`). Isso é proposital: o objetivo é
entender o que o `with` está automatizando (fechamento garantido mesmo em
erro) antes de passar a usá-lo.

## Rodando

```bash
uv run flake8 module04/         # lint em todo o módulo
uv run mypy module04/           # type check
uv run python module04/ex0/ft_ancient_text.py algum_arquivo.txt
```

`ex1` e `ex2` pedem um nome de arquivo para salvar (via `input()` ou via
`sys.stdin`) — rodar sem fornecer isso interativamente vai parar esperando
digitação no terminal.
