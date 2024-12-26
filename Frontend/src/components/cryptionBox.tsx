  import React, { useEffect, useState } from "react";

  interface CryptionProps {
    operation: string; // Add a parameter 'message'
  }

  const Cryption: React.FC<CryptionProps> = ({ operation }) => {
    type State = string[][]; 
    type Step = State[]; 
    const [text, settext] = useState<string>("");
    const [type, setType] = useState("String");
    const [key, setkey] = useState<string>("");
    const [errorMessage, setErrorMessage] = useState<string>("");
    const [responseMessage, setResponseMessage] = useState<string>("");
    const [steps, setSteps] = useState<Step[]>([]); // Array of steps// To store AES steps
    const regexPattern = /^[a-zA-Z0-9]*$/;

    useEffect(() => {
      if (!regexPattern.test(key)) {
        setErrorMessage("Key contains invalid characters.");
      } else {
        setErrorMessage(""); // Clear error message when valid
      }
      if (/^(.)\1{1,}$/.test(key)) setErrorMessage("This is a weak key");
      if (type === "String" && text.length !== 16) {
        setErrorMessage("Text must be 16 characters long");
      }
      if (type === "Hexadecimal" && text.length !== 32) {
        setErrorMessage("Text must be 32 characters long");
      }
      if (type === "Binary" && text.length !== 128) {
        setErrorMessage("Text must be 128 bits long");
      }
    }, [text, key]);

    const formatState = (state: (string)[][]): string => {
      return state
        .map(row =>
          row
            .map(val => (val !== null && val !== undefined ? String(val) : "")) // Leave empty values as they are
            .join(" ")
        )
        .join("\n");
    };
    
    
    const handleSubmit = async () => {
      if (errorMessage) return; // Prevent submission if validation fails
      try {
        let formText = text;
        if (type === "String") {
          formText = text
            .split("")
            .map((c) => c.charCodeAt(0).toString(16).padStart(2, "0"))
            .join("");
        }
        if (type === "Binary") {
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
              text: formText,
              key: key,
            }),
          }
        );
        if (!response.ok) {
          throw new Error(`Server responded with status: ${response.status}`);
        }
        const data = await response.json();
        setResponseMessage(data.ciphertext || "Operation successful!");
        setSteps(data.Steps); // Save Steps to state
      } catch (error) {
        setResponseMessage("An error occurred while processing the request.");
        console.error("Error:", error);
      }
    };

    return (
      <div className="my-36 flex items-center justify-center w-full min-h-[30vh] z-10 !w-screen">
        <div className="w-[70%] p-6 rounded-lg border border-green-600 backdrop-blur shadow-lg">
          <h1 className="text-center text-2xl font-bold text-green-400 mb-4">
            {operation}
          </h1>
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
            <button
              onClick={handleSubmit}
              className="p-2 bg-green-600 text-black font-bold rounded hover:bg-green-500 transition duration-300"
            >
              Submit
            </button>
          </div>
          {errorMessage && (
            <div className="mt-4 text-center text-red-400 font-semibold">
              {errorMessage}
            </div>
          )}
          {responseMessage && (
            <div className="mt-4 text-center text-green-400 font-semibold">
             Encryption Result =  {responseMessage}
            </div>
          )}
          {/* Table to Display Steps */}
          {steps.length > 0 && (
            <table className="w-full mt-6 border-collapse text-green-400 border border-green-600">
              <thead>
                <tr>
                  <th className="border border-green-600 px-4 py-2 text-green-400 ">Rounds</th>
                  {steps[0]?.map((_, i) => (
                    <th key={`header-${i}`} className="border border-green-600 px-4 py-2">
                      {operation === "Encryption" ? (
                        ["Round Start", "After SubBytes", "After ShiftRows", "After MixColumns", "Round Key"][i]
                          .split(" ")
                          .map((line, index) => (
                            <span key={`line-${index}`}>
                              {line}
                              <br />
                            </span>
                          ))
                      ) : (
                        `Round ${i + 1}`
                      )}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {steps.map((step, stepIndex) => (
                  <tr key={stepIndex}>
                    <td className="border border-green-600 text-green-400 px-4 py-2">Round {stepIndex}</td>
                    {step.map((state, stateIndex) => (
                      <td
                        key={`step-${stepIndex}-state-${stateIndex}`}
                        className="border text-center border-green-600 text-green-400 px-4 py-2 whitespace-pre-wrap"
                      >
                        {formatState(state)}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          )}

        </div>
      </div>
    );
  };

  export default Cryption;


