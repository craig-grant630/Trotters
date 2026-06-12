import tkinter as tk
from tkinter import ttk, messagebox
from application import StudyBuddyApp
from classes import VALID_DAYS, VALID_PERIODS

# Styling references
# https://www.pythontutorial.net/tkinter/ttk-style/
# https://tkdocs.com/tutorial/widgets.html
# https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/entry.html
# https://ttkbootstrap.readthedocs.io/en/version-0.5/widgets/combobox.html
# https://tkdocs.com/tutorial/customstyles.html
# https://stackoverflow.com/questions/68883001/how-to-make-tkinter-combobox-dark-themed
# https://www.geeksforgeeks.org/python/python-pack-method-in-tkinter/
# https://wiki.tcl-lang.org/page/tkinter.Listbox
# https://www.pythontutorial.net/tkinter/tkinter-treeview/
# https://stackoverflow.com/questions/7727804/tkinter-using-scrollbars-on-a-canvas

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
#============================================================================================================
# Initial setup of root container - configure title and size of window, instantiate Studdy Buddy App and set user
# Contains methods for clearing and switching frame logic
class StudyBuddyUI:

    def __init__(self):
        self.app = StudyBuddyApp()
        self.user = None

        self.root = tk.Tk()
        self.root.title("TiT Study Buddy")
        self.root.geometry("800x700")
        self.root.configure(bg=BG_COLOUR)
        self.root.resizable(width=True, height=True)

        self.container = tk.Frame(self.root, bg=BG_COLOUR)
        self.container.pack(fill="both", expand=True)

        self.show_login(mode="student")
        self.root.mainloop()

    def clear(self):
        for w in self.container.winfo_children():
            w.destroy()

    def show_login(self, mode):
        self.clear()
        LoginFrame(self.container, self, mode)

    def show_register(self):
        self.clear()
        RegisterFrame(self.container, self)

    def show_dashboard(self):
        self.clear()
        Dashboard(self.container, self)

    def show_request_form(self, request=None):
        self.clear()
        AddEditRequest(self.container, self, request)

    def show_request_matches(self, request):
        self.clear()
        RequestResults(self.container, self, request)

    def show_admin_dashboard(self):
        self.clear()
        AdminDashboard(self.container, self)

# =====================================================================================
# Header frames used withing main frames of application
class WelcomeHeader(tk.Frame):
    def __init__(self, parent, ui):
        #create instance of the login frame:
        super().__init__(parent, bg=BG_COLOUR2)
        self.pack(fill="both")
        self.ui = ui

        styled_label(self, "Welcome to TiT Study Buddy", font=FONT_HEADER, fg=ACCENT, bg=BG_COLOUR2).pack(pady=(0,4))
        styled_label(self, "Trotters Independent Tuition - Peckham, South East London", font=FONT_SMALL,
                     fg=FG_COLOUR2, bg=BG_COLOUR2).pack(pady=(0,10))
        separator(self).pack(fill="x", pady=10)

class InternalHeader(tk.Frame):
    def __init__(self, parent, ui, title):
        super().__init__(parent, bg=BG_COLOUR3)
        self.pack(fill="both")
        self.ui = ui

        tk.Button(self, text="TiT", bg=BG_COLOUR3, fg=ACCENT, font=FONT_HEADER, command=self.ui.show_dashboard, relief="flat", activebackground=BG_COLOUR3, cursor="fleur").pack(side="left", padx=10)
        styled_label(self, text=f" Study Buddy   |   {title}", bg= BG_COLOUR3,font=FONT_BUTTON, fg=FG_COLOUR).pack(side="left", padx=10, pady=(10,2))

        tk.Button(self, text="Logout", bg=BG_COLOUR2, fg="white", font=("Helvetica", 11, "bold"), relief="flat",
                  borderwidth=1, width=8, command=lambda: ui.show_login(mode="student")).pack(side="right", padx=10)
        row = tk.Frame(parent, bg=BG_COLOUR3)
        row.pack(fill="x")
        separator(row, ACCENT).pack(fill="x", pady=2, padx=100)
