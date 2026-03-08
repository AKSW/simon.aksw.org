#!/usr/bin/env bash
# @(#) All docker RUN commands in one layer
# shellcheck disable=SC1090
# Use the unofficial bash strict mode: http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail; export FS=$'\n\t'

echo "### Upgrade base image"
microdnf update -y
microdnf upgrade -y

echo "### Python environment installation and actitivation"
microdnf install -y tar gzip
curl -LsSf "https://astral.sh/uv/${UV_VERSION}/install.sh" | env UV_UNMANAGED_INSTALL="/usr/local/bin" sh
uv python install "${PYTHON_VERSION}" -i /usr/local --default --no-managed-python --preview-features python-install-default
mv /root/.local/bin/* /usr/local/bin/
rm -rf /root/.local
uv venv "${VIRTUAL_ENV}"
source "${VIRTUAL_ENV}/bin/activate"

echo "### Application installation"
uv pip install uvicorn
uv pip install -r /tmp/requirements.txt
uv pip install --no-deps /tmp/"${APP_PREFIX}"-*.tar.gz

echo "### Output some test results and cleanup"
python --version
uv --version
uv pip list
rm /tmp/"${APP_PREFIX}"* /tmp/requirements.txt

