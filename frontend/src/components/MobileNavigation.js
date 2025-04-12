import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './MobileNavigation.css';

const MobileNavigation = ({ onLogout }) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const handleNavClick = () => {
    setIsOpen(false);
  };

  return (
    <div className="mobile-navigation">
      <button 
        className={`hamburger-menu ${isOpen ? 'open' : ''}`} 
        onClick={toggleMenu}
        aria-label="Toggle navigation menu"
      >
        <span></span>
        <span></span>
        <span></span>
      </button>
      
      <div className={`mobile-menu ${isOpen ? 'open' : ''}`}>
        <div className="mobile-menu-header">
          <h2>GradientLab</h2>
          <button 
            className="close-menu" 
            onClick={toggleMenu}
            aria-label="Close navigation menu"
          >
            &times;
          </button>
        </div>
        
        <nav className="mobile-nav">
          <ul>
            <li>
              <Link to="/" onClick={handleNavClick}>
                <span className="nav-icon">🏠</span>
                Dashboard
              </Link>
            </li>
            <li>
              <Link to="/analytics" onClick={handleNavClick}>
                <span className="nav-icon">📊</span>
                Analytics
              </Link>
            </li>
            <li>
              <Link to="/profile" onClick={handleNavClick}>
                <span className="nav-icon">👤</span>
                Profile
              </Link>
            </li>
            <li>
              <Link to="/settings" onClick={handleNavClick}>
                <span className="nav-icon">⚙️</span>
                Settings
              </Link>
            </li>
            <li>
              <button onClick={() => { handleNavClick(); onLogout(); }}>
                <span className="nav-icon">🚪</span>
                Logout
              </button>
            </li>
          </ul>
        </nav>
      </div>
      
      {isOpen && <div className="menu-backdrop" onClick={toggleMenu}></div>}
    </div>
  );
};

export default MobileNavigation;
