# module06 — The Codex: Mastering Python's Import Mysteries

Ambiente: Python 3.10 | Verificado em: 2026-08-18

## Objetivo do módulo

Segundo o subject, o módulo constrói um único pacote Python
(`alchemy/`) ao longo de quatro partes, cada uma isolando um mecanismo de
import diferente: inicialização de pacote via `__init__.py`, formas de
alcançar um módulo (`import x` vs `from x import y`), import absoluto vs
relativo, e como quebrar uma dependência circular. Não há lógica de negócio
complexa — o próprio subject pede funções simples que só retornam strings,
porque o alvo de aprendizado é o mecanismo de import em si, não o que as
funções fazem.

## `__init__.py`: o que transforma uma pasta em pacote

**TL;DR**: um arquivo `__init__.py` dentro de uma pasta é o que diz ao
Python "isto aqui é um pacote importável, não só uma pasta qualquer". Ele
também controla o que fica visível quando alguém importa o pacote inteiro
(`import nome_do_pacote`) em vez de um arquivo específico dentro dele.

<details>
<summary><strong>🔍 Aprofundando: namespace do pacote e exposição parcial</strong></summary>

> Quando você faz `import alchemy`, o Python executa o código de
> `alchemy/__init__.py` e o resultado desse namespace de módulo é o que fica
> acessível como `alchemy.algo`. Se `__init__.py` não importar uma função
> que existe em `alchemy/elements.py`, essa função simplesmente não existe
> sob `alchemy.*` — mesmo que o arquivo esteja fisicamente na pasta. Isso é
> a base do padrão "expor só parte da API pública de um pacote": um
> `__init__.py` que faz `from .elements import create_x` mas não
> `create_y` deixa `create_y` inacessível via `import alchemy`, embora
> continue acessível via `import alchemy.elements` (import direto do
> submódulo, que não depende do que o `__init__.py` reexporta).
>
> Isso também explica por que uma função pode existir e funcionar
> perfeitamente, mas ainda assim gerar `AttributeError: module 'x' has no
> attribute 'y'` quando acessada por um caminho que passa só pelo
> `__init__.py` — não é a função que está quebrada, é a visibilidade dela
> através daquele namespace específico.

</details>

## `import x` vs `from x import y`

**TL;DR**: `import x` traz o módulo inteiro, e você acessa tudo através do
prefixo `x.algo`. `from x import y` traz só o nome `y` direto pro seu
namespace atual, sem precisar do prefixo — mas também sem trazer o resto do
módulo.

<details>
<summary><strong>🔍 Aprofundando: o que cada forma coloca no namespace</strong></summary>

> `import pacote.submodulo` só cria o nome `pacote` no escopo atual — para
> chegar no submódulo você navega por atributo (`pacote.submodulo.funcao`).
> Só importar `pacote.submodulo` sem mais nada te obriga a escrever o
> caminho inteiro toda vez que for usar algo de lá.
>
> `from pacote.submodulo import funcao` já resolve esse caminho na hora do
> import e deposita só `funcao` no namespace atual — você chama `funcao()`
> direto, sem prefixo. A troca é: menos digitação, mas se dois módulos
> diferentes exportam uma função com o mesmo nome, um `from` de cada um
> colide (o segundo sobrescreve o primeiro); com `import modulo` completo o
> prefixo evita essa colisão porque cada função vive atrás do nome do seu
> próprio módulo.

</details>

## Import absoluto vs relativo

**TL;DR**: import absoluto (`from pacote.sub import x`) sempre começa do
topo — do diretório a partir de onde o programa foi executado. Import
relativo (`from .sub import x`, `from ..outro import y`) começa de onde o
arquivo atual está dentro do próprio pacote, e só funciona para navegar
*dentro* da árvore desse pacote.

<details>
<summary><strong>🔍 Aprofundando: por que relativo não alcança fora do pacote</strong></summary>

> Um ponto (`.`) num import relativo significa "o pacote atual"; dois
> pontos (`..`) significam "o pacote pai do atual". Essa navegação é
> resolvida usando o atributo `__package__` do módulo em execução, que só
> existe e faz sentido dentro da árvore de um pacote. Um módulo solto na
> raiz do projeto (fora de qualquer pasta com `__init__.py`) não é
> ancestral de nada — não há quantidade de `..` que alcance ele a partir de
> dentro de um subpacote, porque ele nunca fez parte dessa árvore para
> começo de conversa.
>
> Na prática isso significa: se o alvo do import está fora do pacote atual
> (por exemplo, um módulo auxiliar solto ao lado do pacote), o caminho é
> import absoluto, tratando esse módulo como top-level. Se o alvo está
> dentro do mesmo pacote (um arquivo irmão ou numa subpasta), o caminho
> natural é relativo. Confundir os dois produz dois erros bem
> característicos: `ModuleNotFoundError` (absoluto apontando pro lugar
> errado) ou `ImportError: attempted relative import beyond top-level
> package` (relativo tentando subir além do topo).

</details>

