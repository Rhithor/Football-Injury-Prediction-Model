import { useState } from "react";
import axios from "axios";

const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        "http://localhost:8000/auth/login/",
        { email, password },
        { withCredentials: true }
      );
      localStorage.setItem("token", response.data.token);
      // Optionally, redirect to dashboard after login
      window.location.href = "/dashboard";
    } catch (err) {
      alert("Login failed");
    }
  };

  const handleGoogleLogin = () => {
    window.location.href = "http://localhost:8000/accounts/google/login/";
  };

  return (
    <form onSubmit={handleLogin}>
      <input
        value={email}
        onChange={e => setEmail(e.target.value)}
        placeholder="Email"
        type="email"
        required
      />
      <input
        value={password}
        onChange={e => setPassword(e.target.value)}
        placeholder="Password"
        type="password"
        required
      />
      <button type="submit">Login</button>
      <button type="button" onClick={handleGoogleLogin}>
        Login with Google
      </button>
    </form>
  );
};

export default LoginPage;
