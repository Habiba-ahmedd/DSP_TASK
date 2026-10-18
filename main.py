import customtkinter as ctk
from tkinter import filedialog, messagebox, simpledialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


# =========================================================
# SIGNAL FUNCTIONS (Requested Implementation)
# =========================================================

# READ SIGNAL
def read_signal(filename):
    indices = []
    samples = []

    with open(filename, "r") as file:
        # Skip the first 3 lines
        file.readline()
        file.readline()
        file.readline()

        for line in file:
            line = line.strip()
            if not line:
                continue
            index, value = line.split()
            indices.append(int(index))
            samples.append(float(value))

    return indices, samples


# ADD SIGNALS
def add_signals(*signals):
    result_indices = []
    result_samples = []

    # Get all indices from all signals
    all_indices = set()

    for indices, samples in signals:
        all_indices.update(indices)

    all_indices = sorted(all_indices)

    # Add the values at each index
    for index in all_indices:
        total = 0

        for indices, samples in signals:
            if index in indices:
                position = indices.index(index)
                total += samples[position]

        result_indices.append(index)
        result_samples.append(total)

    return result_indices, result_samples


# MULTIPLY SIGNAL
def multiply_signal(indices, samples, constant):
    result_indices = indices.copy()
    result_samples = []

    for sample in samples:
        result_samples.append(sample * constant)

    return result_indices, result_samples


# SUBTRACT SIGNALS
def subtract_signals(*signals):
    # Start with the first signal
    result_indices, result_samples = signals[0]

    # Subtract every signal after the first one
    for signal in signals[1:]:
        indices, samples = signal

        # Multiply the current signal by -1
        negative_indices, negative_samples = multiply_signal(
            indices,
            samples,
            -1
        )

        # Add the negative signal to the current result
        result_indices, result_samples = add_signals(
            (result_indices, result_samples),
            (negative_indices, negative_samples)
        )

    return result_indices, result_samples


# SHIFT SIGNAL
def shift_signal(indices, samples, k):
    result_indices = []

    for index in indices:
        result_indices.append(index - k)

    result_samples = samples.copy()

    return result_indices, result_samples


# FOLD SIGNAL
def fold_signal(indices, samples):
    result_indices = []

    for index in indices:
        result_indices.append(-index)

    result_indices.sort()

    result_samples = []

    for index in result_indices:
        original_index = -index
        position = indices.index(original_index)
        result_samples.append(samples[position])

    return result_indices, result_samples


# =========================================================
# APPLICATION SETUP
# =========================================================

root = ctk.CTk()
root.title("Signal Processing Framework")
root.geometry("1250x750")
root.minsize(1000, 650)

signals = []
# Generated signals are stored separately from signals loaded from files.
generated_signals = []

container = ctk.CTkFrame(root, fg_color="transparent")
container.pack(fill="both", expand=True)


def clear_page():
    for widget in container.winfo_children():
        widget.destroy()


def make_header(page_title, subtitle="Signal Processing Framework"):
    header = ctk.CTkFrame(container, height=90, corner_radius=0)
    header.pack(fill="x")
    header.pack_propagate(False)

    ctk.CTkLabel(
        header, text="∿", font=("Arial", 28, "bold"),
        text_color="#1f6aa5"
    ).pack(side="left", padx=(20, 10), pady=14)

    text_frame = ctk.CTkFrame(header, fg_color="transparent")
    text_frame.pack(side="left", pady=14)

    ctk.CTkLabel(
        text_frame, text=page_title, font=("Arial", 18, "bold")
    ).pack(anchor="w")

    ctk.CTkLabel(
        text_frame, text=subtitle, font=("Arial", 11),
        text_color="gray"
    ).pack(anchor="w", pady=(2, 0))


def make_button(parent, text, command, primary=True, width=None):
    kwargs = {"font": ("Arial", 11, "bold"), "height": 35}
    if width is not None:
        kwargs["width"] = width

    if primary:
        button = ctk.CTkButton(parent, text=text, command=command, **kwargs)
    else:
        button = ctk.CTkButton(parent, text=text, command=command, fg_color="transparent", border_width=1, **kwargs)
    return button


