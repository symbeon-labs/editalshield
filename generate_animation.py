"""
Generate EditalShield Demo Animation
Creates a GIF showing the scanning process and metrics
"""

import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import os
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D

def radar_factory(num_vars, frame='circle'):
    """Create a radar chart with `num_vars` axes."""
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    class RadarAxes(PolarAxes):
        name = 'radar'
        RESOLUTION = 1

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            return Circle((0.5, 0.5), 0.5)

        def _gen_axes_spines(self):
            return super()._gen_axes_spines()

    register_projection(RadarAxes)
    return theta

def generate_animation():
    if not os.path.exists('docs/images'):
        os.makedirs('docs/images')

    # Data for animation
    labels = ['Entropy', 'Zipf Deviation', 'Sensitive Patterns', 'Bayesian Risk', 'Technical Density']
    num_vars = len(labels)
    theta = radar_factory(num_vars, frame='polygon')

    # Simulation steps (Safe -> Risk -> Protected)
    steps = 20
    
    # Phase 1: Safe Text (Low metrics)
    phase1 = np.linspace(0.1, 0.2, 5)
    # Phase 2: Scanning Risk (Metrics rising)
    phase2 = np.linspace(0.2, 0.9, 10)
    # Phase 3: Protected (Metrics dropping)
    phase3 = np.linspace(0.9, 0.15, 10)
    
    all_values = np.concatenate([phase1, phase2, phase3])
    
    filenames = []
    
    for i, val in enumerate(all_values):
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='radar'))
        fig.subplots_adjust(top=0.85, bottom=0.05)
        
        # Add some noise/variation to each metric
        current_data = [
            min(1.0, val + np.random.uniform(-0.05, 0.05)), # Entropy
            min(1.0, val * 0.8 + np.random.uniform(-0.05, 0.05)), # Zipf
            min(1.0, val * 1.1 + np.random.uniform(-0.05, 0.05)) if i < 15 else 0.1, # Patterns (drops fast on protect)
            min(1.0, val + np.random.uniform(-0.05, 0.05)), # Risk
            min(1.0, val * 0.9 + np.random.uniform(-0.05, 0.05)) # Tech Density
        ]
        
        # Color based on risk
        risk_level = np.mean(current_data)
        if risk_level < 0.4:
            color = '#00ff00' # Green
            status = "SAFE"
        elif risk_level < 0.7:
            color = '#ffff00' # Yellow
            status = "ANALYZING..."
        else:
            color = '#ff0000' # Red
            status = "RISK DETECTED!"
            
        if i >= 15: # Protection phase
            color = '#00ccff' # Blue
            status = "PROTECTED"

        ax.set_rgrids([0.2, 0.4, 0.6, 0.8])
        ax.set_title("EditalShield Scanner", weight='bold', size=20, position=(0.5, 1.1))
        
        ax.plot(theta, current_data, color=color)
        ax.fill(theta, current_data, facecolor=color, alpha=0.25)
        ax.set_varlabels(labels)
        
        # Add status text
        plt.figtext(0.5, 0.9, f"STATUS: {status}", ha='center', color=color, weight='bold', size=14)
        
        # Save frame
        filename = f'docs/images/frame_{i}.png'
        plt.savefig(filename, facecolor='#1e1e1e', edgecolor='none') # Dark mode bg
        filenames.append(filename)
        plt.close()

    # Build GIF
    with imageio.get_writer('docs/images/demo.gif', mode='I', duration=0.2, loop=0) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
            
    # Cleanup frames
    for filename in filenames:
        os.remove(filename)
        
    print("Animation generated at docs/images/demo.gif")

if __name__ == "__main__":
    generate_animation()
