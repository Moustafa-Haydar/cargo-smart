import React, { useEffect, useState } from "react";
import Sidebar from "../../../Components/Sidebar/Sidebar";
import GroupController from "../../../Controllers/Groups/GroupController";
import PermissionController from "../../../Controllers/Permissions/PermissionController";
import GroupPermissionsController from "../../../Controllers/GroupPermissions/GroupPermissionsController";
import Button from '../../../Components/Button/Button';
import './style.css';
import '../../../Styles/variables.css';

const GroupPermissionsPage = () => {
    
    const [groups, setGroups] = useState([]);
    const [selectedGroupId, setSelectedGroupId] = useState("");
    const [groupPermissions, setGroupPermissions] = useState([]);
    const [allPermissions, setAllPermissions] = useState([]);
    const [newPermissionId, setNewPermissionId] = useState("");

    // Fetch groups + all permissions on mount
    useEffect(() => {
        const fetchData = async () => {
            try {
                const g = await GroupController.getAllGroups();
                const p = await PermissionController.getAllPermissions();
                setGroups(g);
                setAllPermissions(p);
            } catch (e) {
                console.log(e);
            }
        };
        fetchData();
    }, []);

    // Fetch permissions for selected group
    useEffect(() => {
        const fetchGroupPermissions = async () => {
            try {
                if (!selectedGroupId) return;
                const perms = await GroupPermissionsController.getGroupPermissions(selectedGroupId);
                setGroupPermissions(perms.permissions);
                console.log(perms.permissions);
            } catch (error) {
                console.log(error);
            }
        };
        fetchGroupPermissions();
    }, [selectedGroupId]);

    const handleAddPermission = () => {
        if (!newPermissionId) return;
        console.log(newPermissionId);
        const perm = allPermissions.find(p => p.id === newPermissionId);
        if (perm && !groupPermissions.some(p => p.id === perm.id)) {
            setGroupPermissions(prev => [...prev, perm]);
            setNewPermissionId("");
        }
    };

    const handleRemovePermission = (id) => {
        if (!id) return;
        console.log(id);
        setGroupPermissions(prev => prev.filter(p => p.id !== id));
    };

    const handleSave = async () => {
        const permission_ids = groupPermissions.map(p => p.id);
        await GroupPermissionsController.setGroupPermissions(selectedGroupId, permission_ids);
    };

    return (
        <div className="main-dashboard">
        <Sidebar />
        <main className="admin-dashboard">
            <header className="dashboard-header">
            <h1 className="dashboard-title">Manage Group Permissions</h1>
            </header>

            <div className="dashboard-header">
                <div className="dashboard-subheader">
                    <section className="filters">
                        <select
                            value={selectedGroupId}
                            onChange={(e) => setSelectedGroupId(e.target.value)}
                            className="filter-select"
                        >
                            <option value="">Select Group</option>
                            {groups.map((g) => (
                            <option key={g.id} value={g.id}>{g.name}</option>
                            ))}
                        </select>
                    </section>

                    <div className="add-permission">
                        <select
                            value={newPermissionId}
                            onChange={(e) => setNewPermissionId(e.target.value)}
                            className="filter-select"
                        >
                            <option value="">Add Permission</option>
                            {allPermissions
                            .filter(p => !groupPermissions.some(gp => gp.id === p.id))
                            .map(p => (
                                <option key={p.id} value={p.id}>{p.description}</option>
                            ))}
                        </select>
                        <Button btn_name="Add" onClick={handleAddPermission} type="primary" />
                    </div>

                </div>
                
                <Button btn_name="Save Changes" onClick={handleSave} type="primary" />
            </div>


            {selectedGroupId && (
            <section className="permissions-section">
                <h2>Assigned Permissions</h2>
                {groupPermissions.length === 0 ? (
                <p>No permissions assigned to this group.</p>
                ) : (
                <ul className="permission-list">
                    {groupPermissions.map((perm) => (
                    <li key={perm.id} className="permission-item">
                        {perm.code}
                        <button onClick={() => handleRemovePermission(perm.id)} className="remove-btn">❌</button>
                    </li>
                    ))}
                </ul>
                )}

                
            </section>
            )}
        </main>
        </div>
    );

}

export default GroupPermissionsPage;