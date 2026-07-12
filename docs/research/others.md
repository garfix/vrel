(Comments from Claude)

## Attempto Controlled English (ACE)

Developed at the University of Zurich since 1995, parses into Discourse Representation Structures (a first-order logic variant), which can then be executed as queries or rules, translated to OWL/SWRL, or reasoned over. It's intended for professionals who want the rigor of formal methods without needing to learn formal notations. This is still actively maintained and researched — recent papers (2025–2026) apply it to legal knowledge formalization and even compare it against LLM-based approaches.

## Inform 7 (2006–present)

Probably the most successful "write real English, get real executable code" system ever built. Inform 7 is a programming language and design system for interactive fiction that compiles Inform source into story files for the Z-code or Glulx virtual machines — genuinely executable games, not toy output. It's rule-based (a real parser and compiler, no ML), was open-sourced in 2022, and has ranked in the TIOBE index's top 100 most influential programming languages. It's still under very active development — the latest beta version was released in June 2026.

http://www.inform7.com
https://en.wikipedia.org/wiki/Inform
https://github.com/ganelson/inform
https://ganelson.github.io/inform/core-module/1-cm.html
preform: https://ganelson.github.io/inform/words-module/4-ap.html
sentence conversion: https://ganelson.github.io/inform/calculus-module/5-sc.html
https://worrydream.com/refs/Nelson_G_2008_-_Inform_7,_The_Program.pdf

## Catala (2021–present)

A more recent, and arguably more consequential, example: Catala is designed to allow a straightforward, systematic translation of statutory law into an executable implementation, preserving a near-line-by-line correspondence between legal text and code. It's not "write in plain English" so much as "annotate real legislative prose with formal meaning," but the output is genuinely executable — the French tax authority (DGFIP) has used it as a proof-of-concept to recode parts of its tax-calculation infrastructure, and the project won a 2026 scientific interdisciplinarity prize from CNRS and France Universités for the lawyer/programmer collaboration model it enables.

## RuleSpeak / SBVR

(Semantics of Business Vocabulary and Rules, an OMG standard) — controlled-English business rules that compile into executable rule-engine logic (e.g., Drools), used in enterprise rule management.
