"""Package URL identity normalization."""

from __future__ import annotations

import re
from urllib.parse import quote

from .identity_common import required


def package_identity(system: str, name: str, version: str = "") -> str:
    package_type = required(system, "package system").lower()
    package_name = required(name, "package name")
    package_version = version.strip()
    encoded_name = _encode_package_name(package_type, package_name)
    identity = f"pkg:{package_type}/{encoded_name}"
    if package_version:
        identity += f"@{quote(package_version, safe='.+~-')}"
    return identity


def _encode_package_name(package_type: str, package_name: str) -> str:
    if package_type == "npm" and package_name.startswith("@"):
        scope, separator, leaf = package_name.partition("/")
        if not separator or not leaf:
            raise ValueError("scoped npm package name must include a package")
        return f"{quote(scope, safe='')}/{quote(leaf, safe='')}"
    if package_type == "pypi":
        package_name = re.sub(r"[-_.]+", "-", package_name).lower()
    return quote(package_name, safe="/")
