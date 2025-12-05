"""
Generate EditalShield Demo Animation (Cyberpunk Style)
Creates a Neon-Glow GIF showing the scanning process
"""

import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import os
import mplcyberpunk
from matplotlib.projections import register_projection
from matplotlib.projections.polar import PolarAxes
from matplotlib.patches import Circle

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
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
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

    register_projection(RadarAxes)
    return theta

def generate_animation():
    if not os.path.exists('docs/images'):
        os.makedirs('docs/images')

    # Use Cyberpunk style
    plt.style.use("cyberpunk")

    labels = ['Entropy', 'Zipf Deviation', 'Patterns', 'Bayes Risk', 'Tech Density']
    num_vars = len(labels)
    theta = radar_factory(num_vars, frame='polygon')

    # Animation phases
    steps = 20
    phase1 = np.linspace(0.1, 0.2, 5)   # Idle
    phase2 = np.linspace(0.2, 0.95, 12) # Scanning (High Risk)
    phase3 = np.linspace(0.95, 0.1, 12) # Protecting
    
    all_values = np.concatenate([phase1, phase2, phase3])
    filenames = []
    
    for i, val in enumerate(all_values):
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='radar'))
        fig.subplots_adjust(top=0.85, bottom=0.05)
        
        # Dynamic data with noise
        current_data = [
            min(1.0, val + np.random.uniform(-0.05, 0.05)),
            min(1.0, val * 0.9 + np.random.uniform(-0.05, 0.05)),
            min(1.0, val * 1.1 + np.random.uniform(-0.05, 0.05)) if i < 17 else 0.05,
            min(1.0, val + np.random.uniform(-0.05, 0.05)),
            min(1.0, val * 0.8 + np.random.uniform(-0.05, 0.05))
        ]
        
        # Dynamic Colors (Neon)
        risk_level = np.mean(current_data)
        if i >= 17: # Protected
            color = 'cyan'
            status = "PROTECTED"
            glow_color = 'cyan'
        elif risk_level < 0.4:
            color = 'lime'
            status = "SAFE"
            glow_color = 'lime'
        elif risk_level < 0.7:
            color = 'yellow'
            status = "ANALYZING..."
            glow_color = 'yellow'
        else:
            color = 'deeppink' # Cyberpunk Red/Pink
            status = "RISK DETECTED"
            glow_color = 'deeppink'

        # Plot with Glow
        ax.plot(theta, current_data, color=color, linewidth=2)
        ax.fill(theta, current_data, facecolor=color, alpha=0.2)
        
        # Add Glow Effect manually (since mplcyberpunk doesn't fully support polar yet)
        for n in range(1, 4):
            ax.plot(theta, current_data, color=color, linewidth=2 + 2*n, alpha=0.2/n)

        ax.set_varlabels(labels)
        ax.set_rgrids([0.2, 0.4, 0.6, 0.8], labels=[]) # Hide grid labels for cleaner look
        ax.grid(color='#444444', alpha=0.5) # Subtle grid
        
        # Title and Status
        ax.set_title("EDITALSHIELD // SCANNER", weight='bold', size=18, color='white', position=(0.5, 1.1))
        plt.figtext(0.5, 0.9, f"[{status}]", ha='center', color=color, weight='bold', size=14)
        
        # Save frame
        filename = f'docs/images/frame_{i}.png'
        plt.savefig(filename, facecolor='#212946') # Cyberpunk background
        filenames.append(filename)
        plt.close()

    # Build GIF
    with imageio.get_writer('docs/images/demo.gif', mode='I', duration=0.15, loop=0) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
            
    # Cleanup
    for filename in filenames:
        os.remove(filename)
        
    print("Cyberpunk animation generated at docs/images/demo.gif")

if __name__ == "__main__":
    generate_animation()
