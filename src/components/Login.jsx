import { useState } from "react";
import { signInWithEmailAndPassword } from "firebase/auth";
import { auth } from "../firebase";
import { Link, useNavigate } from "react-router-dom";

export default function Login() {
  const [email, setEmail] = useState("");
  const [pass, setPass] = useState("");
  const [err, setErr] = useState("");
  const navigate = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    try {
      await signInWithEmailAndPassword(auth, email, pass);
      navigate("/");
    } catch (e) {
      setErr(e.message);
    }
  };

  return (
    <div className="card">
      <h2>Log In</h2>
      <form onSubmit={submit}>
        <input placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required />
        <input placeholder="Password" type="password" value={pass} onChange={e => setPass(e.target.value)} required />
        <button type="submit">Log in</button>
      </form>
      {err && <div className="error">{err}</div>}
      <div>
        Need account? <Link to="/signup">Sign up</Link>
      </div>
    </div>
  );
}
