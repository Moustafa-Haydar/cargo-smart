import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './Pages/Common/Login/LoginPage';

import UserPage from './Pages/Admin/UserPage/UserPage';
import GroupPage from './Pages/Admin/GroupPage/GroupPage';
import PermissionPage from './Pages/Admin/PermissionPage/PermissionPage';

import './Styles/index.css';
import './Styles/style.css';
import './Styles/variables.css';

function App() {
  return (
    <Router>
      <Routes>
      

        {/* Public Routes */}
        <Route path="/" element={<Login />} />

        {/* Admin Routes */}
        <Route path="/AdminDashboard" element={<UserPage />} />
        <Route path="/GroupPage" element={<GroupPage />} />
        <Route path="/PermissionPage" element={<PermissionPage />} />


      </Routes>
    </Router>
  );
}

export default App;
