import api from "../api";

class UserController {

    static async getAllUsers() {
        try {

            const { data } = await api.get("/accounts/csrf/");
            const csrfToken = data?.csrfToken;

            const res = await api.get(
                "/accounts/users/", 
                { 
                    headers: { 
                        "X-CSRFToken": csrfToken } 
                },
            );
            console.log(res.data.users);
            return res.data.users;
            
        } catch (error) {
            console.error(error);
            return [];
        }
    }

    static async addUser(userData) {
        
        return;
    }

    static async deleteUser(user_id) {
        try {

            const { data } = await api.get("/accounts/csrf");
            const csrfToken = data?.csrfToken;

            const res = await api.post(
                "accounts/users/delete/",
                {
                    "user_id": user_id
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

export default UserController;
    

    