# 🧠 Re-Monster-Color-Agent

Een geavanceerd emotioneel geïnformeerd AI-besluitvormingssysteem gebaseerd op kleurvectoren en multi-agent feedback.

## 🌈 Systeem Architectuur

### Core Componenten

1. **Agent White (Orchestrator)**
   - Coördineert alle kleur-agents
   - Verwerkt input en berekent regenboogvector
   - Bepaalt optimale reactiestrategie
   - Balanseert multi-agent feedback

2. **Kleur Agents**
   - Green: Positieve emoties (blij, gelukkig, neutraal)
   - Yellow: Twijfelachtige emoties (ongeloof, walging, afkeer)
   - Blue: Empathische emoties (verward, gekwetst, verdriet)
   - Purple: Complexe emoties (jaloezie, ego, miscommunicatie)
   - Pink: Kwetsbare emoties (schuld, negatief, naïef)
   - Red: Intense emoties (verraad, kwaad, woede)
   - Gray: Overweldigende emoties (overweldigd, saturatie, ambivalentie)

### Bestanden

- `agent_white.py`: Implementatie van de orchestrator agent
- `colorinterperter.py`: Kleur- en emotie-interpretatie logica
- `color_config.json`: Configuratie van kleuren en sub-tints
- `color_agent_core.py`: Basis agent configuratie

## 🚀 Installatie

1. Clone de repository
2. Installeer dependencies:
```bash
pip install -r requirements.txt
```

## 💻 Gebruik

### Basis Gebruik

```python
from agent_white import AgentWhite

# Initialiseer Agent White
agent = AgentWhite()

# Analyseer context
response = agent.calculate_balanced_response("Ik ben erg blij met het resultaat!")

# Bekijk resultaten
print(f"Regenboogvector: {response['rainbow_vector']}")
print(f"Strategie: {response['strategy']}")
print(f"Dominante emoties: {response['dominant_emotions']}")
```

### Test Uitvoeren

```bash
python agent_white.py
```

## 🎨 Kleur Systeem

Elke kleur heeft drie sub-tints:
- Light: Verhoogde intensiteit
- Medium: Basis kleur
- Dark: Verlaagde intensiteit

De regenboogvector wordt berekend door:
1. Emotionele scores per agent
2. Gewichten van sub-tints
3. Confidence scores van agents

## 🤖 Reactie Strategieën

- **Direct**: Voor positieve, sterke emoties
- **Neutral**: Voor lage emotionele intensiteit
- **Empathetic**: Voor gemengde of subtiele emoties
- **Cautious**: Voor negatieve, sterke emoties

## 📝 Requirements

- Python 3.8+
- numpy
- colorama
- pydantic
- termcolor

## 🔄 Workflow

1. Input wordt ontvangen door Agent White
2. Alle kleur-agents analyseren de input
3. Emotionele scores worden berekend
4. Regenboogvector wordt gegenereerd
5. Optimale strategie wordt bepaald
6. Gebalanceerde feedback wordt gegenereerd

## 🎯 Toekomstige Verbeteringen

- [ ] Machine learning integratie voor betere emotieherkenning
- [ ] Real-time feedback systeem
- [ ] Uitgebreide context analyse
- [ ] Custom agent training
- [ ] API integratie

## Features

- **Multi-Color Space Support**:
  - RGB color space for basic color representation
  - CMYK color space for print-ready color analysis
  - CIE 1976 LAB color space for perceptually uniform color analysis
  - Chroma and hue angle calculations for detailed color analysis

- **Emotion Analysis**:
  - Analyzes text input for emotional content
  - Maps emotions to color weights
  - Calculates dominant emotions and strategies
  - Provides color-based emotional feedback

- **Color Conversion**:
  - RGB ↔ CMYK conversion
  - RGB ↔ LAB conversion
  - XYZ color space intermediate conversions
  - Chroma and hue angle calculations
  - Color blending with weights

- **Visualization**:
  - Interactive color space visualization
  - Real-time color updates
  - Multiple color space views
  - Emotion-to-color mapping display

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/re-monster.git
cd re-monster
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Enter text in the input field to analyze its emotional content.

3. View the results:
   - Color analysis in multiple color spaces
   - Dominant emotions and their weights
   - Suggested response strategy
   - Color visualization

## Color Spaces

### RGB
- Standard color space for digital displays
- Values range from 0-255 for each channel
- Direct representation of screen colors

### CMYK
- Print-oriented color space
- Values range from 0-1 for each channel
- Better suited for physical color representation

### CIE 1976 LAB
- Perceptually uniform color space
- L*: Lightness (0-100)
- a*: Green-Red axis (-128 to 127)
- b*: Blue-Yellow axis (-128 to 127)
- Includes chroma and hue angle calculations

## API Reference

### ColorConverter
- `rgb_to_cmyk(r, g, b)`: Convert RGB to CMYK
- `cmyk_to_rgb(c, m, y, k)`: Convert CMYK to RGB
- `rgb_to_lab(r, g, b)`: Convert RGB to LAB
- `lab_to_rgb(l, a, b)`: Convert LAB to RGB
- `calculate_chroma(a, b)`: Calculate color chroma
- `calculate_hue_angle(a, b)`: Calculate hue angle

### ColorEmotionInterpreter
- `analyze_context(text)`: Analyze text for emotional content
- `get_emotional_score(context, color_weights)`: Calculate emotional scores
- `determine_strategy(emotional_scores, cmyk_vector)`: Determine response strategy

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
