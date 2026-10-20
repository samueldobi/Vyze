import { Link } from "react-router-dom";

export function ContactPage() {
  return (
    <main className="contact-page">
      <Link className="contact-brand" to="/" aria-label="Back to Vyze home">Vyze</Link>
      <div className="contact-content">
        <p className="eyebrow">Contact Vyze</p>
        <h1>Let&apos;s start a conversation.</h1>
        <p>The contact form and direct contact details will be added here next.</p>
        <Link className="cta-button" to="/">
          Back to home <span aria-hidden="true">←</span>
        </Link>
      </div>
    </main>
  );
}
