# module01 — Code Cultivation: Object-Oriented Garden Systems

Ambiente: Python 3.10.11 | Verificado em: 2026-08-06

## Objetivo do módulo

O subject introduz a estrutura básica de um programa Python (ponto de
entrada, `__name__`) e progride para Programação Orientada a Objetos:
classes, atributos, métodos, encapsulamento, herança e conceitos mais
avançados como `staticmethod`, `classmethod` e classes aninhadas. Todo o
módulo gira em torno de um único domínio (um sistema de gestão de jardim
comunitário), reaproveitado e evoluído a cada exercício.

## `__name__ == "__main__"`

**TL;DR**: todo módulo Python tem uma variável interna `__name__`. Quando
um arquivo é executado diretamente (`python3 arquivo.py`), o Python atribui
`__name__ = "__main__"` a esse módulo. Se o mesmo arquivo for **importado**
por outro (`import arquivo`), `__name__` passa a valer o nome do arquivo,
não `"__main__"`. O bloco `if __name__ == "__main__":` roda só no primeiro
caso — é um filtro para separar "definir comportamento" de "executar
comportamento ao ser importado".

<details>
<summary><strong>🔍 Aprofundando: por que isso importa antes de existir import entre arquivos do projeto</strong></summary>

> Sem esse `if`, qualquer código solto no nível do módulo executaria
> automaticamente toda vez que o arquivo fosse importado — quase sempre
> indesejado, porque quem importa só quer as definições (funções/classes)
> disponíveis, não efeitos colaterais disparados no momento do import.
>
> ```
> # arquivo: exemplo_modulo.py
> def saudacao() -> None:
>     print("Oi!")
>
> if __name__ == "__main__":
>     saudacao()
> ```
>
> Rodando `python3 exemplo_modulo.py` imprime "Oi!" (`__name__` vale
> `"__main__"`). Se outro arquivo fizer `import exemplo_modulo`, nada é
> impresso automaticamente — `saudacao` fica disponível, mas o bloco `if`
> não dispara, porque ali `__name__` vale `"exemplo_modulo"`.
>
> O valor prático completo desse padrão só fica óbvio quando se divide
> código em múltiplos arquivos e um importa o outro — tema de um projeto
> futuro, mas a base conceitual já é introduzida aqui.

</details>

## Shebang (`#!`)

**TL;DR**: a linha `#!/caminho/para/interpretador` no topo de um script diz
ao sistema operacional qual programa deve executá-lo quando chamado
diretamente (`./arquivo.py` em vez de `python3 arquivo.py`). Não é sintaxe
do Python — é uma convenção do Unix/Linux, reconhecida pelo kernel, válida
para qualquer tipo de script (`.sh`, `.py`, `.rb`, etc).

<details>
<summary><strong>🔍 Aprofundamento: quem lê a shebang, e por que ela não afeta o Python em si</strong></summary>

> Quando um arquivo executável começa com `#!`, o kernel lê o resto dessa
> primeira linha como o caminho de um interpretador, e invoca esse programa
> passando o arquivo como argumento. Duas formas comuns:
>
> - `#!/usr/bin/python3` — caminho fixo, quebra se o Python estiver em outro
>   lugar.
> - `#!/usr/bin/env python3` — usa `env` para procurar `python3` no `PATH`,
>   mais portável (funciona em ambientes virtuais).
>
> Para o próprio interpretador Python, a shebang é só um comentário comum
> (`#`) — ela só importa para o kernel, no caso específico de execução
> direta via `./arquivo.py` com permissão de execução (`chmod +x`).
>
> ⚠️ não verificado: comportamento exato em Windows nativo (fora de
> WSL/Git Bash) — a shebang é convenção Unix; a associação de `.py` a um
> interpretador no Windows passa por outro mecanismo (registro do SO / `py
> launcher`), não testado neste ambiente.

</details>

## Classes, atributos e `__init__`

**TL;DR**: uma classe é um molde para criar objetos com a mesma estrutura
(mesmos atributos) mas valores próprios. `__init__` é o método especial
chamado automaticamente quando uma instância é criada — nele, os
parâmetros recebidos viram atributos (`self.algo = algo`), disponíveis em
todo método futuro daquele objeto via `self`.

