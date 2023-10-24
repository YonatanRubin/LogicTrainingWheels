# Proof Verification

Making mistakes in proofs is normal; however, without a way to check if you've made a mistake, you can't learn and
improve. In practice, it`s sometimes easier to learn the reasons through the rules, even though we generally want to
understand the reasons behind the rules. Knowing that you know the rules is crucial for learning the reasons. This tool
aims to help you verify that you know the rules, assisting you in understanding if you are making errors in your proofs.

## Installation

*Note:* If you want to use this tool with .ods files, you need to have LibreOffice installed.

### As an app

If you're not a technical user and don't want to use the terminal to check your proofs, you can download the .exe file
from the [releases](https://github.com/YonatanRubin/LogicTrainingWheels/releases/latestlatest/download/logic_verify_file.exe) page. Simply download and run the executable file.

### From Source

1. If you don't have Python installed, install Python first.
2. Download the source code from this library.
3. Run `pip install -r requirements.txt` to install the necessary packages.
4. Run `python logic_verify_file.py` to check a file.

## Configuration

The default symbols used by this tool are the formal symbols found in the book, and provided by the keyboard in this
repository for easy access. However, these symbols are Unicode characters and may not be well-supported in all text
editors. You can override these symbols and define a custom symbol set in the configuration file. The configuration file
should look like this:

```ini
[symbols]
not=~
and=&
or=∨
if=→
iff=↔
contradiction=⨳
all=∀
some=∃
```

Place this configuration file either in the same folder as the executable or in one of the following locations:

**Windows:**

1. %APPDATA%/logic/proof-verification.ini

**Linux:**

1. /etc/proof-verification.ini
2. /usr/local/etc/proof-verification.ini
3. ~/.config/logic/proof-verification.ini

## Supported Files and Formats

This script supports the following file formats:

- Sheet files (.xlsx and .ods if LibreOffice is installed)
- Microsoft Word files (.docx)
- Plain Text (.txt)

The script attempts to support as many formats as possible for these files, but there are specific requirements for each
filetype. If you encounter errors, you should check the format of the file.

### Sheet Files

Sheet files assume there are three columns:

- Column **A** for the row number in the proof (used for justification), which should be a number.
- Column **B** for the actual statements.
- Column **C** for the justification for each row.

Each file can contain multiple proofs, as long as each proof restarts the numbering in column A. The verification will
create a new file named `**original_file**-checked.xlsx`. This file will contain the original proofs with justification
colors according to the following rules:

- <span style="color:green">GREEN</span> when the statement follows from the justification or a showline, and its
  related lines are in accordance with the specified method.
- <span style="color:red">RED</span> when it does not.
- <span style="color:yellow">YELLOW</span> when there is no justification for the line.
- <span style="color:purple">PURPLE</span> when there was an error in checking the justification. This usually indicates
  that either the statement was not a valid statement or that the justification does not have enough rows as it should.

### Docs File

Docs files assume a table for each proof. The table should have 3 columns:

- First column for the row number in the proof (used for justification).
- Second column with the actual statements.
- Third column with the justification for each row.

The verification will create a new file named `**original_file-checked**.docx`. This file will contain the original proofs
with justification colors according to the following rules:

- <span style="color:green">GREEN</span> when the statement follows from the justification or a showline, and its
  related lines are in accordance with the specified method.
- <span style="color:red">RED</span> when it does not.
- <span style="color:yellow">YELLOW</span> when there is no justification for the line.
- <span style="color:purple">PURPLE</span> when there was an error in checking the justification. This usually indicates
  that either the statement was not a valid statement or that the justification does not have enough rows as it should.

You can also write as text, but due to the indifference between two different lines being a single paragraph or two
paragraphs, the output will be the same as a plain text file.

### Plain Text

The plain text assumes a group of rows, each with a number separated in some way from the main statement, which is
separated again from the justification. The separators can be a combination of the following: `,`, `.`, `|`, or
spaces.  
Some examples for plain text:

```text
1. A→B PR
2| ~B | PR
3,Show: ~A, ~D
4. A | AS
5. Show: ⨳.DD
```

The verification will create a new file named `**original_file**-checked.txt`. This file will contain the original
proofs and add an indicator for the legality of the move:

- [**V**] when the statement follows from the justification or a showline, and its related lines are in accordance with
  the specified method.
- [**X**] when it does not.
- [**?**] when there is no justification for the line.
- [**!!!**] when there was an error in checking the justification. This usually indicates that either the statement was
  not a valid statement or that the justification does not have enough rows as it should.
