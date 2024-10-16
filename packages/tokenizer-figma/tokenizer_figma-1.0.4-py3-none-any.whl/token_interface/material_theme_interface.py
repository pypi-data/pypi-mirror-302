"""
This module is designed to parse a JSON file exported from Google's [Material Theme Builder](https://m3.material.io/theme-builder#/custom). 
It defines a series of typed dictionaries that represent the structure of the Material Theme 
JSON file, including core colors, extended colors, color schemes, and palettes. 
The main function, `prase`, reads and parses the JSON file, returning the data as a 
`MaterialTheme` object for use in applications that support Material Design tokens.
"""

from typing import TypedDict, NotRequired
import json


class _CoreColors(TypedDict):
    """
    Represents the core colors defined in a Material Theme.

    Attributes:
        primary (str): The primary color.
        secondary (str): The secondary color.
        tertiary (Optional[str]): The tertiary color (optional).
        error (Optional[str]): The error color (optional).
        neutral (Optional[str]): The neutral color (optional).
        neutralVariant (Optional[str]): The neutral variant color (optional).
    """
    primary: str
    secondary: str
    tertiary: NotRequired[str]
    error: NotRequired[str]
    neutral: NotRequired[str]
    neutralVariant: NotRequired[str]


class _ExtendedColor(TypedDict):
    """
    Represents an extended color defined in the Material Theme.

    Attributes:
        name (str): The name of the extended color.
        color (str): The hexadecimal color code.
        description (str): A brief description of the color's usage or meaning.
        harmonized (bool): Whether the color is harmonized with the theme.
    """
    name: str
    color: str
    description: str
    harmonized: bool


class _Scheme(TypedDict):
    primary: str
    surfaceTint: str
    onPrimary: str
    primaryContainer: str
    onPrimaryContainer: str
    secondary: str
    onSecondary: str
    secondaryContainer: str
    onSecondaryContainer: str
    tertiary: str
    onTertiary: str
    tertiaryContainer: str
    onTertiaryContainer: str
    error: str
    onError: str
    errorContainer: str
    onErrorContainer: str
    background: str
    onBackground: str
    surface: str
    onSurface: str
    surfaceVariant: str
    onSurfaceVariant: str
    outline: str
    outlineVariant: str
    shadow: str
    scrim: str
    inverseSurface: str
    inverseOnSurface: str
    inversePrimary: str
    primaryFixed: str
    onPrimaryFixed: str
    primaryFixedDim: str
    onPrimaryFixedVariant: str
    secondaryFixed: str
    onSecondaryFixed: str
    secondaryFixedDim: str
    onSecondaryFixedVariant: str
    tertiaryFixed: str
    onTertiaryFixed: str
    tertiaryFixedDim: str
    onTertiaryFixedVariant: str
    surfaceDim: str
    surfaceBright: str
    surfaceContainerLowest: str
    surfaceContainerLow: str
    surfaceContainer: str
    surfaceContainerHigh: str
    surfaceContainerHighest: str


_Schemes = TypedDict(
    "_Schemes",
    {
        "light": _Scheme,
        "light-medium-contrast": _Scheme,
        "light-high-contrast": _Scheme,
        "dark": _Scheme,
        "dark-medium-contrast": _Scheme,
        "dark-high-contrast": _Scheme,
    },
)

_Palette = TypedDict(
    "_Palette",
    {
        "0": str,
        "5": str,
        "10": str,
        "15": str,
        "20": str,
        "25": str,
        "30": str,
        "35": str,
        "40": str,
        "50": str,
        "60": str,
        "70": str,
        "80": str,
        "90": str,
        "95": str,
        "98": str,
        "99": str,
        "100": str,
    },
)


class _Palettes(TypedDict):
    primary: _Palette
    secondary: _Palette
    tertiary: _Palette
    error: _Palette
    neutral: _Palette
    neutralVariant: _Palette


class MaterialTheme(TypedDict):
    """
    Represents the overall Material Theme, as defined by Google's Material Theme Builder.

    Attributes:
        description (str): A description of the theme.
        seed (str): The seed color used to generate the theme.
        coreColors (_CoreColors): Core color definitions of the theme.
        extendedColors (list[_ExtendedColor]): Extended color definitions in the theme.
        schemes (_Schemes): Color schemes for light and dark themes.
        palettes (_Palettes): Color palettes for each color type.
    """
    description: str
    seed: str
    coreColors: _CoreColors
    extendedColors: list[_ExtendedColor]
    schemes: _Schemes
    palettes: _Palettes


def parse(material_theme_json:str) -> MaterialTheme:
    """
    Imports and parses a JSON file exported from Google's Material Theme Builder.

    Args:
        material_theme_json (str): The path to the Material Theme JSON file.

    Returns:
        MaterialTheme: A dictionary structure representing the parsed Material Theme, 
        including core colors, extended colors, schemes, and palettes.
    """
    with open(material_theme_json, 'r') as f:
        return json.load(f)
    
