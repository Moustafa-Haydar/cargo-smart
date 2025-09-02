import api from "../api";

class UserController {

    static async getAllUsers(token) {
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

    static async addUser(userData, token) {
        
        return;
    }

}

export default UserController;
    

    