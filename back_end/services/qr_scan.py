from pyzbar.pyzbar import decode
from PIL import Image


def read_qr_from_image(image_path):
    """
    Reads a QR code from an image file.
    Returns the decoded data as string.
    Returns None if no QR code is found.
    """

    try:
        img = Image.open(image_path)
    except Exception as e:
        raise Exception(f"Could not open image: {e}")

    decoded_objects = decode(img)

    if not decoded_objects:
        return None

    # Return first detected QR code data
    qr_data = decoded_objects[0].data.decode("utf-8")
    return qr_data