## Dependência circular

**TL;DR**: acontece quando o módulo A importa algo do módulo B no topo do
arquivo, e B importa algo de A também no topo do arquivo. Quando um dos
dois começa a carregar primeiro, o outro tenta buscar um nome que ainda não
foi definido — porque o primeiro módulo está "pela metade".

<details>
<summary><strong>🔍 Aprofundando: por que o erro menciona "partially initialized"</strong></summary>

> O Python executa um módulo de cima para baixo na primeira vez que ele é
> importado, e registra esse módulo em `sys.modules` *antes* de terminar de
> executá-lo — isso evita loop infinito se dois módulos se importam mutuamente,
> mas não evita o problema de ordem. Se A começa a carregar, chega numa
> linha `import B` antes de ter definido a função que B precisa, e B por
> sua vez tenta `from A import essa_funcao` nesse meio-tempo, o Python
> encontra o módulo A em `sys.modules` (então não tenta recarregar do
> zero, o que causaria loop infinito) mas esse módulo A ainda não tem o
> atributo pedido — daí `ImportError: cannot import name '...' from
> partially initialized module`.
>
> Formas comuns de quebrar esse ciclo: (1) inverter a direção da
> dependência, fazendo só um dos dois módulos importar do outro; (2) mover
> o import para dentro da função que o usa, em vez do topo do arquivo,
> adiando a resolução até o momento em que ambos os módulos já terminaram
> de carregar; (3) receber o dado necessário como parâmetro em vez de
> importá-lo diretamente, quebrando o acoplamento entre os dois módulos.

</details>

## Regras e restrições do subject

- **Python 3.10+, flake8, e type annotations com `mypy`** — as três
  exigências padrão dos módulos da 42.
- **Só imports de arquivos/módulos criados no próprio projeto** — nenhuma
  biblioteca externa, porque o objetivo é entender o mecanismo puro de
  import da linguagem, sem abstrações de terceiros por cima.
- **Proibido modificar `sys.path`** — existe a tentação de "resolver" um
  import quebrado inserindo manualmente um caminho em `sys.path`, mas isso
  mascara o problema em vez de ensinar a estrutura correta de pacote. O
  subject fecha essa saída de propósito.
- **`eval()` e `exec()` proibidos** — únicos builtins vetados; não têm
  relação direta com o tema de imports, é uma restrição de segurança geral
  recorrente na 42.

## Correlação com exercícios existentes

- **Parte I (Alembic)**: contrasta `import x` com `from x import y`
  acessando um módulo solto na raiz e depois um módulo dentro do pacote,
  terminando em `import alchemy` — onde fica evidente que só o que o
  `__init__.py` reexporta é alcançável por esse caminho.
- **Parte II (Distillation)**: introduz import aninhado (um módulo do
  pacote que por sua vez importa de outro módulo do mesmo pacote) e o
  conceito de alias de pacote via `import ... as nome`.
- **Parte III (Transmutation)**: exige explicitamente misturar um import
  absoluto e um relativo no mesmo arquivo, porque o alvo de um está fora do
  pacote e o do outro está dentro.
- **Parte IV (Kaboom)**: implementa lado a lado um par de módulos que
  evita dependência circular e um par que a sofre de propósito, para
  comparar as duas estruturas e o traceback resultante.

## Erros comuns

- Usar import relativo (`.` ou `..`) para alcançar um módulo que está fora
  da árvore do pacote atual — gera `attempted relative import beyond
  top-level package`.
- Usar import absoluto sem perceber que o nome do módulo já existe em
  outro lugar do `sys.path` (por exemplo, um arquivo de mesmo nome na
  raiz e dentro de um subpacote) — o Python resolve para o primeiro que
  encontrar, que pode não ser o pretendido, silenciosamente.
- Assumir que "expor uma função no `__init__.py`" e "a função existir no
  arquivo" são a mesma coisa — são independentes; a segunda não implica a
  primeira.

## Perguntas de autoavaliação

- Se dois arquivos dentro do mesmo pacote importam um do outro no topo do
  módulo, em que ordem o Python precisa executá-los para isso não quebrar
  — e por que essa ordem nem sempre é garantida?
- Por que `import pacote.submodulo` não expõe automaticamente
  `pacote.submodulo` como atributo de `pacote` para quem só fez
  `import pacote` antes, a menos que o `__init__.py` faça esse import?
- Dado um módulo fora de qualquer pacote (solto na raiz do projeto), que
  tipo de import (absoluto ou relativo) alcança ele a partir de dentro de
  um subpacote, e por quê?

## Fontes consultadas

- Subject oficial do module06 (lido integralmente antes de escrever este
  material).
- [docs.python.org/3/reference/import.html](https://docs.python.org/3/reference/import.html)
  — semântica formal do sistema de import, resolução absoluta/relativa.
- [docs.python.org/3/tutorial/modules.html#packages](https://docs.python.org/3/tutorial/modules.html#packages)
  — papel do `__init__.py` e imports relativos dentro de pacotes.
