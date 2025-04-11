import React, { useState, useEffect } from 'react';
import './VmTable.css';

const VmTable = () => {
  const [vms, setVms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Mock data for development (will be replaced with actual API calls)
  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setVms([
        {
          id: 1,
          name: 'oracle-vm-1',
          provider: 'oracle',
          region: 'us-west-1',
          ip_address: '192.168.1.1',
          status: 'running',
          created_at: '2023-04-10T12:00:00Z'
        },
        {
          id: 2,
          name: 'oracle-vm-2',
          provider: 'oracle',
          region: 'us-east-1',
          ip_address: '192.168.1.2',
          status: 'stopped',
          created_at: '2023-04-11T14:30:00Z'
        },
        {
          id: 3,
          name: 'google-vm-1',
          provider: 'google',
          region: 'us-central1',
          ip_address: '192.168.1.3',
          status: 'running',
          created_at: '2023-04-12T09:15:00Z'
        },
        {
          id: 4,
          name: 'azure-vm-1',
          provider: 'azure',
          region: 'eastus',
          ip_address: '192.168.1.4',
          status: 'provisioning',
          created_at: '2023-04-13T16:45:00Z'
        }
      ]);
      setLoading(false);
    }, 1000);
  }, []);

  const handleStartVM = (id) => {
    console.log(`Starting VM with ID: ${id}`);
    // Update VM status in the state
    setVms(vms.map(vm => 
      vm.id === id ? { ...vm, status: 'running' } : vm
    ));
  };

  const handleStopVM = (id) => {
    console.log(`Stopping VM with ID: ${id}`);
    // Update VM status in the state
    setVms(vms.map(vm => 
      vm.id === id ? { ...vm, status: 'stopped' } : vm
    ));
  };

  const handleDeleteVM = (id) => {
    console.log(`Deleting VM with ID: ${id}`);
    // Remove VM from the state
    setVms(vms.filter(vm => vm.id !== id));
  };

  if (loading) {
    return <div className="loading">Loading VMs...</div>;
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  return (
    <div className="vm-table-container">
      <h2>Virtual Machines</h2>
      {vms.length === 0 ? (
        <p>No VMs found. Create a new VM to get started.</p>
      ) : (
        <table className="vm-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Provider</th>
              <th>Region</th>
              <th>IP Address</th>
              <th>Status</th>
              <th>Created</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {vms.map(vm => (
              <tr key={vm.id}>
                <td>{vm.name}</td>
                <td>{vm.provider}</td>
                <td>{vm.region}</td>
                <td>{vm.ip_address}</td>
                <td>
                  <span className={`status-badge status-${vm.status}`}>
                    {vm.status}
                  </span>
                </td>
                <td>{new Date(vm.created_at).toLocaleDateString()}</td>
                <td className="actions">
                  {vm.status !== 'running' && (
                    <button 
                      className="action-button start"
                      onClick={() => handleStartVM(vm.id)}
                      disabled={vm.status === 'provisioning'}
                    >
                      Start
                    </button>
                  )}
                  {vm.status === 'running' && (
                    <button 
                      className="action-button stop"
                      onClick={() => handleStopVM(vm.id)}
                    >
                      Stop
                    </button>
                  )}
                  <button 
                    className="action-button delete"
                    onClick={() => handleDeleteVM(vm.id)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      <div className="vm-actions">
        <button className="create-button">Create New VM</button>
      </div>
    </div>
  );
};

export default VmTable;
