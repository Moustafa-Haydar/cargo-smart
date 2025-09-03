import React, { useEffect, useState } from "react";
import Sidebar from "../../../Components/Sidebar/Sidebar";
import PermissionController from "../../../Controllers/Permissions/PermissionController";
import Button from '../../../Components/Button/Button';
import './style.css';
import '../../../Styles/variables.css';

const PermissionPage = () => {
    
    const [permissions, setPermissions] = useState([]);
    const [filteredPermissions, setFilteredPermissions] = useState([]);
    const [searchQuery, setSearchQuery] = useState("");
    const [showModal, setShowModal] = useState(false);
    const [newPermission, setNewPermission] = useState({ name: "", description: "", app_label: "",  codename: ""});

    // Fetch all permissions
    useEffect(() => {
        const fetchPermissions = async () => {
            const allPermissions = await PermissionController.getAllPermissions();
            setPermissions(allPermissions);
            setFilteredPermissions(allPermissions);
            console.log(allPermissions);
        };
        fetchPermissions();
    }, [setPermissions]);

    // // Filter groups based on search query
    // useEffect(() => {
    // let filtered = groups;

    // if (searchQuery.trim()) {
    //     filtered = filtered.filter((group) =>
    //     group.name.toLowerCase().includes(searchQuery.toLowerCase())
    //     );
    // }

    // setFilteredGroups(filtered);
    // }, [searchQuery, groups]);


    // Handle adding a new group
    const handleAddPermission = async () => {
        if (!newPermission.name || !newPermission.app_label || !newPermission.codename) return;
        const res = await PermissionController.addPermission(newPermission);
        const addedPermission = res.data.permission;
        console.log(addedPermission);
        const updatedPermissions = [...permissions, addedPermission];
        setPermissions(updatedPermissions);
        setFilteredPermissions(updatedPermissions);

        setShowModal(false);
        setNewPermission({ name: "", description: "", app_label: "", codename: "" });
        return null;
    };


    // handle delele groups
    // const [ toDeleteGroups, setToDeleteGroups ] = useState([]);
    // const addToDeleteList = (group_id) => {

    //     setToDeleteGroups(prev => {
    //         const isSelected = prev.includes(group_id);
    //         const updated = isSelected
    //             ? prev.filter(id => id !== group_id) :
    //             [...prev, group_id];

    //         console.log(updated);
    //         return updated;
    //     })
    // }
    // const deleteGroups = async () => {

    //     try {

    //         await Promise.all( 
    //             toDeleteGroups.map(group_id =>
    //                 GroupController.deleteGroup(group_id))
    //         );

    //         const updatedGroups = groups.filter(
    //             group => !toDeleteGroups.includes(group.id)
    //         );
    //         setGroups(updatedGroups);
    //         setFilteredGroups(updatedGroups);
    //         setToDeleteGroups([]);
    //         console.log("Groups deleted successfully.")

    //     } catch (error) {
    //         console.error(error);
    //         return;
    //     }
    // }


    return (
    <div className="main-dashboard">
        <Sidebar/>
        <main className="admin-dashboard">
        <header className="dashboard-header">
            <h1 className="dashboard-title">Manage Groups</h1>
            <div className="admin-actions">
            <Button btn_name="+ Add Permission" onClick={() => setShowModal(true)} type="primary" />
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
            {filteredPermissions.length === 0 ? (
            <p className="no-groups">No permissions found.</p>
            ) : (
            <table className="user-table">
                <thead>
                    <tr>
                        <th></th>
                        <th>Name</th>
                        <th>App_Label</th>
                        <th>Codename</th>
                        <th>Description</th>
                        
                    </tr>
                </thead>
                <tbody>
                    {filteredPermissions.map((permission) => (
                        <tr key={permission.id}>
                            <td>
                                {/* <input
                                    type="checkbox"
                                    onChange={() => addToDeleteList(group.id)}
                                /> */}
                            </td>
                            <td>{permission.name}</td>
                            <td>{permission.app_label}</td>
                            <td>{permission.codename}</td>
                            <td>{permission.description}</td>
                        </tr>
                    ))}

                    <tr>
                        <td colSpan={3} className="deleteBtn">
                            {/* <Button btn_name={"Delete"} type="delete"
                            onClick={deleteGroups}/> */}
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
                <h2>Add New Permission</h2>

                <input
                type="text"
                placeholder="Name"
                value={newPermission.name}
                onChange={(e) => setNewPermission({ ...newPermission, name: e.target.value })}
                className="modal-input"
                />

                <select
                    value={newPermission.app_label}
                    onChange={(e) => setNewPermission({ ...newPermission, app_label: e.target.value })}
                    className="modal-select"
                >
                    <option value="">Select App_Name</option>
                    <option value={(e) => e.name.toLowerCase()}>shipments</option>
                    <option value={(e) => e.name.toLowerCase()}>rbac</option>
                    <option value={(e) => e.name.toLowerCase()}>alerts</option>
                    <option value={(e) => e.name.toLowerCase()}>vehicles</option>

                </select>

                <input
                type="text"
                placeholder="codename"
                value={newPermission.codename}
                onChange={(e) => setNewPermission({ ...newPermission, codename: e.target.value })}
                className="modal-input"
                />

                <input
                type="text"
                placeholder="Description"
                value={newPermission.description}
                onChange={(e) => setNewPermission({ ...newPermission, description: e.target.value })}
                className="modal-input"
                />

                <div className="modal-actions">
                <button className="modal-cancel" onClick={() => setShowModal(false)}>
                    Cancel
                </button>
                <button className="modal-confirm" onClick={handleAddPermission}>
                    Add Permission
                </button>
                </div>
            </div>
            </div>
        )}
        </main>
    </div>
    );

}

export default PermissionPage;