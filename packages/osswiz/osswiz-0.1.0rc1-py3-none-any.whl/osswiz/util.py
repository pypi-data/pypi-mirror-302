from collections.abc import Iterable
from typing import TypeVar


def classify_license(license_text: str) -> str | None:
    """Attempt to classify a license based on its text. Returns the SPDX identifier if recognized, otherwise None."""

    # FIXME: Very naive heuristic
    def _is_mit_license(license_text: str) -> bool:
        return "MIT License" in license_text

    def _is_apache2_license(license_text: str) -> bool:
        return "Apache License" in license_text and "Version 2" in license_text

    def _is_gplv3_license(license_text: str) -> bool:
        return (
            "GNU GENERAL PUBLIC LICENSE" in license_text and "Version 3" in license_text
        )

    def _is_lgplv3_license(license_text: str) -> bool:
        return (
            "GNU LESSER GENERAL PUBLIC LICENSE" in license_text
            and "Version 3" in license_text
        )

    def _is_agplv3_license(license_text: str) -> bool:
        return (
            "GNU AFFERO GENERAL PUBLIC LICENSE" in license_text
            and "Version 3" in license_text
        )

    def _is_mozilla2_license(license_text: str) -> bool:
        return "Mozilla Public License Version 2.0" in license_text

    def _is_bsd_2_clause_license(license_text: str) -> bool:
        return "BSD 2-Clause License" in license_text

    def _is_bsd_3_clause_license(license_text: str) -> bool:
        return "BSD 3-Clause License" in license_text

    # SPDX identifiers to checks
    checks = {
        "MIT": _is_mit_license,
        "Apache-2.0": _is_apache2_license,
        "MPL-2.0": _is_mozilla2_license,
        "GPL-3.0": _is_gplv3_license,
        "LGPL-3.0": _is_lgplv3_license,
        "AGPL-3.0": _is_agplv3_license,
        "BSD-2-Clause": _is_bsd_2_clause_license,
        "BSD-3-Clause": _is_bsd_3_clause_license,
    }

    license_name = next((name for name, fn in checks.items() if fn(license_text)), None)
    return license_name


K = TypeVar("K")
V = TypeVar("V")


def inverse_mapping(m: dict[K, V]) -> dict[V, Iterable[K]]:
    """Invert a mapping of unique values to unique keys to a mapping of unique values to sets of keys.

    Examples
    --------
    >>> result = inverse_mapping({1: "a", 2: "b", 3: "a"})
    >>> {k: v for k, v in sorted(result.items())}
    {'a': {1, 3}, 'b': {2}}
    """
    return {v: {k for k, vv in m.items() if vv == v} for v in set(m.values())}
