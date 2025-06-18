# UK Weighted Voting System

A comprehensive Python-based simulator for advanced voting systems modeled on UK election data, designed to demonstrate how voter expertise, participation, and other factors can influence governance decisions. This system uses real data from the 2024 UK General Election to model both ranked choice voting and weighted yes/no policy decisions.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## 🎯 Overview

Traditional "one person, one vote" systems treat all votes equally, regardless of voters' knowledge, experience, or stake in the outcome. This system addresses that limitation by implementing a sophisticated weighted voting mechanism that considers multiple voter attributes while maintaining democratic principles.

## 🌟 Key Features

### 📊 **Weighted Yes/No Voting**
Simulate policy decisions with weighted voter profiles based on:
- **Expertise (E)**: Political knowledge and subject matter understanding
- **Participation (P)**: Historical voting engagement and civic involvement
- **Decision Quality (D)**: Track record of thoughtful, consistent decisions
- **Alignment (A)**: Consideration of broader public interest
- **Stake (S)**: Personal impact from the decision outcome

### 🗳️ **Ranked Choice Voting (Alternative Vote)**
- Complete implementation of single transferable vote (STV) system
- Eliminates vote splitting and tactical voting concerns
- Real-time round-by-round elimination with 30-second intervals
- Supports multiple candidates and complex preference patterns

### 📈 **Interactive Visualizations**
- **Weighted Vote Comparison Charts**: Side-by-side analysis of different weighting systems
- **Ranked Choice Progression**: Visual timeline of vote transfers and eliminations
- **Voter Profile Heatmaps**: Demographic attribute analysis across voter groups
- **First Preferences Distribution**: Initial vote breakdown by party/candidate

### 🇬🇧 **Real UK Election Data**
Based on the 2024 UK General Election featuring:
- **7 Major Political Parties**: Conservative, Labour, Liberal Democrats, Reform UK, Green Party, SNP, Plaid Cymru
- **9 Demographic Voter Segments**: From urban professionals to first-time voters
- **Realistic Regional Patterns**: Scotland, Wales, urban/rural England variations
- **Authentic Policy Simulation**: "UK Rejoining the EU" referendum scenario

### ⚡ **Multiple Simulation Modes**
- **Quick Demo**: 3-second rounds for rapid testing and demonstrations
- **Full Simulation**: 30-second rounds for realistic election timing
- **Visualization Suite**: Complete analysis with charts and graphs

## 🔬 Why Weighted Voting?

### Current Democratic Limitations
- Equal weighting regardless of knowledge or stake
- Susceptible to populist manipulation
- May not reflect optimal outcomes for community welfare
- Limited consideration of expertise in technical decisions

### Weighted Voting Advantages
- **Recognizes Expertise**: Values subject matter knowledge appropriately
- **Rewards Participation**: Encourages long-term civic engagement
- **Accounts for Stakes**: Considers who is most affected by decisions
- **Promotes Quality**: Factors in decision-making track record
- **Maintains Democracy**: Transparent, mathematically verifiable system

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/UK-Weighted-Voting-System.git
   cd UK-Weighted-Voting-System/voting-simulator-py
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run simulations**
   
   **Quick Demo (3-second rounds):**
   ```bash
   python quick_demo.py
   ```
   
   **Full Demo (30-second rounds):**
   ```bash
   python full_demo.py
   ```
   
   **Complete with Visualizations:**
   ```bash
   python run.py
   ```

## 📋 System Verification

The system includes built-in verification to ensure proper implementation:

✅ **Ranked Choice Voting Compliance**
- Voters rank candidates in order of preference
- Lowest candidates eliminated until majority achieved
- Votes transfer to next available preference
- Prevents vote splitting and tactical voting

✅ **Weighted Voting Accuracy**
- Mathematical formula: `W = wE×E + wP×P + wD×D + wA×A + wS×S`
- All coefficients sum to 1.0 for proper weighting
- Min-max normalization for fair comparison across scales

✅ **Democratic Principles**
- Transparent calculation methods
- Verifiable results
- Configurable weighting systems
- Maintains voter privacy

## 🏛️ Use Cases

### **Decentralized Autonomous Organizations (DAOs)**
Perfect for blockchain governance where:
- Token holdings represent stake
- Participation history is tracked on-chain
- Technical expertise can be verified through credentials
- Decision quality measured through outcome tracking

### **Corporate Governance**
Enhance traditional shareholder voting by considering:
- Industry expertise and knowledge
- Long-term vs. short-term investment horizons
- Historical engagement with company decisions
- Alignment with stakeholder interests

### **Community Governance**
For local government and community decisions:
- Recognize long-term residents vs. newcomers
- Value subject matter expertise in technical decisions
- Consider impact on different demographic groups
- Reward consistent civic participation

### **Expert Committees**
Technical decision-making bodies where:
- Domain knowledge varies significantly among members
- Decisions require specialized understanding
- Long-term consequences must be considered
- Multiple stakeholder interests need balancing

## 📊 Sample Results

