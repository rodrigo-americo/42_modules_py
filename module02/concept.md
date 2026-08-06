# module02 — Garden Guardian: Data Engineering for Smart Agriculture

Ambiente: Python 3.10.11 | Verificado em: 2026-08-06

## Objetivo do módulo

O subject introduz o sistema de exceções do Python: capturar erros com
`try`/`except`, levantar erros deliberadamente com `raise`, diferenciar
tipos de exceção nativos, criar hierarquias de exceção próprias, e garantir
limpeza de recursos com `finally`. O fio condutor é sempre o mesmo: um
pipeline de dados agrícola que não pode travar mesmo quando os dados de
entrada são inválidos.

## `try`/`except`: isolar o ponto de falha

**TL;DR**: `try` marca um bloco de código que pode falhar. Se uma exceção
acontecer dentro dele, o Python interrompe aquele bloco no ponto exato da
falha e desvia para o `except` correspondente, em vez de encerrar o
programa. Código depois do bloco `try`/`except` continua rodando
normalmente.

<details>
<summary><strong>🔍 Aprofundando: por que capturar demais é tão arriscado quanto não capturar nada</strong></summary>

> ```python
> def converte(valor: str) -> int:
>     return int(valor)
>
>
> try:
>     numero = converte("abc")
> except Exception as err:
>     print(f"Falhou: {err}")
> ```
>
> Um `except Exception` genérico captura qualquer subclasse de `Exception`
> — não só o erro que você previu, mas também bugs completamente
> diferentes (um `AttributeError` por ter chamado o método errado, por
> exemplo), silenciando-os como se fossem o mesmo problema. Capturar o
> tipo mais específico possível (`except ValueError`, não `except
> Exception`) é geralmente preferível — só se abre para o tipo genérico
> quando de fato qualquer falha ali deve ser tratada da mesma forma, como
> pede o próprio exercício introdutório deste módulo.
>
> Duas classes ficam **fora** de `Exception`: `SystemExit` e
> `KeyboardInterrupt` herdam direto de `BaseException`. Isso é proposital
> — `except Exception` não interfere no `Ctrl+C` do usuário nem numa saída
> intencional via `sys.exit()`. Só `except BaseException` (raramente usado)
> capturaria essas também.

</details>

## `raise`: sinalizar uma falha por decisão própria

**TL;DR**: `raise` cria e lança uma exceção manualmente, mesmo quando
nenhuma operação do Python falhou sozinha. Serve para expressar uma regra
de negócio ("esse valor está fora da faixa aceitável") como um erro formal,
em vez de deixar um valor inválido se propagar silenciosamente pelo resto
do programa.

<details>
<summary><strong>🔍 Aprofundando: quem decide o que fazer com o erro não é quem o levanta</strong></summary>

> ```python
> def valida_percentual(valor: int) -> int:
>     if valor < 0 or valor > 100:
>         raise ValueError(f"{valor} fora da faixa 0-100")
>     return valor
>
>
> def relatorio() -> None:
>     try:
>         print(valida_percentual(150))
>     except ValueError as err:
>         print(f"Entrada inválida: {err}")
> ```
>
> `valida_percentual` não imprime nada quando encontra um valor inválido —
> ela só levanta a exceção e devolve o controle para quem a chamou. É
> `relatorio()`, no `except`, que decide como reportar isso (nesse caso,
> via `print`). Essa separação importa porque a mesma função de validação
> pode ser reaproveitada em contextos que tratam o erro de formas
> diferentes (um imprime na tela, outro grava num log, outro simplesmente
> ignora e usa um valor padrão) — se a função de validação já imprimisse
> a mensagem internamente, ela ficaria presa a uma única forma de reportar
> erro.
>
> A mensagem de erro passada para `ValueError(...)` fica acessível via
> `str(err)` (ou dentro de um f-string, `f"{err}"`) em qualquer `except`
> que capture essa exceção — é assim que o texto chega ao `relatorio()`
> sem ele precisar saber o que aconteceu dentro de `valida_percentual`.

</details>

## Múltiplos tipos de exceção num único `try`

**TL;DR**: um bloco `except` pode capturar mais de um tipo de exceção ao
mesmo tempo, agrupando os tipos numa tupla: `except (TipoA, TipoB) as
err`. Isso evita repetir o mesmo tratamento em vários blocos `except`
idênticos quando a resposta ao erro é igual, não importa qual dos tipos
aconteceu.

<details>
<summary><strong>🔍 Aprofundando: descobrir o tipo real sem usar <code>type()</code></strong></summary>

