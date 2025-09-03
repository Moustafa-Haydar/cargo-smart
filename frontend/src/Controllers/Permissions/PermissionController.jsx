import api from "../api";

class PermissionController {

    static async getAllPermissions() {
        try {

            const { data } = await api.get("/accounts/csrf/");
            const csrfToken = data?.csrfToken;

            const res = await api.get(
                "/rbac/permissions/", 
                { 
                    headers: { 
                        "X-CSRFToken": csrfToken } 
                },
            );
            return res.data.permissions;
            
        } catch (error) {
            console.error(error);
            return [];
        }
    }

}


export default PermissionController;