### Weighted Yes/No Vote: "UK Rejoining EU"
```
SIMULATION 1: WEIGHTED YES/NO VOTE ON 'UK REJOINING THE EU'

Voting Groups:
YES voters: urban_professionals, students, young_professionals, public_sector, first_time_voters
NO voters: rural_voters, retirees, working_class, business_owners

Results with different weighting systems:
1. Equal weights: PASSED (51.1% - 48.9%)
2. Expertise focus: PASSED (51.1% - 48.9%)  
3. Stake focus: PASSED (51.8% - 48.2%)
```

### Ranked Choice Election Results
```
SIMULATION 2: RANKED CHOICE VOTING FOR UK PARTIES

Round 1: Labour (35.7%), Conservative (23.8%), Green (14.3%)...
Round 2: Labour (38.1%), Conservative (23.8%)... [Plaid Cymru eliminated]
...
Final Result: Labour Party WINNER with 120 votes (57.1%)
```

## 🔧 Customization

### Voter Profile Configuration
```python
# Define custom voter segments
profiles = [
    VoterProfile(id='tech_experts', E=9, P=80, D=8, A=7, S=85),
    VoterProfile(id='community_leaders', E=7, P=95, D=9, A=9, S=90),
    # Add more segments as needed
]
```

### Weighting System Adjustment
```python
# Customize coefficient weights (must sum to 1.0)
coefficients = WeightCoefficients(
    wE=0.3,  # 30% expertise
    wP=0.2,  # 20% participation  
    wD=0.2,  # 20% decision quality
    wA=0.2,  # 20% alignment
    wS=0.1   # 10% stake
)
```

### Timing Configuration
```python
# Adjust round duration for different scenarios
results = run_election(candidates, ballots, round_duration=60)  # 1-minute rounds
```

## 📁 Project Structure

```
voting-simulator-py/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── setup.py                 # Package installation
├── FEATURES_SUMMARY.md      # Detailed feature overview
├── RENAME_GUIDE.md          # GitHub repository setup
│
├── vote_types.py            # Data structures and types
├── election.py              # Core voting algorithms
├── visualization.py         # Chart generation
├── main.py                  # Complete simulation suite
│
├── quick_demo.py           # 3-second rounds demo
├── full_demo.py            # 30-second rounds demo
├── run.py                  # Main execution script
│
└── charts/                 # Generated visualizations
    ├── weighted_vote_comparison.html
    ├── ranked_choice_results.html
    ├── voter_profiles.html
    └── first_preferences.html
```

## 🔬 Mathematical Model

### Weight Calculation Formula
```
Weight(voter) = wE × norm(E) + wP × norm(P) + wD × norm(D) + wA × norm(A) + wS × norm(S)
```

Where:
- `norm()` applies min-max normalization: `(value - min) / (max - min)`
- Coefficients `wE, wP, wD, wA, wS` sum to 1.0
- Each attribute is normalized to [0,1] scale for fair comparison

### Ranked Choice Algorithm
1. **Count first preferences** for all remaining candidates
2. **Check for majority winner** (>50% of valid votes)
3. **Eliminate lowest candidate** if no majority exists
4. **Transfer votes** to next preference on each ballot
5. **Repeat** until majority winner found

## 🎓 Research Applications

### Academic Research
- **Political Science**: Study alternative democratic mechanisms
- **Economics**: Analyze stakeholder voting in corporate governance
- **Computer Science**: Test algorithmic governance systems
- **Sociology**: Examine demographic influences on collective decisions

### Policy Analysis
- **Electoral Reform**: Model impact of different voting systems
- **Governance Innovation**: Test new democratic mechanisms
- **Stakeholder Engagement**: Optimize decision-making processes
- **Risk Assessment**: Evaluate decision quality under various systems

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit changes** (`git commit -m 'Add amazing feature'`)
4. **Push to branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Development Setup
```bash
# Clone for development
git clone https://github.com/YOUR-USERNAME/UK-Weighted-Voting-System.git
cd UK-Weighted-Voting-System/voting-simulator-py

# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **UK Electoral Commission** for 2024 election data
- **Democratic innovation researchers** worldwide
- **Open source visualization libraries**: Matplotlib, Plotly
- **Python community** for excellent tooling

## 📞 Support

- **Documentation**: Check the `/docs` folder for detailed guides
- **Issues**: Report bugs via GitHub Issues
- **Discussions**: Join conversations in GitHub Discussions
- **Email**: [your-email@domain.com] for direct inquiries

## 🔮 Future Roadmap

### Phase 2 Features
- [ ] **Blockchain Integration**: On-chain voting with smart contracts
- [ ] **Machine Learning**: Predictive modeling for voter behavior
- [ ] **Multi-language Support**: Internationalization for global use
- [ ] **Mobile Interface**: Web app for broader accessibility

### Phase 3 Features  
- [ ] **Real-time Voting**: Live election management system
- [ ] **API Development**: RESTful API for integration
- [ ] **Advanced Analytics**: Deep statistical analysis tools
- [ ] **Audit Trails**: Comprehensive vote verification systems

---

**Made with ❤️ for democratic innovation**

*"Democracy is not just about counting votes, but ensuring every voice is heard with appropriate weight."*