#==============================================================================================
# Main frames of application
class LoginFrame(tk.Frame):
    def __init__(self, parent, ui, mode="student"):
        # create instance of the login frame:
        super().__init__(parent, bg=BG_COLOUR)
        self.pack(fill="both", expand=True)
        self.ui = ui
        self.login_msg = tk.StringVar()
        self.mode = mode

        outer = tk.Frame(self, bg=BG_COLOUR2,padx=40, pady=36)
        outer.place(relx=0.5, rely=0.5, anchor="center")

        WelcomeHeader(outer, ui)

        row = tk.Frame(outer, bg=BG_COLOUR2)
        row.pack(pady=10)
        login_frame_btn = tk.Button(row, text="Login", bg=ACCENT, fg="white", font=FONT_BUTTON, relief="flat",
                                    borderwidth=1, width=20, command=lambda: ui.show_login(mode="student"))
        login_frame_btn.grid(row=0, column=0)

        register_frame_btn = tk.Button(row, text="Register", bg=BG_COLOUR, fg="white", font=FONT_BUTTON, relief="flat",
                                       borderwidth=1, width=20, command=ui.show_register)
        register_frame_btn.grid(row=0, column=1)

        row2 = tk.Frame(outer, bg=BG_COLOUR2)
        row2.pack(pady=5)

        tk.Label(row2, bg=BG_COLOUR2, fg="red",font=FONT_MSG, textvariable=self.login_msg).grid()
        if self.mode == "student":
            styled_label(row2, "Student ID (10 digits)", bg=BG_COLOUR2, font=FONT_BODY,
                         fg=FG_COLOUR2).grid(row=1, column=0, sticky="w", padx=8, pady=8)
        else:
            styled_label(row2, "Admin Username", bg=BG_COLOUR2, font=FONT_BODY,
                             fg=FG_COLOUR2).grid(row=1, column=0, sticky="w", padx=8, pady=8)

        self.login_id = tk.Entry(row2, bg=BG_COLOUR3,fg="white", relief="flat", font=FONT_BODY, width=40, highlightcolor=ACCENT, highlightthickness=1, insertbackground='white')
        self.login_id.grid(row=2, column=0, sticky="w", padx=8)

        styled_label(row2, "Password", bg=BG_COLOUR2, fg=FG_COLOUR2,
                     font=FONT_BODY).grid(row=3, column=0, sticky="w", padx=8, pady=8)
        self.login_pwd = tk.Entry(row2, bg=BG_COLOUR3, fg="white", relief="flat", font=FONT_BODY, width=40, show="*",
                                  highlightcolor=ACCENT, highlightthickness=1, insertbackground='white')
        self.login_pwd.grid(row=4, column=0, sticky="w", padx=8)

        tk.Button(outer, text="Login >>", bg=BG_COLOUR2, fg="white", font=FONT_BUTTON, relief="flat",
                  borderwidth=1, command=self.login).pack(pady=15)
        separator(outer, ACCENT).pack(fill="x", pady=2, padx=100)
        if self.mode == "student":
            tk.Button(outer, text="For admin login click here", bg=BG_COLOUR2, font=FONT_SMALL, fg=FG_COLOUR2,relief="flat", command=lambda: ui.show_login(mode="admin")).pack(pady=5)
        else:
            tk.Button(outer, text="For student login click here", bg=BG_COLOUR2, font=FONT_SMALL, fg=FG_COLOUR2,
                      relief="flat", command=lambda: ui.show_login(mode="student")).pack(pady=5)

    def login(self):
        sid = self.login_id.get()
        password = self.login_pwd.get()
        if self.mode == "student":
            valid, result = self.ui.app.authenticate(sid, password)

            if valid:
                self.ui.user = result
                # show_dash
                self.ui.show_dashboard()
            else:
                self.login_msg.set(result)
        else:
            valid, result = self.ui.app.authenticate_admin(sid, password)

            if valid:
                self.ui.user = result
                # show_dash
                self.ui.show_admin_dashboard()
            else:
                self.login_msg.set(result)

