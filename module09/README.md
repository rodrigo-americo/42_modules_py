# module09 — Cosmic Data: Discover Pydantic Models & Validation

Material de estudo (TL;DR + aprofundamento por conceito): [`concept.md`](concept.md).

## Estrutura

O subject não desenha uma árvore de arquivos explícita — cada capítulo de
exercício só define o diretório (`ex0/`, `ex1/`, `ex2/`) e o arquivo a
submeter. Os três exercícios são independentes: nenhum importa código de
outro, mas cada um reaproveita conceitos do anterior.

```
module09/
├── ex0/
│   └── space_station.py     # BaseModel + Field: constraints de tamanho/faixa, datetime, Optional
├── ex1/
│   └── alien_contact.py     # Enum + @model_validator(mode="after"): regras entre campos
└── ex2/
    └── space_crew.py        # modelos aninhados: SpaceMission contém List[CrewMember]
```

`pyproject.toml` e `uv.lock` declaram a única dependência (`pydantic>=2.13`)
de forma reproduzível — equivalente ao `requirements.txt` que o subject
menciona. O `.venv/` fica fora do repositório (`.gitignore` na raiz).
`data_generator.py`, `data_exporter.py` e `generated_data/` são ferramentas
de apoio fornecidas com o subject.

## Partes do subject

| Exercício | Arquivo | Conceito principal |
|-----------|---------|---------------------|
| ex0 — Space Station Data | `space_station.py` | *validação de campo*: um modelo `BaseModel` onde cada campo carrega suas próprias regras via `Field` (comprimento de string, faixa numérica), coerção automática de tipos (string ISO → `datetime`), campo `Optional` com default |
| ex1 — Alien Contact Logs | `alien_contact.py` | *validação entre campos*: um `Enum` para um conjunto fechado de valores + `@model_validator(mode="after")` para regras de negócio que dependem de mais de um campo ao mesmo tempo |
| ex2 — Space Crew Management | `space_crew.py` | *modelos aninhados*: um campo cujo tipo é outro modelo (`List[CrewMember]`); o Pydantic valida cada item recursivamente antes do `@model_validator` da missão, que agrega sobre a lista inteira |

## Rodando

```bash
uv run python module09/ex0/space_station.py
uv run python module09/ex1/alien_contact.py
uv run python module09/ex2/space_crew.py
```

Cada `main()` cria uma instância válida (imprime os dados no formato do
"Expected Output" do subject) e depois tenta uma instância inválida dentro
de `try/except ValidationError`, imprimindo a mensagem de erro que o
Pydantic gera.

```bash
uv run --with flake8 --with mypy flake8 module09/ex0 module09/ex1 module09/ex2
uv run --with mypy mypy module09/ex0/space_station.py \
    module09/ex1/alien_contact.py module09/ex2/space_crew.py
```

Os três exercícios ficam limpos em `flake8` e `mypy`. O subject exige
Python 3.10+ e Pydantic 2.x; o ambiente foi testado em Python 3.12.3 com
`pydantic 2.13.5`.
