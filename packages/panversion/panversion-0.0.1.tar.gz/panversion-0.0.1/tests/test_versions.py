import pytest

from panversion import Version


def test_semantic_error():
    with pytest.raises(ValueError):
        Version("foobar")


def test_semantic_representation():
    assert str(Version("1.0.0")) == "1.0.0"
    assert str(Version("1.0.0-alpha")) == "1.0.0-alpha"
    assert str(Version("1.0.0-alpha+build")) == "1.0.0-alpha+build"
    assert str(Version("1.0.0+build")) == "1.0.0+build"


def test_semantic_equality():
    assert Version("1.0.0") == Version("1.0.0")
    assert Version("1.0.0-alpha") == Version("1.0.0-alpha+build")


def test_semantic_non_equality():
    assert Version("1.0.0") != Version("1.0.1")
    assert Version("1.0.0-alpha") != Version("1.0.1-alpha+build")


def test_semantic_lesser_than_major():
    assert Version("1.0.0") < Version("2.0.0")


def test_semantic_lesser_than_minor():
    assert Version("1.0.0") < Version("1.1.0")
    assert Version("1.8.0") < Version("1.10.0")


def test_semantic_lesser_than_patch():
    assert Version("1.0.0") < Version("1.0.1")
    assert Version("1.0.8") < Version("1.0.10")


def test_semantic_lesser_than_prerelease():
    assert Version("1.0.0-rc.1") < Version("1.0.0")
    assert Version("1.0.0-alpha") < Version("1.0.0-alpha.1")
    assert Version("1.0.0-alpha.1") < Version("1.0.0-alpha.beta")
    assert Version("1.0.0-0.3.7") < Version("1.0.0-alpha.beta")
    assert Version("1.0.0-alpha.beta") < Version("1.0.0-x.7.z.92")
    assert Version("1.0.0-x.7.z.92") < Version("1.0.0-x-y-z.--")
    assert Version("1.0.0-alpha.beta") < Version("1.0.0-rc.1")


def test_semantic_lesser_than_or_equal():
    assert Version("1.0.0") <= Version("1.0.0")
    assert Version("1.0.0+build") <= Version("1.0.0")
    assert Version("1.0.0") <= Version("2.0.0")
    assert Version("1.0.0") <= Version("1.1.0")
    assert Version("1.8.0") <= Version("1.10.0")
    assert Version("1.0.0") <= Version("1.0.1")
    assert Version("1.0.8") <= Version("1.0.10")
    assert Version("1.0.0-rc.1") <= Version("1.0.0")
    assert Version("1.0.0-alpha") <= Version("1.0.0-alpha+build")
    assert Version("1.0.0-alpha") <= Version("1.0.0-alpha.1")
    assert Version("1.0.0-alpha.1") <= Version("1.0.0-alpha.beta")
    assert Version("1.0.0-0.3.7") <= Version("1.0.0-alpha.beta")
    assert Version("1.0.0-alpha.beta") <= Version("1.0.0-x.7.z.92")
    assert Version("1.0.0-x.7.z.92") <= Version("1.0.0-x-y-z.--")
    assert Version("1.0.0-alpha.beta") <= Version("1.0.0-rc.1")


def test_semantic_greater_than():
    assert Version("1.0.0") > Version("1.0.0-rc.1")
    assert Version("1.0.0-alpha.1") > Version("1.0.0-alpha")
    assert Version("1.0.0-alpha.beta") > Version("1.0.0-alpha.1")
    assert Version("1.0.0-alpha.beta") > Version("1.0.0-0.3.7")
    assert Version("1.0.0-x.7.z.92") > Version("1.0.0-alpha.beta")
    assert Version("1.0.0-x-y-z.--") > Version("1.0.0-x.7.z.92")
    assert Version("1.0.0-rc.1") > Version("1.0.0-alpha.beta")


def test_semantic_greater_than_or_equal():
    assert Version("1.0.0") >= Version("1.0.0")
    assert Version("1.0.0") >= Version("1.0.0+build")
    assert Version("2.0.0") >= Version("1.0.0")
    assert Version("1.1.0") >= Version("1.0.0")
    assert Version("1.10.0") >= Version("1.8.0")
    assert Version("1.0.1") >= Version("1.0.0")
    assert Version("1.0.10") >= Version("1.0.8")
    assert Version("1.0.0") >= Version("1.0.0-rc.1")
    assert Version("1.0.0-alpha") >= Version("1.0.0-alpha+build")
    assert Version("1.0.0-alpha.1") >= Version("1.0.0-alpha")
    assert Version("1.0.0-alpha.beta") >= Version("1.0.0-alpha.1")
    assert Version("1.0.0-alpha.beta") >= Version("1.0.0-0.3.7")
    assert Version("1.0.0-x.7.z.92") >= Version("1.0.0-alpha.beta")
    assert Version("1.0.0-x-y-z.--") >= Version("1.0.0-x.7.z.92")
    assert Version("1.0.0-rc.1") >= Version("1.0.0-alpha.beta")


# ~ def test_equality():
    # ~ assert Version("1.0") == Version("1.0.0")


# ~ def test_inequality():
    # ~ assert Version("1.0") != Version("1.0.1")


# ~ def test_lesser_than():
    # ~ assert Version("1.0") < Version("1.0.1")
    # ~ assert Version("1.1.0") < Version("2.1.0")
    # ~ assert Version("2.1.0") < Version("3.1.0")


