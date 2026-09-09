# module08 — The Matrix: Welcome to the Real World of Data Engineering

Ambiente: Python 3.10+ (testado em 3.13.2, Windows) | Verificado em: 2026-09-09

## Objetivo do módulo

Segundo o subject (`py8.pdf`), o módulo cobre três ferramentas que todo
engenheiro de dados usa para não deixar um projeto virar bagunça: ambientes
Python isolados (`ex0`), gerência de dependências de terceiros com pip e
Poetry (`ex1`), e configuração por variáveis de ambiente com arquivos
`.env` mantendo segredos fora do git (`ex2`). Os três exercícios são
independentes — o fio condutor não é código compartilhado, é a ideia de
que *onde* o código roda e *o que* ele consome de fora precisam ser
explícitos e controlados.

## Virtual environment: um Python isolado por projeto

**TL;DR**: um *virtual environment* (venv) é uma pasta com uma cópia (ou
link) do interpretador Python e um diretório próprio de pacotes. Enquanto
ele está ativo, `pip install` põe as libs lá dentro em vez de no Python do
sistema — então cada projeto tem suas versões, sem conflito.

<details>
<summary><strong>🔍 Aprofundando: como um script sabe que está dentro de um venv</strong></summary>

> Um venv não é um processo separado nem mágica de shell — é uma pasta com
> um `pyvenv.cfg` e um `python` que, ao iniciar, ajusta os caminhos de
> busca de pacotes para apontar para o `site-packages` de dentro da
> própria pasta.
>
> O rastro disso fica em atributos do módulo `sys`. A checagem documentada
> na página do `venv` (docs.python.org) é comparar dois prefixos: um que
> aponta para o ambiente em uso e outro que sempre aponta para a
> instalação base. Fora de um venv os dois são idênticos; dentro, o
> primeiro aponta para a pasta do venv e o segundo continua na instalação
> original. Verificado por execução (Python 3.13.2): fora do venv os
> prefixos batem; dentro de um venv recém-criado eles divergem.
>
> Existe também uma checagem legada — um atributo que só passa a existir
> quando o ambiente foi criado pela lib externa `virtualenv` (anterior à
> PEP 405, que trouxe o `venv` para a biblioteca padrão no Python 3.3).
> Confirmado que esse atributo **não** existe num Python 3.13 fora de venv;
> um script robusto testa as duas coisas com um `or`.
>
> Para "onde os pacotes seriam instalados", o módulo `site` expõe uma
> função que devolve os diretórios `site-packages` do ambiente atual — no
> Windows ela retorna uma lista com o prefixo e o `...\Lib\site-packages`;
> hardcodar `lib/pythonX.Y/site-packages` quebra entre sistemas
> operacionais, por isso o subject autoriza `site` explicitamente.
>
> **Conexões:**
> - `Histórico:` o módulo `venv` entrou na biblioteca padrão pela PEP 405 (Python 3.3); antes só existia o `virtualenv` externo, o que explica os dois métodos de detecção coexistirem.

</details>

## Dependências: pip com requirements.txt vs Poetry com pyproject.toml

**TL;DR**: as duas ferramentas resolvem o mesmo problema — instalar as
libs que o projeto precisa —, mas com formatos e garantias diferentes.
`pip` lê uma lista simples (`requirements.txt`); Poetry lê um arquivo
declarativo (`pyproject.toml`) e grava um `poetry.lock` com toda a árvore
de dependências transitivas travada.

<details>
<summary><strong>🔍 Aprofundando: por que importar dependências opcionais sob try/except</strong></summary>

