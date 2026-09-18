import mobase


def _comparablePair(organiser: mobase.IOrganizer, version: str):
    """Returns the running Mod Organizer version and a target version to compare it to.

    IOrganizer.version() returns a mobase.Version, while the deprecated
    appVersion() it replaced returns a mobase.VersionInfo. Those are separate
    types with no conversion or comparison between them, so both halves of the
    pair are always produced by the same API. Older Mod Organizer releases have
    neither IOrganizer.version nor mobase.Version, which is why the newer path
    is attempted first rather than assumed.
    """
    try:
        return organiser.version(), mobase.Version.parse(version)
    except (AttributeError, TypeError, ValueError):
        return organiser.appVersion(), mobase.VersionInfo(version)


def moVersionAtLeast(organiser: mobase.IOrganizer, version: str) -> bool:
    """Determines whether the running Mod Organizer is at least the given version."""
    running, target = _comparablePair(organiser, version)
    return running >= target


def moVersionAtMost(organiser: mobase.IOrganizer, version: str) -> bool:
    """Determines whether the running Mod Organizer is at most the given version."""
    running, target = _comparablePair(organiser, version)
    return running <= target
