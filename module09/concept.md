# module09 — Cosmic Data: Discover Pydantic Models & Validation

Ambiente: Python 3.10+ (testado em 3.12.3, Windows) | Verificado em: 2026-09-09

## Objetivo do módulo

Segundo o subject (`py9.pdf`), o módulo ensina o Pydantic v2 — uma
biblioteca de validação de dados — através de três exercícios com
tema espacial que sobem em dificuldade: um modelo simples com regras por
campo (`ex0`), regras de negócio que cruzam vários campos (`ex1`), e
modelos que contêm outros modelos (`ex2`). O fio condutor é a ideia de que
dado que entra num sistema precisa ser checado *na fronteira*, e que
declarar as regras junto do tipo é melhor do que espalhar `if` pelo código.

## Pydantic: validação declarada no tipo

**TL;DR**: Pydantic é uma biblioteca que valida dados na hora de criar um
objeto. Você declara "este campo é um inteiro entre 1 e 20"; se alguém
passar 25 ou `"banana"`, o Pydantic recusa com uma mensagem explicando o
que deu errado, em vez de deixar o dado ruim entrar no programa.

<details>
<summary><strong>🔍 Aprofundando: BaseModel vs dataclass, e quando a validação dispara</strong></summary>

> Um modelo Pydantic é uma classe que herda de `BaseModel`. Cada linha
> `nome: tipo` dentro dela vira um campo validado — não se escreve
> `__init__`.
>
> A `@dataclass` da biblioteca padrão também transforma `nome: tipo` em
> campo, mas **não valida nada em runtime**: a anotação é só documentação
> para ferramentas estáticas. `Estacao(crew_size="muitos")` com dataclass
> simplesmente guarda a string. `BaseModel` gera, no momento em que a
> classe é definida, um schema de validação (compilado em Rust, no pacote
> `pydantic-core`) que roda a cada construção.
>
> A validação dispara em três situações: na construção (`Model(...)`), em
> `Model.model_validate(dict)` e em `Model.model_validate_json(str)`. Por
> padrão **não** roda em atribuição depois (`obj.campo = valor` passa
> batido) — isso só liga com `model_config = {"validate_assignment": True}`.
>
> Se vários campos falham, o Pydantic **não para no primeiro**: coleta
> todos e levanta um único `ValidationError` no fim. Verificado (Python
> 3.12.3, pydantic 2.13.5) — dois campos inválidos produzem
> `error_count() == 2`. Isso importa para o `main()` dos exercícios: um
> único `try/except ValidationError` captura o objeto inteiro.

</details>

## Field: constraints por campo

**TL;DR**: `Field()` é como você anexa regras a um campo — tamanho de
string, faixa de número, valor padrão. Vai no lado direito da declaração:
`tag: str = Field(min_length=3, max_length=10)`.

<details>
<summary><strong>🔍 Aprofundando: os parâmetros e as mensagens que o Pydantic gera</strong></summary>

> Parâmetros usados no módulo:
>
> | Constraint | Significado | Aplica a |
> |---|---|---|
> | `min_length` / `max_length` | comprimento | `str` e coleções (`list`) |
> | `ge` / `le` | ≥ / ≤ (inclusivo) | números |
> | `gt` / `lt` | > / < (exclusivo) | números |
> | `default=...` | valor se o campo for omitido | qualquer |
>
> "3-10 caracteres" (inclusivo nas duas pontas) → `min_length=3,
> max_length=10`. "1-20 people" → `ge=1, le=20` (não `lt=20`, que
> rejeitaria o próprio 20). Em Pydantic v2 use `min_length`/`max_length`
> também para listas; `min_items`/`max_items` são o nome antigo,
> depreciado.
>
> As mensagens que o Pydantic produz para essas violações (verificado):
>
> ```
> Input should be less than or equal to 20    [type=less_than_equal]
> Input should be greater than or equal to 1  [type=greater_than_equal]
> String should have at least 3 characters    [type=string_too_short]
> String should have at most 10 characters    [type=string_too_long]
> List should have at least 1 item ...         [type=too_short]
> ```
>
> Você nunca escreve essas strings — o "Expected validation error" do
> subject (`Input should be less than or equal to 20`) sai literalmente de
> um campo com `le=20` recebendo `> 20`. O `main()` só imprime o
> `ValidationError` capturado.
>
> Estilo equivalente e mais amigável ao mypy:
> `tag: Annotated[str, Field(min_length=3, max_length=10)]` — separa o tipo
> das regras.

