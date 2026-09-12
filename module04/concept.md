# module04 — Data Archivist: Digital Preservation in the Cyber Archives

Ambiente: Python 3.10.11 | Verificado em: 2026-08-10

## Objetivo do módulo

O módulo introduz operações de arquivo em Python — abrir, ler, escrever e
fechar — junto com os três canais de fluxo padrão (`stdin`, `stdout`,
`stderr`) e o `with` statement como forma seguro de gerenciar recursos. O
fio condutor é um sistema de arquivamento digital: um exercício recupera o
conteúdo de um arquivo como o comando `cat`, o seguinte transforma e salva
esse conteúdo, o terceiro troca `print()`/`input()` pelos streams
explícitos, e o último consolida tudo numa função que lê ou escreve de
forma seguro usando `with`.

## `open()`: o que ele retorna, e por que fechar importa

**TL;DR**: `open(caminho)` devolve um objeto arquivo (não uma string com o
conteúdo) — para obter o texto é preciso chamar `.read()` nesse objeto. Todo
arquivo aberto ocupa um recurso do sistema operacional que precisa ser
liberado explicitamente com `.close()` quando o `with` ainda não está
disponível.

<details>
<summary><strong>🔍 Aprofundando: o tipo exato retornado, e por que ele muda com o modo</strong></summary>

> ```
> >>> f = open("arquivo.bin", "rb")
> >>> type(f)
> <class '_io.BufferedReader'>
> >>> f.close()
> >>> f2 = open("arquivo.txt", "w")
> >>> type(f2)
> <class '_io.TextIOWrapper'>
> ```
>
> (comportamento confirmado em REPL Python 3.10.11 local)
>
> O tipo devolvido por `open()` depende do modo: em modo texto (o padrão,
> sem `b` no segundo argumento) é um `TextIOWrapper`, que decodifica bytes
> em `str` automaticamente; em modo binário (`"rb"`, `"wb"`) é um
> `BufferedReader`/`BufferedWriter`, que trabalha com `bytes` crus. Ambos
> são instâncias do tipo abstrato descrito pelo módulo `io`, e é por isso
> que o subject autoriza `import typing` + `typing.IO` — essa é a anotação
> de tipo que descreve "um objeto arquivo, seja qual for o tipo concreto
> exato por trás dele", útil para dar type hint ao valor de retorno de uma
> função que abre um arquivo sem amarrar a assinatura a `TextIOWrapper`
> especificamente.

</details>

## Exceções de arquivo: todas nascem de `OSError`

**TL;DR**: tentar abrir um arquivo que não existe, ou que existe mas sem
permissão de leitura, não trava o programa — lança uma exceção que pode ser
capturada com `try`/`except` e transformada numa mensagem de erro amigável
em vez de um crash.

<details>
<summary><strong>🔍 Aprofundando: FileNotFoundError e PermissionError são subclasses de OSError</strong></summary>

> ```
> >>> try:
> ...     open("/not/existing/file")
> ... except OSError as e:
> ...     print(type(e).__name__, "|", str(e), "| errno:", e.errno)
> ...
> FileNotFoundError | [Errno 2] No such file or directory: '/not/existing/file' | errno: 2
> ```
>
> (comportamento confirmado em REPL Python 3.10.11 local)
>
> `FileNotFoundError` (arquivo inexistente, `errno` 2) e `PermissionError`
> (sem permissão, `errno` 13) são ambas subclasses de `OSError` — capturar
> `OSError` sozinho já cobre os dois casos sem precisar de dois blocos
> `except` separados. A mensagem que aparece com `str(e)` já vem formatada
> pelo próprio Python no padrão `[Errno N] descrição: 'caminho'` — é esse
> texto, não algo montado manualmente, que aparece nos exemplos do subject
> quando um arquivo não pode ser aberto.

</details>

## `with`: fechamento garantido mesmo com erro no meio

**TL;DR**: `with open(caminho) as f:` abre o arquivo, executa o bloco
indentado, e fecha o arquivo automaticamente ao sair do bloco — inclusive se
uma exceção interromper o bloco no meio. Antes do `with`, a mesma garantia
exige `try`/`finally` manual; o subject proíbe usar `with` antes do
exercício que o introduz, exatamente para que essa diferença fique visível.

<details>
<summary><strong>🔍 Aprofundando: o fechamento acontece mesmo quando uma exceção escapa do bloco</strong></summary>

> ```
> >>> class Boom(Exception): pass
> ...
> >>> try:
> ...     with open("arquivo.txt") as f:
> ...         raise Boom("falha")
> ... except Boom:
> ...     pass
> ...
> >>> f.closed
> True
> ```
>
> (comportamento confirmado em REPL Python 3.10.11 local)
>
> `f` continua acessível fora do bloco `with` (o `with` não cria um escopo
> próprio de variável), e `f.closed` confirma que o arquivo foi fechado
> mesmo que a exceção `Boom` tenha interrompido a execução no meio do
> bloco, antes de qualquer `.close()` explícito. Isso é o `with` chamando o
> método `__exit__` do objeto arquivo automaticamente ao sair do bloco —
> por exceção ou normalmente — o que evita o padrão repetitivo (e fácil de
> esquecer) de um `try`/`finally` com `.close()` no `finally`.

</details>

## `sys.stdin`/`sys.stdout`/`sys.stderr`: os três canais por trás de `input()`/`print()`

