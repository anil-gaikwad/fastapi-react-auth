import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Dashboard.css';

const Dashboard = () => {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem('user'));

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-content">
        <div className="dashboard-header">
          <img 
            src="/welcome-dashboard.svg" 
            alt="Welcome" 
            className="dashboard-image"
          />
          <h1>Welcome to Your Dashboard</h1>
        </div>
        
        <div className="user-info">
          <div className="info-item">
            <span className="label">Email:</span>
            <span className="value">{user?.email}</span>
          </div>
          <div className="info-item">
            <span className="label">Account Status:</span>
            <span className={`value status ${user?.is_verified ? 'verified' : 'unverified'}`}>
              {user?.is_verified ? 'Verified' : 'Unverified'}
            </span>
          </div>
        </div>

        <button className="logout-button" onClick={handleLogout}>
          Logout
        </button>
      </div>
    </div>
  );
};

export default Dashboard; 