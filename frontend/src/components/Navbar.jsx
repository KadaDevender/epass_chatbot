import logo from "../assets/logo.png";
import { Link } from "react-router-dom";

function Navbar() {
  const username = localStorage.getItem("username");

  const handleLogout = () => {
    localStorage.removeItem("username");
    window.location.href = "/login";
  };

  return (
    <div style={styles.header}>
      
      {/* LEFT */}
      <div style={styles.left}>
        <img src={logo} alt="logo" style={styles.logo} />
        <div>
          <h2 style={styles.title}>Telangana ePass AI Assistant</h2>
          <p style={styles.subtitle}>తెలంగాణ ఇపాస్ AI సహాయకుడు</p>
        </div>
      </div>

      {/* RIGHT */}
      <div style={styles.right}>
        <span style={styles.online}>● Online</span>
        <span style={styles.phone}>📞 1800-599-4977</span>

        {/* USER AUTH */}
        <div style={styles.authButtons}>
          {username ? (
            <>
              <span style={styles.user}>Welcome, {username}</span>

              <button onClick={handleLogout} style={styles.logoutBtn}>
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" style={styles.link}>
                Login
              </Link>

              <Link to="/signup" style={styles.link}>
                Signup
              </Link>
            </>
          )}
        </div>
      </div>

    </div>
  );
}

const styles = {
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    background: "#ff6b00",
    color: "white",
    padding: "12px 20px",
  },

  left: {
    display: "flex",
    alignItems: "center",
    gap: "10px",
  },

  // 🔥 UPDATED LOGO STYLE (SMALL + ROUND)
  logo: {
    width: "40px",
    height: "40px",
    borderRadius: "50%",
    objectFit: "cover",
    border: "2px solid white",
    background: "white",
    padding: "2px",
  },

  title: {
    margin: 0,
    fontSize: "18px",
  },

  subtitle: {
    margin: 0,
    fontSize: "11px",
  },

  right: {
    display: "flex",
    flexDirection: "column",
    alignItems: "flex-end",
    fontSize: "12px",
    gap: "5px",
  },

  online: {
    color: "lightgreen",
    fontWeight: "bold",
  },

  phone: {
    fontSize: "11px",
  },

  authButtons: {
    display: "flex",
    gap: "10px",
    marginTop: "5px",
    alignItems: "center",
  },

  link: {
    color: "white",
    textDecoration: "none",
    background: "#138808",
    padding: "5px 10px",
    borderRadius: "6px",
    fontSize: "12px",
  },

  logoutBtn: {
    background: "#b22222",
    color: "white",
    border: "none",
    padding: "5px 10px",
    borderRadius: "6px",
    cursor: "pointer",
    fontSize: "12px",
  },

  user: {
    fontWeight: "bold",
    marginRight: "5px",
  },
};

export default Navbar;