</details>

## Coerção automática de tipos

**TL;DR**: Pydantic tenta converter o valor para o tipo declarado antes de
reclamar. String `"7"` num campo `int` vira o inteiro `7`; string
`"2024-01-15T10:30:00"` num campo `datetime` vira um objeto `datetime` de
verdade.

<details>
<summary><strong>🔍 Aprofundando: "lax mode", a assimetria int/float, e o que não converte</strong></summary>

> Por padrão o Pydantic v2 roda em *lax mode*: aceita conversões "seguras e
> sem perda". Verificado no ambiente:
>
> | Você passa | Campo | Resultado |
> |---|---|---|
> | `"7"` | `int` | `7` |
> | `"50.5"` | `float` | `50.5` |
> | `"2024-01-15T10:30:00"` | `datetime` | `datetime(2024, 1, 15, 10, 30)` |
> | `"true"`, `"yes"`, `"1"`, `1` | `bool` | `True` |
> | `"0"`, `"no"` | `bool` | `False` |
> | `"2"` | `bool` | **erro** — não é booleano reconhecível |
> | `7.5` | `int` | **erro** — `int_from_float`, tem parte fracionária |
> | `"not-a-date"` | `datetime` | **erro** — `datetime_from_date_parsing` |
>
> `"7"` → `7` é sem perda; `7.5` → `7` perderia informação, então é
> recusado. Já `7` → `7.0` (int num campo float) é aceito. Essa assimetria
> é intencional.
>
> Datas: o parser aceita ISO 8601 (com `Z` ou offset) e int/float como
> *timestamp Unix*. Não aceita formatos livres como `"15/01/2024"`.
>
> Para exigir o tipo exato existe `strict=True` (no `Field`, no tipo, ou no
> `model_config`). O módulo não pede isso — mas a coerção é uma escolha,
> não uma imposição.
>
> **Conexões:**
> - `Histórico:` em Pydantic v1 a coerção era mais agressiva; a v2 apertou as regras no rewrite em Rust (pydantic-core).

</details>

## Campos opcionais e defaults

**TL;DR**: um campo com valor default pode ser omitido na criação.
`Optional[str]` (ou `str | None`, em 3.10+) significa "aceita uma string ou
`None`".

<details>
<summary><strong>🔍 Aprofundando: a pegadinha de "Optional com constraint"</strong></summary>

> Todo campo Pydantic é obrigatório por padrão. `Optional[str]` sozinho
> ainda é obrigatório — só passa a aceitar `None` como valor; para poder
> *omitir* precisa de `= None` também.
>
> Juntar "opcional" + "max 200 caracteres" tem uma sutileza: a constraint
> de `max_length` deve valer só no ramo `str`, não no ramo `None`. Forma
> correta:
>
> ```python
> notes: Optional[str] = Field(default=None, max_length=200)
> ```
>
> Verificado: passar `None` é aceito, e passar uma string de 300 chars dá
> `string_too_long`. O Pydantic aplica a constraint condicionalmente ao
> tipo do valor dentro do `Optional`.
>
> `is_operational: bool = True` é o suficiente para "boolean, defaults to
> True" — `Optional[bool]` afrouxaria o tipo sem motivo (passaria a aceitar
> `None`, que o subject não menciona).

</details>

## Enum: conjunto fechado de valores

**TL;DR**: um `Enum` é uma lista fixa de opções válidas com nome. Em vez de
`contact_type: str` aceitar qualquer texto, `contact_type: ContactType` só
aceita os membros declarados — qualquer outra coisa é erro.

<details>
<summary><strong>🔍 Aprofundando: por que herdar de str, e a mensagem de erro</strong></summary>

