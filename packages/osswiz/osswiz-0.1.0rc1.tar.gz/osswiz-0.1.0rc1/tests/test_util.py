import httpx
import pytest

from osswiz.util import classify_license


@pytest.mark.parametrize(
    "spdx_id, full_text_url",
    [
        (
            "MIT",
            "https://raw.githubusercontent.com/github/choosealicense.com/refs/heads/gh-pages/_licenses/mit.txt",
        ),
        (
            "Apache-2.0",
            "https://raw.githubusercontent.com/github/choosealicense.com/refs/heads/gh-pages/_licenses/apache-2.0.txt",
        ),
        (
            "MPL-2.0",
            "https://raw.githubusercontent.com/github/choosealicense.com/refs/heads/gh-pages/_licenses/mpl-2.0.txt",
        ),
        (
            "GPL-3.0",
            "https://raw.githubusercontent.com/github/choosealicense.com/refs/heads/gh-pages/_licenses/gpl-3.0.txt",
        ),
        (
            "LGPL-3.0",
            "https://raw.githubusercontent.com/github/choosealicense.com/refs/heads/gh-pages/_licenses/lgpl-3.0.txt",
        ),
        (
            "AGPL-3.0",
            "https://raw.githubusercontent.com/github/choosealicense.com/refs/heads/gh-pages/_licenses/agpl-3.0.txt",
        ),
        (
            "BSD-2-Clause",
            "https://raw.githubusercontent.com/github/choosealicense.com/refs/heads/gh-pages/_licenses/bsd-2-clause.txt",
        ),
        (
            "BSD-3-Clause",
            "https://raw.githubusercontent.com/github/choosealicense.com/refs/heads/gh-pages/_licenses/bsd-3-clause.txt",
        ),
    ],
)
def test_classify_license(spdx_id: str, full_text_url: str) -> None:
    # Split at --- since the license text follows the frontmatter
    license_text = httpx.get(full_text_url).text.split("---", 2)[-1].strip()
    assert classify_license(license_text) == spdx_id, license_text
