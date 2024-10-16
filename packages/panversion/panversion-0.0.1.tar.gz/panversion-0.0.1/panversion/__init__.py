from itertools import zip_longest
import re


version_pattern = re.compile(
    r"^"
    # regex from https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string
    r"^(?P<semantic>(?P<sem_major>0|[1-9]\d*)\.(?P<sem_minor>0|[1-9]\d*)\.(?P<sem_patch>0|[1-9]\d*)(?P<prerelease>-[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?)(?P<buildmetadata>\+[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?$"
    # ~ r"|"
    # regex from https://peps.python.org/pep-0440/#appendix-b-parsing-version-strings-with-regular-expressions
    # ~ r"(?P<pep_440>[Vv]?(?:(?:(?P<epoch>[0-9]+)!)?(?P<pep_major>\d*)(\.?(?P<pep_minor>\d*)(\.?(?P<pep_patch>\d*))?)?(?P<pre>[-_\.]?(?P<pre_l>alpha|a|beta|b|preview|pre|c|rc)[-_\.]?(?P<pre_n>[0-9]+)?)?(?P<post>(?:-(?P<post_n1>[0-9]+))|(?:[-_\.]?(?P<post_l>post|rev|r)[-_\.]?(?P<post_n2>[0-9]+)?))?(?P<dev>[-_\.]?(?P<dev_l>dev)[-_\.]?(?P<dev_n>[0-9]+)?)?)(?:\+(?P<local>[a-z0-9]+(?:[-_\.][a-z0-9]+)*))?)"
    r"$"
)


class Version:
    def __init__(self, version):
        self.is_semantic = False
        self.epoch = 0
        self.major = 0
        self.minor = 0
        self.patch = 0
        self.prerelease = []
        self.buildmetadata = ""

        # Parsing verison for comparisons
        parts = version_pattern.match(version)
        if parts is None:
            raise ValueError
        if parts.group("semantic") is not None:
            self.is_semantic = True
            self.major = int(parts.group("sem_major") or "0")
            self.minor = int(parts.group("sem_minor") or "0")
            self.patch = int(parts.group("sem_patch") or "0")
            if parts.group("prerelease") is None:
                self.prerelease = []
            else:
                self.prerelease = parts.group("prerelease")[1:].split(".")
            self.buildmetadata = parts.group("buildmetadata") or ""

    def compare_semantic_prereleases(self, prereleases):
        # https://semver.org/#spec-item-11
        for prerelease in prereleases:
            try:
                self_prerelease = int(prerelease[0])
            except (ValueError, TypeError):
                self_prerelease = prerelease[0]
            try:
                other_prerelease = int(prerelease[1])
            except (ValueError, TypeError):
                other_prerelease = prerelease[1]
            # Identifiers consisting of only digits are compared numerically.
            # Identifiers with letters or hyphens are compared lexically in ASCII sort
            # order.
            if type(self_prerelease) == type(other_prerelease):
                if self_prerelease < other_prerelease:
                    return -1
                elif self_prerelease > other_prerelease:
                    return 1
            else:
                # Numeric identifiers always have lower precedence than non-numeric
                # identifiers.
                if (
                    isinstance(self_prerelease, int) and
                    isinstance(other_prerelease, str)
                ):
                    return -1
                if (
                    isinstance(self_prerelease, str) and
                    isinstance(other_prerelease, int)
                ):
                    return 1
                # A larger set of pre-release fields has a higher precedence than a
                # smaller set, if all of the preceding identifiers are equal.
                if self_prerelease is None:
                    return -1
                if self_prerelease is not None:
                    return 1
        return 0

    def __lt__(self, other):
        if self.epoch < other.epoch:
            return True
        # Semantic Version
        # Precedence is determined by the first difference when comparing each of these
        # identifiers from left to right as follows: Major, minor, and patch versions
        # are always compared numerically.
        if self.major < other.major:
            return True
        if self.minor < other.minor:
            return True
        if self.patch < other.patch:
            return True
        if self.is_semantic:
            # When major, minor, and patch are equal, a pre-release version has lower
            # precedence than a normal version
            if len(self.prerelease) > 0 and len(other.prerelease) == 0:
                return True
            # Precedence for two pre-release versions with the same major, minor, and
            # patch version MUST be determined by comparing each dot separated
            # identifier from left to right until a difference is found as follows.
            if self.compare_semantic_prereleases(
                zip_longest(self.prerelease, other.prerelease)
            ) < 0:
                return True

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __gt__(self, other):
        if self.epoch > other.epoch:
            return True
        # Semantic Version
        # Precedence is determined by the first difference when comparing each of these
        # identifiers from left to right as follows: Major, minor, and patch versions
        # are always compared numerically.
        if self.major > other.major:
            return True
        if self.minor > other.minor:
            return True
        if self.patch > other.patch:
            return True
        if self.is_semantic:
            # When major, minor, and patch are equal, a pre-release version has lower
            # precedence than a normal version
            if len(self.prerelease) == 0 and len(other.prerelease) > 0:
                return True
            # Precedence for two pre-release versions with the same major, minor, and
            # patch version MUST be determined by comparing each dot separated
            # identifier from left to right until a difference is found as follows.
            if self.compare_semantic_prereleases(
                zip_longest(self.prerelease, other.prerelease)
            ) > 0:
                return True

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)

    def __eq__(self, other):
        return (
            self.major == other.major and
            self.minor == other.minor and
            self.patch == other.patch and
            self.prerelease == other.prerelease
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        version = f"{self.major}.{self.minor}.{self.patch}"
        if len(self.prerelease) > 0:
            version = f"{version}-" + ".".join(self.prerelease)
        if self.buildmetadata != "":
            version = f"{version}{self.buildmetadata}"

        return version
