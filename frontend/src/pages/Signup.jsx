import { useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

function Signup() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  // 🔥 AUTO WORKS BOTH LOCAL + LIVE
  const API = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";

  const handleSignup = async () => {
    if (!username || !password) {
      alert("Please fill all fields");
      return;
    }

    try {
      const res = await axios.post(`${API}/signup`, {
        username,
        password,
      });

      alert("Account created successfully ✅");
      window.location.href = "/login";
    } catch (err) {
      console.log(err);
      alert("User already exists or error occurred ❌");
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h2 style={styles.title}>Create Account</h2>

        <input
          placeholder="Username"
          style={styles.input}
          onChange={(e) => setUsername(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          style={styles.input}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button onClick={handleSignup} style={styles.button}>
          Register
        </button>

        <p style={styles.text}>
          Already have an account?{" "}
          <Link to="/login" style={styles.link}>
            Login
          </Link>
        </p>
      </div>
    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    height: "100vh",
    background: "#fff3e8",
  },

  card: {
    background: "white",
    padding: "30px",
    borderRadius: "12px",
    boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
    width: "320px",
    textAlign: "center",
  },

  title: {
    marginBottom: "15px",
  },

  input: {
    width: "100%",
    padding: "10px",
    margin: "10px 0",
    borderRadius: "6px",
    border: "1px solid #ccc",
  },

  button: {
    width: "100%",
    padding: "10px",
    background: "#ff6b00",
    color: "white",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
  },

  text: {
    marginTop: "12px",
  },

  link: {
    color: "blue",
    textDecoration: "none",
  },
};

export default Signup;










// import { useState } from "react";
// import axios from "axios";

// function Signup() {
//   const [username, setUsername] = useState("");
//   const [password, setPassword] = useState("");

//   const handleSignup = async () => {
//     try {
//       const res = await axios.post("http://localhost:8000/signup", {
//         username,
//         password,
//       });

//       alert(res.data.message);
//     } catch (err) {
//       console.log(err);
//     }
//   };

//   return (
//     <div style={{ padding: "50px" }}>
//       <h2>Signup</h2>

//       <input
//         placeholder="Username"
//         onChange={(e) => setUsername(e.target.value)}
//       /><br /><br />

//       <input
//         type="password"
//         placeholder="Password"
//         onChange={(e) => setPassword(e.target.value)}
//       /><br /><br />

//       <button onClick={handleSignup}>Signup</button>
//     </div>
//   );
// }

// export default Signup;