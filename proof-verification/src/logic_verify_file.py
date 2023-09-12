from openpyxl import *
from openpyxl.styles import PatternFill
from openpyxl.workbook import workbook
from openpyxl.xml import lxml_available
import logic_rules as proof
from tkinter.filedialog import askopenfilename
from shutil import which
import shlex
import os

RED = PatternFill(start_color="00FF0000", end_color="00FF0000", fill_type="solid")
GREEN = PatternFill(start_color="0000FF00", end_color="0000FF00", fill_type="solid")
YELLOW = PatternFill(start_color="FFFF0000", end_color="FFFF0000", fill_type="solid")


def always_valid(*args, **kwargs):
    return True


def always_invalid(*args, **kwargs):
    return False


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
    "AS": always_valid,
}


def extract_reason(line):
    reasons = line.split(" ")
    verification_method = reason_map.get(reasons[-1].upper(), always_invalid)
    return [int(i) for i in reasons[:-1]], verification_method


def find_start(column):
    for index, cell in enumerate(column):
        if cell.value is not None:
            return index + 1


def clean_line(line):
    if not line:
        return line
    return line.replace("[", "(").replace("]", ")").replace(" ", "").rstrip()


def verify_excel(file):
    wb = load_workbook(file, data_only=True)
    sheet = wb.active
    index = find_start(sheet["C"])
    while sheet[f"A{index}"].value is not None:
        index += 1
        proof_index = sheet.cell(index, 1).value
        output = clean_line(sheet.cell(index, 2).value)
        if not output:
            print(index)
            continue
        if not isinstance(proof_index, int) or "SHOW" in output.upper():
            continue
        reason = sheet[f"C{index}"].value
        if reason is None or reason == "":
            continue
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
        if not valid:
            sheet.cell(index, 3).fill = RED
            print(output, reason, valid)
            print(relies)
            print(proof.shunting_yard_statement(output))
        else:
            sheet.cell(index, 3).fill = GREEN
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
    f = ""
    home_directory = os.path.expanduser("~")
    documents_directory = os.path.join(home_directory, "Documents")

    while not verify_file(f):
        f = askopenfilename(
            initialdir=documents_directory,    
            filetypes=(("Spreadsheet files", "*.xlsx *.ods"), ("All Files", "*.*"))
        )
