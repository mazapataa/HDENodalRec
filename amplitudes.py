import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from matplotlib.ticker import AutoMinorLocator

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "font.size": 16,
    "axes.labelsize": 16,
    "axes.titlesize": 16,
    "xtick.labelsize": 16,
    "ytick.labelsize": 16,
})

data = {
    "1 Node": [[-0.1, 0.02, 0.1]],
    "2 Nodes": [[-1.5, 0.4, 0.2], [-1.74, 0.4, 0.1]],
    "3 Nodes": [[-1.9, 0.13, 0.5], [-2.03,0.4,0.1,], [-2.8, 0.7, 0.2]],
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
            fmt='o', 
            markersize=6,
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

# Add bracket outlines closer to the y-axis
bracket_width = 0.10  # Narrower brackets

for label in node_names:
    group = y_groups[label]
    y_center = (group['min'] + group['max']) / 2
    height = group['max'] - group['min'] + 0.8
    
    # Left vertical line (closer to y-axis)
    ax.plot(
        [-0.15, -0.15],  # Moved closer to y-axis
        [group['min'] - 0.4, group['max'] + 0.4],
        color=node_colors[label],
        linewidth=1.5,
        clip_on=False,
        transform=ax.get_yaxis_transform()
    )
    
    # Top horizontal line
    ax.plot(
        [-0.15, -0.15 + bracket_width],
        [group['min'] - 0.4, group['min'] - 0.4],
        color=node_colors[label],
        linewidth=1.5,
        clip_on=False,
        transform=ax.get_yaxis_transform()
    )
    
    # Bottom horizontal line
    ax.plot(
        [-0.15, -0.15 + bracket_width],
        [group['max'] + 0.4, group['max'] + 0.4],
        color=node_colors[label],
        linewidth=1.5,
        clip_on=False,
        transform=ax.get_yaxis_transform()
    )
    
    # Group label moved closer to brackets
    ax.text(
        -0.3, y_center,  # Moved closer to brackets
        label,
        ha='right',
        va='center',
        color=node_colors[label],
        fontsize=11,
        fontweight='bold',
        transform=ax.get_yaxis_transform()
    )

# Add reference lines (only these will appear in legend)
ax.axvline(-2, color='darkgreen', linestyle=':', linewidth=1.5, alpha=0.8, label=r'HDE')
ax.axvline(0, color='violet', linestyle='--', linewidth=1.5, alpha=0.8, label=r'$\Lambda$CDM')

# Formatting
ax.set_yticks(yticks)
ax.set_yticklabels(yticklabels)
ax.invert_yaxis()

ax.set_xlabel(r'$f$', labelpad=10)
ax.set_xlim(left=-3.2)

# Add minor ticks and grid
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())
ax.grid(True, which='major', axis='x', linestyle=':', linewidth=0.5, alpha=0.5)
ax.set_title('PantheonPlus+DESI+SH0ES')
# Clean up spines
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)

# Legend (now only shows reference lines)
ax.legend(
    loc='best', 
    frameon=True, 
    framealpha=0.9,
    edgecolor='none'
)

plt.savefig(
    '/home/alfonsozapata/Documentos/Holographic_final/amplitudes_PP.pdf',
    dpi=300, 
    bbox_inches='tight', 
    pad_inches=0.05,
    transparent=True
)

plt.show()