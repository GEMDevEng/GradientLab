-- Initialize the database schema for GradientLab

-- VMs table to store information about provisioned virtual machines
CREATE TABLE IF NOT EXISTS vms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT NOT NULL,  -- e.g., 'oracle', 'google', 'azure'
    vm_id TEXT NOT NULL,     -- Provider-specific VM identifier
    ip_address TEXT,         -- IP address of the VM
    region TEXT,             -- Region where the VM is deployed
    status TEXT,             -- e.g., 'running', 'stopped', 'terminated'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Nodes table to store information about Sentry Nodes
CREATE TABLE IF NOT EXISTS nodes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vm_id INTEGER,           -- Foreign key to vms table
    status TEXT,             -- e.g., 'good', 'disconnected', 'unsupported'
    uptime_percentage REAL,  -- Percentage of time the node has been online
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vm_id) REFERENCES vms (id)
);

-- Rewards table to store information about earned rewards
CREATE TABLE IF NOT EXISTS rewards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    node_id INTEGER,         -- Foreign key to nodes table
    poa_points INTEGER,      -- Proof-of-Availability points
    poc_points INTEGER,      -- Proof-of-Connectivity points
    referral_points INTEGER, -- Points earned from referrals
    date DATE,               -- Date when rewards were earned
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (node_id) REFERENCES nodes (id)
);

-- Referrals table to store information about referral relationships
CREATE TABLE IF NOT EXISTS referrals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    referrer_node_id INTEGER, -- Node that referred another node
    referred_node_id INTEGER, -- Node that was referred
    bonus_percentage REAL,    -- Percentage bonus for the referrer
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (referrer_node_id) REFERENCES nodes (id),
    FOREIGN KEY (referred_node_id) REFERENCES nodes (id)
);
