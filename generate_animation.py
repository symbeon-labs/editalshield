"""
Generate EditalShield Demo Animation (Cyberpunk HUD v2)
Features: Rotating Radar Scan Line, Timestamps, and Enhanced Glow
"""

import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import os
import datetime
from matplotlib.projections import register_projection
from matplotlib.projections.polar import PolarAxes
from matplotlib import gridspec
from matplotlib.patches import Wedge

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

def get_timestamp(frame_idx):
    """Generate a fake timestamp progressing with frames"""
    base_time = datetime.datetime(2025, 12, 4, 14, 30, 0)
    delta = datetime.timedelta(milliseconds=frame_idx * 200)
    return (base_time + delta).strftime("%H:%M:%S.%f")[:-3]

def get_agent_log(step, total_steps):
    """Returns the log messages with timestamps"""
    
    raw_logs = [
        ("SYS", "Initializing EditalShield Core v0.2.1..."),
        ("SYS", "Loading Brazilian IP Law (LPI 9.279/96)..."),
        ("AGT", "Ready. Waiting for input stream..."),
        ("AGT", "Reading 'memorial_tecnico_v1.pdf'..."),
        ("AGT", "Segmenting paragraphs..."),
        ("MET", "Shannon Entropy calculation started."),
        ("MET", "Zipfian Deviation analysis running..."),
        ("WRN", "⚠️ ANOMALY DETECTED in Paragraph 4."),
        ("WRN", "High technical density (Zipf Score: 0.92)."),
        ("RSK", "Pattern Match: 'BehaviorAnalyzer V2' (Algo)."),
        ("RSK", "Pattern Match: 'W=0.7, K=1.5' (Params)."),
        ("LEG", "VIOLATION RISK: Trade Secret Exposure."),
        ("LEG", "Recommendation: Immediate obfuscation."),
        ("ACT", "Initiating Protection Protocol..."),
        ("ACT", "Replacing sensitive terms..."),
        ("ACT", "Generating generic descriptors..."),
        ("CHK", "Re-scanning document..."),
        ("CHK", "Entropy normalized. Zipf score stable."),
        ("FIN", "Document is COMPLIANT."),
        ("SYS", "SAFE VERSION SAVED.")
    ]
    
    idx = int((step / total_steps) * len(raw_logs))
    visible_logs = raw_logs[max(0, idx-9):idx+1]
    
    formatted_logs = []
    for i, (tag, msg) in enumerate(visible_logs):
        ts = get_timestamp(step - (len(visible_logs) - i) * 2)
        formatted_logs.append(f"[{ts}] [{tag}] {msg}")
        
    return formatted_logs

