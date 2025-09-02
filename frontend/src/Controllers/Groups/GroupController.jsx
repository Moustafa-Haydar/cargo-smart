import api from "../api";

class GroupController {

    static async getAllGroups() {
        try {

            const { data } = await api.get("/accounts/csrf/");
            const csrfToken = data?.csrfToken;

            const res = await api.get(
                "/rbac/groups/", 
                { 
                    headers: { 
                        "X-CSRFToken": csrfToken } 
                },
            );
            console.log(res.data.groups);
            return res.data.groups;
            
        } catch (error) {
            console.error(error);
            return [];
        }
    }

}

export default GroupController;