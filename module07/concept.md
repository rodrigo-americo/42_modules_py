# module07 — DataDeck: Abstract Card Architecture

Ambiente: Python 3.10 | Verificado em: 2026-09-03

## Objetivo do módulo

Segundo o subject (`py7.pdf`), o módulo constrói um sistema de cartas de
criaturas em três camadas que se apoiam: uma hierarquia de classes
abstratas para as criaturas em si (`ex0`), capacidades extras plugadas via
herança múltipla e desacopladas da hierarquia de criaturas (`ex1`), e um
sistema de estratégias de batalha que decide em tempo de execução se é
compatível com a criatura recebida (`ex2`). O fio condutor é usar
`abc.ABC`/`@abstractmethod` para forçar contratos, em vez de confiar em
convenção ou documentação.

## Abstract Factory: esconder a família por trás de uma interface

**TL;DR**: uma *abstract factory* é uma classe que sabe criar um conjunto
de objetos relacionados (aqui, a versão base e a evoluída de uma família),
mas o código que usa a fábrica nunca precisa conhecer as classes concretas
— só o contrato da fábrica e o contrato do produto.

<details>
<summary><strong>🔍 Aprofundando: por que o pacote não expõe as classes concretas</strong></summary>

> O subject pede explicitamente que o pacote `ex0` "não pode expor Creature
> concreta diretamente, só as factories". Isso não é regra arbitrária — é
> o próprio ponto do padrão: se o código cliente (o script de teste, por
> exemplo) importasse `FamiliaX` e `FamiliaXEvoluida` diretamente, ele
> ficaria acoplado a essas classes específicas. Trocar a implementação de
> uma família inteira (ou adicionar uma nova) exigiria mexer em todo lugar
> que faz esse import direto.
>
> Com a fábrica no meio, o cliente só depende de duas coisas estáveis: o
> contrato abstrato da fábrica (`criar_base`, `criar_evoluida`) e o
> contrato abstrato do produto (`atacar`, `descrever`). Trocar
> `FabricaFamiliaX` por `FabricaFamiliaY` no código cliente é uma troca de
> uma linha, porque ambas cumprem a mesma interface — o cliente nunca sabe
> qual classe concreta recebeu de volta, só que ela responde aos métodos
> esperados.
>
> Um jeito de verificar se o encapsulamento está correto: se você
> conseguir fazer `from ex0 import FabricaFamiliaX` e usá-la sem nunca
> escrever o nome de uma classe de criatura concreta no seu script de
> teste, o pacote está expondo a interface certa.

</details>

## Capabilities como mixins independentes da hierarquia principal

**TL;DR**: uma capacidade (como "pode curar" ou "pode se transformar") foi
modelada como uma classe abstrata própria, sem herdar de `Creature` — uma
criatura que tem essa capacidade herda das duas classes ao mesmo tempo
(`class Exemplo(Creature, CapacidadeX)`), em vez da capacidade estar
embutida na classe base.

<details>
<summary><strong>🔍 Aprofundando: por que separar em vez de colocar tudo em Creature</strong></summary>

