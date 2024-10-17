from importlib.abc import Traversable


def license_files(root: Traversable) -> list[Traversable]:
    """Identify common license files in the repository"""
    prefixes = ("LICENSE", "COPYING")
    return [f for f in root.iterdir() if f.name.startswith(prefixes)]