# ~ def test_semantic_lesser_than_other_without_prerelease():
    # ~ assert Version("1.0.0-rc.1") < Version("1.0.0")
    # ~ assert Version("1.0.0-alpha.beta") < Version("1.0.0")
    # ~ assert Version("1.0.0-alpha") < Version("1.0.0")
    # ~ assert Version("1.0.0-alpha.1") < Version("1.0.0")
    # ~ assert Version("1.0.0-0.3.7") < Version("1.0.0")
    # ~ assert Version("1.0.0-x.7.z.92") < Version("1.0.0")
    # ~ assert Version("1.0.0-x-y-z.--") < Version("1.0.0")


# ~ def test_semantic_lesser_than_other_with_prerelease():
    # ~ assert Version("1.0.0-rc.1") < Version("1.0.0-beta.11")
    # ~ assert Version("1.0.0-alpha") < Version("1.0.0-alpha.beta")
    # ~ assert Version("1.0.0-alpha.1") < Version("1.0.0-alpha.beta")
    # ~ assert Version("1.0.0-alpha") < Version("1.0.0-beta")
    # ~ assert Version("1.0.0-alpha") < Version("1.0.0-beta.11")


# ~ def test_semantic_lesser_than_with_build():
    # ~ assert Version("1.0.0-rc.1+build") < Version("1.0.0-beta.11")
    # ~ assert Version("1.0.0-alpha+build") < Version("1.0.0-alpha.beta")
    # ~ assert Version("1.0.0-alpha.1") < Version("1.0.0-alpha.beta+build")
    # ~ assert Version("1.0.0-alpha") < Version("1.0.0-beta+build")
    # ~ assert Version("1.0.0-alpha+build") < Version("1.0.0-beta.11")


# ~ def test_pep440_lesser_than():
    # ~ assert Version("0.9") < Version("1.0.0")
    # ~ assert Version("1.0a1") < Version("1.0a2")
    # ~ assert Version("1.0a1") < Version("1.0.0")
    # ~ assert Version("1.0") < Version("1.1a1")


# ~ def test_lesser_than_or_equal():
    # ~ assert Version("1.0") <= Version("1.0.0")
    # ~ assert Version("1.0") <= Version("1.0.1")
    # ~ assert Version("1.1.0") <= Version("2.1.0")
    # ~ assert Version("2.1.0") <= Version("3.1.0")
    # ~ assert Version("1.0.0-rc.1") <= Version("1.0.0")
    # ~ assert Version("1.0.0-alpha.beta") <= Version("1.0.0")
    # ~ assert Version("1.0.0-alpha") <= Version("1.0.0")
    # ~ assert Version("1.0.0-rc.1") <= Version("1.0.0-beta.11")
    # ~ assert Version("1.0.0-alpha") <= Version("1.0.0-alpha.beta")
    # ~ assert Version("1.0.0-alpha.1") <= Version("1.0.0-alpha.beta")
    # ~ assert Version("1.0.0-alpha") <= Version("1.0.0-beta")
    # ~ assert Version("1.0.0-alpha") <= Version("1.0.0-beta.11")
    # ~ assert Version("0.9") <= Version("1.0.0")
    # ~ assert Version("1.0a1") <= Version("1.0a2")
    # ~ assert Version("1.0a1") <= Version("1.0.0")
    # ~ assert Version("1.0") <= Version("1.1a1")
    # ~ assert Version("1.0") <= Version("1.0.0+build_foobar")


# ~ def sorting_comparison(versions_to_compare):
    # ~ result_expected = [version for version in versions_to_compare]
    # ~ assert result_expected == sorted(versions_to_compare[::-1], key=Version)


# ~ def test_simple_versions():
    # ~ sorting_comparison(
        # ~ [
            # ~ "1.1.0",
            # ~ "2.1.0",
            # ~ "3.1.0",
        # ~ ]
    # ~ )


# ~ def test_strange_versions():
    # ~ sorting_comparison(
        # ~ [
            # ~ "4.5.5",
            # ~ "04.05.06",
            # ~ "4.5.7",
        # ~ ]
    # ~ )


# ~ def test_big_sub_versions():
    # ~ sorting_comparison(
        # ~ [
            # ~ "1.8.0",
            # ~ "1.9.0",
            # ~ "1.12.0",
        # ~ ]
    # ~ )


# ~ def test_semantic_versions():
    # ~ sorting_comparison(
        # ~ [
            # ~ "1.0.0-alpha",
            # ~ "1.0.0-alpha.1",
            # ~ "1.0.0-alpha.beta",
            # ~ "1.0.0-beta",
            # ~ "1.0.0-beta.2",
            # ~ "1.0.0-beta.11",
            # ~ "1.0.0-rc.1",
            # ~ "1.0.0",
        # ~ ]
    # ~ )


# ~ def test_semantic_versions_of_semver():
    # ~ sorting_comparison(
        # ~ [
            # ~ "1.0.0-beta",
            # ~ "1.0.0",
            # ~ "2.0.0-rc.1",
            # ~ "2.0.0-rc.2",
            # ~ "2.0.0",
        # ~ ]
    # ~ )


# ~ def test_PEP440_versions_1():
    # ~ sorting_comparison(
        # ~ [
            # ~ "0.9",
            # ~ "1.0a1",
            # ~ "1.0a2",
            # ~ "1.0b1",
            # ~ "1.0rc1",
            # ~ "1.0",
            # ~ "1.1a1",
            # ~ "1!0.8",
        # ~ ]
    # ~ )