> O subject pede que o programa do `ex1` "detecte quais pacotes estão
> disponíveis e dê mensagens de erro úteis se faltarem" — e explicitamente
> tolera erros de `flake8`/`mypy` ligados a import, só nesse exercício.
>
> Um `import` no topo do arquivo que falha derruba o programa inteiro com
> `ModuleNotFoundError` antes da primeira linha de lógica rodar. Envolver
> cada import num `try/except ImportError` e guardar `None` quando falha
> permite que o programa continue até o ponto em que decide, de forma
> controlada, o que fazer: listar o que está instalado, dizer o que falta
> e como instalar, e sair com um código de status em vez de um traceback.
>
> A versão instalada de cada pacote sai de `importlib.metadata.version()`,
> que lê os metadados do pacote sem precisar importá-lo — e levanta uma
> exceção específica quando o pacote não está presente, tratável do mesmo
> jeito.
>
> A diferença prática entre os dois arquivos de dependência: um
> `requirements.txt` com versões travadas (`==`) fixa só as dependências
> *diretas*; o que essas libs puxam por baixo pode variar entre
> instalações. O `poetry.lock` que o Poetry gera trava a árvore inteira
> por hash, então `poetry install` reproduz exatamente o mesmo conjunto de
> pacotes em qualquer máquina. Neste exercício os dois arquivos declaram
> as mesmas libs — a diferença demonstrada é de ferramenta e formato, não
> de conteúdo.

</details>

## Configuração por ambiente: env vars, .env e precedência

**TL;DR**: em vez de escrever credenciais e URLs direto no código, o
programa lê essas configurações de *variáveis de ambiente*. Um arquivo
`.env` (carregado pela lib `python-dotenv`) é uma conveniência de
desenvolvimento para não exportar tudo à mão — mas uma variável já
definida no shell tem prioridade sobre o `.env`.

<details>
<summary><strong>🔍 Aprofundando: por que o shell vence o .env, e por que o .env fica fora do git</strong></summary>

> A ideia vem do item III da metodologia "12-factor app" (12factor.net):
> configuração que varia entre ambientes (dev, staging, produção) vive no
> ambiente, não no código. O mesmo arquivo `.py` roda em qualquer lugar; o
> que muda é o que o ambiente fornece.
>
> **Precedência.** A função de carga do `python-dotenv` tem um parâmetro
> `override` que por padrão é `False` — ela só preenche as chaves que
> ainda *não* existem no ambiente. Verificado por execução (python-dotenv
> 1.2.1): com uma variável já setada no shell, `load_dotenv()` no default
> mantém o valor do shell; passando `override=True`, o valor do arquivo
> passa a ganhar. O default protege contra um `.env` esquecido no
> diretório sobrescrever, sem querer, uma configuração que um operador
> definiu de propósito no ambiente — em produção, as variáveis vêm do
> orquestrador (systemd, container, secrets de CI), e o `.env` nem deveria
> existir lá.
>
> **`.env` fora do git.** O `.env` real guarda valores sensíveis (chave de
> API, string de conexão com senha). Um arquivo commitado entra no
> histórico do repositório de forma permanente — apagá-lo num commit
> posterior não remove as versões anteriores, então a credencial vazada
> continua recuperável por qualquer um que clone o repo. O que vai para o
> controle de versão é um `.env.example`: as mesmas chaves, com valores
> falsos, servindo de template (`cp .env.example .env` e preencha). O
> `.gitignore` do exercício ignora só o `.env`, deixando o `.env.example`
> versionado.
>
> **Tratamento de ausência.** "Config faltando" não pode virar `KeyError`
> cru. Ler com `os.environ.get()` (devolve `None` se ausente) ou
> `os.getenv(nome, default)` permite decidir por variável: algumas têm
> um default sensato, outras são obrigatórias — e, quando obrigatórias,
> qual a consequência da falta pode depender do modo (dev tolera, produção
> não).

</details>

## Regras e restrições do subject

- **Python 3.10+, `flake8`, type annotations completas (`mypy`)** — regra
  geral do módulo. A exceção é o `ex1`, onde erros de import em `flake8` e
  `mypy` são tolerados, porque as libs são opcionais por design.
- **ex0 — só `sys`, `os`, `site` e `print()`** — o exercício quer que você
  inspecione o ambiente *em que o script já roda*, não que crie ou invoque
  outro; por isso `venv` e `subprocess` ficam de fora da lista.
- **ex1 — o dataset tem que vir de `numpy`** — não listas hardcoded, não
  `range()`. `requests` é autorizado mas opcional (só se você buscar dados
  de uma API real); simular com `numpy` é o caminho padrão.
