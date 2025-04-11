import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import VmTable from './VmTable';

// Mock the useEffect hook to avoid API calls
jest.mock('react', () => {
  const originalReact = jest.requireActual('react');
  return {
    ...originalReact,
    useEffect: (callback) => callback(),
  };
});

describe('VmTable Component', () => {
  test('renders virtual machines title', () => {
    render(<VmTable />);
    const titleElement = screen.getByText(/Virtual Machines/i);
    expect(titleElement).toBeInTheDocument();
  });

  test('renders loading state initially', () => {
    render(<VmTable />);
    const loadingElement = screen.getByText(/Loading VMs/i);
    expect(loadingElement).toBeInTheDocument();
  });

  test('renders create button', () => {
    // Override the loading state
    jest.spyOn(React, 'useState').mockImplementationOnce(() => [false, jest.fn()]);
    jest.spyOn(React, 'useState').mockImplementationOnce(() => [[], jest.fn()]);
    
    render(<VmTable />);
    const createButton = screen.getByText(/Create New VM/i);
    expect(createButton).toBeInTheDocument();
  });
});
