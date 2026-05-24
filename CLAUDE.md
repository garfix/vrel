# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

Vrel is an **experimental** Natural Language Understanding and Execution library for Python (>=3.10). It replicates and extends classic NLU/NLI systems (SHRDLU, Chat-80, SIR, PAM, etc.) on top of a single shared engine — minimizing custom code per application. Each system under `tests/integration/` is both an example and a regression test.

The name and motivation are explained in `docs/name_meaning.md`. The dev journal — current direction, half-finished ideas, open design questions — lives in `docs/2026-remarks.md` (newest entries at the top). Read recent entries before making non-trivial design changes.

## Setup, tests, distribution

```sh
python3 -m venv venv
. venv/bin/activate
pip install -e .
pip install pytest
```

Run tests:

```sh
. venv/bin/activate
pytest                                    # all tests
pytest tests/unit/CoreModule_test.py      # single file
pytest tests/integration/pam/test.py -k test_pam   # single test
```

`pytest.ini` config lives in `setup.cfg` (`testpaths = tests`). Distribution steps (sdist + twine) are in `docs/distribution.md`.

## Architecture

Vrel is organized as a four-stage pipeline plus a shared knowledge engine:

```
text  →  Parser  →  Composer  →  Executor  →  (Model / Solver)  →  Generator  →  text
```

Wired together by `BasicSystem` (`src/vrel/core/BasicSystem.py`). All four stages are optional — `enter()` short-circuits at whichever stage isn't provided. Each integration test (e.g. `tests/integration/hello_world/test.py`) shows the standard wiring: build a `Model` from modules, attach a `BasicParser` + `SemanticComposer` + `AtomExecutor` + `BasicGenerator`, then drive it through `DialogTester`.

### Atoms and the Solver — the engine

Everything reduces to **atoms** (`src/vrel/entity/Atom.py`): `predicate + arguments + modifiers + determiner + exec`. Arguments may be variables, constants, or **lists of atoms** (this is how the system handles things like `count`, `det_all`, `or`, sub-queries — see `docs/atom.md` for the modeling conventions, especially when something must be an argument vs. a modifier).

The `Solver` (`src/vrel/core/Solver.py`) resolves a list of atoms against a `Model`. A `Model` (`src/vrel/core/Model.py`) is just a collection of `SomeModule`s. Each `Module` registers `Relation`s; each `Relation` binds a predicate string to a `query_function` and/or `write_function`. The solver looks up *all* modules that define the predicate and unions their results. This is the central extension point: new domains, new built-ins, new data sources are all just new modules registering relations.

`CoreModule` (`src/vrel/module/CoreModule.py`) is always added to every Model — it provides the built-in predicates (`equals`, `count`, `det_all`, `not`, `exec`, `find_all`, `store`, `create_query`, `create_records`, etc.). Read it to understand the calling convention for query functions: they receive `(arguments, ExecutionContext)` and return either `list[list]` (one row per binding, same arity as arguments) or a `BindingResult`.

### Modules of note

- `CoreModule` — built-in predicates and quantifiers.
- `DeductionModule` — Prolog-like rules loaded from `*.pl` files via `SimpleInferenceRuleParser`. Each rule head's predicate is auto-registered as a relation.
- `InductionModule` — PAM-style plan/goal analysis. Loads three rule sets (fact induction, plan analysis, deductions) and exposes `induce_facts`, `analyze_plans`, `explain`.
- Data-source modules under `src/vrel/data_source/` (Sqlite3, MySQL, PsycoPg2/3, Sparql, Wikidata, SimpleDataSource, SimpleFrameDataSource) — wrap external storage as relations.

### Pipeline stages

- **Parser** (`processor/parser/`) — Earley parser over a `SimpleGrammar`; grammar rules carry semantic attachments (`sem`) that build atoms.
- **Composer** (`processor/semantic_composer/`) — turns parse trees into `SemanticSentence`s (lists of atoms).
- **Executor** (`processor/semantic_executor/`) — `AtomExecutor` runs the resulting atoms via the Solver. Helpers under `helper/` handle name resolution, constant resolution, and inline code execution.
- **Generator** (`core/BasicGenerator.py`) — uses a write-grammar (`grammar/en_us_write.py` plus per-app rules) to produce surface text from an output buffer.

### Each integration test is a complete app

`tests/integration/<app>/` is a self-contained NLU demo and the canonical reference for how to build a new domain:

- `read_grammar.py`, `write_grammar.py` — parse and generation grammars.
- `intents.pl`, `inferences.pl`, `deductions.pl`, `plan_analysis.pl`, `fact_induction.pl` — Prolog-like rule files (DSL parsed by `SimpleInferenceRuleParser`).
- `<App>DB.py`, `<App>Module.py` — domain data + a module that registers query/write functions for it.
- `test.py` — wires it all up and runs `DialogTester` over a list of `[input, expected_output]` pairs.

When adding a new app, copy `hello_world` as the simplest template; `pam` shows the InductionModule wiring; `chat80` is the largest grammar.

## Design principles (from `docs/design-principles.md`)

- Prefer immutable classes; annotate types.
- Replicate classic systems by *extending the shared engine*, not by writing app-specific code.
- Simple techniques for simple problems, complex ones only when needed.
- Keep external dependencies minimal; make them optional where possible.
- Expose shortcomings rather than paper over them.
