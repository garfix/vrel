from vrel.entity.Atom import MODIFIER_POSITION_PRE, Atom


def create_records(atoms: list[Atom]):
    """
    Convert atoms to a list of storable records (currently also atoms, just not nested)
    TODO: conditional constructions (if ... then ...) should be returned in this conditional form, not as facts
    """
    records = []
    for atom in atoms:
        flat = atom.flatten()
        records.append(flat)
        records.extend(create_records(atom.get_modifier_atoms()))
    return records
