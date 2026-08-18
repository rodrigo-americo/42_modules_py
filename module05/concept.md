# module05 — Code Nexus: Polymorphic Data Streams in the Digital Matrix

Ambiente: Python 3.10.11 | Verificado em: 2026-08-18

## Objetivo do módulo

O módulo introduz orientação a objetos avançada: classes abstratas (`ABC`),
sobrescrita de método (method overriding), polymorphism e `Protocol`
(duck typing estrutural). O fio condutor é um sistema de processamento de
dados: um exercício define o contrato comum entre tipos de dado diferentes,
o seguinte roteia um stream heterogêneo para o processor certo sem checar
tipo manualmente, e o último exporta os resultados através de plugins que
não precisam herdar de nada para serem aceitos.

## `ABC`: uma classe que não pode ser instanciada sozinha

**TL;DR**: uma classe abstrata é um molde — define quais métodos toda
subclasse é obrigada a implementar, mas não pode ser instanciada
diretamente. Tentar instanciar `ABC` (ou uma subclasse que não implementou
todos os métodos abstratos) lança `TypeError`.

<details>
<summary><strong>🔍 Aprofundando: a mensagem exata do TypeError, e como o ABC sabe o que falta</strong></summary>

> ```
> >>> from abc import ABC, abstractmethod
> >>> class Shape(ABC):
> ...     @abstractmethod
> ...     def area(self) -> float: ...
> ...
> >>> Shape()
> TypeError: Can't instantiate abstract class Shape with abstract method area
> ```
>
> (comportamento confirmado em REPL Python 3.10.11 local)
>
> `ABC` usa uma metaclasse (`ABCMeta`) que rastreia, na definição da classe,
> quais nomes foram marcados com `@abstractmethod` e ainda não foram
> sobrescritos por uma subclasse concreta. Essa checagem acontece no momento
> de instanciar (`Shape()`), antes mesmo de `__init__` rodar — por isso o
> erro aparece mesmo que a classe nunca chegue a executar código próprio.

</details>

## Method overriding: mesma assinatura, comportamento próprio

**TL;DR**: overriding é quando uma subclasse redefine um método que já
existe na superclasse, mantendo o nome (e, tipicamente, a assinatura), mas
com lógica própria. Quem chama o método não precisa saber qual subclasse
está por trás — só que ela "sabe responder" àquela chamada.

<details>
<summary><strong>🔍 Aprofundando: por que a assinatura pode mudar entre validate e ingest</strong></summary>

> Um método sobrescrito pode manter a assinatura idêntica à da superclasse
> (caso de `validate(self, data: Any) -> bool` neste module — precisa
> aceitar qualquer tipo, já que quem chama não sabe de antemão o que vai
> testar) ou especializar o tipo do parâmetro (caso de `ingest`, onde cada
> subclasse já sabe, pelo próprio nome do método sendo chamado, que tipo
> esperar). Isso é coerente com o comportamento normal de sobrescrita em
> Python: o interpretador não impõe verificação de assinatura em tempo de
> execução — quem garante essa coerência é o `mypy`, checando estaticamente
> se o tipo declarado em cada `ingest` sobrescrito é compatível com o uso
> real no restante do código.

</details>

## Polymorphism: chamar o mesmo método em objetos de classes diferentes

**TL;DR**: polymorphism é poder chamar `.validate(x)` (ou qualquer método
do contrato comum) em objetos de classes diferentes, sem saber qual classe
é qual — cada um responde do seu próprio jeito, decidido em tempo de
execução pelo tipo real do objeto, não pelo tipo declarado na variável.

<details>
<summary><strong>🔍 Aprofundando: o que isso evita, e o que continua sendo O(n) mesmo assim</strong></summary>