> ```python
> class ContactType(str, Enum):
>     RADIO = "radio"
>     VISUAL = "visual"
>     PHYSICAL = "physical"
>     TELEPATHIC = "telepathic"
> ```
>
> `class ContactType(str, Enum)` faz cada membro ser **também uma string**.
> Verificado: `isinstance(c.contact_type, str)` → `True`, e
> `c.contact_type == "radio"` → `True`. Isso permite comparar direto com
> string nas regras de negócio e serializar para JSON como `"radio"` em vez
> de `"ContactType.RADIO"`.
>
> Sem herdar de `str`: `model_dump()` devolve o membro
> (`{'e': <PlainE.A: 'a'>}`), `model_dump_json()` ainda dá `{"e":"a"}`, mas
> `contact_type == "radio"` seria `False` — precisaria de
> `contact_type.value == "radio"` ou `is ContactType.RADIO`.
>
> Ao criar o modelo você passa a string (`contact_type="radio"`) e o
> Pydantic resolve para o membro. Valor fora do enum gera (verificado):
>
> ```
> contact_type
>   Input should be 'radio', 'visual', 'physical' or 'telepathic'
>   [type=enum, input_value='smoke_signal', input_type=str]
> ```
>
> O Pydantic lista as opções válidas automaticamente. Nota para o mypy: ele
> reclama de `contact_type="radio"` num campo tipado `ContactType`; passar
> o membro (`ContactType.RADIO`) satisfaz a checagem estática, e em runtime
> a string funcionaria igual.
>
> Em Python 3.11+ existe `enum.StrEnum`, açúcar para `(str, Enum)`. Como o
> subject exige apenas 3.10+, `(str, Enum)` é a forma portável.

</details>

## @model_validator(mode="after"): regras entre campos

**TL;DR**: é um método decorado que roda **depois** de todos os campos já
terem sido validados individualmente. Dentro dele você tem o objeto pronto
(`self`) e checa combinações: "campo A e campo B juntos fazem sentido?". Se
não, você levanta `ValueError`.

<details>
<summary><strong>🔍 Aprofundando: after vs before, raise vs return, e o "return self"</strong></summary>

> **`mode="after"`**: recebe `self` — a instância já construída, todos os
> campos do tipo certo e dentro das constraints de `Field`. É um método de
> instância normal. Use para regras de negócio que leem valores finais.
>
> **`mode="before"`**: recebe os dados crus (normalmente um `dict`) *antes*
> de qualquer parsing. É `@classmethod`. Use para normalizar entrada
> (renomear chaves, preencher default calculado). Verificado:
> `before() got: dict -> {'x': 1, 'y': 2}`.
>
> **Como sinalizar falha**: dentro do validator você levanta
> `raise ValueError("mensagem")` (ou `AssertionError`). O Pydantic
> **captura** essa exceção e a re-embrulha num `ValidationError` com
> `type=value_error`. Verificado:
>
> ```
> 1 validation error for AlienContact
>   Value error, Telepathic contact requires at least 3 witnesses
>   [type=value_error, input_value={...}, input_type=dict]
> ```
>
> O `loc` fica vazio (erro do modelo, não de um campo). Não levante
> `ValidationError` você mesmo — é chato de construir.
>
> **`return self` no fim**: obrigatório. Verificado que esquecer o `return`
> num caso simples ainda funcionou, mas retornar *outra coisa* que não
> `self` dispara `UserWarning` e "isn't supported when validating via
> `__init__`" — e quebra silenciosamente em `model_validate` /
> `validate_assignment`. O subject destaca isso no "Advanced Tip".
>
> **Múltiplos validators**: se você declarar dois `@model_validator`, ambos
> rodam, na ordem de definição no arquivo. Verificado. Para regras
> relacionadas, um único método com vários `if` (cada um com seu `raise`) é
> mais legível — o `raise` já faz o short-circuit no primeiro que quebra.

</details>

## Ordem de execução: Field primeiro, model_validator depois

**TL;DR**: se um campo já falha na validação básica (ex: `signal_strength`
fora da faixa), o `@model_validator(mode="after")` **nem chega a rodar**.
Ele só executa quando o objeto inteiro passou na etapa de campos.

<details>
<summary><strong>🔍 Aprofundando: o que aparece no ValidationError</strong></summary>

> Verificado: um `AlienContact` com `signal_strength=99.0` (viola
> `Field(le=10.0)`) **e** telepático com 2 testemunhas (violaria a regra de
> negócio). O `ValidationError` traz **apenas 1 erro**
> (`error_count() == 1`): o de `signal_strength`. A regra de negócio no
> `model_validator` não rodou porque a fase de campos falhou antes.
>
> Consequência prática para o `main()`: se você quer demonstrar um erro do
> `model_validator` especificamente, todos os *outros* campos do exemplo
> inválido têm que estar válidos — só a combinação alvo é que quebra.
>
> Contraste com o comportamento de campos: dois erros de `Field` aparecem
> juntos na mesma passada (`error_count() == 2`). O `model_validator` é uma
> passada *posterior* que nem começa se a primeira falhou.

</details>

## Modelos aninhados: um modelo como tipo de campo

**TL;DR**: `SpaceMission` tem um campo `crew: List[CrewMember]`. Quando você
cria uma missão passando uma lista de dicionários, o Pydantic valida cada
dicionário como um `CrewMember` sozinho — recursivamente — antes de validar
a missão. Você não escreve nenhum loop para isso.

