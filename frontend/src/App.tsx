import { useEffect, useState } from "react";
import { checkBackendHealth } from "./services/api";

function App() {
  const [backendStatus, setBackendStatus] = useState("Checking...");

  useEffect(() => {
    checkBackendHealth()
      .then((data) => {
        setBackendStatus(data.status);
      })
      .catch(() => {
        setBackendStatus("Backend unavailable");
      });
  }, []);

  return (
    <div>
      <h1>AI Researcher</h1>
      <p>Backend Status: {backendStatus}</p>
    </div>
  );
}

export default App;