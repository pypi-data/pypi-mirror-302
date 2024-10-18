"""
This module provides an interface to create Figma Styles via the Tokens Studio for Figma Plugin.
Tokens Studio for Figma Plugin allows the importing of Style Tokens from a JSON file. 
This module provides classes that represent Style Tokens, which can then be serialized 
into the JSON format required by Tokens Studio. 

The TokenDictionary class is instantiated with a dictionary of Token instances. 
It includes the export function that writes the JSON file, ready for import into the Tokens Studio Plugin.
"""

from dataclasses import dataclass
from typing import Literal, Mapping, Optional, Protocol, Any
import json, re

EXPORT_PATH = None  # The default path to where serialized TokenCollections are exported


def validate_hex_color(hex_code: str) -> None:
    """
    Validates whether the supplied hex code is a valid color hex code.
    It must start with '#' and can optionally contain an alpha channel (either 6 or 8 characters after '#').

    Args:
        hex_code (str): The hex code string to validate (e.g., #FFFFFF or #FFFFFFCC).

    Raises:
        ValueError: If the hex code is invalid, with a descriptive message.

    Returns:
        None: If the hex code is valid.
    """
    # Regular expression to check for valid hex code with optional alpha channel
    if not re.fullmatch(r"^#[0-9a-fA-F]{6}([0-9a-fA-F]{2})?$", hex_code):
        raise ValueError(
            f"Invalid hex code: {hex_code}. A valid hex code must start with '#' "
            "and contain exactly 6 hex digits for color and optionally 2 more for alpha."
        )


def convert_snake_to_camel(snake_str: str) -> str:
    """
    Converts a snake_case string to camelCase.

    Args:
        snake_str (str): The string in snake_case format.

    Returns:
        str: The string converted to camelCase.
    """
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


class _Token(Protocol):
    """
    A base class to represent a Token used in Tokens Studio for Figma.

    Tokens are data structures that represent design properties like typography, color, shadows, etc.
    Each token is serialized into a dictionary format required by Tokens Studio and can be
    exported as a JSON file for Figma integration.
    """

    def __prepare_dict__(self) -> dict[str, Any]:
        """
        Prepares the token data for serialization in the format required by Tokens Studio.

        Returns:
            dict[str, Any]: A dictionary representing the token in Tokens Studio format.
        """
        ...

    def __repr__(self) -> str:
        """
        Serializes the token as a JSON-formatted string.

        Returns:
            str: The JSON string of the token's data.
        """
        return json.dumps(self.__prepare_dict__(), indent=4)


@dataclass(repr=False)
class Typography(_Token):
    """
    A token representing typography settings for use in Tokens Studio.

    Attributes:
        font_family (str): The font family of the typography.
        font_weight (Literal): The weight of the font (e.g., Regular, Bold).
        font_size (float): The size of the font.
        line_height (Literal|float): The line height of the text, default is "auto".
        letter_spacing (float): Spacing between letters, default is 0.
        paragraph_spacing (float): Spacing between paragraphs, default is 0.
        paragraph_indent (float): Indentation for paragraphs, default is 0.
        text_case (Optional[Literal]): Text case (e.g., uppercase, lowercase), optional.
        text_decoration (Optional[Literal]): Text decoration (e.g., underline), optional.
        description (Optional[str]): Optional description of the typography token.
    """

    font_family: str
    font_weight: (
        Literal["Regular", "Display Regular", "Bold", "Medium", "SemiBold"] | str
    )
    font_size: float
    line_height: Literal["auto"] | float = "auto"
    letter_spacing: float = 0
    paragraph_spacing: float = 0
    paragraph_indent: float = 0
    text_case: Optional[
        Literal[
            "uppercase",
            "lowercase",
            "small_caps_forced",
            "capitalize",
            "small_caps",
        ]
    ] = None
    text_decoration: Optional[Literal["underline", "line-through"]] = None
    description: Optional[str] = None

    def __prepare_dict__(self) -> dict[str, Any]:
        """
        Prepares the typography token data for Tokens Studio.

        Returns:
            dict[str, Any]: The dictionary representation of the typography token,
            including its font properties and optional description.
        """
        value = {
            convert_snake_to_camel(k): str(v) if v is not None else "none"
            for k, v in self.__dict__.items()
            if k != "description"
        }

        mapping: dict[str, Any] = {
            "value": value,
            "type": "typography",
        }

        if self.description is not None:
            mapping.update({"description": self.description})
        return mapping