<details>
<summary><strong>🔍 Aprofundando: camadas de validação e o loc multi-nível</strong></summary>

> Verificado (Python 3.12.3, pydantic 2.13.5): ao passar
> `crew=[{...}, {...}]` (dicts), `m.crew[0]` sai como um `CrewMember` de
> verdade (`isinstance(m.crew[0], CrewMember)` → `True`), com `rank` já
> convertido para o `Enum`. É o mesmo mecanismo da coerção string →
> `datetime`, só que "dict → modelo", em cascata.
>
> A validação acontece em camadas, de dentro para fora:
>
> 1. Cada `CrewMember` da lista é validado individualmente — seus `Field` e
>    (se tivesse) seu próprio `model_validator`.
> 2. A lista `crew` em si — `min_length` / `max_length`.
> 3. Só então o `@model_validator(mode="after")` de `SpaceMission` roda,
>    com `self.crew` já sendo uma lista de `CrewMember` válidos.
>
> **Se um `CrewMember` falha**, o erro aponta o caminho completo.
> Verificado — segundo membro com `age=15`:
>
> ```
> crew.1.age
>   Input should be greater than or equal to 18 [type=greater_than_equal]
> ```
>
> `loc == ('crew', 1, 'age')` → campo `age`, do item de índice `1`, dentro
> de `crew`. Esse é o "Think About" do subject: o erro é preciso sobre
> *qual* membro e *qual* campo.
>
> **Se um `CrewMember` falha, o `model_validator` da missão nem roda.**
> Verificado: uma missão com um único cadete `age=15` — isso viola o
> `Field` do membro *e* a regra "must have a Commander/Captain". O
> `ValidationError` traz **1 erro só** (`crew.0.age`). Mesma lógica de
> "Field antes de model_validator", agora com um nível a mais.
>
> Dentro do `model_validator` da missão, as regras que dependem do
> *conjunto* de membros se escrevem lendo `self.crew` com list
> comprehension / `all()` / `sum(1 for ...)`:
>
> | Regra do subject | Como se lê `self.crew` |
> |---|---|
> | ≥ 1 Commander ou Captain | filtrar por `m.rank in (COMMANDER, CAPTAIN)` e checar se sobrou alguém |
> | > 365 dias: 50% com 5+ anos | contar `m.years_experience >= 5` e comparar com `len(self.crew)` |
> | todos ativos | `all(m.is_active for m in self.crew)` |
>
> `crew: list` sem parametrizar (em vez de `list[CrewMember]`) faz o
> Pydantic *não* validar os itens como modelos — o parâmetro é o que liga
> a validação recursiva.

</details>

## Regras e restrições do subject

- **Pydantic 2.x, nada de `@validator`.** `@validator` é a API do Pydantic
  v1, depreciada. O v2 divide em `@field_validator` (um campo) e
  `@model_validator` (modelo inteiro). O subject quer a API atual, não a
  legada que ainda aparece em tutoriais antigos.
- **Python 3.10+.** Habilita `str | None` (PEP 604) como sinônimo de
  `Optional[str]`, entre outras coisas.
- **flake8 + type annotations completas (mypy).** Modelos Pydantic *são*
  anotações de tipo — o módulo força você a pensar nos tipos, que é o
  ponto. mypy pega incoerência antes do runtime.
- **`Authorized: None` em todos os exercícios.** Só `pydantic` + biblioteca
  padrão (`enum`, `datetime`). Sem libs de conveniência: você exercita a
  API crua.
- **"Exception handling should protect the data streams".** O `main()` com
  dado inválido não pode derrubar o programa — capturar `ValidationError`
  é o mecanismo.
- **"Remember to `return self`" (Advanced Tip do ex1).** Um validator
  "after" que não devolve a instância quebra silenciosamente fora do
  `__init__`.

## Correlação com exercícios existentes

- **ex0 (`space_station.py`)** exercita validação por campo: `Field` com
  `min_length`/`max_length`/`ge`/`le`, um campo `datetime` que aceita
  string ISO por coerção, um `Optional[str]` com default e `max_length`, e
  um `bool` com default. O `main()` demonstra a coerção imprimindo o tipo
  real do campo `datetime` depois da construção.
