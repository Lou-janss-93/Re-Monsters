import streamlit as st
import numpy as np
import plotly.graph_objects as go
from agent_white import AgentWhite
from color_utils import ColorConverter
from typing import Tuple, List
import colorsys

def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_lab(rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
    """Convert RGB to CIELAB color space."""
    # Convert RGB to XYZ
    r, g, b = [x/255.0 for x in rgb]
    
    # Convert to sRGB
    r = r/12.92 if r <= 0.04045 else ((r + 0.055)/1.055)**2.4
    g = g/12.92 if g <= 0.04045 else ((g + 0.055)/1.055)**2.4
    b = b/12.92 if b <= 0.04045 else ((b + 0.055)/1.055)**2.4
    
    # Convert to XYZ
    x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
    y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
    z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041
    
    # Convert to Lab
    x = x/0.95047
    y = y/1.00000
    z = z/1.08883
    
    x = x**(1/3) if x > 0.008856 else (7.787 * x) + 16/116
    y = y**(1/3) if y > 0.008856 else (7.787 * y) + 16/116
    z = z**(1/3) if z > 0.008856 else (7.787 * z) + 16/116
    
    L = (116 * y) - 16
    a = 500 * (x - y)
    b = 200 * (y - z)
    
    return L, a, b

def create_lab_visualization(colors: List[Tuple[str, float]]) -> go.Figure:
    """Create a 3D visualization of colors in CIELAB space."""
    # Convert colors to LAB
    lab_points = []
    for hex_color, weight in colors:
        rgb = hex_to_rgb(hex_color)
        lab = rgb_to_lab(rgb)
        lab_points.append((*lab, weight))
    
    # Create 3D scatter plot
    fig = go.Figure(data=[go.Scatter3d(
        x=[p[1] for p in lab_points],  # a*
        y=[p[2] for p in lab_points],  # b*
        z=[p[0] for p in lab_points],  # L*
        mode='markers',
        marker=dict(
            size=[p[3] * 10 for p in lab_points],  # Scale size by weight
            color=[hex_color for hex_color, _ in colors],
            opacity=0.8
        ),
        text=[f"L*: {p[0]:.1f}<br>a*: {p[1]:.1f}<br>b*: {p[2]:.1f}" for p in lab_points],
        hoverinfo='text'
    )])
    
    # Update layout
    fig.update_layout(
        title='CIELAB Color Space Visualization',
        scene=dict(
            xaxis_title='a* (green-red)',
            yaxis_title='b* (blue-yellow)',
            zaxis_title='L* (lightness)',
            xaxis=dict(range=[-128, 128]),
            yaxis=dict(range=[-128, 128]),
            zaxis=dict(range=[0, 100])
        ),
        showlegend=False
    )
    
    return fig

def main():
    st.title("🧠 Re-Monster Color Agent")
    st.write("Test de Re-Monster Color Agent met eigen input en bekijk de kleuranalyse in CIELAB ruimte.")
    
    # Initialize Agent White
    agent = AgentWhite()
    
    # Text input
    user_input = st.text_area("Voer je tekst in:", "Ik ben erg blij met het resultaat!")
    
    if st.button("Analyseer"):
        # Get response from Agent White
        response = agent.calculate_balanced_response(user_input)
        
        # Display results
        st.subheader("Resultaten")
        st.write(f"Regenboogvector: {response['rainbow_vector']}")
        st.write(f"Strategie: {response['strategy']}")
        
        # Display dominant emotions
        st.write("Dominante emoties:")
        for emotion, score in response['dominant_emotions'].items():
            st.write(f"- {emotion}: {score:.2f}")
        
        # Create color list for visualization
        colors = []
        for color, feedback in response['agent_feedbacks'].items():
            if feedback['confidence'] > 0:
                colors.append((feedback['color'], feedback['confidence']))
        
        # Add the rainbow vector
        colors.append((response['rainbow_vector'], 1.0))
        
        # Create and display CIELAB visualization
        st.subheader("CIELAB Kleurruimte Visualisatie")
        fig = create_lab_visualization(colors)
        st.plotly_chart(fig)
        
        # Display agent feedback
        st.subheader("Agent Feedback")
        for color, feedback in response['agent_feedbacks'].items():
            if feedback['confidence'] > 0:
                st.write(f"\n{color.upper()} Agent:")
                st.write(f"Confidence: {feedback['confidence']:.2f}")
                st.write(f"Suggestion: {feedback['suggestion']}")
                st.write("Emoties:", feedback['emotion_scores'])

if __name__ == "__main__":
    main() 