# rules/pedagogical.md

Como tornar o material didático sem sacrificar rigor.

1. **TL;DR de 1–3 frases primeiro.** Sem jargão. Deve fazer sentido pra alguém que
   nunca ouviu falar do conceito.

2. **Aprofundamento técnico vai em bloco colapsável**, para não intimidar quem só
   quer o essencial. Formato exato em `templates/concept.md` — inclui blockquote
   (`>`) dentro do `<details>` para diferenciar visualmente do TL;DR mesmo expandido.

3. **Um exemplo mínimo antes da teoria densa.** Mostrar antes de explicar por
   completo reduz a barreira de entrada sem reduzir o rigor do que vem depois.

4. **Explique o erro comum mais frequente**, de forma genérica — nunca citando o
   erro específico do usuário (isso é coberto também por `rules/public-repo.md`
   quando aplicável, mas vale mesmo fora de repo público: expor erro específico
   não ensina o conceito, só o erro).

5. **Compare com algo já conhecido quando genuinamente esclarecer** — não force
   comparação (ex: com C) em conceito que não se beneficia disso. Uma comparação
   forçada confunde mais do que ajuda.

6. **Termine com 2–3 perguntas de autoavaliação, sem gabarito.** O objetivo é o
   leitor testar se entendeu, não copiar uma resposta pronta.

7. **Teste antes de finalizar**: um iniciante conseguiria ler só os TL;DRs
   (ignorando todo `<details>`) e sair com entendimento correto? Se não, o TL;DR
   está fazendo o trabalho errado — ele precisa ser autossuficiente para o nível
   básico, mesmo que superficial.
