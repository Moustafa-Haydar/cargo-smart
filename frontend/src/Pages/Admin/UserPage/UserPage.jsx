import React, { useEffect, useState } from "react";
import { useNavigate } from 'react-router-dom';
import UserController from "../../../Controllers/Users/UserController";
import GroupController from "../../../Controllers/Groups/GroupController";
import AuthController from "../../../Controllers/Common/AuthController";
import Button from '../../../Components/Button/Button';
import './style.css';
import '../../../Styles/variables.css';
import Sidebar from "../../../Components/Sidebar/Sidebar";

const UserPage = () => {

  const [users, setUsers] = useState([]);
  const [filteredUsers, setFilteredUsers] = useState([]);

  const [groupsList, setGroupsList] = useState([]);
  const [groupFilter, setGroupFilter] = useState("all");

  const [searchQuery, setSearchQuery] = useState("");

  const [showModal, setShowModal] = useState(false);
  const [newUser, setNewUser] = useState({ first_name: "", last_name:"", email: "", username:"", password:"", group: "" });
  
  const navigate = useNavigate();

  // Fetch all users
  useEffect(() => {
    const fetchUsers = async () => {
      const allUsers = await UserController.getAllUsers();
      setUsers(allUsers);
      setFilteredUsers(allUsers);
    };
    fetchUsers();
    }, []);

  // Fetch all groups
  useEffect(() => {
    const fetchGroups = async () => {
      const allGroups = await GroupController.getAllGroups();
      console.log(allGroups);
      setGroupsList(allGroups);
    };
    fetchGroups();
  }, []);

  // Filter users based on role and search query
  // useEffect(() => {
  //   let filtered = [...users];

  //   if (groupFilter !== "all") {
  //     filtered = filtered.filter((user) => 
  //       user.groups[0].name === groupFilter
  //   );
  //   }

  //   if (searchQuery.trim()) {
  //     filtered = filtered.filter((user) =>
  //       user.first_name.toLowerCase().includes(searchQuery.toLowerCase())
  //     );
  //   }

  //   setFilteredUsers(filtered);
  // }, [groupFilter, searchQuery, users]);

  // Handle adding a new user
  const handleAddUser = async () => {
    if (!newUser.first_name || !newUser.last_name || !newUser.email || !newUser.username || !newUser.password || !newUser.group) return;
    const id = users.length + 1;
    console.log(newUser);
    setUsers([...users, { ...newUser, id }]);
    await UserController.addUser(newUser);
    setShowModal(false);
    setNewUser({ first_name: "", last_name: "", username: "", password: "", email: "", group: "" });
    return null;
  };

  const logout = () => {
    AuthController.logout();
    navigate("/");
  }

  // handle delele users
    const [ toDeleteUsers, setToDeleteUsers ] = useState([]);
    const addToDeleteList = (user_id) => {

        setToDeleteUsers(prev => {
            const isSelected = prev.includes(user_id);
            const updated = isSelected
                ? prev.filter(id => id !== user_id) :
                [...prev, user_id];

            console.log(updated);
            return updated;
        })
    }
    const deleteUsers = async () => {

        try {

            await Promise.all( 
                toDeleteUsers.map(user_id =>
                    UserController.deleteUser(user_id))
            );

            const updatedUsers = users.filter(
                user => !toDeleteUsers.includes(user.id)
            );
            setUsers(updatedUsers);
            setFilteredUsers(updatedUsers);
            setToDeleteUsers([]);
            console.log("Users deleted successfully.")

        } catch (error) {
            console.error(error);
            return;
        }
    }


  return (
    <div className="main-dashboard">
      <Sidebar/>
      <main className="admin-dashboard">
        <header className="dashboard-header">
          <h1 className="dashboard-title">Manage Users</h1>
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
            value={groupFilter}
            onChange={(e) => setGroupFilter(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Roles</option>
            <option value="Admin">Admin</option>
            <option value="Ops Manager">Ops Manager</option>
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
                  <th></th>
                  <th>First-Name</th>
                  <th>Last-Name</th>
                  <th>Username</th>
                  <th>Email</th>
                  <th>Group</th>
                </tr>
              </thead>
              <tbody>
                {filteredUsers.map((user) => (
                  <tr key={user.id}>
                    <td>
                      <input
                          type="checkbox"
                          onChange={() => addToDeleteList(user.id)}
                      />
                    </td>
                    <td>{user.first_name}</td>
                    <td>{user.last_name}</td>
                    <td>{user.username}</td>
                    <td>{user.email}</td>
                    <td>{user.groups[0].name}</td>
                  </tr>
                ))}

                <tr>
                        <td colSpan={3} className="deleteBtn">
                            <Button btn_name={"Delete"} type="delete"
                            onClick={deleteUsers}/>
                        </td>
                    </tr>
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
                value={newUser.group}
                onChange={(e) => setNewUser({ ...newUser, group: e.target.value })}
                className="modal-select"
              >
                <option value="">Select Group</option>
                {groupsList.map(g => (
                  <option key={g.id} value={g.name.toLowerCase()}>{g.name}</option>
                ))}

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
    </div>
  );

}
 

export default UserPage;
