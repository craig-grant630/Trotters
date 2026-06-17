
import tkinter as tk
from tkinter import ttk
# Colours, fonts for UI
#====================================================================================================
BG_COLOUR = "#1a1a2e"
BG_COLOUR2 = "#16213e"
BG_COLOUR3 = "#0f3460"

BORDER = "#0f3460"
ENTRY_BG="#0d2137"
FG_COLOUR = "#eaeaea"
FG_COLOUR2 = "#a0a0b0"
MSG_BG_COLOUR = BG_COLOUR2

ACCENT = "#e94560"

FONT_BODY = ("Helvetica", 12)
FONT_HEADER = ("Helvetica", 20, "bold")
FONT_SMALL = ("Helvetica", 10)
FONT_BUTTON= ("Helvetica", 12, "bold")
FONT_MSG = ("helvetica", 9)
#=================================================================================================================
#Stlyed Reusable Widgets

# Card is a frame with the border
def card(parent, padx=10, pady=14, bg=BG_COLOUR2):
    frame = tk.Frame(parent, bg=bg, padx=padx, pady=pady,
                     highlightthickness=1, highlightbackground=BORDER)
    return frame

# Styled Label for quick use for displaying text
def styled_label(parent, text, font=FONT_BODY, fg=FG_COLOUR, bg=BG_COLOUR2, **kwargs):
    return tk.Label(parent, text=text, font=font,
                    fg=fg, bg=bg, **kwargs)

# Dropdown menu that is styled that can be reused
def styled_combobox(parent, options, width, **kwargs):

    # Fundamental to overwrite the base styling
    parent.option_add("*TCombobox*Listbox.background", BG_COLOUR3)
    parent.option_add('*TCombobox*Listbox.foreground', 'white')
    parent.option_add('*TCombobox*Listbox.selectBackground', ACCENT)
    parent.option_add('*TCombobox*Listbox.font', FONT_BODY)

    style = ttk.Style()
    style.theme_use("clam")

    style.configure("Dark.TCombobox", background=BG_COLOUR3, font=FONT_BODY,
                    fieldbackground=ENTRY_BG, foreground=FG_COLOUR,arrowcolor=ACCENT,
                    bordercolor=BORDER, lightcolor="white", darkcolor="white")
    style.map("Dark.TCombobox", fieldbackground=[("readonly",BG_COLOUR3), ("focus", BG_COLOUR3), ("pressed",BG_COLOUR3)], foreground=[("readonly",FG_COLOUR)],
              selectbackground=[("readonly",BG_COLOUR3), ("pressed",BG_COLOUR3)], selectforeground=[("readonly","white")])

    combobox = ttk.Combobox(parent, state="readonly", values=options, width=width, style="Dark.TCombobox", font=FONT_BODY, **kwargs)
    return combobox

def separator(parent, bg=BORDER):
    return tk.Frame(parent, bg=bg, height=1)

def styled_treeview(parent, columns, headings, widths):
    style = ttk.Style()
    style.theme_use('clam')

    style.configure("Dark.Treeview",background=BG_COLOUR2,foreground=FG_COLOUR2,fieldbackground=BG_COLOUR2,
        rowheight=27,font=FONT_SMALL, borderwidth=0)
    style.map("Dark.Treeview",background=[('selected', ACCENT)])

    style.configure("Dark.Treeview.Heading",background=BG_COLOUR3,foreground="white",
                    font=("Helvetica",10, "bold"),rowheight=35,borderwidth=0,relief="flat")
    style.map("Dark.Treeview.Heading",background=[('active', BG_COLOUR3)],foreground=[('active', ACCENT)])

    tree = ttk.Treeview(parent, columns=columns, style="Dark.Treeview", show="headings")

    for col, heading, width in zip(columns, headings, widths):
        tree.heading(col, text=heading)
        tree.column(col, width=width, anchor="center")

    return tree