**TL;DR**: `input()` e `print()` são atalhos convenientes sobre três objetos
arquivo que já existem antes de qualquer `open()` — `sys.stdin` (entrada),
`sys.stdout` (saída normal) e `sys.stderr` (saída de erro). Escrever
diretamente nesses objetos (com `.write()`) separa mensagens de erro da
saída normal, o que importa quando alguém redireciona só uma das duas para
um arquivo.

<details>
<summary><strong>🔍 Aprofundando: por que separar stdout de stderr importa na prática</strong></summary>

> `sys.stdin`, `sys.stdout` e `sys.stderr` são objetos arquivo como
> qualquer outro devolvido por `open()` — têm `.read()`, `.readline()`,
> `.write()`, mas nunca precisam (nem devem) ser fechados pelo programa,
> porque pertencem ao processo, não a um arquivo que o programa abriu. A
> razão de existirem dois canais de saída distintos (`stdout` e `stderr`)
> em vez de um só é permitir que quem executa o programa redirecione cada
> um para um destino diferente — por exemplo `programa > saida.txt` só
> captura o que foi escrito em `stdout`; qualquer `[STDERR] ...` escrito em
> `sys.stderr` continua aparecendo no terminal. Um erro reportado em
> `stdout` se mistura com dados válidos nesse cenário; reportado em
> `stderr`, fica sempre separável da saída normal, mesmo com redirecionamento.

</details>

## Regras e restrições do subject

- **Lista de builtins/métodos autorizados cresce por exercício, nunca
  encolhe** — `ex0` libera `open()`/`.read()`/`.close()`; `ex1` soma
  `.write()` e `input()`; `ex2` troca `input()`/`print()` pelos streams
  (`sys.stdin`, `sys.stdout`, `sys.stderr`) e soma `.readline()`/`.flush()`;
  `ex3` restringe de novo, para `open()`, `.read()`, `.write()`, `print()`
  — mas dessa vez com `with` obrigatório.
- **`with` é proibido antes do ex3, e obrigatório a partir dele** — não é
  uma sugestão de estilo; o subject verifica isso na correção.
- **Tipos e coleções permitidos em todo o módulo**: `str`, `int`, `float`,
  `list`, `dict`, `set`, `tuple`, com todos os métodos associados.
- **`mypy` obrigatório**, incluindo a anotação `typing.IO` para valores de
  retorno de funções que abrem arquivo, quando o exercício não usa `with`.
- **`ex3` exige uma função `secure_archive()`** que devolve sempre uma
  tupla `(bool, str)` — nunca lança exceção para quem chamou, mesmo quando
  a operação de arquivo falha; o `bool` sinaliza sucesso/falha e o `str`
  carrega o conteúdo lido ou a mensagem de erro.

## Correlação com exercícios existentes

- **ex0** isola o caso mais simples: `open()` manual, leitura completa,
  `.close()` manual, e captura de exceção para não travar em arquivo
  inexistente ou sem permissão.
- **ex1** retoma o ex0 e soma escrita: transformar o conteúdo lido,
  perguntar (via `input()`) um nome de arquivo opcional, e só escrever se
  algo foi digitado.
- **ex2** retoma o ex1 trocando `input()`/`print()` de mensagem de erro
  pelos streams explícitos — a leitura de nome de arquivo passa a vir de
  `sys.stdin`, e erros passam a ir para `sys.stderr` em vez de se misturar
  com a saída normal.
- **ex3** reencena leitura e escrita dos exercícios anteriores dentro de
  uma única função com assinatura fixa, usando `with` pela primeira vez no
  módulo, e devolvendo sucesso/erro como valor de retorno em vez de deixar
  a exceção propagar.

## Erros comuns

- Tratar o retorno de `open()` como se já fosse o conteúdo do arquivo — é
  preciso chamar `.read()` (ou `.readline()`) explicitamente sobre o objeto
  devolvido.
- Esquecer `.close()` nos exercícios em que `with` ainda não é permitido —
  o arquivo continua "ocupado" até o programa terminar ou o `.close()` ser
  chamado, o que pode causar comportamento inesperado em escrita.
- Capturar `Exception` genérico em vez de `OSError` (ou uma subclasse
  específica) ao redor de `open()` — funciona, mas esconde erros de
  programação não relacionados a arquivo que deveriam continuar visíveis.
- Escrever mensagem de erro com `print()` comum nos exercícios que exigem
  `sys.stderr` — a mensagem aparece no terminal do mesmo jeito, mas vai
  para o canal errado, o que só fica visível ao redirecionar `stdout` e
  `stderr` separadamente.

## Perguntas de autoavaliação

1. Por que `open()` sozinho não é suficiente para "ler o conteúdo de um
   arquivo como texto" — o que exatamente falta chamar, e sobre qual
   objeto?
2. Um bloco `with open(...) as f:` levanta uma exceção não capturada no
   meio da execução. O arquivo fica aberto ou fechado depois que a exceção
   escapa do bloco? Por quê?
3. Por que separar `sys.stdout` de `sys.stderr` faz diferença prática ao
   rodar um programa com `programa > saida.txt`, mesmo que as duas
   mensagens apareçam idênticas no terminal quando não há redirecionamento?

## Fontes consultadas

- REPL Python 3.10.11 local (via `uv run python`), para confirmar
  empiricamente: tipo concreto devolvido por `open()` em modo texto e
  binário, hierarquia de exceção de `FileNotFoundError`/`PermissionError`
  sob `OSError`, formato de `str()` dessas exceções, fechamento garantido
  de arquivo dentro de `with` mesmo com exceção escapando do bloco, e
  presença de `.readline()` em `sys.stdin`.
