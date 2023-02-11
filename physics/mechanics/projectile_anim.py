import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
from matplotlib.widgets import Button
import tkinter as tk
from tkinter import simpledialog


class InputDialog(simpledialog.Dialog):
    def __init__(self, parent, title, prompt, init_value):
        self.prompt = prompt
        self.init_value = init_value
        simpledialog.Dialog.__init__(self, parent, title)

    def body(self, master):
        tk.Label(master, text=self.prompt).grid(row=0)
        self.e1 = tk.Entry(master)
        self.e1.insert(0, str(self.init_value))
        self.e1.grid(row=0, column=1)
        return self.e1

    def apply(self):
        try:
            self.result = float(self.e1.get())
        except ValueError:
            self.result = None

# Define a function to ask for the initial conditions
def ask_for_initial_conditions():
    root = tk.Tk()
    root.withdraw()
    prompt = 'Enter the initial velocity (m/s): '
    init_value = 1
    dlg = InputDialog(root, "Initial Velocity", prompt, init_value)
    if dlg.result is None:
        return None
    else:
        v0 = dlg.result

    prompt = 'Enter the launch angle (degrees): '
    init_value = 0
    dlg = InputDialog(root, "Launch Angle", prompt, init_value)
    if dlg.result is None:
        return None
    else:
        theta0 = dlg.result

    root.destroy()
    return v0, theta0


# Ask for the initial conditions
result = ask_for_initial_conditions()
if result is None:
    print("Input error. Exiting program.")
    exit()
else:
    v0, theta0 = result

g = 9.8 # Acceleration due to gravity (m/s^2)
x0=0
y0=0

# Convert the launch angle to radians
theta = np.deg2rad(theta0)

# Calculate the x and y components of velocity
v0x = v0 * np.cos(theta)
v0y = v0 * np.sin(theta)

# Maximum time to display animation
t_max = 2 * v0y / g

# Number of time steps to display
N = 100

# Time step size
dt = t_max / N

# Time array
t = np.linspace(0, t_max, N)

# X and Y position arrays
x = x0 + v0x * t
y = y0 + v0y * t - 0.5 * g * t**2

# Create the figure and axis objects
fig, ax = plt.subplots()

# Set the axis limits
ax.set_xlim(0, np.max(x))
ax.set_ylim(0, 2*np.max(y))



# Update function for the animation
def update(frame):
    ax.clear()
    ax.set_xlim(0, np.max(x))
    ax.set_ylim(0, 2*np.max(y))

    # Add the text labels
    x_pos_text = ax.text(0.02, 0.9, '', transform=ax.transAxes)
    y_pos_text = ax.text(0.02, 0.8, '', transform=ax.transAxes)
    x_vel_text = ax.text(0.02, 0.7, '', transform=ax.transAxes)
    y_vel_text = ax.text(0.02, 0.6, '', transform=ax.transAxes)

    theta_text = ax.text(0.78, 0.9, '', transform=ax.transAxes)
    x0_text = ax.text(0.78, 0.8, '', transform=ax.transAxes)
    y0_text = ax.text(0.78, 0.7, '', transform=ax.transAxes)
    v0_text = ax.text(0.78, 0.6, '', transform=ax.transAxes)


    # Label for the x-axis
    ax.set_xlabel('X(t) [m]', fontsize=12)

    # Label for the y-axis
    ax.set_ylabel('Y(t) [m]', fontsize=12)

    # Title for the plot
    ax.set_title('Projectile Motion', fontsize=14, fontweight='bold')

    # Add a background grid
    ax.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)

        
    
    # Plot the X and Y velocity components
    vx = v0x
    vy = v0y - g * t[frame]

    # Plot the X component of the projectile motion along the x-axis
    ax.plot([x0, x[frame]], [0.05, 0.05], 'o', linewidth=0.5, color='g')
    
    # Plot the Y component of the projectile motion along the y-axis
    ax.plot([0.05, 0.05], [y0, y[frame]], 'o', linewidth=0.5, color='b')

    ax.quiver(x[frame], y[frame], vx, 0, color='g', width=0.0018, headwidth=3., headlength=4.)
    ax.quiver(x[frame], y[frame], 0, vy, color='b', width=0.0018,headwidth=3., headlength=4.)
    
    # Plot the velocity vector
    ax.quiver(x[frame], y[frame], vx, vy, color='r', width=0.002,headwidth=3., headlength=4.)
    
    # Plot the curve of motion
    #ax.plot(x[:frame], y[:frame], '-k')
    # Plot the trajectory
    ax.plot(x[:frame], y[:frame], '-k', linewidth=1.5, label='Projectile')
    
    # Add a legend
    #ax.legend(loc='best')

    # Plot the X and Y positions as dots
    ax.plot(x[frame], y[frame], 'o', color='r')

    x_pos_text.set_text('$x=$ {:.2f} m'.format(x[frame]))
    y_pos_text.set_text('$y=$ {:.2f} m'.format(y[frame]))
    x_vel_text.set_text('$v_x=$ {:.2f} m/s'.format(vx))
    y_vel_text.set_text('$v_y = $ {:.2f} m/s'.format(vy))
    theta_text.set_text(r'$\theta_0 = $'+str(theta0)+'$^{o}$')
    x0_text.set_text(r'$x_0 = $'+str(x0))
    y0_text.set_text(r'$y_0 = $'+str(y0))
    v0_text.set_text('$v_0 = $ {:.0f} m/s'.format(v0))


# Animate the motion

ani = FuncAnimation(fig, update, frames=range(N), repeat=True)
ani._running = True

# Create the stop/resume button
stop_button_ax = plt.axes([0.5, 0.8, 0.1, 0.075])
stop_button = Button(stop_button_ax, 'Stop',color='green', hovercolor='red')

# Define the stop button callback function
def stop(event):
    ani.event_source.stop()
    ani._running = False

# Define the resume button callback function
def resume(event):
    if not ani._running:
        ani.event_source.start()
        ani._running = True


# Connect the stop button to the callback function
stop_button.on_clicked(stop)

# Create the resume button
resume_button_ax = plt.axes([0.5, 0.7, 0.1, 0.075])
resume_button = Button(resume_button_ax, 'Resume',color='red', hovercolor='green')

# Connect the resume button to the callback function
resume_button.on_clicked(resume)

# Show the animation
plt.show()

