import api from "../api";

class AuthController {

    static async login({ user }) {
        try {
            const { data } = await api.get("/accounts/csrf/");
            const csrfToken = data?.csrfToken;

            const res = await api.post(
                "/accounts/login/", 
                user,
                { 
                    headers: { 
                        "X-CSRFToken": csrfToken } 
                },
            );
            return res.data.user;
        
        } catch (error) {
            console.log(error?.response?.data);
            throw new Error("Login failed. Please try again.");
        }
    }

    static async logout() {

        try {
            const { data } = await api.get("/accounts/csrf/");
            const csrfToken = data?.csrfToken;

            const res = await api.post(
                "/accounts/logout/", 
                {},
                { 
                    headers: { 
                        "X-CSRFToken": csrfToken } 
                },
            );
            console.log(res);
            return res;
        
        } catch (error) {
            console.log(error?.response?.data);
            throw new Error("Logout failed.");
        }
    }

}

export default AuthController;