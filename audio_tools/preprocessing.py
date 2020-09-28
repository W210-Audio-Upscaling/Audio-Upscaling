"""
Preprocessing Package for audio files
"""

import os, glob
from tqdm import tqdm
from ffmpy import FFmpeg


def normalize(original_file: str, target_location: str, bitrate: int):
    """
    Use FFmpeg to convert source audio into specified bitrate
    Args:
        original_file: Location of original audio source
        target_location: Location to save file
        bitrate: Bit rate
    """
    assert(
        target_location[-4:].lower() == ".mp3",
        "Target needs to be in .mp3 format"
    )
    ff = FFmpeg(
        inputs={original_file: None},
        outputs={target_location: '-ac 1 -ab %s'%(bitrate)}
    )
    ff.run()
    return


def bulk_normalize(
    original_files: list,
    target_location: str,
    bitrate: int,
    ignore_errors: bool = True
):
    """
    Bulk normalize files based on the normalize function
    Args:
        original_files: List of source files to normalize
        target_location: Location to save output files, reuses file name
        bitrate: Bit rate
        ignore_errors: Ignore files not suitable for normalization
    """
    for _file in tqdm(original_files):
        if ignore_errors:
            continue
        else:
            assert(
                _file[-4:].lower() == ".wav",
                f"This file is not a WAV file: {_file}"
            )
        target = os.path.join(target_location, _file[-4:])
        normalize(_file, target, bitrate)
    return
