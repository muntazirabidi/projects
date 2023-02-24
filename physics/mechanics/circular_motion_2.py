import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Set up the figure and axis
fig = plt.figure(figsize=(8, 8))
ax = plt.axes(xlim=(-1.5, 1.5), ylim=(-1.5, 1.5))
ax.set_aspect('equal')
circle = plt.Circle((0, 0), 1, fill=False, ls='dashed', color='gray', alpha=0.5, lw=2)
ax.add_artist(circle)

# Initialize the particle
particle, = ax.plot([], [], 'o', ms=15, mfc='brown', mec='white', mew=2, zorder=10)

# Add x and y axes
ax.axhline(0, color='gray', lw=1.5, alpha=0.5)
ax.axvline(0, color='gray', lw=1.5, alpha=0.5)

# Initialize the position vector, unit vectors, and scaling factor
vector, = ax.plot([], [], 'r', lw=1.5, label=r'Position vector $\vec{r}$', zorder=5)
r_unit_arrow = None
theta_unit_arrow = None
scale_factor = 0.3

# Add legend to the plot
ax.legend(loc='upper left', fontsize=12)

# Initialize the angle text annotation
angle_text = ax.text(1.3, 1.3, '', fontsize=16, ha='center', va='center')
# Initialize the position text annotation
position_text = ax.text(1.1, 1.1, '', fontsize=16, ha='center', va='center')


# Define the function to update the particle and position vector
def update_particle(frame):
    global r_unit_arrow, theta_unit_arrow
    
    # Clear the previous unit vectors
    if r_unit_arrow:
        r_unit_arrow.remove()
        r_unit_arrow = None
    if theta_unit_arrow:
        theta_unit_arrow.remove()
        theta_unit_arrow = None
    # Compute the new position
    x = np.cos(frame)
    y = np.sin(frame)
    particle.set_data([x], [y])
    
    # Compute the position vector
    vector.set_data([0, x], [0, y])
    
    # Compute the unit vectors of r and theta
    r = np.array([x, y])
    r_unit_vec = r / np.linalg.norm(r)
    v = np.array([-y, x])
    theta_unit_vec = v / np.linalg.norm(v)
    
    # Update the unit vectors with scaling
    #r_unit.set_data([x, x + scale_factor * r_unit_vec[0]], [y, y + scale_factor * r_unit_vec[1]])
    #theta_unit.set_data([x, x + scale_factor * theta_unit_vec[0]], [y, y + scale_factor * theta_unit_vec[1]])
    
    # Update the unit vectors with scaling
    r_unit_arrow = ax.arrow(x, y, scale_factor * r_unit_vec[0], scale_factor * r_unit_vec[1], head_width=0.05, head_length=0.1, fc='g', ec='g', lw=3)
    theta_unit_arrow = ax.arrow(x, y, scale_factor * theta_unit_vec[0], scale_factor * theta_unit_vec[1], head_width=0.05, head_length=0.1, fc='b', ec='b', lw=3)
    

    # Update the angle text annotation
    angle_degrees = np.degrees(frame)
    angle_text.set_text(r'$\theta$: {:.1f}°'.format(angle_degrees))
    angle_text.set_position((0.8, 1.3))

    # Update the position text annotation
    position_text.set_text(r'$r: $({:.2f}, {:.2f})'.format(x, y))
    position_text.set_position((1.0, 1.05))
    
    return particle, vector, r_unit_arrow, theta_unit_arrow, angle_text, position_text
    

# Set up the animation
ani = animation.FuncAnimation(fig, update_particle, frames=np.linspace(0, 2*np.pi, 100))


# Show the animation
plt.show()

#ani.save('particle_motion.gif', writer='pillow')

# Save the animation as a GIF using Pillow
writer = animation.PillowWriter(fps=5)
ani.save("particle_motion.gif", writer=writer)
