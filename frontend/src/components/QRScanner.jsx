import { useEffect } from "react";
import { Html5Qrcode } from "html5-qrcode";

function QRScanner({ onScan }) {

  useEffect(() => {

    const scanner = new Html5Qrcode("reader");

    const startScanner = async () => {

      try {

        await scanner.start(
          { facingMode: "environment" },
          {
            fps: 10,
            qrbox: 250
          },
          (decodedText) => {
            onScan(decodedText);

            scanner.stop().catch(() => {});
          },
          () => {}
        );

      } catch (err) {
        console.log("Camera start error:", err.message);
      }
    };

    startScanner();

    return () => {
      if (scanner.isScanning) {
        scanner.stop().catch(() => {});
      }
    };

  }, [onScan]);

  return <div id="reader"></div>;
}

export default QRScanner;