<details>
<summary><strong>🔍 Aprofundando: anotação de tipo solta vs. atributo de fato</strong></summary>

> ```python
> class Exemplo:
>     valor: int      # só anotação — não cria atributo real
>
>     def __init__(self, valor: int) -> None:
>         self.valor = valor   # aqui sim, atributo de instância de verdade
> ```
>
> `valor: int` sozinho (sem `=`), no corpo da classe, não cria um atributo
> utilizável — só registra o tipo em `Exemplo.__annotations__`, sem valor
> nenhum atribuído. `hasattr(Exemplo, 'valor')` seria `False` até uma
> instância passar pelo `__init__`. Esse padrão de anotação solta é mais
> usado com o decorator `@dataclass`, que lê essas anotações para gerar o
> `__init__` automaticamente — sem `@dataclass`, é só documentação opcional
> para quem lê o código ou para ferramentas como `mypy`/IDEs.

</details>

## Encapsulamento: convenção `_protected` vs. mangling `__private`

**TL;DR**: um único underscore no início de um atributo (`_altura`) é uma
*convenção* — um sinal para outros programadores de "acesse isso só através
de um método, não diretamente". O Python não impede o acesso de fato. Já
dois underscores (`__altura`) ativam o *name mangling*: o Python renomeia
o atributo internamente, o que resolve um problema diferente (colisão de
nomes em cadeias de herança), não é sobre disciplina de acesso.

<details>
<summary><strong>🔍 Aprofundando: o que name mangling faz de verdade</strong></summary>

> ```
> >>> class Exemplo:
> ...     def __init__(self):
> ...         self.__x = 1
> ...
> >>> Exemplo().__dict__
> {'_Exemplo__x': 1}
> ```
>
> `__x` foi renomeado para `_Exemplo__x` no dicionário interno do objeto.
> Isso existe para evitar que uma subclasse acidentalmente sobrescreva um
> atributo "privado" da classe-mãe com o mesmo nome — não é uma proteção de
> acesso mais forte que a convenção simples, é um mecanismo distinto, com
> outro propósito. Por isso o subject deste módulo pede especificamente a
> convenção de um underscore, não o mangling: o objetivo pedagógico aqui é
> disciplina de acesso via getters/setters, tema que antecede o problema
> que o mangling resolve.

</details>

## Validação centralizada: por que o `__init__` também deve usar o setter

**TL;DR**: se existe um método que valida um dado (ex: rejeitar um valor
negativo), todo caminho que define esse dado — incluindo a criação do
objeto — deve passar por essa mesma validação. Caso contrário, o `__init__`
vira uma porta dos fundos que ignora a regra que o setter aplica.

<details>
<summary><strong>🔍 Aprofundamento: uma única fonte de verdade</strong></summary>

> Duplicar a lógica de validação (uma vez dentro do `__init__`, outra
> dentro do setter) cria duas fontes de verdade que podem divergir com o
> tempo — se a regra mudar, é fácil atualizar um lugar e esquecer o outro.
> Chamar o setter de dentro do `__init__` elimina essa duplicação: existe
> uma única definição do que é "válido", reaproveitada em todos os pontos
> de entrada dos dados.
>
> Um padrão comum: atribuir primeiro um valor padrão seguro diretamente
> (garantindo que o atributo sempre existe), depois chamar o setter para
> tentar sobrescrever com o valor recebido — se a validação falhar, o
> objeto ainda fica em um estado consistente.

</details>

## Herança e `super()`

**TL;DR**: uma subclasse herda atributos e métodos de uma classe-mãe, e
pode adicionar ou sobrescrever comportamento. `super()` permite chamar a
versão do método da classe-mãe de dentro da subclasse — usado tanto para
reaproveitar a lógica de `__init__` quanto a de métodos como `show()`, sem
duplicar código.

<details>
<summary><strong>🔍 Aprofundamento: sobrescrever sem duplicar</strong></summary>

