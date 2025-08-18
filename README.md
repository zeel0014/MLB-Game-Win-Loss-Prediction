# MLB Game Prediction System

A comprehensive machine learning pipeline for predicting MLB game outcomes using historical player and team statistics.

## 🎯 Project Overview

This project implements an end-to-end data science pipeline that fetches, processes, and analyzes MLB (Major League Baseball) data to predict game outcomes. The system combines team-level and player-level statistics to build robust predictive models.

## 📊 Dataset Description

- **Time Period**: 2024 MLB Season
- **Total Games**: Complete regular season schedule
- **Features**: 75+ engineered features including:
  - Team batting statistics (average, OBP, SLG, OPS)
  - Team pitching statistics (ERA, WHIP, K/BB ratio)
  - Player-level batting and pitching metrics
  - Game context (venue, day/night, series progress)
  - Historical performance indicators

## 🏗️ Architecture

### Data Pipeline
```
Raw API Data → Data Cleaning → Feature Engineering → Model Training → Predictions
```

### Project Structure
```
mlb-project/
├── data fetch/           # API data extraction scripts
├── data clean/           # Data preprocessing notebooks
├── data marge/           # Data integration and merging
├── train data/           # Model training and evaluation
├── mlbenv/              # Python virtual environment
└── README.md            # This file
```

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/mlb-prediction-system.git
   cd mlb-prediction-system
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv mlbenv
   source mlbenv/bin/activate  # On Windows: mlbenv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Data Pipeline Execution

1. **Fetch Raw Data**
   ```bash
   python data fetch/batting_player_2024.py
   python data fetch/batting_team_2024.py
   python data fetch/game_schedule_2024.py
   python data fetch/pitche_player_2024.py
   python data fetch/pitche_team_2024.py
   ```

2. **Clean and Process Data**
   - Run all notebooks in `data clean/` directory
   - Execute notebooks sequentially for each data type

3. **Merge Datasets**
   - Run `data marge/final_marge.ipynb` to create final training dataset

4. **Train Models**
   - Execute `train data/train_data.ipynb` for model training and evaluation

## 🤖 Models Implemented

### Algorithms Tested
- **Logistic Regression** (L1/L2 regularization)
- **Random Forest Classifier** (with hyperparameter tuning)
- **XGBoost Classifier**
- **Stacking Ensemble** (combining multiple models)

### Performance Metrics
- **Accuracy**: ~65-70% (varies by model)
- **ROC-AUC**: ~0.72
- **Precision/Recall**: Balanced for both home win/loss classes

## 📈 Key Features

### Feature Engineering
- **Series Context**: Game position within series
- **Venue Normalization**: MLB stadium categorization
- **Performance Ratios**: K/BB, ground/fly ball ratios
- **Team Form**: Recent performance indicators

### Data Quality
- Duplicate removal
- Outlier detection and handling
- Missing value imputation
- Feature standardization

## 🔧 Technical Stack

### Core Libraries
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **scikit-learn**: Machine learning algorithms
- **xgboost**: Gradient boosting framework
- **jupyter**: Interactive development environment

### Development Tools
- **Python 3.10**: Primary programming language
- **Virtual Environment**: Dependency management
- **Jupyter Notebooks**: Exploratory data analysis

## 📊 Model Evaluation

### Cross-Validation Results
- **5-fold stratified cross-validation**
- **StratifiedShuffleSplit** for train/test separation
- **GridSearchCV** for hyperparameter optimization

### Feature Importance
Top predictive features include:
- Team batting average
- Starting pitcher ERA
- Home field advantage
- Recent team form

## 🎯 Use Cases

1. **Game Outcome Prediction**: Predict win probability for upcoming games
2. **Betting Analytics**: Inform sports betting decisions
3. **Team Performance Analysis**: Identify key performance indicators
4. **Player Impact Assessment**: Evaluate individual player contributions

## 🔮 Future Enhancements

- [ ] Real-time prediction API
- [ ] Advanced feature engineering (weather, injuries)
- [ ] Deep learning models (LSTM for sequence data)
- [ ] Historical backtesting framework
- [ ] Interactive dashboard for predictions

## 📄 Data Sources

- **Primary**: MLB Stats API
- **Coverage**: 2024 Regular Season
- **Update Frequency**: Daily during season

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

Your Name - [@your_twitter](https://twitter.com/your_twitter) - your.email@example.com

Project Link: [https://github.com/yourusername/mlb-prediction-system](https://github.com/yourusername/mlb-prediction-system)

## 🙏 Acknowledgments

- MLB Stats API for providing comprehensive baseball data
- scikit-learn and XGBoost communities for excellent ML tools
- Baseball-Reference for historical context and validation
