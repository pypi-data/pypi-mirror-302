import logging
import os
import time
from datetime import datetime
from pathlib import Path

import numpy as np
from fw_file.dicom.utils import generate_uid
from flywheel_gear_toolkit.utils.zip_tools import zip_output
from PIL import Image
from pydicom._storage_sopclass_uids import SecondaryCaptureImageStorage
from pydicom.dataset import Dataset
from pydicom.sequence import Sequence

from flywheel_gear_toolkit.utils.file import sanitize_filename

log = logging.getLogger(__name__)


def convert_array_to_dcm_slice(
    slice_number,
    pixel_data,
    BitsAllocated,
    StudyInstanceUID,
    SeriesInstanceUID,
    PixelSpacing,
    SeriesDescription,
    output_dir,
):
    """
    Creates a OHIF-Compliant DICOM file from a two-dimensional array.

    BitsAllocated must match the datatype of the pixel_data. The pixel_data can only be
    uint8 or uint16 to be viewed by the OHIF Viewer.

    Args:
        slice_number (integer): Index of the 3D array pixel_data is selected from
        pixel_data (numpy.Array): Array of values representing pixels
        BitsAllocated (integer): Bits allocted for each pixel
        StudyInstanceUID (string): UID of this study
        SeriesInstanceUID (string): UID of this series
        PixelSpacing (list): A list of two floats denoting pixel spacing
        SeriesDescription (string): The series description
        output_dir (string): The directory to output each dicom
    """
    dcm_filename = f"{output_dir}/{slice_number+1}.dcm"
    SOPInstanceUID = generate_uid()

    # Main data elements
    ds = Dataset()
    ContentDate = datetime.today().strftime("%Y%m%d")
    ContentTime = datetime.today().strftime("%H%M%S")

    # Patient Module
    ds.PatientName = SeriesDescription
    ds.PatientID = SeriesDescription
    ds.PatientBirthDate = ""
    ds.PatientSex = "U"

    # General Study Module
    ds.StudyInstanceUID = StudyInstanceUID
    ds.StudyID = None
    ds.StudyDate = ContentDate
    ds.StudyTime = ContentTime
    ds.ReferringPhysicianName = None
    ds.AccessionNumber = None

    # General Series Module
    ds.Modality = "SC"  # Secondary Capture
    ds.SeriesInstanceUID = SeriesInstanceUID
    ds.SeriesDescription = SeriesDescription
    ds.SeriesNumber = None

    # General Equipment Module
    ds.ConversionType = "DF"  # Digitized Film

    # General Acquisition Module

    # Image Pixel Module
    ds.ImageType = ["DERIVED", "SECONDARY", "OTHER"]
    ds.InstanceNumber = str(slice_number + 1)
    ds.NumberOfFrames = 1
    ds.Rows, ds.Columns = pixel_data.shape[:2]

    if len(pixel_data.shape) < 3 or pixel_data.shape[2] == 1:
        ds.SamplesPerPixel = 1
        ds.PhotometricInterpretation = "MONOCHROME2"
    elif pixel_data.shape[2] == 3:
        ds.SamplesPerPixel = 3
        ds.PhotometricInterpretation = "RGB"

    ds.BitsAllocated = BitsAllocated
    ds.BitsStored = BitsAllocated
    ds.HighBit = BitsAllocated - 1
    ds.PixelRepresentation = 0  # unsigned integer
    ds.PlanarConfiguration = 0  # The sample values for the first pixel are
    # followed by the sample values for the second pixel, etc. Important for RGB.

    ds.SOPClassUID = SecondaryCaptureImageStorage
    ds.SOPInstanceUID = SOPInstanceUID

    ds.PixelSpacing = PixelSpacing

    ds.LossyImageCompression = "01"  # Image has been subjected to lossy compression
    ds.RepresentativeFrameNumber = 1

    ds.PixelData = pixel_data.tobytes()

    ds.is_implicit_VR = True
    # ds["PixelData"].VR = "OB"
    ds.is_little_endian = True

    # Flywheel-Specific DICOM Tags:
    # Check Marks (✓) indicate these tags were addressed above
    # Down Arrows (↓) indicate these tags are addressed below

    # OHIF Viewer Requirements
    # https://docs.flywheel.io/User_Guides/user_minimum_required_dicom_tags_for_functionality/#the-ohif-viewer
    """
        (0020,000E) UI SeriesInstanceUID ✓
        (0020,000D) UI StudyInstanceUID ✓
        (0008,0060) CS Modality ✓
        (0020,0011) IS SeriesNumber ↓
        (0040,0009) SH ScheduledProcedureStepID ↓
        (0040,1001) SH RequestedProcedureID ↓
        (0008,0020) DA StudyDate ✓
        (0008,0030) TM StudyTime ✓
        (0008,0010) SH StudyID ✓
        (0020,0011) IS SeriesNumber ↓
        (0010,0020) LO PatientID ✓
        (0028,0010) US Rows ✓
        (0028,0011) US Columns ✓
        (0028,0002) US SamplesPerPixel ✓
        (0008,0018) UI SOPInstanceUID ✓
        
        Other DICOM Tags included beyond OHIF Viewer Requirements:
        (0008,0201) SH Timezone Offset from UTC ↓
        (0008,103E) LO Series Description ✓
        (0008,1190) UI RetrieveURL ↓

        (0020,1209) IS NumberOfSeriesRelatedInstances ↓
        (0040,0244) DA PerformedProcedureStepStartDate ↓
        (0040,0245) TM PerformedProcedureStepStartTime ↓
        (0040,0275) SQ RequestAttributesSequence ↓

    """
    ds.TimezoneOffsetFromUTC = time.strftime("%z")  # e.g. "-0600"

    ds.SeriesNumber = "1"
    ds.NumberOfSeriesRelatedInstances = "1"
    ds.PerformedProcedureStepStartDate = ContentDate
    ds.PerformedProcedureStepStartTime = ContentTime
    ds.RequestAttributesSequence = Sequence()
    ds.ScheduledProcedureStepID = "1"
    ds.RequestedProcedureID = "1"

    # DICOM MR Classifier Requirements
    """
        (0008,0060) CS Modality ✓
        (0008,103E)	LO SeriesDescription ✓
        (0020,000D)	UI StudyInstanceUID ✓
        (0020,0010)	SH StudyID ✓
        (7FE0,0010) OB or OW Pixel Data ✓
        (0008,0070)	LO Manufacturer ↓
    """
    ds.Manufacturer = "Flywheel"

    # Save single DICOM file
    ds.save_as(dcm_filename, write_like_original=False)


