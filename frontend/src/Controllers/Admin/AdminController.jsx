import axios from "axios";
const BASE_URL = "http://localhost:8000/api/v0.1/admin";

class AdminController {

    static async getAllUsers(token) {
        try {

            const response = await axios.get(`${BASE_URL}/getAllUsers`,
                {
                    headers: {
                    Authorization: `Bearer ${token}`,
                },
                }
            );
            const users = (await response).data.payload;
            return users;
            
        } catch (error) {
            console.error(error);
            return [];
        }
    }

    static async addUser(userData, token) {
        try {
            const response = await axios.post(`${BASE_URL}/addUser`, userData, 
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            return response.data;

        } catch (error) {
            console.error("Error adding user:", error);
        }
    }

}

export default AdminController;
    

    