> ```python
> class Animal:
>     def __init__(self, nome: str) -> None:
>         self.nome = nome
>
>     def descricao(self) -> None:
>         print(f"Nome: {self.nome}")
>
>
> class Cachorro(Animal):
>     def __init__(self, nome: str, raca: str) -> None:
>         super().__init__(nome)
>         self.raca = raca
>
>     def descricao(self) -> None:
>         super().descricao()
>         print(f"Raça: {self.raca}")
> ```
>
> `Cachorro.descricao()` não reescreve a linha do nome — ela chama
> `super().descricao()` para rodar a versão da classe-mãe primeiro, e só
> acrescenta a parte nova. Isso evita que a mesma lógica de formatação
> exista duplicada em cada subclasse, e centraliza qualquer mudança futura
> num único lugar (a classe-mãe).

</details>

## `staticmethod` vs. `classmethod` vs. método de instância

**TL;DR**: um método normal recebe `self` (a instância) automaticamente.
Um `classmethod` recebe `cls` (a própria classe) — comum para criar
instâncias de formas alternativas ao `__init__` padrão. Um `staticmethod`
não recebe nem `self` nem `cls` — comporta-se como uma função comum que só
"mora" dentro da classe por organização lógica.

<details>
<summary><strong>🔍 Aprofundamento: por que classmethod usa `cls` em vez do nome da classe</strong></summary>

> ```python
> class Item:
>     @classmethod
>     def desconhecido(cls) -> "Item":
>         return cls("Sem nome")
> ```
>
> Usar `cls(...)` em vez de escrever `Item(...)` diretamente importa quando
> existe herança: se uma subclasse herdar esse `classmethod` sem
> sobrescrevê-lo, `cls` será a subclasse no momento da chamada, não
> `Item`. Escrever `Item(...)` fixo faria a fábrica sempre devolver a
> classe-mãe, mesmo chamada a partir da subclasse — perdendo a informação
> de qual classe realmente pediu a criação. Esse é um erro fácil de não
> perceber porque, testado só a partir da classe-mãe, o comportamento
> parece idêntico.

</details>

## Classe aninhada (nested class)

**TL;DR**: uma classe definida dentro do corpo de outra. Serve para
agrupar um conceito que só faz sentido no contexto da classe externa — por
exemplo, dados estatísticos de uso de um objeto, que não têm razão de
existir como classe solta no módulo. Uma classe aninhada não tem acesso
mágico à classe que a contém; ela é instanciada e usada como qualquer
outro atributo.

<details>
<summary><strong>🔍 Aprofundamento: herança entre classes aninhadas, e um limite do mypy</strong></summary>

> Se uma subclasse precisa de uma variação da classe aninhada da mãe (ex:
> um contador extra que só faz sentido para um tipo específico), o caminho
> mais direto é herdar da classe aninhada da mãe, em vez de duplicar os
> atributos e métodos comuns:
>
> ```python
> class Base:
>     class _Info:
>         def __init__(self) -> None:
>             self.chamadas = 0
>
>     class _InfoEspecial(_Info):
>         def __init__(self) -> None:
>             super().__init__()
>             self.chamadas_extra = 0
> ```
>
> Um detalhe de tipagem estática vale atenção: se `self._info` é
> inicializado em `Base.__init__` como `_Info`, e uma subclasse o
> reatribui para `_InfoEspecial()` dentro do próprio `__init__` da
> subclasse, o `mypy` continua tratando o atributo, herdado da classe-mãe,
> como `_Info` — porque o tipo é inferido a partir da primeira atribuição
> encontrada na hierarquia. Chamar um método que só existe em
> `_InfoEspecial` a partir desse atributo gera erro de tipo, mesmo o
> código rodando sem problema em tempo de execução (Python não checa
> tipos em runtime). A correção é anotar explicitamente o atributo, na
> subclasse, com o tipo mais específico: `self._info: Base._InfoEspecial
> = Base._InfoEspecial()`.

</details>

## Regras e restrições do subject

- **Lista de builtins/recursos autorizados cresce a cada exercício**
  (`print()` no ex0, depois `range()`/`round()`, depois `super()`, depois
  `staticmethod()`/`classmethod()`). A 42 restringe deliberadamente o
  vocabulário disponível para forçar o uso do conceito sendo ensinado
  naquele exercício específico, em vez de pular direto para uma ferramenta
  mais avançada antes de entender o fundamento.
