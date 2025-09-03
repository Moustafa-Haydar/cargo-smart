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

    static async addPermission(permission) {
        try {

            const { data } = await api.get("/accounts/csrf/");
            const csrfToken = data?.csrfToken;

            const res = await api.post(
                "rbac/permissions/create/",
                permission,
                {
                    headers: {
                        "X-CSRFToken" : csrfToken }
                }
            )
            console.log(res);
            return res;

        } catch (error) {
            console.error(error);
            return;
        }
    }

}


export default PermissionController;