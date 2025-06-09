from typing import Tuple, Dict, List
import numpy as np

class ColorConverter:
    @staticmethod
    def rgb_to_cmyk(r: int, g: int, b: int) -> Tuple[float, float, float, float]:
        """Converteert RGB naar CMYK."""
        # Normaliseer RGB waarden
        r, g, b = r/255.0, g/255.0, b/255.0
        
        # Bereken K (Key/Black)
        k = 1 - max(r, g, b)
        
        if k == 1:
            return 0.0, 0.0, 0.0, 1.0
        
        # Bereken CMY
        c = (1 - r - k) / (1 - k)
        m = (1 - g - k) / (1 - k)
        y = (1 - b - k) / (1 - k)
        
        return c, m, y, k

    @staticmethod
    def cmyk_to_rgb(c: float, m: float, y: float, k: float) -> Tuple[int, int, int]:
        """Converteert CMYK naar RGB."""
        r = 255 * (1 - c) * (1 - k)
        g = 255 * (1 - m) * (1 - k)
        b = 255 * (1 - y) * (1 - k)
        
        return int(round(r)), int(round(g)), int(round(b))

    @staticmethod
    def hex_to_cmyk(hex_color: str) -> Tuple[float, float, float, float]:
        """Converteert hex kleur naar CMYK."""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return ColorConverter.rgb_to_cmyk(r, g, b)

    @staticmethod
    def cmyk_to_hex(c: float, m: float, y: float, k: float) -> str:
        """Converteert CMYK naar hex kleur."""
        r, g, b = ColorConverter.cmyk_to_rgb(c, m, y, k)
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)

    @staticmethod
    def calculate_emotional_cmyk(emotions: Dict[str, float]) -> Tuple[float, float, float, float]:
        """Berekent CMYK waarden op basis van emotionele scores."""
        # Emotie mapping naar CMYK componenten
        emotion_mapping = {
            'clarity': ['verward', 'gekwetst', 'verdriet'],  # Cyan
            'passion': ['kwaad', 'woede', 'verraad'],        # Magenta
            'energy': ['blij', 'gelukkig', 'neutraal'],      # Yellow
            'depth': ['overweldigd', 'saturatie', 'ambivalentie']  # Key/Black
        }
        
        # Bereken gewogen gemiddelde voor elke component
        c = sum(emotions.get(e, 0) for e in emotion_mapping['clarity']) / len(emotion_mapping['clarity'])
        m = sum(emotions.get(e, 0) for e in emotion_mapping['passion']) / len(emotion_mapping['passion'])
        y = sum(emotions.get(e, 0) for e in emotion_mapping['energy']) / len(emotion_mapping['energy'])
        k = sum(emotions.get(e, 0) for e in emotion_mapping['depth']) / len(emotion_mapping['depth'])
        
        # Normaliseer waarden
        total = c + m + y + k
        if total > 0:
            c, m, y, k = c/total, m/total, y/total, k/total
        
        return c, m, y, k

    @staticmethod
    def blend_cmyk_colors(colors: List[Tuple[float, float, float, float]], weights: List[float]) -> Tuple[float, float, float, float]:
        """Blendt meerdere CMYK kleuren met gewichten."""
        if not colors or not weights or len(colors) != len(weights):
            return 0.0, 0.0, 0.0, 0.0
        
        # Normaliseer gewichten
        total_weight = sum(weights)
        if total_weight == 0:
            return 0.0, 0.0, 0.0, 0.0
        
        weights = [w/total_weight for w in weights]
        
        # Bereken gewogen gemiddelde
        c = sum(color[0] * weight for color, weight in zip(colors, weights))
        m = sum(color[1] * weight for color, weight in zip(colors, weights))
        y = sum(color[2] * weight for color, weight in zip(colors, weights))
        k = sum(color[3] * weight for color, weight in zip(colors, weights))
        
        return c, m, y, k

# Voorbeeld gebruik
if __name__ == "__main__":
    converter = ColorConverter()
    
    # Test RGB naar CMYK conversie
    rgb_color = (255, 0, 0)  # Rood
    cmyk = converter.rgb_to_cmyk(*rgb_color)
    print(f"RGB {rgb_color} -> CMYK {cmyk}")
    
    # Test emotionele CMYK berekening
    emotions = {
        'blij': 0.8,
        'kwaad': 0.2,
        'verward': 0.3,
        'overweldigd': 0.1
    }
    emotional_cmyk = converter.calculate_emotional_cmyk(emotions)
    print(f"Emotionele CMYK: {emotional_cmyk}")
    
    # Test kleur blending
    colors = [
        (1.0, 0.0, 0.0, 0.0),  # Cyan
        (0.0, 1.0, 0.0, 0.0),  # Magenta
        (0.0, 0.0, 1.0, 0.0)   # Yellow
    ]
    weights = [0.3, 0.3, 0.4]
    blended = converter.blend_cmyk_colors(colors, weights)
    print(f"Geblende CMYK: {blended}") 