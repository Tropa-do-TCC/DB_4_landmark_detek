import sys

import gdcm


def decompress_dcm(file_path: str):
    reader = gdcm.ImageReader()
    reader.SetFileName(file_path)

    if not reader.Read():
        print("test")
        sys.exit(1)

    change = gdcm.ImageChangeTransferSyntax()
    change.SetTransferSyntax(gdcm.TransferSyntax(
        gdcm.TransferSyntax.ImplicitVRLittleEndian))
    change.SetInput(reader.GetImage())
    if not change.Change():
        sys.exit(1)

    writer = gdcm.ImageWriter()
    writer.SetFileName(file_path)
    writer.SetFile(reader.GetFile())
    writer.SetImage(change.GetOutput())

    if not writer.Write():
        sys.exit(1)
