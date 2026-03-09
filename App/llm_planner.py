# # llm_planner.py
# # Fully Deterministic Planner (No LLM)

# from datetime import datetime, timedelta


# class AgentState:
#     def __init__(self):
#         self.interacted_selectors: set = set()
#         self.phase: str = "init"          # init → navigating → form_open → form_filling → submitted → done
#         self.project_submitted: bool = False

#     def reset(self):
#         self.__init__()


# # One shared state per session (reset between runs from agent.py if needed)
# state = AgentState()

# # =========================================================
# # 🚀 ENTRY FUNCTION
# # =========================================================

# async def decide_action(goal, dom, url, email=None, password=None):
#     return await decide_action_with_failed_indices(
#         goal, dom, url, email, password
#     )


# # =========================================================
# # 🧠 MAIN DECISION FUNCTION
# # =========================================================

# async def decide_action_with_failed_indices(
#     goal,
#     dom,
#     url,
#     email=None,
#     password=None
# ):

#     # =========================================================
#     # 🔐 LOGIN HANDLER
#     # =========================================================
#     try:
#         email_input = None
#         password_input = None
#         next_button = None
#         sign_in_button = None
#         yes_button = None

#         for el in dom:
#             print(f"this is el: {el}")
#             label = (el.get("label") or "").lower().strip()
#             tag = (el.get("tag") or "").lower()
#             el_type = el.get("type")

#             if el_type == "email" or (tag == "input" and "email" in label):
#                 email_input = el

#             if el_type == "password":
#                 password_input = el

#             if tag in ["button", "input"]:
#                 if "next" in label:
#                     next_button = el
#                 if any(x in label for x in ["sign in", "login", "submit"]):
#                     sign_in_button = el
#                 if "yes" in label:
#                     yes_button = el

#         if yes_button:
#             return {"action": "click", "selector": yes_button["selector"]}

#         if email_input and not password_input:
#             if not email_input.get("value") and email:
#                 return {"action": "type", "selector": email_input["selector"], "text": email}
#             if email_input.get("value") and next_button:
#                 return {"action": "click", "selector": next_button["selector"]}

#         if password_input:
#             if not password_input.get("value") and password:
#                 return {"action": "type", "selector": password_input["selector"], "text": password}
#             if password_input.get("value") and sign_in_button:
#                 return {"action": "click", "selector": sign_in_button["selector"]}

#     except Exception as e:
#         print("Login handler error:", e)

#     # =========================================================
#     # 📁 PROJECT CREATION HANDLER
#     # =========================================================

#     is_create_project = any(
#         keyword in goal.lower()
#         for keyword in ["create project", "add project", "new project"]
#     )

#     if not is_create_project:
#         return {"action": "wait", "seconds": 2}

#     try:
#         # -----------------------------------------------------
#         # 🔍 Detect Elements
#         # -----------------------------------------------------

#         resource_planner_btn = None
#         projects_tab = None
#         add_project_btn = None

#         project_name_input = None
#         start_date_input = None
#         end_date_input = None
#         project_category_dropdown = None
#         client_dropdown = None
#         project_lead_dropdown = None
#         project_manager_dropdown = None
#         employee_dropdown = None
#         submit_btn = None

#         for el in dom:
#             label = (el.get("label") or "").lower()
#             tag = (el.get("tag") or "").lower()
#             el_type = el.get("type")

#             if "column menu" in label:
#                 continue

#             # Navigation
            
#             if "resource" in label and "planner" in label:
#                 resource_planner_btn = el

#             if label == "projects" and tag == "button":
#                 projects_tab = el

#             if ("add project" in label or "create project" in label) and tag == "button":
#                 add_project_btn = el

#             # Form Fields
#             if tag == "input" and "project" in label and "name" in label:
#                 project_name_input = el

#             if tag == "input" and el_type == "date" and "start" in label:
#                 start_date_input = el

