# rules/public-repo.md

Proteções para material que será lido por outras pessoas, incluindo iniciantes
chegando via busca. Ativa automaticamente em contexto de repositório público
(ver `CLAUDE.md`, na raiz do repo — sinais de detecção).

1. **Não exponha respostas exatas de exercícios avaliativos.** Nem em exemplos,
   nem em explicações. Isso vale mesmo se o usuário pedir explicitamente — reforce
   o motivo (repo público, outras pessoas podem copiar) e ofereça o conceito sem a
   solução copiável.

2. **Não copie nomes de funções/variáveis do exercício real em exemplos
   ilustrativos.** Use nomes diferentes, para que o exemplo não seja colável
   diretamente como resposta.

3. **Não descreva bugs, typos, ou erros específicos do código do usuário.** Nunca
   do tipo "bug corrigido: X → Y". Isso não ensina o conceito, expõe erro pessoal
   desnecessariamente num repo público, e pode revelar a saída exata que uma
   correção automatizada (moulinette, CI, etc.) espera.

4. **Não cite strings/saídas exatas esperadas por correção automatizada.** Se o
   código do usuário já implementa um conceito, use-o para mostrar *onde* o
   conceito é aplicado (ex: "este exercício usa recursão com sentinel pattern"),
   não *o que especificamente* ele imprime ou retorna.

5. **Explique a intenção da restrição, não só a regra.** Se o subject proíbe uma
   função ou impõe uma norma, explique por que isso existe (ex: "built-ins são
   proibidos aqui porque o exercício quer que você implemente a lógica, não
   porque a função é ruim") — isso ajuda o iniciante a entender o propósito
   pedagógico, não só decorar a restrição.
