import os
import qrcode


def generate_qrs(records, output_folder="Technology_Driven_Detection_and_Prevention_of_Medicine_Adulteration\\managment_side\\generated_qrs"):
    os.makedirs(output_folder, exist_ok=True)

    total = len(records)

    for index, record in enumerate(records):
        serial = record["serial"]
        hash_value = record["hash"]

        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=6,
            border=4,
        )

        qr.add_data(hash_value)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(os.path.join(output_folder, f"{serial}.png"))

        yield index + 1, total  # for GUI progress updates