#             if tag == "input" and el_type == "date" and "end" in label:
#                 end_date_input = el

#             if tag == "input" and "category" in label:
#                 project_category_dropdown = el

#             if tag == "input" and "client" in label:
#                 client_dropdown = el

#             if tag == "input" and "lead" in label:
#                 project_lead_dropdown = el

#             if tag == "input" and "manager" in label:
#                 project_manager_dropdown = el

#             if tag == "input" and "employee" in label:
#                 employee_dropdown = el

#             if tag == "button" and "create new project" in label:
#                 submit_btn = el

#         # -----------------------------------------------------
#         # 🔥 Combobox Fallback Mapping
#         # -----------------------------------------------------

#         comboboxes = [
#             el for el in dom
#             if el.get("tag") == "input"
#             and (el.get("label") or "").lower() == "combobox"
#         ]

#         if comboboxes:
#             if not client_dropdown and len(comboboxes) >= 1:
#                 client_dropdown = comboboxes[0]
#             if not project_lead_dropdown and len(comboboxes) >= 2:
#                 project_lead_dropdown = comboboxes[1]
#             if not project_manager_dropdown and len(comboboxes) >= 3:
#                 project_manager_dropdown = comboboxes[2]
#             if not employee_dropdown and len(comboboxes) >= 4:
#                 employee_dropdown = comboboxes[3]

#         # -----------------------------------------------------
#         # 🚀 Navigation Flow
#         # ----------------------------------------------------
#         is_on_resource_page = "resource" in url.lower()
        

#             # If form not opened yet, open it
#         if add_project_btn and not project_name_input:
#                 return {"action": "click", "selector": add_project_btn["selector"]}

    
#         if resource_planner_btn and not is_on_resource_page:
#             return {"action": "click", "selector": resource_planner_btn["selector"]}

#         if projects_tab and is_on_resource_page and not add_project_btn:
#             return {"action": "click", "selector": projects_tab["selector"]}

#         if add_project_btn and not project_name_input:
#             {"action": "click", "selector": add_project_btn["selector"]}
    

#         # -----------------------------------------------------
#         # 📝 Fill Form
#         # -----------------------------------------------------

#         if project_name_input and project_name_input["selector"] not in INTERACTED_SELECTORS:
#             INTERACTED_SELECTORS.add(project_name_input["selector"])
#             return {
#                 "action": "type",
#                 "selector": project_name_input["selector"],
#                 "text": f"AutoProject_{datetime.now().strftime('%H%M%S')}"
#             }

#         if start_date_input and start_date_input["selector"] not in INTERACTED_SELECTORS:
#             INTERACTED_SELECTORS.add(start_date_input["selector"])
#             return {
#                 "action": "type",
#                 "selector": start_date_input["selector"],
#                 "text": datetime.now().strftime("%Y-%m-%d")
#             }

#         if end_date_input and end_date_input["selector"] not in INTERACTED_SELECTORS:
#             INTERACTED_SELECTORS.add(end_date_input["selector"])
#             return {
#                 "action": "type",
#                 "selector": end_date_input["selector"],
#                 "text": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
#             }

#         # Dropdowns (single interaction each)
#         for dropdown in [
#             project_category_dropdown,
#             client_dropdown,
#             project_lead_dropdown,
#             project_manager_dropdown,
#         ]:
#             if dropdown and dropdown["selector"] not in INTERACTED_SELECTORS:
#                 INTERACTED_SELECTORS.add(dropdown["selector"])
#                 return {
#                     "action": "type",
#                     "selector": dropdown["selector"],
#                     "text": "a"
#                 }

#         # -----------------------------------------------------
#         # 👥 EMPLOYEE MULTI SELECT (ONLY 1)
#         # -----------------------------------------------------

#         # -----------------------------------------------------
# # 👥 EMPLOYEE MULTI SELECT (Fixed)
# # -----------------------------------------------------

