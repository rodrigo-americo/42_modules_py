# module10 — FuncMage: Master the Ancient Arts of Functional Programming

Ambiente: Python 3.10+ (testado em 3.13.2, Windows) | Verificado em: 2026-09-12

## Objetivo do módulo

Segundo o subject (`py10.pdf`), o módulo ensina programação funcional através
de cinco exercícios com tema de magos ("Function Mages") que sobem em
dificuldade: expressões `lambda` (`ex0`), funções de alta ordem (`ex1`),
closures e escopo léxico (`ex2`), o módulo `functools` (`ex3`), e
decoradores + `@staticmethod` (`ex4`). O fio condutor é a ideia de que
funções em Python são "cidadãs de primeira classe" — podem ser passadas,
retornadas e guardadas como qualquer outro valor — e que essa propriedade
sozinha explica todos os padrões vistos no módulo.

## Lambda expressions

**TL;DR**: `lambda` cria uma função sem nome, direto na linha onde ela é
usada — útil quando a função é curta e só serve para aquele momento (ex:
dizer a `sorted()` por qual campo ordenar).

<details>
<summary><strong>🔍 Aprofundando: sintaxe, limitações e quando NÃO usar</strong></summary>

> Uma lambda é uma expressão, não uma instrução — por isso só pode conter
> uma única expressão, nunca statements como `if/else` soltos ou múltiplas
> linhas. `lambda x: x if x > 0 else -x` funciona porque `if/else` aí é o
> **operador condicional de expressão**, não um bloco `if` comum.
>
> Toda lambda tem uma função `def` equivalente:
> ```
> f = lambda x, y: x + y
> # equivale a:
> def f(x, y):
>     return x + y
> ```
>
> A diferença real não é poder — é forma. Uma lambda não tem nome próprio no
> objeto (verificado: `f.__name__` retorna `'<lambda>'` mesmo atribuída a
> `f`), e não pode ter docstring nem anotações de tipo completas. Por isso o
> subject proíbe usá-la para "operações complexas": se a lógica precisa de
> mais de uma expressão ou de um nome que documente a intenção, `def` é a
> ferramenta certa.
>
> **Conexões:**
> - `Histórico:` lambda em Python vem do cálculo lambda de Alonzo Church,
>   mas a implementação em Python é deliberadamente limitada (só uma
>   expressão) — decisão de Guido van Rossum para não competir com `def`
>   como forma de definir funções complexas.

</details>

## Higher-order functions embutidas: map, filter, sorted

**TL;DR**: `map()` transforma cada item de uma lista, `filter()` seleciona
só os itens que passam num teste, e `sorted(..., key=...)` ordena usando uma
função que diz "por qual valor comparar". As três recebem uma função como
argumento — por isso combinam bem com lambda.

<details>
<summary><strong>🔍 Aprofundando: preguiça (laziness), assinatura posicional, e key=</strong></summary>

> `map()` e `filter()` em Python 3 retornam **iteradores preguiçosos** — só
> processam a lista quando alguém itera sobre eles (`list(...)`, um `for`,
> ou passando direto para `sorted()`/`sum()`). Isso é diferente do Python 2,
> onde ambos retornavam listas prontas.
>
> A assinatura de ambos é posicional — `map(function, iterable)` e
> `filter(function, iterable)` — nenhum dos dois aceita as palavras `func=`
> ou `iterable=` como keyword argument; passar nomeado lança `TypeError`
> (verificado, Python 3.13.2).
>
> `sorted(iteravel, key=funcao, reverse=True)` chama `funcao(item)` para
> cada item e ordena pelo valor retornado — não pelo item inteiro. Isso
> evita escrever uma função de comparação manual (`cmp`, removida do
> `sorted()` em Python 3).
>
> Diferente de `map`/`filter`/`sorted`, `sum()` **não aceita `key=`**
> (verificado — `TypeError: sum() takes no keyword arguments` em Python
> 3.13.2). Para somar um campo específico de uma lista de dicts, primeiro
> se extrai os valores com `map()`, depois soma o resultado.

</details>

## Higher-order functions: função que recebe/retorna função

**TL;DR**: uma função de alta ordem é qualquer função que recebe outra
função como argumento, ou que **retorna** uma função. Em Python isso é
natural porque funções são objetos como qualquer outro — podem ser
guardadas em variáveis, passadas adiante, devolvidas.

