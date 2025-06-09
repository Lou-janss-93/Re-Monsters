import json
from typing import Dict, List, Tuple
import numpy as np
from dataclasses import dataclass
from enum import Enum
from color_utils import ColorConverter

class Strategy(Enum):
    DIRECT = "direct"
    NEUTRAL = "neutral"
    EMPATHIC = "empathetic"
    CAUTIOUS = "cautious"

@dataclass
class AgentDecision:
    strategy: Strategy
    fallback: bool
    rainbow_vector: str
    cmyk_vector: Tuple[float, float, float, float]

class ColorEmotionInterpreter:
    def __init__(self, config_path: str = "color_config.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.converter = ColorConverter()
        
        # Agent configuratie
        self.agent_config = {
            "agent_white": {
                "role": "orchestrator",
                "description": "Verwerkt input, stuurt door naar alle agents, verzamelt scores, berekent regenboogkleur en beslist outputstrategie.",
                "agents": ["green", "yellow", "blue", "purple", "pink", "red"],
                "rainbow_vector": "#000000",
                "cmyk_vector": (0.0, 0.0, 0.0, 1.0),
                "decision": {
                    "strategy": "",
                    "fallback": False
                }
            },
            "agents": {
                "green": {
                    "color": "#00FF00",
                    "cmyk": (1.0, 0.0, 1.0, 0.0),  # Cyan + Yellow
                    "emotion": ["blij", "gelukkig", "neutraal"],
                    "weight": 0.0
                },
                "yellow": {
                    "color": "#FFFF00",
                    "cmyk": (0.0, 0.0, 1.0, 0.0),  # Yellow
                    "emotion": ["ongeloof", "walging", "afkeer"],
                    "weight": 0.0
                },
                "blue": {
                    "color": "#0000FF",
                    "cmyk": (1.0, 1.0, 0.0, 0.0),  # Cyan + Magenta
                    "emotion": ["verward", "gekwetst", "verdriet"],
                    "weight": 0.0
                },
                "purple": {
                    "color": "#800080",
                    "cmyk": (0.5, 1.0, 0.0, 0.0),  # Magenta + Cyan
                    "emotion": ["jaloezie", "ego", "miscommunicatie"],
                    "weight": 0.0
                },
                "pink": {
                    "color": "#FFC0CB",
                    "cmyk": (0.0, 0.25, 0.2, 0.0),  # Light Magenta + Yellow
                    "emotion": ["schuld", "negatief", "naïef"],
                    "weight": 0.0
                },
                "red": {
                    "color": "#FF0000",
                    "cmyk": (0.0, 1.0, 1.0, 0.0),  # Magenta + Yellow
                    "emotion": ["verraad", "kwaad", "woede"],
                    "weight": 0.0
                },
                "gray": {
                    "color": "#808080",
                    "cmyk": (0.0, 0.0, 0.0, 0.5),  # 50% Black
                    "emotion": ["overweldigd", "saturatie", "ambivalentie"],
                    "weight": 0.0
                }
            }
        }

    def calculate_rainbow_vector(self, color_weights: Dict[str, float]) -> Tuple[str, Tuple[float, float, float, float]]:
        """Berekent de regenboogvector in zowel hex als CMYK."""
        total_weight = sum(color_weights.values())
        if total_weight == 0:
            return "#000000", (0.0, 0.0, 0.0, 1.0)

        # Verzamel CMYK waarden en gewichten
        cmyk_colors = []
        weights = []
        
        for color, weight in color_weights.items():
            if color in self.agent_config["agents"]:
                cmyk_colors.append(self.agent_config["agents"][color]["cmyk"])
                weights.append(weight)

        # Bereken gewogen CMYK vector
        cmyk_vector = self.converter.blend_cmyk_colors(cmyk_colors, weights)
        
        # Converteer naar hex voor backward compatibility
        hex_color = self.converter.cmyk_to_hex(*cmyk_vector)
        
        return hex_color, cmyk_vector

    def determine_strategy(self, emotional_scores: Dict[str, float], cmyk_vector: Tuple[float, float, float, float]) -> AgentDecision:
        """Bepaalt de beste strategie op basis van emotionele scores en CMYK vector."""
        c, m, y, k = cmyk_vector
        
        # Bereken intensiteit (1 - k) omdat k de "key" (zwart) component is
        intensity = 1 - k
        
        # Bepaal de dominante emotie
        dominant_emotion = max(emotional_scores.items(), key=lambda x: x[1])[0]
        dominant_score = emotional_scores[dominant_emotion]
        
        # Bepaal de strategie op basis van CMYK componenten
        if k > 0.7:  # Veel zwart = overweldigd
            strategy = Strategy.CAUTIOUS
        elif y > 0.5 and c < 0.3:  # Hoog geel, laag cyaan = positief
            strategy = Strategy.DIRECT
        elif m > 0.5:  # Hoog magenta = intens
            strategy = Strategy.CAUTIOUS
        elif c > 0.5:  # Hoog cyaan = helder/duidelijk
            strategy = Strategy.EMPATHIC
        else:
            strategy = Strategy.NEUTRAL

        # Converteer CMYK naar hex voor backward compatibility
        hex_color = self.converter.cmyk_to_hex(*cmyk_vector)
        
        return AgentDecision(
            strategy=strategy,
            fallback=k > 0.8,  # Fallback als er te veel zwart is
            rainbow_vector=hex_color,
            cmyk_vector=cmyk_vector
        )

    def get_emotional_score(self, context: str, color_weights: Dict[str, float]) -> Dict[str, float]:
        """Berekent emotionele scores op basis van context en kleurgewichten."""
        emotional_scores = {}
        
        # Bereken basis emotionele scores
        for color, agent in self.agent_config["agents"].items():
            base_weight = color_weights.get(color, 0.0)
            
            # Bereken sub-tint gewichten
            for emotion in agent["emotion"]:
                if emotion not in emotional_scores:
                    emotional_scores[emotion] = 0.0
                
                # Verdeel het gewicht over de sub-tints
                for tint_type in ['light', 'medium', 'dark']:
                    tint_weight = self.config['colors'][color]['sub_tints'][tint_type]['weight']
                    emotional_scores[emotion] += (base_weight * tint_weight) / 100

        return emotional_scores

    def analyze_context(self, context: str) -> Tuple[Dict[str, float], AgentDecision]:
        """Analyseert de context en geeft emotionele scores en beslissing terug."""
        color_weights = {color: 0.0 for color in self.agent_config["agents"]}
        
        # Voorbeeld: verhoog gewichten op basis van bepaalde woorden in de context
        context_lower = context.lower()
        
        if "blij" in context_lower or "gelukkig" in context_lower:
            color_weights["green"] = 30.0
        if "kwaad" in context_lower or "woede" in context_lower:
            color_weights["red"] = 30.0
        if "verdriet" in context_lower or "gekwetst" in context_lower:
            color_weights["blue"] = 30.0
        if "jaloezie" in context_lower:
            color_weights["purple"] = 30.0
        if "schuld" in context_lower:
            color_weights["pink"] = 30.0
        if "ongeloof" in context_lower:
            color_weights["yellow"] = 30.0
        if "overweldigd" in context_lower:
            color_weights["gray"] = 30.0

        emotional_scores = self.get_emotional_score(context, color_weights)
        rainbow_vector, cmyk_vector = self.calculate_rainbow_vector(color_weights)
        decision = self.determine_strategy(emotional_scores, cmyk_vector)

        return emotional_scores, decision

# Voorbeeld gebruik
if __name__ == "__main__":
    interpreter = ColorEmotionInterpreter()
    
    # Test met verschillende contexten
    test_contexts = [
        "Ik ben erg blij met het resultaat!",
        "Ik ben woedend over wat er is gebeurd.",
        "Ik voel me een beetje verdrietig vandaag.",
        "Ik weet niet wat ik moet doen, ik voel me overweldigd."
    ]
    
    for context in test_contexts:
        print(f"\nContext: {context}")
        emotional_scores, decision = interpreter.analyze_context(context)
        print(f"Emotionele scores: {emotional_scores}")
        print(f"Regenboogvector (hex): {decision.rainbow_vector}")
        print(f"CMYK vector: {decision.cmyk_vector}")
        print(f"Strategie: {decision.strategy.value}")
        print(f"Fallback: {decision.fallback}")