#         if employee_dropdown and employee_dropdown["selector"] not in INTERACTED_SELECTORS:
#             INTERACTED_SELECTORS.add(employee_dropdown["selector"])
#             return {
#                 "action": "type",
#                 "selector": employee_dropdown["selector"],
#                 "text": "a"
#             }


#         # -----------------------------------------------------
#         # ✅ Submit
#         # -----------------------------------------------------

#         if submit_btn:
#             return {"action": "click", "selector": submit_btn["selector"]}
#         print(submit_btn, add_project_btn)
  
#     except Exception as e:
#         print("Project handler error:", e)

#     return {"action": "wait", "seconds": 2}





# _______________________________________1 st resolved code _________________________________________________




# from datetime import datetime, timedelta

# # =========================================================
# # 🗂️ STATE MACHINE
# # Tracks progress so we never re-open a completed form
# # =========================================================

# class AgentState:
#     def __init__(self):
#         self.interacted_selectors: set = set()
#         self.phase: str = "init"          # init → navigating → form_open → form_filling → submitted → done
#         self.project_submitted: bool = False

#     def reset(self):
#         self.__init__()


# # One shared state per session (reset between runs from agent.py if needed)
# state = AgentState()


# # =========================================================
# # 🚀 ENTRY FUNCTION
# # =========================================================

# async def decide_action(goal, dom, url, email=None, password=None):
#     return await decide_action_with_failed_indices(goal, dom, url, email, password)


# # =========================================================
# # 🧠 MAIN DECISION FUNCTION
# # =========================================================

# async def decide_action_with_failed_indices(goal, dom, url, email=None, password=None):

#     # =========================================================
#     # 🔐 LOGIN HANDLER
#     # =========================================================
#     try:
#         email_input = None
#         password_input = None
#         next_button = None
#         sign_in_button = None
#         yes_button = None

#         for el in dom:
#             label = (el.get("label") or "").lower().strip()
#             tag = (el.get("tag") or "").lower()
#             el_type = el.get("type")

#             if el_type == "email" or (tag == "input" and "email" in label):
#                 email_input = el
#             if el_type == "password":
#                 password_input = el
#             if tag in ["button", "input"]:
#                 if "next" in label:
#                     next_button = el
#                 if any(x in label for x in ["sign in", "login", "submit"]):
#                     sign_in_button = el
#                 if "yes" in label:
#                     yes_button = el

#         if yes_button:
#             return {"action": "click", "selector": yes_button["selector"]}

#         if email_input and not password_input:
#             if not email_input.get("value") and email:
#                 return {"action": "type", "selector": email_input["selector"], "text": email}
#             if email_input.get("value") and next_button:
#                 return {"action": "click", "selector": next_button["selector"]}

#         if password_input:
#             if not password_input.get("value") and password:
#                 return {"action": "type", "selector": password_input["selector"], "text": password}
#             if password_input.get("value") and sign_in_button:
#                 return {"action": "click", "selector": sign_in_button["selector"]}

#     except Exception as e:
#         print("Login handler error:", e)

#     # =========================================================
#     # 🚦 GOAL ROUTING
#     # =========================================================
#     is_create_project = any(
#         keyword in goal.lower()
#         for keyword in ["create project", "add project", "new project"]
#     )

#     if not is_create_project:
#         return {"action": "wait", "seconds": 2}

#     # =========================================================
#     # ✅ ALREADY DONE — never re-enter the flow
#     # =========================================================
#     if state.project_submitted:
#         print("🎉 Project already submitted. Signalling done.")
#         return {"action": "done"}

#     # =========================================================
#     # 📁 PROJECT CREATION HANDLER
#     # =========================================================
#     try:
#         # ---------------------------------------------------------
#         # 🔍 Detect Elements
#         # ---------------------------------------------------------
#         resource_planner_btn = None
#         projects_tab = None
#         add_project_btn = None

