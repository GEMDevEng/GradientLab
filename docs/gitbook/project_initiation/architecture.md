# Architecture

## System Architecture

GradientLab follows a client-server architecture with several key components:

1. **Backend API**: A Flask-based RESTful API that handles data processing, authentication, and business logic
2. **Frontend UI**: A React-based user interface for monitoring and managing nodes
3. **Database**: A PostgreSQL database for storing node information, rewards, and user data
4. **VM Infrastructure**: Virtual machines deployed across multiple cloud providers
5. **Sentry Nodes**: Gradient Sentry Node extensions running on the VMs
6. **Monitoring System**: Scripts and services for monitoring node status and performance
7. **Data Collection System**: Scripts for collecting reward data from the Gradient Network

## Component Diagram

```
+------------------+      +------------------+      +------------------+
|                  |      |                  |      |                  |
|  Frontend (React)|<---->|  Backend (Flask) |<---->|  Database (SQL)  |
|                  |      |                  |      |                  |
+------------------+      +------------------+      +------------------+
                                   ^
                                   |
                                   v
+------------------+      +------------------+      +------------------+
|                  |      |                  |      |                  |
|  VM Management   |<---->|  Sentry Nodes    |<---->|  Gradient Network|
|                  |      |                  |      |                  |
+------------------+      +------------------+      +------------------+
        ^                         ^
        |                         |
        v                         v
+------------------+      +------------------+
|                  |      |                  |
|  Monitoring      |<---->|  Data Collection |
|                  |      |                  |
+------------------+      +------------------+
```

## Backend Architecture

The backend is built with Flask and follows a modular architecture:

1. **API Layer**: RESTful endpoints for client communication
2. **Service Layer**: Business logic and data processing
3. **Data Access Layer**: Database interactions and data models
4. **Authentication Layer**: User authentication and authorization
5. **WebSocket Layer**: Real-time updates for monitoring
6. **Task Layer**: Background tasks for data collection and monitoring

## Frontend Architecture

The frontend is built with React and follows a component-based architecture:

1. **Component Layer**: Reusable UI components
2. **Container Layer**: State management and business logic
3. **API Layer**: Communication with the backend API
4. **Routing Layer**: Navigation and page routing
5. **Authentication Layer**: User authentication and session management
6. **Visualization Layer**: Charts and graphs for data visualization

## VM Infrastructure

The VM infrastructure spans multiple cloud providers:

1. **Oracle Cloud**: Primary provider with free tier VMs
2. **Google Cloud**: Secondary provider for IP diversity
3. **Azure**: Tertiary provider for additional capacity

Each VM runs:

1. **Operating System**: Ubuntu or Oracle Linux
2. **Docker**: For containerized services
3. **Chromium**: For running the Sentry Node extension
4. **Monitoring Tools**: For collecting performance metrics
5. **Status Page**: For displaying node status

## Sentry Node Architecture

Each Sentry Node consists of:

1. **Chromium Browser**: Running in headless mode
2. **Sentry Node Extension**: Installed in Chromium
3. **Monitoring Scripts**: Checking node status and performance
4. **POC Tap Scripts**: Executing POC taps at scheduled intervals
5. **Status Page**: Displaying node status and metrics

## Monitoring System

The monitoring system includes:

1. **Node Monitoring**: Checking if nodes are online and functioning
2. **Performance Monitoring**: Tracking resource usage and response times
3. **Alert System**: Sending notifications for node issues
4. **Auto-Recovery**: Automatically restarting nodes when issues are detected
5. **Status Dashboard**: Displaying the status of all nodes

## Data Collection System

The data collection system includes:

1. **Reward Collection**: Gathering reward data from the Gradient Network API
2. **Performance Collection**: Collecting performance metrics from nodes
3. **Data Storage**: Storing collected data in the database
4. **Data Analysis**: Analyzing data to identify optimization opportunities
5. **Reporting**: Generating reports on rewards and performance

## Security Architecture

The security architecture includes:

1. **Authentication**: JWT-based authentication for API access
2. **Authorization**: Role-based access control for different operations
3. **Encryption**: Encryption of sensitive data at rest and in transit
4. **Firewall**: Restricting access to VMs and services
5. **Monitoring**: Detecting and alerting on security issues

## Deployment Architecture

The deployment architecture includes:

1. **Backend Deployment**: Heroku for hosting the backend API
2. **Frontend Deployment**: GitHub Pages for hosting the frontend UI
3. **Database Deployment**: Heroku PostgreSQL for the database
4. **VM Deployment**: Scripts for deploying VMs across cloud providers
5. **CI/CD**: GitHub Actions for continuous integration and deployment

## Data Flow

1. **User Interaction**: Users interact with the frontend UI
2. **API Requests**: The frontend sends requests to the backend API
3. **Data Processing**: The backend processes requests and interacts with the database
4. **VM Management**: The backend manages VMs through cloud provider APIs
5. **Node Monitoring**: Monitoring scripts check node status and performance
6. **Data Collection**: Collection scripts gather reward data from the Gradient Network
7. **Reporting**: The backend generates reports based on collected data
8. **Real-time Updates**: WebSockets provide real-time updates to the frontend

## Conclusion

The GradientLab architecture is designed to be modular, scalable, and secure. By separating concerns and following best practices, the system provides a robust platform for deploying and managing Gradient Sentry Nodes across multiple cloud providers.