> Se `curar()` fosse um método (abstrato ou não) dentro da própria
> `Creature`, toda criatura do sistema seria obrigada a ter algum
> comportamento de cura — mesmo as que nunca deveriam curar. Colocar a
> capacidade numa classe separada, e só herdar dela nas famílias que
> realmente precisam, mantém `Creature` enxuta (só o que é universal:
> nome, tipo, atacar, descrever) e evita que classes implementem métodos
> que não fazem sentido pra elas.
>
> O efeito colateral positivo é que a capacidade fica reutilizável fora do
> domínio de criaturas — o subject comenta isso diretamente ("maybe one
> day, these capabilities will not only apply to Creature"). Uma classe
> `CapacidadeCura(ABC)` sem qualquer dependência de `Creature` pode, em
> teoria, ser reaproveitada em outro sistema de objetos que precise de
> cura, sem carregar bagagem do domínio de criaturas junto.
>
> Isso também é o que permite checar capacidade via `isinstance` no `ex2`
> (ver seção seguinte) — como a capacidade é uma classe própria na cadeia
> de herança, perguntar "esse objeto tem essa capacidade?" vira perguntar
> "esse objeto é instância dessa classe?", sem precisar de nenhuma flag ou
> atributo extra pra marcar a presença da capacidade.

</details>

## Strategy pattern com validação por isinstance

**TL;DR**: cada estratégia de batalha sabe executar sua sequência de ações
(`agir`) e também sabe sozinha se é compatível com uma criatura recebida
(`é_valida`), tipicamente checando se a criatura é instância da capacidade
que aquela estratégia depende.

<details>
<summary><strong>🔍 Aprofundando: isinstance como verificação de contrato, não de nome</strong></summary>

> A alternativa mais ingênua para "essa criatura sabe curar?" seria
> `hasattr(objeto, "curar")` — checar se existe um atributo/método com
> esse nome. O problema é que isso é *duck typing* raso: qualquer objeto
> que por acaso tenha um método chamado `curar`, sem nenhuma relação com o
> contrato real de cura do sistema, passaria na checagem.
>
> `isinstance(objeto, CapacidadeCura)` é mais forte porque depende da
> hierarquia de tipos declarada, não do nome de um atributo. Só passa
> nessa checagem quem de fato herdou daquela classe abstrata — e herdar
> dela implica ter implementado o método abstrato correspondente (senão o
> Python nem deixaria instanciar a classe concreta). A checagem de tipo
> vira, na prática, uma checagem de contrato cumprido.
>
> Isso também resolve um problema de tipagem estática: dentro de uma
> função que recebe o tipo genérico da base, um bloco `if
> isinstance(objeto, CapacidadeX):` não é só uma checagem em tempo de
> execução — ferramentas de type-check como `mypy` também usam esse `if`
> para "estreitar" o tipo da variável dentro do bloco, permitindo chamar
> métodos da capacidade sem precisar de um cast manual ou de silenciar o
> checador.

</details>

## Regras e restrições do subject

- **`import typing` e `import abc` autorizados, bibliotecas externas
  proibidas** — o módulo inteiro depende só da biblioteca padrão porque o
  objetivo é o *padrão de projeto* em si, não integração com ferramentas
  externas.
- **`__init__.py` obrigatório em cada pasta de exercício** — sem ele a
  pasta não é um pacote Python importável, só um diretório qualquer (ver
  também [module06](../module06/concept.md), que aprofunda mecanismo de
  import).
- **Cada pacote só expõe suas fábricas/estratégias, nunca as classes
  concretas de criatura** — reforça o próprio ponto do abstract factory:
  o acoplamento do cliente deve ser com a interface, não com a
  implementação.
- **`eval()` e `exec()` proibidos** (regra geral do módulo) — evita que a
  lógica de despacho de comportamento (que aqui deveria vir de
  polimorfismo e `isinstance`) seja resolvida por execução dinâmica de
  string, o que anularia o propósito de praticar os padrões abstratos.

## Correlação com exercícios existentes

- **ex0** exercita abstract factory: uma classe abstrata de fábrica define
  o contrato de criação, duas fábricas concretas implementam esse contrato
  para famílias diferentes de criatura.
- **ex1** exercita mixins/herança múltipla: as capacidades vivem em
  hierarquia própria, e as criaturas que as usam herdam de duas bases ao
  mesmo tempo, construindo sobre as fábricas do `ex0`.
- **ex2** exercita strategy pattern com despacho por tipo: cada estratégia
  decide sua própria compatibilidade via `isinstance` contra as
  capacidades definidas no `ex1`, e o script de torneio orquestra fábricas
  e estratégias de forma genérica, sem `if` explícito por família de
  criatura.

## Erros comuns

- Declarar um método abstrato com uma assinatura (por exemplo, um
  parâmetro obrigatório) e implementar as versões concretas com uma
  assinatura mais permissiva (o mesmo parâmetro com valor padrão). Python
  não impede isso em tempo de execução, mas quebra a garantia de tipo: uma
  ferramenta como `mypy`, que só conhece o tipo abstrato, vai assumir o
  contrato mais restritivo — e código que só sabe que está lidando com o
  tipo abstrato vai falhar a checagem de tipos ao usar a chamada
  simplificada.
- Confundir "checar se uma ação é válida" com "executar a ação". Separar
  os dois em métodos distintos (um que só responde `bool`, outro que age)
  evita que a validação tenha efeito colateral, e permite checar
  compatibilidade sem disparar a ação de verdade.
- Esquecer que um atributo de instância (como o nome de uma criatura) não
  é um método — tentar chamá-lo com `()` gera `TypeError`, um erro que só
  aparece em tempo de execução porque o Python não distingue atributo de
  método na hora de escrever o acesso (`objeto.nome` vs `objeto.nome()`).

## Perguntas de autoavaliação

- Por que a fábrica abstrata (`CreatureFactory`) não precisa saber nada
  sobre capacidades (cura, transformação), mesmo que algumas fábricas
  concretas produzam criaturas que têm essas capacidades?
- Se uma nova capacidade fosse adicionada ao sistema (por exemplo, uma
  capacidade de "voar"), quais arquivos precisariam mudar, e quais
  poderiam continuar exatamente como estão?
- Por que `isinstance(objeto, CapacidadeX)` funciona como checagem de
  compatibilidade aqui, mas deixaria de funcionar se `CapacidadeX` fosse
  apenas um método solto dentro de `Creature` em vez de uma classe
  abstrata própria?

## Fontes consultadas

- `py7.pdf` (subject oficial do module07, lido integralmente antes de
  escrever este material).
- [docs.python.org — abc](https://docs.python.org/3/library/abc.html),
  para confirmar o comportamento de `ABC`/`@abstractmethod` referenciado
  nas seções de aprofundamento.
