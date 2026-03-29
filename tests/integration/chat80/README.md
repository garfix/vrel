## Chat-80

Replicates a Chat-80 dialog (found here: https://github.com/JanWielemaker/chat80/blob/master/prolog/chat80/demo)
CHAT-80 is mainly described in
- Efficient Processing of Interactive Relational Database Queries Expressed in Logic - Warren (1981)
- An efficient easily adaptable system for interpreting natural language queries - Pereira, Warren (1982)

Topics:
- long distance dependencies (extraposition)
- proper nouns
- superlatives ('largest')
- relative clauses
- aggregations
- inference: in(A, B) -> contains(C, A), in(C, B).
- different result formats: yes/no, scalar, list, table
- query optimization: reordering and isolating sub-queries

## To run the original Chat-80 application:

Install SWI Prolog

    sudo apt install swi-prolog

Get Chat-80 source code:

    git clone https://github.com/JanWielemaker/chat80.git

Enter the right directory

    cd chat80/prolog

Start interactive shell    

    swipl

Compile Chat-80    

    compile(chat80).

Start Chat-80 interactive, turn on tracing, enter sentences

    chat80:hi.
    Trace.
    What are the continents no country in which contains more than  two cities whose population exceeds 1 million?

Stop
    ctrl/c
    e

