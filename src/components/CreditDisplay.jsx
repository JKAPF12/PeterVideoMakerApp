import { useAuth } from "./contexts/AuthContext";

export default function CreditDisplay() {
  const { credits } = useAuth();
  return (
    <div className="credit-box">
      <strong>Video credits:</strong> {credits}
    </div>
  );
}
