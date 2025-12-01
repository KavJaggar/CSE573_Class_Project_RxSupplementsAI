
import React, { useState, useEffect, useRef } from "react";
import "./App.css"; 

export default function Chat() {
  // --- STATE ---
  const [sessions, setSessions] = useState(() => {
    const saved = localStorage.getItem("chatSessions");
    return saved ? JSON.parse(saved) : [{ id: 1, title: "New Chat", messages: [] }];
  });
  
  const [currentSessionId, setCurrentSessionId] = useState(() => {
    const saved = JSON.parse(localStorage.getItem("chatSessions"));
    return saved ? saved[0].id : 1;
  });

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  
  const msgEndRef = useRef(null);

  // --- EFFECTS ---
  useEffect(() => {
    localStorage.setItem("chatSessions", JSON.stringify(sessions));
  }, [sessions]);

  useEffect(() => {
    msgEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [sessions, currentSessionId, loading]);

  // --- HELPERS ---
  const getCurrentSession = () => sessions.find(s => s.id === currentSessionId);

  const createNewChat = () => {
    const newId = Date.now();
    const newSession = { id: newId, title: "New Chat", messages: [] };
    setSessions([newSession, ...sessions]);
    setCurrentSessionId(newId);
    if (window.innerWidth < 768) setIsSidebarOpen(false);
  };

  const deleteChat = (e, id) => {
    e.stopPropagation();
    const filtered = sessions.filter(s => s.id !== id);
    if (filtered.length === 0) {
      setSessions([{ id: 1, title: "New Chat", messages: [] }]);
      setCurrentSessionId(1);
    } else {
      setSessions(filtered);
      if (id === currentSessionId) setCurrentSessionId(filtered[0].id);
    }
  };

  const updateCurrentSessionMessages = (newMessagesOrUpdater) => {
    setSessions(prev => prev.map(session => {
      if (session.id === currentSessionId) {
        const updatedMessages = typeof newMessagesOrUpdater === 'function' 
          ? newMessagesOrUpdater(session.messages) 
          : newMessagesOrUpdater;
        
        let newTitle = session.title;
        if (session.title === "New Chat" && updatedMessages.length > 0) {
           const firstUserMsg = updatedMessages.find(m => m.sender === "user");
           if (firstUserMsg) newTitle = firstUserMsg.text.slice(0, 30) + (firstUserMsg.text.length > 30 ? "..." : "");
        }

        return { ...session, messages: updatedMessages, title: newTitle };
      }
      return session;
    }));
  };

  // --- SEND MESSAGE LOGIC ---
  const sendMessage = async () => {
    if (!input.trim()) return;

    const userText = input;
    setInput("");
    setLoading(true);

    updateCurrentSessionMessages(prev => [...prev, { sender: "user", text: userText }]);
    updateCurrentSessionMessages(prev => [...prev, { sender: "bot", text: "" }]);

    try {
      const response = await fetch("http://localhost:8181/run_query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: userText }),
      });

      if (!response.body) throw new Error("No response body");

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let assistantMsg = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        assistantMsg += chunk;

        updateCurrentSessionMessages(prev => {
            const newMsgs = [...prev];
            newMsgs[newMsgs.length - 1].text = assistantMsg;
            return newMsgs;
        });
      }
    } catch (err) {
      console.error(err);
      updateCurrentSessionMessages(prev => {
        const newMsgs = [...prev];
        newMsgs[newMsgs.length - 1].text = "Error: Could not connect to backend.";
        return newMsgs;
      });
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // --- RENDER ---
  const currentMessages = getCurrentSession()?.messages || [];

  return (
    <div className="app-layout">
      {/* SIDEBAR */}
      <aside className={`sidebar ${isSidebarOpen ? "open" : "closed"}`}>
        <div className="sidebar-header">
            <button className="new-chat-btn" onClick={createNewChat}>
                <span className="icon">+</span> New Chat
            </button>
        </div>

        <div className="session-list">
            <div className="session-label">History</div>
            {sessions.map(session => (
                <div 
                    key={session.id} 
                    className={`session-item ${session.id === currentSessionId ? "active" : ""}`}
                    onClick={() => {
                        setCurrentSessionId(session.id);
                        if (window.innerWidth < 768) setIsSidebarOpen(false);
                    }}
                >
                    <span className="session-title">{session.title}</span>
                    <button className="delete-btn" onClick={(e) => deleteChat(e, session.id)}>×</button>
                </div>
            ))}
        </div>
      </aside>

      {/* MAIN CHAT AREA */}
      <main className="chat-main">
        <header className="top-bar">
            <button className="hamburger-btn" onClick={() => setIsSidebarOpen(!isSidebarOpen)}>
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <line x1="3" y1="12" x2="21" y2="12"></line>
                    <line x1="3" y1="6" x2="21" y2="6"></line>
                    <line x1="3" y1="18" x2="21" y2="18"></line>
                </svg>
            </button>
            <div className="header-title">SupplementRx AI</div>
        </header>

        <div className="messages-container">
            {currentMessages.length === 0 ? (
                <div className="empty-state">
                    <h1>SupplementRx AI</h1>
                    <p>Ask about supplements, interactions, or dosage.</p>
                </div>
            ) : (
                currentMessages.map((msg, i) => (
                    <div key={i} className={`message-wrapper ${msg.sender}`}>
                        <div className="message-content">
                            {msg.text.split("\n").map((line, idx) => (
                                <p key={idx}>{line}</p>
                            ))}
                        </div>
                    </div>
                ))
            )}
            {loading && currentMessages.length > 0 && currentMessages[currentMessages.length-1].sender !== 'bot' && (
               <div className="message-wrapper bot">
                  <div className="message-content typing">Thinking...</div>
               </div>
            )}
            <div ref={msgEndRef} />
        </div>

        <div className="input-container">
            <div className="input-box">
                <input 
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Message SupplementRx..."
                    disabled={loading}
                />
                <button onClick={sendMessage} disabled={loading || !input.trim()}>
                    SEND
                </button>
            </div>
        </div>
      </main>

      {isSidebarOpen && (
        <div className="mobile-overlay" onClick={() => setIsSidebarOpen(false)}></div>
      )}
    </div>
  );
}
