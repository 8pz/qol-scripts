import time, os
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pynput import mouse, keyboard

actions = {'mouse_clicks': 0, 'keyboard_actions': 0}
actions_total = {'mouse_clicks': 0, 'keyboard_actions': 0}
timestamps = []
timestamps_counter = []
apm = []
apm_counter_values = []
running = False
recorded_actions = []
mouse_listener = None
keyboard_listener = None
pause = False
elapsed_time = 0
graph_values = []
current_directory = os.getcwd()
parent_directory = os.path.join(current_directory, '..')
file_path = os.path.join(parent_directory, 'logs', 'recorded_actions.txt')

def on_click(x, y, button, pressed):
    global pause
    if running and pressed and not pause:
        if button == mouse.Button.left:
            actions['mouse_clicks'] += 1
            actions_total['mouse_clicks'] += 1
            recorded_actions.append('LMB')
        elif button == mouse.Button.right:
            actions['mouse_clicks'] += 1
            actions_total['mouse_clicks'] += 1
            recorded_actions.append('RMB')
        elif button == mouse.Button.middle:
            actions['mouse_clicks'] += 1
            actions_total['mouse_clicks'] += 1
            recorded_actions.append('MMB')

key_states = {}

def on_press(key):
    global pause
    if running and not pause:
        if key not in key_states:
            actions['keyboard_actions'] += 1
            actions_total['keyboard_actions'] += 1
            recorded_actions.append(f'{key}')
        key_states[key] = True

def on_release(key):
    if key in key_states:
        del key_states[key]

def update_counters():
    global timestamps_counter, apm_counter_values, running, elapsed_label, elapsed_time

    if not pause:
        total_actions = sum(actions_total.values())
        current_time = time.time()
        elapsed_minutes = int(elapsed_time // 60)
        elapsed_seconds = int(elapsed_time % 60)

        timestamps_counter.append(current_time)
        apm_counter_values.append(total_actions / ((current_time - timestamps_counter[0]) / 60))

        apm_counter.config(text=f"APM: {apm_counter_values[-1]:.2f}")
        counter_label.config(text=f"Actions: {total_actions}")
        elapsed_label.config(text=f"Elapsed Time: {elapsed_minutes:02d}:{elapsed_seconds:02d}")
        elapsed_time += 1

    if running:
        root.after(1000, update_counters)

def calculate_apm():
    global timestamps, apm, running, graph_values, actions, pause
    total_actions = sum(actions.values())

    if not pause:
        if len(graph_values) != 1:
            apm.append(total_actions)

        if len(apm) >= 1:
            graph.clear()
            graph.plot(graph_values, apm)
            graph.set_xlabel('Time (Minutes)')
            graph.xaxis.label.set_color('white')
            graph.set_ylabel('APM')
            graph.yaxis.label.set_color('white')
            graph.tick_params(colors='white')
            fig.set_facecolor('#303030')
            canvas.draw()

        graph_values.append(len(graph_values) + 1)

        actions = {'mouse_clicks': 0, 'keyboard_actions': 0}

    if running:
        root.after(60000, calculate_apm)

def start_recording():
    global running, timestamps, apm, actions, recorded_actions, mouse_listener, keyboard_listener, elapsed_time, graph_values, timestamps_counter, apm_counter_values, actions_total, pause, key_states

    running = True
    pause = False
    timestamps = [time.time()]
    timestamps_counter = [time.time()]
    elapsed_time = 0
    apm = [0]
    apm_counter_values = []
    graph_values = [0]
    key_states = {}
    actions = {'mouse_clicks': 0, 'keyboard_actions': 0}
    actions_total = {'mouse_clicks': 0, 'keyboard_actions': 0}
    recorded_actions.clear()

    pause_button.config(text="Pause", bg='#303030', fg='white')

    mouse_listener = mouse.Listener(on_click=on_click)
    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

    mouse_listener.start()
    keyboard_listener.start()

    graph.clear()

    calculate_apm()
    update_counters()

def stop_recording():
    global running, mouse_listener, keyboard_listener, graph_values

    running = False

    if mouse_listener is not None:
        mouse_listener.stop()
    if keyboard_listener is not None:
        keyboard_listener.stop()

    with open(file_path, 'w') as file:
        file.write('\n'.join(recorded_actions))

def pause_recording():
    global running, elapsed_time, pause

    if not pause:
        pause = True
        pause_button.config(text="Resume", bg='white', fg='#303030')
    elif pause:
        pause = False
        pause_button.config(text="Pause", bg='#303030', fg='white')
    else:
        print(pause)
        pass

root = tk.Tk()
root.title("APM Tracker")
root.configure(bg='#303030')

fig = Figure(figsize=(6, 4), dpi=100)
graph = fig.add_subplot(111)
graph.set_xlabel('Time (Minutes)')
graph.xaxis.label.set_color('white')
graph.set_ylabel('APM')
graph.yaxis.label.set_color('white')
graph.tick_params(colors='white')
graph.set_facecolor('#303030')
fig.set_facecolor('#303030')
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

frame = tk.Frame(root, bg='#303030')
frame.pack(pady=10)

start_button = tk.Button(frame, text="Start", command=start_recording, bg='#303030', fg='white')
start_button.pack(side='left', padx=5)

stop_button = tk.Button(frame, text="Stop", command=stop_recording, bg='#303030', fg='white')
stop_button.pack(side='left', padx=5)

pause_button = tk.Button(frame, text="Pause", command=pause_recording, bg='#303030', fg='white')
pause_button.pack(side='left', padx=5)

counter_label = tk.Label(frame, text="Actions: 0", bg='#303030', fg='white')
counter_label.pack(side='left', padx=5)

apm_counter = tk.Label(frame, text="APM: 0.00", bg='#303030', fg='white')
apm_counter.pack(side='left', padx=5)

elapsed_label = tk.Label(frame, text="Elapsed Time: 00:00", bg='#303030', fg='white')
elapsed_label.pack(side='left', padx=5)

root.resizable(False, False)
root.mainloop()
