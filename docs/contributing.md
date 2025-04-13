# Contributing Guidelines

Thank you for your interest in contributing to GradientLab! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Please read and follow our [Code of Conduct](code_of_conduct.md) to foster an inclusive and respectful community.

## How to Contribute

There are many ways to contribute to GradientLab:

1. **Report Bugs**: Submit bug reports to help improve the project
2. **Suggest Features**: Propose new features or improvements
3. **Write Code**: Implement bug fixes or new features
4. **Write Documentation**: Improve or expand the documentation
5. **Review Code**: Review pull requests from other contributors
6. **Share Knowledge**: Help others by answering questions

## Getting Started

### 1. Fork the Repository

Fork the [GradientLab repository](https://github.com/GEMDevEng/GradientLab) on GitHub.

### 2. Clone Your Fork

```bash
git clone https://github.com/your-username/GradientLab.git
cd GradientLab
```

### 3. Set Up the Development Environment

Follow the [Installation Guide](installation.md) to set up the development environment.

### 4. Create a Branch

Create a branch for your contribution:

```bash
git checkout -b feature/your-feature-name
```

Use a descriptive branch name that reflects the nature of your contribution.

## Development Guidelines

### Code Style

- **Python**: Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- **JavaScript**: Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- **HTML/CSS**: Follow [Google HTML/CSS Style Guide](https://google.github.io/styleguide/htmlcssguide.html)

### Commit Messages

Write clear and descriptive commit messages:

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests after the first line

Example:
```
Add node status monitoring feature

- Implement status check endpoint
- Add monitoring script
- Update documentation

Fixes #123
```

### Testing

- Write tests for all new features and bug fixes
- Ensure all tests pass before submitting a pull request
- Aim for high test coverage

To run tests:

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Documentation

- Update documentation for all new features and changes
- Write clear and concise documentation
- Include code examples where appropriate

## Pull Request Process

### 1. Update Your Fork

Before submitting a pull request, update your fork with the latest changes:

```bash
git remote add upstream https://github.com/GEMDevEng/GradientLab.git
git fetch upstream
git checkout main
git merge upstream/main
git checkout your-branch-name
git rebase main
```

### 2. Submit a Pull Request

1. Push your branch to your fork:
   ```bash
   git push origin your-branch-name
   ```

2. Go to the [GradientLab repository](https://github.com/GEMDevEng/GradientLab) and create a pull request.

3. Fill out the pull request template with:
   - A clear title and description
   - References to any related issues
   - A checklist of completed items

### 3. Code Review

- All pull requests require review before merging
- Address all review comments and update your pull request
- Be responsive to feedback and questions

### 4. Merge

Once your pull request is approved, it will be merged into the main branch.

## Issue Reporting

### Bug Reports

When reporting a bug, include:

1. **Title**: A clear and descriptive title
2. **Description**: A detailed description of the bug
3. **Steps to Reproduce**: Step-by-step instructions to reproduce the bug
4. **Expected Behavior**: What you expected to happen
5. **Actual Behavior**: What actually happened
6. **Environment**: Details about your environment (OS, browser, etc.)
7. **Screenshots**: If applicable, add screenshots to help explain the problem
8. **Additional Context**: Any other information that might be relevant

### Feature Requests

When requesting a feature, include:

1. **Title**: A clear and descriptive title
2. **Description**: A detailed description of the feature
3. **Use Case**: How this feature would be used
4. **Benefits**: The benefits of implementing this feature
5. **Alternatives**: Any alternative solutions you've considered
6. **Additional Context**: Any other information that might be relevant

## Community

Join our community to get help, share ideas, and collaborate:

- **GitHub Discussions**: For general discussions and questions
- **Issue Tracker**: For bug reports and feature requests
- **Pull Requests**: For code contributions

## License

By contributing to GradientLab, you agree that your contributions will be licensed under the project's [MIT License](license.md).