- **`class`/`def` não entram na lista de autorizados** — são palavras-chave
  fundamentais da linguagem, não builtins/funções.
- **Encapsulamento exige a convenção `_protegido`, não o mangling
  `__privado`** — ver seção específica acima.
- **flake8 e mypy obrigatórios em todos os exercícios deste módulo**
  (diferente do module00, onde mypy só era exigido a partir de um
  exercício específico) — type hints em todas as funções/métodos desde o
  início.

## Correlação com exercícios existentes

- **ex0** exercita `__name__`/shebang isoladamente, sem classe.
- **ex1–ex3** introduzem classe, atributos, métodos que alteram estado
  (`grow()`/`age()`), e inicialização direta via `__init__`.
- **ex4** aplica encapsulamento sobre a classe já existente — getters,
  setters e validação, sem trocar a estrutura de dados.
- **ex5** introduz herança sobre a mesma classe-base, criando
  especializações que reaproveitam `__init__` e `show()` via `super()`.
- **ex6** combina tudo dos exercícios anteriores com conceitos novos
  (`staticmethod`, `classmethod`, classe aninhada, uma segunda camada de
  herança) — é o exercício mais denso do módulo, e o subject avisa
  explicitamente que a avaliação vai focar em como os componentes
  interagem entre si, não só se cada peça funciona isolada.

## Erros comuns

- Referenciar um **método** e um **atributo protegido** de nomes parecidos
  (ex: `self.idade` sendo o método, `self._idade` sendo o dado) — o Python
  não impede a coexistência dos dois nomes, então o erro não aparece como
  exceção óbvia na hora de definir, só quando o valor errado (a referência
  ao método, não o dado) acaba sendo usado onde um número era esperado.
- Reaproveitar o mesmo tipo de aspas (`"`) tanto para o f-string externo
  quanto para uma string usada dentro das chaves `{}` — em versões do
  Python anteriores à mudança de sintaxe de f-strings (PEP 701, Python
  3.12), isso é `SyntaxError`. Regra prática: se o f-string usa aspas
  duplas, o que precisar de aspas dentro das chaves usa aspas simples.
- Colocar dentro de um f-string a chamada de um método que já faz
  `print()` internamente e não tem `return` — o método imprime sua própria
  linha, e o valor interpolado no f-string acaba sendo `None` (retorno
  padrão de função sem `return` explícito), numa segunda linha
  inesperada.
- Concatenar strings adjacentes (inclusive f-strings em linhas separadas
  dentro do mesmo `print(...)`) sem espaço ou pontuação entre elas — o
  Python concatena strings adjacentes automaticamente, sem inserir nada
  entre elas, então o texto sai colado se cada pedaço não terminar/começar
  com o espaçamento certo.
- Misturar `int` e `float` num mesmo atributo ao longo do tempo (ex: criar
  com um valor inteiro, depois somar um incremento fracionário) — o
  `mypy` sinaliza a inconsistência de tipo mesmo quando o Python, em
  runtime, aceita a operação sem erro (a soma `int + float` sempre produz
  `float`).

## Perguntas de autoavaliação

1. Por que um bloco `if __name__ == "__main__":` não impede o resto do
   arquivo de ser executado quando o script roda diretamente — ele
   restringe ou habilita código?
2. Se uma classe filha herda um `classmethod` da classe-mãe sem
   sobrescrevê-lo, e a classe-mãe usa `cls(...)` para criar a instância,
   qual classe é efetivamente instanciada quando o método é chamado a
   partir da classe filha?
3. Por que centralizar uma validação (ex: "altura não pode ser negativa")
   num único setter, chamado tanto pelo `__init__` quanto por qualquer
   método que altere o dado depois, é mais seguro do que validar em cada
   ponto separadamente?

## Fontes consultadas

- REPL Python 3.10.11 local, para os exemplos de anotação de classe,
  name mangling, e comportamento de f-string
- https://peps.python.org/pep-0484/ (compatibilidade `int`/`float` em
  type hints)
- https://peps.python.org/pep-0701/ (mudança de sintaxe de f-strings no
  Python 3.12)
