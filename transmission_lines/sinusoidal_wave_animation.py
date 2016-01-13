from bokeh.plotting import figure, curdoc, vplot,  hplot
from bokeh.models.widgets import Button, Toggle, Slider, VBoxForm, HBox, VBox
from bokeh.driving import linear
import numpy as np


# Forward & reverse propagating waves. Use global variables to pass values into function.
def forward_wave():
    return np.exp(-alpha*(z - zmin)) * np.cos(twopi * (current_time - z_norm))
def reverse_wave():
    return (np.exp(-alpha*(z[-1] - zmin)) * reflection_coef) * \
           np.exp(alpha*z) * np.cos(twopi * (current_time + z_norm))

# Initializations
freq_Hz = 100e6
velocity_mps = 2e8
wavelength_m = velocity_mps / freq_Hz
twopi = 2.0*np.pi
n_samp_one_temporal_cycle = 30
alpha = 0.0
reflection_coef = 1.0
current_time = 0.0
zmin = -20
zmax = 0
numpnts = 500
periodic_callback_time_ms = 16
z = np.linspace(zmin,zmax,numpnts)
z_norm = z/wavelength_m
v1 = forward_wave()
v2 = reverse_wave()

ii = 0

# Set up plot
p = figure(plot_width=600, plot_height=400, x_range=(zmin,zmax), y_range=(-2.1,2.1), \
           title="Forward & Reverse Pulses", \
           tools="pan,box_zoom,resize,save,reset")
l_forward = p.line(z, v1, line_width=2, color='blue', line_alpha=0.5)
l_reverse = p.line(z, v2, line_width=2, color='red', line_alpha=0.5)
p.xaxis.axis_label = "z (m)"
p.yaxis.axis_label = "Voltage (V)"
#t1 = p.text(zmin+1.5, 1.0, text=['u = {} m/s'.format(u)], text_align="left", text_font_size="10pt")
#t2 = p.text(zmin+1.5, 1.0-0.08, text=['t = {} s'.format(current_time)], text_align="left", text_font_size="10pt")
t3 = p.text(zmin+1.5, 1.0-0.16, text=['Stopped'], text_align="left", text_font_size="10pt")

# Set up toggle button & callback function
def toggle_handler(active):
    if active:
        toggle.label = 'Stop'
        t3.data_source.data["text"] = ['Running']
        curdoc().add_periodic_callback(update, periodic_callback_time_ms)
    else:
        toggle.label = 'Start'
        t3.data_source.data["text"] = ['Stopped']
        curdoc().remove_periodic_callback(update)
toggle = Toggle(label="Start", type="success")
toggle.on_click(toggle_handler)
toggle.active = False

# Set up reset button
def reset_handler():
    global ii, current_time
    ii = 0
    current_time = 0
    l_forward.data_source.data["y"] = forward_wave()
    l_reverse.data_source.data["y"] = reverse_wave()
    #t2.data_source.data["text"] = ['t = {:.3f} s'.format(current_time)]
button_reset = Button(label="Reset", type="success")
button_reset.on_click(reset_handler)

# Set up slider & callback function
def update_alpha(attrname, old, new):
    global alpha, current_time
    alpha = alpha_slider.value
    if not toggle.active:
        l_forward.data_source.data["y"] = forward_wave()
        l_reverse.data_source.data["y"] = reverse_wave()
    #t1.data_source.data["text"] = ['u = {} m/s'.format(u)]
alpha_slider = Slider(title="Alpha (1/m)", value=0.0, start=0.0, end=0.25, step=0.005)
alpha_slider.on_change('value', update_alpha)

# Set up layout
layout = hplot(p, VBox(toggle, button_reset, alpha_slider, height=400), width=900)

# Create callback function for periodic callback
def update():
    global ii, current_time
    if toggle.active:
        ii += 1
        current_time = ii / n_samp_one_temporal_cycle
        l_forward.data_source.data["y"] = forward_wave()
        l_reverse.data_source.data["y"] = reverse_wave()
        #t2.data_source.data["text"] = ['t = {:.3f} s'.format(current_time)]
