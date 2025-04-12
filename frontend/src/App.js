import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Switch, Redirect, Link } from 'react-router-dom';
import './App.css';
import './styles/mobile.css';

// Import pages
import Home from './pages/Home';
import Login from './pages/Login';
import Settings from './pages/Settings';
import Profile from './pages/Profile';
import Analytics from './pages/Analytics';

// Import components
import MobileNavigation from './components/MobileNavigation';

// Import auth utilities
import { isAuthenticated, logout } from './api/auth';

// Import contexts
import { ToastProvider } from './contexts/ToastContext';
import { SocketProvider } from './contexts/SocketContext';

function App() {
  const [authenticated, setAuthenticated] = useState(false);

  useEffect(() => {
    // Check if user is authenticated on component mount
    setAuthenticated(isAuthenticated());
  }, []);

  const handleLogout = async () => {
    try {
      await logout();
      setAuthenticated(false);
    } catch (error) {
      console.error('Logout error:', error);
      // Still set authenticated to false even if API call fails
      setAuthenticated(false);
    }
  };

  // Private route component
  const PrivateRoute = ({ component: Component, ...rest }) => (
    <Route
      {...rest}
      render={props =>
        authenticated ? (
          <Component {...props} />
        ) : (
          <Redirect to="/login" />
        )
      }
    />
  );

  return (
    <ToastProvider>
      <SocketProvider>
        <Router basename={process.env.PUBLIC_URL}>
          <div className="App">
            {authenticated && (
              <>
                <nav className="navbar">
                  <div className="navbar-brand">
                    <Link to="/">GradientLab</Link>
                  </div>
                  <ul className="navbar-nav">
                    <li className="nav-item">
                      <Link to="/" className="nav-link">Dashboard</Link>
                    </li>
                    <li className="nav-item">
                      <Link to="/analytics" className="nav-link">Analytics</Link>
                    </li>
                    <li className="nav-item">
                      <Link to="/profile" className="nav-link">Profile</Link>
                    </li>
                    <li className="nav-item">
                      <Link to="/settings" className="nav-link">Settings</Link>
                    </li>
                    <li className="nav-item">
                      <button onClick={handleLogout} className="nav-link logout-button">Logout</button>
                    </li>
                  </ul>
                  <MobileNavigation onLogout={handleLogout} />
                </nav>
              </>
            )}

            <main className="main-content">
              <Switch>
                <Route path="/login" render={() => (
                  authenticated ? <Redirect to="/" /> : <Login setAuthenticated={setAuthenticated} />
                )} />
                <PrivateRoute exact path="/" component={Home} />
                <PrivateRoute path="/analytics" component={Analytics} />
                <PrivateRoute path="/profile" component={Profile} />
                <PrivateRoute path="/settings" component={Settings} />
                <Redirect to="/" />
              </Switch>
            </main>

            {authenticated && (
              <footer className="footer">
                <p>&copy; {new Date().getFullYear()} GradientLab - A $0-budget research tool for the Gradient Network</p>
              </footer>
            )}
          </div>
        </Router>
      </SocketProvider>
    </ToastProvider>
  );
}

export default App;
