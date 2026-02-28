import jsQR from "jsqr";

function QRGalleryScanner({ onScan }) {

  const handleButtonClick = () => {
    document.getElementById("qr-file-input").click();
  };

  const handleImageUpload = (event) => {

    const file = event.target.files[0];
    if (!file) return;

    const img = new Image();
    img.src = URL.createObjectURL(file);

    img.onload = () => {

      const canvas = document.createElement("canvas");

      canvas.width = img.width;
      canvas.height = img.height;

      const ctx = canvas.getContext("2d");

      ctx.drawImage(img, 0, 0);

      const imageData = ctx.getImageData(
        0,
        0,
        canvas.width,
        canvas.height
      );

      const code = jsQR(
        imageData.data,
        imageData.width,
        imageData.height
      );

      if (code) {
        onScan(code.data);
      } else {
        alert("❌ No QR detected in image");
      }
    };
  };

  return (
    <div style={{ marginTop: "15px" }}>

      <input
        id="qr-file-input"
        type="file"
        accept="image/*"
        onChange={handleImageUpload}
        style={{ display: "none" }}
      />

      <button
        type="button"
        onClick={handleButtonClick}
      >
        🖼 Upload QR From Gallery
      </button>

    </div>
  );
}

export default QRGalleryScanner;