import { Link } from "react-router-dom";

const opportunities = [
  { name: "Northstar Labs", type: "Startup role", signal: "Hiring", score: "86" },
  { name: "Fieldwork Studio", type: "Agency partner", signal: "New case study", score: "79" },
  { name: "Lumen Works", type: "Direct client", signal: "Growth signal", score: "74" },
];

export function HomePage() {
  return (
    <div className="home-page">
      <header className="home-nav">
        <Link className="home-brand" to="/" aria-label="Vyze home">
          <span className="home-brand-mark" aria-hidden="true">V</span>
          <span>Vyze</span>
        </Link>
        <nav aria-label="Home navigation">
          <a href="#how-it-works">How it works</a>
          <a href="#workflows">Workflows</a>
          <a href="#principles">Principles</a>
        </nav>
        <Link className="button button-dark" to="/workspace">Open workspace</Link>
      </header>

      <main>
        <section className="home-hero">
          <div className="hero-copy">
            <p className="eyebrow">Your local opportunity engine</p>
            <h1>Find the right work. Know why it matters.</h1>
            <p>
              Vyze brings companies, roles, market signals, contacts, and follow-ups into one
              evidence-led workspace—without handing your pipeline to a hosted platform.
            </p>
            <div className="hero-actions">
              <Link className="button button-dark" to="/workspace">Open workspace</Link>
              <a className="button button-outline" href="#how-it-works">See how it works</a>
            </div>
          </div>

          <div className="product-frame" aria-label="Illustrative Vyze opportunity workspace">
            <div className="product-bar">
              <span className="product-wordmark">Vyze</span>
              <span className="product-search">Search companies and opportunities…</span>
              <span className="product-avatar">ID</span>
            </div>
            <div className="product-body">
              <div className="product-sidebar" aria-hidden="true">
                <span className="selected">Overview</span>
                <span>Opportunities</span>
                <span>Companies</span>
                <span>Outreach</span>
              </div>
              <div className="product-content">
                <div className="product-heading">
                  <div><small>Today</small><strong>Opportunity inbox</strong></div>
                  <span className="mini-pill">3 newly ranked</span>
                </div>
                <div className="product-stats">
                  <div><small>High confidence</small><strong>12</strong></div>
                  <div><small>Follow-ups due</small><strong>4</strong></div>
                  <div className="dark"><small>Ready to review</small><strong>7</strong></div>
                </div>
                <div className="product-table">
                  <div className="product-row product-labels">
                    <span>Company</span><span>Opportunity</span><span>Signal</span><span>Score</span>
                  </div>
                  {opportunities.map((item) => (
                    <div className="product-row" key={item.name}>
                      <strong>{item.name}</strong><span>{item.type}</span>
                      <span><i />{item.signal}</span><b>{item.score}</b>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="home-intro" id="how-it-works">
          <p className="eyebrow">One considered system</p>
          <h2>From scattered public evidence to a focused next move.</h2>
          <p>
            Vyze is designed to make opportunity research cumulative. Every company can connect
            to roles, signals, contacts, scoring reasons, drafts, and activity history.
          </p>
        </section>

        <section className="workflow-grid" id="workflows">
          <article>
            <span>01</span>
            <h3>Discover across three paths</h3>
            <p>Track startup roles, agency partnerships, and direct-client needs without forcing them into one generic pipeline.</p>
          </article>
          <article className="inverted">
            <span>02</span>
            <h3>Rank with visible evidence</h3>
            <p>Separate missing evidence from negative evidence, and see the reasons behind every opportunity score.</p>
          </article>
          <article>
            <span>03</span>
            <h3>Build relationships deliberately</h3>
            <p>Research public contacts, prepare editable outreach, and record follow-ups while keeping every send under your control.</p>
          </article>
        </section>

        <section className="principles-section" id="principles">
          <div>
            <p className="eyebrow">Quiet infrastructure</p>
            <h2>Your research stays local. Your judgment stays central.</h2>
          </div>
          <ul>
            <li><strong>Local first</strong><span>PostgreSQL and both app servers run on your machine.</span></li>
            <li><strong>Evidence first</strong><span>Sources, timestamps, confidence, and unknowns remain visible.</span></li>
            <li><strong>Human first</strong><span>Vyze assists with qualification and drafting; you make the final call.</span></li>
          </ul>
        </section>

        <section className="home-cta">
          <p className="eyebrow">The workspace is ready</p>
          <h2>Build a pipeline you can actually explain.</h2>
          <Link className="button button-light" to="/workspace">Enter Vyze</Link>
        </section>
      </main>

      <footer className="home-footer">
        <span>Vyze</span>
        <p>Local-first opportunity discovery and relationship management.</p>
      </footer>
    </div>
  );
}
