import { useState } from "react";

const App = function () {
  const [error, setError] = useState("");
  const [value, setValue] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const randomPrompts = [
    "Who won the oscar on 1994",
    "Name the notes on do major scale",
    "singelton implementation in C++",
  ];

  const getRandPrompt = () => {
    const rand_val =
      randomPrompts[Math.floor(Math.random() * randomPrompts.length)];
    setValue(rand_val);
  };

  const clearAll = () => {
    setValue("")
    setError("")
    setChatHistory([])
  }
  const getResponse = async () => {
    if (!value) {
      setError("Please provide a non empty prompt");
      return;
    }
    try {
      const options = {
        method: "POST",
        body: JSON.stringify({
          history: chatHistory,
          message: value,
        }),
        headers: {
          "Content-Type": "application/json",
        },
      };
      const url = "http://localhost:8000/gemini";
      console.log(
        `Sending POST with options ${JSON.stringify(
          options,
          null,
          4
        )} to ${url} `
      );
      const response = await fetch(url, options);
      const data = await response.text();
      console.log(data);
      setChatHistory((oldChatHistory) => [
        ...oldChatHistory,
        {
          role: "user",
          parts: value,
        },
        {
          role: "model",
          parts: data,
        },
      ]);
      setValue("");
    } catch (error) {
      console.error(error);
      setError("Got Error " + error);
    }
  };
  return (
    <div className="GeminiChatbot">
      <section className="search-section">
        <p>
          What do you want to know?
          <button
            className="surprise-me"
            onClick={getRandPrompt}
            disabled={!chatHistory}
          >
            Surprise me
          </button>
        </p>
        <div className="input-container">
          <input
            value={value}
            placeholder="What is python programming language?"
            onChange={(e) => setValue(e.target.value)}
          />
          {!error && <button onClick={getResponse}> "Ask a question?" </button>}
          {error && <button onClick={clearAll}> "Clear" </button>}
        </div>
        {error && <p className="error-message"> {error} </p>}
        <div className="search-result">
          {chatHistory.map((item, idx) => (
            <div key={idx}>
              <p className="answer">
                {" "}
                {item.role} : {item.parts}
              </p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

export default App;
