import VideoCreator from "./VideoCreator";
import CreditDisplay from "./CreditDisplay";
import { useAuth } from "../components/contexts/AuthContext.jsx";
import { Link } from "react-router-dom";


export default function Dashboard() {
  const { user } = useAuth();

  const logout = () => {
    // simple sign out
    import("firebase/auth").then(({ signOut }) => {
      signOut(require("../firebase").auth);
    });
  };

  return (
    <div className="container">
      <header>
        <div>
          <h1>ExplainIt</h1>
          <div>Welcome, {user.email}</div>
        </div>
        <div>
          <CreditDisplay />
          <Link to="/buy-credits">
            <button>Buy More Credits</button>
          </Link>
          
          <button onClick={logout}>Log out</button>
        </div>
      </header>
      <main>
        <VideoCreator />
      </main>
    </div>
  );
}
