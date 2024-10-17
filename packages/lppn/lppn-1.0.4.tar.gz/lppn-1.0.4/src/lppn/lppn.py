#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import re


def get(major: int, minor: int) -> int:
    """
    Returns the latest Python patch number of a given major and minor version.

    :param major: Python major version
    :param minor: Python minor version
    :return: An integer containing the latest Python patch number
    """

    # Check if able to cast into int
    int(major)
    int(minor)

    # Check if float
    if not (float(major).is_integer() and float(minor).is_integer()):
        raise ValueError("Input must be integer")

    # Cast into int
    major = int(major)
    minor = int(minor)

    # Check if negative
    if major < 0 or minor < 0:
        raise ValueError("Input must be positive")

    # Python download URL
    url = "https://www.python.org/ftp/python/"

    # Get python download page
    s = requests.Session()
    r = s.get(url)
    if r.status_code != 200:
        raise ConnectionError(f"'{url}' status code: {r.status_code}")
    page_content = str(r.content)
    r.close()

    # Create pattern of what we want in the page
    patch_pattern_string = (
        f'(<a href="{major}\\.{minor}\\.\\d+/">{major}\\.{minor}\\.)'
        "(\\d+)"
        "(/</a>)"
    )
    patch_pattern = re.compile(patch_pattern_string)

    # Parse the page for a patch and add it to a list
    patches = []
    results = re.findall(patch_pattern, page_content)
    for result_tuple in results:
        re_group_1, re_group_2, re_group_3 = result_tuple
        patch = int(re_group_2)
        patches.append(patch)
    if patches == []:
        raise RuntimeError(
            f"Could not find a suitable version for '{major}.{minor}'"
        )

    # Get the latest patch
    latest_patch = max(patches)

    return latest_patch
