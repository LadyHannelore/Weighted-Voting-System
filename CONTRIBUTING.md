# Contributing to UK Weighted Voting System

Thank you for your interest in contributing to the UK Weighted Voting System! This document provides guidelines and information for contributors.

## 🎯 Project Vision

We're building a comprehensive, research-grade voting simulation system that demonstrates how different democratic mechanisms can lead to different outcomes. Our goal is to provide tools for:

- Academic research in political science and governance
- Practical implementation in DAOs and corporate governance
- Educational demonstrations of voting system mathematics
- Policy analysis and electoral reform research

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- Git for version control
- Basic understanding of voting systems and democratic principles

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR-USERNAME/UK-Weighted-Voting-System.git
   cd UK-Weighted-Voting-System
   ```

2. **Set up Development Environment**
   ```bash
   cd voting-simulator-py
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

3. **Verify Installation**
   ```bash
   python quick_demo.py
   ```

## 🛠️ Development Workflow

### Branching Strategy
- `main`: Stable, production-ready code
- `develop`: Integration branch for new features
- `feature/feature-name`: Individual feature development
- `hotfix/issue-description`: Critical bug fixes

### Making Changes

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Follow the coding standards below
   - Add tests for new functionality
   - Update documentation as needed

3. **Test Your Changes**
   ```bash
   python -m pytest tests/
   python quick_demo.py  # Smoke test
   ```

4. **Commit and Push**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request**
   - Use the PR template
   - Link any related issues
   - Ensure CI checks pass

## 📝 Coding Standards

### Python Style Guide
- Follow PEP 8 style guidelines
- Use type hints for all function parameters and returns
- Maximum line length: 88 characters (Black formatter)
- Use meaningful variable and function names

### Code Organization
```python
# Standard library imports
import json
from typing import List, Dict

# Third-party imports
import matplotlib.pyplot as plt
import pandas as pd

# Local imports
from vote_types import VoterProfile, Candidate
from election import run_election
```

### Documentation Standards
- All public functions must have docstrings
- Use Google-style docstrings
- Include type hints and examples where helpful

```python
def calculate_weights(
    profiles: List[VoterProfile],
    coeffs: WeightCoefficients,
    bounds: Dict[str, VoterProfile]
) -> Dict[str, float]:
    """
    Calculate weighted voting power for each voter profile.
    
    Args:
        profiles: List of voter profile objects
        coeffs: Weight coefficients for each attribute
        bounds: Min/max bounds for normalization
        
    Returns:
        Dictionary mapping voter IDs to their calculated weights
        
    Example:
        >>> profiles = [VoterProfile(id='alice', E=8, P=70, D=7, A=6, S=80)]
        >>> coeffs = WeightCoefficients(wE=0.2, wP=0.2, wD=0.2, wA=0.2, wS=0.2)
        >>> weights = calculate_weights(profiles, coeffs, bounds)
        >>> weights['alice']
        0.642
    """
```

## 🧪 Testing Guidelines

### Test Structure
```
tests/
├── unit/                    # Unit tests for individual functions
│   ├── test_election.py
│   ├── test_visualization.py
│   └── test_vote_types.py
├── integration/             # Integration tests
│   ├── test_full_simulation.py
│   └── test_data_flow.py
└── fixtures/               # Test data and fixtures
    ├── sample_ballots.json
    └── test_profiles.json
```

### Writing Tests
- Use pytest framework
- Aim for >90% code coverage
- Test both happy path and edge cases
- Use descriptive test names

```python
def test_ranked_choice_elimination_with_tied_candidates():
    """Test that tied candidates are eliminated alphabetically."""
    # Test implementation here
```

### Running Tests
```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=voting_simulator_py

# Run specific test file
python -m pytest tests/unit/test_election.py

# Run tests matching pattern
python -m pytest -k "test_weighted"
```

## 🎨 Contribution Areas

### High Priority
- **Performance Optimization**: Large-scale voting simulations
- **Additional Voting Systems**: Approval voting, STAR voting, etc.
- **Data Import/Export**: CSV, JSON, database connectivity
- **Accessibility**: Screen reader support, keyboard navigation

### Medium Priority
- **Advanced Visualizations**: 3D charts, interactive plots
- **Statistical Analysis**: Confidence intervals, significance testing
- **Documentation**: Video tutorials, interactive guides
- **Internationalization**: Multi-language support

