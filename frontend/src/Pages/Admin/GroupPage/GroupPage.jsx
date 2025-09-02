import React, { useEffect, useState } from "react";
import Sidebar from "../../../Components/Sidebar/Sidebar";
import { useNavigate } from 'react-router-dom';
import GroupController from "../../../Controllers/Groups/GroupController";
import AuthController from "../../../Controllers/Common/AuthController";
import Button from '../../../Components/Button/Button';
import './style.css';
import '../../../Styles/variables.css';

const GroupPage = () => {
    
    const [groups, setGroups] = useState([]);
    const [filteredGroups, setFilteredGroups] = useState([]);
    const [searchQuery, setSearchQuery] = useState("");
    const [showModal, setShowModal] = useState(false);
    const [newGroup, setNewGroup] = useState({ name: "", email: "", role: "manager" });
    const navigate = useNavigate();

    // Fetch all groups
    useEffect(() => {
    const fetchGroups = async () => {
        const allGroups = await GroupController.getAllGroups();
        setGroups(allGroups);
        setFilteredGroups(allGroups);
    };
    fetchGroups();
    }, []);

    // Filter groups based on search query
    useEffect(() => {
    let filtered = groups;

    if (searchQuery.trim()) {
        filtered = filtered.filter((group) =>
        group.name.toLowerCase().includes(searchQuery.toLowerCase())
        );
    }

    setFilteredGroups(filtered);
    }, [filteredGroups, searchQuery, groups]);

    // Handle adding a new group
    const handleAddUser = async () => {
    if (!newGroup.first_name) return;
    const id = newGroup.length + 1;
    setGroups([...groups, { ...newGroup, id }]);
    await GroupController.addUser(newGroup);
    setShowModal(false);
    setNewGroup({ name: "", email: "", role: "manager" });
    return null;
    };

    const logout = () => {
    AuthController.logout();
    navigate("/");
    }


    return (
    <div className="main-dashboard">
        <Sidebar/>
        <main className="admin-dashboard">
        <header className="dashboard-header">
            <h1 className="dashboard-title">Manage Groups</h1>
            <div className="admin-actions">

            <Button btn_name="+ Add Group" onClick={() => setShowModal(true)} type="primary" />
            <Button btn_name="Logout" onClick={() => logout()} type="secondary" />

            </div>
        </header>

        <section className="filters">
            <input
            type="text"
            placeholder="Search by name..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="filter-input"
            />
        </section>

        <section className="user-list">
            {filteredGroups.length === 0 ? (
            <p className="no-groups">No groups found.</p>
            ) : (
            <table className="user-table">
                <thead>
                <tr>
                    <th>Name</th>
                    <th>Description</th>
                    
                </tr>
                </thead>
                <tbody>
                {filteredGroups.map((group) => (
                    <tr key={group.id}>
                        <td>{group.name}</td>
                        <td>{group.description}</td>
                    </tr>
                ))}
                </tbody>
            </table>
            )}
        </section>

        {/* Modal */}
        {showModal && (
            <div className="modal-overlay">
            <div className="modal">
                <h2>Add New Group</h2>

                <input
                type="text"
                placeholder="First Name"
                value={newGroup.first_name}
                onChange={(e) => setNewGroup({ ...newGroup, first_name: e.target.value })}
                className="modal-input"
                />

                <input
                type="text"
                placeholder="Last Name"
                value={newGroup.last_name}
                onChange={(e) => setNewGroup({ ...newGroup, last_name: e.target.value })}
                className="modal-input"
                />

                <input
                type="email"
                placeholder="Email"
                value={newGroup.email}
                onChange={(e) => setNewGroup({ ...newGroup, email: e.target.value })}
                className="modal-input"
                />

                {/* <select
                value={newUser.role}
                onChange={(e) => setNewUser({ ...newUser, role: e.target.value })}
                className="modal-select"
                >
                <option value="admin">Admin</option>
                <option value="manager">Operations Manager</option>
                <option value="driver">Analyst</option>
                </select> */}

                <div className="modal-actions">
                <button className="modal-cancel" onClick={() => setShowModal(false)}>
                    Cancel
                </button>
                <button className="modal-confirm" onClick={handleAddUser}>
                    Add User
                </button>
                </div>
            </div>
            </div>
        )}
        </main>
    </div>
    );

}

export default GroupPage;