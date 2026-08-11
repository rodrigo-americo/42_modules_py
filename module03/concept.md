# module03 — Data Quest: Mastering Python Collections

Ambiente: Python 3.10.11 | Verificado em: 2026-08-10

## Objetivo do módulo

O módulo introduz as estruturas de coleção nativas do Python — lista, tupla,
`set`, `dict` — e dois recursos que operam sobre elas: generators (`yield`) e
comprehensions. O fio condutor é um sistema de analytics para um jogo:
argumentos de linha de comando viram scores, coordenadas 3D, conquistas de
jogador, inventário, um fluxo de eventos e, por fim, uma transformação de
dados condensada em comprehensions. Cada exercício restringe deliberadamente
quais funções/métodos podem ser usados, para forçar o uso do mecanismo que
está sendo ensinado em vez de um atalho pronto.

## Listas: indexação, slicing e concatenação sem métodos mutadores

**TL;DR**: uma lista guarda itens em ordem e cada um é acessível pelo índice
(`lista[0]`), incluindo fatias (`lista[1:]`). Quando métodos que mutam a
lista in-place (`append`, `pop`) não estão disponíveis, o mesmo resultado
sai de **concatenação** (`lista + [novo_item]`) ou de **slice assignment**
(`lista[i:i+1] = []`) — a diferença entre as duas é se a variável passa a
apontar para uma lista nova, ou se a lista original é editada no lugar.

<details>
<summary><strong>🔍 Aprofundando: reatribuição vs. slice assignment</strong></summary>

> ```
> >>> a = [1, 2, 3]
> >>> b = a
> >>> a = a[:1] + a[2:]     # reatribuição: 'a' passa a apontar pra lista nova
> >>> a, b
> ([1, 3], [1, 2, 3])
>
> >>> a = [1, 2, 3]
> >>> b = a
> >>> a[1:2] = []           # slice assignment: edita o objeto no lugar
> >>> a, b
> ([1, 3], [1, 3])
> ```
>
> (comportamento confirmado em REPL Python 3.10.11 local)
>
> `variavel = algo` sempre reatribui — a variável passa a apontar para um
> objeto diferente, e qualquer outra variável que apontava para o objeto
> antigo continua vendo o objeto antigo, intocado. `variavel[fatia] = algo`
> é uma operação diferente: o operador `=` aqui não reatribui `variavel`,
> ele **muta o conteúdo do objeto** que `variavel` já aponta — por isso toda
> outra referência ao mesmo objeto (`b` no exemplo acima) enxerga a mudança.
> É o mesmo princípio por trás de `lista.append(x)` ou `lista.pop(i)`: ambos
> editam o objeto existente, sem reatribuir nada.

</details>

## Tuplas: coleção ordenada e imutável

**TL;DR**: uma tupla é como uma lista, mas depois de criada não pode ser
alterada — não existe "adicionar item" nem "trocar posição". Serve bem para
agrupar valores relacionados que não devem mudar depois de montados (como
três coordenadas x, y, z).

<details>
<summary><strong>🔍 Aprofundando: por que a imutabilidade importa aqui</strong></summary>

> ```
> >>> t = (1.0, 2.5, 3.0)
> >>> t[0] = 9.0
> Traceback (most recent call last):
>   ...
> TypeError: 'tuple' object does not support item assignment
> ```
>
> (comportamento confirmado em REPL Python 3.10.11 local)
>
> A imutabilidade não é só uma restrição — é o que permite usar uma tupla
> como chave de `dict` ou elemento de `set`, coisa que uma lista jamais
> pode fazer (listas não são "hasháveis" porque seu conteúdo pode mudar
> depois de inserida). Isso não é exercitado neste módulo, mas explica por
> que o subject descreve tupla como "ordered, immutable, hashable" desde a
> introdução.

</details>

## `set`: coleção sem ordem, sem duplicatas, e operações de conjunto

**TL;DR**: um `set` guarda itens únicos, sem posição fixa — dois itens iguais
viram um só automaticamente. As três operações centrais são `union` (tudo
que está em qualquer um), `intersection` (só o que está em todos) e
`difference` (o que está no primeiro mas não nos outros).

<details>
<summary><strong>🔍 Aprofundando: union/intersection/difference aceitam múltiplos argumentos</strong></summary>

> ```
> >>> a, b, c = {1, 2, 3}, {2, 3, 4}, {3, 4, 5}
> >>> a.union(b, c)
> {1, 2, 3, 4, 5}
> >>> a.intersection(b, c)
> {3}
> >>> a.difference(b, c)
> {1}
> ```
>
> (comportamento confirmado em REPL Python 3.10.11 local)
>
> Os três métodos aceitam qualquer quantidade de conjuntos de uma vez — não
> é preciso encadear `a.union(b).union(c)` nem aninhar chamadas para
> comparar mais de dois conjuntos ao mesmo tempo. Isso simplifica bastante
> quando o problema pede "o que é comum a quatro jogadores" ou "o que só
> este jogador tem, comparado com todos os outros juntos": o segundo caso
> ainda precisa de uma união prévia dos "outros" antes do `difference`,
> porque `difference` compara contra um único conjunto de referência.
>
> `print()` de um `set` vazio mostra `set()`, não `{}` — `{}` já está
> reservado para dicionário vazio na sintaxe do Python, então o `set` vazio
> precisa do construtor por extenso para não ser ambíguo.

