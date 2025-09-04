// import { createContext, useState } from "react";

// // Token Provider
// // store a user's auth token
// // provide access to it across the app
// // allow updates (e.g., login, logout)

// export const TokenContext = createContext();

// const TokenProvider = ({ children }) => {
//     const [tokenState, setTokenState] = useState(
//         localStorage.getItem('token') || null);

//     const saveToken = (newToken) => {
//         setTokenState(newToken);
//         localStorage.setItem('token', newToken);
//     };

//     const clearToken = () => {
//         setTokenState(null);
//         localStorage.removeItem('token');
//     };

//     return (
//         <TokenContext.Provider value={{ tokenState, saveToken, clearToken }}>
//             {children}
//         </TokenContext.Provider>
//     );
// };

// export default TokenProvider;


