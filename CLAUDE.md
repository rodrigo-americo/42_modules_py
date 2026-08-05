# Python Study Kit V1.1

Orquestrador. Este arquivo não contém regras — só diz quais arquivos carregar e quando.
As regras de verdade vivem em `.claude/rules/`, `.claude/verify/` e `.claude/profiles/`.

## Sempre carregar

- `.claude/rules/core.md`

## Carregar por sinal de contexto (não depender de o humano lembrar)

Antes de responder, verifique sinais no que foi fornecido (path, conteúdo do
diretório, menção do usuário) e carregue automaticamente:

- Se o diretório de trabalho contém um `.pdf` de subject (ex: `en.subject.pdf`,
  `py0.pdf`), uma pasta `module_XX/` ou `moduleXX/`, ou o usuário menciona "42",
  "piscine", "moulinette" →
  carregue `.claude/rules/public-repo.md` **e** `.claude/profiles/42.md`.
- Se o usuário pede explicação didática, material de estudo, ou "me ensina X" →
  carregue `.claude/rules/pedagogical.md`.
- Se a pergunta envolve bytecode, internals do CPython, performance,
  comportamento específico de versão, ou comparação com C →
  carregue `.claude/verify/technical.md`.

Não pergunte ao usuário "qual arquivo devo carregar" — infira pelos sinais acima.
Se estiver genuinamente ambíguo (ex: não dá pra saber se é repo público), pergunte
uma vez e siga.

## Template

Para gerar material de estudo, use `.claude/templates/concept.md` como esqueleto.

## Glossário

Termos recorrentes entre módulos ficam em `.claude/GLOSSARY.md`.

## Ordem de precedência em conflito

Se duas regras carregadas conflitarem, a ordem de prioridade é:
`rules/public-repo.md` > `rules/core.md` > `verify/technical.md` > `rules/pedagogical.md` > `profiles/*.md`

(Proteção de repositório público nunca cede espaço para didática ou perfil.)
