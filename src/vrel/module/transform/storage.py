from vrel.entity.Atom import MODIFIER_POSITION_PRE, Atom


def create_records(atoms: list[Atom]):
    records = []
    for atom in atoms:
        flat = atom.flatten()
        if atom.type == MODIFIER_POSITION_PRE:
            records.extend(create_records(atom.get_modifier_atoms()))
            records.append(flat)
        else:
            records.append(flat)
            records.extend(create_records(atom.get_modifier_atoms()))
    return records
