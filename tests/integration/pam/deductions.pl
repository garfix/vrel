grasp(C1, E1, E2) :- pick_up(C1, E1, E2).

restaurant_guide(E1) :- michelin_guide(E1).

feature(`person:Willa`, 'gender', 'female').
feature(`person:Willa`, 'type', 'person').

feature(`person:John`, 'gender', 'male').
feature(`person:John`, 'type', 'person').

# todo: add `where()`?
tell(X, B, C, D) :- ask(Y, C, B, D).

him(E1) :- feature(E1, 'gender', 'male').
