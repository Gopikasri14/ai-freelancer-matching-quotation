import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const API =
  "https://ai-freelancer-matching-backend.onrender.com/api/v1";

function App() {
  const [form, setForm] = useState({
    title: "",
    description: "",
    project_type: "Website",
    complexity: "Medium",
    expected_hours: "",
    deadline_days: 7,
    revisions: 2,
    budget: "",
  });

  const [project, setProject] = useState(null);
  const [matches, setMatches] = useState([]);
  const [selected, setSelected] = useState(null);
  const [quote, setQuote] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const update = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  async function createProject(e) {
    e.preventDefault();

    setError("");
    setLoading(true);
    setProject(null);
    setMatches([]);
    setSelected(null);
    setQuote(null);

    try {
      const body = {
        ...form,

        expected_hours: form.expected_hours
          ? Number(form.expected_hours)
          : null,

        deadline_days: Number(form.deadline_days),

        revisions: Number(form.revisions),

        budget: form.budget
          ? Number(form.budget)
          : null,
      };

      // CREATE PROJECT
      const projectResponse = await fetch(
        `${API}/projects`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify(body),
        }
      );

      if (!projectResponse.ok) {
        throw new Error(
          await projectResponse.text()
        );
      }

      const createdProject =
        await projectResponse.json();

      setProject(createdProject);

      // FIND MATCHING FREELANCERS
      const matchResponse = await fetch(
        `${API}/matching/projects/${createdProject.id}`,
        {
          method: "POST",
        }
      );

      if (!matchResponse.ok) {
        throw new Error(
          await matchResponse.text()
        );
      }

      const matchedFreelancers =
        await matchResponse.json();

      setMatches(matchedFreelancers);

    } catch (err) {
      console.error(err);

      setError(
        err.message ||
          "Something went wrong"
      );

    } finally {
      setLoading(false);
    }
  }

  async function generateQuote() {
    if (!selected || !project) {
      return;
    }

    setError("");
    setLoading(true);

    try {
      const response = await fetch(
        `${API}/quotations/generate`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            project_id: project.id,
            freelancer_id: selected.id,
          }),
        }
      );

      if (!response.ok) {
        throw new Error(
          await response.text()
        );
      }

      const quotation =
        await response.json();

      setQuote(quotation);

    } catch (err) {
      console.error(err);

      setError(
        err.message ||
          "Failed to generate quotation"
      );

    } finally {
      setLoading(false);
    }
  }

  const formatNumber = (value) => {
    const number = Number(value);

    if (Number.isNaN(number)) {
      return value;
    }

    return number.toLocaleString("en-IN");
  };

  return (
    <div className="page">

      {/* HEADER */}

      <header>
        <div>
          <h1>AI Freelancer Match</h1>

          <p>
            Requirement matching + quotation
            optimization
          </p>
        </div>

        <span className="badge">
          TF-IDF • XGBoost
        </span>
      </header>


      <main>

        {/* =====================================
            STEP 1
        ====================================== */}

        <section className="card">

          <h2>
            1. Create Project
          </h2>

          <form onSubmit={createProject}>

            <input
              name="title"
              placeholder="Project title"
              value={form.title}
              onChange={update}
              required
            />

            <textarea
              name="description"
              placeholder="Describe the requirements, technologies and features..."
              value={form.description}
              onChange={update}
              required
            />

            <div className="grid">

              <label>
                Type

                <select
                  name="project_type"
                  value={form.project_type}
                  onChange={update}
                >
                  <option>
                    Website
                  </option>

                  <option>
                    E-commerce
                  </option>

                  <option>
                    Mobile App
                  </option>

                  <option>
                    Data Science
                  </option>

                  <option>
                    NLP
                  </option>

                  <option>
                    Dashboard
                  </option>

                  <option>
                    API
                  </option>
                </select>
              </label>


              <label>
                Complexity

                <select
                  name="complexity"
                  value={form.complexity}
                  onChange={update}
                >
                  <option>
                    Low
                  </option>

                  <option>
                    Medium
                  </option>

                  <option>
                    High
                  </option>
                </select>
              </label>


              <label>
                Expected hours

                <input
                  name="expected_hours"
                  type="number"
                  min="1"
                  value={form.expected_hours}
                  onChange={update}
                />
              </label>


              <label>
                Deadline days

                <input
                  name="deadline_days"
                  type="number"
                  min="1"
                  value={form.deadline_days}
                  onChange={update}
                />
              </label>


              <label>
                Revisions

                <input
                  name="revisions"
                  type="number"
                  min="0"
                  value={form.revisions}
                  onChange={update}
                />
              </label>


              <label>
                Budget (₹)

                <input
                  name="budget"
                  type="number"
                  min="1"
                  value={form.budget}
                  onChange={update}
                />
              </label>

            </div>


            <button
              type="submit"
              disabled={loading}
            >
              {loading
                ? "Processing..."
                : "Find Suitable Freelancers"}
            </button>

          </form>


          {error && (
            <div className="error">
              {error}
            </div>
          )}

        </section>


        {/* PROJECT */}

        {project && (
          <section className="card">

            <h2>
              Project Created
            </h2>

            <p>
              <b>Project ID:</b>{" "}
              {project.id}
            </p>

            <p>
              <b>Title:</b>{" "}
              {project.title}
            </p>

          </section>
        )}


        {/* =====================================
            STEP 2
        ====================================== */}

        {matches.length > 0 && (
          <section className="card">

            <h2>
              2. Recommended Freelancers
            </h2>

            <div className="cards">

              {matches.map((m) => (

                <div
                  className={`person ${
                    selected?.id === m.id
                      ? "selected"
                      : ""
                  }`}
                  key={m.id}
                >

                  <div className="rank">
                    #{m.rank}
                  </div>

                  <h3>
                    {m.name}
                  </h3>

                  <p>
                    {m.bio}
                  </p>


                  {m.skills &&
                    m.skills.length > 0 && (

                    <div className="skills">

                      {m.skills.map(
                        (skill) => (
                          <span key={skill}>
                            {skill}
                          </span>
                        )
                      )}

                    </div>
                  )}


                  <p>
                    <b>
                      {(
                        Number(
                          m.similarity_score || 0
                        ) * 100
                      ).toFixed(1)}
                      %
                    </b>{" "}
                    requirement similarity
                  </p>


                  <p>
                    {m.experience_years} yrs
                    {" • "}
                    ₹
                    {formatNumber(
                      m.hourly_rate
                    )}
                    /hr
                  </p>


                  <button
                    type="button"
                    onClick={() => {
                      setSelected(m);
                      setQuote(null);
                      setError("");
                    }}
                  >
                    {selected?.id === m.id
                      ? "Selected"
                      : "Select Freelancer"}
                  </button>

                </div>

              ))}

            </div>

          </section>
        )}


        {/* =====================================
            STEP 3
        ====================================== */}

        {selected && (
          <section className="card">

            <h2>
              3. Generate AI Quotation
            </h2>

            <p>
              Selected:{" "}
              <b>
                {selected.name}
              </b>
            </p>

            <p>
              Hourly rate:{" "}
              <b>
                ₹
                {formatNumber(
                  selected.hourly_rate
                )}
              </b>
            </p>


            <button
              type="button"
              onClick={generateQuote}
              disabled={loading}
            >
              {loading
                ? "Generating..."
                : "Generate Quotation"}
            </button>

          </section>
        )}


        {/* =====================================
            STEP 4
        ====================================== */}

        {quote && (
          <section className="card quote">

            <h2>
              4. Optimized Quotation
            </h2>


            <div className="price">

              ₹
              {formatNumber(
                quote.final_min_price
              )}

              {" – "}

              ₹
              {formatNumber(
                quote.final_max_price
              )}

            </div>


            <div className="grid stats">

              <div>
                <small>
                  Estimated effort
                </small>

                <b>
                  {quote.effort_min}
                  {"–"}
                  {quote.effort_max}
                  {" hours"}
                </b>
              </div>


              <div>
                <small>
                  Base model price
                </small>

                <b>
                  ₹
                  {formatNumber(
                    quote.base_price
                  )}
                </b>
              </div>


              <div>
                <small>
                  Included revisions
                </small>

                <b>
                  {quote.included_revisions}
                </b>
              </div>


              <div>
                <small>
                  Extra revision
                </small>

                <b>
                  ₹
                  {formatNumber(
                    quote.extra_revision_price
                  )}
                </b>
              </div>

            </div>


            {quote.adjustments && (
              <>
                <h3>
                  Adjustments
                </h3>

                <ul>

                  {Object.entries(
                    quote.adjustments
                  ).map(
                    ([key, value]) => (
                      <li key={key}>
                        {key.replaceAll(
                          "_",
                          " "
                        )}
                        : {value}%
                      </li>
                    )
                  )}

                </ul>
              </>
            )}

          </section>
        )}

      </main>

    </div>
  );
}

createRoot(
  document.getElementById("root")
).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);