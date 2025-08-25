import axios from "axios";

class AuthController {

    static async login({ user, saveToken, navigate, url}) {

         try {

            const response = await axios
            .post("http://localhost:8000/api/v0.1/auth/login", user);

            const user_token = response.data.payload.token;               
            saveToken(user_token);
            navigate(url);

        } catch (error) {
            const message ="Login failed. Please try again.";
            console.log(error.response.data);
            throw new Error(message);
        }
    }
}

export default AuthController;