import { useEffect, useState } from "react";
import {
  checkBackendHealth,
  createResearchProject,
  getResearchProjects,
  runResearch,
  type ResearchProject,
} from "./services/api";
import "./App.css";

function App() {
  const [backendStatus, setBackendStatus] = useState("Checking...");
  const [question, setQuestion] = useState("");
  const [depth, setDepth] = useState("deep");
  const [sources, setSources] = useState("web");
  const [projects, setProjects] = useState<ResearchProject[]>([]);
  const [isCreating, setIsCreating] = useState(false);

  useEffect(() => {
    checkBackendHealth()
      .then((data) => {
        setBackendStatus(data.status);
      })
      .catch(() => {
        setBackendStatus("Backend unavailable");
      });

    getResearchProjects()
      .then((data) => {
        setProjects(data);
      })
      .catch(() => {
        console.error("Failed to load research projects");
      });
  }, []);

  const handleStartResearch = async () => {
    if (!question.trim()) {
      return;
    }

    setIsCreating(true);

    try {
      // -------------------------------------------------
      // STEP 1: CREATE RESEARCH PROJECT
      // -------------------------------------------------

      const project = await createResearchProject({
        title: question.trim().slice(0, 60),
        question: question.trim(),
        depth,
        sources,
      });

      // Add the newly created project to the sidebar
      setProjects((currentProjects) => [
        project,
        ...currentProjects,
      ]);

      // -------------------------------------------------
      // STEP 2: RUN RESEARCH PIPELINE
      // -------------------------------------------------

      const result = await runResearch(project.id);

      // -------------------------------------------------
      // STEP 3: UPDATE PROJECT STATUS
      // -------------------------------------------------

      setProjects((currentProjects) =>
        currentProjects.map((item) =>
          item.id === project.id
            ? {
              ...item,
              status: result.status,
            }
            : item
        )
      );

      console.log("Research completed:", result);

      // Clear the research input after successful execution
      setQuestion("");
    } catch (error) {
      console.error("Research failed:", error);
    } finally {
      setIsCreating(false);
    }
  };

  return (
    <div className="app">
      {/* -------------------------------------------------
          TOP BAR
      ------------------------------------------------- */}

      <header className="topbar">
        <div className="brand">
          <div className="brand-icon">✦</div>

          <div>
            <h1>AI Researcher</h1>
            <span>Intelligent Research Workspace</span>
          </div>
        </div>

        <div className="topbar-actions">
          <button
            className="header-button"
            type="button"
          >
            Projects
          </button>

          <button
            className="header-button"
            type="button"
          >
            Settings
          </button>

          <div className="status">
            <span className="status-dot"></span>
            API {backendStatus}
          </div>
        </div>
      </header>

      {/* -------------------------------------------------
          MAIN WORKSPACE
      ------------------------------------------------- */}

      <main className="workspace">

        {/* -------------------------------------------------
            SIDEBAR
        ------------------------------------------------- */}

        <aside className="sidebar">

          <button
            className="new-research"
            onClick={() => setQuestion("")}
            type="button"
          >
            <span>+</span>
            New Research
          </button>

          <div className="sidebar-section">
            <p className="section-title">
              Workspace
            </p>

            <button
              className="sidebar-item active"
              type="button"
            >
              <span>⌂</span>
              Overview
            </button>

            <button
              className="sidebar-item"
              type="button"
            >
              <span>◷</span>
              Research History
            </button>

            <button
              className="sidebar-item"
              type="button"
            >
              <span>☆</span>
              Saved Reports
            </button>
          </div>

          {/* -------------------------------------------------
              RECENT RESEARCH
          ------------------------------------------------- */}

          <div className="sidebar-section">
            <p className="section-title">
              Recent Research
            </p>

            {projects.length === 0 ? (
              <p
                style={{
                  padding: "0 10px",
                  fontSize: "12px",
                  color: "#626b7b",
                }}
              >
                No research projects yet
              </p>
            ) : (
              projects.map((project) => (
                <button
                  className="research-item"
                  key={project.id}
                  onClick={() =>
                    setQuestion(project.question)
                  }
                  type="button"
                >
                  {project.title}
                </button>
              ))
            )}
          </div>
        </aside>

        {/* -------------------------------------------------
            MAIN CONTENT
        ------------------------------------------------- */}

        <section className="content">

          {/* -------------------------------------------------
              WELCOME SECTION
          ------------------------------------------------- */}

          <div className="welcome">
            <p className="eyebrow">
              RESEARCH WORKSPACE
            </p>

            <h2>
              What would you like to research?
            </h2>

            <p>
              Explore a topic, analyze sources, and
              generate a citation-backed research report.
            </p>
          </div>

          {/* -------------------------------------------------
              RESEARCH CARD
          ------------------------------------------------- */}

          <div className="research-card">

            <textarea
              className="research-input"
              placeholder="e.g. How is generative AI transforming software development?"
              value={question}
              onChange={(event) =>
                setQuestion(event.target.value)
              }
            />

            {/* -------------------------------------------------
                RESEARCH OPTIONS
            ------------------------------------------------- */}

            <div className="research-options">

              {/* RESEARCH DEPTH */}

              <div className="option-group">
                <label>
                  Research Depth
                </label>

                <div className="option-buttons">

                  <button
                    className={`option-button ${depth === "quick"
                      ? "selected"
                      : ""
                      }`}
                    onClick={() =>
                      setDepth("quick")
                    }
                    type="button"
                  >
                    Quick
                  </button>

                  <button
                    className={`option-button ${depth === "deep"
                      ? "selected"
                      : ""
                      }`}
                    onClick={() =>
                      setDepth("deep")
                    }
                    type="button"
                  >
                    Deep
                  </button>

                  <button
                    className={`option-button ${depth === "academic"
                      ? "selected"
                      : ""
                      }`}
                    onClick={() =>
                      setDepth("academic")
                    }
                    type="button"
                  >
                    Academic
                  </button>

                </div>
              </div>

              {/* SOURCES */}

              <div className="option-group">
                <label>
                  Sources
                </label>

                <div className="option-buttons">

                  <button
                    className={`option-button ${sources === "web"
                      ? "selected"
                      : ""
                      }`}
                    onClick={() =>
                      setSources("web")
                    }
                    type="button"
                  >
                    Web
                  </button>

                  <button
                    className={`option-button ${sources === "papers"
                      ? "selected"
                      : ""
                      }`}
                    onClick={() =>
                      setSources("papers")
                    }
                    type="button"
                  >
                    Papers
                  </button>

                  <button
                    className={`option-button ${sources === "documents"
                      ? "selected"
                      : ""
                      }`}
                    onClick={() =>
                      setSources("documents")
                    }
                    type="button"
                  >
                    Documents
                  </button>

                </div>
              </div>

            </div>

            {/* -------------------------------------------------
                START RESEARCH BUTTON
            ------------------------------------------------- */}

            <button
              className="start-button"
              onClick={handleStartResearch}
              disabled={
                isCreating ||
                !question.trim()
              }
              type="button"
            >
              {isCreating
                ? "Researching..."
                : "Start Research"}

              <span>→</span>
            </button>

          </div>

          {/* -------------------------------------------------
              FEATURE CARDS
          ------------------------------------------------- */}

          <div className="feature-grid">

            <div className="feature-card">
              <span className="feature-icon">
                ⌕
              </span>

              <h3>
                Deep Research
              </h3>

              <p>
                Break complex questions into focused
                research tasks.
              </p>
            </div>

            <div className="feature-card">
              <span className="feature-icon">
                ◈
              </span>

              <h3>
                Source Intelligence
              </h3>

              <p>
                Collect and analyze information from
                multiple sources.
              </p>
            </div>

            <div className="feature-card">
              <span className="feature-icon">
                ✦
              </span>

              <h3>
                AI Analysis
              </h3>

              <p>
                Synthesize evidence into structured
                research reports.
              </p>
            </div>

          </div>

        </section>
      </main>
    </div>
  );
}

export default App;