<details>
<summary><strong>🔍 Aprofundando: "first-class citizens" e o padrão fábrica</strong></summary>

> Dizer que funções são "cidadãs de primeira classe" significa que têm os
> mesmos direitos que `int`, `str`, `list`: podem ser atribuídas a uma
> variável, guardadas numa lista, passadas como argumento, e retornadas por
> outra função.
>
> O padrão central do ex1 é "função que fabrica função":
> ```
> def power_amplifier(base_spell, multiplier):
>     def amplified(target, power):
>         return base_spell(target, power * multiplier)
>     return amplified
> ```
> A função interna (`amplified`) "lembra" de `base_spell` e `multiplier`
> mesmo depois que `power_amplifier` já terminou de rodar — isso é uma
> **closure**, aprofundada formalmente no conceito seguinte.
>
> **Conexões:**
> - `Diagrama:` a relação é hierárquica — a função externa é a "fábrica", e
>   cada chamada dela produz uma função filha independente, cada uma com
>   seus próprios valores fechados no escopo.

</details>

## Callable como type hint

**TL;DR**: `Callable` é o tipo usado para dizer "isto é uma função (ou
qualquer objeto que pode ser chamado com `()`)", em vez de um tipo de dado
comum como `int` ou `str`.

<details>
<summary><strong>🔍 Aprofundando: de onde vem Callable, e o que callable() faz</strong></summary>

> O subject pede explicitamente: "when using Callable as a type hint, use
> `collections.abc`". Desde a PEP 585 (Python 3.9), `collections.abc.Callable`
> é preferível a `typing.Callable` — este último ainda existe, mas seu uso é
> desencorajado desde que os tipos de `collections.abc` passaram a suportar
> subscrição genérica diretamente (`Callable[[int, str], bool]`).
>
> `callable(obj)` é diferente — é uma função embutida (não um tipo), que
> devolve `True`/`False` em runtime perguntando "esse objeto pode ser
> chamado com `()`?". Funções, métodos, classes e objetos com `__call__`
> retornam `True`.

</details>

## Closures e escopo léxico

**TL;DR**: uma closure é uma função que "leva junto" as variáveis do lugar
onde foi criada, mesmo depois que essa função externa já terminou de
rodar. É assim que uma função consegue "lembrar" e até modificar um valor
entre chamadas, sem usar variável global.

<details>
<summary><strong>🔍 Aprofundando: por que global é proibido mas nonlocal é permitido</strong></summary>

> Escopo léxico significa que o Python decide onde uma variável "vive"
> olhando para **onde o código foi escrito**, não para a ordem em que as
> funções são chamadas em runtime.
>
> Por padrão, uma atribuição (`x = x + 1`) dentro de uma função interna cria
> uma variável **local nova**, mesmo que exista uma de mesmo nome na função
> externa — Python não modifica a de fora automaticamente. Isso causa
> `UnboundLocalError` se a variável for lida antes de ser atribuída
> localmente (verificado, Python 3.13.2: remover `nonlocal` de um contador
> que faz `count += 1` produz exatamente esse erro).
>
> `nonlocal x` resolve isso dizendo explicitamente: "não crie uma variável
> local, use a já existente no escopo envolvente". `global x` faria o mesmo,
> mas apontando para o escopo do módulo inteiro — e é por isso que o
> subject proíbe `global`: usar variável de módulo quebra o isolamento de
> estado que o exercício exige (duas fábricas de contador não podem
> compartilhar estado entre si).
>
> `nonlocal` só é necessário quando a função interna **reatribui** a
> variável do escopo externo (`total += valor`). Quando a variável é só
> **lida**, ou quando é uma estrutura mutável (dict, list) que só recebe
> `.append()`/atribuição de chave (`d[k] = v`), a closure já enxerga a
> variável de fora sem precisar de `nonlocal` — porque nesses casos não há
> reatribuição da variável em si, só mutação do objeto que ela referencia.
>
> **Conexões:**
> - `Diagrama:` cada chamada de uma função-fábrica cria um novo escopo
>   isolado — não é uma variável compartilhada entre todas as closures
>   geradas, é uma célula própria por instância.

</details>

## functools.reduce + operator

**TL;DR**: `reduce()` pega uma função de "combinar dois valores" e aplica
repetidamente numa lista, até sobrar um único resultado. O módulo
`operator` fornece essas funções de combinar (`add`, `mul`, etc.) já
prontas, para não precisar escrever lambda toda vez.

