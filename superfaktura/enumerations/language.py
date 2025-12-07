"""
Language Enumeration.

This module provides an enumeration of languages that can be used in the SuperFaktura API.

Classes:
    - Language: Enumeration of languages.

Usage:
    from superfaktura.enumerations.language import Language
    language = Language.CZECH
"""
from enum import Enum


class Language(str, Enum):
    """
    Language Enumeration.

    This enumeration represents the different languages that can be used in the SuperFaktura API.

    Values:
        - CZECH: Czech
        - GERMAN: German
        - ENGLISH: English
        - CROATIAN: Croatian
        - HUNGARIAN: Hungarian
        - ITALIAN: Italian
        - DUTCH: Dutch
        - POLISH: Polish
        - ROMANIAN: Romanian
        - RUSSIAN: Russian
        - SLOVAK: Slovak
        - SLOVENE: Slovene
        - SPANISH: Spanish
        - UKRAINIAN: Ukrainian

    Usage:
        language = Language.CZECH
    """

    CZECH = "cze"
    GERMAN = "deu"
    ENGLISH = "eng"
    CROATIAN = "hrv"
    HUNGARIAN = "hun"
    ITALIAN = "ita"
    DUTCH = "nld"
    POLISH = "pol"
    ROMANIAN = "rom"
    RUSSIAN = "rus"
    SLOVAK = "slo"
    SLOVENE = "slv"
    SPANISH = "spa"
    UKRAINIAN = "ukr"

    def __str__(self) -> str:
        """Return the string value of the language."""
        return self.value
