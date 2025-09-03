import React, { useEffect, useState } from "react";
import Sidebar from "../../../Components/Sidebar/Sidebar";
import GroupController from "../../../Controllers/Groups/GroupController";
import Button from '../../../Components/Button/Button';
import './style.css';
import '../../../Styles/variables.css';

const GroupPage = () => {
    
    const [groups, setGroups] = useState([]);
    const [filteredGroups, setFilteredGroups] = useState([]);
    const [searchQuery, setSearchQuery] = useState("");
    const [showModal, setShowModal] = useState(false);
    const [newGroup, setNewGroup] = useState({ name: "", description: "" });

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
    }, [searchQuery, groups]);

    // Handle adding a new group
    const handleAddGroup = async () => {
        if (!newGroup.name) return;
        const id = groups.length + 1;
        setGroups([...groups, { ...newGroup, id }]);
        await GroupController.addGroup(newGroup);
        setShowModal(false);
        setNewGroup({ name: "", description: "" });
        return null;
    };

    // handle delele groups
    const [ toDeleteGroups, setToDeleteGroups ] = useState([]);
    const addToDeleteList = (group_id) => {

        setToDeleteGroups(prev => {
            const isSelected = prev.includes(group_id);
            const updated = isSelected
                ? prev.filter(id => id !== group_id) :
                [...prev, group_id];

            console.log(updated);
            return updated;
        })
    }
    const deleteGroups = async () => {

        try {

            await Promise.all( 
                toDeleteGroups.map(group_id =>
                    GroupController.deleteGroup(group_id))
            );

            const updatedGroups = groups.filter(
                group => !toDeleteGroups.includes(group.id)
            );
            setGroups(updatedGroups);
            setFilteredGroups(updatedGroups);
            setToDeleteGroups([]);
            console.log("Groups deleted successfully.")

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
            <h1 className="dashboard-title">Manage Groups</h1>
            <div className="admin-actions">
                <Button btn_name="+ Add Group" onClick={() => setShowModal(true)} type="primary" />
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
                        <th></th>
                        <th>Name</th>
                        <th>Description</th>
                        
                    </tr>
                </thead>
                <tbody>
                    {filteredGroups.map((group) => (
                        <tr key={group.id}>
                            <td>
                                <input
                                    type="checkbox"
                                    onChange={() => addToDeleteList(group.id)}
                                />
                            </td>
                            <td>{group.name}</td>
                            <td>{group.description}</td>
                        </tr>
                    ))}

                    <tr>
                        <td colSpan={3} className="deleteBtn">
                            <Button btn_name={"Delete"} type="delete"
                            onClick={deleteGroups}/>
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
                <h2>Add New Group</h2>

                <input
                type="text"
                placeholder="Name"
                value={newGroup.name}
                onChange={(e) => setNewGroup({ ...newGroup, name: e.target.value })}
                className="modal-input"
                />

                <input
                type="text"
                placeholder="Description"
                value={newGroup.description}
                onChange={(e) => setNewGroup({ ...newGroup, description: e.target.value })}
                className="modal-input"
                />

                <div className="modal-actions">
                <button className="modal-cancel" onClick={() => setShowModal(false)}>
                    Cancel
                </button>
                <button className="modal-confirm" onClick={handleAddGroup}>
                    Add Group
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