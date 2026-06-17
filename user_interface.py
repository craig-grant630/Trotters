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
        self.form_progress = None

        self.root = tk.Tk()
        self.root.title("TiT Study Buddy")
        self.root.geometry("900x700")
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

    def show_programme_form(self, programme=None, progress_data=None):
        self.clear()
        AddEditProgramme(self.container, self, programme, progress_data)

    def show_module_form(self, module, parent_form):
        self.form_progress = {
            "name": parent_form.name_entry.get(),
            "code": parent_form.code_entry.get(),
            "modules": parent_form.module_codes,
            "campuses": parent_form.campus_codes
        }
        self.clear()
        EditModule(self.container, self, module, parent_form)

    def show_campus_form(self, campus=None):
        self.clear()
        AddEditCampus(self.container, self, campus)

    def show_admin_students(self):
        self.clear()
        AdminStudents(self.container, self)

    def show_edit_student(self):
        self.clear()
        EditStudent(self.container, self)

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

        tk.Button(self, text="TiT", bg=BG_COLOUR3, fg=ACCENT, font=FONT_HEADER, relief="flat", activebackground=BG_COLOUR3, cursor="fleur").pack(side="left", padx=10)
        styled_label(self, text=f" Study Buddy   |   {title}", bg= BG_COLOUR3,font=FONT_BUTTON, fg=FG_COLOUR).pack(side="left", padx=10, pady=(10,2))

        tk.Button(self, text="Logout", bg=BG_COLOUR2, fg="white", font=("Helvetica", 11, "bold"), relief="flat",
                  borderwidth=1, width=8, command=lambda: ui.show_login(mode="student")).pack(side="right", padx=10)
        row = tk.Frame(parent, bg=BG_COLOUR3)
        row.pack(fill="x")
        separator(row, ACCENT).pack(fill="x", pady=2, padx=100)