> Sem polymorphism, rotear um elemento para o processor certo exigiria uma
> cadeia `if isinstance(p, NumericProcessor): ... elif isinstance(p,
> TextProcessor): ...` — toda vez que um processor novo fosse adicionado,
> essa cadeia precisaria crescer em um lugar central. Com polymorphism, o
> código que roteia só chama `p.validate(elemento)`; a decisão de "o que
> este dado significa para mim" fica encapsulada dentro de cada subclasse,
> e adicionar um processor novo não exige tocar em quem roteia.
>
> Isso não muda a complexidade de perguntar "qual processor aceita este
> elemento?" — ainda é preciso perguntar a cada processor registrado, no
> pior caso, até achar um que aceite (ou esgotar todos). Polymorphism
> elimina a necessidade de checar tipo manualmente; não elimina a
> necessidade de perguntar.

</details>

## `Protocol`: duck typing estrutural, sem herança

**TL;DR**: diferente de `ABC` (herança nominal explícita — `class X(Base)`),
`Protocol` define uma "forma" que qualquer classe satisfaz automaticamente
desde que tenha os métodos certos com a assinatura certa — sem herdar de
nada. O `mypy` aceita essa compatibilidade checando a estrutura, não o
parentesco de classes.

<details>
<summary><strong>🔍 Aprofundando: mypy aceita uma classe sem parentesco nenhum com o Protocol</strong></summary>

