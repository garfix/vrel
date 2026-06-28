An **experimental** Natural Language Understanding and Execution library in Python.

The aim of this project is to make comprehensive rule-based natural language understanding and execution simple.

The system is intentionally completely rule-based, which means that you as a developer have to write the grammar and create functions for all logic. The benefit is complete control over the code that is to be executed. The results are accurate, repeatable, and transparent.

## Features

- Commands, queries, and story processing
- An implementation of Earley's parser with semantic attachments
- Prolog-like deduction and induction rules
- Identification of id's using same-as handling
- Multiple sentence parsing and morphological parsing
- Interaction with any type of data source
- Predefined data sources for Postgres, MySql, Sqlite, and Sparql
- Implementation of David H.D. Warren's query optimizations (from CHAT-80)

Demos:

All demos are in the form of automatic test suites.

- A replication of a dialog with Chat-80 (complex queries)
- A replication of a dialog with SIR (many kinds of simple queries)
- A replication of a dialog with Cooper's system (3-valued logic queries)
- A proof-of-concept of a dialog with Wikidata (using Sparql)
- Work in progress: A replication of a dialog with PAM

## Tutorial

Read how to use the library in the [tutorial](docs/tutorial/README.md)

## Requires

- Python 3.10 (or higher)

## Use

- Clone the repository
- Create the virtual environment: `pip install -r requirements.txt`
- Activate the virtual environment (linux example): `. venv/bin/activate`
- Run (for example) the CHAT-80 test `pytest tests/integration/chat80/test.py`
