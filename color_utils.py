from typing import Tuple, Dict, List
import numpy as np

class ColorConverter:
    # CIE 1976 LAB constants
    LAB_E = 0.008856
    LAB_K = 903.3
    LAB_WHITE = (0.95047, 1.0, 1.08883)  # D65 illuminant

    @staticmethod
    def _lab_f(t: float) -> float:
        """Helper function for LAB conversion."""
        if t > ColorConverter.LAB_E:
            return t ** (1/3)
        return (ColorConverter.LAB_K * t + 16) / 116

    @staticmethod
    def _lab_inv_f(t: float) -> float:
        """Inverse helper function for LAB conversion."""
        if t > ColorConverter.LAB_E:
            return t ** 3
        return (t - 16/116) / ColorConverter.LAB_K

    @staticmethod
    def rgb_to_xyz(r: int, g: int, b: int) -> Tuple[float, float, float]:
        """Converts RGB to XYZ color space."""
        # Normalize RGB values
        r, g, b = r/255.0, g/255.0, b/255.0
        
        # Convert to linear RGB
        r = r/12.92 if r <= 0.04045 else ((r + 0.055)/1.055) ** 2.4
        g = g/12.92 if g <= 0.04045 else ((g + 0.055)/1.055) ** 2.4
        b = b/12.92 if b <= 0.04045 else ((b + 0.055)/1.055) ** 2.4
        
        # Convert to XYZ
        x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
        y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
        z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041
        
        return x, y, z

    @staticmethod
    def xyz_to_lab(x: float, y: float, z: float) -> Tuple[float, float, float]:
        """Converts XYZ to LAB color space."""
        # Normalize by white point
        x = x / ColorConverter.LAB_WHITE[0]
        y = y / ColorConverter.LAB_WHITE[1]
        z = z / ColorConverter.LAB_WHITE[2]
        
        # Calculate LAB values
        fx = ColorConverter._lab_f(x)
        fy = ColorConverter._lab_f(y)
        fz = ColorConverter._lab_f(z)
        
        l = 116 * fy - 16
        a = 500 * (fx - fy)
        b = 200 * (fy - fz)
        
        return l, a, b

    @staticmethod
    def lab_to_xyz(l: float, a: float, b: float) -> Tuple[float, float, float]:
        """Converts LAB to XYZ color space."""
        # Calculate intermediate values
        fy = (l + 16) / 116
        fx = a / 500 + fy
        fz = fy - b / 200
        
        # Convert to XYZ
        x = ColorConverter.LAB_WHITE[0] * ColorConverter._lab_inv_f(fx)
        y = ColorConverter.LAB_WHITE[1] * ColorConverter._lab_inv_f(fy)
        z = ColorConverter.LAB_WHITE[2] * ColorConverter._lab_inv_f(fz)
        
        return x, y, z

    @staticmethod
    def xyz_to_rgb(x: float, y: float, z: float) -> Tuple[int, int, int]:
        """Converts XYZ to RGB color space."""
        # Convert to linear RGB
        r = x * 3.2404542 - y * 1.5371385 - z * 0.4985314
        g = -x * 0.9692660 + y * 1.8760108 + z * 0.0415560
        b = x * 0.0556434 - y * 0.2040259 + z * 1.0572252
        
        # Convert to non-linear RGB
        r = 12.92 * r if r <= 0.0031308 else 1.055 * (r ** (1/2.4)) - 0.055
        g = 12.92 * g if g <= 0.0031308 else 1.055 * (g ** (1/2.4)) - 0.055
        b = 12.92 * b if b <= 0.0031308 else 1.055 * (b ** (1/2.4)) - 0.055
        
        # Convert to 8-bit RGB
        r = max(0, min(255, int(round(r * 255))))
        g = max(0, min(255, int(round(g * 255))))
        b = max(0, min(255, int(round(b * 255))))
        
        return r, g, b

    @staticmethod
    def rgb_to_lab(r: int, g: int, b: int) -> Tuple[float, float, float]:
        """Converts RGB to LAB color space."""
        x, y, z = ColorConverter.rgb_to_xyz(r, g, b)
        return ColorConverter.xyz_to_lab(x, y, z)

    @staticmethod
    def lab_to_rgb(l: float, a: float, b: float) -> Tuple[int, int, int]:
        """Converts LAB to RGB color space."""
        x, y, z = ColorConverter.lab_to_xyz(l, a, b)
        return ColorConverter.xyz_to_rgb(x, y, z)

    @staticmethod
    def calculate_chroma(a: float, b: float) -> float:
        """Calculates chroma (colorfulness) from LAB a* and b* values."""
        return np.sqrt(a*a + b*b)

    @staticmethod
    def calculate_hue_angle(a: float, b: float) -> float:
        """Calculates hue angle from LAB a* and b* values in degrees."""
        return np.degrees(np.arctan2(b, a)) % 360

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

    @staticmethod
    def generate_analogous_palette(l: float, a: float, b: float, num_colors: int = 5) -> List[Tuple[float, float, float]]:
        """Generate an analogous color palette in LAB space."""
        palette = []
        hue_angle = ColorConverter.calculate_hue_angle(a, b)
        chroma = ColorConverter.calculate_chroma(a, b)
        
        # Generate colors with same lightness and chroma but different hue angles
        angle_step = 30.0 / (num_colors - 1)
        for i in range(num_colors):
            new_angle = (hue_angle + (i - num_colors//2) * angle_step) % 360
            new_a = chroma * np.cos(np.radians(new_angle))
            new_b = chroma * np.sin(np.radians(new_angle))
            palette.append((l, new_a, new_b))
        
        return palette

    @staticmethod
    def generate_complementary_palette(l: float, a: float, b: float) -> List[Tuple[float, float, float]]:
        """Generate a complementary color palette in LAB space."""
        hue_angle = ColorConverter.calculate_hue_angle(a, b)
        chroma = ColorConverter.calculate_chroma(a, b)
        
        # Generate complementary color (180 degrees opposite)
        comp_angle = (hue_angle + 180) % 360
        comp_a = chroma * np.cos(np.radians(comp_angle))
        comp_b = chroma * np.sin(np.radians(comp_angle))
        
        return [(l, a, b), (l, comp_a, comp_b)]

    @staticmethod
    def generate_triadic_palette(l: float, a: float, b: float) -> List[Tuple[float, float, float]]:
        """Generate a triadic color palette in LAB space."""
        hue_angle = ColorConverter.calculate_hue_angle(a, b)
        chroma = ColorConverter.calculate_chroma(a, b)
        
        # Generate two additional colors (120 degrees apart)
        angles = [hue_angle, (hue_angle + 120) % 360, (hue_angle + 240) % 360]
        palette = []
        
        for angle in angles:
            new_a = chroma * np.cos(np.radians(angle))
            new_b = chroma * np.sin(np.radians(angle))
            palette.append((l, new_a, new_b))
        
        return palette

    @staticmethod
    def generate_emotion_palette(emotions: Dict[str, float], num_colors: int = 5) -> List[Tuple[float, float, float]]:
        """Generate a color palette based on emotional scores."""
        # Map emotions to LAB color ranges
        emotion_to_lab = {
            'blij': (70, 20, 60),      # Bright yellow
            'kwaad': (50, 60, -20),    # Deep red
            'verdriet': (40, -20, -40), # Deep blue
            'gelukkig': (80, 10, 40),   # Light yellow
            'neutraal': (60, 0, 0),     # Gray
            'verward': (50, -30, 30),   # Purple
            'overweldigd': (30, 0, 0)   # Dark gray
        }
        
        # Calculate weighted average LAB values
        total_weight = sum(emotions.values())
        if total_weight == 0:
            return [(60, 0, 0)] * num_colors  # Default to neutral gray
        
        weighted_lab = [0, 0, 0]
        for emotion, weight in emotions.items():
            if emotion in emotion_to_lab:
                lab = emotion_to_lab[emotion]
                weighted_lab[0] += lab[0] * weight
                weighted_lab[1] += lab[1] * weight
                weighted_lab[2] += lab[2] * weight
        
        weighted_lab = [v/total_weight for v in weighted_lab]
        
        # Generate palette variations
        return ColorConverter.generate_analogous_palette(*weighted_lab, num_colors)

    @staticmethod
    def check_color_contrast(lab1: Tuple[float, float, float], lab2: Tuple[float, float, float]) -> float:
        """Calculate color contrast ratio between two LAB colors."""
        # Convert LAB to RGB
        rgb1 = ColorConverter.lab_to_rgb(*lab1)
        rgb2 = ColorConverter.lab_to_rgb(*lab2)
        
        # Calculate relative luminance
        def get_luminance(rgb):
            r, g, b = [c/255 for c in rgb]
            r = r/12.92 if r <= 0.03928 else ((r + 0.055)/1.055) ** 2.4
            g = g/12.92 if g <= 0.03928 else ((g + 0.055)/1.055) ** 2.4
            b = b/12.92 if b <= 0.03928 else ((b + 0.055)/1.055) ** 2.4
            return 0.2126 * r + 0.7152 * g + 0.0722 * b
        
        l1 = get_luminance(rgb1)
        l2 = get_luminance(rgb2)
        
        # Calculate contrast ratio
        lighter = max(l1, l2)
        darker = min(l1, l2)
        return (lighter + 0.05) / (darker + 0.05)

    @staticmethod
    def simulate_color_blindness(lab: Tuple[float, float, float], type: str = 'deuteranopia') -> Tuple[float, float, float]:
        """Simulate color blindness for a LAB color."""
        # Convert LAB to RGB
        rgb = ColorConverter.lab_to_rgb(*lab)
        r, g, b = rgb
        
        # Color blindness simulation matrices
        matrices = {
            'protanopia': [
                [0.567, 0.433, 0],
                [0.558, 0.442, 0],
                [0, 0.242, 0.758]
            ],
            'deuteranopia': [
                [0.625, 0.375, 0],
                [0.7, 0.3, 0],
                [0, 0.3, 0.7]
            ],
            'tritanopia': [
                [0.95, 0.05, 0],
                [0, 0.433, 0.567],
                [0, 0.475, 0.525]
            ]
        }
        
        if type not in matrices:
            return lab
        
        # Apply color blindness simulation
        matrix = matrices[type]
        new_r = r * matrix[0][0] + g * matrix[0][1] + b * matrix[0][2]
        new_g = r * matrix[1][0] + g * matrix[1][1] + b * matrix[1][2]
        new_b = r * matrix[2][0] + g * matrix[2][1] + b * matrix[2][2]
        
        # Convert back to LAB
        return ColorConverter.rgb_to_lab(int(new_r), int(new_g), int(new_b))

    @staticmethod
    def lab_to_hex(l: float, a: float, b: float) -> str:
        """Converts LAB to hex color."""
        r, g, b = ColorConverter.lab_to_rgb(l, a, b)
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)

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