import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
from matplotlib.widgets import Button
from PIL import Image

# Set up the figure and axis
fig = plt.figure(figsize=(12, 12))
ax = plt.axes(xlim=(-1.5, 1.5), ylim=(-1.5, 1.5))
ax.set_aspect('equal')
fig.patch.set_facecolor('lightblue')

# Add a title and axis labels
plt.title('Particle Spiral Animation')
plt.xlabel('x')
plt.ylabel('y')

# Load a background image and display it behind the plot
bg_image = Image.open('background.jpg')
ax.imshow(bg_image, extent=(-1.5, 1.5, -1.5, 1.5), aspect='auto')

# Initialize the particle
particle, = ax.plot([], [], 'o', ms=15, mfc='brown', mec='white', mew=2, zorder=10)


# Initialize the spiral curve
curve, = ax.plot([], [], '--', color='magenta', lw=3)

# Add x and y axes
ax.axhline(0, color='gray', lw=1.5, alpha=0.5)
ax.axvline(0, color='gray', lw=1.5, alpha=0.5)

# Initialize the position vector, unit vectors, and scaling factor
vector, = ax.plot([], [], 'r', lw=1.5, label=r'Position vector $\vec{r}$', zorder=5)
r_unit_arrow = None
theta_unit_arrow = None
r_unit_text = None
theta_unit_text = None


scale_factor = 0.3

# Add legend to the plot
ax.legend(loc='upper left', fontsize=12)

# Initialize the angle text annotation
angle_text = ax.text(1.3, 1.3, '', fontsize=16, ha='center', va='center')

# Initialize the position text annotation
position_text = ax.text(1.1, 1.1, '', fontsize=16, ha='center', va='center')

# Initialize the radius text annotation
radius_text = ax.text(-1.8, 1.7, '', fontsize=16, ha='left', va='center')

# Define the function to update the particle and position vector
def update_particle(frame):
    global r_unit_arrow, theta_unit_arrow, r_unit_text, theta_unit_text
    
    # Clear the previous unit vectors and text annotations
    if r_unit_arrow:
        r_unit_arrow.remove()
        r_unit_arrow = None
    if theta_unit_arrow:
        theta_unit_arrow.remove()
        theta_unit_arrow = None
    if r_unit_text:
        r_unit_text.remove()
        r_unit_text = None
    if theta_unit_text:
        theta_unit_text.remove()
        theta_unit_text = None
    
    
    # Compute the new position and radius
    t = 5 * frame  # time-dependent term for radius
    r = 0.05 + 0.05 * t  # radius depends on time
    x = r * np.cos(5*frame)
    y = r * np.sin(5*frame)
    particle.set_data([x], [y])
    
    # Compute the position vector
    vector.set_data([0, x], [0, y])

    # Compute the unit vectors of r and theta
    r = np.array([x, y])
    r_unit_vec = r / np.linalg.norm(r)
    v = np.array([-y, x])
    theta_unit_vec = v / np.linalg.norm(v)

    # Update the unit vectors with scaling
    r_unit_arrow = ax.arrow(x, y, scale_factor * r_unit_vec[0], scale_factor * r_unit_vec[1], head_width=0.05, head_length=0.1, fc='k', ec='k', lw=3)
    theta_unit_arrow = ax.arrow(x, y, scale_factor * theta_unit_vec[0], scale_factor * theta_unit_vec[1], head_width=0.05, head_length=0.1, fc='b', ec='b', lw=3)

    # Add text annotations for the unit vectors
    r_unit_text = ax.text(x + scale_factor * r_unit_vec[0], y + scale_factor * r_unit_vec[1], r"$\hat{r}$", fontsize=16,color='white')
    theta_unit_text = ax.text(x + scale_factor * theta_unit_vec[0], y + scale_factor * theta_unit_vec[1], r"$\hat{\theta}$", fontsize=16, color='white')
    

    # Update the angle text annotation
    angle_degrees = np.degrees(5*frame)
    angle_text.set_text(r'$\theta$: {:.1f}°'.format(angle_degrees % 360))
    angle_text.set_position((0.88, 1.3))
    angle_text.set_fontsize(16)
    angle_text.set_fontfamily('serif')
    angle_text.set_fontweight('bold')
    angle_text.set_color('white')


    # Update the position text annotation
    position_text.set_text(r'$r: $({:.2f}, {:.2f})'.format(x, y))
    position_text.set_position((1.0, 1.05))
    position_text.set_fontsize(16)
    position_text.set_fontfamily('sans-serif')
    position_text.set_fontstyle('normal')
    position_text.set_fontweight('bold')
    position_text.set_color('white')

    # Compute the spiral curve
    t_values = np.linspace(0, 5 * frame, 1000)
    r_values = 0.05 + 0.05 * t_values
    x_values = r_values * np.cos(t_values)
    y_values = r_values * np.sin(t_values)
    curve.set_data(x_values, y_values)

    return particle, vector, r_unit_arrow, theta_unit_arrow, angle_text, position_text, curve

ani = animation.FuncAnimation(fig, update_particle, frames=np.linspace(0, 10*np.pi, 1000), repeat=True)
ani._running = True
# Create the stop/resume button
stop_button_ax = plt.axes([0.14, 0.78, 0.1, 0.05])
stop_button = Button(stop_button_ax, 'Stop', color='red', hovercolor='darkred')

# Define the stop button callback function
def stop(event):
    ani.event_source.stop()
    ani._running = False
    stop_button.label.set_text('Paused')
    stop_button.color = 'gray'
    stop_button.hovercolor = 'gray'

# Create the resume button
resume_button_ax = plt.axes([0.14, 0.72, 0.1, 0.05])
resume_button = Button(resume_button_ax, 'Resume', color='green', hovercolor='darkgreen')


# Define the resume button callback function
def resume(event):
    if not ani._running:
        ani.event_source.start()
        ani._running = True
        stop_button.label.set_text('Stop')
        stop_button.color = 'red'
        stop_button.hovercolor = 'darkred'

# Create the reset button
#reset_button_ax = plt.axes([0.14, 0.66, 0.1, 0.05])
#reset_button = Button(reset_button_ax, 'Reset', color='blue', hovercolor='darkblue')


# Define the reset button callback function

# Define the reset button callback function
def reset(event):
    global r_unit_arrow, theta_unit_arrow
    if r_unit_arrow:
        r_unit_arrow.remove()
        r_unit_arrow = None
    if theta_unit_arrow:
        theta_unit_arrow.remove()
        theta_unit_arrow = None
    particle.set_data([], [])
    vector.set_data([], [])
    curve.set_data([], [])



# Connect the stop and resume buttons to their callback functions
stop_button.on_clicked(stop)
resume_button.on_clicked(resume)
#reset_button.on_clicked(reset)


# Customize the stop and resume button labels
stop_button.label.set_fontsize(14)
stop_button.label.set_fontweight('bold')
resume_button.label.set_fontsize(14)
resume_button.label.set_fontweight('bold')


# Show the animation
plt.show()

# Save the animation as a GIF using Pillow
#writer = animation.PillowWriter(fps=5)
#ani.save("particle_spiral.gif", writer=writer)
