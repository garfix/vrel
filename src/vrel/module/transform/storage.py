from vrel.entity.Atom import Atom


def create_records(atoms: list[Atom]):
    records = []
    for atom in atoms:
        a = Atom(atom.predicate, *atom.arguments)
        records.append(a)
        # todo: consider pre/post
        records.extend(create_records(atom.modifiers))
    return records
