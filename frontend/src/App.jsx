import { useState, useRef } from "react";
import QRScanner from "./components/QRScanner";
import QRGalleryScanner from "./components/QRGalleryScanner";

function App() {

  const [mode, setMode] = useState(null);
  const [hashKey, setHashKey] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const isVerifying = useRef(false);

  const verifyHash = async (value) => {

    if (!value || isVerifying.current) return;

    isVerifying.current = true;

    setError("");
    setResult(null);
    setLoading(true);

    try {

      const response = await fetch(
        "http://xxx.xxx.x.x:8000/api/verify", 
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            hash_key: value
          })
        }
      );

      const data = await response.json();

      if (!data || !data.data || !data.data.serial) {
        setError("< fake >");
        return;
      }

      setResult(data);

    } catch (err) {
      setError("Server error. Please try again.");
    }

    finally {
      setLoading(false);
      isVerifying.current = false;
    }
  };

  const handleScan = (decodedText) => {
    setHashKey(decodedText);
    verifyHash(decodedText);
  };

  const resetApp = () => {
    setMode(null);
    setHashKey("");
    setResult(null);
    setError("");
  };

  return (
    <div className="app-container">

      <div className="card">

        <h2>Medicine Verification</h2>

        {!mode && (
          <div>

            <button onClick={() => setMode("scan")}>
              📷 Scan QR Code
            </button>

            <button onClick={() => setMode("manual")}>
              ⌨️ Enter Hash Manually
            </button>

            <QRGalleryScanner onScan={handleScan} />

          </div>
        )}

        {mode === "manual" && (
          <div>

            <input
              type="text"
              placeholder="Paste hash key"
              value={hashKey}
              onChange={(e) => setHashKey(e.target.value)}
            />

            <button onClick={() => verifyHash(hashKey)}>
              {loading ? "Verifying..." : "Verify"}
            </button>

            <button className="back-btn" onClick={resetApp}>
              Back
            </button>

          </div>
        )}

        {mode === "scan" && (
          <div>

            <QRScanner onScan={handleScan} />

            <button className="back-btn" onClick={resetApp}>
              Back
            </button>

          </div>
        )}

        {error && <p className="error-text">{error}</p>}

        {result && result.valid && (
          <div className="result-box">
            <p><strong>Serial:</strong> {result.data.serial}</p>
            <p><strong>Batch No:</strong> {result.data.batch_no}</p>
            <p><strong>Expiry Date:</strong> {result.data.date_expire}</p>
            <p><strong>Manufacturing Date:</strong> {result.data.date_manufacturing}</p>
            <p><strong>Colour:</strong> {result.data.colour}</p>
            <p><strong>Manufactured By:</strong> {result.data.manufactured_by}</p>
            <p><strong>License No:</strong> {result.data.manufacturing_license_no}</p>
          </div>
        )}

        {result && !result.data.serial && (
          <p className="error-text">❌ Invalid Medicine</p>
        )}

      </div>

    </div>
  );
}

export default App;