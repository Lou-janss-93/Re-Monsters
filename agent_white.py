from typing import Dict, List, Tuple
from colorinterperter import ColorEmotionInterpreter, AgentDecision
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
                    "emotion_scores": fb.emotion_scores,
                    "confidence": fb.confidence,
                    "suggestion": fb.suggestion
                }
                for color, fb in feedbacks.items()
            }
        }

def main():
    agent_white = AgentWhite()
    
    # Test met verschillende contexten
    test_contexts = [
        "Ik ben erg blij met het resultaat!",
        "Ik ben woedend over wat er is gebeurd.",
        "Ik voel me een beetje verdrietig vandaag.",
        "Ik weet niet wat ik moet doen, ik voel me overweldigd."
    ]
    
    for context in test_contexts:
        print(f"\nAnalyse van context: {context}")
        response = agent_white.calculate_balanced_response(context)
        
        print("\nResultaten:")
        print(f"Regenboogvector: {response['rainbow_vector']}")
        print(f"Strategie: {response['strategy']}")
        print("\nDominante emoties:")
        for emotion, score in response['dominant_emotions'].items():
            print(f"- {emotion}: {score:.2f}")
        
        print("\nAgent feedback:")
        for color, feedback in response['agent_feedbacks'].items():
            print(f"\n{color.upper()} Agent:")
            print(f"Confidence: {feedback['confidence']:.2f}")
            print(f"Suggestion: {feedback['suggestion']}")
            print("Emoties:", feedback['emotion_scores'])

if __name__ == "__main__":
    main() 