- **ex1 — os dois arquivos de dependência são obrigatórios** — o objetivo
  é comparar pip e Poetry lado a lado, então `requirements.txt` e
  `pyproject.toml` precisam coexistir declarando o mesmo conjunto.
- **ex2 — usar a lib `python-dotenv`, não escrever um parser de `.env`** —
  o subject é explícito: o objetivo é aprender a ferramenta padrão de
  configuração, não reimplementá-la.
- **ex2 — o `.env` real nunca vai para o controle de versão** — e você
  precisa saber explicar o porquê na peer-review (histórico permanente do
  git, credencial recuperável mesmo após remoção).
- **Não submeter o virtual environment no repositório** — ele deve poder
  ser recriado do zero durante a review a partir dos arquivos de
  dependência.

## Correlação com exercícios existentes

- **ex0** exercita detecção de ambiente: o programa lê `sys` e `site` para
  responder "estou isolado?" e ramifica a saída — um caminho instrui como
  criar/ativar um venv, o outro mostra os detalhes do venv ativo
  (interpretador, caminho, `site-packages`).
- **ex1** exercita import resiliente e gerência de dependências: libs de
  terceiros importadas sob `try/except`, versões lidas via
  `importlib.metadata`, dataset gerado por `numpy`, transformado com
  `pandas` e plotado com `matplotlib` num backend não-interativo; as
  mesmas deps declaradas para pip e para Poetry.
- **ex2** exercita configuração externa: `python-dotenv` carrega o `.env`
  sem sobrescrever o ambiente, as variáveis são lidas com `os.getenv` /
  `os.environ.get`, e o programa varia comportamento entre `development` e
  `production` de forma visível na saída, com os segredos mascarados.

## Erros comuns

- Hardcodar o caminho de `site-packages` (`lib/pythonX.Y/site-packages`)
  em vez de perguntar ao módulo `site` — o layout difere entre sistemas
  operacionais e o caminho fixo quebra em um deles.
- Confundir "criar o gerador de números aleatórios" com "usá-lo": instanciar
  um RNG e depois chamar a API global de aleatoriedade, deixando o gerador
  sem efeito.
- Deixar um `import` de biblioteca externa no topo do arquivo sem proteção
  quando o programa precisa funcionar com a lib ausente — a falha ocorre
  antes de qualquer tratamento e derruba tudo.
- Tratar variável de ambiente ausente com acesso direto por índice
  (`os.environ["CHAVE"]`), que levanta `KeyError`, em vez de `.get()` /
  `getenv` com decisão explícita (default ou erro tratado).
- Assumir que o `.env` sempre sobrescreve o ambiente — o comportamento
  padrão do `python-dotenv` é o oposto, e inverter isso sem querer muda
  qual valor o programa acaba usando.

## Perguntas de autoavaliação

- Se `sys.prefix` e `sys.base_prefix` são iguais, o script está rodando
  dentro ou fora de um virtual environment — e por que a comparação
  funciona?
- Um `requirements.txt` com todas as versões travadas em `==` garante que
  duas máquinas terão exatamente os mesmos pacotes instalados? O que o
  `poetry.lock` acrescenta a essa garantia?
- Rodando `API_KEY=xyz python oracle.py` com um `.env` que também define
  `API_KEY`, qual valor o programa usa, e qual parâmetro do
  `python-dotenv` inverteria esse resultado?

## Fontes consultadas

- `py8.pdf` (subject oficial do module08, lido integralmente antes de
  escrever este material).
- [docs.python.org — venv](https://docs.python.org/3/library/venv.html) e
  [docs.python.org — sys](https://docs.python.org/3/library/sys.html),
  para a checagem de prefixos referenciada no primeiro aprofundamento.
- [docs.python.org — site](https://docs.python.org/3/library/site.html),
  para o comportamento de `getsitepackages()`.
- [docs.python.org — importlib.metadata](https://docs.python.org/3/library/importlib.metadata.html),
  para leitura de versão de pacote sem importá-lo.
- [python-dotenv (PyPI)](https://pypi.org/project/python-dotenv/), para o
  parâmetro `override` e o comportamento de precedência (confirmado por
  execução com a versão 1.2.1).
