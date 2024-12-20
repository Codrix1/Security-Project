import React, { useEffect, useState } from "react";
interface CryptionProps {
  operation: string; // Add a parameter 'message'
}
const Cryption: React.FC<CryptionProps> = ({ operation }) => {
  // States for input fields
  const [text, settext] = useState<string>("");
  const [key, setkey] = useState<string>("");
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [responseMessage, setResponseMessage] = useState<string>("");
  // Regex pattern for validation (example: allows only alphanumeric strings)
  const regexPattern = /^[a-zA-Z0-9]*$/;
  // useEffect to validate fields whenever inputs change
  useEffect(() => {
    if (!regexPattern.test(text)) {
      setErrorMessage("Text contains invalid characters.");
    } else if (!regexPattern.test(key)) {
      setErrorMessage("Key contains invalid characters.");
    } else {
      setErrorMessage(""); // Clear error message when valid
    }
  }, [text, key]);
  // Function to send POST request to the server
  const handleSubmit = async () => {
    if (errorMessage) return; // Prevent submission if validation fails
    try {
      const response = await fetch(`https://example.com/api/${operation}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          operation: operation,
          text: text,
          key: key,
        }),
      });
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
            onChange={(e) => setkey(e.target.value)}
            className="p-2 bg-transparent border border-green-600 text-green-400 placeholder-green-500 rounded focus:outline-none focus:ring-2 focus:ring-green-500"
          />
          <label
            className="p-2 bg-transparent border border-green-600 text-green-400 placeholder-green-500 rounded focus:outline-none focus:ring-2 focus:ring-green-500"
          >
            Text Type:
            <select
              name="text-type"
              className="mx-2"
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
