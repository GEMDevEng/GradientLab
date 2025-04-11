import React, { useState, useEffect } from 'react';
import './UserProfile.css';
import { getCurrentUser } from '../api/auth';

const UserProfile = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editMode, setEditMode] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    bio: ''
  });

  useEffect(() => {
    // Fetch user data
    const fetchUserData = async () => {
      try {
        setLoading(true);
        // In a real app, this would be an API call
        const userData = getCurrentUser();
        
        if (userData) {
          setUser(userData);
          setFormData({
            name: userData.name || '',
            email: userData.email || '',
            bio: userData.bio || ''
          });
        } else {
          setError('User not found');
        }
      } catch (err) {
        setError('Error fetching user data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      // In a real app, this would be an API call to update the user
      // For now, we'll just update the local state
      setUser({
        ...user,
        name: formData.name,
        email: formData.email,
        bio: formData.bio
      });
      
      setEditMode(false);
      // Show success message
      alert('Profile updated successfully');
    } catch (err) {
      setError('Error updating profile');
      console.error(err);
    }
  };

  if (loading) {
    return <div className="loading">Loading user profile...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (!user) {
    return <div className="error">User not found</div>;
  }

  return (
    <div className="user-profile">
      <h2>User Profile</h2>
      
      {editMode ? (
        <form onSubmit={handleSubmit} className="profile-form">
          <div className="form-group">
            <label htmlFor="name">Name</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="bio">Bio</label>
            <textarea
              id="bio"
              name="bio"
              value={formData.bio}
              onChange={handleInputChange}
              rows="4"
            />
          </div>
          
          <div className="form-actions">
            <button type="submit" className="save-button">Save Changes</button>
            <button 
              type="button" 
              className="cancel-button"
              onClick={() => setEditMode(false)}
            >
              Cancel
            </button>
          </div>
        </form>
      ) : (
        <div className="profile-info">
          <div className="profile-header">
            <div className="profile-avatar">
              {user.name ? user.name.charAt(0).toUpperCase() : 'U'}
            </div>
            <div className="profile-details">
              <h3>{user.name || user.username}</h3>
              <p className="profile-role">{user.role}</p>
            </div>
            <button 
              className="edit-button"
              onClick={() => setEditMode(true)}
            >
              Edit Profile
            </button>
          </div>
          
          <div className="profile-section">
            <h4>Email</h4>
            <p>{user.email || 'No email provided'}</p>
          </div>
          
          <div className="profile-section">
            <h4>Bio</h4>
            <p>{user.bio || 'No bio provided'}</p>
          </div>
          
          <div className="profile-section">
            <h4>Account Information</h4>
            <p><strong>Username:</strong> {user.username}</p>
            <p><strong>Role:</strong> {user.role}</p>
            <p><strong>Member Since:</strong> {new Date().toLocaleDateString()}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default UserProfile;