@dataclass(repr=False)
class Color(_Token):
    """
    A token representing color settings for use in Tokens Studio.

    Attributes:
        hex_code (str): The hexadecimal color code.
        description (Optional[str]): Optional description of the color token.
    """

    hex_code: str
    description: Optional[str] = None

    def __post_init__(self):
        validate_hex_color(self.hex_code)

    def __prepare_dict__(self) -> dict[str, Any]:
        """
        Prepares the color token data for Tokens Studio.

        Returns:
            dict[str, Any]: The dictionary representation of the color token,
            including the color's hexadecimal code and optional description.
        """
        mapping: dict[str, Any] = {
            "value": self.hex_code,
            "type": "color",
        }
        if self.description is not None:
            mapping.update({"description": self.description})
        return mapping


@dataclass(repr=False)
class DropShadow(_Token):
    """
    A token representing drop shadow settings for use in Tokens Studio.

    Attributes:
        color (str|color): The color of the drop shadow.
        x (int): The horizontal offset of the shadow.
        y (int): The vertical offset of the shadow.
        blur (int): The blur radius of the shadow.
        spread (int): The spread radius of the shadow.
    """

    color: str|Color
    x: int
    y: int
    blur: int
    spread: int

    def __post_init__(self):
        if isinstance(self.color, Color):
            self.color = self.color.hex_code
        validate_hex_color(self.color)

    def __prepare_dict__(self) -> dict[str, Any]:
        """
        Prepares the drop shadow token data for Tokens Studio.

        Returns:
            dict[str, Any]: The dictionary representation of the drop shadow token,
            including its color, offsets, blur, and spread.
        """
        self.__dict__.update({"type": "dropShadow"})
        return self.__dict__


class BoxShadow(_Token):
    """
    A token representing box shadow settings for use in Tokens Studio.

    Attributes:
        drop_shadows (Shadow): A collection of drop shadow tokens.
        description (Optional[str]): Optional description of the box shadow token.
    """

    def __init__(
        self, *drop_shadow: DropShadow, description: Optional[str] = None
    ) -> None:
        self.drop_shadows = drop_shadow
        self.description = description

    def __prepare_dict__(self) -> dict[str, Any]:
        """
        Prepares the box shadow token data for Tokens Studio.

        Returns:
            dict[str, Any]: The dictionary representation of the box shadow token,
            including its drop shadow settings and optional description.
        """
        mapping: dict[str, Any] = {
            "value": [x.__prepare_dict__() for x in self.drop_shadows],
            "type": "boxShadow",
        }
        if self.description is not None:
            mapping.update({"description": self.description})
        return mapping


STYLE_MAPPING = Mapping[str, "_Token|STYLE_MAPPING"]


def add_alpha(color: str | Color, opacity: int) -> str:
    """
    Given a hex code representing a solid color, generate an updated code reflecting the specified opacity.

    Args:
        color (str): The original 6-character hex code prefixed with '#' (e.g., #000000) or a Color instance
        opacity (int): The opacity value (0 to 100), where 0 is fully transparent and 100 is fully opaque.

    Returns:
        str: The 8-character hex code with the specified opacity.

    Example:
        add_alpha("#000000", 30) -> "#0000004d"
    """
    if not (0 <= opacity <= 100):
        raise ValueError("Opacity must be between 0 and 100")

    # Convert opacity percentage to a hex value (0 to 255 range)
    alpha = round(opacity * 255 / 100)

    # Format the alpha as a two-character hex string
    alpha_hex = f"{alpha:02x}"

    # Combine the original hex code with the alpha hex value
    hex_code = color if isinstance(color, str) else color.hex_code
    validate_hex_color(hex_code)
    return f"{hex_code}{alpha_hex}"


