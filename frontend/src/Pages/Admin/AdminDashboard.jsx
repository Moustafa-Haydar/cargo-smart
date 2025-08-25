import React, { useEffect, useState, useContext } from "react";
import { TokenContext } from '../../Contexts/TokenContexts';
import { useNavigate } from 'react-router-dom';
import AdminController from "../../Controllers/Admin/AdminController";
import Button from '../../Components/Button/Button';
import './style.css';

function AdminDashboard() {
  const [users, setUsers] = useState([]);
  const { tokenState, clearToken } = useContext(TokenContext);
  const [filteredUsers, setFilteredUsers] = useState([]);
  const [roleFilter, setRoleFilter] = useState("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [showModal, setShowModal] = useState(false);
  const [newUser, setNewUser] = useState({ name: "", email: "", role: "manager" });
  const navigate = useNavigate();

  // Fetch all users
  useEffect(() => {
    const fetchUsers = async () => {
        const allUsers = await AdminController.getAllUsers(tokenState);
        setUsers(allUsers);
        setFilteredUsers(allUsers);
    };
    fetchUsers();
    }, [tokenState]);

  // Filter users based on role and search query
  useEffect(() => {
    let filtered = users;

    if (roleFilter !== "all") {
      filtered = filtered.filter((user) => user.role === roleFilter);
    }

    if (searchQuery.trim()) {
      filtered = filtered.filter((user) =>
        user.name.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    setFilteredUsers(filtered);
  }, [roleFilter, searchQuery, users]);

  // Handle adding a new user
  const handleAddUser = async () => {
    if (!newUser.first_name || !newUser.last_name || !newUser.email || !newUser.username || !newUser.password || !newUser.role) return;
    const id = users.length + 1;
    setUsers([...users, { ...newUser, id }]);
    await AdminController.addUser(newUser, tokenState);
    setShowModal(false);
    setNewUser({ name: "", email: "", role: "manager" });
    return null;
  };

  const logout = () => {
    clearToken();
    navigate('/');
  }
    

  return (
    <main className="admin-dashboard">
      <header className="dashboard-header">
        <h1 className="dashboard-title">Admin Dashboard</h1>
        <div className="admin-actions">

          <Button btn_name="+ Add User" onClick={() => setShowModal(true)} type="primary" />
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

        <select
          value={roleFilter}
          onChange={(e) => setRoleFilter(e.target.value)}
          className="filter-select"
        >
          <option value="all">All Roles</option>
          <option value="admin">Admin</option>
          <option value="manager">Manager</option>
          <option value="driver">Driver</option>
        </select>
      </section>

      <section className="user-list">
        {filteredUsers.length === 0 ? (
          <p className="no-users">No users found.</p>
        ) : (
          <table className="user-table">
            <thead>
              <tr>
                <th>First-Name</th>
                <th>First-Name</th>
                <th>Email</th>
                <th>Username</th>
                <th>Role</th>
              </tr>
            </thead>
            <tbody>
              {filteredUsers.map((user) => (
                <tr key={user.id}>
                  <td>{user.first_name}</td>
                  <td>{user.last_name}</td>
                  <td>{user.email}</td>
                  <td>{user.username}</td>
                  <td>{user.role}</td>
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
            <h2>Add New User</h2>

            <input
              type="text"
              placeholder="First Name"
              value={newUser.first_name}
              onChange={(e) => setNewUser({ ...newUser, first_name: e.target.value })}
              className="modal-input"
            />

            <input
              type="text"
              placeholder="Last Name"
              value={newUser.last_name}
              onChange={(e) => setNewUser({ ...newUser, last_name: e.target.value })}
              className="modal-input"
            />

            <input
              type="email"
              placeholder="Email"
              value={newUser.email}
              onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
              className="modal-input"
            />

            <input
              type="text"
              placeholder="Username"
              value={newUser.username}
              onChange={(e) => setNewUser({ ...newUser, username: e.target.value })}
              className="modal-input"
            />

            <input
              type="password"
              placeholder="Password"
              value={newUser.password}
              onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
              className="modal-input"
            />

            <select
              value={newUser.role}
              onChange={(e) => setNewUser({ ...newUser, role: e.target.value })}
              className="modal-select"
            >
              <option value="admin">Admin</option>
              <option value="manager">Operations Manager</option>
              <option value="driver">Analyst</option>
            </select>

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
  );
}

export default AdminDashboard;
