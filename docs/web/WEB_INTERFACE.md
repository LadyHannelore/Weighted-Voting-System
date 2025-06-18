# UK Weighted Voting System - Web Interface

🌐 **Interactive Web Application** for advanced democratic simulations using real UK political data.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Web Application
```bash
python app.py
```

### 3. Access the Interface
Open your browser and go to: **http://localhost:5000**

## 🎯 Web Features

### 📊 **Interactive Simulations**
- **Weighted Yes/No Voting**: Policy decisions with expert weighting
- **Ranked Choice Elections**: STV elections with real-time results
- **Live Visualizations**: Interactive charts and graphs

### 🎨 **Modern Interface**
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Updates**: Live election progress and status
- **Interactive Charts**: Embedded Plotly visualizations
- **Professional UI**: Bootstrap-based modern design

### 🗳️ **UK Election Data**
- **7 Political Parties**: Conservative, Labour, LibDem, Reform, Green, SNP, Plaid Cymru
- **9 Voter Demographics**: Urban professionals, rural voters, students, retirees, etc.
- **Realistic Patterns**: Based on 2024 UK General Election data

## 📱 Using the Web Interface

### **Homepage (`/`)**
- Overview of the system and features
- Navigation to different simulation types
- Information about UK political parties

### **Weighted Voting (`/weighted-vote`)**
1. Enter a policy question (default: "UK Rejoining the EU")
2. Click "Run Simulation" 
3. View results across three weighting systems:
   - **Equal**: All factors weighted equally
   - **Expertise**: Knowledge and experience prioritized  
   - **Stake**: Personal impact emphasized
4. Generate interactive comparison charts

### **Ranked Choice Election (`/ranked-choice`)**
1. Select round duration (3-30 seconds)
2. Click "Start Election"
3. Watch real-time elimination rounds
4. View final winner and vote transfers
5. Generate timeline and preference analysis charts

## 🔧 API Endpoints

### **POST** `/api/run-weighted-vote`
Run weighted yes/no vote simulation
```json
{
    "question": "UK Rejoining the EU"
}
```

### **POST** `/api/run-ranked-choice`  
Run ranked choice election
```json
{
    "round_duration": 5
}
```

### **GET** `/api/generate-chart/<chart_type>`
Generate visualization charts:
- `weighted-comparison` - Vote comparison across weighting systems
- `ranked-choice` - Election timeline and transfers
- `voter-profiles` - Demographic attribute heatmap
- `first-preferences` - Initial vote distribution

### **GET** `/api/simulation-status`
Get current simulation status and progress

## 🎨 Customization

### **Change Voter Demographics**
Edit the `get_voter_profiles()` function in `app.py`:
```python
def get_voter_profiles():
    return [
        VoterProfile(id="custom_group", E=8, P=75, D=7, A=6, S=80, 
                    name="Custom Group", count=25),
        # Add more profiles...
    ]
```

### **Modify Political Parties**
Edit the `get_uk_parties()` function:
```python
def get_uk_parties():
    return [
        Candidate(id="party1", name="Your Party Name"),
        # Add more parties...
    ]
```

### **Adjust Weighting Systems**
Modify the weighting coefficients in `api_run_weighted_vote()`:
```python
equal_weights = WeightCoefficients(0.2, 0.2, 0.2, 0.2, 0.2)
expertise_weights = WeightCoefficients(0.4, 0.3, 0.1, 0.1, 0.1)
custom_weights = WeightCoefficients(0.3, 0.2, 0.2, 0.2, 0.1)
```

## 🔒 Production Deployment

For production use, replace the development server:

### **Using Gunicorn**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### **Using uWSGI**
```bash
pip install uwsgi
uwsgi --http :5000 --wsgi-file app.py --callable app
```

### **Environment Variables**
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key-here
```

## 🛠️ Development

### **Project Structure**
```
voting-simulator-py/
├── app.py                 # Flask web application
├── templates/             # HTML templates
│   ├── index.html        # Homepage
│   ├── weighted_vote.html # Weighted voting page
│   └── ranked_choice.html # Ranked choice page
├── static/               # CSS, JS, images (auto-created)
├── vote_types.py         # Data structures
├── election.py           # Voting algorithms
├── visualization.py      # Chart generation
└── requirements.txt      # Dependencies
```

### **Adding New Features**

1. **New Simulation Type**:
   - Add route in `app.py`
   - Create HTML template
   - Add API endpoint
   - Update navigation

2. **New Chart Type**:
   - Add function to `visualization.py`
   - Update `api_generate_chart()` endpoint
   - Add button to HTML template

3. **Custom Styling**:
   - Create `static/css/custom.css`
   - Link in HTML templates
   - Override Bootstrap styles

### **Testing the API**
```bash
# Test weighted vote
curl -X POST http://localhost:5000/api/run-weighted-vote \
     -H "Content-Type: application/json" \
     -d '{"question": "Test Policy"}'

# Test ranked choice
curl -X POST http://localhost:5000/api/run-ranked-choice \
     -H "Content-Type: application/json" \
     -d '{"round_duration": 3}'
```

## 🌟 Advanced Features

### **Real-time Updates**
The interface polls simulation status every second to show live progress during ranked choice elections.

### **Responsive Charts**
All visualizations are embedded as interactive Plotly charts that work on any device.

### **Professional Design** 
- Bootstrap 5 responsive framework
- Font Awesome icons
- Gradient backgrounds and hover effects
- Loading spinners and progress bars

### **Error Handling**
- Graceful error messages
- Fallback for failed chart generation
- Input validation and sanitization

## 🔍 Troubleshooting

### **Port Already in Use**
```bash
# Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### **Template Not Found**
Ensure the `templates/` directory exists in the same folder as `app.py`.

### **Chart Generation Fails**
Check that matplotlib and plotly are installed:
```bash
pip install matplotlib plotly pandas
```

### **Import Errors**
Run from the `voting-simulator-py` directory:
```bash
cd voting-simulator-py
python app.py
```

## 📊 Sample Usage

1. **Start the application**: `python app.py`
2. **Open browser**: Go to `http://localhost:5000`
3. **Run weighted vote**: Click "Try Weighted Voting" → Enter question → Run simulation
4. **View results**: Compare different weighting systems
5. **Generate charts**: Click visualization buttons
6. **Try ranked choice**: Navigate to "Ranked Choice" → Start election
7. **Watch real-time**: See elimination rounds in real-time
8. **Analyze results**: Generate timeline and preference charts

## 🎓 Educational Use

Perfect for:
- **Political Science**: Demonstrate alternative voting systems
- **Computer Science**: Web development with data visualization
- **Statistics**: Understanding weighted averages and normalization
- **Civic Education**: Interactive democracy and voting methods

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test the web interface
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

---

**🌐 Experience democracy in action at http://localhost:5000**
