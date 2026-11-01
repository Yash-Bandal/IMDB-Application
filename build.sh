#!/usr/bin/env bash
set -euo pipefail

export ACCEPT_EULA=Y
export DEBIAN_FRONTEND=noninteractive

if [ "$(id -u)" -eq 0 ]; then
    SUDO=()
else
    if ! command -v sudo >/dev/null 2>&1; then
        echo "Installing Microsoft ODBC Driver 18 requires root access or sudo." >&2
        exit 1
    fi
    SUDO=(sudo)
fi

temporary_directory="$(mktemp -d)"
trap 'rm -rf "$temporary_directory"' EXIT

curl -fsSLo "$temporary_directory/packages-microsoft-prod.deb" \
    https://packages.microsoft.com/config/debian/12/packages-microsoft-prod.deb
"${SUDO[@]}" dpkg -i "$temporary_directory/packages-microsoft-prod.deb"
"${SUDO[@]}" apt-get update
"${SUDO[@]}" env ACCEPT_EULA=Y DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --no-install-recommends msodbcsql18

python -m pip install -r requirements.txt
python -c "import pyodbc; assert 'ODBC Driver 18 for SQL Server' in pyodbc.drivers(), 'Microsoft ODBC Driver 18 was not installed'"
