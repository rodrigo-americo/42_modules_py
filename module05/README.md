# module05 — Code Nexus: Polymorphic Data Streams in the Digital Matrix

Material de estudo (TL;DR + aprofundamento por conceito): [`concept.md`](concept.md).

## Exercícios

| Dir  | Arquivo              | Conceito principal                                                        |
|------|-----------------------|-----------------------------------------------------------------------------|
| ex0  | `data_processor.py`   | `ABC`, `@abstractmethod`, method overriding, hierarquia de exceções         |
| ex1  | `data_stream.py`      | polymorphism (roteamento sem `isinstance`), estatísticas por processor      |
| ex2  | `data_pipeline.py`    | `Protocol` (duck typing estrutural), sistema de plugins de exportação       |

Cada exercício é um arquivo independente (só ele é submetido) — por isso
`ex1` retoma as classes do `ex0`, e `ex2` retoma as do `ex1`, cada uma
copiada e adaptada dentro do próprio arquivo, não importada entre pastas.

## Arquitetura em uma frase por exercício

- **ex0**: `DataProcessor(ABC)` define o contrato (`validate`/`ingest`
  abstratos, `output` concreto); `NumericProcessor`, `TextProcessor` e
  `LogProcessor` implementam esse contrato cada um à sua maneira.
- **ex1**: `DataStream` recebe uma lista heterogênea e, para cada elemento,
  pergunta a cada processor registrado "você aceita isso?" (`validate`) até
  achar um que aceite — sem nunca checar o tipo da classe manualmente.
- **ex2**: `ExportPlugin` é um `Protocol`, não uma superclasse — os plugins
  concretos (`CSVExportPlugin`, `JSONExportPlugin`) não herdam dele, só têm
  o método certo com a assinatura certa.

## Restrição do subject: só `abc` e `typing`

Os três exercícios autorizam apenas esses dois imports, além de builtins e
tipos/coleções padrão. Isso é proposital — força a solução a usar o
mecanismo de `ABC`/`Protocol` da própria linguagem em vez de qualquer
biblioteca de terceiros para "abstração".

## Rodando

```bash
uv run flake8 module05/         # lint em todo o módulo
uv run mypy module05/           # type check
uv run python module05/ex0/data_processor.py
uv run python module05/ex1/data_stream.py
uv run python module05/ex2/data_pipeline.py
```

O `ex0` deixa um `# type: ignore[arg-type]` proposital numa chamada de
`ingest` com tipo incompatível — é o próprio subject que pede esse teste,
para provar que a proteção em runtime (exceção) funciona mesmo quando a
checagem estática do `mypy` é contornada.
