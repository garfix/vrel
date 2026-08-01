# She picked up the Michelin Guide

# [['is', ['actor', '?x'], ['state', ['hunger', ['val', '?n']]]], ['pos-val', '?n']],
# [['goal', ['planner', '?x'], ['objective', ['is', ['actor', '?x'], ['state', ['hunger', ['val', [0]]]]]]]]
goal(not(hungry(E1))) => hungry(C1, E1).

# [['goal', ['planner', '?x'], ['objective', ['is', ['actor', '?x'], ['state', ['hunger', ['val', [0]]]]]]]],
# [['do-$restaurant-plan', ['planner', '?x'], ['restaurant', '?y']]]
plan(do_restaurant(E1, E2)) => goal(not(hungry(E1))).

# [['do-$restaurant-plan', ['planner', '?x'], ['restaurant', '?y']]],
# [['goal', ['planner', '?x'],
#             ['objective', ['prox', ['actor', '?x'], ['location', '?y']]]], ['isa', 'restaurant', '?y']]
goal(prox(E1, E2)), equals(E2, 'restaurant') => plan(do_restaurant(E1, E2)).

# [['goal', ['planner', '?x'], ['objective', ['prox', ['actor', '?x'], ['location', '?y']]]]],
# [['goal', ['planner', '?x'],
#           ['objective', ['know', ['actor', '?x'], ['fact', ['is', ['actor', '?y'], ['prox', '?z']]]]]]]
goal(know(E1, fact(distance(E2)))) => goal(prox(E1, E2)).

# [['goal', ['planner', '?x'],
#             ['objective', ['know', ['actor', '?x'],
#                                     ['fact', ['is', ['actor', 'restaurant'], ['prox', '?z']]]]]]],
# [['read-plan', ['planner', '?x'], ['object', '?w']], ['isa', 'restaurant-guide', '?w']]
plan(read(S1, E1, E2), restaurant_guide(E2)) => goal(know(E1, fact(distance('restaurant')))).

# [['goal', ['planner', '?x'], ['objective', ['enjoyment', ['actor', '?x']]]]],
# [['read-plan', ['planner', '?x'], ['object', '?w']], ['isa', 'book', '?w']]
plan(read(S1, E1, E2)) => goal(enjoyment(E1)).

# [['read-plan', ['planner', '?x'], ['object', '?y']]],
# [['goal', ['planner', '?x'],
#             ['objective', ['poss', ['actor', '?x'], ['object', '?y']]]], ['isa', 'book', '?y']]
goal(possess(S1, E1, E2)) => plan(read(S1, E1, E2)).

# [['goal', ['planner', '?x'], ['objective', ['poss', ['actor', '?x'], ['object', '?y']]]]],
# [['take-plan', ['planner', '?x'], ['object', '?y']]]
plan(take(S1, E1, E2)) => goal(possess(S1, E1, E2)).

# [['take-plan', ['planner', '?x'], ['object', '?y']]],
# [['grasp', ['actor', '?x'], ['object', '?y']]]
grasp(S1, E1, E2) => plan(take(S1, E1, E2)).


# She got into her car

# [['goal', ['planner', '?x'], ['objective', ['prox', ['actor', '?x'], ['location', '?y']]]]],
# [['use-vehicle-plan', ['planner', '?x']]]
plan(use_vehicle(E1, 'car')) => goal(prox(E1, E2)).

# [['use-vehicle-plan', ['planner', '?x'], ['object', '?y']]],
# [['goal', ['planner', '?x'],
#             ['objective', ['prox', ['actor', '?x'], ['location', '?y']]]], ['isa', 'car', '?y']]
goal(prox(E1, 'car')) => plan(use_vehicle(E1, 'car')).

# [['goal', ['planner', '?x'], ['objective', ['prox', ['actor', '?x'], ['location', '?y']]]]],
# [['walk-plan', ['planner', '?x'], ['location', '?y']]]
plan(walk(S1, E1, E2)) => goal(prox(E1, E2)).

# [['walk-plan', ['planner', '?x'], ['location', '?y']]],
# [['ptrans', ['actor', '?x'], ['object', '?x'], ['to', '?y']]]
get_into(S1, E1, E2), car(E2) => plan(walk(S1, E1, 'car')).

# John was lost.

goal(know(C1, E1, location(C2, E1, L1))) => Plan => goal(be_at(C1, E1, L2)).
lost(C1, E1) => goal(know(C2, E1, location(C2, E1, L1))).


# know_location: goal(know(C1, E1, location(C2, E1, L1)))
# at_location: goal(be_at(C1, E1, L2))

# know_location => Plan => at_location.
# lost(C1, E1) => know_location.

# He pulled over to a farmer standing by the side of the road.

goal(be_near(C1, E1, E2)) => Plan => goal(know(C2, E1, location(C2, E1, L1))).
plan(use_vehicle(C1, E1, E2)) => goal(be_near(C2, E1, E2)).
pull_over(C1, E1), to(C1, E2) => plan(use_vehicle(C2, E1, E2)).
