import axios from "axios";

class AuthController {

    static async login({ user }) {

        try {
            const response = await axios
            .post("http://localhost:8000/api/v0.1/auth/login", user);

            return response.data.payload;               

        } catch (error) {
            const message ="Login failed. Please try again.";
            console.log(error.response.data);
            throw new Error(message);
        }
    }

    static async sendResetLink({ username }) {

        try {
            const response = await axios
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