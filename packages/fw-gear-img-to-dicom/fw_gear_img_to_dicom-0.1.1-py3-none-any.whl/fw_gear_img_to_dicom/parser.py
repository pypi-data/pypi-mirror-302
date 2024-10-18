"""Parser module to parse gear config.json."""

from pathlib import Path

from flywheel_gear_toolkit import GearToolkitContext


def parse_config(gear_context: GearToolkitContext) -> Path:
    """Parse config.json file for config options and inputs.

    Args:
        gear_context (GearToolkitContext): Context for the gear.

    Returns:
        path: Input File
    """

    image_path = Path(gear_context.get_input_path("image"))

    return image_path
