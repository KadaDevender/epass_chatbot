import { useState, useEffect, useRef, useCallback } from "react";
import axios from "axios";

function ChatbotUI() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([
    { type: "bot", text: "నమస్కారం! 🙏 How can I help you?" },
  ]);

  const chatEndRef = useRef(null);

  // 🔥 API URL (LIVE BACKEND)
  const API = process.env.REACT_APP_API_URL;

  // 🔥 LOAD HISTORY
  useEffect(() => {
    const loadHistory = async () => {
      const username = localStorage.getItem("username");
      if (!username) return;

      try {
        const res = await axios.get(`${API}/history/${username}`);

        const history = res.data
          .map((item) => [
            { type: "user", text: item.message },
            { type: "bot", text: item.reply },
          ])
          .flat();

        if (history.length > 0) setChat(history);
      } catch (err) {
        console.log(err);
      }
    };

    if (API) loadHistory();
  }, [API]);

  // 🔥 SEND MESSAGE (WITH TYPING EFFECT)
  const sendMessage = useCallback(
    async (customMsg = null) => {
      const finalMessage = customMsg || message;
      if (!finalMessage) return;

      const username = localStorage.getItem("username");

      // Add user + typing
      setChat((prev) => [
        ...prev,
        { type: "user", text: finalMessage },
        { type: "bot", text: "Typing..." },
      ]);

      try {
        const res = await axios.post(`${API}/chat`, {
          message: finalMessage,
          username: username,
        });

        // Delay for typing feel
        setTimeout(() => {
          setChat((prev) => {
            const updated = [...prev];
            updated[updated.length - 1] = {
              type: "bot",
              text: res.data.reply,
            };
            return updated;
          });
        }, 700);
      } catch (err) {
        console.log(err);
      }

      setMessage("");
    },
    [message, API]
  );

  // 🔥 LISTEN BUTTON EVENTS
  useEffect(() => {
    const handler = (e) => {
      sendMessage(e.detail);
    };

    window.addEventListener("chat", handler);
    return () => window.removeEventListener("chat", handler);
  }, [sendMessage]);

  // 🔥 AUTO SCROLL
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chat]);

  return (
    <div style={styles.container}>
      {/* LEFT PANEL */}
      <div style={styles.sidebar}>
        <h4 style={styles.heading}>Categories</h4>

        <button onClick={() => sendMessage("bc")} style={styles.btn}>
          BC Welfare
        </button>

        <button onClick={() => sendMessage("sc")} style={styles.btn}>
          SC Welfare
        </button>

        <button onClick={() => sendMessage("st")} style={styles.btn}>
          ST Welfare
        </button>

        <button onClick={() => sendMessage("general")} style={styles.btn}>
          General
        </button>
      </div>

      {/* RIGHT CHAT */}
      <div style={styles.chatSection}>
        {/* CHAT BOX */}
        <div style={styles.chatBox}>
          {chat.map((msg, i) => (
            <div
              key={i}
              style={msg.type === "user" ? styles.userMsg : styles.botMsg}
            >
              {msg.text === "Typing..." ? "🤖 Typing..." : msg.text}
            </div>
          ))}
          <div ref={chatEndRef}></div>
        </div>

        {/* INPUT */}
        <div style={styles.inputArea}>
          <input
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Ask about ePass..."
            style={styles.input}
            onKeyDown={(e) => {
              if (e.key === "Enter") sendMessage();
            }}
          />

          <button onClick={() => sendMessage()} style={styles.button}>
            ➤
          </button>
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    height: "520px",
    padding: "15px",
    background: "#fff3e8",
    gap: "10px",
  },

  sidebar: {
    width: "200px",
    background: "#ffffff",
    borderRadius: "10px",
    padding: "10px",
    boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
  },

  heading: {
    marginBottom: "10px",
  },

  btn: {
    width: "100%",
    padding: "8px",
    margin: "5px 0",
    borderRadius: "8px",
    border: "1px solid #ddd",
    background: "#fff8f0",
    cursor: "pointer",
  },

  chatSection: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
  },

  chatBox: {
    flex: 1,
    padding: "15px",
    background: "#ffffff",
    borderRadius: "12px",
    boxShadow: "0 2px 10px rgba(0,0,0,0.1)",
    overflowY: "auto",
    display: "flex",
    flexDirection: "column",
  },

  userMsg: {
    alignSelf: "flex-end",
    background: "#138808",
    color: "white",
    padding: "10px",
    borderRadius: "12px",
    margin: "5px",
    maxWidth: "60%",
    textAlign: "right",
  },

  botMsg: {
    alignSelf: "flex-start",
    background: "#fff8f0",
    padding: "10px",
    borderRadius: "12px",
    margin: "5px",
    border: "1px solid #f0d9c8",
    maxWidth: "60%",
  },

  inputArea: {
    display: "flex",
    marginTop: "10px",
  },

  input: {
    flex: 1,
    padding: "10px",
    borderRadius: "10px",
    border: "1px solid #ccc",
  },

  button: {
    padding: "10px 15px",
    background: "#ff6b00",
    color: "white",
    border: "none",
    borderRadius: "10px",
    marginLeft: "5px",
    cursor: "pointer",
  },
};

export default ChatbotUI;