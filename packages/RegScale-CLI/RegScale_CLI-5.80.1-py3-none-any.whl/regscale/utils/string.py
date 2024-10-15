"""Define commonly used methods for strings."""

import re
from typing import Optional

ANSI_ESCAPE_REGEX = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def remove_ansi_escape_sequences(text: str) -> str:
    """Remove all ANSI escape sequences from a text

    :param str text: a string to remove ANSI escape sequences from
    :return: a string with no ANSI escape sequences
    :rtype: str
    """
    return ANSI_ESCAPE_REGEX.sub("", text)


def replace_unknown_spaces_and_newlines(input_string: str) -> str:
    """Replace unknown spaces and newlines with a single space

    :param str input_string: a string to replace unknown spaces and newlines with a single space
    :return: a string with unknown spaces and newlines replaced with a single space
    :rtype: str
    """
    return re.sub(r"\s+", " ", input_string)


def extract_double_curly_braces_contents(query_string: str) -> list[str]:
    """Extract the contents of double curly braces from a string

    :param str query_string: a string to extract the contents of double curly braces from
    :return: a list of strings that were contained within double curly braces
    :rtype: list[str]
    """
    pattern = r"{{(.*?)}}"
    return re.findall(pattern, query_string)


def extract_dag_run_conf_key(query_string: str) -> Optional[str]:
    """
    Extract the key from a dag_run.conf key-value pair

    :param str query_string: a string to extract the key from a dag_run.conf key-value pair
    :return: the key from a dag_run.conf key-value pair
    :rtype: Optional[str]
    """
    pattern = r"dag_run\.conf\[['\"]([^'\"]+)['\"]\]"
    match = re.search(pattern, query_string)
    return match[1] if match else None


def extract_param(query_string: str) -> Optional[list]:
    """
    Extract the parameter from a params key-value pair

    :param str query_string: a string to extract the parameter from a params key-value pair
    :return: the parameter from a params key-value pair
    :rtype: Optional[list]
    """
    pattern = r"\bparams\.(\w+)\s.*"
    matches = re.findall(pattern, query_string)
    return matches[0] if matches else None


def levenshtein_distance(first_string: str, second_string: str) -> int:
    """
    Calculate the Levenshtein distance between two strings

    :param str first_string: the first string to compare
    :param str second_string: the second string to compare
    :return: the Levenshtein distance between two strings
    :rtype: int
    """
    if len(first_string) < len(second_string):
        return levenshtein_distance(second_string, first_string)

    if len(second_string) == 0:
        return len(first_string)

    previous_row = range(len(second_string) + 1)
    for i, c1 in enumerate(first_string):
        current_row = [i + 1]
        for j, c2 in enumerate(second_string):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]
