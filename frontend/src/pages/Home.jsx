import { useEffect } from "react";
import Navbar from "../components/Navbar";
import ChatbotUI from "../components/ChatbotUI";

function Home() {

  // 🔐 PROTECT ROUTE
  useEffect(() => {
    const user = localStorage.getItem("username");
    if (!user) {
      window.location.href = "/login";
    }
  }, []);

  if (!localStorage.getItem("username")) return null;

  return (
    <div>
      <Navbar />

      {/* 🔥 MAIN LAYOUT */}
      <div style={styles.container}>
        
        {/* CHATBOT */}
        <div style={styles.chatArea}>
          <ChatbotUI />
        </div>

        {/* 🔥 RIGHT PANEL */}
        <div style={styles.sidePanel}>

          {/* 🔴 IMPORTANT UPDATE */}
          <div style={styles.card}>
            <h4>📢 Latest Update</h4>
            <p>Scholarship last date extended till 30th April!</p>
          </div>

          {/* 🟡 QUICK ACTIONS */}
          <div style={styles.card}>
            <h4>⚡ Quick Actions</h4>

            <button
              style={styles.actionBtn}
              onClick={() =>
                window.dispatchEvent(
                  new CustomEvent("chat", { detail: "how to apply" })
                )
              }
            >
              Apply Scholarship
            </button>

            <button
              style={styles.actionBtn}
              onClick={() =>
                window.dispatchEvent(
                  new CustomEvent("chat", { detail: "documents" })
                )
              }
            >
              Required Documents
            </button>

            <button
              style={styles.actionBtn}
              onClick={() =>
                window.dispatchEvent(
                  new CustomEvent("chat", { detail: "status" })
                )
              }
            >
              Check Status
            </button>

            <button
              style={styles.actionBtn}
              onClick={() =>
                window.dispatchEvent(
                  new CustomEvent("chat", { detail: "income limit" })
                )
              }
            >
              Income Limit
            </button>
          </div>

          {/* 🔵 FAQ */}
          <div style={styles.card}>
            <h4>❓ FAQs</h4>

            <p
              style={styles.faq}
              onClick={() =>
                window.dispatchEvent(
                  new CustomEvent("chat", { detail: "how to apply" })
                )
              }
            >
              How to apply for ePass?
            </p>

            <p
              style={styles.faq}
              onClick={() =>
                window.dispatchEvent(
                  new CustomEvent("chat", { detail: "documents" })
                )
              }
            >
              What documents are required?
            </p>

            <p
              style={styles.faq}
              onClick={() =>
                window.dispatchEvent(
                  new CustomEvent("chat", { detail: "status" })
                )
              }
            >
              How to check status?
            </p>

            <p
              style={styles.faq}
              onClick={() =>
                window.dispatchEvent(
                  new CustomEvent("chat", { detail: "income limit" })
                )
              }
            >
              What is income limit?
            </p>
          </div>

        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    padding: "10px",
    gap: "10px",
  },

  chatArea: {
    flex: 2,
  },

  sidePanel: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },

  card: {
    background: "white",
    padding: "12px",
    borderRadius: "12px",
    boxShadow: "0 2px 10px rgba(0,0,0,0.1)",
  },

  actionBtn: {
    width: "100%",
    padding: "10px",
    margin: "6px 0",
    borderRadius: "8px",
    border: "none",
    background: "#ff6b00",
    color: "white",
    cursor: "pointer",
    fontWeight: "bold",
  },

  faq: {
    cursor: "pointer",
    margin: "6px 0",
    color: "#333",
  },
};

export default Home;













































































// import { useEffect } from "react";
// import Navbar from "../components/Navbar";
// import ChatbotUI from "../components/ChatbotUI";

// function Home() {

//   useEffect(() => {
//     const user = localStorage.getItem("username");

//     if (!user) {
//       window.location.href = "/login";
//     }
//   }, []);

//   // 🔥 ADD THIS LINE HERE
//   if (!localStorage.getItem("username")) return null;

//   return (
//     <div>
//       <Navbar />
//       <ChatbotUI />
//     </div>
//   );
// }

// export default Home;