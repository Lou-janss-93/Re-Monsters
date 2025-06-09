import json
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Color:
    hex: str
    cmyk: List[float]
    weight: float

class ColorAgentCore:
    def __init__(self, config_path: str = "color_config.json"):
        self.config_path = config_path
        self.colors = self._load_colors()
        
    def _load_colors(self) -> Dict[str, Dict]:
        with open(self.config_path, 'r') as f:
            return json.load(f)['colors']
    
    def get_color(self, color_name: str, tint: str = "medium") -> Color:
        """Get a specific color and tint combination."""
        if color_name not in self.colors:
            raise ValueError(f"Color {color_name} not found in configuration")
        
        color_data = self.colors[color_name]
        if tint not in color_data['sub_tints']:
            raise ValueError(f"Tint {tint} not found for color {color_name}")
        
        tint_data = color_data['sub_tints'][tint]
        return Color(
            hex=tint_data['hex'],
            cmyk=tint_data['cmyk'],
            weight=tint_data['weight']
        )
    
    def get_all_colors(self) -> Dict[str, Dict[str, Color]]:
        """Get all colors and their tints."""
        result = {}
        for color_name, color_data in self.colors.items():
            result[color_name] = {
                tint: Color(
                    hex=tint_data['hex'],
                    cmyk=tint_data['cmyk'],
                    weight=tint_data['weight']
                )
                for tint, tint_data in color_data['sub_tints'].items()
            }
        return result
    
    def mix_colors(self, color1: Color, color2: Color, ratio: float = 0.5) -> Color:
        """Mix two colors using CMYK values."""
        # Convert CMYK to RGB for mixing
        rgb1 = self._cmyk_to_rgb(color1.cmyk)
        rgb2 = self._cmyk_to_rgb(color2.cmyk)
        
        # Mix RGB values
        mixed_rgb = [
            rgb1[i] * (1 - ratio) + rgb2[i] * ratio
            for i in range(3)
        ]
        
        # Convert back to CMYK
        mixed_cmyk = self._rgb_to_cmyk(mixed_rgb)
        
        # Calculate mixed weight
        mixed_weight = color1.weight * (1 - ratio) + color2.weight * ratio
        
        # Convert RGB to hex
        mixed_hex = self._rgb_to_hex(mixed_rgb)
        
        return Color(
            hex=mixed_hex,
            cmyk=mixed_cmyk,
            weight=mixed_weight
        )
    
    def _cmyk_to_rgb(self, cmyk: List[float]) -> List[float]:
        """Convert CMYK to RGB values."""
        c, m, y, k = cmyk
        r = 255 * (1 - c) * (1 - k)
        g = 255 * (1 - m) * (1 - k)
        b = 255 * (1 - y) * (1 - k)
        return [r/255, g/255, b/255]
    
    def _rgb_to_cmyk(self, rgb: List[float]) -> List[float]:
        """Convert RGB to CMYK values."""
        r, g, b = rgb
        
        # Convert to 0-1 range
        r, g, b = r, g, b
        
        # Calculate K (black)
        k = 1 - max(r, g, b)
        
        if k == 1:
            return [0, 0, 0, 1]
        
        # Calculate CMY
        c = (1 - r - k) / (1 - k)
        m = (1 - g - k) / (1 - k)
        y = (1 - b - k) / (1 - k)
        
        return [c, m, y, k]
    
    def _rgb_to_hex(self, rgb: List[float]) -> str:
        """Convert RGB to hex color code."""
        r, g, b = [int(x * 255) for x in rgb]
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def get_complementary_color(self, color: Color) -> Color:
        """Get the complementary color using CMYK values."""
        # Convert to RGB
        rgb = self._cmyk_to_rgb(color.cmyk)
        
        # Calculate complementary RGB
        comp_rgb = [1 - x for x in rgb]
        
        # Convert back to CMYK
        comp_cmyk = self._rgb_to_cmyk(comp_rgb)
        
        # Convert to hex
        comp_hex = self._rgb_to_hex(comp_rgb)
        
        return Color(
            hex=comp_hex,
            cmyk=comp_cmyk,
            weight=color.weight
        )
    
    def get_analogous_colors(self, color: Color, num_colors: int = 2) -> List[Color]:
        """Get analogous colors by rotating the hue in CMYK space."""
        # Convert to RGB
        rgb = self._cmyk_to_rgb(color.cmyk)
        
        # Convert RGB to HSV
        h, s, v = self._rgb_to_hsv(rgb)
        
        # Calculate analogous colors
        analogous_colors = []
        for i in range(num_colors):
            # Rotate hue by 30 degrees
            new_h = (h + (i + 1) * 30) % 360
            new_rgb = self._hsv_to_rgb(new_h, s, v)
            new_cmyk = self._rgb_to_cmyk(new_rgb)
            new_hex = self._rgb_to_hex(new_rgb)
            
            analogous_colors.append(Color(
                hex=new_hex,
                cmyk=new_cmyk,
                weight=color.weight
            ))
        
        return analogous_colors
    
    def _rgb_to_hsv(self, rgb: List[float]) -> Tuple[float, float, float]:
        """Convert RGB to HSV."""
        r, g, b = rgb
        
        max_val = max(r, g, b)
        min_val = min(r, g, b)
        delta = max_val - min_val
        
        # Calculate hue
        if delta == 0:
            h = 0
        elif max_val == r:
            h = 60 * (((g - b) / delta) % 6)
        elif max_val == g:
            h = 60 * (((b - r) / delta) + 2)
        else:
            h = 60 * (((r - g) / delta) + 4)
        
        # Calculate saturation
        s = 0 if max_val == 0 else delta / max_val
        
        # Value is the maximum
        v = max_val
        
        return h, s, v
    
    def _hsv_to_rgb(self, h: float, s: float, v: float) -> List[float]:
        """Convert HSV to RGB."""
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c
        
        if 0 <= h < 60:
            rgb = [c, x, 0]
        elif 60 <= h < 120:
            rgb = [x, c, 0]
        elif 120 <= h < 180:
            rgb = [0, c, x]
        elif 180 <= h < 240:
            rgb = [0, x, c]
        elif 240 <= h < 300:
            rgb = [x, 0, c]
        else:
            rgb = [c, 0, x]
        
        return [r + m for r in rgb]
