import React from 'react';
import { render, screen } from '@testing-library/react';
import Dashboard from './Dashboard';

// Mock the useEffect hook to avoid API calls
jest.mock('react', () => {
  const originalReact = jest.requireActual('react');
  return {
    ...originalReact,
    useEffect: (callback) => callback(),
  };
});

describe('Dashboard Component', () => {
  test('renders dashboard title', () => {
    render(<Dashboard />);
    const titleElement = screen.getByText(/Dashboard/i);
    expect(titleElement).toBeInTheDocument();
  });

  test('renders stat cards', () => {
    render(<Dashboard />);
    
    // Check for stat card titles
    expect(screen.getByText(/VMs/i)).toBeInTheDocument();
    expect(screen.getByText(/Nodes/i)).toBeInTheDocument();
    expect(screen.getByText(/Total Points/i)).toBeInTheDocument();
    expect(screen.getByText(/Avg. Points\/Node/i)).toBeInTheDocument();
  });

  test('renders recent activity section', () => {
    render(<Dashboard />);
    
    const activitySection = screen.getByText(/Recent Activity/i);
    expect(activitySection).toBeInTheDocument();
  });
});
