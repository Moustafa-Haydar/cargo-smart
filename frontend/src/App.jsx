import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './Pages/Common/Login/LoginPage';
import AdminDashboard from './Pages/Admin/AdminDashboard';

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
        <Route path="/AdminDashboard" element={<AdminDashboard />} />



      </Routes>
    </Router>
  );
}

export default App;
