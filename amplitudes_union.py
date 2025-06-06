import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from matplotlib.ticker import AutoMinorLocator
import re

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "font.size": 20,
    "axes.labelsize": 20,
    "axes.titlesize": 24,
    "xtick.labelsize": 20,
    "ytick.labelsize": 20,
})

# Data
data = {
    "1 Node ($\\chi^2 = 53.43$)": [[-0.1, 0.02, 0.1]],
    "2 Nodes ($\\chi^2 = 47.82$)": [[-1.48, 0.4, 0.1], [-1.74, 0.4, 0.1]],
    "3 Nodes ($\\chi^2 = 43.23$)": [[-1.9, 0.5, 0.13], [-2.03, 0.4, 0.1], [-2.8, 0.7, 0.2]],
}

node_names = list(data.keys())
cmap = cm.get_cmap('tab10', len(node_names))
node_colors = {name: cmap(i) for i, name in enumerate(node_names)}	

# Extract chi^2 values	
chi2_values = {}
for name in node_names:
    match = re.search(r'chi\^2\s*=\s*([\d.]+)', name)
    if match:
        chi2_values[name] = float(match.group(1))
    else:
        raise ValueError(f"Could not extract chi^2 from label: {name}")

# Create figure and main axis
fig, ax = plt.subplots(figsize=(6.5, 5), constrained_layout=True)

yticks = []
yticklabels = []
y_index = 0
y_groups = {}

for label in data:
    entries = data[label]
    y_groups[label] = {'min': y_index, 'max': y_index + len(entries) - 1}
    
    for i, (val, err_low, err_up) in enumerate(entries):
        ax.errorbar(
            val, y_index,
            xerr=[[err_low], [err_up]],
            fmt='s',
            markersize=7,
            markeredgecolor='black',
            markerfacecolor=node_colors[label],
            ecolor=node_colors[label],
            elinewidth=1.5,
            capsize=3,
            capthick=1.5,
            label=None
        )
        yticklabels.append(r"$f_{}$".format(i + 1))
        yticks.append(y_index)
        y_index += 1

    y_index += 1

# Add bracket outlines
bracket_width = 0.10
for label in node_names:
    group = y_groups[label]
    y_center = (group['min'] + group['max']) / 2
    ax.plot(
        [-0.2, -0.2],
        [group['min'] - 0.6, group['max'] + 0.6],
        color=node_colors[label],
        linewidth=2.5,
        clip_on=False,
        transform=ax.get_yaxis_transform()
    )
    ax.plot(
        [-0.2, -0.2 + bracket_width],
        [group['min'] - 0.6, group['min'] - 0.6],
        color=node_colors[label],
        linewidth=2.5,
        clip_on=False,
        transform=ax.get_yaxis_transform()
    )
    ax.plot(
        [-0.2, -0.2 + bracket_width],
        [group['max'] + 0.6, group['max'] + 0.6],
        color=node_colors[label],
        linewidth=2.5,
        clip_on=False,
        transform=ax.get_yaxis_transform()
    )
    ax.text(
        -0.3, y_center,
        label.split(' ($')[0],
        ha='right',
        va='center',
        color=node_colors[label],
        fontsize=16,
        fontweight='bold',
        transform=ax.get_yaxis_transform()
    )

# Reference lines
ax.axvline(-2, color='darkgreen', linestyle=':', linewidth=2.0, alpha=0.8, label=r'HDE')
ax.axvline(0, color='violet', linestyle='--', linewidth=2.0, alpha=0.8, label=r'$\Lambda$CDM')

# Axis formatting
ax.set_yticks(yticks)
ax.set_yticklabels(yticklabels)
ax.invert_yaxis()
ax.set_xlabel(r'$f$', labelpad=16)
ax.set_xlim(left=-3.2)

ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())
ax.grid(True, which='major', axis='x', linestyle=':', linewidth=0.5, alpha=0.7)
#ax.set_title('CC+DESI+Union3+SH0ES')

for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)

# Add upper chi^2 axis with tick labels and values
ax_top = ax.twiny()
ax_top.set_xlim(40, 65)
ax_top.set_xlabel(r'$\chi^2$', labelpad=14)
ax_top.set_xticks(np.arange(40, 66, 10))
ax_top.tick_params(axis='x', direction='in', length=5, labelsize=16)

# Plot colored tick markers for chi^2 values on upper axis
chi2_markers = {
    "HDE": (61.25, 'darkgreen'),
    r'$\Lambda$CDM': (53.64, 'violet'),
    "1 Node ($\\chi^2 = 53.43$)": (53.43, node_colors["1 Node ($\\chi^2 = 53.43$)"]),
    "2 Nodes ($\\chi^2 = 47.82$)": (47.82, node_colors["2 Nodes ($\\chi^2 = 47.82$)"]),
    "3 Nodes ($\\chi^2 = 43.23$)": (43.23, node_colors["3 Nodes ($\\chi^2 = 43.23$)"]),
}

for _, (x_val, color) in chi2_markers.items():
    ax_top.plot(x_val, 1.00, marker='d', color=color, markersize=12, transform=ax_top.get_xaxis_transform(), clip_on=False)

# Legend
ax.legend(
    loc='best',
    frameon=True,
    framealpha=0.9,
    edgecolor='none'
)

# Save and show
plt.savefig(
    '/home/alfonsozapata/Documentos/Holographic_final/amplitudes_union.pdf',
    dpi=300,
    bbox_inches='tight',
    pad_inches=0.05,
    transparent=True
)

plt.show()