def convert_image_to_dicom(input_filename, work_dir, session_id):
    """
    Convert provided image to dicom archive.

    Args:
        input_filename (Pathlike): Path to input file.
        work_dir (Pathlike): The working directory to save DICOM slices in

    Returns:
        Pathlike: Path to archive of dicom slices produced
    """
    try:
        # Prepare named output directory under the working directory
        input_filepath = Path(input_filename)
        output_dir = Path(work_dir) / sanitize_filename(input_filepath.stem)
        os.makedirs(output_dir, exist_ok=True)

        # Load the image file into a numpy array
        image_ptr = Image.open(input_filepath)

        # See PIL.Image modes:
        # https://pillow.readthedocs.io/en/stable/handbook/concepts.html#modes
        # Convert to "RGB" if not already there.
        if image_ptr.mode in ["RGBA", "CMYK", "LAB", "YCbCr", "HSV"]:
            image_ptr = image_ptr.convert(mode="RGB")

        image_array = np.array(image_ptr)
        # modes L, P, RGB, RGBA, CMYK, YCbCr, LAB, and HSV are all 8-bit
        # May need work to accomodate other image types.
        BitsAllocated = 8

        # Collate DICOM tags that will be shared across slices.
        StudyInstanceUID = generate_uid(entropy_srcs=[session_id])
        # uid_prefix = StudyInstanceUID[
        #     : StudyInstanceUID.replace(".", ":", 7).find(".") + 1
        # ]
        SeriesInstanceUID = generate_uid()

        PixelSpacing = [1, 1]
        SeriesDescription = output_dir.name
        convert_array_to_dcm_slice(
            0,
            image_array,
            BitsAllocated,
            StudyInstanceUID,
            SeriesInstanceUID,
            PixelSpacing,
            SeriesDescription,
            output_dir,
        )

        output_filename = str(output_dir) + ".dicom.zip"
        cwd = os.getcwd()
        os.chdir(work_dir)
        zip_output(work_dir, output_dir, output_filename)
        os.chdir(cwd)

    except Exception as e:
        log.error("Error converting image to dicom.")
        log.exception(e)
        output_filename = None

    return output_filename
