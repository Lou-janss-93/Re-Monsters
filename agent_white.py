from typing import Dict, List, Tuple
from colorinterpreter import ColorEmotionInterpreter, AgentDecision
import json
from dataclasses import dataclass
from enum import Enum

@dataclass
class AgentFeedback:
    color: str
    emotion_scores: Dict[str, float]
    confidence: float
    suggestion: str

class AgentWhite:
    def __init__(self):
        self.interpreter = ColorEmotionInterpreter()
        self.agent_feedbacks: Dict[str, AgentFeedback] = {}
        
    def collect_agent_feedback(self, context: str) -> Dict[str, AgentFeedback]:
        """Verzamelt feedback van alle agents voor de gegeven context."""
        feedbacks = {}
        
        # Verzamel feedback van elke agent
        for color, agent in self.interpreter.agent_config["agents"].items():
            # Simuleer agent feedback (in een echte implementatie zou dit door de agents zelf worden gedaan)
            emotional_scores, decision = self.interpreter.analyze_context(context)
            
            # Filter scores voor deze agent's emoties
            agent_emotions = {emotion: score for emotion, score in emotional_scores.items() 
                            if emotion in agent["emotion"]}
            
            # Bereken confidence score
            confidence = sum(agent_emotions.values()) / len(agent_emotions) if agent_emotions else 0.0
            
            # Genereer suggestie op basis van emoties
            suggestion = self._generate_suggestion(color, agent_emotions, decision)
            
            feedbacks[color] = AgentFeedback(
                color=agent["color"],
                emotion_scores=agent_emotions,
                confidence=confidence,
                suggestion=suggestion
            )
        
        self.agent_feedbacks = feedbacks
        return feedbacks
    
    def _generate_suggestion(self, color: str, emotions: Dict[str, float], decision: AgentDecision) -> str:
        """Genereert een suggestie op basis van de agent's emoties en beslissing."""
        dominant_emotion = max(emotions.items(), key=lambda x: x[1])[0]
        
        suggestions = {
            "green": "Positieve en ondersteunende reactie",
            "yellow": "Voorzichtig en verduidelijkend",
            "blue": "Empathisch en begripvol",
            "purple": "Professioneel en afstandelijk",
            "pink": "Zorgzaam en attent",
            "red": "Direct en duidelijk",
            "gray": "Neutraal en balancerend"
        }
        
        return suggestions.get(color, "Neutrale reactie")
    
    def calculate_balanced_response(self, context: str) -> Dict:
        """Berekent een gebalanceerde respons op basis van alle agent feedback."""
        feedbacks = self.collect_agent_feedback(context)
        
        # Bereken gewogen gemiddelde van alle feedback
        total_confidence = sum(fb.confidence for fb in feedbacks.values())
        weighted_scores = {}
        
        for color, feedback in feedbacks.items():
            weight = feedback.confidence / total_confidence if total_confidence > 0 else 0
            for emotion, score in feedback.emotion_scores.items():
                if emotion not in weighted_scores:
                    weighted_scores[emotion] = 0
                weighted_scores[emotion] += score * weight
        
        # Bepaal de dominante emoties
        dominant_emotions = sorted(weighted_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Genereer de uiteindelijke beslissing
        _, decision = self.interpreter.analyze_context(context)
        
        return {
            "context": context,
            "rainbow_vector": decision.rainbow_vector,
            "strategy": decision.strategy.value,
            "dominant_emotions": dict(dominant_emotions),
            "agent_feedbacks": {
                color: {
                    "color": fb.color,
                    "emotion_scores": fb.emotion_scores,
                    "confidence": fb.confidence,
                    "suggestion": fb.suggestion
                }
                for color, fb in feedbacks.items()
            }
        }

def main():
    agent_white = AgentWhite()
    
    # Complex test cases with mixed emotions
    test_contexts = [
        # Basic emotions
        "Ik ben erg blij met het resultaat!",
        "Ik ben woedend over wat er is gebeurd.",
        "Ik voel me een beetje verdrietig vandaag.",
        "Ik weet niet wat ik moet doen, ik voel me overweldigd.",
        
        # Complex mixed emotions
        "Ik ben blij met de promotie, maar ook een beetje nerveus over de nieuwe verantwoordelijkheden.",
        "Ik voel me gefrustreerd en teleurgesteld, maar probeer positief te blijven.",
        "Ik ben boos op mezelf omdat ik me zo verdrietig voel over iets kleins.",
        "Ik ben overweldigd door alle positieve reacties, maar ook een beetje onzeker.",
        
        # Subtle emotional nuances
        "Het is een bitterzoete ervaring, met veel gemengde gevoelens.",
        "Ik voel me zowel opgelucht als bezorgd over de toekomst.",
        "Er is een mengeling van trots en nederigheid in mijn hart.",
        "Ik ervaar een diep gevoel van tevredenheid, maar ook een vleugje melancholie."
    ]
    
    for context in test_contexts:
        print(f"\n{'='*80}")
        print(f"Analyse van context: {context}")
        print(f"{'='*80}")
        
        response = agent_white.calculate_balanced_response(context)
        
        # Color Analysis
        print("\nKleur Analyse:")
        print(f"Regenboogvector: {response['rainbow_vector']}")
        
        # Convert to different color spaces
        from color_utils import ColorConverter
        converter = ColorConverter()
        
        # Convert hex to RGB
        hex_color = response['rainbow_vector'].lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        # Convert to CMYK
        c, m, y, k = converter.rgb_to_cmyk(r, g, b)
        print(f"CMYK: C={c:.2f}, M={m:.2f}, Y={y:.2f}, K={k:.2f}")
        
        # Convert to LAB
        l, a, b = converter.rgb_to_lab(r, g, b)
        print(f"LAB: L*={l:.2f}, a*={a:.2f}, b*={b:.2f}")
        
        # Calculate chroma and hue
        chroma = converter.calculate_chroma(a, b)
        hue = converter.calculate_hue_angle(a, b)
        print(f"Chroma: {chroma:.2f}, Hue: {hue:.2f}°")
        
        # Emotional Analysis
        print("\nEmotionele Analyse:")
        print(f"Strategie: {response['strategy']}")
        
        print("\nDominante emoties (met confidence scores):")
        for emotion, score in response['dominant_emotions'].items():
            confidence_level = "Hoog" if score > 3.0 else "Medium" if score > 1.0 else "Laag"
            print(f"- {emotion}: {score:.2f} ({confidence_level})")
        
        # Agent Analysis
        print("\nGedetailleerde Agent Analyse:")
        for color, feedback in response['agent_feedbacks'].items():
            if feedback['confidence'] > 0:
                print(f"\n{color.upper()} Agent:")
                print(f"Confidence: {feedback['confidence']:.2f}")
                print(f"Suggestion: {feedback['suggestion']}")
                print("Emotie Scores:")
                for emotion, score in feedback['emotion_scores'].items():
                    if score > 0:
                        print(f"  - {emotion}: {score:.2f}")
        
        # Color Harmony Analysis
        print("\nKleur Harmonie Analyse:")
        lab_colors = converter.generate_analogous_palette(l, a, b)
        print("Analogous kleuren:")
        for lab_color in lab_colors:
            hex_color = converter.lab_to_hex(*lab_color)
            print(f"- {hex_color}")
        
        # Accessibility Check
        white_lab = (100, 0, 0)
        contrast = converter.check_color_contrast((l, a, b), white_lab)
        print(f"\nToegankelijkheid:")
        print(f"Contrast ratio: {contrast:.2f}:1")
        print(f"WCAG AA compliant: {'✓' if contrast >= 4.5 else '✗'}")

if __name__ == "__main__":
    main() 