</details>

## `dict`: pares chave-valor, e iterar sem `.items()`

**TL;DR**: um dicionário associa cada chave a um valor (`inventario["sword"]
= 1`). Iterar um `dict` diretamente num `for` percorre só as chaves, uma de
cada vez — para obter chave e valor juntos ao mesmo tempo o jeito usual é
`.items()`, mas quando esse método não está disponível, dá para indexar o
dicionário a partir de uma lista de chaves que já se tem em mãos.

<details>
<summary><strong>🔍 Aprofundando: por que <code>for k, v in dicionario</code> quebra</strong></summary>

> ```
> >>> d = {"a": 1, "b": 2}
> >>> for k, v in d:
> ...     print(k, v)
> Traceback (most recent call last):
>   ...
> ValueError: not enough values to unpack (expected 2, got 1)
> ```
>
> (comportamento confirmado em REPL Python 3.10.11 local)
>
> Um `dict` sem `.items()`/`.values()` só entrega as chaves ao ser iterado
> — cada chave é uma única string, e desempacotar uma string em duas
> variáveis (`k, v`) tenta distribuir *caractere a caractere*: com uma
> chave de exatamente 2 caracteres o desempacotamento "funciona" (mas com
> um resultado sem sentido — `k` e `v` viram letras avulsas da chave, não
> chave e valor), e com qualquer outro tamanho de chave levanta
> `ValueError`. Nenhum dos dois casos é o que se queria. Sem `.items()`
> disponível, a alternativa é
> percorrer uma lista de chaves already conhecida e indexar o dicionário
> dentro do loop: `for chave in lista_de_chaves: valor = dicionario[chave]`
> — isso usa só indexação simples, que não é um método de `dict` e por isso
> costuma continuar disponível mesmo quando `.items()`/`.values()` não
> estão na lista de autorizados de um exercício.

</details>

## Generators: valores sob demanda com `yield`

