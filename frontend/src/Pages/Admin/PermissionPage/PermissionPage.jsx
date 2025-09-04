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
            const all = await PermissionController.getAllPermissions();
            setPermissions(all);
            setFilteredPermissions(all);
        };
        fetchPermissions();
    }, []);

    useEffect(() => {

        if (!searchQuery.trim()) {
            setFilteredPermissions(permissions);
        } else {
            const q = searchQuery.toLowerCase();
            setFilteredPermissions(
                permissions.filter(p =>
                (p?.name || "").toLowerCase().includes(q) ||
                (p?.description || "").toLowerCase().includes(q) ||
                (p?.app_label  || "").toLowerCase().includes(q) ||
                (p?.codename  || "").toLowerCase().includes(q)
                )
            )}
        }, [searchQuery, permissions]
    );


    // Handle adding a new group
    const handleAddPermission = async () => {
        if (!newPermission.name || !newPermission.app_label || !newPermission.codename) return;

        try {
            const res = await PermissionController.addPermission(newPermission);
            const added = res.data.permission;
            console.log(added);

            setPermissions(prev => [...prev, added]);

            setShowModal(false);
            setNewPermission({ name: "", description: "", app_label: "", codename: "" });

        } catch ( error) {
            console.error(error);
        }      
    };


    // handle delele groups
    const [ toDeletePermissions, setToDeletePermissions ] = useState([]);
    const addToDeleteList = (permission_id) => {

        setToDeletePermissions(prev => {
            const isSelected = prev.includes(permission_id);
            const updated = isSelected
                ? prev.filter(id => id !== permission_id) :
                [...prev, permission_id];

            console.log(updated);
            return updated;
        })
    }
    const deletePermissions = async () => {

        try {
            await Promise.all( 
                toDeletePermissions.map(permission_id =>
                    PermissionController.deletePermission(permission_id))
            );

            const updatedPermissions = permissions.filter(
                permission => !toDeletePermissions.includes(permission.id)
            );
            setPermissions(updatedPermissions);
            setFilteredPermissions(updatedPermissions);
            setToDeletePermissions([]);
            console.log("Permissions deleted successfully.")

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
            <h1 className="dashboard-title">Manage Permissions</h1>
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
                                <input
                                    type="checkbox"
                                    onChange={() => addToDeleteList(permission.id)}
                                />
                            </td>
                            <td>{permission.name}</td>
                            <td>{permission.app_label}</td>
                            <td>{permission.codename}</td>
                            <td>{permission.description}</td>
                        </tr>
                    ))}

                    <tr>
                        <td colSpan={3} className="deleteBtn">
                            <Button btn_name={"Delete"} type="delete"
                            onClick={deletePermissions}/>
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
                    {["shipments", "rbac", "alerts", "vehicles"].map((name) => (
                        <option key={name} value={name}>
                        {name}
                        </option>
                    ))}

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