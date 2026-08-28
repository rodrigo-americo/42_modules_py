---
name: scaffold-module
description: Lê o PDF de subject de um module da piscine Python e cria a árvore de arquivos/pastas exigida, todos vazios — nada de conteúdo, nada de ex0/ex1/ex2 genérico se o subject define outra estrutura.
trigger: /scaffold-module
---

# /scaffold-module

Recebe um número ou nome de module (ex: `06`, `module06`, `moduleXX`), lê o
PDF de subject de verdade, e cria só a árvore de arquivos e pastas que o
subject exige — todos os arquivos vazios. Não escreve nenhuma linha de
código, README ou concept.md; isso é trabalho de outra etapa, depois que o
humano começa a resolver os exercícios.

## Uso

```
/scaffold-module 06
/scaffold-module module07
```

Se nenhum argumento for passado, pergunte ao usuário qual module.

## Passo a passo

1. **Resolva o caminho do module.** Normalize o argumento para
   `moduleNN` (dois dígitos, ex: `06`). A pasta raiz do repo é onde está
   `CLAUDE.md` — os modules ficam em `moduleNN/` direto na raiz.

2. **Ache o PDF do subject dentro dessa pasta.** O padrão observado nos
   modules existentes é `pyN.pdf` (ex: `py0.pdf`, `py6.pdf`), mas não
   assuma o número — procure qualquer `*.pdf` dentro de `moduleNN/`. Se a
   pasta não existir ainda, crie-a primeiro (ela é onde o usuário
   normalmente já colocou o PDF antes de pedir o scaffold).

   - **Se não achar nenhum PDF**: pare e avise o usuário explicitamente.
     Não crie estrutura genérica adivinhada pelo número do módulo — isso
     viola a regra 1 de `rules/core.md` (ler a fonte antes de responder) e
     a regra 5 de `profiles/42.md`. Peça para o usuário colocar o PDF do
     subject na pasta antes de continuar.

3. **Leia o PDF inteiro de verdade** com a ferramenta de leitura de PDF
   disponível. Não infira conteúdo do nome do arquivo, do número do
   module, ou de módulos anteriores parecidos — cada subject da 42 define
   sua própria árvore, e elas variam bastante em forma (compare, por
   exemplo, um module com pastas `ex0/ex1/ex2` versus um module com um
   pacote próprio e scripts soltos, como aconteceu no module06 com
   `alchemy/` + `ft_*.py`).

4. **Extraia a árvore de arquivos exigida.** A maioria dos subjects da
   piscine tem uma seção com um diagrama de árvore tipo:
   ```
   .
   |-- pasta/
   |   |-- __init__.py
   |   `-- arquivo.py
   `-- outro_arquivo.py
   ```
   Use esse diagrama literalmente — ele é a fonte da verdade sobre nomes
   de arquivo, nomes de pasta e nesting. Não renomeie nada, não resuma,
   não "melhore" a estrutura.

   - **Se o subject não tiver um diagrama de árvore explícito** (alguns
     modules mais antigos/simples só listam exercícios por texto, sem
     desenhar a árvore), infira a partir da descrição de cada exercício:
     nome de arquivo esperado (geralmente aparece em negrito ou `code`
     span perto de "will contain" / "create a file"), e se o padrão do
     repo até aqui usa `exN/arquivo.py` (majoritário nos modules já
     existentes) — confira o padrão real olhando 1-2 modules já
     concluídos no repo antes de decidir, não assuma de cor.

5. **Não presuma `ex0/ex1/ex2`.** Esse padrão existe nos modules 00-05
   deste repo porque os subjects deles definiam exercícios independentes
   nomeados assim. Não é uma convenção fixa da piscine — é só o que
   aqueles subjects específicos pediam. Se o subject atual descreve outra
   forma (um pacote com submódulos, scripts soltos, etc.), siga o subject,
   não o hábito dos modules anteriores.

6. **Crie a árvore inteira, todos os arquivos vazios.** Pastas com
   `mkdir -p` / `New-Item -ItemType Directory`, arquivos com `touch` /
   `New-Item -ItemType File` (nunca escreva conteúdo, nem um `pass`, nem
   um docstring, nem um comentário). Isso vale também para `__init__.py`
   — vazio, mesmo que o subject descreva o que ele "deve conter": esse
   conteúdo é trabalho de implementação, não de scaffold.

7. **Avise o que foi criado.** Liste a árvore final criada (comando tipo
   `find moduleNN -type f | sort` ou equivalente PowerShell) para o
   usuário conferir contra o subject. Não crie `README.md` nem
   `concept.md` nesta etapa — isso é outro passo, só depois que os
   exercícios tiverem sido resolvidos (ver o padrão dos modules
   anteriores no repo: esses dois arquivos descrevem o que foi
   *aprendido*, não podem existir antes do código).

## O que esta skill não faz

- Não escreve nenhuma linha de código nos arquivos criados.
- Não gera `README.md` / `concept.md` (isso vem depois, ao final do
  module, seguindo `.claude/templates/concept.md`).
- Não resolve exercícios nem sugere soluções — só monta o esqueleto vazio.
- Não commita nada automaticamente — deixe o `git status` visível e
  pergunte antes de fazer `git add`/`commit`, como qualquer outra mudança
  neste repo.

## Sinal de contexto

Como este repo é o kit de estudo Python da 42 (ver `CLAUDE.md` na raiz),
sempre que esta skill rodar aqui, as regras de `.claude/rules/public-repo.md`
e `.claude/profiles/42.md` já se aplicam — mas elas afetam pouco esta skill
especificamente, porque scaffold não gera conteúdo nenhum (nada a proteger
de exposição, já que os arquivos ficam vazios).
