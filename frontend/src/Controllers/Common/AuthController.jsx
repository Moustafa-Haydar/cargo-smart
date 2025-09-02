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

    static async sendResetLink({ username }) {

        try {
            const response = await api
            .post("http://localhost:8000/api/v0.1/auth/forgot-password", { username });
            return response.data.payload;               

        } catch (error) {
            const message ="Failed to send reset link. Please try again.";
            console.log(error.response.data);
            throw new Error(message);
        }
    }
}

export default AuthController;