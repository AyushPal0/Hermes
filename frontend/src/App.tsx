import { useEffect, useState } from "react";
import { checkBackendHealth } from "./services/api";
import "./App.css";

function App() {
  const [backendStatus, setBackendStatus] = useState("Checking...");
  const [question, setQuestion] = useState("");
  const [depth, setDepth] = useState("Deep");
  const [sources, setSources] = useState("Web");

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
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <div className="brand-icon">✦</div>
          <div>
            <h1>AI Researcher</h1>
            <span>Intelligent Research Workspace</span>
          </div>
        </div>

        <div className="topbar-actions">
          <button className="header-button">Projects</button>
          <button className="header-button">Settings</button>
          <div className="status">
            <span className="status-dot"></span>
            API {backendStatus}
          </div>
        </div>
      </header>

      <main className="workspace">
        <aside className="sidebar">
          <button className="new-research">
            <span>+</span>
            New Research
          </button>

          <div className="sidebar-section">
            <p className="section-title">Workspace</p>

            <button className="sidebar-item active">
              <span>⌂</span>
              Overview
            </button>

            <button className="sidebar-item">
              <span>◷</span>
              Research History
            </button>

            <button className="sidebar-item">
              <span>☆</span>
              Saved Reports
            </button>
          </div>

          <div className="sidebar-section">
            <p className="section-title">Recent Research</p>

            <button className="research-item">
              AI in Drug Discovery
            </button>

            <button className="research-item">
              Future of Quantum Computing
            </button>

            <button className="research-item">
              Impact of AI on Education
            </button>
          </div>
        </aside>

        <section className="content">
          <div className="welcome">
            <p className="eyebrow">RESEARCH WORKSPACE</p>
            <h2>What would you like to research?</h2>
            <p>
              Explore a topic, analyze sources, and generate a
              citation-backed research report.
            </p>
          </div>

          <div className="research-card">
            <textarea
              className="research-input"
              placeholder="e.g. How is generative AI transforming software development?"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
            />

            <div className="research-options">
              <div className="option-group">
                <label>Research Depth</label>

                <div className="option-buttons">
                  <button
                    className={`option-button ${depth === "Quick" ? "selected" : ""}`}
                    onClick={() => setDepth("Quick")}
                  >
                    Quick
                  </button>

                  <button
                    className={`option-button ${depth === "Deep" ? "selected" : ""}`}
                    onClick={() => setDepth("Deep")}
                  >
                    Deep
                  </button>

                  <button
                    className={`option-button ${depth === "Academic" ? "selected" : ""}`}
                    onClick={() => setDepth("Academic")}
                  >
                    Academic
                  </button>
                </div>
              </div>

              <div className="option-group">
                <label>Sources</label>

                <div className="option-buttons">
                  <button
                    className={`option-button ${sources === "Web" ? "selected" : ""}`}
                    onClick={() => setSources("Web")}
                  >
                    Web
                  </button>

                  <button
                    className={`option-button ${sources === "Papers" ? "selected" : ""}`}
                    onClick={() => setSources("Papers")}
                  >
                    Papers
                  </button>

                  <button
                    className={`option-button ${sources === "Documents" ? "selected" : ""}`}
                    onClick={() => setSources("Documents")}
                  >
                    Documents
                  </button>
                </div>
              </div>
            </div>

            <button className="start-button">
              Start Research
              <span>→</span>
            </button>
          </div>

          <div className="feature-grid">
            <div className="feature-card">
              <span className="feature-icon">⌕</span>
              <h3>Deep Research</h3>
              <p>
                Break complex questions into focused research tasks.
              </p>
            </div>

            <div className="feature-card">
              <span className="feature-icon">◈</span>
              <h3>Source Intelligence</h3>
              <p>
                Collect and analyze information from multiple sources.
              </p>
            </div>

            <div className="feature-card">
              <span className="feature-icon">✦</span>
              <h3>AI Analysis</h3>
              <p>
                Synthesize evidence into structured research reports.
              </p>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;