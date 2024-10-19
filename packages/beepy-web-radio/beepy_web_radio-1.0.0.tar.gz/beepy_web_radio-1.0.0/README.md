# Beepy Web Radio

Beepy app to play web radio


## Project Initialization/Quickstart

To init this project, after running the cookiecutter:

```
$ git init
$ just init
$ just test
$ just run
$ git add * .*
$ git commit -am "Initial commit."
$ git branch -M main
$ git remote add origin git@github.com:conor-f/Beepy Web Radio.git  # Note this may need to be modified based on your Github username/repo name.
$ git push -u origin main
```

Don't forget to add your PyPi secrets to your github repo under `PYPI_API_TOKEN`.


When you're ready for this application to appear on the `bapp-store`, add the `beepy-app` as a topic/tag to your Github repo.

## License

This project is licensed under the GPLv3 license.


## Pre-commit Hooks

This template includes pre-commit hooks for linting, formatting, and type-checking.

The hooks will run automatically on every commit, applying the specified checks and auto-formatting without asking for confirmation.

The pre-commit configuration includes:
- Black (code formatting)
- isort (import sorting)
- Flake8 (linting)
- MyPy (type checking)
- Various file checks (trailing whitespace, YAML validation, etc.)
