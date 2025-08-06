import { useState } from "react";
import { useAuth } from "./contexts/AuthContext";
import { doc, updateDoc, getDoc } from "firebase/firestore";
import { db } from "../firebase";
import { Link } from "react-router-dom";


export default function PaymentPage() {
  const { user } = useAuth();
  const [amount, setAmount] = useState(5); // default credits to buy
  const [status, setStatus] = useState("");

  const handlePurchase = async () => {
    if (!user) {
      setStatus("You must be logged in to buy credits.");
      return;
    }
    setStatus("Processing payment...");

    // Simulate successful payment after 2s
    setTimeout(async () => {
      try {
        const userRef = doc(db, "users", user.uid);
        const snap = await getDoc(userRef);
        const currentCredits = snap.data()?.credits || 0;

        await updateDoc(userRef, { credits: currentCredits + amount });
        setStatus(`✅ Payment successful! Added ${amount} credits to your account.`);
      } catch (err) {
        console.error(err);
        setStatus("❌ Something went wrong updating your credits.");
      }
    }, 2000);
  };

  return (
    <div className="card">
      <h2>Buy More Credits</h2>
      <p>Each credit allows you to generate 1 video.</p>

      <label>Number of credits to buy:</label>
      <input
        type="number"
        min="1"
        value={amount}
        onChange={(e) => setAmount(Number(e.target.value))}
      />

      <button onClick={handlePurchase}>Pay (Simulated)</button>

      {status && <p>{status}</p>}

      <hr />
      <Link to="/">⬅ Back to Dashboard</Link>
    </div>
  );
}
