# coding: utf-8
default_language = {"and": "&", "or": "∨", "not": "~", "if": "→", "iff": "↔", "all": "∀", "some": "∃",
                    "contradiction": "⨳"}
lang_rs = "~∃∀"
lang_ops = {"~": 3, "&": 2, "∨": 2, "→": 2, "↔": 2, "∃": 3, "∀": 3, "(": 0}
lang_ops_args = {"~": 1, "&": 2, "∨": 2, "→": 2, "↔": 2, "∃": 2, "∀": 2}


def shunting_yard_statement(statement):
    unit = ""
    symbol_stack = []
    priority = lang_ops
    right_associativity = lang_rs
    operator_stack = []
    for letter in statement:
        if letter >= "a" and letter <= "z":
            unit += letter
        else:
            if unit:
                symbol_stack.append(unit)
            unit = letter if letter.isalpha() or letter == "⨳" else ""  # need to address special characters directly
        if letter == "(":
            operator_stack.append(letter)
        elif letter in priority:
            while len(operator_stack) > 0 and (
                    (pl := priority[letter]) < (ps := priority[operator_stack[-1]])
                    or (ps == pl and operator_stack[-1] not in right_associativity)
            ):
                symbol_stack.append(operator_stack.pop())
            operator_stack.append(letter)
        elif letter == ")":
            while (p := operator_stack.pop()) != "(":
                symbol_stack.append(p)
    if unit:
        symbol_stack.append(unit)
    symbol_stack += operator_stack[::-1]
    return symbol_stack


def endswith(l1, l2):
    return compare(l1[-len(l2):], l2)


def compare(l1, l2):
    return all(map(lambda x: x[0] == x[1], zip(l1, l2)))


def length(stack):
    operator = stack.pop()
    operators = lang_ops_args
    if operator not in operators:
        return 1
    l = []
    for i in range(operators.get(operator, 0)):
        peek = stack[-1]
        if peek not in operators:
            l.insert(0, 1)
            stack.pop()
        else:
            l.insert(0, sum(length(stack)) + 1)
    return l


def choose_next_items(lst, length_map):
    next_items = []
    for length in length_map:
        next_items.append(lst[:length])
        lst = lst[length:]
    return next_items


def operands(stack):
    lengths = length(stack.copy())
    return choose_next_items(stack, lengths)


def diffs(s1, s2, placeholder="X", reverse=False):
    if reverse:
        return "".join(y for x, y in zip(s1, s2) if x != y)
    return "".join([x if x == y else placeholder for x, y in zip(s1, s2)])


def or_out(relies, output):
    negated, fr = sorted(
        relies, key=len
    )  # the line that has the original or must be longer
    if negated[-1] != "~" or fr[-1] != "∨":
        return False
    ops = operands(fr)
    return [negated[:-1], output] == ops or [output, negated[:-1]] == ops


def not_or_out(relies, output):
    if not endswith(relies, ["∨", "~"]):
        return False
    if not output[-1] == "~":
        return False
    return output[:-1] in operands(relies[:-1])


def and_out(relies, output):
    return relies[-1] == "&" and output in operands(relies)


def and_in(relies, output):
    return output[-1] == "&" and all(
        [operand in relies for operand in operands(output)]
    )


def or_in(relies, output):
    return output[-1] == "∨" and relies in operands(output)


def not_and_out(relies, output):
    if not endswith(relies, ["&", "~"]) or not endswith(output, ["~", "→"]):
        return False
    return output[:-2] == relies[:-2]


def iff_in(relies, output):
    if not all(line[-1] == "→" for line in relies) or output[-1] != "↔":
        return False
    ops1, ops2 = [operands(x) for x in relies]
    ops_out = operands(output)
    return ops1[::-1] == ops2 and (ops1 == ops_out or ops2 == ops_out)


def iff_out(relies, output):
    if relies[-1] != "↔" or output[-1] != "→":
        return False
    ops_in = operands(relies)
    ops_out = operands(output)
    return ops_in == ops_out or ops_in[::-1] == ops_out


def not_iff_out(relies, output):
    if not endswith(relies, ["↔", "~"]) or output[-1] != "↔":
        return False
    ops_in = operands(relies[:-1])
    ops_out = operands(output)
    return ops_in[0] + ["~"] == ops_out[0] and ops_in[1] == ops_out[1]


def if_out(relies, output):
    ir, fr = sorted(relies, key=len)  # the line that has the original if must be longer
    if not fr[-1] == "→":
        return False
    if ir + output + ["→"] == fr:  # modus ponens
        return True
    if ir[-1] != "~" or output[-1] != "~":
        return False
    return output[:-1] + ir[:-1] + ["→"] == fr


def not_if_out(relies, output):
    if not endswith(relies, ["→", "~"]) or not endswith(output, ["~", "&"]):
        return False
    return relies[:-2] == output[:-2]


def double_negation(relies, output):
    short, long = sorted([relies, output], key=len)
    return short + ["~", "~"] == long


def rep(relies, output):
    return relies == output


def x_in(relies, output):
    short, long = sorted(relies, key=len)
    return short + ["~"] == long


def all_out(relies, output):
    variable, line = operands(relies)
    if len(line) != len(output):
        return False
    changed_from = set("".join(diffs(b, a, reverse=True) for a, b in zip(line, output)))
    changed_to = set("".join(diffs(a, b, reverse=True) for a, b in zip(line, output)))
    return (
            len(changed_to) == 1
            and len(changed_from) == 1
            and variable[0] in changed_from
            and not any(variable[0] in arg for arg in output)
    )


def exist_out(relies, output):
    variable, line = operands(relies)
    if len(line) != len(output):
        return False
    changed_from = set("".join(diffs(b, a, reverse=True) for a, b in zip(line, output)))
    changed_to = set("".join(diffs(a, b, reverse=True) for a, b in zip(line, output)))
    return (
            len(changed_to) == 1
            and len(changed_from) == 1
            and variable[0] in changed_from
            and not any(variable[0] in arg for arg in output)
    )


def not_all_out(relies, output):
    if not endswith(relies, ["∀", "~"]) or not endswith(output, ["~", "∃"]):
        return False
    return relies[:-2] == output[:-2]


def not_exist_out(relies, output):
    if not endswith(relies, ["∃", "~"]) or not endswith(output, ["~", "∀"]):
        return False
    return relies[:-2] == output[:-2]


def exist_in(relies, output):
    variable, line = operands(output)
    changed_from = set("".join(diffs(b, a, reverse=True) for a, b in zip(relies, line)))
    changed_to = set("".join(diffs(a, b, reverse=True) for a, b in zip(relies, line)))
    return len(changed_to) == 1 and len(changed_from) == 1 and variable[0] in changed_to


# show rules
def show_cd(original, following):
    if original[-1] != "→":
        return False
    assumption, derivation = following
    return assumption + derivation + ["→"] == original


def show_id(original, following):
    assumption, derivation = following
    return original + ["~"] == assumption and derivation == ["⨳"]


# ~D
def show_td(original, following):
    assumption, derivation = following
    return assumption + ["~"] == original and derivation == ["⨳"]


def show_ud(original, following):
    return all_out(original, following)
