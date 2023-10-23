# Proof Verification

Making mistakes in proofs is normal, however without a way to check if you made a mistake you cannot learn and
improve.  
Generally we want to learn the reason behind the rules, but in practice it is sometimes easier to learn the reasons
through the rules.
That is why knowing that you know the rules is crucial to learn the reasons. This tool is aimed to help exactly in this
way - verify that you know the rules to help you understand if you are making stuff up.

## Installation

*Note:* If you want to use this with ods files you need libreoffice installed.

### From Source

1. If you don't have python installed, install python first.
2. Download the source from this library
3. Run `pip install -r requirements.txt` to install the sources.
4. Run `python logic_verify_file.py` to check a file

### For Windows Users

Assuming you are not a technical person and don't want to start using the terminal just to check your proofs you can
download the `.exe` file from the releases page.   
After that just click on it and run.

## Configuration

The default symbols this code works with are the formal symbols used in the book, and supplied by the keyboard in this
repo for easy access. Still, those are Unicode symbols which might not have the best support across all editors. You can
override those symbols and define a custom symbol set in the _configuration file_.
The configuration file should look like this:

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

And should be placed either in the same folder as the executable or in one of the following places:
**Windows:**

1. %APPDATA%/logic/proof-verification.ini

**Linux:**

1. /etc/proof-verification.ini
2. /usr/local/etc/proof-verification.ini
3. ~/.config/logic/proof-verification.ini

## Supported Files and Formats

The script supports the following files:

* Sheet files (`.xlsx` and `ods` if libreoffice is installed)
* Microsoft Word files (`.docx`)
* Plain Text (`.txt`)

The code tries to support as many formats as possible for this files, but there are still some requirements for each
filetype. You should just try with a given file and check the format if you get errors.

### Sheet files

Sheet files assumes that there are 3 columns:

* column **A** for row number in the proof (the one you use for justification). This should be a number.
* column **B** with the actual statements.
* column **C** with the justification for each row.

Each file can contain as many proofs as you want as long as each proof restarts the numbering (in column `A`)

### Docs File

Docs files assumes a table for each proof. The table should have 3 columns:

* First column for row number in the proof (the one you use for justification).
* Second column with the actual statements.
* Third column with the justification for each row.

You can also write as text, but due to the indifference between two different lines being a single paragraph or two
paragraphs the output will be the same as a plain text file.

### Plain text

The plain text assumes a group of rows, each with a number separated in some way from the main statement which is
separated again from the justification.
The separators can be a combination of the following: `,` `.` `|` or ` `(spaces).  
Some examples for plain text:
```text
1. A→B PR
2| ~B | PR
3,Show: ~A, ~D
4. A | AS
5. Show: ⨳.DD
```