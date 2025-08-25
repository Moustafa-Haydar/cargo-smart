import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './Pages/Login/LoginPage';

import './Styles/index.css';
import './Styles/style.css';
import './Styles/variables.css';

function App() {
  return (
    <Router>
      <Routes>

        {/* Public Routes */}
        <Route path="/" element={<Login />} />

      </Routes>
    </Router>
  );
}

export default App;