#         project_name_input = None
#         start_date_input = None
#         end_date_input = None
#         project_category_dropdown = None
#         client_dropdown = None
#         project_lead_dropdown = None
#         project_manager_dropdown = None
#         employee_dropdown = None
#         submit_btn = None

#         for el in dom:
#             label = (el.get("label") or "").lower().strip()
#             tag = (el.get("tag") or "").lower()
#             el_type = el.get("type")

#             # Skip noisy menu elements
#             if "column menu" in label:
#                 continue

#             # --- Navigation ---
#             if "resource" in label and "planner" in label:
#                 resource_planner_btn = el

#             if label == "projects" and tag == "button":
#                 projects_tab = el

#             if ("add project" in label or "create project" in label) and tag == "button":
#                 add_project_btn = el

#             # --- Form Fields ---
#             if tag == "input" and "project" in label and "name" in label:
#                 project_name_input = el

#             if tag == "input" and el_type == "date" and "start" in label:
#                 start_date_input = el

#             if tag == "input" and el_type == "date" and "end" in label:
#                 end_date_input = el

#             if tag == "input" and "category" in label:
#                 project_category_dropdown = el

#             if tag == "input" and "client" in label:
#                 client_dropdown = el

#             if tag == "input" and "lead" in label:
#                 project_lead_dropdown = el

#             if tag == "input" and "manager" in label:
#                 project_manager_dropdown = el

#             if tag == "input" and "employee" in label:
#                 employee_dropdown = el

#             if tag == "button" and "create new project" in label:
#                 submit_btn = el

#         # ---------------------------------------------------------
#         # 🔥 Combobox Fallback Mapping
#         # ---------------------------------------------------------
#         comboboxes = [
#             el for el in dom
#             if el.get("tag") == "input"
#             and (el.get("label") or "").lower() == "combobox"
#         ]

#         if comboboxes:
#             if not client_dropdown and len(comboboxes) >= 1:
#                 client_dropdown = comboboxes[0]
#             if not project_lead_dropdown and len(comboboxes) >= 2:
#                 project_lead_dropdown = comboboxes[1]
#             if not project_manager_dropdown and len(comboboxes) >= 3:
#                 project_manager_dropdown = comboboxes[2]
#             if not employee_dropdown and len(comboboxes) >= 4:
#                 employee_dropdown = comboboxes[3]

#         # ---------------------------------------------------------
#         # 🚀 Navigation Flow  (only runs when form is NOT open)
#         # ---------------------------------------------------------
#         form_is_open = project_name_input is not None

#         if not form_is_open:
#             is_on_resource_page = "resource" in url.lower()

#             if not is_on_resource_page and resource_planner_btn:
#                 print("➡️  Navigating to Resource Planner")
#                 return {"action": "click", "selector": resource_planner_btn["selector"]}

#             if is_on_resource_page and not projects_tab and add_project_btn:
#                 # Already on the right page, open form directly
#                 print("➡️  Opening Add Project form")
#                 return {"action": "click", "selector": add_project_btn["selector"]}

#             if is_on_resource_page and projects_tab and not add_project_btn:
#                 print("➡️  Clicking Projects tab")
#                 return {"action": "click", "selector": projects_tab["selector"]}

#             if add_project_btn:
#                 print("➡️  Opening Add Project form")
#                 return {"action": "click", "selector": add_project_btn["selector"]}

#             # Nothing to act on yet — wait for page to settle
#             return {"action": "wait", "seconds": 2}

#         # ---------------------------------------------------------
#         # 📝 Fill Form  (runs only when form IS open)
#         # ---------------------------------------------------------

#         def _not_done(el):
#             """True if this field exists and hasn't been interacted with yet."""
#             return el is not None and el["selector"] not in state.interacted_selectors

#         if _not_done(project_name_input):
#             state.interacted_selectors.add(project_name_input["selector"])
#             return {
#                 "action": "type",
#                 "selector": project_name_input["selector"],
#                 "text": f"AutoProject_{datetime.now().strftime('%H%M%S')}"
#             }

