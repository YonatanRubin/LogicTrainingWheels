from openpyxl import *
from openpyxl.styles import PatternFill
import logic_rules as proof
from tkinter.filedialog import askopenfilename
from shutil import which
import shlex
import configparser
import os
import re

langmap = configparser.ConfigParser()

ERROR = PatternFill(start_color="2d0c45", end_color="2d0c45", fill_type="solid")
RED = PatternFill(start_color="00FF0000", end_color="00FF0000", fill_type="solid")
GREEN = PatternFill(start_color="0000FF00", end_color="0000FF00", fill_type="solid")
YELLOW = PatternFill(start_color="FFFF0000", end_color="FFFF0000", fill_type="solid")


def always_valid(*args, **kwargs):
    return True


def always_invalid(*args, **kwargs):
    return False


def ignore(*args, **kwargs):
    return None


reason_map = {
    "∨O": proof.or_out,
    "∨I": proof.or_in,
    "~∨O": proof.not_or_out,
    "&O": proof.and_out,
    "&I": proof.and_in,
    "~&O": proof.not_and_out,
    "→O": proof.if_out,
    "~→O": proof.not_if_out,
    "↔O": proof.iff_out,
    "↔I": proof.iff_in,
    "~↔O": proof.not_iff_out,
    "DN": proof.double_negation,
    "REP": proof.rep,
    "⨳I": proof.x_in,
    "∀O": proof.all_out,
    "~∀O": proof.not_all_out,
    "∃O": proof.exist_out,
    "∃I": proof.exist_in,
    "~∃O": proof.not_exist_out,
    "PR": always_valid,
    "AS": ignore,
}

show_map = {
    "DD": (0, always_valid),
    "~D": (2, proof.show_td),
    "ID": (2, proof.show_id),
    "CD": (2, proof.show_cd),
    "∀D": (1, proof.show_ud),
    "UD": (1, proof.show_ud)
}


def extract_reason(line):
    line = clean_language(line)
    rule = re.findall(r"[^0-9\ \,\.]+", line)
    sources = re.findall(r"[0-9]+", line)
    verification_method = reason_map.get(rule[0].upper(), always_invalid)
    return [int(i) for i in sources], verification_method


def extract_show_follow(tp):
    return show_map[tp.upper()]


def find_start(column):
    for index, cell in enumerate(column):
        if cell.value is not None:
            return index + 1


def clean_language(line):
    if "symbols" not in langmap:
        return line
    for operand, symbol in langmap["symbols"].items():
        line = line.replace(symbol, proof.default_language[operand])
    return line


def clean_line(line):
    if not line:
        return line
    line = clean_language(line)
    return line.replace("[", "(").replace("]", ")").replace(" ", "").rstrip()


def handle_showline(sheet, index):
    tp = clean_language(sheet.cell(index, 3).value)
    if tp is None or tp == "":
        sheet.cell(index, 3).fill = YELLOW
        return
    p = re.compile("show:?", re.IGNORECASE)
    show = proof.shunting_yard_statement(p.sub("", clean_line(sheet.cell(index, 2).value)))
    following_size, rule = extract_show_follow(tp)
    following = [p.sub("", clean_line(sheet.cell(index + line + 1, 2).value)) for line in range(following_size)]
    following = list(map(proof.shunting_yard_statement, following))

    if len(following) <= 1:
        valid = rule(show, *following)
    else:
        valid = rule(show, following)

    if valid is None:
        return
    elif not valid:
        for line in range(following_size + 1):
            sheet.cell(index + line, 3).fill = RED
    else:
        for line in range(following_size + 1):
            sheet.cell(index + line, 3).fill = GREEN


def handle_proofline(sheet, index, proof_index):
    output = clean_line(sheet.cell(index, 2).value)
    reason = sheet[f"C{index}"].value
    if reason is None or reason == "":
        sheet.cell(index, 3).fill = YELLOW
        return
    relies, rule = extract_reason(reason)
    indices = [index - (proof_index - i) for i in relies]
    relies = list(
        map(
            proof.shunting_yard_statement,
            map(lambda cell: clean_line(sheet.cell(cell, 2).value), indices),
        )
    )
    if len(relies) <= 1:
        valid = rule(*relies, proof.shunting_yard_statement(output))
    else:
        valid = rule(relies, proof.shunting_yard_statement(output))
    if valid is None:
        return
    elif not valid:
        sheet.cell(index, 3).fill = RED
    else:
        sheet.cell(index, 3).fill = GREEN


def verify_excel(file):
    wb = load_workbook(file, data_only=True)
    sheet = wb.active
    index = find_start(sheet["C"])
    while sheet[f"A{index}"].value is not None:
        index += 1
        try:
            proof_index = sheet.cell(index, 1).value
            output = clean_line(sheet.cell(index, 2).value)
            if not output:
                continue
            if not isinstance(proof_index, int):
                continue
            if "SHOW" in output.upper():
                handle_showline(sheet, index)
            else:
                handle_proofline(sheet, index, proof_index)
        except Exception as e:
            print(e)
            sheet.cell(index, 3).fill = ERROR
    name = file.split(".")[0]
    wb.save(f"{name}-checked.xlsx")


def verify_ods(f):
    libreoffice = which("libreoffice") or which("LibreOffice")
    if libreoffice is None:
        print("ERROR: LibreOffice is not installed but required for ods support")
        return False
    path = os.path.dirname(f)
    os.chdir(path)
    command = f"{libreoffice} --headless --invisible --convert-to xlsx {shlex.quote(f)}"
    print(command)
    os.system(command)
    converted = f.replace(".ods", ".xlsx")

    verify_excel(converted)

    checked = f.replace(".ods", "-checked.xlsx")
    command = (
        f"{libreoffice} --headless --invisible --convert-to ods {shlex.quote(checked)}"
    )
    print(command)
    os.system(command)
    os.remove(converted)
    os.remove(checked)
    return True


def verify_file(f):
    if f.endswith(".xlsx"):
        verify_excel(f)
        return True
    if f.endswith(".ods"):
        return verify_ods(f)
    return False


if __name__ == "__main__":
    langmap.read_dict(
        {"symbols": {"or": "||", "not": "!", "if": ">>", "iff": "<>", "all": "@", "some": "#", "contradiction": "XX"}})
    f = ""
    home_directory = os.path.expanduser("~")
    documents_directory = os.path.join(home_directory, "Documents")

    while not verify_file(f):
        f = askopenfilename(
            initialdir=documents_directory,
            filetypes=(("Spreadsheet files", "*.xlsx *.ods"), ("All Files", "*.*")),
        )
