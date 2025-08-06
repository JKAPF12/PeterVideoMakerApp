// src/contexts/AuthContext.jsx
import { createContext, useContext, useEffect, useState } from "react";
import {
  auth,
  onAuthStateChanged,
  ensureUserDoc,
  doc,
  getDoc,
  updateDoc,
  db,
} from "../../firebase.js";

const AuthContext = createContext();

export function useAuth() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [credits, setCredits] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsub = onAuthStateChanged(auth, async (u) => {
      if (u) {
        setUser(u);
        const userRef = await ensureUserDoc(u.uid);
        const snap = await getDoc(userRef);
        setCredits(snap.data()?.credits || 0);
      } else {
        setUser(null);
        setCredits(0);
      }
      setLoading(false);
    });
    return unsub;
  }, []);

  const deductCredit = async () => {
    if (!user) return;
    const userRef = doc(db, "users", user.uid);
    await updateDoc(userRef, { credits: credits - 1 });
    setCredits((c) => c - 1);
  };

  const value = { user, credits, deductCredit };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
}