#         if _not_done(start_date_input):
#             state.interacted_selectors.add(start_date_input["selector"])
#             return {
#                 "action": "type",
#                 "selector": start_date_input["selector"],
#                 "text": datetime.now().strftime("%Y-%m-%d")
#             }

#         if _not_done(end_date_input):
#             state.interacted_selectors.add(end_date_input["selector"])
#             return {
#                 "action": "type",
#                 "selector": end_date_input["selector"],
#                 "text": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
#             }

#         # Dropdowns — type "a" to trigger autocomplete, executor clicks first option
#         for dropdown in [
#             project_category_dropdown,
#             client_dropdown,
#             project_lead_dropdown,
#             project_manager_dropdown,
#             employee_dropdown,
#         ]:
#             if _not_done(dropdown):
#                 state.interacted_selectors.add(dropdown["selector"])
#                 return {
#                     "action": "type",
#                     "selector": dropdown["selector"],
#                     "text": "a"
#                 }

#         # ---------------------------------------------------------
#         # ✅ Submit
#         # ---------------------------------------------------------
#         if submit_btn:
#             print("🚀 Submitting project form...")
#             state.project_submitted = True          # ← set BEFORE returning
#             return {"action": "click", "selector": submit_btn["selector"]}

#         # Form is open but submit not yet visible — wait
#         print("⏳ Form open but submit button not found yet, waiting...")
#         return {"action": "wait", "seconds": 2}

#     except Exception as e:
#         print("Project handler error:", e)

#     return {"action": "wait", "seconds": 2}


# # =========================================================
# # 🔄 RESET — call this from agent.py between runs
# # =========================================================
# def reset_state():
#     state.reset()
#     print("🔄 Agent state reset")

from datetime import datetime, timedelta


# =========================================================
# 🗂️ STATE MACHINE
# =========================================================

class AgentState:
    def __init__(self):
        self.interacted_selectors: set = set()
        self.project_submitted: bool = False
        self.project_verified: bool = False
        self.last_project_name: str = ""
        self.phase: str = "init"  # init → navigating → form_open → submitted → verified → done

    def reset(self):
        self.__init__()


state = AgentState()


def reset_state():
    state.reset()
    print("🔄 Agent state reset")


# =========================================================
# 🚀 ENTRY FUNCTION
# =========================================================

async def decide_action(goal, dom, url, email=None, password=None):
    return await _decide(goal, dom, url, email, password)


# =========================================================
# 🔐 LOGIN HANDLER
# =========================================================

def _handle_login(dom, email, password):
    email_input = None
    password_input = None
    next_button = None
    sign_in_button = None
    yes_button = None

    for el in dom:
        label = (el.get("label") or "").lower().strip()
        tag = (el.get("tag") or "").lower()
        el_type = el.get("type")

        if el_type == "email" or (tag == "input" and "email" in label):
            email_input = el
        if el_type == "password":
            password_input = el
        if tag in ["button", "input"]:
            if "next" in label:
                next_button = el
            if any(x in label for x in ["sign in", "login", "submit"]):
                sign_in_button = el
            if "yes" in label:
                yes_button = el

    if yes_button:
        return {"action": "click", "selector": yes_button["selector"]}

    if email_input and not password_input:
        if not email_input.get("value") and email:
            return {"action": "type", "selector": email_input["selector"], "text": email}
        if email_input.get("value") and next_button:
            return {"action": "click", "selector": next_button["selector"]}

    if password_input:
        if not password_input.get("value") and password:
            return {"action": "type", "selector": password_input["selector"], "text": password}
        if password_input.get("value") and sign_in_button:
            return {"action": "click", "selector": sign_in_button["selector"]}

    return None


# =========================================================
# 🔍 DOM ELEMENT DETECTOR
# =========================================================

