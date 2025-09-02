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

    static async addGroup(group) {
        try {

            const { data } = await api.get("/accounts/csrf/");
            const csrfToken = data?.csrfToken;

            const res = await api.post(
                "rbac/groups/create/",
                group,
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

    static async deleteGroup(group_id) {
        try {

            const { data } = await api.get("/accounts/csrf");
            const csrfToken = data?.csrfToken;

            const res = await api.post(
                "rbac/groups/delete/",
                {
                    "group_id": group_id
                },
                {
                    headers: {
                        "X-CSRFToken" : csrfToken
                    }
                }
            )
            console.log(res);
            return res;

        } catch (error) {
            console.error(error.message);
            return;
        }
    }
}

export default GroupController;