from typing import TypeAlias, cast

import repo_review
import repo_review.checks

from osswiz.checks.licenses import LicenseCheck

CheckResult: TypeAlias = bool | str | None


def repo_review_checks() -> dict[str, repo_review.checks.Check]:
    license_checks = {
        # Need to cast here since we're not explicitly implementing the Check protocol,
        # which doesn't allow for fixture arguments to the `check` method.
        p.__name__: cast(repo_review.checks.Check, p)
        for p in LicenseCheck.__subclasses__()
    }
    return license_checks
