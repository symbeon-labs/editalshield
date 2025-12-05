"""
Generate EditalShield Demo Animation (Cyberpunk HUD Style)
Creates a split-screen GIF: Radar Scanner + Juridical AI Agent Log
"""

import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import os
import mplcyberpunk
from matplotlib.projections import register_projection
from matplotlib.projections.polar import PolarAxes
from matplotlib import gridspec

def radar_factory(num_vars, frame='circle'):
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

def get_agent_log(step, total_steps):
    """Returns the log messages for the Juridical AI Agent based on the current step"""
    
    logs = [
        "[SYSTEM] Initializing EditalShield Core v0.2.1...",
        "[SYSTEM] Loading Brazilian IP Law (LPI 9.279/96)...",
        "[AGENT]  Ready. Waiting for input stream...",
        "[AGENT]  > Reading 'memorial_tecnico_v1.pdf'...",
        "[AGENT]  > Segmenting paragraphs...",
        "[METRIC] Shannon Entropy calculation started.",
        "[METRIC] Zipfian Deviation analysis running...",
        "[ALERT]  ⚠️ ANOMALY DETECTED in Paragraph 4.",
        "[ALERT]  High technical density (Zipf Score: 0.92).",
        "[RISK]   Pattern Match: 'BehaviorAnalyzer V2' (Algorithm).",
        "[RISK]   Pattern Match: 'W=0.7, K=1.5' (Parameters).",
        "[LEGAL]  VIOLATION RISK: Trade Secret Exposure.",
        "[LEGAL]  Recommendation: Immediate obfuscation.",
        "[ACTION] Initiating Protection Protocol...",
        "[ACTION] Replacing sensitive terms...",
        "[ACTION] Generating generic descriptors...",
        "[CHECK]  Re-scanning document...",
        "[CHECK]  Entropy normalized. Zipf score stable.",
        "[FINAL]  Document is COMPLIANT.",
        "[SYSTEM] SAFE VERSION SAVED."
    ]
    
    # Return the logs up to the current step (scaled to fit animation length)
    idx = int((step / total_steps) * len(logs))
    return logs[max(0, idx-8):idx+1] # Show last 8 lines

def generate_animation():
    if not os.path.exists('docs/images'):
        os.makedirs('docs/images')

    plt.style.use("cyberpunk")
    
    # Setup Data
    labels = ['Entropy', 'Zipf Score', 'Patterns', 'Risk', 'Density']
    num_vars = len(labels)
    theta = radar_factory(num_vars, frame='polygon')

    # Animation phases
    steps = 40 # More frames for reading time
    phase1 = np.linspace(0.1, 0.2, 8)    # Init
    phase2 = np.linspace(0.2, 0.95, 16)  # Risk Rising
    phase3 = np.linspace(0.95, 0.15, 16) # Protecting
    
    all_values = np.concatenate([phase1, phase2, phase3])
    filenames = []
    
    for i, val in enumerate(all_values):
        # Create Layout: Left (Radar), Right (Terminal)
        fig = plt.figure(figsize=(12, 6))
        gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1])
        
        # --- LEFT: RADAR CHART ---
        ax = fig.add_subplot(gs[0], projection='radar')
        
        # Dynamic data
        current_data = [
            min(1.0, val + np.random.uniform(-0.05, 0.05)),
            min(1.0, val * 0.9 + np.random.uniform(-0.05, 0.05)),
            min(1.0, val * 1.1 + np.random.uniform(-0.05, 0.05)) if i < 24 else 0.05,
            min(1.0, val + np.random.uniform(-0.05, 0.05)),
            min(1.0, val * 0.8 + np.random.uniform(-0.05, 0.05))
        ]
        
        # Colors
        risk_level = np.mean(current_data)
        if i >= 24: # Protected
            color = 'cyan'
            status = "PROTECTED"
        elif risk_level < 0.4:
            color = 'lime'
            status = "SAFE"
        elif risk_level < 0.7:
            color = 'yellow'
            status = "ANALYZING"
        else:
            color = 'deeppink'
            status = "RISK DETECTED"

        ax.plot(theta, current_data, color=color, linewidth=2)
        ax.fill(theta, current_data, facecolor=color, alpha=0.2)
        
        # Glow effect manually
        for n in range(1, 4):
            ax.plot(theta, current_data, color=color, linewidth=2 + 2*n, alpha=0.2/n)

        ax.set_varlabels(labels)
        ax.set_rgrids([0.2, 0.4, 0.6, 0.8], labels=[])
        ax.grid(color='#444444', alpha=0.5)
        ax.set_title(f"SCANNER // STATUS: {status}", color=color, weight='bold', size=14, pad=20)

        # --- RIGHT: JURIDICAL AGENT TERMINAL ---
        ax_log = fig.add_subplot(gs[1])
        ax_log.set_facecolor('#1a1a1a') # Slightly darker terminal
        ax_log.axis('off')
        
        # Terminal Border
        rect = plt.Rectangle((0, 0), 1, 1, transform=ax_log.transAxes, 
                             color=color, fill=False, linewidth=2)
        ax_log.add_patch(rect)
        
        # Header
        ax_log.text(0.05, 0.92, "AI JURIDICAL AGENT // LOG", 
                    color='white', weight='bold', size=12, transform=ax_log.transAxes)
        ax_log.axhline(y=0.88, xmin=0.02, xmax=0.98, color=color, linewidth=1)
        
        # Log Messages
        logs = get_agent_log(i, len(all_values))
        for idx, line in enumerate(logs):
            # Colorize based on content
            msg_color = '#00ff00' # Default green
            if "[ALERT]" in line or "[RISK]" in line: msg_color = '#ff0055' # Red
            if "[SYSTEM]" in line: msg_color = '#00ccff' # Blue
            if "[LEGAL]" in line: msg_color = '#ffff00' # Yellow
            
            ax_log.text(0.05, 0.80 - (idx * 0.08), line, 
                        color=msg_color, fontfamily='monospace', size=10, 
                        transform=ax_log.transAxes)

        # Save frame
        filename = f'docs/images/frame_{i}.png'
        plt.savefig(filename, facecolor='#212946')
        filenames.append(filename)
        plt.close()

    # Build GIF
    with imageio.get_writer('docs/images/demo.gif', mode='I', duration=0.15, loop=0) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
            
    for filename in filenames:
        os.remove(filename)
        
    print("HUD Animation generated at docs/images/demo.gif")

if __name__ == "__main__":
    generate_animation()
