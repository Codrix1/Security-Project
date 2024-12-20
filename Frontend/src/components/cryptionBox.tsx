import React, { useEffect, useState } from "react";
interface CryptionProps {
  operation: string; // Add a parameter 'message'
}
const Cryption: React.FC<CryptionProps> = ({ operation }) => {
  // States for input fields
  const [text, settext] = useState<string>("");
  const [type, setType] = useState("String");
  const [key, setkey] = useState<string>("");
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [responseMessage, setResponseMessage] = useState<string>("");
  // Regex pattern for validation (example: allows only alphanumeric strings)
  const regexPattern = /^[a-zA-Z0-9]*$/;
  // useEffect to validate fields whenever inputs change
  useEffect(() => {
    if (!regexPattern.test(key)) {
      setErrorMessage("Key contains invalid characters.");
    } else {
      setErrorMessage(""); // Clear error message when valid
    }
    if (/^(.)\1{1,}$/.test(key)) setErrorMessage("This is a weak key");
    if (type == "String") {
      if (text.length != 16) {
        setErrorMessage("Text must be 16 characters long");
      }
    }
    if (type == "Hexadecimal") {
      if (text.length != 32) {
        setErrorMessage("Text must be 32 characters long");
      }
    }
    if (type == "Binary") {
      if (text.length != 128) {
        setErrorMessage("Text must be 128 bits long");
      }
    }
  }, [text, key]);
  // Function to send POST request to the server
  const handleSubmit = async () => {
    if (errorMessage) return; // Prevent submission if validation fails
    try {
      let formText = text;
      if (type == "String") {
        formText = text.split("")
          .map((c) => c.charCodeAt(0).toString(16).padStart(2, "0"))
          .join("");
      }
      if (type == "Binary") {
        formText = parseInt(text, 2).toString(16);
      }
      const response = await fetch(
        `http://localhost:5000/submit/${operation}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            operation: operation,
            text: formText,
            key: key,
          }),
        },
      );
      if (!response.ok) {
        throw new Error(`Server responded with status: ${response.status}`);
      }
      const data = await response.json();
      setResponseMessage(data.message || "Operation successful!");
      console.log("Server response:", data);
    } catch (error) {
      setResponseMessage("An error occurred while processing the request.");
      console.error("Error:", error);
    }
  };
  return (
    <div className="my-36 flex items-center justify-center w-full min-h-[30vh] z-10 !w-screen ">
      {/* Form Container */}
      <div className="w-[70%] p-6 rounded-lg border border-green-600 backdrop-blur shadow-lg">
        <h1 className="text-center text-2xl font-bold text-green-400 mb-4">
          {operation}
        </h1>
        {/* Input Fields */}
        <div className="flex flex-col gap-4">
          <input
            type="text"
            placeholder="Text"
            value={text}
            onChange={(e) => settext(e.target.value)}
            className="p-2 bg-transparent border border-green-600 text-green-400 placeholder-green-500 rounded focus:outline-none focus:ring-2 focus:ring-green-500"
          />
          <input
            type="text"
            placeholder="Key"
            value={key}
            maxLength={32}
            minLength={32}
            onChange={(e) => setkey(e.target.value)}
            className="p-2 bg-transparent border border-green-600 text-green-400 placeholder-green-500 rounded focus:outline-none focus:ring-2 focus:ring-green-500"
          />
          <label className="p-2 bg-transparent border border-green-600 text-green-400 placeholder-green-500 rounded focus:outline-none focus:ring-2 focus:ring-green-500">
            Text Type:
            <select
              name="text-type"
              className="mx-2"
              onChange={(e) => {
                setType(e.target.value);
              }}
            >
              <option>String</option>
              <option>Hexadecimal</option>
              <option>Binary</option>
            </select>
          </label>
          {/* Submit Button */}
          <button
            onClick={handleSubmit}
            className="p-2 bg-green-600 text-black font-bold rounded hover:bg-green-500 transition duration-300"
          >
            Submit
          </button>
        </div>
        {/* Error Message */}
        {errorMessage && (
          <div className="mt-4 text-center text-red-400 font-semibold">
            {errorMessage}
          </div>
        )}
        {/* Response Message */}
        {responseMessage && (
          <div className="mt-4 text-center text-green-400 font-semibold">
            {responseMessage}
          </div>
        )}
      </div>
    </div>
  );
};
export default Cryption;