<details>
<summary><strong>🔍 Aprofundando: como reduce processa a lista, e por que não é built-in</strong></summary>

> `reduce(function, iterable)` funciona assim: pega os dois primeiros
> itens, aplica `function(item1, item2)`, guarda o resultado; pega esse
> resultado e o próximo item, aplica de novo; repete até acabar a lista.
> ```
> reduce(operator.add, [10, 20, 30])
> # passo 1: add(10, 20) = 30
> # passo 2: add(30, 30) = 60
> ```
> `functools.reduce` não é built-in desde Python 3 (era em Python 2) — a
> mudança moveu `reduce` para dentro de `functools` justamente para
> desencorajar seu uso indiscriminado, já que `sum()`, list comprehensions e
> loops explícitos cobrem a maioria dos casos de forma mais legível.
>
> `operator.add(a, b)` é equivalente a `a + b`, mas como função nomeada —
> existe porque `reduce` (e `sorted`, `map`, etc.) esperam receber uma
> função, evitando escrever `lambda a, b: a + b` repetidamente. `reduce`
> também aceita funções built-in de dois argumentos diretamente, como
> `max`/`min` (verificado: `reduce(max, [3, 7, 2])` retorna `7`).
>
> Chamar `reduce` numa lista vazia sem valor inicial lança `TypeError`
> (verificado) — por isso o subject pede tratamento explícito de lista
> vazia (retornar `0`) *antes* de chamar `reduce`.

</details>

## functools.partial

**TL;DR**: `partial` cria uma nova função a partir de uma existente, mas já
"travando" alguns dos argumentos — como preencher parte de um formulário e
deixar só o resto em branco para depois.

<details>
<summary><strong>🔍 Aprofundando: partial vs. lambda para o mesmo efeito</strong></summary>

> ```
> from functools import partial
> fire_enchant = partial(base_enchantment, power=50, element="fire")
> fire_enchant(target="Sword")  # só falta o argumento não travado
> ```
> Isso é equivalente a `lambda target: base_enchantment(power=50,
> element="fire", target=target)`, mas `partial` preserva melhor a
> introspecção da função original e deixa a intenção — "estou fixando
> argumentos" — explícita, em vez de escondida dentro de uma lambda.

</details>

## functools.lru_cache (memoização)

**TL;DR**: `lru_cache` guarda os resultados de chamadas já feitas; se a
função for chamada de novo com os mesmos argumentos, devolve o resultado
guardado em vez de recalcular — essencial para fibonacci recursivo, que sem
cache recalcula os mesmos valores exponencialmente.

<details>
<summary><strong>🔍 Aprofundando: por que fibonacci recursivo é lento sem cache</strong></summary>

> `fib(n) = fib(n-1) + fib(n-2)` sem memoização recalcula os mesmos
> subproblemas repetidamente — cresce exponencialmente (O(2^n)). Com
> `lru_cache`, cada `fib(k)` só é calculado uma vez — complexidade cai para
> O(n).
>
> "LRU" significa *Least Recently Used* — quando o cache atinge o tamanho
> máximo (`maxsize`, padrão 128), o valor usado há mais tempo é descartado
> primeiro.
>
> `.cache_info()` retorna um `namedtuple` com `hits`, `misses`, `maxsize`,
> `currsize`. Verificado (Python 3.13.2): calcular `fib(15)` com cache limpo
> produz `hits=16, misses=16` — cada um dos 16 valores distintos de `n`
> (`0` a `15`) é calculado uma única vez (`misses`), e as chamadas
> recursivas repetidas para os mesmos `n` reaproveitam o cache (`hits`).

</details>

## functools.singledispatch

**TL;DR**: `singledispatch` permite que uma função tenha comportamentos
diferentes dependendo do **tipo** do primeiro argumento, sem precisar de
uma cadeia de `if isinstance(...)` dentro do corpo.

<details>
<summary><strong>🔍 Aprofundando: como o registro de tipos funciona</strong></summary>

> ```
> from functools import singledispatch
>
> @singledispatch
> def cast(spell):
>     return "Unknown spell type"
>
> @cast.register
> def _(spell: int):
>     return f"{spell} damage"
> ```
> A função decorada com `@singledispatch` vira a implementação "padrão"
> (para tipos não registrados). Cada `@cast.register` adiciona uma
> implementação alternativa associada a um tipo específico, inferido pela
> anotação do parâmetro. Quando `cast(algum_valor)` é chamado, Python
> escolhe automaticamente a implementação certa olhando `type(algum_valor)`.
> Verificado: um valor de tipo não registrado (`float`, no exercício deste
> módulo) cai corretamente na implementação padrão.

