import React, { useState, useEffect, useRef } from "react";

export default function Chat() {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hi! What supplement questions can I assist you with today?" }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  
  const msgEndRef = useRef(null);

  useEffect(() => {
    msgEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = input;
    setMessages(prev => [...prev, { sender: "user", text: userMessage }]);
    setInput("");
    setLoading(true);

    setMessages(prev => [...prev, { role: "assistant", text: "" }]);


    try {
  const response = await fetch("http://localhost:8181/run_query", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt: userMessage }),  
  });

  if (!response.body) {
    console.error("No response body");
    return;
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder("utf-8");
  let assistantMsg = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value, { stream: false });
    // const cleanChunk = chunk.replace(/\s+/g, "");

    // const formatted = cleanChunk
    //     .replace(/\s+([.,!?;:])/g, "$1")   // fix spaces before punctuation
    //     .replace(/\s{2,}/g, " ");           // collapse multiple spaces
        
    assistantMsg += chunk;


    // Update last assistant message
    setMessages(prev => {
      const updated = [...prev];
      updated[updated.length - 1].text = assistantMsg;
      return updated;
    });
  }
} catch (err) {
  console.error(err);
  setMessages(prev => [
    ...prev,
    { role: "assistant", text: "Error: Could not get a response." }
  ]);
}

    setLoading(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") sendMessage();
  };

  return (
    <div style={styles.container}>
      <div style={{
            height: "60px",
            backgroundColor: "#000",
            color: "white",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: "20px",
            fontWeight: "bold",
            boxShadow: "0 2px 4px rgba(0,0,0,0.2)"
        }}>
            SupplementsRxAI
      </div>
      <div style={styles.chatBox}>
        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              ...styles.message,
              alignSelf: msg.sender === "user" ? "flex-end" : "flex-start",
              background: msg.sender === "user" ? "#000000" : "#e8e8e8",
              color: msg.sender === "user" ? "white" : "black"
            }}
          >
            {msg.text}
          </div>
        ))}

        {loading && (
          <div style={{ ...styles.message, background: "#e8e8e8" }}>
            Thinking...
          </div>
        )}

        <div ref={msgEndRef} />
      </div>

      <div style={styles.inputBar}>
        <input
          style={styles.input}
          placeholder="..."
          value={input}
          onKeyDown={handleKeyDown}
          onChange={(e) => setInput(e.target.value)}
        />
        <button class="send_button" style={styles.button} onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}


const styles = {
  container: {
    height: "100vh",
    width: "100vw",          
    display: "flex",
    flexDirection: "column",
    background: "#b49d7cff"
  },
  chatBox: {
    flex: 1,
    overflowY: "auto",
    padding: "20px",
    display: "flex",
    flexDirection: "column",
    gap: "12px"
  },
  message: {
    maxWidth: "70%",
    padding: "12px 16px",
    borderRadius: "12px",
    fontSize: "14px",
    lineHeight: "1.5",
    boxShadow: "0 2px 4px rgba(0,0,0,0.1)"
  },
  inputBar: {
    display: "flex",
    padding: "15px",
    background: "#0000",
  },
  input: {
    flex: 1,
    padding: "12px",
    border: "1px solid #ccc",
    marginRight: "10px",
    fontSize: "16px",
    background: "#e8e8e8"
  },
  button: {
    background: "#020202ff",
    color: "white",
    border: "none",
    padding: "12px 18px",
    cursor: "pointer",
    fontSize: "16px"
  }
};