**TL;DR**: uma função com `yield` no corpo não executa tudo de uma vez —
ela vira uma fábrica de [generator](../.claude/GLOSSARY.md#generator). Cada
chamada de `next()` roda o código até o próximo `yield`, entrega aquele
valor, e **pausa** ali (variáveis locais e posição no código ficam
guardadas). A próxima chamada de `next()` continua de onde parou, não do
início.

<details>
<summary><strong>🔍 Aprofundando: por que um <code>while True</code> com <code>yield</code> não trava</strong></summary>

> ```
> >>> def contador():
> ...     n = 0
> ...     while True:
> ...         yield n
> ...         n += 1
> ...
> >>> g = contador()
> >>> next(g), next(g), next(g)
> (0, 1, 2)
> ```
>
> (comportamento confirmado em REPL Python 3.10.11 local)
>
> Um `while True` comum, numa função normal, trava o programa — nada
> interrompe o laço. Dentro de uma função geradora, porém, cada `yield`
> devolve o controle para quem chamou `next()`; o laço só "anda mais uma
> volta" quando alguém pede o próximo valor de novo. É esse comportamento
> que permite descrever um gerador infinito (útil para "o próximo evento do
> jogo", que em tese nunca acaba) sem nunca de fato calcular todos os
> valores de uma vez — só o que for pedido, quando for pedido.
>
> Chamar a função geradora (`contador()`) não executa nada do corpo ainda
> — só cria o objeto gerador, parado no início. É `next()` (ou um `for`, que
> chama `next()` internamente) que efetivamente avança a execução.

</details>

## Comprehensions: transformar e filtrar em uma expressão

**TL;DR**: `[expressao for item in iteravel if condicao]` constrói uma lista
nova percorrendo `iteravel`, aplicando `expressao` a cada item, e mantendo só
os que passam no `if` (opcional). A mesma sintaxe, com `{chave: valor for
...}`, constrói um dicionário.

<details>
<summary><strong>🔍 Aprofundando: comprehension como açúcar sintático para o mesmo laço manual</strong></summary>

> ```python
> maiusculas = [nome.capitalize() for nome in nomes]
>
> # equivalente, escrito como loop:
> maiusculas = []
> for nome in nomes:
>     maiusculas += [nome.capitalize()]
> ```
>
> Uma comprehension não é uma ferramenta com poder diferente de um `for`
> comum — é a mesma operação (percorrer, opcionalmente transformar,
> opcionalmente filtrar) com sintaxe mais compacta. A diferença prática
> relevante aqui é de leiturabilidade e de restrição de builtins: quando um
> exercício não libera `dict.items()`/`.values()`, uma dict comprehension
> escrita como `{k: v for k, v in dicionario}` falha pelo mesmo motivo que
> o `for` manual falharia (ver seção de `dict` acima) — a comprehension não
> contorna essa limitação, porque por baixo ela é o mesmo laço.

</details>

## Regras e restrições do subject

- **Lista de builtins/métodos autorizados é definida por exercício, não
  pelo módulo inteiro.** Um exercício que introduz `set` libera
  `set.union()`/`set.intersection()`/`set.difference()`, mas não `dict` ou
  `enumerate()` — mesmo que essas ferramentas resolvessem o problema mais
  rápido. A lista de autorizados de cada exercício deve ser conferida antes
  de escrever a solução, não depois.
- **Métodos de `str`, `int`, `float` são liberados globalmente no módulo**
  (fora da lista específica de cada exercício) — é a única categoria de
  "todos os métodos de um tipo" liberada por padrão em todo o projeto.
- **`No file I/O` — todo dado vem de `sys.argv` ou `input()`, nunca de
  arquivo.**
- **`mypy` obrigatório em todo o módulo**, com hints completos em toda
  função — incluindo os parâmetros de tipos genéricos (`list[int]`, não só
  `list`; `dict[str, int]`, não só `dict`).
- **`max-complexity=6` no `flake8`** — funções que centralizam parsing e
  orquestração ao mesmo tempo tendem a estourar esse limite; extrair o
  parsing para uma função auxiliar separada costuma resolver sem mudar o
  comportamento.

## Correlação com exercícios existentes

- **ex0** isola o caso mais simples de lista: `sys.argv` já pronto, só
  indexação e slicing (`argv[0]`, `argv[1:]`), sem nenhuma construção
  manual.
- **ex1** introduz construção de lista por concatenação (sem `append`) e
  `try`/`except` aplicado item a item dentro de um laço, descartando
  entradas inválidas em vez de interromper o processamento.
- **ex2** troca lista por tupla (retorno imutável de uma função) e exige
  parsing de string caractere a caractere, sem `str.split()` disponível —
  reaproveita a mesma ideia de "acumular num buffer até um delimitador" que
  seria natural resolver com `split()`, mas escrita manualmente.
- **ex3** troca a estrutura de dados para `set`, e desloca o foco de
  "construir a coleção" para "comparar coleções entre si" via
  união/interseção/diferença.
- **ex4** introduz `dict`, reaproveita a técnica de parsing manual do ex2
  (adaptada para separador `:` em vez de `,`), e soma a esse parsing duas
  camadas de validação: sintaxe do parâmetro e regra de negócio (chave
  repetida, valor não numérico).
- **ex5** desloca de "guardar tudo numa coleção" para "produzir valores sob
  demanda" via generator — o segundo generator do exercício reaproveita a
  técnica de slice assignment da seção de listas acima para remover itens
  sem método mutador disponível.
- **ex6** reencena as transformações dos exercícios anteriores (capitalizar
  nomes, filtrar, montar um dicionário de valores, filtrar por um limiar)
  inteiramente com comprehensions, sem nenhum `for` explícito.

## Erros comuns

- Assumir que um método de coleção resolve o problema só porque existe no
  Python, sem checar se aquele exercício específico o autoriza — a mesma
  operação pode estar liberada em um exercício e não no seguinte, mesmo
  quando ambos usam o mesmo tipo de dado.
- Confundir reatribuição de uma variável (`lista = lista[:i] + lista[i+1:]`)
  com mutação do objeto original — a primeira nunca é vista por quem
  também segurava uma referência à lista antiga; só a segunda
  (`lista[i:i+1] = []`, ou um método mutador) é.
- Iterar um `dict` esperando pares chave-valor sem usar `.items()` (ou, na
  ausência dele, sem indexar a partir de uma lista de chaves) — o laço
  entrega só as chaves, e tentar desempacotar isso em duas variáveis falha.
- Esperar que uma função com `yield` execute algo ao ser chamada — ela só
  cria o objeto gerador; nada do corpo roda até o primeiro `next()` (ou
  início de um `for`).

## Perguntas de autoavaliação

1. Por que `lista = lista[:i] + lista[i+1:]`, dentro de uma função que
   recebeu `lista` como parâmetro, não altera a lista original vista por
   quem chamou a função — mas `lista[i:i+1] = []` altera?
2. Um `set` A tem 5 elementos, um `set` B tem 3, e todos os elementos de B
   também estão em A. O que `A.difference(B)` e `B.difference(A)` retornam,
   e por que os dois resultados são diferentes?
3. Numa função geradora com `while True: yield x`, o que exatamente
   acontece na memória entre uma chamada de `next()` e a próxima — o que
   fica guardado, e o que é recalculado do zero?

## Fontes consultadas

- REPL Python 3.10.11 local (via `uv run python`), para confirmar
  empiricamente: diferença entre reatribuição e slice assignment em lista,
  imutabilidade de tupla, `union`/`intersection`/`difference` com múltiplos
  argumentos, comportamento de `for k, v in dict` sem `.items()`, e
  pausa/retomada de generator com `yield` dentro de `while True`.
- `flake8`/`mypy` rodados sobre os arquivos reais do módulo (todos os 7
  exercícios), para confirmar limite de complexidade e cobertura de type
  hints.
