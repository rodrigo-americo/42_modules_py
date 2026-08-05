# module00 — Growing Code: Python Fundamentals

Ambiente: Python 3.10.11 | Verificado em: 2026-08-04

## Objetivo do módulo

O subject introduz a sintaxe básica de Python através de 8
exercícios que simulam dados de uma horta comunitária: `print()`, `input()`,
conversão de tipo, condicionais, iteração vs. recursão, e por fim type hints
obrigatórios. Cada exercício pede **só uma função** por arquivo — sem bloco
`if __name__ == "__main__":`, sem chamada direta, sem código fora de função.

## Expressões e saída com `print()`

**TL;DR**: `print()` mostra texto na tela. F-strings (`f"..."`) deixam
misturar texto fixo com o valor de variáveis sem concatenar manualmente.

<details>
<summary><strong>🔍 Aprofundando: f-string vs. concatenação</strong></summary>

> `f"Olá, {nome}"` e `"Olá, " + nome` produzem o mesmo resultado para strings,
> mas a f-string resolve conversão de tipo automaticamente — `f"Total: {n}"`
> funciona mesmo se `n` for `int`, enquanto `"Total: " + n` levanta
> `TypeError` porque `+` entre `str` e `int` não é definido.
>
> ```
> >>> n = 5
> >>> "Total: " + n
> TypeError: can only concatenate str (not "int") to str
> >>> f"Total: {n}"
> 'Total: 5'
> ```

</details>

## Entrada com `input()` e conversão de tipo

**TL;DR**: `input()` sempre devolve uma [string](../.claude/GLOSSARY.md#pep) — mesmo
se o usuário digitar `"42"`, você recebe o texto `"42"`, não o número. Por
isso `int(input(...))` aparece tanto nos exercícios: primeiro lê como texto,
depois converte.

<details>
<summary><strong>🔍 Aprofundando: por que input() não devolve int direto</strong></summary>

> Do ponto de vista do terminal, tudo que chega por `stdin` é texto — o
> Python não tem como saber se o que foi digitado devia virar `int`, `float`
> ou continuar `str`. Por isso a conversão é sempre uma etapa manual e
> explícita (`int(...)`), nunca implícita.
>
> ```
> >>> valor = input("Digite um número: ")
> Digite um número: 7
> >>> type(valor)
> <class 'str'>
> ```

</details>

## Condicionais (`if`/`elif`/`else`)

**TL;DR**: o programa escolhe um caminho de execução com base numa condição
booleana. Só o primeiro `if`/`elif` cuja condição for verdadeira roda; o
`else` é o caso "nenhuma das anteriores".

## Iteração vs. recursão

**TL;DR**: dois jeitos de repetir uma ação um número determinado de vezes.
Iteração usa um laço (`for`/`while`); recursão faz a função chamar a si
mesma, com uma condição de parada que evita repetir para sempre.

<details>
<summary><strong>🔍 Aprofundando: limite de recursão e por que ele existe</strong></summary>

> Cada chamada de função empilha um [frame](../.claude/GLOSSARY.md#frame) novo
> guardando o estado daquela chamada. Numa recursão sem parada, essa pilha
> cresce a cada chamada até estourar a memória disponível — o Python evita
> isso com um limite configurável, checado em runtime nesta instalação:
>
> ```
> >>> import sys
> >>> sys.getrecursionlimit()
> 1000
> ```
>
> Isso não é um número mágico do problema em si, é uma proteção do
> interpretador. Uma função recursiva simples de contagem, como as usadas
> neste módulo, fica muito abaixo desse teto para entradas pequenas — mas o
> limite existe justamente para casos onde a condição de parada falha (bug
> comum: esquecer o caso base, ou a chamada recursiva nunca converge para
> ele).

</details>

## Type hints

**TL;DR**: anotação opcional (nos exercícios 0–6) ou obrigatória (exercício
7) do tipo esperado de parâmetros e retorno, tipo
`def somar(a: int, b: int) -> int:`. Não muda o comportamento em runtime —
é documentação lida por humanos e por ferramentas externas como `mypy`.

<details>
<summary><strong>🔍 Aprofundando: type hints não são verificados pelo Python</strong></summary>

> ```
> >>> def dobro(x: int) -> int:
> ...     return x * 2
> ...
> >>> dobro("a")
> 'aa'
> ```
>
> O Python aceita essa chamada sem reclamar — `x: int` é só uma anotação,
> ignorada pelo interpretador em tempo de execução. Quem verifica se o tipo
> declarado bate com o uso real é uma ferramenta externa, `mypy` neste caso,
> rodada separadamente (`uv run mypy arquivo.py`), não o `python3
> arquivo.py`.

</details>

## Regras e restrições do subject

- **Um arquivo por exercício, só a função pedida.** Sem `main`, sem chamada
  direta no módulo. Isso força separar "definir o comportamento" de
  "executar o comportamento" — quem importa o arquivo decide quando chamar
  a função, o arquivo em si só declara.
- **Lista de builtins autorizados por exercício** (ex: `input()`, `int()`,
  `print()`, e a partir do ex6 também `range()` e helper functions para
  recursão). A 42 restringe deliberadamente o vocabulário disponível em
  módulos iniciais para forçar o uso do que está sendo ensinado naquele
  exercício específico, em vez de pular direto para ferramentas mais
  poderosas antes de entender o fundamento.
- **flake8 obrigatório.** Verifica estilo (PEP 8) e erros lógicos simples
  (import não usado, variável não usada) — não verifica tipos nem lista de
  builtins autorizados, isso fica por conta da correção humana/moulinette.
- **mypy obrigatório a partir do exercício 7**, quando type hints deixam de
  ser recomendação e passam a ser exigência.

## Correlação com exercícios existentes

- **ex0–ex3** exercitam `print()`/`input()`/conversão de tipo isoladamente,
  sem controle de fluxo.
- **ex4, ex5** introduzem `if`/`else` sobre o valor convertido.
- **ex6** é o único exercício com duas soluções paralelas (iterativa e
  recursiva) do mesmo problema — bom ponto de comparação direta entre as
  duas técnicas, já que o subject pede saída idêntica para ambas.
- **ex7** consolida o módulo: parâmetros nomeados com type hints
  obrigatórios, múltiplos ramos condicionais, e uso de string methods em vez
  de `input()`.

## Erros comuns

- Montar uma f-string com quebra de linha (`\n`) ou espaço antes/depois de
  forma que sobra (ou falta) um espaço na saída final — fácil de não notar
  visualmente, mas quebra comparação exata de string. Vale sempre comparar a
  saída real, caractere a caractere, com o exemplo do subject antes de
  considerar um exercício pronto.
- Esquecer o ramo `else` (ou um `elif` final) para o caso "nenhuma das
  opções esperadas" — a função roda sem erro, mas silenciosamente não
  produz a saída esperada para entradas fora do previsto.
- Confundir `print()` (mostra na tela, retorna `None`) com `return`
  (devolve um valor para quem chamou a função, sem imprimir nada sozinho).

## Perguntas de autoavaliação

1. Por que `input()` sempre devolve `str`, mesmo quando o usuário digita só
   números?
2. Numa função recursiva, o que acontece se a condição de parada (caso
   base) nunca for satisfeita?
3. Se um type hint diz `-> None` mas a função tem um `return valor`, o
   Python impede a execução? Por quê?

## Fontes consultadas

- REPL Python 3.10.11 local, para `sys.getrecursionlimit()` e o exemplo de
  `TypeError` em concatenação
- https://docs.python.org/3/library/functions.html#input