def _detect_elements(dom):
    elements = {
        "resource_planner_btn": None,
        "projects_tab": None,
        "add_project_btn": None,
        "project_name_input": None,
        "start_date_input": None,
        "end_date_input": None,
        "project_category_dropdown": None,
        "client_dropdown": None,
        "project_lead_dropdown": None,
        "project_manager_dropdown": None,
        "employee_dropdown": None,
        "submit_btn": None,
        "comboboxes": [],
    }

    for el in dom:
        label = (el.get("label") or "").lower().strip()
        tag = (el.get("tag") or "").lower()
        el_type = el.get("type")

        if "column menu" in label:
            continue

        # Navigation
        if "resource" in label and "planner" in label:
            elements["resource_planner_btn"] = el
        if label == "projects" and tag == "button":
            elements["projects_tab"] = el
        if ("add project" in label or "create project" in label) and tag == "button":
            elements["add_project_btn"] = el

        # Form fields
        if tag == "input" and "project" in label and "name" in label:
            elements["project_name_input"] = el
        if tag == "input" and el_type == "date" and "start" in label:
            elements["start_date_input"] = el
        if tag == "input" and el_type == "date" and "end" in label:
            elements["end_date_input"] = el
        if tag == "input" and "category" in label:
            elements["project_category_dropdown"] = el
        if tag == "input" and "client" in label:
            elements["client_dropdown"] = el
        if tag == "input" and "lead" in label:
            elements["project_lead_dropdown"] = el
        if tag == "input" and "manager" in label:
            elements["project_manager_dropdown"] = el
        if tag == "input" and "employee" in label:
            elements["employee_dropdown"] = el
        if tag == "button" and "create new project" in label:
            elements["submit_btn"] = el

        # Combobox fallback
        if tag == "input" and label == "combobox":
            elements["comboboxes"].append(el)

    # Apply combobox fallback
    cb = elements["comboboxes"]
    if cb:
        if not elements["client_dropdown"] and len(cb) >= 1:
            elements["client_dropdown"] = cb[0]
        if not elements["project_lead_dropdown"] and len(cb) >= 2:
            elements["project_lead_dropdown"] = cb[1]
        if not elements["project_manager_dropdown"] and len(cb) >= 3:
            elements["project_manager_dropdown"] = cb[2]
        if not elements["employee_dropdown"] and len(cb) >= 4:
            elements["employee_dropdown"] = cb[3]

    return elements


# =========================================================
# ✅ VERIFICATION — check project visible in DOM
# =========================================================

def _verify_project_in_dom(dom, project_name):
    name_lower = project_name.lower()
    for el in dom:
        label = (el.get("label") or "").lower()
        text = (el.get("text") or "").lower()
        value = (el.get("value") or "").lower()
        if name_lower in label or name_lower in text or name_lower in value:
            return True
    return False


# =========================================================
# 🧠 MAIN DECISION FUNCTION
# =========================================================