class RegisterFrame(tk.Frame):
    def __init__(self, parent, ui):
        super().__init__(parent, bg=BG_COLOUR)
        self.pack(fill="both", expand=True)
        self.ui = ui
        self.register_msg = tk.StringVar()

        outer = tk.Frame(self, bg=BG_COLOUR2, padx=40, pady=20)
        outer.place(relx=0.5, rely=0.5, anchor="center")

        WelcomeHeader(outer, ui)

        row = tk.Frame(outer, bg=BG_COLOUR2)
        row.pack(pady=10)
        login_frame_btn = tk.Button(row, text="Login", bg=BG_COLOUR, fg="white", font=FONT_BUTTON, relief="flat",
                                    borderwidth=1, width=20, command=lambda: ui.show_login(mode="student"))
        login_frame_btn.grid(row=0, column=0)
        register_frame_btn = tk.Button(row, text="Register", bg=ACCENT, fg="white", font=FONT_BUTTON, relief="flat",
                                       borderwidth=1, width=20, command=ui.show_register)
        register_frame_btn.grid(row=0, column=1)

        fields = [
            ("Student ID (10 digits)", False),
            ("Full Name", False),
            ("Password", True),
            ("Confirm Password", True),
        ]
        self.entries = {}
        for label, show in fields:
            row2 = tk.Frame(outer, bg=BG_COLOUR2)
            row2.pack(fill="x")
            row2.grid_columnconfigure(0, minsize=180, uniform="reg_col")
            styled_label(row2, label, bg=BG_COLOUR2, font=FONT_BODY,
                         fg=FG_COLOUR2).grid(row=0, column=0, sticky="e", padx=8, pady=5)
            if show:
                entry = tk.Entry(row2, bg=BG_COLOUR3, fg="white", relief="flat", font=FONT_BODY, width=27, show="*",
                                 highlightcolor=ACCENT, highlightthickness=1)
            else:
                entry = tk.Entry(row2, bg=BG_COLOUR3, fg="white", relief="flat", font=FONT_BODY, width=27,
                                 highlightcolor=ACCENT, highlightthickness=1)

            self.entries[label] = entry
            entry.grid(row=0, column=1, sticky="w", padx=8)

        separator(outer).pack(fill="x", pady=10)
        self.row2 = tk.Frame(outer, bg=BG_COLOUR2)
        self.row2.pack(fill="x")
        self.row2.grid_columnconfigure(0, minsize=180, uniform="reg_col")

        styled_label(self.row2, "Year of Study:", bg=BG_COLOUR2, font=FONT_BODY,
                                 fg=FG_COLOUR2).grid(row=2, column=0, sticky="e", padx=6)
        self.yos = styled_combobox(self.row2, ["  1","  2","  3"], 3)
        self.yos.grid(row=2, column=1, sticky="w", padx=6, pady=5)

        prog_options = []
        for p in self.ui.app.programmes.values():
            prog_options.append(f"{p.programme_code} - {p.name}")
        styled_label(self.row2, "Programme:", bg=BG_COLOUR2, font=FONT_BODY,
                     fg=FG_COLOUR2).grid(row=0, column=0, sticky="e", padx=6)
        self.programme_drop = styled_combobox(self.row2, prog_options, 26)
        self.programme_drop.grid(row=0, column=1, sticky="w", padx=6, pady=5)

        camp_options = []
        for c in self.ui.app.campuses.values():
            camp_options.append(f"{c.name} - {c.campus_code}")
        styled_label(self.row2, "Campus:", bg=BG_COLOUR2, font=FONT_BODY,
                     fg=FG_COLOUR2).grid(row=1, column=0, sticky="e", padx=6)
        self.campus_drop = styled_combobox(self.row2, camp_options, 26)
        self.campus_drop.grid(row=1, column=1, sticky="w", padx=6, pady=5)

        register_frame_btn = tk.Button(self.row2, text="Create Account", bg=BG_COLOUR3, fg="white", font=FONT_BUTTON, relief="flat",
                                    borderwidth=1, width=15, command=self.register_student)
        register_frame_btn.grid(row=3, column=1, sticky="e", pady=(40,5), padx = 10)

        self.msg_label = tk.Label(self.row2, bg=BG_COLOUR2, fg="red", textvariable=self.register_msg, font=FONT_MSG, wraplength=180)
        self.msg_label.grid(row=3, column=0, sticky="sw", pady=5)

    def register_student(self):
        sid = self.entries["Student ID (10 digits)"].get()
        name = self.entries["Full Name"].get()
        password = self.entries["Password"].get()
        con_password = self.entries["Confirm Password"].get()
        prog_sel = self.programme_drop.get()
        camp_sel = self.campus_drop.get()
        try:
            prog_code = prog_sel.split("-")[0].strip()
            camp_code = camp_sel.split("-")[1].strip()
        except IndexError:
            prog_code= None
            camp_code = None
        year = self.yos.get().strip()

        valid, msg = self.ui.app.check_register_credentials(sid, password, con_password, camp_code, prog_code,year, name)

        if not valid:
            self.register_msg.set(msg)
            self.msg_label = tk.Label(self.row2, bg=BG_COLOUR2, fg="red", textvariable=self.register_msg, font=FONT_MSG,
                                      wraplength=180)
            self.msg_label.grid(row=3, column=0, sticky="sw", pady=5)
        else:
            self.ui.app.add_student(sid, name, password, camp_code, prog_code, year)
            self.register_msg.set("Student Registered Successfully: You are welcome to Log in")
            self.msg_label = tk.Label(self.row2, bg=BG_COLOUR2, fg="green", textvariable=self.register_msg, font=FONT_MSG,
                                      wraplength=180)
            self.msg_label.grid(row=3, column=0, sticky="sw", pady=5)