def make_card(parent, title, description):
    card = ctk.CTkFrame(parent, corner_radius=10)

    ctk.CTkLabel(card, text=title, font=("Arial", 14, "bold")).pack(anchor="w", padx=15, pady=(15, 5))
    ctk.CTkLabel(card, text=description, font=("Arial", 11), text_color="gray", justify="left", wraplength=260).pack(
        anchor="w", padx=15, pady=(0, 15)
    )
    return card


def show_home():
    clear_page()
    make_header("Signal Processing Framework", "Analyze, generate and visualize signals")

    content = ctk.CTkFrame(container, fg_color="transparent")
    content.pack(fill="both", expand=True, padx=35, pady=30)

    ctk.CTkLabel(content, text="Welcome", font=("Arial", 22, "bold")).pack(anchor="w")
    ctk.CTkLabel(
        content, text="Choose a workspace to get started.",
        font=("Arial", 11), text_color="gray"
    ).pack(anchor="w", pady=(5, 20))

    cards = ctk.CTkFrame(content, fg_color="transparent")
    cards.pack(fill="x")

    operations_card = make_card(
        cards, "Signal Operations",
        "Load signals and perform addition, subtraction, multiplication, shifting and folding."
    )
    operations_card.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
    make_button(operations_card, "Open Operations →", show_operations).pack(
        anchor="w", padx=15, pady=(0, 15), fill="x"
    )

    generation_card = make_card(
        cards, "Signal Generation",
        "Create sinusoidal signals by choosing sine or cosine, amplitude, phase and frequencies."
    )
    generation_card.grid(row=0, column=1, padx=5, sticky="nsew")
    make_button(generation_card, "Open Generation →", show_generation).pack(
        anchor="w", padx=15, pady=(0, 15), fill="x"
    )

    display_card = make_card(
        cards, "Signal Display",
        "Display loaded or generated signals as continuous curves, discrete samples, or both."
    )
    display_card.grid(row=0, column=2, padx=(10, 0), sticky="nsew")
    make_button(display_card, "Open Display →", show_display).pack(
        anchor="w", padx=15, pady=(0, 15), fill="x"
    )

    quantization_card = make_card(
        cards, "Quantization (Task 3)",
        "Quantize a loaded signal using a chosen number of bits or levels, and view encoded values, quantized samples and quantization error."
    )
    quantization_card.grid(row=1, column=0, padx=(0, 10), pady=12, sticky="nsew")
    make_button(quantization_card, "Open Quantization →", show_quantization).pack(
        anchor="w", padx=15, pady=(0, 15), fill="x"
    )

    for column in range(3):
        cards.grid_columnconfigure(column, weight=1, uniform="cards")


# =========================================================
# PROFESSIONAL EMBEDDED PLOTTING HELPER
# =========================================================

def apply_modern_plot_style(fig, ax):
    is_dark = ctk.get_appearance_mode() == "Dark"

    bg_color = "#2b2b2b" if is_dark else "#ffffff"
    text_color = "#dce4ee" if is_dark else "#222222"
    grid_color = "#404040" if is_dark else "#e0e0e0"

    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    ax.tick_params(colors=text_color, labelsize=9)
    ax.xaxis.label.set_color(text_color)
    ax.yaxis.label.set_color(text_color)
    ax.title.set_color(text_color)

    for spine in ax.spines.values():
        spine.set_color(grid_color)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, linestyle="--", alpha=0.4, color=grid_color)