#==============================================================================================
# Main frames of application - students
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
            tk.Button(outer, text="Not a Student? Admin Login Click Here", bg=BG_COLOUR2, font=FONT_SMALL, fg=FG_COLOUR2,relief="flat", command=lambda: ui.show_login(mode="admin")).pack(pady=5)
        else:
            tk.Button(outer, text="Back to student login click here", bg=BG_COLOUR2, font=FONT_SMALL, fg=FG_COLOUR2,
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

        styled_label(left_side_frame, "Request Actions", font=FONT_BUTTON, fg=ACCENT).pack(anchor="w")
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
        matches_button.pack(pady=3)

        styled_label(left_side_frame, "Profile Actions", font=FONT_BUTTON, fg=ACCENT).pack(anchor="w", pady=(15,0))
        separator(left_side_frame, bg=ACCENT).pack(fill="x", pady=8, padx=10)

        edit_profile_button = tk.Button(left_side_frame, bg=BG_COLOUR3, fg=FG_COLOUR, relief="flat", text="Edit Profile",
                                font=("Helvetica", 10, "bold"), width=15, command=self.edit_profile)
        edit_profile_button.pack(pady=3)
        delete_profile_button = tk.Button(left_side_frame, bg="red", fg=FG_COLOUR, relief="flat", text="Delete Profile",
                                  font=("Helvetica", 10, "bold"), width=15, command=self.delete_profile)
        delete_profile_button.pack(pady=3)
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

    def delete_profile(self):
        student= self.ui.user
        if not messagebox.askyesno("Delete Profile",
                                   f"Are you sure you want to delete profile: {student.student_id}?\nThis will permanently remove the profile and requests from the system."):
            return
        self.ui.app.delete_profile(student.student_id)
        self.ui.show_dashboard()

    def edit_profile(self):
        self.ui.show_edit_student()

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

class EditStudent(tk.Frame):
    def __init__(self, parent, ui):
        super().__init__(parent, bg=BG_COLOUR)
        self.pack(fill="both", expand=True)
        self.ui = ui
        self.register_msg = tk.StringVar()

        student = self.ui.user

        outer = tk.Frame(self, bg=BG_COLOUR2, padx=40, pady=20)
        outer.place(relx=0.5, rely=0.5, anchor="center")

        # Note: Set parent to 'self' or 'outer' depending on your header layout preference
        InternalHeader(outer, ui, "Edit Profile")

        fields = [
            ("Student ID (10 digits)", False),
            ("Full Name", False),
            ("Password", True),
        ]
        self.entries = {}
        for label, show in fields:
            row2 = tk.Frame(outer, bg=BG_COLOUR2)
            row2.pack(fill="x")
            row2.grid_columnconfigure(0, minsize=180, uniform="reg_col")
            styled_label(row2, label, bg=BG_COLOUR2, font=FONT_BODY,
                         fg=FG_COLOUR2).grid(row=0, column=0, sticky="e", padx=8, pady=5)

            entry = tk.Entry(row2, bg=BG_COLOUR3, fg="white", relief="flat", font=FONT_BODY, width=27,
                             show="*" if show else None, highlightcolor=ACCENT, highlightthickness=1)

            self.entries[label] = entry
            entry.grid(row=0, column=1, sticky="w", padx=8)

        separator(outer).pack(fill="x", pady=10)

        self.row2 = tk.Frame(outer, bg=BG_COLOUR2)
        self.row2.pack(fill="x")
        self.row2.grid_columnconfigure(0, minsize=180, uniform="reg_col")

        # Row 0: Programme
        prog_options = []
        for p in self.ui.app.programmes.values():
            prog_options.append(f"{p.programme_code} - {p.name}")
        styled_label(self.row2, "Programme:", bg=BG_COLOUR2, font=FONT_BODY, fg=FG_COLOUR2).grid(row=0, column=0,
                                                                                                 sticky="e", padx=6)
        self.programme_drop = styled_combobox(self.row2, prog_options, 26)
        self.programme_drop.grid(row=0, column=1, sticky="w", padx=6, pady=5)

        camp_options = []
        for c in self.ui.app.campuses.values():
            camp_options.append(f"{c.name} - {c.campus_code}")
        styled_label(self.row2, "Campus:", bg=BG_COLOUR2, font=FONT_BODY, fg=FG_COLOUR2).grid(row=1, column=0,
                                                                                              sticky="e", padx=6)
        self.campus_drop = styled_combobox(self.row2, camp_options, 26)
        self.campus_drop.grid(row=1, column=1, sticky="w", padx=6, pady=5)

        styled_label(self.row2, "Year of Study:", bg=BG_COLOUR2, font=FONT_BODY, fg=FG_COLOUR2).grid(row=2, column=0,
                                                                                                     sticky="e", padx=6)
        self.yos = styled_combobox(self.row2, ["  1", "  2", "  3"], 3)
        self.yos.grid(row=2, column=1, sticky="w", padx=6, pady=5)

        register_frame_btn = tk.Button(self.row2, text="Save Changes", bg=BG_COLOUR3, fg="white", font=FONT_BUTTON,
                                       relief="flat",
                                       borderwidth=1, width=15, command=self.save_student_changes)
        register_frame_btn.grid(row=3, column=1, sticky="e", pady=(40, 5), padx=10)

        self.msg_label = tk.Label(self.row2, bg=BG_COLOUR2, fg="red", textvariable=self.register_msg, font=FONT_MSG,
                                  wraplength=180)
        self.msg_label.grid(row=3, column=0, sticky="sw", pady=5)

        if student is not None:
            # Fill in all the students details
            self.entries["Student ID (10 digits)"].insert(0, str(student.student_id))
            self.entries["Full Name"].insert(0, str(student.name))
            self.entries["Password"].insert(0, str(student.password))

            self.entries["Student ID (10 digits)"].config(state="disabled")
            self.programme_drop.config(state="disabled")
            self.entries["Student ID (10 digits)"].bind("<Key>", lambda e: "break")

            for item in prog_options:
                if item.startswith(f"{student.programme_code} -"):
                    self.programme_drop.set(item)
                    break

            for item in camp_options:
                if item.endswith(f"- {student.campus_code}"):
                    self.campus_drop.set(item)
                    break

            clean_yos = str(student.year_of_study).strip()
            for opt in ["  1", "  2", "  3"]:
                if opt.strip() == clean_yos:
                    self.yos.set(opt)
                    break

    def save_student_changes(self):
        student = self.ui.user
        name = self.entries["Full Name"].get().strip()
        password = self.entries["Password"].get()
        prog_sel = self.programme_drop.get()
        camp_sel = self.campus_drop.get()

        try:
            prog_code = prog_sel.split("-")[0].strip()
            camp_code = camp_sel.split("-")[1].strip()
        except IndexError:
            prog_code = None
            camp_code = None

        year = self.yos.get().strip()

        valid, msg = self.ui.app.check_update_credentials(
            student.student_id, name, password, camp_code, prog_code, year
        )

        if not valid:
            self.register_msg.set(msg)
            self.msg_label.config(fg="red")
            return

        success = self.ui.app.update_student(
            student.student_id, name, password, camp_code, prog_code, year)

        if success:
            self.register_msg.set("Profile changes saved successfully!")
            self.msg_label.config(fg="green")
            self.ui.user = self.ui.app.students[student.student_id]
            self.ui.show_dashboard()
        else:
            self.register_msg.set("Error: Profile could not be found.")
            self.msg_label.config(fg="red")

# Main frames of application - Admin
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
        programmes_btn = tk.Button(row1, text="Programmes & Campuses", bg=ACCENT, fg="white", font=FONT_BUTTON, relief="flat",
                                   borderwidth=1, command=self.ui.show_admin_dashboard)
        programmes_btn.pack(side="left", padx=10, pady=5)

        student_btn = tk.Button(row1, text="Students", bg=BG_COLOUR, fg="white", font=FONT_BUTTON, relief="flat",
                               borderwidth=1, command=self.ui.show_admin_students)
        student_btn.pack(side="left", padx=10, pady=5)

        row2 = tk.Frame(self, bg=BG_COLOUR)
        row2.pack(fill="both", expand=True)

        row2.grid_columnconfigure(0, weight=1)
        row2.grid_columnconfigure(1, weight=0)
        row2.rowconfigure(0, weight=1)
        row2.rowconfigure(1, weight=1)
    #===============================================================================================================
        left_side_frame = card(row2, bg=BG_COLOUR2)
        left_side_frame.grid(row=0, column=0, sticky="new")

        styled_label(left_side_frame, "All Programmes", font=FONT_BUTTON, fg=ACCENT).pack(anchor="w")
        separator(left_side_frame, bg=ACCENT).pack(fill="x", pady=8, padx=10)

        self.prog_treeview = styled_treeview(left_side_frame, ["Code", "Programme Name", "Campus Codes", "# Modules"],
                                        ["Code", "Programme Name", "Campus Codes", "# Modules"], [40, 120, 40, 40])
        self.prog_treeview.pack(fill="both", expand=True)
        self.refresh_programmes_treeview()
#=================================================================================================
        right_side_frame = card(row2, bg=BG_COLOUR2)
        right_side_frame.grid(row=0, column=1, sticky="nsew")

        styled_label(right_side_frame, "Programme Actions", font=FONT_BUTTON, fg=ACCENT).pack(anchor="w")
        separator(right_side_frame, bg=ACCENT).pack(fill="x", pady=8, padx=5)
        add_button = tk.Button(right_side_frame, bg=BG_COLOUR3, fg=FG_COLOUR, relief="flat", text="Add Programme",
                               font=("Helvetica", 10, "bold"), width=15, command=self.add_programme)
        add_button.pack(pady=3)
        edit_button = tk.Button(right_side_frame, bg=BG_COLOUR3, fg=FG_COLOUR, relief="flat", text="Edit Programme",
                                font=("Helvetica", 10, "bold"), width=15, command=self.edit_programme)
        edit_button.pack(pady=3)
        delete_button = tk.Button(right_side_frame, bg="red", fg=FG_COLOUR, relief="flat", text="Delete Programme",
                                  font=("Helvetica", 10, "bold"), width=15, command=self.delete_programme)
        delete_button.pack(pady=3, side="bottom")
    #=========================================================================================================
        leftb_side_frame = card(row2, bg=BG_COLOUR2)
        leftb_side_frame.grid(row=1, column=0, sticky="new")

        styled_label(leftb_side_frame, "All Campuses", font=FONT_BUTTON, fg=ACCENT).pack(anchor="w")
        separator(leftb_side_frame, bg=ACCENT).pack(fill="x", pady=8, padx=10)

        self.camp_treeview = styled_treeview(leftb_side_frame, ["Code", "Campus Code"],
                                        ["Code", "Campus Name"], [120, 40])
        self.camp_treeview.pack(fill="both", expand=True)
        self.refresh_campus_treeview()
#===================================================================================================================
        rightb_side_frame = card(row2, bg=BG_COLOUR2)
        rightb_side_frame.grid(row=1, column=1, sticky="nsew")

        styled_label(rightb_side_frame, "Campus Actions", font=FONT_BUTTON, fg=ACCENT).pack(anchor="w")
        separator(rightb_side_frame, bg=ACCENT).pack(fill="x", pady=8, padx=5)
        camp_add_button = tk.Button(rightb_side_frame, bg=BG_COLOUR3, fg=FG_COLOUR, relief="flat", text="Add Campus",
                               font=("Helvetica", 10, "bold"), width=15, command=self.add_campus)
        camp_add_button.pack(pady=3)
        camp_edit_button = tk.Button(rightb_side_frame, bg=BG_COLOUR3, fg=FG_COLOUR, relief="flat", text="Edit Campus",
                                font=("Helvetica", 10, "bold"), width=15, command=self.edit_campus)
        camp_edit_button.pack(pady=3)
        camp_delete_button = tk.Button(rightb_side_frame, bg="red", fg=FG_COLOUR, relief="flat", text="Delete Campus",
                                  font=("Helvetica", 10, "bold"), width=15, command=self.delete_campus)
        camp_delete_button.pack(pady=3, side="bottom")
#====================================================================================================================
    def refresh_programmes_treeview(self):
        for item in self.prog_treeview.get_children():
            self.prog_treeview.delete(item)

        all_programmes = list(self.ui.app.programmes.values())

        if not all_programmes:
            self.prog_treeview.insert("", "end", iid="none", values=("No Programmes Here", "", "", ""))
            return

        for item in all_programmes:

            self.prog_treeview.insert("", "end", iid=str(item.programme_code),
                                 values=(f"{item.programme_code}", str(item.name), len(item.campus_codes), len(item.modules)))

    def refresh_campus_treeview(self):
        for item in self.camp_treeview.get_children():
            self.camp_treeview.delete(item)

        all_campus = list(self.ui.app.campuses.values())

        if not all_campus:
            self.camp_treeview.insert("", "end", iid="none", values=("No Campuses Here", ""))
            return

        for item in all_campus:

            self.camp_treeview.insert("", "end", iid=str(item.campus_code),
                                 values=(f"{item.campus_code}", str(item.name)))

    def selection_prog_treeview(self):
        selection = self.prog_treeview.selection()
        if not selection or selection[0] == "none":
            return None
        programme_code = selection[0]
        return self.ui.app.get_programme(programme_code)

    def selection_campus_treeview(self):
        selection = self.camp_treeview.selection()
        if not selection or selection[0] == "none":
            return None
        campus_code = selection[0]
        return self.ui.app.get_campus(campus_code)

    def add_campus(self):
        self.ui.show_campus_form()

    def edit_campus(self):
        c_obj = self.selection_campus_treeview()
        if not c_obj:
            messagebox.showwarning("Warning", "No Campus selected")
            return
        self.ui.show_campus_form(c_obj)

    def delete_campus(self):
        campus = self.selection_campus_treeview()

        if not campus:
            messagebox.showwarning("Warning", "No Campus selected")
            return

        if not messagebox.askyesno("Delete Campus",
                                   f"Are you sure you want to delete Campus: [{campus.campus_code}, {campus.name}]?\nThis will permanently remove all associated students and requests."):
            return

        success, num_students, num_requests = self.ui.app.delete_campus(campus.campus_code)

        if success:
            self.refresh_campus_treeview()
            messagebox.showinfo("Success",
                                f"Campus deleted successfully!\nRemoved {num_students} students and {num_requests} requests.")
        else:
            messagebox.showwarning("Warning", "Could not delete Campus")

    def add_programme(self):
        self.ui.show_programme_form()

    def edit_programme(self):
        p_obj = self.selection_prog_treeview()
        if not p_obj:
            messagebox.showwarning("Warning", "No programme selected")
            return
        self.ui.show_programme_form(p_obj)

    def delete_programme(self):
        programme = self.selection_prog_treeview()

        if not programme:
            messagebox.showwarning("Warning", "No programme selected")
            return

        if not messagebox.askyesno("Delete Programme",
                                   f"Are you sure you want to delete programme: [{programme.programme_code}, {programme.name}]?\nThis will permanently remove all associated students and requests."):
            return

        success, num_students, num_requests = self.ui.app.delete_programme(programme.programme_code)

        if success:
            self.refresh_programmes_treeview()
            messagebox.showinfo("Success",
                                f"Programme deleted successfully!\nRemoved {num_students} students and {num_requests} requests.")
        else:
            messagebox.showwarning("Warning", "Could not delete programme")

class AddEditProgramme(tk.Frame):
    def __init__(self, parent, ui, programme=None, progress_data=None):
        super().__init__(parent, bg=BG_COLOUR)
        self.pack(fill="both", expand=True, pady=(20, 10), padx=20)
        self.ui = ui

        # Determine the mode
        self.programme = programme
        if self.programme is not None:
            mode = "Edit Programme"
        else:
            mode = "Add Programme"

        # HEADER
        InternalHeader(self, ui, f"{mode}")

        row1 = tk.Frame(self, bg=BG_COLOUR)
        row1.pack(fill="both", expand=True)
        # ==============================================================================================
        # LEFT SIDE FORM
        left_side_frame = card(row1, bg=BG_COLOUR2)
        left_side_frame.pack(side="left", fill="both", expand=True)

        buttons_frame = tk.Frame(left_side_frame, bg=BG_COLOUR2)
        buttons_frame.pack(anchor="w", pady=5, padx=8)

        if programme:
            save_button = tk.Button(buttons_frame, bg=ACCENT, fg=FG_COLOUR, relief="flat", text="Save", width=7,command=self.save_programme)
            save_button.grid(row=0, column=0, padx=8, sticky="w")
        else:
            add_button = tk.Button(buttons_frame, bg=ACCENT, fg=FG_COLOUR, relief="flat", text="Add Programme",
                                   width=12, command=self.save_programme)
            add_button.grid(row=0, column=1, padx=8, sticky="w")

        cancel_button = tk.Button(buttons_frame, bg=ACCENT, fg=FG_COLOUR, relief="flat", text="Cancel", width=7,
                                  command=self.ui.show_admin_dashboard)
        cancel_button.grid(row=0, column=2, padx=8, sticky="w")

        form = tk.Frame(left_side_frame, bg=BG_COLOUR2)
        form.pack(anchor="w")

        styled_label(form, "Programme Name", bg=BG_COLOUR2, anchor="w").grid(row=0, column=0, padx=(8, 2), pady=6,
                                                                             sticky="w")
        self.name_entry = tk.Entry(form, bg=BG_COLOUR3, fg="white", relief="flat", font=FONT_BODY, width=27,
                                   highlightcolor=ACCENT, highlightthickness=1)
        self.name_entry.grid(row=0, column=1, padx=8, sticky="w")

        styled_label(form, "Programme Code", bg=BG_COLOUR2, anchor="w").grid(row=1, column=0, padx=(8, 0), pady=6,
                                                                             sticky="w")
        self.code_entry = tk.Entry(form, bg=BG_COLOUR3, fg="white", relief="flat", font=FONT_BODY, width=27,
                                   highlightcolor=ACCENT, highlightthickness=1)
        self.code_entry.grid(row=1, column=1, padx=8, sticky="w", pady=(0, 4))
        # ===================================================================================================================================================
        # CAMPUS FRAME - contains dropdown for campus codes, add, delete for campus treeview
        campus_frame = card(left_side_frame, bg=BG_COLOUR2)
        campus_frame.pack(fill="both", expand=True)

        styled_label(campus_frame, "Campuses", FONT_BUTTON, fg=ACCENT).grid(row=0, column=0, sticky="w", pady=(0, 2))

        separator(campus_frame, bg=ACCENT).grid(row=1, column=0, columnspan=4, sticky="ew", pady=(2, 6))

        styled_label(campus_frame, "Campus Code", FONT_BODY, fg=FG_COLOUR2).grid(row=2, column=0, sticky="w", pady=2)
        all_campuses = list(self.ui.app.campuses.keys())

        self.campus_code = styled_combobox(campus_frame,all_campuses,10)
        self.campus_code.grid(row=2, column=1, padx=(10, 0), sticky="w", pady=2)
        tk.Button(campus_frame, text="Add", bg="green", fg=FG_COLOUR, width=6, relief="flat",
                  font=("Helvetica", 10, "bold"), command=self.add_campus_treeview).grid(row=2, column=2, padx=(2, 2), sticky="w", pady=2)
        tk.Button(campus_frame, text="Remove Selected", bg="red", fg=FG_COLOUR, relief="flat",
                  font=("Helvetica", 10, "bold"),command=self.remove_campus_treeview).grid(row=2, column=3, padx=(0, 0), sticky="w", pady=2)

        self.campus_treeview = styled_treeview(campus_frame, ["Campus Code"],
                                               ["Campus Code"], [10])
        self.campus_treeview.grid(row=4, column=0, columnspan=4, sticky="nsew", pady=8)

        campus_frame.grid_rowconfigure(4, weight=1)
        campus_frame.grid_columnconfigure(1, weight=1)

        # ==========================================================================================================================
        # RIGHT SIDE - Module add, edit, delete for programme
        right_side_frame = card(row1, bg=BG_COLOUR2)
        right_side_frame.pack(fill="both", expand=True, side="right")

        styled_label(right_side_frame, "Modules", font=FONT_BUTTON, fg=ACCENT).pack(anchor="w")
        separator(right_side_frame, bg=ACCENT).pack(fill="x", pady=8, padx=10)

        styled_label(right_side_frame, "Add the modules that are required for this programme", font=FONT_SMALL,
                     fg=FG_COLOUR2, bg=BG_COLOUR2).pack(anchor="w", pady=(0, 8))

        module_row = tk.Frame(right_side_frame, bg=BG_COLOUR2)
        module_row.pack(anchor="w", pady=4)

        styled_label(module_row, "Module Code", FONT_BODY, fg=FG_COLOUR2).pack(anchor="w")
        self.module_code = tk.Entry(module_row, bg=BG_COLOUR3, fg="white", relief="flat", font=FONT_BODY, width=27,
                                    highlightcolor=ACCENT, highlightthickness=1)
        self.module_code.pack(pady=(0, 8), anchor="w")

        styled_label(module_row, "Module Name", FONT_BODY, fg=FG_COLOUR2).pack(anchor="w")
        self.module_name = tk.Entry(module_row, bg=BG_COLOUR3, fg="white", relief="flat", font=FONT_BODY, width=27,
                                    highlightcolor=ACCENT, highlightthickness=1)
        self.module_name.pack(pady=(0, 8), anchor="w")

        styled_label(module_row, "Year", FONT_BODY, fg=FG_COLOUR2).pack(anchor="w")
        self.year = styled_combobox(module_row, ['1', '2', '3'], 5)
        self.year.pack(pady=(0, 8), side="left", padx=3)

        tk.Button(module_row, text="Add", bg="green", fg=FG_COLOUR, width=6, relief="flat",
                  font=("Helvetica", 10, "bold"), command=self.add_module_treeview).pack(padx=3, side="left")
        tk.Button(module_row, text="Remove Selected", bg="red", fg=FG_COLOUR, relief="flat",
                  font=("Helvetica", 10, "bold"), command=self.remove_module_treeview).pack(padx=3, side="left")
        tk.Button(module_row, text="Edit Selected", bg="orange", fg=FG_COLOUR, relief="flat",
                  font=("Helvetica", 10, "bold"), command=self.edit_module).pack(padx=3, side="left")

        self.module_treeview = styled_treeview(right_side_frame, ["Module Code", "Name", "Year"],
                                               ["Module Code", "Name", "Year"], [10, 120, 10])
        self.module_treeview.pack(fill="both", pady=8)

        # =======================================================================================================================
        # SOURCE - DATA HANDLER
        if progress_data:
            self.name_entry.insert(0, progress_data["name"])
            self.code_entry.insert(0, progress_data["code"])
            self.module_codes = progress_data["modules"]
            self.campus_codes = progress_data["campuses"]
        elif self.programme:
            self.name_entry.insert(0, getattr(self.programme, 'name', ''))
            self.code_entry.insert(0, getattr(self.programme, 'programme_code', ''))

            self.campus_codes = list(self.programme.campus_codes)
            self.module_codes = [
                {"module_code": m.module_code, "name": m.name, "year": m.year}
                for m in getattr(self.programme, 'modules', [])]
        else:
            self.module_codes = []
            self.campus_codes = []

        # Refresh both tree views
        self.refresh_campus_form()
        self.refresh_module_form()
#=======================================================================================================================
    # MODULE TREEVIEW FUNCTIONALITY
    def refresh_module_form(self):
        for item in self.module_treeview.get_children():
            self.module_treeview.delete(item)

        if not self.module_codes:
            self.module_treeview.insert("", "end", iid="none", values=("No Modules Yet", "", ""))
            return

        for index, item in enumerate(self.module_codes):
            self.module_treeview.insert("","end",iid=str(index),values=(item['module_code'], item['name'], item['year']))

    def selection_module_treeview(self):
        selection = self.module_treeview.selection()
        if not selection or selection[0] == "none":
            return None
        idx = int(selection[0])
        return self.module_codes[idx]

    def remove_module_treeview(self):
        selection = self.module_treeview.selection()
        if not selection or selection[0] == "none":
            return
        idx = int(selection[0])
        del self.module_codes[idx]
        self.refresh_module_form()

    def edit_module(self):
        module_dict = self.selection_module_treeview()
        if not module_dict:
            messagebox.showwarning("Warning", "No Module selected")
            return
        self.ui.show_module_form(module_dict, self)

    def add_module_treeview(self):
        code = self.module_code.get().strip().upper()
        name = self.module_name.get().strip()
        year = self.year.get()

        if not code or not name or not year:
            messagebox.showerror("Error", "Please select a Module Code, Name and Year")
            return
        slot = {"module_code": code, "name": name, "year": year}
        if code in self.ui.app.all_module_codes or any(item['module_code'] == code for item in self.module_codes):
            messagebox.showerror("Error", f"Module code '{code}' already exists.")
            return
        self.module_codes.append(slot)
        self.refresh_module_form()
#=======================================================================================================================
    def refresh_campus_form(self):
        for item in self.campus_treeview.get_children():
            self.campus_treeview.delete(item)
        if not self.campus_codes:
            self.campus_treeview.insert("", "end", iid="none", values=("No Campuses Yet", "", ""))
            return

        for index, item in enumerate(self.campus_codes):
            self.campus_treeview.insert("", "end", iid=str(index),
                                 values=item)

    def remove_campus_treeview(self):
        selection = self.campus_treeview.selection()
        if not selection or selection[0] == "none":
            return
        idx = int(selection[0])
        del self.campus_codes[idx]
        self.refresh_campus_form()

    def add_campus_treeview(self):
        code = self.campus_code.get().strip().upper()
        if not code:
            messagebox.showerror("Error", "Please select a Campus Code")
            return
        if code in self.campus_codes:
            messagebox.showerror("Error", f"Campus code '{code}' already exists.")
            return
        self.campus_codes.append(code)
        self.refresh_campus_form()

#=======================================================================================================================
    def save_programme(self):
        p_name = self.name_entry.get().strip()
        p_code = self.code_entry.get().strip().upper()

        if not p_name:
            messagebox.showerror("Error", "Please enter a Programme Name.")
            return
        if not p_code or len(p_code) != 5:
            messagebox.showerror("Error", "Please enter a Programme Code.")
            return
        if not self.campus_codes:
            messagebox.showerror("Error", "A programme must contain at least one campus.")
            return
        if not self.module_codes:
            messagebox.showerror("Error", "A programme must contain at least one module.")
            return
        # Determine editing or adding
        is_edit_mode = self.programme is not None
        old_code = self.programme.programme_code if is_edit_mode else None

        valid, error_msg = self.ui.app.programme_add_edit(
            is_edit=is_edit_mode,
            old_code=old_code,
            new_code=p_code,
            name=p_name,
            modules_list=self.module_codes,
            campuses_list=self.campus_codes
        )

        if valid:
            messagebox.showinfo("Success", f"Programme '{p_code}' successfully saved.")
            self.ui.show_admin_dashboard()
        else:
            messagebox.showerror("Error", error_msg)

class EditModule(tk.Frame):
    def __init__(self, parent, ui, module_dict, parent_form):
        super().__init__(parent, bg=BG_COLOUR)
        self.pack(fill="both", expand=True, pady=(20, 10), padx=20)
        self.ui = ui
        self.module_dict = module_dict
        self.parent_form = parent_form

        frame = tk.Frame(self, bg=BG_COLOUR2, padx=40, pady=36)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        InternalHeader(frame, ui, "Edit Module")

        module_row = tk.Frame(frame, bg=BG_COLOUR2)
        module_row.pack(anchor="w", pady=10, expand=True, fill="both")

        styled_label(module_row, "Module Code", FONT_BODY, fg=FG_COLOUR2).grid(row=0, column=0, padx=10, pady=5)
        self.module_code = tk.Entry(module_row, bg=BG_COLOUR3, fg="black", relief="flat", font=FONT_BODY, width=27,
                                    highlightcolor=ACCENT, highlightthickness=1)
        self.module_code.grid(row=0, column=1)

        styled_label(module_row, "Module Name", FONT_BODY, fg=FG_COLOUR2).grid(row=1, column=0, padx=10, pady=5)
        self.module_name = tk.Entry(module_row, bg=BG_COLOUR3, fg="white", relief="flat", font=FONT_BODY, width=27,
                                    highlightcolor=ACCENT, highlightthickness=1)
        self.module_name.grid(row=1, column=1)

        styled_label(module_row, "Year", FONT_BODY, fg=FG_COLOUR2).grid(row=2, column=0, padx=10, pady=5)
        self.year = styled_combobox(module_row, ['1', '2', '3'], 5)
        self.year.grid(row=2, column=1, sticky="w")

        tk.Button(module_row, text="Save Changes", bg=ACCENT, fg=FG_COLOUR, relief="flat",
                  font=("Helvetica", 10, "bold"), command=self.save_module).grid(row=3, column=0, padx=10, pady=5)

        # Populate fields from the local dictionary reference
        self.module_code.insert(0, self.module_dict.get('module_code', ''))
        self.module_name.insert(0, self.module_dict.get('name', ''))
        self.year.set(str(self.module_dict.get('year', '')))

        self.module_code.config(state="readonly")

    def save_module(self):
        new_name = self.module_name.get().strip()
        new_year = self.year.get()

        if not new_name or not new_year:
            messagebox.showerror("Error", "All module fields are required.")
            return

        self.module_dict['name'] = new_name
        self.module_dict['year'] = new_year

        orig_programme = getattr(self.parent_form, 'programme', None)
        self.ui.show_programme_form(orig_programme, progress_data=self.ui.form_progress)

class AddEditCampus(tk.Frame):
    def __init__(self, parent, ui, campus=None):
        # Initialise the frame with background colour
        super().__init__(parent, bg=BG_COLOUR)
        self.pack(fill="both", expand=True, pady=(40, 40), padx=20)
        self.ui = ui

        # Determine mode and button text based on campus presence
        if campus is not None:
            self.campus = campus
            self.mode = "Edit Campus"
            button_text = "Save Changes"
        else:
            self.campus = None
            self.mode = "Add Campus"
            button_text = "Add Campus"

        # Centred container frame
        frame = tk.Frame(self, bg=BG_COLOUR2, padx=40, pady=36)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Header title
        InternalHeader(frame, ui, self.mode)

        campus_row = tk.Frame(frame, bg=BG_COLOUR2)
        campus_row.pack(anchor="w", pady=10, expand=True, fill="both")

        styled_label(campus_row, "Campus Code", FONT_BODY, fg=FG_COLOUR2).grid(row=0, column=0, padx=10, pady=5,
                                                                               sticky="w")
        self.campus_code = tk.Entry(campus_row, bg=BG_COLOUR3, fg=FG_COLOUR2, relief="flat", font=FONT_BODY, width=27,
                                    highlightcolor=ACCENT, highlightthickness=1, disabledforeground="black")
        self.campus_code.grid(row=0, column=1, pady=5)

        styled_label(campus_row, "Campus Name", FONT_BODY, fg=FG_COLOUR2).grid(row=1, column=0, padx=10, pady=5,
                                                                               sticky="w")
        self.campus_name = tk.Entry(campus_row, bg=BG_COLOUR3, fg=FG_COLOUR2, relief="flat", font=FONT_BODY, width=27,
                                    highlightcolor=ACCENT, highlightthickness=1)
        self.campus_name.grid(row=1, column=1, pady=5)

        if campus is not None:
            self.campus_code.insert(0, str(campus.campus_code))
            self.campus_name.insert(0, str(campus.name))
            self.campus_code.config(state="readonly")

        self.submit_btn = tk.Button(campus_row, text=button_text, bg=ACCENT, fg=FG_COLOUR, relief="flat",
                                    font=("Helvetica", 10, "bold"), command=self.save_campus)
        self.submit_btn.grid(row=3, column=0, columnspan=2, pady=15)

    def save_campus(self):
        code = self.campus_code.get().strip()
        name = self.campus_name.get().strip()

        if not code or not name:
            messagebox.showerror("Error", "All campus fields are required.")
            return

        if self.mode == "Add Campus":
            valid, msg = self.ui.app.add_campus(str(code), name)

            if valid:
                self.ui.show_admin_dashboard()
            else:
                messagebox.showerror("Error", msg)
        else:
            valid, msg = self.ui.app.edit_campus(str(code), name)

            if valid:
                self.ui.show_admin_dashboard()
            else:
                messagebox.showerror("Error", msg)

class AdminStudents(tk.Frame):
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
        programmes_btn = tk.Button(row1, text="Programmes & Campuses", bg=BG_COLOUR, fg="white", font=FONT_BUTTON, relief="flat",
                                   borderwidth=1, command=self.ui.show_admin_dashboard)
        programmes_btn.pack(side="left", padx=10, pady=5)

        campus_btn = tk.Button(row1, text="Students", bg=ACCENT, fg="white", font=FONT_BUTTON, relief="flat",
                               borderwidth=1, command=self.ui.show_admin_students)
        campus_btn.pack(side="left", padx=10, pady=5)

        row2 = tk.Frame(self, bg=BG_COLOUR)
        row2.pack(fill="both", expand=True)

        styled_label(row2, "All Students", font=FONT_BUTTON, fg=ACCENT).pack(anchor="w")
        separator(row2, bg=ACCENT).pack(fill="x", pady=8, padx=10)

        self.treeview = styled_treeview(row2,['Student ID', 'Name', 'Programme Code', 'Campus Code', 'Year'],['Student ID', 'Name', 'Programme Code', 'Campus Code', 'Year'], [20,120,20,20,10])
        self.treeview.pack(fill="both", expand=True)

        self.refresh_treeview()

    def refresh_treeview(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        all_students = list(self.ui.app.students.values())

        if not all_students:
            self.treeview.insert("", "end", iid="none", values=("No Students Here", "", "", "", ""))
            return

        for item in all_students:

            self.treeview.insert("", "end", iid=str(item.student_id),
                                 values=(f"{item.student_id}", str(item.name), item.programme_code, item.campus_code, item.year_of_study))

if __name__=="__main__":
    StudyBuddyUI()