</details>

## Decoradores

**TL;DR**: um decorador é uma função que recebe outra função e devolve uma
versão "envolvida" dela — permite adicionar comportamento (log, validação,
timing) sem alterar o código da função original. A sintaxe `@decorador`
acima de uma `def` é um atalho para `funcao = decorador(funcao)`.

<details>
<summary><strong>🔍 Aprofundando: decorador simples vs. parametrizado, e o papel de wraps</strong></summary>

> Um decorador simples tem essa forma:
> ```
> def spell_timer(func):
>     @wraps(func)
>     def wrapper(*args, **kwargs):
>         result = func(*args, **kwargs)
>         return result
>     return wrapper
> ```
> Um decorador que recebe **parâmetros próprios** (ex: um limite mínimo de
> poder, ou um número de tentativas) precisa de uma camada extra: uma
> função externa que recebe o parâmetro e retorna o decorador de verdade:
> ```
> def power_validator(min_power):
>     def decorator(func):
>         @wraps(func)
>         def wrapper(*args, **kwargs):
>             ...
>         return wrapper
>     return decorator
> ```
> `functools.wraps` resolve um problema sutil: sem ele, depois de decorar,
> `func.__name__` e `func.__doc__` passam a apontar para o `wrapper`
> genérico, não para a função original. Verificado (Python 3.13.2): sem
> `@wraps(func)`, `func.__name__` dentro do wrapper de um decorador ainda é
> o nome certo (porque `func` é a referência original capturada na
> closure), mas é a função **decorada e exposta ao chamador** que perde o
> nome — `nome_da_funcao.__name__` externamente vira `'wrapper'` sem
> `@wraps`. Isso quebra introspecção, debugging e qualquer código externo
> que dependa do nome real da função.
>
> Um decorador que precisa inspecionar um argumento específico da chamada
> (como "qual é o valor de `power` nesta chamada?") sem conhecer a
> assinatura exata da função decorada esbarra numa limitação real: sem usar
> `inspect.signature` (fora do escopo autorizado neste módulo), a única
> saída é assumir uma convenção — por exemplo, checar `kwargs` primeiro e
> cair para uma posição fixa em `args` como alternativa. Essa abordagem é
> frágil fora de um exercício controlado: quebra se a ordem dos parâmetros
> da função decorada mudar, ou se o argumento não for passado nem por nome
> nem na posição esperada.
>
> **Conexões:**
> - `Diagrama:` um decorador parametrizado tem 3 níveis de aninhamento — a
>   fábrica externa (recebe o parâmetro) → o decorador (recebe a função) →
>   o wrapper (recebe os argumentos da chamada real). Cada nível fecha
>   (closure) sobre o de fora.

</details>

## @staticmethod

**TL;DR**: um método estático é uma função dentro de uma classe que **não
recebe `self`** — não acessa nem modifica dados da instância, só está ali
porque faz sentido organizacionalmente.

<details>
<summary><strong>🔍 Aprofundando: staticmethod vs. método de instância</strong></summary>

> Diferente de um método normal (`def metodo(self, ...)`), um
> `@staticmethod` pode ser chamado tanto numa instância
> (`instancia.metodo(...)`) quanto direto na classe
> (`Classe.metodo(...)`), porque não precisa de `self` para funcionar — não
> olha para nenhum estado de uma instância específica. Verificado: chamar o
> método estático de validação de nome direto na classe, sem instanciar
> nada, funciona normalmente.

</details>

## Regras e restrições do subject

- **Cada exercício restringe as ferramentas autorizadas progressivamente.**
  `ex0` só libera `map`/`filter`/`sorted`/`min`/`max`/`round`/`sum`/`len`;
  `ex1` libera `callable()`/`Callable`; `ex2` libera `nonlocal`; `ex3`
  libera `functools`/`operator`; `ex4` libera `functools.wraps` e
  `staticmethod`. Essa progressão força usar exatamente o conceito que cada
  exercício quer ensinar, em vez de resolver tudo com uma ferramenta só.
- **`global` é proibido em todo o módulo** ("Common Instructions" → Forbidden).
  A proibição existe porque o módulo inteiro treina "estado sem variável
  global" — closures (`nonlocal`) são a alternativa funcional correta.
