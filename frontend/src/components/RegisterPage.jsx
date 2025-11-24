import { useState } from "react";
import axios from "axios";

const RegisterPage = () => {
  const [email, setEmail] = useState("");
  const [password1, setPassword1] = useState("");
  const [password2, setPassword2] = useState("");

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        "http://localhost:8000/auth/registration/",
        { email, password1, password2 },
        { withCredentials: true }
      );
      localStorage.setItem("token", response.data.token);
      // Optionally, redirect
      window.location.href = "/dashboard";
    } catch (err) {
      alert("Registration failed");
    }
  };

  const handleGoogleLogin = () => {
    window.location.href = "http://localhost:8000/accounts/google/login/";
  };

  return (
    <form onSubmit={handleRegister}>
      <input
        value={email}
        onChange={e => setEmail(e.target.value)}
        placeholder="Email"
        type="email"
        required
      />
      <input
        value={password1}
        onChange={e => setPassword1(e.target.value)}
        placeholder="Password"
        type="password"
        required
      />
      <input
        value={password2}
        onChange={e => setPassword2(e.target.value)}
        placeholder="Confirm Password"
        type="password"
        required
      />
      <button type="submit">Register</button>
      <button type="button" onClick={handleGoogleLogin}>
        Register with Google
      </button>
    </form>
  );
};

export default RegisterPage;
