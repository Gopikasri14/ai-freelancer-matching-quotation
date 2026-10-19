
import { useState } from "react";
import axios from "axios";
import "./App.css";

const API = "http://127.0.0.1:8000/api/v1";

function App() {
  const [form, setForm] = useState({
    title: "",
    description: "",
    project_type: "Website Development",
    complexity: "Medium",
    expected_hours: 35,
    deadline_days: 14,
    revisions: 2,
    budget: 25000,
  });

  const [freelancers, setFreelancers] = useState([]);
  const [projectId, setProjectId] = useState(null);
  const [selectedFreelancer, setSelectedFreelancer] = useState(null);
  const [quotation, setQuotation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function updateField(event) {
    const { name, value } = event.target;
    setForm((previous) => ({
      ...previous,
      [name]: [
        "expected_hours",
        "deadline_days",
        "revisions",
        "budget",
      ].includes(name)
        ? Number(value)
        : value,
    }));
  }

  async function findFreelancers(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setFreelancers([]);
    setSelectedFreelancer(null);
    setQuotation(null);

    try {
      const projectResponse = await axios.post(`${API}/projects`, form);
      const createdProjectId = projectResponse.data.id;
      setProjectId(createdProjectId);

      const matchingResponse = await axios.post(
        `${API}/matching/projects/${createdProjectId}`
      );

      const data = matchingResponse.data;
      const results = Array.isArray(data)
        ? data
        : data.recommendations ?? data.matches ?? [];

      setFreelancers(results);

      if (results.length === 0) {
        setError(
          "The project was created, but no matching freelancers were returned. Check the matching API response."
        );
      }
    } catch (err) {
      setError(
        err.response?.data?.detail
          ? JSON.stringify(err.response.data.detail)
          : "Could not connect to the backend. Make sure FastAPI is running on port 8000."
      );
    } finally {
      setLoading(false);
    }
  }

  async function generateQuotation(freelancer) {
    setSelectedFreelancer(freelancer);
    setQuotation(null);
    setError("");
    setLoading(true);

    try {
      const freelancerId =
        freelancer.freelancer_id ?? freelancer.id;

      const response = await axios.post(`${API}/quotations/generate`, {
        project_id: projectId,
        freelancer_id: freelancerId,
      });

      setQuotation(response.data);
    } catch (err) {
      setError(
        err.response?.data?.detail
          ? JSON.stringify(err.response.data.detail)
          : "Could not generate the quotation. Check the API response."
      );
    } finally {
      setLoading(false);
    }
  }

  function displayValue(item, keys, fallback = "Not provided") {
    for (const key of keys) {
      if (item?.[key] !== undefined && item[key] !== null) {
        return item[key];
      }
    }
    return fallback;
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <a className="brand" href="#home">
          <span className="brand-icon">✦</span>
          <span>Freelance<span className="brand-accent">AI</span></span>
        </a>
        <span className="topbar-label">MATCHING & QUOTATION OPTIMIZER</span>
        <span className="status"><span /> API-powered</span>
      </header>

      <main className="main-content" id="home">
        <section className="hero">
          <div className="eyebrow">SMARTER FREELANCING STARTS HERE</div>
          <h1>Great work starts with<br /><span>the right match.</span></h1>
          <p>Describe your project. Discover suitable freelancers. Get an AI-assisted effort and price estimate.</p>
        </section>

        {error && <div className="error-message">{error}</div>}

        <div className="workspace">
          <section className="panel project-panel">
            <div className="panel-heading">
              <div className="step-number">01</div>
              <div>
                <h2>Project requirements</h2>
                <p>Tell us what you need to build.</p>
              </div>
            </div>

            <form onSubmit={findFreelancers}>
              <label>Project title</label>
              <input
                name="title"
                value={form.title}
                onChange={updateField}
                placeholder="e.g. E-commerce website"
                required
              />

              <label>Project description</label>
              <textarea
                name="description"
                value={form.description}
                onChange={updateField}
                placeholder="Describe the features, deliverables and goals..."
                rows={4}
                required
              />

              <div className="form-grid">
                <div>
                  <label>Project type</label>
                  <select name="project_type" value={form.project_type} onChange={updateField}>
                    <option>Website Development</option>
                    <option>Mobile App Development</option>
                    <option>Data Science</option>
                    <option>Machine Learning</option>
                    <option>UI/UX Design</option>
                    <option>Content Writing</option>
                    <option>Graphic Design</option>
                  </select>
                </div>
                <div>
                  <label>Complexity</label>
                  <select name="complexity" value={form.complexity} onChange={updateField}>
                    <option>Low</option>
                    <option>Medium</option>
                    <option>High</option>
                  </select>
                </div>
                <div>
                  <label>Expected hours</label>
                  <input type="number" min="1" name="expected_hours" value={form.expected_hours} onChange={updateField} required />
                </div>
                <div>
                  <label>Deadline (days)</label>
                  <input type="number" min="1" name="deadline_days" value={form.deadline_days} onChange={updateField} required />
                </div>
                <div>
                  <label>Revisions included</label>
                  <input type="number" min="0" name="revisions" value={form.revisions} onChange={updateField} required />
                </div>
                <div>
                  <label>Budget (₹)</label>
                  <input type="number" min="0" name="budget" value={form.budget} onChange={updateField} required />
                </div>
              </div>

              <button className="primary-button" type="submit" disabled={loading}>
                {loading ? "Working..." : "Find matching freelancers →"}
              </button>
            </form>
          </section>

          <section className="panel results-panel">
            <div className="panel-heading">
              <div className="step-number">02</div>
              <div>
                <h2>Recommended talent</h2>
                <p>Choose a freelancer for your project.</p>
              </div>
            </div>

            {freelancers.length === 0 ? (
              <div className="empty-state">
                <div className="empty-icon">◎</div>
                <h3>Your next great match is waiting</h3>
                <p>Complete the project form and select Find matching freelancers to see recommendations from your backend.</p>
              </div>
            ) : (
              <div className="freelancer-list">
                {freelancers.map((freelancer, index) => (
                  <article className="freelancer-card" key={freelancer.freelancer_id ?? freelancer.id ?? index}>
                    <div className="freelancer-avatar">
                      {String(displayValue(freelancer, ["name", "freelancer_name"], `F${index + 1}`)).charAt(0).toUpperCase()}
                    </div>
                    <div className="freelancer-info">
                      <h3>{displayValue(freelancer, ["name", "freelancer_name"], `Freelancer ${index + 1}`)}</h3>
                      <p>{displayValue(freelancer, ["skills", "skill_set", "experience_years"], "Profile available")}</p>
                      <span className="match-score">
                        Match score: {displayValue(freelancer, ["similarity_score", "match_score"], "N/A")}
                      </span>
                    </div>
                    <button
                      className="select-button"
                      onClick={() => generateQuotation(freelancer)}
                      disabled={loading}
                    >
                      Select
                    </button>
                  </article>
                ))}
              </div>
            )}

            {selectedFreelancer && (
              <div className="quotation-section">
                <div className="panel-heading">
                  <div className="step-number">03</div>
                  <div>
                    <h2>AI quotation</h2>
                    <p>Estimated effort and price range.</p>
                  </div>
                </div>

                {quotation ? (
                  <>
                    <div className="price-card">
                      <span>Estimated project price</span>
                      <h3>₹{Number(quotation.final_min_price).toLocaleString("en-IN")} – ₹{Number(quotation.final_max_price).toLocaleString("en-IN")}</h3>
                      <p>Based on your project and selected freelancer</p>
                    </div>
                    <div className="quotation-metrics">
                      <div>
                        <span>Predicted effort</span>
                        <strong>{quotation.predicted_effort} hrs</strong>
                      </div>
                      <div>
                        <span>Base price</span>
                        <strong>₹{Number(quotation.base_price).toLocaleString("en-IN")}</strong>
                      </div>
                      <div>
                        <span>Included revisions</span>
                        <strong>{quotation.included_revisions}</strong>
                      </div>
                      <div>
                        <span>Extra revision</span>
                        <strong>₹{Number(quotation.extra_revision_price).toLocaleString("en-IN")}</strong>
                      </div>
                    </div>
                    <p className="disclaimer">This is an estimate generated by your current model and pricing rules, not a guaranteed market price.</p>
                  </>
                ) : (
                  <p className="helper-text">Generating a quotation for your selected freelancer...</p>
                )}
              </div>
            )}
          </section>
        </div>

        <footer>FreelanceAI · AI-assisted matching and quotation optimization</footer>
      </main>
    </div>
  );
}

export default App;