### Research Contributions
- **Academic Papers**: Peer-reviewed research using the system
- **Case Studies**: Real-world applications and outcomes
- **Algorithmic Improvements**: Better optimization, new voting methods
- **Theoretical Analysis**: Mathematical proofs, complexity analysis

## 📊 Data Contributions

### Adding New Election Data
1. **Data Format**: Use standardized JSON structure
2. **Validation**: Ensure data integrity and completeness
3. **Documentation**: Provide source and methodology
4. **Privacy**: Remove personally identifiable information

### Example Data Structure
```json
{
  "election": {
    "name": "2024 UK General Election",
    "date": "2024-07-04",
    "source": "UK Electoral Commission"
  },
  "candidates": [
    {
      "id": "labour_candidate_1",
      "name": "Candidate Name",
      "party": "Labour Party",
      "constituency": "Example Constituency"
    }
  ],
  "voter_profiles": [
    {
      "demographic": "urban_professionals",
      "attributes": {"E": 8, "P": 70, "D": 7, "A": 6, "S": 80},
      "sample_size": 1000
    }
  ]
}
```

## 🐛 Bug Reports

### Before Submitting
1. **Search existing issues** to avoid duplicates
2. **Try the latest version** to see if it's already fixed
3. **Reproduce consistently** with minimal steps

### Bug Report Template
```markdown
**Bug Description**
Clear description of what went wrong

**Steps to Reproduce**
1. Step one
2. Step two
3. Step three

**Expected Behavior**
What should have happened

**Actual Behavior**
What actually happened

**Environment**
- OS: [e.g., Windows 10]
- Python version: [e.g., 3.9.7]
- Package version: [e.g., 1.2.3]

**Additional Context**
Screenshots, logs, or other relevant information
```

## 💡 Feature Requests

### Feature Request Template
```markdown
**Feature Summary**
Brief description of the proposed feature

**Problem Statement**
What problem does this solve?

**Proposed Solution**
How should this feature work?

**Alternative Solutions**
Other approaches you've considered

**Use Cases**
Who would benefit and how?

**Implementation Notes**
Technical considerations or constraints
```

## 🏆 Recognition

### Contributors Hall of Fame
Contributors will be recognized in:
- README.md acknowledgments
- GitHub contributors page
- Annual project reports
- Academic papers citing contributions

### Types of Recognition
- **Code Contributors**: Direct code contributions
- **Documentation Writers**: Improved docs and tutorials
- **Bug Hunters**: Quality bug reports and testing
- **Researchers**: Academic usage and citations
- **Community Leaders**: Helping others and organizing

## 📚 Resources

### Learning Materials
- **Voting Theory**: [Stanford Encyclopedia of Philosophy](https://plato.stanford.edu/entries/voting-methods/)
- **Python Development**: [Real Python](https://realpython.com/)
- **Data Visualization**: [Plotly Documentation](https://plotly.com/python/)
- **Democratic Innovation**: [Democracy R&D](https://www.democracy.earth/)

### Communication Channels
- **GitHub Discussions**: General questions and ideas
- **GitHub Issues**: Bug reports and feature requests
- **Discord Server**: [Link] - Real-time chat and collaboration
- **Mailing List**: [Link] - Monthly updates and announcements

## ❓ FAQ

**Q: How can I add support for a new voting system?**
A: Start by studying the existing `election.py` module and implementing the new system as a separate function. Include comprehensive tests and documentation.

**Q: Can I use this for commercial purposes?**
A: Yes! The MIT license allows commercial use. We'd love to hear about your application.

**Q: How do I cite this project in academic work?**
A: We're working on a formal citation format. For now, please reference the GitHub repository and any relevant version numbers.

**Q: Is there a roadmap for future development?**
A: Yes! Check the main README.md for our current roadmap and planned features.

## 🤝 Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please read and follow our Code of Conduct:

### Our Pledge
- **Respectful Communication**: Treat all community members with respect
- **Constructive Feedback**: Focus on ideas, not individuals
- **Inclusive Environment**: Welcome people of all backgrounds and experience levels
- **Collaborative Spirit**: Work together toward common goals

### Unacceptable Behavior
- Harassment, discrimination, or hostile communication
- Personal attacks or inflammatory language
- Spam, off-topic discussions, or disruptive behavior
- Sharing private information without permission

### Enforcement
Community leaders will enforce these standards fairly and consistently. Violations may result in temporary or permanent bans from the project.

---

Thank you for contributing to the UK Weighted Voting System! Together, we're building tools that can help improve democratic processes worldwide.

**Questions?** Reach out via GitHub Discussions or email the maintainers.