- **`eval()`/`exec()` proibidos**, junto com bibliotecas externas e I/O de
  arquivo — o módulo é sobre padrões de função em memória, não sobre
  manipular dados externos.
- **Python 3.10+, flake8, type hints em todas as assinaturas.**

## Correlação com exercícios existentes

- **ex0 (`lambda_spells.py`)** exercita lambda combinada com as
  higher-order functions embutidas (`sorted`, `filter`, `map`, `max`,
  `min`, `sum`) para ordenar, filtrar, transformar e agregar listas de
  dicionários.
- **ex1 (`higher_magic.py`)** exercita o padrão "função que recebe e/ou
  retorna função", preservando um contrato de assinatura fixo entre a
  função original e a nova função gerada.
- **ex2 (`scope_mysteries.py`)** exercita closures que mantêm estado
  privado entre chamadas (contador, acumulador, armazenamento chave-valor),
  usando `nonlocal` só onde há reatribuição de uma variável do escopo
  externo.
- **ex3 (`functools_artifacts.py`)** exercita quatro ferramentas do
  `functools` que resolvem, de forma pronta, os mesmos padrões vistos nos
  exercícios anteriores: agregação (`reduce`), aplicação parcial
  (`partial`), memoização (`lru_cache`), e despacho por tipo
  (`singledispatch`).
- **ex4 (`decorator_mastery.py`)** fecha o módulo combinando higher-order
  functions (ex1) e closures (ex2) na forma de decorador — simples,
  parametrizado, e aplicado a um método de classe junto de `@staticmethod`.

## Erros comuns

- Confundir chamada de função com declaração de função: anotar tipo
  (`nome: tipo`) só é válido dentro de uma `def`/lambda, nunca ao passar
  argumentos para uma função já existente.
- Esquecer `nonlocal` quando a função interna faz uma reatribuição
  (`variavel += 1`) sobre uma variável do escopo externo — resulta em
  `UnboundLocalError`.
- Usar `nonlocal` (ou `global`) quando não é necessário — mutar um
  dicionário ou lista existentes (`d[k] = v`, `lista.append(x)`) não exige
  a declaração, só reatribuir a variável em si exige.
- Esquecer `functools.wraps` num decorador — a função decorada perde nome e
  docstring originais silenciosamente, sem erro visível.
- Aplicar um decorador parametrizado sem a camada extra de função externa
  que recebe o parâmetro antes de retornar o decorador de verdade.
- Em `functools.reduce`, tentar reduzir uma lista vazia sem tratar esse
  caso antes — lança `TypeError`.
- Confundir "retornar uma função" com "chamar a função e retornar o
  resultado" — funções de alta ordem devem devolver uma função nova, que só
  executa quando chamada depois pelo código cliente.

## Perguntas de autoavaliação

1. Por que uma lambda não pode conter um `for` ou múltiplas instruções, mas
   uma função com `def` pode?
2. Por que `global` é proibido no módulo mas `nonlocal` é permitido? Quais
   as diferenças-chave entre eles?
3. Como `functools.reduce` permite agregação de dados de forma genérica?
   Quais os benefícios de performance da memoização com `lru_cache`?
4. Qual a diferença entre `@staticmethod` e um método de instância comum?
   Por que um decorador não consegue, de forma genérica, "adivinhar" o
   valor de um argumento nomeado sem assumir uma convenção sobre a
   assinatura da função decorada?

## Fontes consultadas

- Execução real no ambiente: Python 3.13.2 — toda afirmação sobre
  `TypeError` de `map`/`filter`/`sum` com keyword arguments,
  `UnboundLocalError` sem `nonlocal`, comportamento de `reduce` com
  `max`/`min` e lista vazia, `cache_info()` de `lru_cache`,
  `functools.wraps` preservando `__name__`, e `singledispatch` com tipo não
  registrado foi rodada e verificada.
- https://docs.python.org/3/reference/expressions.html#lambda — sintaxe e
  limitações de `lambda`
- https://docs.python.org/3/library/functions.html#map — `map`, `filter`,
  `sorted` (assinatura posicional)
- https://docs.python.org/3/reference/compound_stmts.html#function-definitions
  — closures e `nonlocal`
- https://docs.python.org/3/library/functools.html — `reduce`, `partial`,
  `lru_cache`, `singledispatch`, `wraps`
- https://docs.python.org/3/library/collections.abc.html — `Callable`
  (PEP 585)
