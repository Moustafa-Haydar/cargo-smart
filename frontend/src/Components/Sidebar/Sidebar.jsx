import React from "react";
import { NavLink } from "react-router-dom";
import "./style.css";
import { useNavigate } from 'react-router-dom';
import logo from '../../Assets/Logo/Cargo-Photoroom.png';


const Sidebar = () => {
    const navigate = useNavigate();

    const linkClass = ({ isActive }) =>
        "sidebar__link" + (isActive ? " active" : "");

    return (
        <aside className="sidebar" role="navigation">
            <img src={logo} alt="" className="login-page-logo"/>

            <nav className="sidebar__nav">
                <NavLink to="/AdminDashboard" className={linkClass}>
                <span className="icon" aria-hidden>🏠</span>
                <span className="label">Dashboard</span>
                </NavLink>

                <NavLink to="/Users" className={linkClass}>
                <span className="icon" aria-hidden>👥</span>
                <span className="label">Users</span>
                </NavLink>

                <NavLink to="/Shipments" className={linkClass}>
                <span className="icon" aria-hidden>📦</span>
                <span className="label">Shipments</span>
                </NavLink>

                <NavLink to="/Reports" className={linkClass}>
                <span className="icon" aria-hidden>📊</span>
                <span className="label">Reports</span>
                </NavLink>
            </nav>
        </aside>
    );
};

export default Sidebar;
