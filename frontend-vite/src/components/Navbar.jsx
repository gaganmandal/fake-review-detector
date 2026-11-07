import { NavLink } from "react-router-dom";

export default function Navbar() {
  return (
    <div
      className="
      sticky top-0 z-50
      bg-white/70 backdrop-blur-xl
      border-b border-gray-200
      px-10 py-4 flex justify-between items-center
    "
    >
      {/* LOGO */}
      <h1 className="text-lg font-semibold tracking-tight">ReviewGuard</h1>

      {/* NAV ITEMS */}
      <div className="flex items-center gap-4">
        <NavLink
          to="/"
          end
          onClick={() => {
            localStorage.removeItem("predictResult");
            localStorage.removeItem("reviewsData");
          }}
          className={({ isActive }) =>
            `nav-item ${isActive ? "nav-active" : ""}`
          }
        >
          Home
        </NavLink>

        <NavLink
          to="/predict"
          className={({ isActive }) =>
            `nav-item ${isActive ? "nav-active" : ""}`
          }
        >
          Predict
        </NavLink>

        <NavLink
          to="/models"
          className={({ isActive }) =>
            `nav-item ${isActive ? "nav-active" : ""}`
          }
        >
          Models
        </NavLink>

        <NavLink
          to="/reviews"
          className={({ isActive }) =>
            `nav-item ${isActive ? "nav-active" : ""}`
          }
        >
          Reviews
        </NavLink>

        <NavLink
          to="/about"
          className={({ isActive }) =>
            `nav-item ${isActive ? "nav-active" : ""}`
          }
        >
          About
        </NavLink>

        {/* 🔥 FIXED LOGOUT */}
        <NavLink
          to="/login"
          className={({ isActive }) =>
            `nav-item text-red-500 ${isActive ? "nav-active" : ""}`
          }
        >
          Logout
        </NavLink>
      </div>
    </div>
  );
}
