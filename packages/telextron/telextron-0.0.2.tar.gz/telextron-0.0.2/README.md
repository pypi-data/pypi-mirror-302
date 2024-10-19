# TelexTron

Python stuff for teletext in the terminal.

* Install: `pip install telextron`
* View tti file: `python -m telextron.ttiview titi.tti`
* View t42 stream: `while cat recording.t42; do :; done | pv --quiet --rate-limit 867K | python -m telextron.t42view`

## Development

* Install
```
pip install --constraint requirements-dev.txt --editable '.[dev]'
```
* Check
```
ruff format --check src/telextron/t42view.py
ruff check src/telextron/t42view.py
pyright src/telextron/t42view.py
```
* Upgrade dependencies
```
pip-compile --upgrade --output-file=requirements.txt --strip-extras
pip-compile --upgrade --extra=dev --output-file=requirements-dev.txt --strip-extras
```
