# teach
intent_teach(A) :- store(A), out('understand').

# part of
intent_part_of(A, B) :- (
    # Is a nostril part of a professor?
    proper_part_of(A, B), out('yes')
    # Is a nostril part of a living-creature?
;   proper_isa(BB, B), proper_part_of(A, BB), out('sometimes')
    # Is a nose part of a nose?
;   equals(A, B), out('no_subpart')
    # Is a living-creature part of a nose?
;   proper_isa(AA, A), proper_part_of(B, AA), out('reverse_sometimes')
).

# is a
intent_isa(A, B) :- (
    # is a girl a person?
    full_isa(A, B), out('yes')
    # is a person a girl?
;   proper_isa(B, A), out('sometimes')
    # is a person a person?
;   equals(A, B), out('yes')
    # otherwise
;   out('unknown')
).

# count
intent_count(Atoms) :- count(C, Atoms), not(any_output()), out('count', C).

# yes/no
intent_yn(Atoms) :- (
    exec(Atoms), out('yes')
;
    out('no')
).

# own
# Every fireman owns a pair-of-red-suspenders. A firechief is a fireman. Does a firechief own a pair-of-red-suspenders?
# Alfred owns a log-log-decitrig. A log-log-decitrig is a slide-rule. Does Alfred own a slide-rule?
intent_own(A, B) :- proper_own(A, B), out('yes').

intent_some_own(A, B) :- (
    # own in some cases, but not all
    proper_own(A, B), out('yes')
    # Alfred is a tech-man
    # A tech-man is an engineering-student
    # Alfred owns a log-log-decitrig
    # Does an engineering-student own a log-log-decitrig?
;   proper_isa(AA, A), own(AA, B), out('yes')
    # Does a pair-of-red-suspenders own a pair-of-red-suspenders?
;   equals(A, B), out('no_same')
    # otherwise
;   out('unknown')
).

# claim
intent_claim(Atom) :- checkable(Atom), (
    check_claim(Atom), store(Atom), out('understand')
;
    out('impossible')
).
intent_claim(Atom) :- not(checkable(Atom)), store(Atom), out('understand').

# where
intent_where(Id) :-
    out('location', Id).

# position
intent_position() :-
    out('position').