class Dashboard(tk.Frame):
    def __init__(self, parent, ui):
        super().__init__(parent, bg=BG_COLOUR)
        self.pack(fill="both", expand=True, pady=(40,40), padx=20)
        self.ui = ui

        student = self.ui.user
        # Find all Information of Programme, Campus, Requests for user
        programme_info = self.ui.app.programmes[student.programme_code]
        self.campus_info = self.ui.app.campuses[student.campus_code]
        self.requests = self.ui.app.get_requests_for_student(student.student_id)
        #===============================================================================================================
        #HEADER
        InternalHeader(self, ui, f"Dashboard")

        row1 = tk.Frame(self, bg=BG_COLOUR3)
        row1.pack(fill="x")

        styled_label(row1, f"Welcome {student.name},", bg=BG_COLOUR3, font=FONT_BODY).pack(side="left",pady=10, padx=10)
        styled_label(row1, f"{programme_info.name} | {self.campus_info.name} | Year {student.year_of_study}", bg=BG_COLOUR3,fg=FG_COLOUR2, font=FONT_SMALL).pack(pady=10, padx=10, side="left")
        # ==============================================================================================================
        # LEFT SIDE - action buttons
        row2 = tk.Frame(self, bg=BG_COLOUR)
        row2.pack(fill="both", expand=True)

        left_side_frame = card(row2, bg=BG_COLOUR2)
        left_side_frame.pack(side="left", fill="both", expand=True)

        styled_label(left_side_frame, "Actions", font=FONT_BUTTON, fg=ACCENT).pack(anchor="w")
        separator(left_side_frame, bg=ACCENT).pack(fill="x", pady=8, padx=10)
        add_button = tk.Button(left_side_frame, bg=BG_COLOUR3, fg=FG_COLOUR,relief="flat", text="Add Request",
                               font=("Helvetica", 10, "bold"), width=15, command=self.new_request)
        add_button.pack(pady=3)
        edit_button = tk.Button(left_side_frame, bg=BG_COLOUR3, fg=FG_COLOUR, relief="flat", text="Edit Request",
                               font=("Helvetica", 10, "bold"), width=15, command=self.edit_request)
        edit_button.pack(pady=3)
        delete_button = tk.Button(left_side_frame, bg=BG_COLOUR3, fg=FG_COLOUR, relief="flat", text="Delete Request",
                               font=("Helvetica", 10, "bold"), width=15, command=self.delete_request)
        delete_button.pack(pady=3)
        matches_button = tk.Button(left_side_frame, bg=ACCENT, fg=FG_COLOUR, relief="flat", text="Find Matches",
                                  font=("Helvetica", 10, "bold"), width=15, command=self.find_matches)
        matches_button.pack(side="bottom")
        #===============================================================================================================
        right_side_frame = card(row2, bg=BG_COLOUR2)
        right_side_frame.pack(side="left", fill="both", expand=True)

        styled_label(right_side_frame, "My Match Requests", font=FONT_BUTTON, fg=ACCENT).pack(anchor="w")
        separator(right_side_frame, bg=ACCENT).pack(fill="x", pady=8, padx=10)

        self.treeview = styled_treeview(right_side_frame, ["id", "module", "campus", "year", "slots"],["#", "Module","Campus","Year", "Slots"],[40, 120,120,90,90])
        self.treeview.pack(fill="both", expand=True)
        self.refresh_dashboard_treeview()

    def refresh_dashboard_treeview(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        student_requests = self.ui.app.get_requests_for_student(self.ui.user.student_id)

        if not student_requests:
            self.treeview.insert("", "end", iid="none", values=("", "No requests yet", "", "", ""))
            return

        for item in student_requests:
            slots_count = f"{len(item.availability)} slots" if hasattr(item, 'availability') else "0 slots"

            self.treeview.insert("","end",iid=str(item.request_id),
                values=(str(item.request_id),f"{item.module_code}",item.campus_code,f"Year {item.year}",slots_count))

    def selection_treeview(self):
        selection = self.treeview.selection()
        if not selection or selection[0] == "none":
            return None
        request_id = int(selection[0])
        return self.ui.app.get_request_by_id(request_id)

    def new_request(self):
        self.ui.show_request_form()

    def edit_request(self):
        r_obj = self.selection_treeview()
        if not r_obj:
            messagebox.showwarning("Warning", "No requests selected")
            return
        self.ui.show_request_form(r_obj)

    def delete_request(self):
        request = self.selection_treeview()
        if not request:
            messagebox.showwarning("Warning", "No requests selected")
            return
        if not messagebox.askyesno("Delete Request", f"Are you sure you want to delete request ID: {request.request_id}?"):
            return
        valid, error = self.ui.app.delete_request(request.request_id, self.ui.user.student_id)
        if valid:
            self.refresh_dashboard_treeview()
        else:
            messagebox.showwarning("Warning", "Could not delete request")

    def find_matches(self):
        r_obj = self.selection_treeview()
        if not r_obj:
            messagebox.showwarning("Warning", "No requests selected")
            return
        self.ui.show_request_matches(r_obj)

class AddEditRequest(tk.Frame):
    def __init__(self, parent, ui, request=None):
        super().__init__(parent, bg=BG_COLOUR)
        self.pack(fill="both", expand=True, pady=(40, 40), padx=20)
        self.ui = ui
        self.availability = []
        if request is not None:
            self.request = request
            mode = "Edit Request"
            self.availability = list(request.availability)
        else:
            mode = "Add Request"
            self.request = None

        # HEADER
        InternalHeader(self, ui, f"{mode}")

        row1 = tk.Frame(self, bg=BG_COLOUR)
        row1.pack(fill="both", expand=True)
#==============================================================================================
        # LEFT FORM DROPDOWNS
        left_side_frame = card(row1, bg=BG_COLOUR2)
        left_side_frame.pack(side="left", fill="both", expand=True)

        styled_label(left_side_frame, mode, font=FONT_BUTTON, fg=ACCENT).pack(anchor="w")
        separator(left_side_frame, bg=ACCENT).pack(fill="x", pady=8, padx=10)

        student = self.ui.user
        form = tk.Frame(left_side_frame, bg=BG_COLOUR2)
        form.pack(anchor="w")

        camp_opt = []
        for c in self.ui.app.campuses.values():
            camp_opt.append(f"{c.campus_code} - {c.name}")

        styled_label(form, "Campus", bg=BG_COLOUR2, width=14, anchor="e").grid(row=0, column=0, padx=8, pady=6)
        self.campus_cb = styled_combobox(form, camp_opt, width=30)
        self.campus_cb.grid(row=0, column=1, pady=6, sticky="w")

        prog = self.ui.app.programmes.get(student.programme_code)
        prog_label = f"{student.programme_code} - {prog.name}"

        if len(prog.campus_codes) ==1:
            self.campus_cb.set(f"{student.campus_code} - {self.ui.app.campus_name(student.campus_code)}")
            self.campus_cb.config(state="disabled")

        styled_label(form, "Programme", bg=BG_COLOUR2, width=14, anchor="e").grid(row=1, column=0, padx=8, pady=6)
        self.programme_cb = styled_combobox(form, [prog_label], width=30)
        self.programme_cb.grid(row=1, column=1, pady=6, sticky="w")
        self.programme_cb.set(prog_label)
        self.programme_cb.config(state="disabled")

        styled_label(form, "Year of Study", bg=BG_COLOUR2, width=14, anchor="e").grid(row=2, column=0, padx=8, pady=6)
        self.year_cb = styled_combobox(form, [str(student.year_of_study)], width=6)
        self.year_cb.grid(row=2, column=1, pady=6, sticky="w")
        self.year_cb.set(str(student.year_of_study))
        self.year_cb.config(state="disabled")

        year_mods = prog.modules_for_year(int(student.year_of_study))
        mod_opts = [f"{m.module_code} - {m.name}" for m in year_mods]

        styled_label(form, "Module", bg=BG_COLOUR2, width=14, anchor="e").grid(row=3, column=0, padx=8, pady=6)
        self.module_cb = styled_combobox(form, mod_opts, width=30)
        self.module_cb.grid(row=3, column=1, pady=6, sticky="w")

        self.msg = tk.StringVar()
        tk.Label(form, textvariable=self.msg, bg=BG_COLOUR2, fg="red", wraplength=200).grid(row=4, column=1, pady=8, sticky="w")
        if request:
            save_button = tk.Button(form, bg=ACCENT, fg=FG_COLOUR, relief="flat", text="Save", width=7, command=self.submit)
            save_button.grid(row=5, column=1, padx=3, pady=(20,0), sticky="w")
        else:
            add_button = tk.Button(form, bg=ACCENT, fg=FG_COLOUR, relief="flat", text="Add Request", width=12, command=self.submit)
            add_button.grid(row=5, column=1, padx=3, pady=(20, 0), sticky="w")

        cancel_button = tk.Button(form, bg=ACCENT, fg=FG_COLOUR, relief="flat", text="Cancel", width=7, command=self.ui.show_dashboard)
        cancel_button.grid(row=5, column=1, padx=3, pady=(20, 0))
#==========================================================================================================================
        #RIGHT SIDE DROPDOWNS AND TREEVIEW
        right_side_frame = card(row1, bg=BG_COLOUR2)
        right_side_frame.pack(fill="both", expand=True, side="right")

        styled_label(right_side_frame, "Availability Timeslots", font=FONT_BUTTON, fg=ACCENT).pack(anchor="w")
        separator(right_side_frame, bg=ACCENT).pack(fill="x", pady=8, padx=10)

        styled_label(right_side_frame, "Add the days and times you are free to meet", font=FONT_SMALL, fg=FG_COLOUR2, bg=BG_COLOUR2).pack(anchor="w", pady=(0,8))

        slot_row = tk.Frame(right_side_frame, bg=BG_COLOUR2)
        slot_row.pack(anchor="w",pady=4)

        self.day_cb = styled_combobox(slot_row, VALID_DAYS, width=10)
        self.day_cb.pack(side="left", padx=(0,8))

        self.period_cb = styled_combobox(slot_row, VALID_PERIODS, width=10)
        self.period_cb.pack(side="left", padx=(0,8))

        tk.Button(slot_row, text="Add", bg="green", fg=FG_COLOUR, width=6, relief="flat", font=("Helvetica", 10, "bold"), command=self.add_availability_treeview).pack(side="left")

        self.timeslot_treeview = styled_treeview(right_side_frame,["day","period"], ["Day", "Period"], [10,15])
        self.timeslot_treeview.pack(fill="both", expand=True, pady=8)

        tk.Button(right_side_frame, text="Remove Selected", bg="red", fg=FG_COLOUR, relief="flat", font=("Helvetica", 10, "bold"), command=self.remove_availability_treeview).pack(pady=4)
        self.refresh_request_form()

    def refresh_request_form(self):
        for item in self.timeslot_treeview.get_children():
            self.timeslot_treeview.delete(item)
        if not self.availability:
            self.timeslot_treeview.insert("", "end", iid="none", values=("No timeslots yet", ""))
            return
        for index, item in enumerate(self.availability):
            self.timeslot_treeview.insert("", "end", iid=str(index),
                                 values=(item['day'], item['period']))

    def remove_availability_treeview(self):
        selection = self.timeslot_treeview.selection()
        if not selection or selection[0] == "none":
            return
        idx = int(selection[0])
        del self.availability[idx]
        self.refresh_request_form()

    def add_availability_treeview(self):
        day = self.day_cb.get()
        period = self.period_cb.get()
        if not day or not period:
            messagebox.showerror("Error", "Please select a day and period in order to add availability")
            return
        slot = {"day": day, "period": period}
        if slot in self.availability:
            messagebox.showerror("Error", "Availability already added")
            return
        self.availability.append(slot)
        self.refresh_request_form()

    def submit(self):
        self.msg.set("")
        student = self.ui.user
        campus = self.campus_cb.get().split("-")[0].strip()
        module = self.module_cb.get().split("-")[0].strip()
        if not campus or not module:
            self.msg.set("Please select a campus and module")
            return
        if not self.availability:
            self.msg.set("Please add at least one availability")
            return

        if self.request:
            valid, result = self.ui.app.edit_request(self.request.request_id, student.student_id,
                                                     campus, module, self.availability)
            if valid:
                self.ui.show_dashboard()
            else:
                self.msg.set(result)

        if not self.request:
            valid, result = self.ui.app.add_request(student.student_id, student.programme_code,
                                                     campus, module, self.availability)

            if valid:
                self.ui.show_dashboard()
            else:
                self.msg.set(result)

class RequestResults(tk.Frame):
    def __init__(self, parent, ui, request):
        super().__init__(parent, bg=BG_COLOUR)
        self.pack(fill="both", expand=True, pady=(40, 40), padx=20)
        self.ui = ui
        self.request = request
        # ===============================================================================================================
        # HEADER
        InternalHeader(self, ui, f"Dashboard")

        row1 = tk.Frame(self, bg=BG_COLOUR3)
        row1.pack(fill="x")
        styled_label(row1, f"Source Request: #{request.request_id} | {request.module_code} | {request.campus_code}", bg=BG_COLOUR3, fg=FG_COLOUR2, font=FONT_SMALL).pack(pady=10, padx=10, side="left")
        tk.Button(row1, text="Back to Dashboard", bg=BG_COLOUR3, fg=FG_COLOUR2, relief="flat", command=self.ui.show_dashboard,
                  font=("Helvetica", 10, "bold")).pack(pady=2, side="right", padx=5)
        # =========================================================================================

        row2 = tk.Frame(self, bg=BG_COLOUR2)
        row2.pack(fill="both", expand=True)

        # find matches using application function
        matches = self.ui.app.find_matches(self.request)
        if not matches:
            no_match = tk.Frame(row2, bg=BG_COLOUR3)
            no_match.pack(fill="x", pady=20, padx=20)

            styled_label(
                no_match,"No matches found for this request",font=FONT_BUTTON,fg=FG_COLOUR2,bg=BG_COLOUR3).pack(pady=20, padx=20)
            return

        # Only set up canvas and scroll if matches actually exist
        # Using Canavs and scroll to create a scrollable frame for all matches
        canvas = tk.Canvas(row2, bg=BG_COLOUR, highlightthickness=0)
        canvas.pack(fill="both", expand=True, side="left")

        scrollbar = tk.Scrollbar(row2, orient="vertical", command=canvas.yview, bg=BG_COLOUR3,troughcolor=BG_COLOUR2)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        inner = tk.Frame(canvas, bg=BG_COLOUR)
        canvas_window=canvas.create_window((0,0), window=inner, anchor="nw")

        styled_label(inner, f"Found {len(matches)} matches", font=FONT_BUTTON, fg="green", bg=BG_COLOUR).pack(
            anchor="w", pady=(4, 8))

        def canvas_configuration(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_window, width=canvas.winfo_width())

        inner.bind("<Configure>", canvas_configuration)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=canvas.winfo_width()))

        for rank, match in enumerate(matches, 1):
            self.build_match_card(inner, rank, match)

    def build_match_card(self, parent, rank, match):
        r = match["request"]
        score = match["score"]
        overlaps = match["overlaps"]

        score_colour = "green" if score >= 6 else ("orange" if score >= 4 else FG_COLOUR)

        c = card(parent, bg=BG_COLOUR2)
        c.pack(fill="x", pady=5)
        c.grid_columnconfigure(0, weight=0)
        c.grid_columnconfigure(1, weight=1)
        c.grid_columnconfigure(2, weight=0)

        tk.Label(c, text=f"#{rank}", font=FONT_BUTTON, fg="white", bg=ACCENT, width=4).grid(row=0, column=0,
                                                                                            sticky="nw")
        details = tk.Frame(c, bg=BG_COLOUR2)
        details.grid(row=0, column=1, pady=(8, 8))

        info = [("Campus", self.ui.app.campus_name(r.campus_code)), ("Programme", r.programme_code),
                ("Year", f"Year {r.year}"),
                ("Module", r.module_code), ("Request ID", f"#{r.request_id}")]

        for i, (label, value) in enumerate(info):
            col = (i % 2) * 2
            row = i // 2

            styled_label(details, f"{label}:", fg=FG_COLOUR2, bg=BG_COLOUR2, anchor="e", width=11).grid(
                row=row, column=col, sticky="e", pady=2, padx=(0, 4))
            styled_label(details, value, fg=FG_COLOUR, bg=BG_COLOUR2, anchor="w").grid(row=row, column=col + 1, sticky="w", pady=2)

        tk.Label(c, text=f"Score: {score}", font=FONT_BUTTON, fg=score_colour, bg=BG_COLOUR2).grid(
            row=0, column=2, sticky="ne", padx=(0, 12), pady=4)

        available_frame = tk.Frame(c, bg=BG_COLOUR2)
        available_frame.grid(row=2, columnspan=3, sticky="w")

        styled_label(available_frame,"Availability Slots: ", fg=FG_COLOUR2, bg=BG_COLOUR2, anchor="w", font=FONT_BUTTON).pack(side="left", anchor="nw", pady=2)

        slots_grid = tk.Frame(available_frame, bg=BG_COLOUR2)
        slots_grid.pack(side="left", fill="both", expand=True, padx=(4, 0))

        for i, slot in enumerate(r.availability,0):
            colour = "green" if slot in overlaps else ENTRY_BG
            tk.Label(slots_grid, text=f" {slot['day']} {slot['period']} ", fg="white" if slot in overlaps else FG_COLOUR2, bg=colour, font=FONT_SMALL).grid(row= i // 4, column=(i % 4) +1, padx=4)

class AdminDashboard(tk.Frame):
    def __init__(self, parent, ui):
        super().__init__(parent, bg=BG_COLOUR)
        self.pack(fill="both", expand=True, pady=(40,40), padx=20)
        self.ui = ui

        admin = self.ui.user
        # HEADER
        InternalHeader(self, ui, f"Admin Dashboard")

        row1 = tk.Frame(self, bg=BG_COLOUR3)
        row1.pack(fill="x")

        styled_label(row1, f"Welcome {admin.username},", bg=BG_COLOUR3, font=FONT_BODY).pack(side="left", pady=10,
                                                                                           padx=10)
if __name__=="__main__":
    StudyBuddyUI()