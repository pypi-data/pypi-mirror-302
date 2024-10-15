# Style Tokenizer for Figma

This Python package is designed to help generate and manage design tokens for Figma. It facilitates the creation of tokens using the Material Theme Builder and allows these tokens to be synced with Figma via the  free [Tokens Studio for Figma](https://tokens.studio/) plugin. The package provides utilities to parse exported Material Theme JSON files, organize and export design tokens, and work seamlessly with Figma.

## Features

- **Material Theme Parsing**: Easily parse and use color tokens from Google’s Material Theme Builder.
- **Design Token Management**: Create hierarchical structures of design tokens, such as colors, typography, and shadows, for use in Figma.
- **Token Export**: Automatically export tokens in the required JSON format to be imported into the Tokens Studio plugin.
- **Customizable Styles**: Define custom styles with automatic token normalization, including nested structures, to represent design systems in Figma.

## Installation

`pip install style-tokenizer-figma`

## Usage

### 1. Create Initial Tokens Using Material Theme Builder

1.1 Visit the Material Theme Builder and create a color palette.
1.2 (Optional) Select Color Match to ensure the palette stays true to input colors.
1.3 Download the Material Theme JSON export, which will be used to define colors and themes in your Figma design system.

### 2. Parse the Material Theme JSON

```python
from token_interface import *
THEME_JSON = 'material-theme-default.json'
theme = parse_material(THEME_JSON)
light_scheme = theme['schemes']['light']
print(light_scheme)
```

This allows you to work with typed dictionaries representing the color schemes, palettes, and other theme data.

### 3. Define and Export Tokens for Figma

You can use the TokenCollection class from the token_interface.py module to define and export tokens for use in Figma.

```python
from token_interface import TokenCollection, Color, Typography,DropShadow
DEFAULT_FONT = "Roboto"
class MyTokens(TokenCollection):
    black = Color("#000000")
    white = Color("#FFFFFF")
    # Example of creating shadows
    shadow_1 = DropShadow(black, 0, 4, 4, 0)
    shadow_2 = DropShadow(black, 0, 1, 3, 1)
    class Display:
        large = Typography(DEFAULT_FONT, "Regular", 57, 64, -0.25)
        medium = Typography(DEFAULT_FONT, "Regular", 45, 52)
        small = Typography(DEFAULT_FONT, "Regular", 36, 44)
    class Headline:
        large = Typography(DEFAULT_FONT, "Regular", 32, 40)
        medium = Typography(DEFAULT_FONT, "Regular", 28, 36)
        small = Typography(DEFAULT_FONT, "Regular", 24, 32)
# Export tokens to a JSON file
MyTokens.export('tokens_output.json')
```

### 4. Sync Tokens with Figma

After exporting your tokens to a JSON file, you can import them into your Figma project using the [Token Studio for Figma plugin](https://tokens.studio/plugin).

## Examples

### Simple Custom Tokens

```python
from token_interface import CoreStyles, TokenCollection, Color, Typography
class CustomStyles(TokenCollection):
    black = CoreStyles.black
    white = CoreStyles.white
    primary = Color("#FF5722")
    secondary = Color("#795548")
    class Display:
        large = Typography("Roboto", "Bold", 64, 72)
        medium = Typography("Roboto", "Regular", 45, 52)
# Export the defined styles
CustomStyles.export('custom_styles.json')
```

#### Output

```json
{
    "global": {
        "black": {
            "value": "#000000",
            "type": "color"
        },
        "white": {
            "value": "#FFFFFF",
            "type": "color"
        },
        "display": {
            "large": {
                "value": {
                    "fontFamily": "ROBOTO",
                    "fontWeight": "Regular",
                    "fontSize": "57",
                    "lineHeight": "64",
                    "letterSpacing": "-0.25",
                    "paragraphSpacing": "0",
                    "paragraphIndent": "0",
                    "textCase": "none",
                    "textDecoration": "none"
                },
                "type": "typography"
            },
            "medium": {
                "value": {
                    "fontFamily": "ROBOTO",
                    "fontWeight": "Regular",
                    "fontSize": "45",
                    "lineHeight": "52",
                    "letterSpacing": "0",
                    "paragraphSpacing": "0",
                    "paragraphIndent": "0",
                    "textCase": "none",
                    "textDecoration": "none"
                },
                "type": "typography"
            },
            "small": {
                "value": {
                    "fontFamily": "ROBOTO",
                    "fontWeight": "Regular",
                    "fontSize": "36",
                    "lineHeight": "44",
                    "letterSpacing": "0",
                    "paragraphSpacing": "0",
                    "paragraphIndent": "0",
                    "textCase": "none",
                    "textDecoration": "none"
                },
                "type": "typography"
            }
        },
        "headline": {
            "large": {
                "value": {
                    "fontFamily": "ROBOTO",
                    "fontWeight": "Regular",
                    "fontSize": "32",
                    "lineHeight": "40",
                    "letterSpacing": "0",
                    "paragraphSpacing": "0",
                    "paragraphIndent": "0",
                    "textCase": "none",
                    "textDecoration": "none"
                },
                "type": "typography"
            },
            "medium": {
                "value": {
                    "fontFamily": "ROBOTO",
                    "fontWeight": "Regular",
                    "fontSize": "28",
                    "lineHeight": "36",
                    "letterSpacing": "0",
                    "paragraphSpacing": "0",
                    "paragraphIndent": "0",
                    "textCase": "none",
                    "textDecoration": "none"
                },
                "type": "typography"
            },
            "small": {
                "value": {
                    "fontFamily": "ROBOTO",
                    "fontWeight": "Regular",
                    "fontSize": "24",
                    "lineHeight": "32",
                    "letterSpacing": "0",
                    "paragraphSpacing": "0",
                    "paragraphIndent": "0",
                    "textCase": "none",
                    "textDecoration": "none"
                },
                "type": "typography"
            }
        },
        "elevation-1": {
            "value": [
                {
                    "color": "#0000004c",
                    "x": 0,
                    "y": 1,
                    "blur": 2,
                    "spread": 0,
                    "type": "dropShadow"
                },
                {
                    "color": "#00000026",
                    "x": 0,
                    "y": 1,
                    "blur": 3,
                    "spread": 1,
                    "type": "dropShadow"
                }
            ],
            "type": "boxShadow"
        },
        "elevation-2": {
            "value": [
                {
                    "color": "#0000004c",
                    "x": 0,
                    "y": 1,
                    "blur": 2,
                    "spread": 0,
                    "type": "dropShadow"
                },
                {
                    "color": "#00000026",
                    "x": 0,
                    "y": 2,
                    "blur": 6,
                    "spread": 2,
                    "type": "dropShadow"
                }
            ],
            "type": "boxShadow"
        },
        "elevation-3": {
            "value": [
                {
                    "color": "#00000026",
                    "x": 0,
                    "y": 4,
                    "blur": 8,
                    "spread": 2,
                    "type": "dropShadow"
                },
                {
                    "color": "#0000004c",
                    "x": 0,
                    "y": 1,
                    "blur": 3,
                    "spread": 0,
                    "type": "dropShadow"
                }
            ],
            "type": "boxShadow"
        },
        "elevation-4": {
            "value": [
                {
                    "color": "#00000026",
                    "x": 0,
                    "y": 6,
                    "blur": 10,
                    "spread": 4,
                    "type": "dropShadow"
                },
                {
                    "color": "#0000004c",
                    "x": 0,
                    "y": 2,
                    "blur": 3,
                    "spread": 0,
                    "type": "dropShadow"
                }
            ],
            "type": "boxShadow"
        },
        "elevation-5": {
            "value": [
                {
                    "color": "#00000026",
                    "x": 0,
                    "y": 8,
                    "blur": 12,
                    "spread": 6,
                    "type": "dropShadow"
                },
                {
                    "color": "#0000004c",
                    "x": 0,
                    "y": 4,
                    "blur": 4,
                    "spread": 0,
                    "type": "dropShadow"
                }
            ],
            "type": "boxShadow"
        }
    }
}
```

### Defining Box Shadows/ Elevations

Five default elevation styles can be imported from CoreStyles. These represent the 5 elevation styles used by material 3.

```python
from token_interface import CoreStyles, TokenCollection
class CustomStyles(TokenCollection):
    elevation_1 = CoreStyles.elevation_1
    elevation_2 = CoreStyles.elevation_2
    elevation_3 = CoreStyles.elevation_3
    elevation_4 = CoreStyles.elevation_4
    elevation_5 = CoreStyles.elevation_5
```

You can define custom box shadows by initializing a BoxShadow Instance with a *DropShadow as follows:

```python
from token_interface import *
class CustomStyles(TokenCollection):
    black = CoreStyles.black
    white = CoreStyles.white
    primary = Color("#FF5722")
    secondary = Color("#795548")
    # Elevations
    drop_shadow_1 = DropShadow(add_alpha(black, 30), x = 0, y = 1, blur=3,spread=3) # black 30% opacity
    drop_shadow_2 = DropShadow(add_alpha(black, 15), x = 0, y = 1, blur=5,spread=5) # black 15% opacity
    elevation_1 = BoxShadow(drop_shadow_1, drop_shadow_1)
# Export the defined styles
CustomStyles.export('custom_styles.json')
```

### Importing an M3 theme

## Material Theme Json Schema

The M3_scheme.json schema is as follows:

```txt
description
seed
coreColors
    └── primary
extendedColors
schemes
    └── light
        ├── primary
        ├── surfaceTint
        ├── onPrimary
        ├── ...
    └── light-medium-contrast
        ├── primary
        ├── surfaceTint
        ├── ...
    └── light-high-contrast
        ├── primary
        ├── surfaceTint
        ├── ...
    └── dark
        ├── primary
        ├── surfaceTint
        ├── ...
    └── dark-medium-contrast
        ├── primary
        ├── surfaceTint
        ├── ...
    └── dark-high-contrast
        ├── primary
        ├── surfaceTint
        └── ...
palettes
    └── primary
        ├── 0
        ├── 5
        ├── ...
        └── 100
    └── secondary
        ├── 0
        ├── 5
        ├── ...
        └── 100
    └── tertiary
        ├── 0
        ├── 5
        ├── ...
        └── 100
    └── neutral
        ├── 0
        ├── 5
        ├── ...
        └── 100
    └── neutral-variant
        ├── 0
        ├── 5
        ├── ...
        └── 100
```

The `parse_material` function allows easy type hinted parsing of the material-theme.json file.

```python
import material_theme_interface as mt
THEME_JSON = 'material_themes/material-theme.json'
theme = mt.parse(THEME_JSON)
light_scheme = theme['schemes']['light']
```

In this example, we import the light color scheme from an m3 Json export:

```python
from token_interface import *
MATERIAL = parse_material("path-to-material.json") # path to your material export json
LIGHT_THEME = MATERIAL["schemes"]["light"]
DEFAULT_FONT = "Roboto"
class M3Styles(TokenCollection):
    black = Color("#000000")
    white = Color("#FFFFFF")
    primary = Color(LIGHT_THEME["primary"])
    surfaceTint = Color(LIGHT_THEME["surfaceTint"])
    onPrimary = Color(LIGHT_THEME["onPrimary"])
    primaryContainer = Color(LIGHT_THEME["primaryContainer"])
    onPrimaryContainer = Color(LIGHT_THEME["onPrimaryContainer"])
    secondary = Color(LIGHT_THEME["secondary"])
    onSecondary = Color(LIGHT_THEME["onSecondary"])
    secondaryContainer = Color(LIGHT_THEME["secondaryContainer"])
    onSecondaryContainer = Color(LIGHT_THEME["onSecondaryContainer"])
    tertiary = Color(LIGHT_THEME["tertiary"])
    onTertiary = Color(LIGHT_THEME["onTertiary"])
    tertiaryContainer = Color(LIGHT_THEME["tertiaryContainer"])
    onTertiaryContainer = Color(LIGHT_THEME["onTertiaryContainer"])
    error = Color(LIGHT_THEME["error"])
    onError = Color(LIGHT_THEME["onError"])
    errorContainer = Color(LIGHT_THEME["errorContainer"])
    onErrorContainer = Color(LIGHT_THEME["onErrorContainer"])
    background = Color(LIGHT_THEME["background"])
    onBackground = Color(LIGHT_THEME["onBackground"])
    surface = Color(LIGHT_THEME["surface"])
    onSurface = Color(LIGHT_THEME["onSurface"])
    surfaceVariant = Color(LIGHT_THEME["surfaceVariant"])
    onSurfaceVariant = Color(LIGHT_THEME["onSurfaceVariant"])
    outline = Color(LIGHT_THEME["outline"])
    outlineVariant = Color(LIGHT_THEME["outlineVariant"])
    shadow = Color(LIGHT_THEME["shadow"])
    scrim = Color(LIGHT_THEME["scrim"])
    inverseSurface = Color(LIGHT_THEME["inverseSurface"])
    inverseOnSurface = Color(LIGHT_THEME["inverseOnSurface"])
    inversePrimary = Color(LIGHT_THEME["inversePrimary"])
    primaryFixed = Color(LIGHT_THEME["primaryFixed"])
    onPrimaryFixed = Color(LIGHT_THEME["onPrimaryFixed"])
    primaryFixedDim = Color(LIGHT_THEME["primaryFixedDim"])
    onPrimaryFixedVariant = Color(LIGHT_THEME["onPrimaryFixedVariant"])
    secondaryFixed = Color(LIGHT_THEME["secondaryFixed"])
    onSecondaryFixed = Color(LIGHT_THEME["onSecondaryFixed"])
    secondaryFixedDim = Color(LIGHT_THEME["secondaryFixedDim"])
    onSecondaryFixedVariant = Color(LIGHT_THEME["onSecondaryFixedVariant"])
    tertiaryFixed = Color(LIGHT_THEME["tertiaryFixed"])
    onTertiaryFixed = Color(LIGHT_THEME["onTertiaryFixed"])
    tertiaryFixedDim = Color(LIGHT_THEME["tertiaryFixedDim"])
    onTertiaryFixedVariant = Color(LIGHT_THEME["onTertiaryFixedVariant"])
    surfaceDim = Color(LIGHT_THEME["surfaceDim"])
    surfaceBright = Color(LIGHT_THEME["surfaceBright"])
    surfaceContainerLowest = Color(LIGHT_THEME["surfaceContainerLowest"])
    surfaceContainerLow = Color(LIGHT_THEME["surfaceContainerLow"])
    surfaceContainer = Color(LIGHT_THEME["surfaceContainer"])
    surfaceContainerHigh = Color(LIGHT_THEME["surfaceContainerHigh"])
    surfaceContainerHighest = Color(LIGHT_THEME["surfaceContainerHighest"])
    class Display:
        large = Typography(DEFAULT_FONT, "Regular", 57, 64, -0.25)
        medium = Typography(DEFAULT_FONT, "Regular", 45, 52)
        small = Typography(DEFAULT_FONT, "Regular", 36, 44)
    class Headline:
        large = Typography(DEFAULT_FONT, "Regular", 32, 40)
        medium = Typography(DEFAULT_FONT, "Regular", 28, 36)
        small = Typography(DEFAULT_FONT, "Regular", 24, 32)
    class Title:
        large = Typography(DEFAULT_FONT, "Regular", 22, 28)
        medium = Typography(DEFAULT_FONT, "Medium", 16, 24)
        small = Typography(DEFAULT_FONT, "Medium", 14, 20, 0.1)
    class Label:
        large = Typography(DEFAULT_FONT, "Medium", 14, 20, 0.1)
        medium_prominent = Typography(DEFAULT_FONT, "SemiBold", 12, 16, 0.5)
        medium = Typography(DEFAULT_FONT, "Medium", 12, 16, 0.5)
        small = Typography(DEFAULT_FONT, "Medium", 11, 16, 0.5)
    class Body:
        large = Typography(DEFAULT_FONT, "Regular", 16, 24, 0.5)
        medium = Typography(DEFAULT_FONT, "Regular", 14, 20, 0.25)
        small = Typography(DEFAULT_FONT, "Regular", 12, 16)
    # Elevations
    elevation_1 = CoreStyles.elevation_1
    elevation_2 = CoreStyles.elevation_2
    elevation_3 = CoreStyles.elevation_3
    elevation_4 = CoreStyles.elevation_4
    elevation_5 = CoreStyles.elevation_5
if __name__ == "__main__":
    M3Styles.export('style_tokens.json')
```
