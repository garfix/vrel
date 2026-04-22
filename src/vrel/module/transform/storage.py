from vrel.entity.Atom import MODIFIER_TYPE_PRE, Atom


def create_records(atoms: list[Atom]):
    records = []
    for atom in atoms:
        flat = atom.flatten()
        if atom.type == MODIFIER_TYPE_PRE:
            records.extend(create_records(atom.modifiers))
            records.append(flat)
        else:
            records.append(flat)
            records.extend(create_records(atom.modifiers))
    return records
