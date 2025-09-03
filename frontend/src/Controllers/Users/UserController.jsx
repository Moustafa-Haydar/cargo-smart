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
            return res.data.users;
            
        } catch (error) {
            console.error(error);
            return [];
        }
    }

    static async addUser(user) {
        try {

            const { data } = await api.get("/accounts/csrf");
            const csrfToken = data?.csrfToken;

            console.log(user);

            const res = await api.post(
                "accounts/users/create/",
                user,
                {
                    headers: {
                        "X-CSRFToken" : csrfToken
                    }
                }
            )
            console.log(res);
            return res;

        } catch (error) {
            console.error(error);
            return;
        }
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
    

    