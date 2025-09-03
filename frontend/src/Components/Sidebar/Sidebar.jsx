import React from "react";
import { NavLink } from "react-router-dom";
import "./style.css";
import logo from '../../Assets/Logo/Cargo-Photoroom.png';
import AuthController from "../../Controllers/Common/AuthController";
import { useNavigate } from 'react-router-dom';
import Button from '../../Components/Button/Button';


const Sidebar = () => {

    const navigate = useNavigate();

    const linkClass = ({ isActive }) =>
        "sidebar__link" + (isActive ? " active" : "");

    const logout = () => {
        AuthController.logout();
        navigate("/");
    }

    return (
        <aside className="sidebar" role="navigation">
            <img src={logo} alt="" className="login-page-logo"/>

            <nav className="sidebar__nav">
                <NavLink to="/AdminDashboard" className={linkClass}>
                    <span className="icon" aria-hidden>👥</span>
                    <span className="label">UserDashboard</span>
                </NavLink>

                <NavLink to="/GroupPage" className={linkClass}>
                    <span className="icon" aria-hidden>👥</span>
                    <span className="label">GroupPage</span>
                </NavLink>

                <NavLink to="/PermissionPage" className={linkClass}>
                    <span className="icon" aria-hidden>📦</span>
                    <span className="label">PermissionPage</span>
                </NavLink>

                <NavLink to="/Reports" className={linkClass}>
                    <span className="icon" aria-hidden>📊</span>
                    <span className="label">Reports</span>
                </NavLink>
            </nav>

            <div className="deleteBtn">
                <Button btn_name="Logout" onClick={() => logout()} type="secondary" className="logout-btn" />
            </div>
            
        </aside>
    );
};

export default Sidebar;
