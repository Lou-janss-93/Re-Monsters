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