@dataclass(repr=False)
class TokenDict(_Token):
    """
    A class to manage a dictionary of style tokens for Tokens Studio.

    This class provides a way to organize style tokens and serialize them into
    a format ready for JSON export. It supports nested mappings of tokens and their
    properties.

    Attributes:
        style_mapping (STYLE_MAPPING): A dictionary mapping style names to token instances.
    """

    style_mapping: STYLE_MAPPING

    def __prepare_dict__(self) -> dict[str, Any]:
        """
        Prepares the style mapping data for serialization to Tokens Studio.

        Returns:
            dict[str, Any]: A dictionary representing the nested style mappings.
        """

        def iterate_styles(style_mapping: STYLE_MAPPING) -> dict[str, Any]:
            """
            Recursively iterates over the style mapping to convert all tokens to their serialized format.

            Args:
                style_mapping (STYLE_MAPPING): A dictionary mapping of style names to tokens.

            Returns:
                dict[str, Any]: A dictionary representing the nested style mappings in Tokens Studio format.
            """
            return {k: iterate_styles(v) if isinstance(v, dict) else v.__prepare_dict__() for k, v in style_mapping.items()}  # type: ignore

        return {"global": iterate_styles(self.style_mapping)}

    def export(self, file_path: Optional[str] = None, preview: bool = True):
        if file_path is None:
            from datetime import datetime

            file_path = (
                f"interface_exports/{datetime.now().strftime("%Y-%m-%d_%H%M%S")}.json"
            )

        with open(file_path, "w") as f:
            f.write(str(self))

        if preview:
            print(self)


def normalize_kebab(input: str) -> str:
    """
    Takes a string that can be in CamelCase, PascalCase, or snake_case and
    converts it to kebab-case, which (maybe) is the convention used in Figma styles.

    Args:
        input (str): The input string in CamelCase, PascalCase, or snake_case.

    Returns:
        str: The converted string in kebab-case.

    Examples:
        onSecondaryFixedVariant -> on-secondary-fixed-variant
        secondaryContainer -> secondary-container
        secondary_container -> secondary-container
        TokenCollection -> token-collection
    """

    snake_case = re.sub(r"(?<!^)(?=[A-Z])", "_", input).lower()

    kebab_case = snake_case.replace("_", "-")

    return kebab_case


PARSABLE_TOKENS = (Color, Typography, BoxShadow)


class _CollectionMeta(type):

    def __repr__(self) -> str:
        """
        Serializes the token as a JSON-formatted string.

        Returns:
            str: The JSON string of the token's data.
        """
        return json.dumps(self.__prepare_dict__(), indent=4)

    def __prepare_dict__(cls) -> dict[str, Any]:

        def iterate_styles(cls_body: type) -> dict[str, Any]:
            return {
                normalize_kebab(k): (
                    v.__prepare_dict__()
                    if isinstance(v, PARSABLE_TOKENS)
                    else iterate_styles(v)
                )
                for k, v in cls_body.__dict__.items()
                if not k.startswith("_") and isinstance(v, (type, *PARSABLE_TOKENS))
            }

        return {"global": iterate_styles(cls)}

    def export(self, file_path: str, preview: bool = True) -> None:
        """ if file_path is None:
            from datetime import datetime

            file_path = (
                f"{EXPORT_PATH}/{datetime.now().strftime("%Y-%m-%d-%H%M%S")}.json"
            ) """

        with open(file_path, "w") as f:
            f.write(str(self))

        if preview:
            print(self)


class TokenCollection(metaclass=_CollectionMeta):
    """
    A base class for organizing and creating design tokens in a hierarchical structure for use with the Tokens Studio for Figma plugin.

    The `TokenCollection` class allows you to define design tokens (such as colors, typography, shadows) as static variables within the class body. Each token instance will be automatically normalized and serialized into the JSON format required by Tokens Studio, making it easy to export and integrate with Figma.

    Features:
    - **Token Definition**: Define individual tokens within the class, which will automatically be normalized to kebab-case.
    - **Nested Structure**: You can create nested structures using inner classes, which mimics folder hierarchies in the design system.
    - **Automatic Serialization**: Tokens are automatically serialized into the format required by Tokens Studio, ready for export to a JSON file.
    - **Ignored Non-Token Variables**: Any class attributes that are not token instances will be ignored during the serialization process.

    If more control over token nesting or naming is needed, you can use the `TokenDict` constructor for a more granular approach to token creation and management.
    """

    ...