def embed_figure_in_frame(fig, parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    plt.close(fig)



def plot_file_signal(
    indices,
    samples,
    title,
    parent_frame,
    representation="discrete"
):
    fig, ax = plt.subplots(figsize=(5, 4))

    if representation == "continuous":
        ax.plot(
            indices,
            samples,
            color="#1f6aa5",
            linewidth=2
        )
    else:
        markerline, stemlines, baseline = ax.stem(
            indices,
            samples
        )
        plt.setp(markerline, markersize=4, color="#1f6aa5")
        plt.setp(stemlines, linewidth=1.5, color="#1f6aa5")
        plt.setp(baseline, linewidth=1, color="gray")

    ax.set_title(title, fontsize=11, fontweight="bold", pad=10)
    ax.set_xlabel("Index / Time", fontsize=9)
    ax.set_ylabel("Amplitude", fontsize=9)

    apply_modern_plot_style(fig, ax)
    fig.tight_layout()
    embed_figure_in_frame(fig, parent_frame)



# =========================================================
# OPERATIONS PAGE
# =========================================================

loaded_plot_frame = None
result_plot_frame = None
selected_loaded_signal_var = None
loaded_menu = None


def load_signals():
    global signals
    files = filedialog.askopenfilenames(
        title="Select Signal Text Files",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if not files:
        return

    loaded = []
    try:
        for filename in files:
            loaded.append(read_signal(filename))
    except Exception as error:
        messagebox.showerror("File Error", f"Could not load signals:\n{error}")
        return

    signals = loaded
    messagebox.showinfo("Success", f"{len(signals)} signal(s) loaded.")
    update_loaded_count()
    update_loaded_menu()


def update_loaded_count():
    if "loaded_count_label" in globals() and loaded_count_label.winfo_exists():
        loaded_count_label.configure(
            text=f"Loaded signals: {len(signals)}"
        )


def update_loaded_menu():
    global loaded_menu, selected_loaded_signal_var
    if signals:
        choices = [f"Signal {i + 1}" for i in range(len(signals))]
        selected_loaded_signal_var.set(choices[0])
        loaded_menu.configure(values=choices)
    else:
        selected_loaded_signal_var.set("No signals loaded")
        loaded_menu.configure(values=["No signals loaded"])


def display_selected_loaded_signal():
    if not signals:
        messagebox.showwarning("No signals", "Please load signals first.")
        return

    choice = selected_loaded_signal_var.get()
    if "Signal" not in choice:
        return

    idx = int(choice.split(" ")[1]) - 1
    indices, samples = signals[idx]
    plot_file_signal(indices, samples, f"Loaded: Signal {idx + 1}", loaded_plot_frame)


def choose_loaded_signal_for_op():
    if not signals:
        messagebox.showwarning("No signals", "Please load signals first.")
        return None

    choice = selected_loaded_signal_var.get()
    if "Signal" in choice:
        idx = int(choice.split(" ")[1]) - 1
        return signals[idx]
    return signals[0]


def add_button():
    if len(signals) < 2:
        messagebox.showwarning("Not enough signals", "Load at least two signals.")
        return
    indices, samples = add_signals(*signals)
    plot_file_signal(indices, samples, "Addition Result", result_plot_frame)


def subtract_button():
    if len(signals) < 2:
        messagebox.showwarning("Not enough signals", "Load at least two signals.")
        return
    indices, samples = subtract_signals(*signals)
    plot_file_signal(indices, samples, "Subtraction Result", result_plot_frame)


def multiply_button():
    signal = choose_loaded_signal_for_op()
    if signal is None:
        return
    constant = simpledialog.askfloat("Multiply Signal", "Enter the constant:")
    if constant is None:
        return
    indices, samples = multiply_signal(signal[0], signal[1], constant)
    plot_file_signal(indices, samples, f"Multiplication Result × {constant:g}", result_plot_frame)


def shift_button():
    signal = choose_loaded_signal_for_op()
    if signal is None:
        return
    k = simpledialog.askinteger("Shift Signal", "Enter k (positive or negative):")
    if k is None:
        return
    indices, samples = shift_signal(signal[0], signal[1], k)
    plot_file_signal(indices, samples, f"Shift Result (k = {k})", result_plot_frame)


def fold_button():
    signal = choose_loaded_signal_for_op()
    if signal is None:
        return
    indices, samples = fold_signal(signal[0], signal[1])
    plot_file_signal(indices, samples, "Folding Result", result_plot_frame)


def show_operations():
    global loaded_plot_frame, result_plot_frame, loaded_count_label, selected_loaded_signal_var, loaded_menu
    clear_page()
    make_header("Signal Operations", "Load signals, select one to preview, and view results")

    content = ctk.CTkFrame(container, fg_color="transparent")
    content.pack(fill="both", expand=True, padx=15, pady=10)

    top = ctk.CTkFrame(content, fg_color="transparent")
    top.pack(fill="x", pady=(0, 5))
    make_button(top, "← Back to Home", show_home, primary=False, width=130).pack(side="left")
    loaded_count_label = ctk.CTkLabel(
        top, text=f"Loaded signals: {len(signals)}",
        font=("Arial", 11, "bold")
    )
    loaded_count_label.pack(side="right")

    main_split = ctk.CTkFrame(content, fg_color="transparent")
    main_split.pack(fill="both", expand=True)

    left_panel = ctk.CTkFrame(main_split, fg_color="transparent", width=280)
    left_panel.pack(side="left", fill="y", padx=(0, 8))

    preview_card = ctk.CTkFrame(left_panel, corner_radius=8)
    preview_card.pack(fill="x", pady=(0, 8))
    ctk.CTkLabel(preview_card, text="Loaded Signals Viewer", font=("Arial", 11, "bold")).pack(anchor="w", padx=10,
                                                                                              pady=(8, 4))

    selected_loaded_signal_var = ctk.StringVar(value="No signals loaded" if not signals else f"Signal 1")
    choices = [f"Signal {i + 1}" for i in range(len(signals))] if signals else ["No signals loaded"]
    loaded_menu = ctk.CTkOptionMenu(preview_card, variable=selected_loaded_signal_var, values=choices)
    loaded_menu.pack(fill="x", padx=10, pady=4)
    make_button(preview_card, "Show Selected Signal", display_selected_loaded_signal, width=220).pack(padx=10,
                                                                                                      pady=(4, 10))

    ops_card = ctk.CTkFrame(left_panel, corner_radius=8)
    ops_card.pack(fill="x")
    ctk.CTkLabel(ops_card, text="Operations", font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(8, 4))

    grid = ctk.CTkFrame(ops_card, fg_color="transparent")
    grid.pack(fill="x", padx=6, pady=(0, 8))

    actions = [
        ("Load Files", load_signals),
        ("Add Signals", add_button),
        ("Subtract", subtract_button),
        ("Multiply", multiply_button),
        ("Shift", shift_button),
        ("Fold", fold_button),
    ]

    for i, (label, command) in enumerate(actions):
        row, column = divmod(i, 2)
        btn = make_button(grid, label, command, width=115)
        btn.grid(row=row, column=column, padx=3, pady=3, sticky="nsew")
    for column in range(2):
        grid.grid_columnconfigure(column, weight=1)

    loaded_plot_frame = ctk.CTkFrame(main_split, corner_radius=10)
    loaded_plot_frame.pack(side="left", fill="both", expand=True, padx=(0, 8))

    result_plot_frame = ctk.CTkFrame(main_split, corner_radius=10)
    result_plot_frame.pack(side="right", fill="both", expand=True)



# =========================================================
# SIGNAL GENERATION PAGE
# =========================================================

def generate_sinusoidal_signal(duration, A, theta, F, Fs, wave_type):
    """
    Generate a sine or cosine signal for the requested duration.
    theta is entered in radians. Fs determines samples per second.
    """
    if duration <= 0:
        raise ValueError("Duration must be greater than 0 seconds.")
    if F <= 0 or Fs <= 0:
        raise ValueError("Analog frequency F and sampling frequency Fs must be positive.")
    if Fs < 2 * F:
        raise ValueError(
            f"Sampling theorem not satisfied: Fs must be at least 2F. "
            f"For F={F:g} Hz, choose Fs >= {2 * F:g} Hz."
        )

    sample_count = int(Fs * duration)
    if sample_count < 2:
        raise ValueError("Duration and Fs must produce at least 2 samples.")

    indices = np.arange(sample_count)
    t = indices / Fs

    if wave_type.lower() == "sine wave":
        samples = A * np.sin(2 * np.pi * F * t + theta)
    elif wave_type.lower() == "cosine wave":
        samples = A * np.cos(2 * np.pi * F * t + theta)
    else:
        raise ValueError("Choose sine wave or cosine wave.")

    return indices, samples


def plot_generated_signal(indices, samples, title, parent_frame, representation="discrete"):
    fig, ax = plt.subplots(figsize=(7, 4))

    if representation.lower() == "continuous":
        # The generated values are samples; draw them connected for visual display.
        ax.plot(indices, samples, color="#1f6aa5", linewidth=2, marker="o", markersize=3)
    else:
        markerline, stemlines, baseline = ax.stem(indices, samples)
        plt.setp(markerline, markersize=4, color="#1f6aa5")
        plt.setp(stemlines, linewidth=1.5, color="#1f6aa5")
        plt.setp(baseline, linewidth=1, color="gray")

    ax.set_title(title, fontsize=11, fontweight="bold", pad=10)
    ax.set_xlabel("Sample Index (n)", fontsize=9)
    ax.set_ylabel("Amplitude", fontsize=9)
    apply_modern_plot_style(fig, ax)
    fig.tight_layout()
    embed_figure_in_frame(fig, parent_frame)


def show_generation():
    clear_page()
    make_header(
        "Signal Generation",
        "Generate sine or cosine signals with the required parameters"
    )

    content = ctk.CTkFrame(container, fg_color="transparent")
    content.pack(fill="both", expand=True, padx=20, pady=12)

    top = ctk.CTkFrame(content, fg_color="transparent")
    top.pack(fill="x", pady=(0, 10))
    make_button(top, "← Back to Home", show_home, primary=False, width=130).pack(side="left")

    form = ctk.CTkFrame(content, corner_radius=10)
    form.pack(side="left", fill="y", padx=(0, 12), pady=5)

    ctk.CTkLabel(form, text="Signal Parameters", font=("Arial", 15, "bold")).pack(
        anchor="w", padx=15, pady=(15, 10)
    )

    wave_var = ctk.StringVar(value="sine wave")
    ctk.CTkLabel(form, text="Signal type").pack(anchor="w", padx=15, pady=(4, 2))
    wave_menu = ctk.CTkOptionMenu(
        form, variable=wave_var, values=["sine wave", "cosine wave"], width=220
    )
    wave_menu.pack(padx=15, pady=(0, 8))

    # Keep labels visible above the text boxes instead of using placeholders.
    ctk.CTkLabel(form, text="Amplitude (A)").pack(anchor="w", padx=15, pady=(4, 0))
    amplitude_entry = ctk.CTkEntry(form, width=220)
    amplitude_entry.pack(padx=15, pady=(2, 6))
    amplitude_entry.insert(0, "2")

    ctk.CTkLabel(form, text="Phase shift (theta, radians)").pack(anchor="w", padx=15, pady=(4, 0))
    phase_entry = ctk.CTkEntry(form, width=220)
    phase_entry.pack(padx=15, pady=(2, 6))
    phase_entry.insert(0, "0")

    ctk.CTkLabel(form, text="Analog frequency (F, Hz)").pack(anchor="w", padx=15, pady=(4, 0))
    frequency_entry = ctk.CTkEntry(form, width=220)
    frequency_entry.pack(padx=15, pady=(2, 6))
    frequency_entry.insert(0, "5")

    ctk.CTkLabel(form, text="Sampling frequency (Fs, Hz)").pack(anchor="w", padx=15, pady=(4, 0))
    sampling_entry = ctk.CTkEntry(form, width=220)
    sampling_entry.pack(padx=15, pady=(2, 6))
    sampling_entry.insert(0, "20")

    ctk.CTkLabel(form, text="Duration (seconds)").pack(anchor="w", padx=15, pady=(4, 0))
    duration_entry = ctk.CTkEntry(form, width=220)
    duration_entry.pack(padx=15, pady=(2, 6))
    duration_entry.insert(0, "5")

    representation_var = ctk.StringVar(value="Discrete")
    ctk.CTkLabel(form, text="Representation").pack(anchor="w", padx=15, pady=(8, 2))
    ctk.CTkOptionMenu(
        form, variable=representation_var, values=["Discrete", "Continuous"], width=220
    ).pack(padx=15, pady=(0, 10))

    plot_frame = ctk.CTkFrame(content, corner_radius=10)
    plot_frame.pack(side="left", fill="both", expand=True, pady=5)

    def create_signal():
        global generated_signals
        try:
            A = float(amplitude_entry.get())
            theta = float(phase_entry.get())
            F = float(frequency_entry.get())
            Fs = float(sampling_entry.get())
            duration = float(duration_entry.get())

            indices, samples = generate_sinusoidal_signal(
                duration, A, theta, F, Fs, wave_var.get()
            )
            label = f"Generated {wave_var.get().title()} #{len(generated_signals) + 1}"
            generated_signals.append({
                "indices": indices,
                "samples": samples,
                "label": label,
                "wave_type": wave_var.get(),
                "A": A,
                "theta": theta,
                "F": F,
                "Fs": Fs,
                "duration": duration,
            })

            plot_generated_signal(
                indices, samples, label, plot_frame, representation_var.get()
            )
            messagebox.showinfo(
                "Signal Generated",
                f"{label} created successfully and saved for the Signal Display page."
            )
        except ValueError as error:
            messagebox.showerror("Invalid Parameters", str(error))
        except Exception as error:
            messagebox.showerror("Generation Error", f"Could not generate signal:\n{error}")

    make_button(form, "Generate Signal", create_signal).pack(
        fill="x", padx=15, pady=(5, 15)
    )


# =========================================================
# SIGNAL DISPLAY PAGE
# =========================================================

def show_display():
    clear_page()
    make_header(
        "Signal Display",
        "Display two loaded or generated signals together"
    )

    content = ctk.CTkFrame(container, fg_color="transparent")
    content.pack(fill="both", expand=True, padx=20, pady=12)

    make_button(
        content, "← Back to Home", show_home, primary=False, width=130
    ).pack(anchor="w", pady=(0, 12))

    # Build a list that can contain both file signals and generated signals.
    available_signals = []
    for i, (indices, samples) in enumerate(signals):
        available_signals.append({
            "label": f"Loaded Signal {i + 1}",
            "indices": np.asarray(indices),
            "samples": np.asarray(samples),
        })

    for item in generated_signals:
        available_signals.append({
            "label": item["label"],
            "indices": np.asarray(item["indices"]),
            "samples": np.asarray(item["samples"]),
        })

    if not available_signals:
        ctk.CTkLabel(
            content,
            text="No signals available. Load a text file in Signal Operations or generate a signal first.",
            text_color="gray",
            font=("Arial", 12),
            wraplength=700,
        ).pack(anchor="w", pady=10)
        return

    controls = ctk.CTkFrame(content, corner_radius=10)
    controls.pack(fill="x", pady=(0, 12))

    labels = [item["label"] for item in available_signals]
    first_var = ctk.StringVar(value=labels[0])
    second_var = ctk.StringVar(value=labels[1] if len(labels) > 1 else labels[0])
    mode_var = ctk.StringVar(value="Discrete")

    ctk.CTkLabel(controls, text="Signal 1:").grid(row=0, column=0, padx=(12, 5), pady=12)
    ctk.CTkOptionMenu(
        controls, variable=first_var, values=labels, width=190
    ).grid(row=0, column=1, padx=5, pady=12)

    ctk.CTkLabel(controls, text="Signal 2:").grid(row=0, column=2, padx=(12, 5), pady=12)
    ctk.CTkOptionMenu(
        controls, variable=second_var, values=labels, width=190
    ).grid(row=0, column=3, padx=5, pady=12)

    ctk.CTkLabel(controls, text="Representation:").grid(
        row=0, column=4, padx=(12, 5), pady=12
    )
    ctk.CTkOptionMenu(
        controls, variable=mode_var, values=["Discrete", "Continuous"], width=130
    ).grid(row=0, column=5, padx=5, pady=12)

    plot_frame = ctk.CTkFrame(content, corner_radius=10)
    plot_frame.pack(fill="both", expand=True)

    def display_two_signals():
        first = next(item for item in available_signals if item["label"] == first_var.get())
        second = next(item for item in available_signals if item["label"] == second_var.get())

        fig, ax = plt.subplots(figsize=(8, 5))
        representation = mode_var.get().lower()

        if representation == "discrete":
            ax.stem(
                first["indices"], first["samples"],
                linefmt="C0-", markerfmt="C0o", basefmt=" ",
            )
            ax.stem(
                second["indices"], second["samples"],
                linefmt="C1-", markerfmt="C1s", basefmt=" ",
            )
        else:
            ax.plot(
                first["indices"], first["samples"],
                color="C0", marker="o", markersize=3, linewidth=1.8,
            )
            ax.plot(
                second["indices"], second["samples"],
                color="C1", marker="s", markersize=3, linewidth=1.8,
            )

        from matplotlib.lines import Line2D
        ax.legend(handles=[
            Line2D([0], [0], color="C0", marker="o", label=first["label"]),
            Line2D([0], [0], color="C1", marker="s", label=second["label"]),
        ])
        ax.set_title(f"Two Signals - {mode_var.get()} Representation", fontsize=11, fontweight="bold")
        ax.set_xlabel("Sample Index (n)", fontsize=9)
        ax.set_ylabel("Amplitude", fontsize=9)
        apply_modern_plot_style(fig, ax)
        fig.tight_layout()
        embed_figure_in_frame(fig, plot_frame)

    make_button(
        controls, "Display Both", display_two_signals
    ).grid(row=0, column=6, padx=12, pady=10)


# =========================================================
# TASK 3: QUANTIZATION
# =========================================================

def quantize_signal(samples, levels):
    """Uniform quantization. Error convention matches the provided tests: xq - x."""
    samples = np.asarray(samples, dtype=float)
    if samples.size == 0:
        raise ValueError("The selected signal has no samples.")
    if not isinstance(levels, (int, np.integer)) or levels < 2:
        raise ValueError("The number of levels must be an integer greater than 1.")

    minimum = float(np.min(samples))
    maximum = float(np.max(samples))
    if np.isclose(minimum, maximum):
        raise ValueError("Quantization needs a signal with at least two different sample values.")

    step = (maximum - minimum) / levels
    interval_indices = []
    encoded_values = []
    quantized_values = []
    errors = []
    bits = int(np.ceil(np.log2(levels)))

    for sample in samples:
        # Keep the maximum sample in the final interval.
        interval = int(np.floor((sample - minimum) / step))
        interval = min(max(interval, 0), levels - 1)
        quantized = minimum + (interval + 0.5) * step
        interval_indices.append(interval + 1)  # Test case expects 1-based interval indices.
        encoded_values.append(format(interval, f"0{bits}b"))
        quantized_values.append(float(quantized))
        errors.append(float(quantized - sample))

    return interval_indices, encoded_values, quantized_values, errors


def show_quantization():
    clear_page()
    make_header(
        "Quantization - Task 3",
        "Choose a signal file and quantize it using bits or levels"
    )

    content = ctk.CTkFrame(container, fg_color="transparent")
    content.pack(fill="both", expand=True, padx=18, pady=12)
    make_button(content, "← Back to Home", show_home, primary=False, width=130).pack(anchor="w", pady=(0, 10))

    controls = ctk.CTkFrame(content, corner_radius=10)
    controls.pack(fill="x", pady=(0, 10))

    selected_file_var = ctk.StringVar(value="No input file selected")
    ctk.CTkLabel(controls, text="Input signal", font=("Arial", 12, "bold")).grid(
        row=0, column=0, padx=12, pady=(12, 4), sticky="w"
    )
    ctk.CTkLabel(controls, textvariable=selected_file_var, text_color="gray", wraplength=500).grid(
        row=1, column=0, padx=12, pady=(0, 10), sticky="w"
    )
    chosen = {"path": None}

    def choose_quantization_file():
        filename = filedialog.askopenfilename(
            title="Select a signal input file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            chosen["path"] = filename
            selected_file_var.set(filename)

    make_button(controls, "Browse…", choose_quantization_file, width=120).grid(
        row=0, column=1, rowspan=2, padx=12, pady=10
    )

    mode_var = ctk.StringVar(value="Bits")
    ctk.CTkLabel(controls, text="Input type").grid(row=2, column=0, padx=12, pady=(0, 3), sticky="w")
    ctk.CTkOptionMenu(controls, variable=mode_var, values=["Bits", "Levels"], width=150).grid(
        row=3, column=0, padx=12, pady=(0, 10), sticky="w"
    )

    amount_entry = ctk.CTkEntry(controls, width=150)
    amount_entry.insert(0, "3")
    ctk.CTkLabel(controls, text="Number of bits / levels").grid(
        row=2, column=1, padx=12, pady=(0, 3), sticky="w"
    )
    amount_entry.grid(row=3, column=1, padx=12, pady=(0, 10), sticky="w")

    output_frame = ctk.CTkFrame(content, corner_radius=10)
    output_frame.pack(fill="both", expand=True)
    output_text = ctk.CTkTextbox(output_frame, height=180, font=("Consolas", 11))
    output_text.pack(fill="both", expand=True, padx=10, pady=10)

    plot_frame = ctk.CTkFrame(content, corner_radius=10, height=260)
    plot_frame.pack(fill="both", expand=True, pady=(10, 0))

    def run_quantization():
        if not chosen["path"]:
            messagebox.showwarning("Missing input", "Please browse and select a signal input file first.")
            return
        try:
            indices, samples = read_signal(chosen["path"])
            amount = int(amount_entry.get())
            if amount <= 0:
                raise ValueError("Enter a positive integer.")
            if mode_var.get() == "Bits":
                if amount > 16:
                    raise ValueError("Please choose 16 bits or fewer to keep the output manageable.")
                levels = 2 ** amount
            else:
                levels = amount
            interval_ids, encoded, quantized, errors = quantize_signal(samples, levels)
            bits = int(np.ceil(np.log2(levels)))

            lines = [f"Levels: {levels}    Bits used for encoding: {bits}", ""]
            if mode_var.get() == "Levels":
                lines.append("Index | Code | Quantized | Error (xq - x)")
                lines.append("-" * 43)
                for idx, code, q, err in zip(interval_ids, encoded, quantized, errors):
                    lines.append(f"{idx:5d} | {code:4s} | {q:9.4f} | {err: .4f}")
            else:
                lines.append("Code | Quantized")
                lines.append("-" * 23)
                for code, q in zip(encoded, quantized):
                    lines.append(f"{code:4s} | {q:9.4f}")
            output_text.configure(state="normal")
            output_text.delete("1.0", "end")
            output_text.insert("1.0", "\n".join(lines))

            fig, axes = plt.subplots(2, 1, figsize=(7, 4.5), sharex=True)
            axes[0].stem(indices, samples, linefmt="C0-", markerfmt="C0o", basefmt=" ", label="Original")
            axes[0].step(indices, quantized, where="mid", color="C1", linewidth=1.8, label="Quantized")
            axes[0].set_title("Original and Quantized Signal")
            axes[0].set_ylabel("Amplitude")
            axes[0].legend()
            axes[1].stem(indices, errors, linefmt="C2-", markerfmt="C2o", basefmt=" ")
            axes[1].axhline(0, color="gray", linewidth=1)
            axes[1].set_title("Quantization Error (quantized - original)")
            axes[1].set_xlabel("Sample Index (n)")
            axes[1].set_ylabel("Error")
            for ax in axes:
                apply_modern_plot_style(fig, ax)
            fig.tight_layout()
            embed_figure_in_frame(fig, plot_frame)
        except (ValueError, OSError) as error:
            messagebox.showerror("Quantization Error", str(error))
        except Exception as error:
            messagebox.showerror("Error", f"Could not quantize signal:\n{error}")

    make_button(controls, "Quantize Signal", run_quantization).grid(
        row=3, column=2, padx=12, pady=(0, 10), sticky="e"
    )


# Start on the home page
show_home()
root.mainloop()
