import { useLayoutEffect, useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { Link } from "react-router-dom";

const opportunities = [
  { name: "Northstar Labs", type: "Startup role", signal: "Hiring", score: "86" },
  { name: "Fieldwork Studio", type: "Agency partner", signal: "New case study", score: "79" },
  { name: "Lumen Works", type: "Direct client", signal: "Growth signal", score: "74" },
];

export function HomePage() {
  const pageRef = useRef<HTMLDivElement>(null);
  const heroRef = useRef<HTMLElement>(null);
  const stageRef = useRef<HTMLDivElement>(null);
  const copyRef = useRef<HTMLDivElement>(null);
  const productRef = useRef<HTMLDivElement>(null);
  const stackRef = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    if (!window.matchMedia || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    gsap.registerPlugin(ScrollTrigger);
    const context = gsap.context(() => {
      const media = gsap.matchMedia();
      media.add("(min-width: 769px)", () => {
        gsap.set(productRef.current, { scale: 0.58, y: 190, transformOrigin: "center center" });
        const timeline = gsap.timeline({
          scrollTrigger: {
            trigger: heroRef.current,
            start: "top top",
            end: "bottom bottom",
            pin: stageRef.current,
            scrub: 1,
            anticipatePin: 1,
          },
        });
        timeline
          .to(copyRef.current, { opacity: 0, y: -80, duration: 0.35 }, 0)
          .to(productRef.current, { scale: 1.04, y: 0, duration: 1, ease: "none" }, 0)
          .to(".hero-orbit", { scale: 1.45, opacity: 0.7, duration: 1, ease: "none" }, 0);

        const panels = gsap.utils.toArray<HTMLElement>(".stack-panel", stackRef.current);
        panels.slice(0, -1).forEach((panel, index) => {
          gsap.to(panel, {
            scale: 0.94,
            opacity: 0.58,
            ease: "none",
            scrollTrigger: {
              trigger: panels[index + 1],
              start: "top bottom",
              end: "top top",
              scrub: true,
            },
          });
        });
      });
      return () => media.revert();
    }, pageRef);

    return () => context.revert();
  }, []);

  return (
    <div className="home-page" ref={pageRef}>
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
        <section className="home-hero-scroll" ref={heroRef}>
          <div className="home-hero-stage" ref={stageRef}>
            <div className="hero-orbit" aria-hidden="true" />
            <div className="hero-copy" ref={copyRef}>
              <p className="eyebrow">Your local opportunity engine</p>
              <h1>Find the right work. Know why it matters.</h1>
              <p>
                One private workspace for companies, roles, signals, relationships, and the next
                move worth making.
              </p>
              <div className="hero-actions">
                <Link className="button button-light" to="/workspace">Open workspace</Link>
                <a className="button button-outline-light" href="#how-it-works">Explore Vyze</a>
              </div>
            </div>

          <div
            className="product-frame"
            ref={productRef}
            aria-label="Illustrative Vyze opportunity workspace"
          >
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
          <p className="scroll-cue" aria-hidden="true">Scroll to enter the workspace <span>↓</span></p>
          </div>
        </section>

        <div className="stacked-sections" ref={stackRef}>
          <section className="stack-panel stack-panel-intro" id="how-it-works">
            <div className="home-intro">
              <p className="eyebrow">One considered system</p>
              <h2>From scattered public evidence to a focused next move.</h2>
              <p>
                Vyze is designed to make opportunity research cumulative. Every company can connect
                to roles, signals, contacts, scoring reasons, drafts, and activity history.
              </p>
            </div>
          </section>

          <section className="stack-panel stack-panel-workflows" id="workflows">
            <div className="workflow-grid">
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
            </div>
          </section>

          <section className="stack-panel stack-panel-principles" id="principles">
            <div className="principles-section">
              <div>
                <p className="eyebrow">Quiet infrastructure</p>
                <h2>Your research stays local. Your judgment stays central.</h2>
              </div>
              <ul>
                <li><strong>Local first</strong><span>PostgreSQL and both app servers run on your machine.</span></li>
                <li><strong>Evidence first</strong><span>Sources, timestamps, confidence, and unknowns remain visible.</span></li>
                <li><strong>Human first</strong><span>Vyze assists with qualification and drafting; you make the final call.</span></li>
              </ul>
            </div>
          </section>

          <section className="stack-panel stack-panel-cta">
            <div className="home-cta">
              <p className="eyebrow">The workspace is ready</p>
              <h2>Build a pipeline you can actually explain.</h2>
              <Link className="button button-light" to="/workspace">Enter Vyze</Link>
            </div>
          </section>
        </div>
      </main>

      <footer className="home-footer">
        <span>Vyze</span>
        <p>Local-first opportunity discovery and relationship management.</p>
      </footer>
    </div>
  );
}
