import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from matplotlib.ticker import AutoMinorLocator

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "font.size": 20,  # Increased from 16
    "axes.labelsize": 20,  # Increased from 16
    "axes.titlesize": 24,  # Increased from 16
    "xtick.labelsize": 20,  # Increased from 16
    "ytick.labelsize": 20,  # Increased from 16
})

# Data with original values
data = {
    "1 Node": [[-0.1, 0.02, 0.1]],
    "2 Nodes": [[-1.48, 0.35, 0.15], [-1.74, 0.4, 0.1]],
    "3 Nodes": [[-1.9, 0.47, 0.13], [-2.03, 0.4, 0.1], [-2.8, 0.7, 0.2]],
}

# Chi2 values for each model
chi2_values = {
    "1 Node": 53.43,
    "2 Nodes": 47.82,
    "3 Nodes": 43.23,
    "HDE": 61.25,
    r'$\Lambda$CDM': 53.64
}

node_names = list(data.keys())
cmap = cm.get_cmap('Set1', len(node_names))
node_colors = {name: cmap(i) for i, name in enumerate(node_names)}

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
            fmt='s',  # Changed from 'o' to 's' for square markers
            markersize=7,  # Increased from 6
            markeredgecolor='black',
            markerfacecolor=node_colors[label],
            ecolor=node_colors[label], 
            elinewidth=1.5,
            capsize=3,
            capthick=1.5,
            label=None
        )
        
        if label == "1 Node":
            yticklabels.append(r"$f_1$")
        elif label == "2 Nodes":
            yticklabels.append(r"$f_{}$".format(i+1))
        elif label == "3 Nodes":
            yticklabels.append(r"$f_{}$".format(i+1))
            
        yticks.append(y_index)
        y_index += 1
    
    y_index += 1

# Add bracket outlines with thicker lines
bracket_width = 0.10
for label in node_names:
    group = y_groups[label]
    y_center = (group['min'] + group['max']) / 2
    
    ax.plot(
        [-0.2, -0.2],  # Changed from -0.15
        [group['min'] - 0.6, group['max'] + 0.6],  # Increased from 0.4
        color=node_colors[label],
        linewidth=2.5,  # Increased from 1.5
        clip_on=False,
        transform=ax.get_yaxis_transform()
    )
    
    ax.plot(
        [-0.2, -0.2 + bracket_width],
        [group['min'] - 0.6, group['min'] - 0.6],
        color=node_colors[label],
        linewidth=2.5,  # Increased from 1.5
        clip_on=False,
        transform=ax.get_yaxis_transform()
    )
    
    ax.plot(
        [-0.2, -0.2 + bracket_width],
        [group['max'] + 0.6, group['max'] + 0.6],
        color=node_colors[label],
        linewidth=2.5,  # Increased from 1.5
        clip_on=False,
        transform=ax.get_yaxis_transform()
    )
    
    ax.text(
        -0.3, y_center,
        label,
        ha='right',
        va='center',
        color=node_colors[label],
        fontsize=16,  # Increased from 11
        fontweight='bold',
        transform=ax.get_yaxis_transform()
    )

# Add reference lines with thicker lines
ax.axvline(-2, color='darkgreen', linestyle=':', linewidth=2.0, alpha=0.8, label=r'HDE')  # Increased from 1.5
ax.axvline(0, color='violet', linestyle='--', linewidth=2.0, alpha=0.8, label=r'$\Lambda$CDM')  # Increased from 1.5

# Formatting
ax.set_yticks(yticks)
ax.set_yticklabels(yticklabels)
ax.invert_yaxis()
ax.set_xlabel(r'$f$', labelpad=16)  # Increased from 10
ax.set_xlim(left=-3.2)

ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())
ax.grid(True, which='major', axis='x', linestyle=':', linewidth=0.5, alpha=0.7)  # Increased alpha from 0.5
#ax.set_title('PantheonPlus+DESI+SH0ES')

for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)

# Create upper axis for chi2 values
ax_top = ax.twiny()
ax_top.set_xlim(40, 65)
ax_top.set_xlabel(r'$\chi^2$', labelpad=14)  # Increased from 10
ax_top.set_xticks(np.arange(40, 66, 10))
ax_top.tick_params(axis='x', direction='in', length=5, labelsize=16)  # Added labelsize

# Add chi2 markers with diamond shape and larger size
for label in node_names + ['HDE', r'$\Lambda$CDM']:
    if label in chi2_values:
        color = node_colors.get(label, 'darkgreen' if label == 'HDE' else 'violet')
        ax_top.plot(chi2_values[label], 1.0, marker='d', color=color, 
                   markersize=12,  # Increased from 8
                   transform=ax_top.get_xaxis_transform(), 
                   clip_on=False)

# Legend with adjusted parameters
ax.legend(
    loc='best', 
    frameon=True, 
    framealpha=0.9,
    edgecolor='none',
    fontsize=16  # Added fontsize
)

plt.savefig(
    '/home/alfonsozapata/Documentos/Holographic_final/amplitudes_PP.pdf',
    dpi=300, 
    bbox_inches='tight', 
    pad_inches=0.05,
    transparent=True
)

plt.show()
