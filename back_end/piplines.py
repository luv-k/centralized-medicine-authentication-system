from services.qr_scan import read_qr_from_image
from services.db_lookup import lookup_product_by_hash

image_path = "Technology_Driven_Detection_and_Prevention_of_Medicine_Adulteration/managment_side/generated_qrs/c184e4cd-1061-4a56-83c4-666b83c535de.png"

data = read_qr_from_image(image_path)

if data:
    print("QR Code Data:", data)

    product = lookup_product_by_hash(data)

    if product:
        print("Product Found:")
        print(product)
    else:
        print("Not found")
else:
    print("No QR code found in the image.")