def generate_animation():
    if not os.path.exists('docs/images'):
        os.makedirs('docs/images')

    # Use standard dark background + manual cyberpunk effects
    plt.style.use("dark_background")
    
    labels = ['Entropy', 'Zipf Score', 'Patterns', 'Risk', 'Density']
    num_vars = len(labels)
    theta = radar_factory(num_vars, frame='polygon')

    steps = 50 
    phase1 = np.linspace(0.1, 0.2, 10)
    phase2 = np.linspace(0.2, 0.95, 20)
    phase3 = np.linspace(0.95, 0.15, 20)
    
    all_values = np.concatenate([phase1, phase2, phase3])
    filenames = []
    
    for i, val in enumerate(all_values):
        fig = plt.figure(figsize=(12, 6))
        gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1.2])
        fig.patch.set_facecolor('#0d1117') # GitHub Dark Mode Match
        
        # --- LEFT: RADAR CHART ---
        ax = fig.add_subplot(gs[0], projection='radar')
        ax.set_facecolor('#0d1117')
        
        # Dynamic data
        current_data = [
            min(1.0, val + np.random.uniform(-0.05, 0.05)),
            min(1.0, val * 0.9 + np.random.uniform(-0.05, 0.05)),
            min(1.0, val * 1.1 + np.random.uniform(-0.05, 0.05)) if i < 30 else 0.05,
            min(1.0, val + np.random.uniform(-0.05, 0.05)),
            min(1.0, val * 0.8 + np.random.uniform(-0.05, 0.05))
        ]
        
        # Colors
        risk_level = np.mean(current_data)
        if i >= 30: 
            color = '#00ffff' # Cyan
            status = "PROTECTED"
        elif risk_level < 0.4:
            color = '#00ff00' # Lime
            status = "SAFE"
        elif risk_level < 0.7:
            color = '#ffff00' # Yellow
            status = "ANALYZING"
        else:
            color = '#ff0055' # Neon Red
            status = "RISK DETECTED"

        # Plot Data
        ax.plot(theta, current_data, color=color, linewidth=2)
        ax.fill(theta, current_data, facecolor=color, alpha=0.2)
        
        # Glow
        for n in range(1, 4):
            ax.plot(theta, current_data, color=color, linewidth=2 + 2*n, alpha=0.15/n)

        # ROTATING SCAN LINE
        scan_angle = (i * (2*np.pi / 20)) % (2*np.pi)
        ax.plot([scan_angle, scan_angle], [0, 1], color='white', alpha=0.5, linewidth=1)
        # Scan sector (fading trail)
        wedge = Wedge((0.5, 0.5), 0.5, np.degrees(scan_angle)-15, np.degrees(scan_angle), 
                      color='white', alpha=0.1, transform=ax.transAxes)
        # Note: Wedge on polar axes is tricky, simplified line is safer for stability

        ax.set_varlabels(labels)
        ax.set_rgrids([0.2, 0.4, 0.6, 0.8], labels=[])
        ax.grid(color='#30363d', alpha=0.5) # GitHub border color
        ax.set_title(f"SCANNER // STATUS: {status}", color=color, weight='bold', size=14, pad=20)

        # --- RIGHT: TERMINAL ---
        ax_log = fig.add_subplot(gs[1])
        ax_log.set_facecolor('#0d1117')
        ax_log.axis('off')
        
        # Terminal Box
        rect = plt.Rectangle((0, 0), 1, 1, transform=ax_log.transAxes, 
                             color='#30363d', fill=True, facecolor='#161b22', linewidth=1)
        ax_log.add_patch(rect)
        
        # Header
        ax_log.text(0.05, 0.92, "AI JURIDICAL AGENT // LIVE LOG", 
                    color='#8b949e', weight='bold', size=10, family='monospace', transform=ax_log.transAxes)
        ax_log.axhline(y=0.88, xmin=0.02, xmax=0.98, color='#30363d', linewidth=1)
        
        # Logs
        logs = get_agent_log(i, len(all_values))
        for idx, line in enumerate(logs):
            msg_color = '#3fb950' # Green
            if "WRN" in line or "RSK" in line: msg_color = '#f85149' # Red
            if "SYS" in line: msg_color = '#58a6ff' # Blue
            if "LEG" in line: msg_color = '#d29922' # Yellow
            if "ACT" in line: msg_color = '#a371f7' # Purple
            
            # Cursor effect on last line
            cursor = " █" if idx == len(logs)-1 and i % 2 == 0 else ""
            
            ax_log.text(0.05, 0.80 - (idx * 0.08), line + cursor, 
                        color=msg_color, fontfamily='monospace', size=9, 
                        transform=ax_log.transAxes)

        filename = f'docs/images/frame_{i}.png'
        plt.savefig(filename, facecolor='#0d1117', edgecolor='none')
        filenames.append(filename)
        plt.close()

    with imageio.get_writer('docs/images/demo.gif', mode='I', duration=0.12, loop=0) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
            
    for filename in filenames:
        os.remove(filename)
        
    print("HUD v2 Animation generated at docs/images/demo.gif")

if __name__ == "__main__":
    generate_animation()
