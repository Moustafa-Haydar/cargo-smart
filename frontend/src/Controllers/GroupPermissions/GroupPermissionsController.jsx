import api from "../api";

class GroupPermissionsController {

    static async getGroupPermissions(group_id) {
        try {

            const { data } = await api.get("/accounts/csrf/");
            const csrfToken = data?.csrfToken;

            const res = await api.get(
                `/rbac/groups/${group_id}/permissions/`, 
                { 
                    headers: { 
                        "X-CSRFToken": csrfToken } 
                },
            );
            return res.data;
            
        } catch (error) {
            console.error(error);
            return [];
        }
    }

    static async setGroupPermissions(group_id, permission_ids) {
        try {

            const { data } = await api.get("/accounts/csrf/");
            const csrfToken = data?.csrfToken;

            const res = await api.post(
                `/rbac/groups/${group_id}/permissions/`, 
                {
                    "permission_ids" : permission_ids
                },
                { 
                    headers: { 
                        "X-CSRFToken": csrfToken } 
                },
            );
            return res.data;
            
        } catch (error) {
            console.error(error);
            return [];
        }
    }

}

export default GroupPermissionsController;