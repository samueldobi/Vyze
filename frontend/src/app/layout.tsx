import { Link, NavLink, Outlet } from "react-router-dom";

const navigation = [
  { to: "/workspace", label: "Overview", end: true },
  { to: "/workspace/companies", label: "Companies", end: false },
];

export function AppLayout() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <Link className="brand" to="/" aria-label="Vyze home">
          <span className="brand-mark" aria-hidden="true">V</span>
          <span>Vyze</span>
        </Link>
        <nav aria-label="Primary navigation">
          {navigation.map((item) => (
            <NavLink
              className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}
              end={item.end}
              key={item.to}
              to={item.to}
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
        <p className="local-note">Local workspace</p>
      </aside>
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
}
