# Glossário

Termos que se repetem entre módulos. Cada `concept.md` pode linkar aqui na
primeira menção de um termo (ver `templates/concept.md`).

Formato: só as letras (`## A`, `## B`, ...) usam heading, como âncora de
navegação geral. Os termos em si ficam em texto normal com **negrito**,
precedidos de uma âncora HTML invisível (`<a id="...">`) que permite link direto
de outros arquivos sem virar um heading gigante no GitHub.

O `id` é o termo em minúsculas, espaços viram hífen, sem acentos nem parênteses
(ex: "annotation scope" → `annotation-scope`).

---

## B

<a id="bytecode"></a>**bytecode** — Representação intermediária do código Python,
gerada pelo compilador antes da execução pela máquina virtual do CPython.
Inspecionável com `dis.dis()`.

## F

<a id="frame"></a>**frame** — Estrutura que guarda o estado de execução de uma
chamada de função (variáveis locais, posição de execução, referência ao frame
anterior). Empilhados durante chamadas aninhadas.

## G

<a id="generator"></a>**generator** — Função que usa `yield` para produzir valores
sob demanda, um de cada vez, em vez de construir uma coleção inteira em memória.

## I

<a id="iterable"></a>**iterable** — Objeto capaz de retornar seus elementos um de
cada vez, via `__iter__`.

<a id="iterator"></a>**iterator** — Objeto que implementa `__next__`, produzindo o
próximo valor de uma sequência a cada chamada, até esgotar.

## M

<a id="moulinette"></a>**moulinette** — Sistema de correção automatizada da 42 que
testa o código contra um conjunto de casos, incluindo verificação de norma.

<a id="mutable"></a>**mutable** — Objeto cujo conteúdo pode ser alterado após a
criação (ex: `list`, `dict`), em contraste com imutável.

## N

<a id="norma"></a>**norma** — Conjunto de regras de estilo de código exigido pela
42 (nomenclatura, limites de linha/função, etc.), verificado por ferramenta própria
independente da lógica do programa.

## P

<a id="pep"></a>**PEP (Python Enhancement Proposal)** — Documento formal de
proposta de mudança na linguagem Python, incluindo justificativa de design.
Referência oficial em peps.python.org.

## R

<a id="recursion"></a>**recursion** — Técnica em que uma função chama a si mesma
para resolver um problema em termos de uma versão menor do mesmo problema.

## T

<a id="type-hint"></a>**type hint** — Anotação opcional de tipo esperado para uma
variável, parâmetro ou retorno de função. Não é verificado em tempo de execução
pelo próprio Python (precisa de ferramenta externa como `mypy`).
