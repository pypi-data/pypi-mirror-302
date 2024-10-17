from pathlib import Path
from typing import TYPE_CHECKING, Any

from osswiz.util import classify_license, inverse_mapping

if TYPE_CHECKING:
    from osswiz.checks import CheckResult


class LicenseCheck:
    family = "Licensing"


class LIC001(LicenseCheck):
    """Has a license file"""

    @staticmethod
    def check(license_files: list[Path]) -> "CheckResult":
        return len(license_files) > 0


class LIC002(LicenseCheck):
    """License is specified in pyproject.toml"""

    @staticmethod
    def check(pyproject: dict[str, Any]) -> "CheckResult":
        match pyproject:
            case {"project": {"license": license}}:
                return license is not None
        return False


class LIC003(LicenseCheck):
    """License is valid"""

    requires = {"LIC001"}

    @staticmethod
    def check(license_files: list[Path]) -> "CheckResult":
        for license_file in license_files:
            license_text = license_file.read_text()
            license_name = classify_license(license_text)
            if license_name is None:
                return f"Unrecognized license: {license_file.name} ({license_file})"
        return True


class LIC004(LicenseCheck):
    """License metadata in pyproject.toml is valid and compatible with license file(s)"""

    requires = {"LIC002", "LIC003", "LIC005"}

    @staticmethod
    def check(license_files: list[Path], pyproject: dict[str, Any]) -> "CheckResult":
        # Can use the first license since LIC005 ensures they are consistent
        license_file = license_files[0]
        license_text = license_file.read_text()
        license_name = classify_license(license_text)

        match pyproject:
            case {"project": {"license": {"file": lic_file}}}:
                if lic_file != license_file.name:
                    return f"License file in pyproject.toml ({lic_file}) does not match license file ({license_file.name})"
            case {"project": {"license": {"text": spdx_id}}}:
                if license_name != spdx_id:
                    return f"License in pyproject.toml ({spdx_id}) does not match license file ({license_name})"

        # Validate trove classifiers match license
        match pyproject:
            case {"project": {"classifiers": classifiers}}:
                license_classifiers = [
                    c for c in classifiers if c.startswith("License ::")
                ]

                if len(license_classifiers) > 1:
                    short_names = [
                        c.removeprefix("License :: ").removeprefix("OSI Approved :: ")
                        for c in license_classifiers
                    ]
                    return (
                        "Multiple conflicting license trove classifiers found: "
                        + ", ".join(repr(n) for n in short_names)
                    )

                trove_spdx_map = {
                    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)": "GPL-3.0-only",
                    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)": "GPL-3.0-or-later",
                    "License :: OSI Approved :: MIT License": "MIT",
                    "License :: OSI Approved :: Apache Software License": "Apache-2.0",
                }

                for classifier in license_classifiers:
                    spdx_id = trove_spdx_map.get(classifier)
                    if spdx_id is None:
                        return f"Unknown trove classifier: {classifier}"

                    if spdx_id != license_name:
                        return f"License classifier {classifier} does not match license file(s) ({license_name})"

        return True


class LIC005(LicenseCheck):
    """License files are consistent"""

    requires = {"LIC001"}

    @staticmethod
    def check(license_files: list[Path]) -> "CheckResult":
        licenses = {lic: classify_license(lic.read_text()) for lic in license_files}

        if len(set(licenses.values())) > 1:
            filemap = inverse_mapping(licenses)
            return f"Multiple conflicting licenses found: {', '.join([f"{lic} ({', '.join(str(f) for f in files)})" for lic, files in filemap.items()])}"

        return True