- **ex1 (`alien_contact.py`)** acrescenta um `Enum` (conjunto fechado) e um
  `@model_validator(mode="after")` com quatro regras de negócio que cruzam
  campos (prefixo do id, tipo × verificação, tipo × nº de testemunhas,
  força do sinal × mensagem). Cada regra levanta `ValueError`; o `main()`
  escolhe um exemplo inválido cujos campos são todos válidos, para que seja
  o `model_validator` a rejeitar.
- **ex2 (`space_crew.py`)** compõe os dois anteriores: um `Enum` (`Rank`),
  um modelo `CrewMember` só com `Field`, e um `SpaceMission` que tem
  `List[CrewMember]` como campo. O `@model_validator` da missão lê a lista
  inteira (`leaders`, contagem de experientes, `all(... is_active)`).
  Nenhum conceito novo de Pydantic — é a combinação de ex0 e ex1 num nível
  de aninhamento.

## Erros comuns

- Confundir `ge`/`le` (inclusivo) com `gt`/`lt` (exclusivo). "1-20" inclui
  o 20 → `le=20`.
- Esquecer o `= None` num campo opcional e estranhar que ele continua
  obrigatório.
- Achar que a coerção sempre acontece. `7.5` num `int` *não* vira `7` — é
  erro; só conversões sem perda passam.
- Escrever a mensagem de erro à mão no `main()`. A mensagem de constraint é
  gerada pelo Pydantic; você só a imprime a partir do `ValidationError`.
- Usar `@validator` copiado de tutorial antigo — depreciado em v2, o
  subject proíbe explicitamente.
- Usar `@field_validator` para uma regra que cruza campos — `field_validator`
  vê um campo só; comparar dois campos exige `model_validator`.
- Esquecer `return self` no fim do `model_validator(mode="after")`.
- Levantar `ValidationError` manualmente dentro do validator — levante
  `ValueError`, o Pydantic embrulha.
- Enum sem herdar de `str` e depois comparar `campo == "valor"` esperando
  `True` (dá `False` — seria `.value` ou `is`).
- Testar uma regra de negócio com outros campos inválidos: o
  `model_validator` nem roda, você vê só o erro de `Field`.
- No ex2, `crew: list` sem parametrizar (`list[CrewMember]`) — o Pydantic
  não valida os itens como modelos.
- No ex2, usar `min_items`/`max_items` na lista — depreciado; é
  `min_length`/`max_length`.

## Perguntas de autoavaliação

1. `notes: Optional[str] = Field(default=None, max_length=200)` — o que
   acontece ao passar `notes=None`? E uma string de 250 caracteres? Por que
   os dois casos são tratados diferente?
2. Por que `crew_size="15"` é aceito mas `crew_size=15.5` não? Qual
   princípio o Pydantic está seguindo?
3. Se você cria um modelo inválido **fora** de um `try/except`, o que
   acontece com o código depois dele?
4. Por que a regra "telepático exige ≥ 3 testemunhas" tem que ir num
   `@model_validator` e não num `Field` de `witness_count`?
5. Se um `AlienContact` viola o prefixo do id **e** tem `signal_strength`
   fora da faixa, quantos erros o `ValidationError` reporta? Qual(is)? Por
   quê?
6. Ao passar `crew=[{...dict...}]`, o que `type(mission.crew[0])` retorna?
   Quem fez essa conversão e quando?
7. Se o terceiro membro da tripulação tem `age=200`, qual é o `loc` do
   erro? O `@model_validator` de `SpaceMission` chega a rodar?
8. Qual a diferença entre `crew: list[CrewMember]` e `crew: list` no que o
   Pydantic valida?

## Fontes consultadas

- Execução real no ambiente: Python 3.12.3, `pydantic 2.13.5` — toda
  afirmação sobre coerção, mensagens de erro, `error_count()`, ordem
  Field→model_validator, `loc` multi-nível, `return self`, e serialização
  de enum foi rodada e verificada.
- https://docs.pydantic.dev/2.13/concepts/models/ — `BaseModel`, campos
  obrigatórios vs opcionais, modelos aninhados
- https://docs.pydantic.dev/2.13/concepts/fields/ — parâmetros de `Field`
- https://docs.pydantic.dev/2.13/concepts/validators/#model-validators —
  `@model_validator`, `mode="before"`/`"after"`, `return self`
- https://docs.pydantic.dev/2.13/concepts/conversion_table/ — tabela de
  coerção lax/strict
- https://docs.pydantic.dev/2.13/concepts/enums/ — enums em Pydantic
- https://docs.python.org/3/library/enum.html — `Enum`, `StrEnum` (3.11+)