> Quando vários tipos de exceção caem no mesmo `except`, ainda é possível
> saber qual deles ocorreu de fato, sem chamar `type(err)`: todo objeto de
> exceção tem um atributo `__class__`, e toda classe tem `__name__`.
>
> ```
> >>> try:
> ...     1 / 0
> ... except (ZeroDivisionError, ValueError) as err:
> ...     print(err.__class__.__name__)
> ...
> ZeroDivisionError
> ```
>
> `err.__class__` é a classe do objeto (equivalente ao que `type(err)`
> devolveria), e `.__name__` extrai o nome dela como string. Essa é a
> forma mais direta de montar uma mensagem como `"Caught ZeroDivisionError:
> ..."` de dentro de um único `except` que cobre vários tipos — sem
> precisar de um `except` separado, com uma mensagem escrita à mão, para
> cada tipo.

</details>

## Exceções customizadas e hierarquia

**TL;DR**: uma classe de exceção própria é criada herdando de `Exception`
(ou de outra exceção já criada). Isso permite dar nomes específicos a
categorias de erro do próprio domínio do programa (em vez de reaproveitar
`ValueError` para tudo), e organizar essas categorias em famílias — capturar
a classe mais genérica de uma família também captura qualquer uma das suas
subclasses mais específicas.

<details>
<summary><strong>🔍 Aprofundando: mensagem padrão via <code>__init__</code> sobrescrito</strong></summary>

> ```python
> class FerramentaError(Exception):
>     def __init__(self, message: str = "Erro desconhecido de ferramenta") -> None:
>         super().__init__(message)
>
>
> class MartelinhoError(FerramentaError):
>     def __init__(self, message: str = "Erro desconhecido de martelo") -> None:
>         super().__init__(message)
>
>
> try:
>     raise MartelinhoError()
> except FerramentaError as err:
>     print(err)          # Erro desconhecido de martelo
>
> try:
>     raise MartelinhoError("cabo rachado")
> except MartelinhoError as err:
>     print(err)          # cabo rachado
> ```
>
> Dois pontos que costumam confundir:
>
> - `except FerramentaError` captura um `MartelinhoError` porque, na
>   cadeia de herança, todo `MartelinhoError` também é um
>   `FerramentaError` — é o mesmo princípio de `isinstance()` aplicado a
>   exceções.
> - Cada subclasse define seu próprio valor default para `message` no
>   parâmetro do `__init__`. Se `MartelinhoError` não sobrescrevesse
>   `__init__`, ela herdaria o `__init__` (e o default) de
>   `FerramentaError` diretamente — o que é válido, mas perde a
>   possibilidade de cada subclasse ter uma mensagem padrão diferente das
>   demais.
>
> `super().__init__(message)` repassa a mensagem para
> `Exception.__init__`, que a guarda internamente (em `self.args`) — é
> esse armazenamento que faz `str(err)`/`print(err)` mostrar o texto certo
> depois.

</details>

## `finally`: código que roda não importa o quê

**TL;DR**: um bloco `finally` sempre executa depois do `try` (e de
qualquer `except` correspondente), independente de ter ocorrido uma
exceção, dela ter sido capturada, ou até de o bloco `except` conter um
`return`. Serve para garantir limpeza de recursos (fechar um arquivo,
uma conexão, um "sistema" simulado) que precisa acontecer sempre.

<details>
<summary><strong>🔍 Aprofundando: <code>finally</code> roda antes do <code>return</code> "sair" de verdade</strong></summary>

> ```
> >>> def f():
> ...     try:
> ...         raise ValueError("x")
> ...     except ValueError:
> ...         return "saída pelo except"
> ...     finally:
> ...         print("finally rodou")
> ...
> >>> f()
> finally rodou
> 'saída pelo except'
> ```
>
> (comportamento confirmado em REPL Python 3.10.11 local)
>
> Um `return` dentro de um `except` não interrompe a função
> imediatamente — o Python "guarda" o valor que seria retornado, executa o
> `finally` inteiro primeiro, e só então efetivamente devolve o controle
> para quem chamou a função. Isso vale mesmo que o `finally` não tenha
> nenhum `return` próprio: ele roda pelo efeito colateral (aqui, o
> `print`), e o valor original do `except` é o que acaba sendo retornado.
>
> ⚠️ atenção (não testado neste módulo, mas relevante para entender o
> mecanismo): se o **próprio** `finally` contiver um `return`, esse
> `return` sobrescreve o do `except` — o valor do `finally` "vence". Por
> isso a prática comum é usar `finally` só para efeitos colaterais de
> limpeza (fechar recurso, imprimir log), sem `return` dentro dele.

