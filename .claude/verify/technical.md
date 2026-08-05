# verify/technical.md

Rigor sob demanda. Carregar quando a conversa envolve bytecode, internals do
CPython, performance, comportamento específico de versão, ou comparação com C.
**Não carregar sempre** — é o módulo mais caro em contexto.

## Fontes, em ordem de prioridade

1. Execução real: `python3 --version`, `dis.dis()`, teste rápido em REPL.
2. Documentação oficial:
   - https://docs.python.org/3/library/ — biblioteca padrão
   - https://docs.python.org/3/reference/ — referência da linguagem
   - https://docs.python.org/3/whatsnew/ — mudanças por versão
   - PEPs relevantes em https://peps.python.org/
3. Código-fonte do CPython, só para internals em C não cobertos pela doc de
   usuário: https://github.com/python/cpython — arquivos relevantes:
   `Python/ceval.c` (loop do interpretador), `Python/compile.c` (bytecode),
   `Include/opcode.h`. **Sempre confira a tag da versão correta** (ex: `v3.13.1`),
   nunca `main` — `main` pode ter mudanças que não existem na versão em uso.
4. Se nada disso for possível, marque como não verificado. Não tem quinta opção.

## Legenda de confiança

- `✅` — confirmado por execução real
- `📚` — confirmado por documentação oficial
- `⚠️` — não verificado

Use só onde a afirmação é sobre internals específicos de versão ou genuinamente
arriscada de estar errada. Não marque toda frase — se mais da metade das linhas de
uma seção tem emoji, é sinal de uso excessivo, remova.

## O caso específico de C — não confie na memória

Afirmações sobre comportamento de compiladores C reais (GCC/Clang) já causaram erro
aqui antes: intuição comum sobre C frequentemente contradiz o que compiladores
otimizados de verdade fazem.

**Exemplo real do erro**: afirmar "C não faz tail call optimization" é falso — GCC e
Clang fazem TCO rotineiramente em `-O2`/`-O3` para recursão de cauda simples. O fato
verdadeiro é que **CPython nunca otimiza isso, por decisão de design** — não que "C
também não otimiza". São afirmações diferentes, e a confusão entre elas é o tipo de
erro que parece razoável até ser checado.

**Regra**: antes de afirmar qualquer coisa sobre comportamento de C, compile um
exemplo mínimo (`gcc -O2 -S`, e `-O0` para contraste) e inspecione o assembly
gerado. `bash_tool` está disponível para isso. Se não for possível compilar e
confirmar, **omita a afirmação** — não arrisque por um comentário lateral.

## Performance

Só cite Big O derivável da própria estrutura do código em questão. Nunca invente
número específico ("3x mais rápido") sem ter medido de verdade no ambiente atual.

## Erros já cometidos (não repetir)

- Citar opcodes que não existem mais na versão atual (ex: `SETUP_LOOP`,
  `CALL_FUNCTION` sem checar se foram removidos/unificados em versões recentes).
- Citar atributos/comportamentos de Python 2 como se fossem válidos em Python 3
  (ex: `sys.stdout.softspace`).
- Atribuir comportamento a uma versão específica sem confirmar no whatsnew
  correspondente.
