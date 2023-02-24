import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Set up the figure and axis
fig = plt.figure()
ax = plt.axes(xlim=(-1.5, 1.5), ylim=(-1.5, 1.5))
ax.set_aspect('equal')
circle = plt.Circle((0, 0), 1, fill=False, ls='dashed')
ax.add_artist(circle)

# Initialize the particle
particle, = ax.plot([], [], 'bo', ms=6)

# Add x and y axes
ax.axhline(0, color='gray', lw=1)
ax.axvline(0, color='gray', lw=1)

# Initialize the position vector, unit vectors, and scaling factor
vector, = ax.plot([], [], 'r', lw=1.5, label=r'Position vector $\vec{r}$')
r_unit, = ax.plot([], [], 'g', lw=1.5, label=r'$\hat{r}$ ')
theta_unit, = ax.plot([], [], 'b', lw=1.5, label=r'$\hat{\theta}$')

scale_factor = 0.3

# Add legend to the plot
ax.legend(loc='upper left')

# Initialize the angle text annotation
angle_text = ax.text(1.2, 1.2, '')
# Initialize the position text annotation
position_text = ax.text(1.1, 1.1, '')


# Define the function to update the particle and position vector
def update_particle(frame):
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
    r_unit.set_data([x, x + scale_factor * r_unit_vec[0]], [y, y + scale_factor * r_unit_vec[1]])
    theta_unit.set_data([x, x + scale_factor * theta_unit_vec[0]], [y, y + scale_factor * theta_unit_vec[1]])
    
    # Update the angle text annotation
    angle_degrees = np.degrees(frame)
    angle_text.set_text(r'$\theta$: {:.2f} deg'.format(angle_degrees))
    angle_text.set_position((0.5, 1.3))

    # Update the position text annotation
    position_text.set_text(r'$r$: ({:.2f}, {:.2f})'.format(x, y))
    position_text.set_position((0.5, 1.1))
    
    return particle, vector, r_unit, theta_unit, angle_text, position_text
    

# Set up the animation
ani = animation.FuncAnimation(fig, update_particle, frames=np.linspace(0, 2*np.pi, 100), interval=50, blit=True)

# Show the animation
plt.show()

ani.save('particle_motion.gif', writer='pillow')