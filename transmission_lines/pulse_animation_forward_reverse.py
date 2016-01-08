from bokeh.plotting import figure, curdoc, vplot,  hplot
from bokeh.models.widgets import Button, Toggle, Slider, VBoxForm, HBox, VBox
from bokeh.driving import linear
import numpy as np

# Define a simple arbitrary pulse function. Let's use 1/2 cycle of a cosine centered at 0,
# and zero everywhere else.
def pulse(a):
    if a < np.pi/2.0 and a > -np.pi/2.0:
        return np.cos(a)
    else:
        return 0.0

# Create a vectorized version of the pulse function so we can pass arrays as arguments
# and automatically return an array
vpulse = np.vectorize(pulse)

# Initializations
u = 5.0
current_time = 0.0
zmin = -30
zmax = 30
numpnts = 500
periodic_callback_time_ms = 16
x = np.linspace(zmin,zmax,numpnts)
y1 = vpulse(x - u*current_time)
y2 = vpulse(x + u*current_time)

ii = 0
x_last = 0.0  #sum of u_j*(t_j - t_{j-1}) for changes in velocity
t_last = 0.0  #time at which velocity was last changed by user with slider

# Set up plot
p = figure(plot_width=600, plot_height=400, x_range=(zmin,zmax), y_range=(0,1.1), \
           title="Forward & Reverse Pulses", \
           tools="pan,box_zoom,resize,save,reset")
l_forward = p.line(x, y1, line_width=2, color='blue', line_alpha=0.5)
l_reverse = p.line(x, y2, line_width=2, color='red', line_alpha=0.5)
p.xaxis.axis_label = "Distance (m)"
p.yaxis.axis_label = "Pulse Amplitude"
t1 = p.text(zmin+1.5, 1.0, text=['u = {} m/s'.format(u)], text_align="left", text_font_size="10pt")
t2 = p.text(zmin+1.5, 1.0-0.08, text=['t = {} s'.format(current_time)], text_align="left", text_font_size="10pt")
t3 = p.text(zmin+1.5, 1.0-0.16, text=['Stopped'], text_align="left", text_font_size="10pt")

# Set up toggle button & callback function
def toggle_handler(active):
    #t3.data_source.data["text"] = ['State = {}'.format(toggle.active)]
    if active:
        toggle.label = 'Stop'
        #toggle.type = 'danger'
        t3.data_source.data["text"] = ['Running']
        curdoc().add_periodic_callback(update, periodic_callback_time_ms)
    else:
        toggle.label = 'Start'
        #toggle.type = 'success'
        t3.data_source.data["text"] = ['Stopped']
        curdoc().remove_periodic_callback(update)
toggle = Toggle(label="Start", type="success")
toggle.on_click(toggle_handler)
toggle.active = False

# Set up reset button
def reset_handler():
    global ii, current_time, x_last, t_last
    ii = 0
    current_time = 0
    x_last = 0
    t_last = 0
    l_forward.data_source.data["y"] = vpulse(x - u*current_time)
    l_reverse.data_source.data["y"] = vpulse(x + u*current_time)
    t2.data_source.data["text"] = ['t = {:.3f} s'.format(current_time)]
button_reset = Button(label="Reset", type="success")
button_reset.on_click(reset_handler)

# Set up slider & callback function
def update_velocity(attrname, old, new):
    global u, current_time, x_last, t_last
    x_last += u * (current_time - t_last)
    t_last = current_time
    u = velocity.value
    t1.data_source.data["text"] = ['u = {} m/s'.format(u)]
velocity = Slider(title="Velocity (m/s)", value=5.0, start=0.1, end=10.0, step=0.1)
velocity.on_change('value', update_velocity)

# Set up layout
layout = hplot(p, VBox(toggle, button_reset, velocity, height=400), width=900)

# Create callback function for periodic callback
def update():
    global ii, current_time
    if toggle.active:
        ii += 1
        current_time = ii * 1.e-3 * periodic_callback_time_ms
        l_forward.data_source.data["y"] = vpulse( x - x_last - u*(current_time-t_last) )
        l_reverse.data_source.data["y"] = vpulse( x + x_last + u*(current_time-t_last) )
        t2.data_source.data["text"] = ['t = {:.3f} s'.format(current_time)]