> ```python
> from typing import Protocol
>
> class Honker(Protocol):
>     def honk(self) -> str: ...
>
> class Car:
>     def honk(self) -> str:
>         return "beep"
>
> def make_it_honk(x: Honker) -> None:
>     print(x.honk())
>
> make_it_honk(Car())
> ```
> Rodando `mypy` sobre esse arquivo: `Success: no issues found in 1 source
> file` — mesmo `Car` não herdando de `Honker` em lugar nenhum. Executar o
> arquivo imprime `beep` normalmente.
>
> (comportamento confirmado com `mypy` + execução real, ambiente deste
> projeto)
>
> Fonte: [PEP 544 – Protocols: Structural subtyping](https://peps.python.org/pep-0544/)

</details>

## `bool` é subclasse de `int` — pegadinha ao validar dados numéricos

**TL;DR**: em Python, `bool` herda de `int` de verdade — `isinstance(True,
int)` é `True`. Um `validate` que aceita `int`/`float` via `isinstance` sem
excluir `bool` explicitamente vai aceitar `True`/`False` como "dado
numérico válido", o que pode não ser a intenção.

<details>
<summary><strong>🔍 Aprofundando: isinstance vs type() ao lidar com essa herança</strong></summary>

> ```
> >>> bool.__bases__
> (<class 'int'>,)
> >>> isinstance(True, int)
> True
> >>> type(True) is int
> False
> ```
>
> (comportamento confirmado em REPL Python 3.10.11 local)
>
> `isinstance(x, int)` responde "`x` é `int` ou subclasse de `int`?" — e
> `bool` é subclasse de `int`, então `True`/`False` passam. `type(x) is
> int` responde "o tipo exato de `x` é `int`?" — mais restrito, exclui
> `bool` automaticamente, mas também exclui qualquer outra subclasse
> legítima de `int` que alguém possa criar. Nenhuma das duas é "a
> correta" — a escolha depende de o programa se importar ou não com
> subclasses de `int` além de `bool`.

</details>

## Regras e restrições do subject

- **Imports autorizados: só `abc` e `typing`** — força o uso do mecanismo
  de abstração nativo da linguagem em vez de qualquer biblioteca externa,
  em todos os três exercícios.
- **`validate` sempre com assinatura `(self, data: Any) -> bool`** — tanto
  na classe abstrata quanto em toda subclasse, porque quem chama não sabe
  de antemão o tipo do dado.
- **`ingest` pode mudar de assinatura por subclasse** — cada processor
  declara o tipo específico que espera, mas ainda precisa proteger a si
  mesmo com uma exceção caso alguém chame `ingest` com dado inválido sem
  passar por `validate` antes (o subject pede esse cenário de teste
  explicitamente, avisando que ele gera um warning proposital do `mypy`).
- **`output` é concreto na classe base, nunca sobrescrito** — a lógica de
  "extrair o item mais antigo com seu rank" é igual para qualquer tipo de
  dado, então vive uma vez só na superclasse.
- **`ExportPlugin` herda de `Protocol`, não o contrário** — o plugin
  concreto (CSV, JSON) não herda de `ExportPlugin`; só precisa ter o método
  esperado com a assinatura esperada.
- **Nenhum import de `csv`/`json`** — o próprio subject pede para montar as
  strings de CSV/JSON manualmente, já que o objetivo é o plugin, não a
  biblioteca.

## Correlação com exercícios existentes

- **ex0** isola o caso mais simples: uma classe abstrata com dois métodos
  abstratos e um concreto, e três subclasses que implementam o contrato
  cada uma à sua maneira — nenhuma delas ainda interage com as outras.
- **ex1** retoma o ex0 e soma uma classe orquestradora que recebe uma lista
  heterogênea e usa polymorphism (chamando `validate`/`ingest` sem checar
  tipo) para decidir qual processor registrado trata cada elemento.
- **ex2** retoma o ex1 e soma a ponta de saída do pipeline: um `Protocol`
  que qualquer classe de exportação satisfaz sem herdar dele, e um método
  na classe orquestradora que consome um número fixo de itens de cada
  processor registrado e entrega ao plugin escolhido.

## Erros comuns

- Confundir `Any` (de `typing`, usado em anotação de tipo) com `any()` (a
  função builtin que testa truthiness de um iterável) — os nomes só
  diferem na primeira letra, mas são coisas completamente diferentes.
- Usar `@abstractclassmethod` (deprecated) quando o método deveria ser um
  método de instância comum (`self`, não `cls`) marcado só com
  `@abstractmethod`.
- Criar uma classe própria chamada `Protocol` e herdar dela, em vez de
  importar o `Protocol` de `typing` — isso perde inteiramente o mecanismo
  de duck typing estrutural que o exercício pede para demonstrar.
- Guardar estado mutável (uma lista, por exemplo) como atributo de classe
  em vez de inicializá-lo dentro de `__init__` — todas as instâncias (e
  subclasses) acabam compartilhando o mesmo objeto por engano.
- Ingerir parcialmente uma lista com um item inválido no meio, em vez de
  rejeitar a lista inteira — mistura silenciosamente dados válidos e
  inválidos, o oposto do que "proteger o stream contra corrupção" pede.

## Perguntas de autoavaliação

1. Por que uma classe que herda de `ABC` e não implementa todos os métodos
   marcados com `@abstractmethod` não pode ser instanciada — em que
   momento exatamente o Python detecta isso?
2. Se duas subclasses diferentes de `DataProcessor` tivessem, por engano, o
   mesmo comportamento de `validate` (ambas aceitando o mesmo tipo de
   dado), o que aconteceria ao registrar as duas na mesma classe
   orquestradora e enviar um elemento daquele tipo pelo stream?
3. Por que faz sentido usar `Protocol` para o sistema de plugins de
   exportação, mas `ABC` para os processors de dado — o que muda entre os
   dois cenários que justifica mecanismos diferentes?

## Fontes consultadas

- REPL Python 3.10.11 local (via `uv run python`), para confirmar
  empiricamente: mensagem exata do `TypeError` ao instanciar uma classe
  `ABC` incompleta, e a relação de herança `bool`/`int`
  (`isinstance`/`type()`).
- `mypy` (ambiente deste projeto), para confirmar que uma classe sem
  herança nenhuma de `Protocol` é aceita onde um `Protocol` é esperado,
  desde que tenha o método com a assinatura certa.
- [PEP 544 – Protocols: Structural subtyping](https://peps.python.org/pep-0544/)
