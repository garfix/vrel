from vrel.core.constants import E1, E2, DUMMY
from vrel.entity.Atom import Atom


def get_write_grammar():
    return [
        # sentences
        {
            "syn": "s() -> 'OK'",
            "if": [Atom("output_type", "ok")],
        },
        {
            "syn": "s() -> 'yes'",
            "if": [Atom("output_type", "yes")],
        },
        {
            "syn": "s() -> 'no'",
            "if": [Atom("output_type", "no")],
        },
        {
            "syn": "s() -> value(E1)",
            "if": [Atom("output_type", "value"), Atom("output_value", E1)],
        },
        {
            "syn": "s() -> text(E1) text(E2)",
            "if": [Atom("output_type", "value_with_unit"), Atom("output_value_with_unit", E1, E2)],
        },
        {
            "syn": "s() -> format(E1)",
            "if": [Atom("output_type", "list"), Atom("output_list", E1)],
            "format": lambda elements: format_list(elements),
        },
        {
            "syn": "s() -> format(E1, E2)",
            "if": [Atom("output_type", "table"), Atom("output_table", E1, E2)],
            "format": lambda results, units: format_table(results, units),
        },
        {
            "syn": "s() -> 'Cheerio.'",
            "if": [Atom("output_type", "close_conversation")],
        },
    ]


def format_list(elements):
    elements.sort()
    return ", ".join(elements)


def format_table(table, units):
    sorted_table = sorted(table, key=lambda row: row[0])
    response = []
    for row in sorted_table:
        item = []
        for i, value in enumerate(row):
            item.append(format_cell(value, units[i]))
        response.append(item)
    return response


def format_cell(value, unit):
    if isinstance(value, float):
        formatted = str(int(value))
    else:
        formatted = value

    if unit != "":
        formatted += f" {unit}"

    return formatted
