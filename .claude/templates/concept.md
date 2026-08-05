# templates/concept.md

Esqueleto para gerar `module_XX/concept.md`. Regras que se aplicam a cada seção
estão comentadas inline — remova os comentários `<!-- -->` ao gerar o arquivo real.

```markdown
# {TÍTULO DO MÓDULO}

Ambiente: Python {X.Y} | Verificado em: {AAAA-MM-DD}

## Objetivo do módulo

<!-- Baseado no subject real (en.subject.pdf lido de verdade), em linguagem direta. -->

## {Nome do Conceito 1}

**TL;DR**: {1–3 frases, sem jargão — precisa fazer sentido pra quem nunca ouviu falar disso}

<details>
<summary><strong>🔍 Aprofundando: {bytecode, internals, edge cases}</strong></summary>

> {Conteúdo técnico denso aqui — bytecode real via dis.dis(), trade-offs,
> referências a PEPs, etc. Toda linha do aprofundamento começa com `>`,
> incluindo linhas em branco entre parágrafos e blocos de código.}
>
> ```
> RESUME 0
> LOAD_GLOBAL ...
> ```

<!-- Conexões (opcional, 0 a 3 itens, nunca em todo conceito — só quando
     genuinamente agrega). Cada item é UMA linha. Ver verify/technical.md
     para o padrão de verificação exigido por tipo:
> **Conexões:**
> - `Em C:` {só se compilado e verificado — ver verify/technical.md}
> - `Histórico:` {só com PEP/versão específica, já citada em Fontes}
> - `Diagrama:` {só se a estrutura for genuinamente espacial/hierárquica}
> - `Performance:` {só Big O derivável da estrutura, nunca número inventado}
-->

</details>

## Regras e restrições do subject

<!-- O que o subject exige/proíbe, e o PORQUÊ — não só a regra.
     Ver profiles/42.md quando aplicável. -->

## Correlação com exercícios existentes

<!-- Qual conceito cada exercício exercita e por quê.
     NUNCA cite bugs, typos, ou strings exatas — ver rules/public-repo.md. -->

## Erros comuns

<!-- Descritos de forma genérica (ex: "confundir print() com return"),
     nunca o erro específico que o usuário cometeu. -->

## Perguntas de autoavaliação

<!-- 2–3 perguntas, sem gabarito. -->

## Fontes consultadas

<!-- Links reais usados na verificação — não liste fonte que não foi
     efetivamente consultada. -->
```

## Notas de formatação (não fazem parte do arquivo gerado)

- Blocos de código dentro do blockquote também levam `>` antes e depois dos
  ` ``` `, senão o recuo quebra no meio.
- Link para `GLOSSARY.md` na primeira menção de um termo que existe lá:
  `[bytecode](../.claude/GLOSSARY.md#bytecode)`. Só a primeira ocorrência por
  conceito vira link. Nunca invente âncora — só linka termo que realmente existe
  no glossário com aquele `id`.
- **Nunca linke termo dentro do `<summary>`** — um link ali compete com o clique
  de abrir/fechar o accordion. `<summary>` fica sempre texto puro (só o `🔍` +
  negrito); links de glossário só no corpo, dentro do blockquote.
- Nenhum emoji decorativo fora da legenda de confiança (`✅ 📚 ⚠️`) e do `🔍`
  fixo no `<summary>` do aprofundamento. Sem `🎯`, `🐍`, etc. em título ou texto
  corrido.