</details>

## Regras e restrições do subject

- **Lista de builtins autorizados por exercício é bem restrita**
  (`int()`, `print()` no ex0/ex1; some `open()` no ex2; `str.capitalize()`
  no ex4) — o objetivo é forçar o uso do mecanismo de exceção sendo
  ensinado, não de alguma função pronta que contorne o conceito.
- **`try`, `except`, `finally`, `raise` são palavras-chave da linguagem**,
  não builtins — por isso não aparecem em nenhuma lista de "autorizados"
  do subject, mesmo sendo o tema central do módulo inteiro.
- **"Your programs must never crash" é a regra mais importante do
  módulo** — todo exercício é avaliado, entre outras coisas, por rodar do
  início ao fim sem lançar um traceback não tratado, mesmo alimentado com
  entradas inválidas de propósito.
- **`mypy` obrigatório, com uma exceção documentada**: o ex2 exige uma
  operação que o `mypy` sinaliza como erro de tipo (somar `str` + `int`),
  porque essa é justamente a forma de gerar um `TypeError` real em tempo
  de execução. O próprio subject avisa que esse erro do `mypy`, ali, é
  esperado — não deve ser "corrigido" a ponto de deixar de existir o
  `TypeError` que o exercício pede para capturar.

## Correlação com exercícios existentes

- **ex0** isola o mecanismo básico: uma função que pode falhar, e um
  `try`/`except` em volta da chamada, sem validação de regra de negócio
  ainda — só a conversão de tipo pode falhar.
- **ex1** adiciona `raise` deliberado sobre uma condição que o Python não
  detectaria sozinho (faixa de valores aceitável), reaproveitando a mesma
  estrutura de teste do ex0.
- **ex2** amplia para vários tipos de exceção nativos diferentes,
  reunidos sob um único `except` com tupla de tipos — e mostra como
  identificar qual tipo ocorreu sem `type()`.
- **ex3** introduz hierarquia própria de exceções, preparando a base que
  o ex4 reaproveita.
- **ex4** combina tudo: a exceção customizada do ex3, um `try/except`
  interno por item de uma coleção, e um `finally` externo garantindo
  limpeza mesmo quando o laço é interrompido cedo por um `return` dentro
  do `except`.

## Erros comuns

- Usar `except:` sem especificar nenhum tipo (bare except) — captura
  literalmente qualquer coisa, inclusive interrupções do usuário
  (`Ctrl+C`) e chamadas de saída do programa, que normalmente não deveriam
  ser tratadas como "erro de dado". `flake8` sinaliza isso como aviso de
  estilo (`E722`) justamente por esse risco.
- Colocar a lógica de impressão de erro dentro da função que valida o
  dado, em vez de deixar quem chama essa função decidir como reportar o
  problema — acopla a validação a uma única forma de exibir o erro.
- Fazer a subclasse de exceção herdar de `Exception` diretamente, em vez
  de herdar da exceção "base" da própria família — isso quebra a
  possibilidade de capturar todas as exceções relacionadas com um único
  `except` na classe mais genérica.
- Colocar um `raise` de teste (ou dado de teste específico) como valor
  *default* do `__init__` de uma exceção customizada — o valor default
  deveria ser uma mensagem genérica de fallback, usada só quando ninguém
  passa uma mensagem específica na hora de instanciar o erro.

## Perguntas de autoavaliação

1. Se um `except` captura `(TipoA, TipoB)`, e dentro do bloco você faz
   `err.__class__.__name__`, por que isso funciona sem precisar de um
   `except` separado para cada tipo?
2. Por que uma exceção customizada `FilhaError(BaseError)` é capturada por
   `except BaseError`, mas o inverso não é verdadeiro (uma `BaseError`
   genérica não é capturada por `except FilhaError`)?
3. Num bloco com `try`/`except`/`finally`, se o `except` contém um
   `return` e o `finally` também contém um `return` diferente, qual valor
   a função efetivamente devolve — e por quê?

## Fontes consultadas

- REPL Python 3.10.11 local (via `uv run python`), para confirmar
  empiricamente a ordem de execução entre `return` no `except` e o
  `finally`
- `flake8`/`mypy` rodados sobre os arquivos reais do módulo, para
  confirmar quais avisos são esperados (ex2) e quais precisavam de
  correção (newline final, espaçamento entre funções)
