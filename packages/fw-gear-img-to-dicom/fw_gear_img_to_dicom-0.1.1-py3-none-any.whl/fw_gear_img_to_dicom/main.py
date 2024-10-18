"""Main module."""

import logging
import shutil

from .convert_img_to_dcm import convert_image_to_dicom

log = logging.getLogger(__name__)


def run(image_path, output_dir, work_dir, session_id):
    """Perform the main task of the gear.

    Args:
        image_path (Path): Path to the image to convert.
        output_dir (Path): Path to the directory where to output
                           the resulting image.
        work_dir (Path): Path to the working directory.

    Returns:
        int: The return code for the gear.
    """
    log.info("This is the beginning of the run method in the main.py file")
    output_file = convert_image_to_dicom(image_path, work_dir, session_id)
    if output_file:
        log.info("Output file: %s", output_file)
        shutil.move(output_file, output_dir)
        return_code = 0
    else:
        log.error("No output file was created.")
        return_code = -1
    return return_code