async def _decide(goal, dom, url, email=None, password=None):

    # --- Login ---
    try:
        login_action = _handle_login(dom, email, password)
        if login_action:
            return login_action
    except Exception as e:
        print("Login handler error:", e)

    # --- Goal check ---
    is_create_project = any(
        kw in goal.lower()
        for kw in ["create project", "add project", "new project"]
    )

    if not is_create_project:
        return {"action": "wait", "seconds": 2}

    # =========================================================
    # 📋 PHASE: VERIFY — project submitted, now check visibility
    # =========================================================
    # BAAD MEIN — empty DOM ko handle karo:
    if state.project_submitted and not state.project_verified:
        print(f"🔍 Verifying project '{state.last_project_name}' is visible...")
        print("=== DOM LABELS FOR DEBUG ===")
        for el in dom:
            label = (el.get("label") or "").strip()
            text  = (el.get("text") or "").strip()
            tag   = el.get("tag", "")
            if label or text:
                print(f"  [{tag}] label='{label}' | text='{text}'")
        print("=== END DOM DEBUG ===")

        # ✅ Agar DOM empty hai — page close ya crash
        if not dom:
            print("⚠️ DOM is empty — page may be closed or crashed")
            return {
                "action": "done",
                "result": "UNKNOWN",
                "reason": "Project was submitted but page closed before verification"
            }

        if _verify_project_in_dom(dom, state.last_project_name):
            state.project_verified = True
            state.phase = "done"
            return {
                "action": "done",
                "result": "PASS",
                "reason": f"Project '{state.last_project_name}' visible in DOM"
            }

        print("⏳ Project not yet visible, waiting...")
        return {"action": "wait", "seconds": 2}
    # =========================================================
    # ✅ PHASE: DONE
    # =========================================================
    if state.project_verified:
        return {"action": "done", "result": "PASS"}

    # =========================================================
    # 📁 PROJECT CREATION HANDLER
    # =========================================================
    try:
        els = _detect_elements(dom)
        form_is_open = els["project_name_input"] is not None

        # ---------------------------------------------------------
        # 🚀 PHASE: NAVIGATE (form not open yet)
        # ---------------------------------------------------------
        if not form_is_open:
            is_on_resource_page = "resource" in url.lower()
            state.phase = "navigating"

            if not is_on_resource_page and els["resource_planner_btn"]:
                print("➡️  Navigating to Resource Planner")
                return {"action": "click", "selector": els["resource_planner_btn"]["selector"]}

            if is_on_resource_page and els["projects_tab"] and not els["add_project_btn"]:
                print("➡️  Clicking Projects tab")
                return {"action": "click", "selector": els["projects_tab"]["selector"]}

            if els["add_project_btn"]:
                print("➡️  Opening Add Project form")
                return {"action": "click", "selector": els["add_project_btn"]["selector"]}

            return {"action": "wait", "seconds": 2}

        # ---------------------------------------------------------
        # 📝 PHASE: FILL FORM
        # ---------------------------------------------------------
        state.phase = "form_filling"

        def _pending(el):
            return el is not None and el["selector"] not in state.interacted_selectors

        # Project Name
        if _pending(els["project_name_input"]):
            name = f"AutoProject_{datetime.now().strftime('%H%M%S')}"
            state.last_project_name = name
            state.interacted_selectors.add(els["project_name_input"]["selector"])
            return {
                "action": "type",
                "selector": els["project_name_input"]["selector"],
                "text": name
            }

        # Start Date
        if _pending(els["start_date_input"]):
            state.interacted_selectors.add(els["start_date_input"]["selector"])
            return {
                "action": "type",
                "selector": els["start_date_input"]["selector"],
                "text": datetime.now().strftime("%Y-%m-%d")
            }

        # End Date
        if _pending(els["end_date_input"]):
            state.interacted_selectors.add(els["end_date_input"]["selector"])
            return {
                "action": "type",
                "selector": els["end_date_input"]["selector"],
                "text": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
            }

        # Dropdowns
        for dropdown in [
            els["project_category_dropdown"],
            els["client_dropdown"],
            els["project_lead_dropdown"],
            els["project_manager_dropdown"],
            els["employee_dropdown"],
        ]:
            if _pending(dropdown):
                state.interacted_selectors.add(dropdown["selector"])
                return {
                    "action": "type",
                    "selector": dropdown["selector"],
                    "text": "a"
                }

        # ---------------------------------------------------------
        # ✅ SUBMIT
        # ---------------------------------------------------------
        if els["submit_btn"]:
            print(f"🚀 Submitting project '{state.last_project_name}'...")
            state.phase = "submitted"
            state.project_submitted = True
            return {"action": "click", "selector": els["submit_btn"]["selector"]}

        print("⏳ Form open but submit not visible yet...")
        return {"action": "wait", "seconds": 2}

    except Exception as e:
        print("Project handler error:", e)
        import traceback
        traceback.print_exc()

    return {"action": "wait", "seconds": 2}



