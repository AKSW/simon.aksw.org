# simon.aksw.org

Kondolenzbuch für unseren Kollegen Simon Bin
  
[![poetry][poetry-shield]][poetry-link] [![ruff][ruff-shield]][ruff-link] [![mypy][mypy-shield]][mypy-link] [![copier][copier-shield]][copier] 

## Start Container

```
$ cat .env
SIMON_AKSW_ORG_DATA_DIR=/data
SIMON_AKSW_ORG_ALLOW_MESSAGES=true
SIMON_AKSW_ORG_SHOW_MESSAGES=true
SIMON_AKSW_ORG_RECAPTCHA_SECRET_KEY=...
SIMON_AKSW_ORG_RECAPTCHA_SITE_KEY=...

$ docker run --pull=always -i -t --rm -p 5050:5050 --env-file .env -v ./data:/data ghcr.io/aksw/simon.aksw.org:1.1.0
```


## Development

- Run [task](https://taskfile.dev/) to see all major development tasks.
- Use [pre-commit](https://pre-commit.com/) to avoid errors before commit.
- This repository was created with [this copier template](https://github.com/eccenca/cmem-plugin-template).


[poetry-link]: https://python-poetry.org/
[poetry-shield]: https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json
[ruff-link]: https://docs.astral.sh/ruff/
[ruff-shield]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&label=Code%20Style
[mypy-link]: https://mypy-lang.org/
[mypy-shield]: https://www.mypy-lang.org/static/mypy_badge.svg
[copier]: https://copier.readthedocs.io/
[copier-shield]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-purple.json
