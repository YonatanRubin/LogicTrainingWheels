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
Windows:

1. %APPDATA%/logic/proof-verification.ini  
  
Linux:
1. /etc/proof-verification.ini
2. /usr/local/etc/proof-verification.ini
3. ~/.config/logic/proof-verification.ini

## Supported Files and Formats
