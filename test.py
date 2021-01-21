"""
Programmatically lint and write results.
"""
from pylint.lint import Run


data = {}

run = Run(['--rcfile', '.pylint', 'main.py'], do_exit=False)
data["pylint-score"] = round(run.linter.stats["global_note"], ndigits=2)
readme = open("README.md", "r")
readme_text = readme.read()
readme.close()
readme = open("README.md", "w")
readme.write(readme_text.replace("{{pylint-score}}", str(data["pylint-score"])))
readme.close()
