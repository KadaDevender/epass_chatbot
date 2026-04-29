import { useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  // 🔥 Works for both local + deployed
  const API = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";

  const handleLogin = async () => {
    if (!username || !password) {
      alert("Please enter username and password");
      return;
    }

    try {
      const res = await axios.post(`${API}/login`, {
        username,
        password,
      });

      if (res.data.message === "Login successful") {
        localStorage.setItem("username", username);
        window.location.href = "/";
      } else {
        alert("User not found. Please register.");
      }
    } catch (err) {
      console.log(err);
      alert("Login failed ❌");
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h2 style={styles.title}>Login</h2>

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

        <button onClick={handleLogin} style={styles.button}>
          Login
        </button>

        {/* 🔥 REGISTER OPTION */}
        <p style={styles.text}>
          New user?{" "}
          <Link to="/signup" style={styles.link}>
            Register here
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

export default Login;













// import { useState } from "react";
// import axios from "axios";

// function Login() {
//   const [username, setUsername] = useState("");
//   const [password, setPassword] = useState("");

//   const handleLogin = async () => {
//     try {
//       const res = await axios.post("http://localhost:8000/login", {
//         username,
//         password,
//       });

//       alert(res.data.message);

//      if (res.data.message === "Login successful") {
//         localStorage.setItem("username", username); // 🔥 store user
//         window.location.href = "/";
//       }
//     } catch (err) {
//       console.log(err);
//     }
//   };

//   return (
//     <div style={{ padding: "50px" }}>
//       <h2>Login</h2>

//       <input
//         placeholder="Username"
//         onChange={(e) => setUsername(e.target.value)}
//       /><br /><br />

//       <input
//         type="password"
//         placeholder="Password"
//         onChange={(e) => setPassword(e.target.value)}
//       /><br /><br />

//       <button onClick={handleLogin}>Login</button>
//     </div>
//   );
// }

// export default Login;