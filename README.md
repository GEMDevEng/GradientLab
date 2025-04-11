# GradientLab

## Overview
GradientLab is a web application designed to automate VM setup and Sentry Node management on the Gradient Network. Built with Flask and React, it uses free-tier cloud resources (Oracle, Google, Azure) to collect data on POA (Proof-of-Availability), POC (Proof-of-Connectivity), and referral rewards. This $0-budget research tool analyzes network effects over 60 months, with the potential to scale with future grants.

## Purpose
This project aims to study reward mechanisms on the Gradient Network, a decentralized compute infrastructure built on Solana. By running Sentry Nodes on free-tier cloud VMs, we can collect data on how participants earn points through uptime, network connectivity, and referrals, providing insights into network effects and optimization strategies.

## Features
- **VM Provisioning**: Automated setup of VMs on free-tier cloud platforms
- **Node Deployment**: Installation and configuration of Gradient Sentry Nodes
- **Data Collection**: Tracking of POA, POC, and referral rewards
- **Analytics Dashboard**: Visualization of reward trends and network performance
- **Referral Simulation**: Testing of referral bonus mechanisms

## Technology Stack
- **Backend**: Flask (Python)
- **Frontend**: React.js
- **Database**: SQLite
- **Cloud Providers**: Oracle Cloud, Google Cloud Platform, Microsoft Azure (free tiers)
- **Deployment**: GitHub Pages

## Repository Structure
```
GradientLab/
├── backend/                    # Flask backend API
├── frontend/                   # React frontend application
├── database/                   # SQLite database and migrations
├── docs/                       # Project documentation
│   ├── network_effects/        # Network effects analysis
│   ├── project_description/    # Project overview and goals
│   ├── planning/               # Planning documents (WBS, PRD, etc.)
│   ├── technical/              # Technical specifications
│   ├── features/               # Feature documentation
│   └── implementation/         # Implementation guides
├── logs/                       # Application logs
└── .github/                    # GitHub workflows and templates
```

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+
- Free-tier accounts on cloud providers (Oracle, Google, Azure)

### Installation
1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/GradientLab.git
   cd GradientLab
   ```

2. Set up the backend
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Set up the frontend
   ```bash
   cd frontend
   npm install
   ```

### Running the Application
1. Start the backend server
   ```bash
   cd backend
   python app.py
   ```

2. Start the frontend development server
   ```bash
   cd frontend
   npm start
   ```

## Deployment
The application is designed to be deployed on GitHub Pages for the frontend, with the backend potentially hosted on a free-tier platform like Heroku or using serverless functions.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements
- Gradient Network for providing the Sentry Node infrastructure
- Free-tier cloud providers for enabling $0-budget research
