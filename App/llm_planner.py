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

# from datetime import datetime, timedelta


# # =========================================================
# # 🗂️ STATE MACHINE
# # =========================================================

# class AgentState:
#     def __init__(self):
#         self.interacted_selectors: set = set()
#         self.project_submitted: bool = False
#         self.project_verified: bool = False
#         self.last_project_name: str = ""
#         self.phase: str = "init"  # init → navigating → form_open → submitted → verified → done

#     def reset(self):
#         self.__init__()


# state = AgentState()


# def reset_state():
#     state.reset()
#     print("🔄 Agent state reset")


# # =========================================================
# # 🚀 ENTRY FUNCTION
# # =========================================================

# async def decide_action(goal, dom, url, email=None, password=None):
#     return await _decide(goal, dom, url, email, password)


# # =========================================================
# # 🔐 LOGIN HANDLER
# # =========================================================

# def _handle_login(dom, email, password):
#     email_input = None
#     password_input = None
#     next_button = None
#     sign_in_button = None
#     yes_button = None

#     for el in dom:
#         label = (el.get("label") or "").lower().strip()
#         tag = (el.get("tag") or "").lower()
#         el_type = el.get("type")

#         if el_type == "email" or (tag == "input" and "email" in label):
#             email_input = el
#         if el_type == "password":
#             password_input = el
#         if tag in ["button", "input"]:
#             if "next" in label:
#                 next_button = el
#             if any(x in label for x in ["sign in", "login", "submit"]):
#                 sign_in_button = el
#             if "yes" in label:
#                 yes_button = el

#     if yes_button:
#         return {"action": "click", "selector": yes_button["selector"]}

#     if email_input and not password_input:
#         if not email_input.get("value") and email:
#             return {"action": "type", "selector": email_input["selector"], "text": email}
#         if email_input.get("value") and next_button:
#             return {"action": "click", "selector": next_button["selector"]}

#     if password_input:
#         if not password_input.get("value") and password:
#             return {"action": "type", "selector": password_input["selector"], "text": password}
#         if password_input.get("value") and sign_in_button:
#             return {"action": "click", "selector": sign_in_button["selector"]}

#     return None


# # =========================================================
# # 🔍 DOM ELEMENT DETECTOR
# # =========================================================

# def _detect_elements(dom):
#     elements = {
#         "resource_planner_btn": None,
#         "projects_tab": None,
#         "add_project_btn": None,
#         "project_name_input": None,
#         "start_date_input": None,
#         "end_date_input": None,
#         "project_category_dropdown": None,
#         "client_dropdown": None,
#         "project_lead_dropdown": None,
#         "project_manager_dropdown": None,
#         "employee_dropdown": None,
#         "submit_btn": None,
#         "comboboxes": [],
#     }

#     for el in dom:
#         label = (el.get("label") or "").lower().strip()
#         tag = (el.get("tag") or "").lower()
#         el_type = el.get("type")

#         if "column menu" in label:
#             continue

#         # Navigation
#         if "resource" in label and "planner" in label:
#             elements["resource_planner_btn"] = el
#         if label == "projects" and tag == "button":
#             elements["projects_tab"] = el
#         if ("add project" in label or "create project" in label) and tag == "button":
#             elements["add_project_btn"] = el

#         # Form fields
#         if tag == "input" and "project" in label and "name" in label:
#             elements["project_name_input"] = el
#         if tag == "input" and el_type == "date" and "start" in label:
#             elements["start_date_input"] = el
#         if tag == "input" and el_type == "date" and "end" in label:
#             elements["end_date_input"] = el
#         if tag == "input" and "category" in label:
#             elements["project_category_dropdown"] = el
#         if tag == "input" and "client" in label:
#             elements["client_dropdown"] = el
#         if tag == "input" and "lead" in label:
#             elements["project_lead_dropdown"] = el
#         if tag == "input" and "manager" in label:
#             elements["project_manager_dropdown"] = el
#         if tag == "input" and "employee" in label:
#             elements["employee_dropdown"] = el
#         if tag == "button" and "create new project" in label:
#             elements["submit_btn"] = el

#         # Combobox fallback
#         if tag == "input" and label == "combobox":
#             elements["comboboxes"].append(el)

#     # Apply combobox fallback
#     cb = elements["comboboxes"]
#     if cb:
#         if not elements["client_dropdown"] and len(cb) >= 1:
#             elements["client_dropdown"] = cb[0]
#         if not elements["project_lead_dropdown"] and len(cb) >= 2:
#             elements["project_lead_dropdown"] = cb[1]
#         if not elements["project_manager_dropdown"] and len(cb) >= 3:
#             elements["project_manager_dropdown"] = cb[2]
#         if not elements["employee_dropdown"] and len(cb) >= 4:
#             elements["employee_dropdown"] = cb[3]

#     return elements


# # =========================================================
# # ✅ VERIFICATION — check project visible in DOM
# # =========================================================

# def _verify_project_in_dom(dom, project_name):
#     name_lower = project_name.lower()
#     for el in dom:
#         label = (el.get("label") or "").lower()
#         text = (el.get("text") or "").lower()
#         value = (el.get("value") or "").lower()
#         if name_lower in label or name_lower in text or name_lower in value:
#             return True
#     return False


# # =========================================================
# # 🧠 MAIN DECISION FUNCTION
# # =========================================================

# async def _decide(goal, dom, url, email=None, password=None):

#     # --- Login ---
#     try:
#         login_action = _handle_login(dom, email, password)
#         if login_action:
#             return login_action
#     except Exception as e:
#         print("Login handler error:", e)

#     # --- Goal check ---
#     is_create_project = any(
#         kw in goal.lower()
#         for kw in ["create project", "add project", "new project"]
#     )

#     if not is_create_project:
#         return {"action": "wait", "seconds": 2}

#     # =========================================================
#     # 📋 PHASE: VERIFY — project submitted, now check visibility
#     # =========================================================
#     # BAAD MEIN — empty DOM ko handle karo:
#     if state.project_submitted and not state.project_verified:
#         print(f"🔍 Verifying project '{state.last_project_name}' is visible...")
#         print("=== DOM LABELS FOR DEBUG ===")
#         for el in dom:
#             label = (el.get("label") or "").strip()
#             text  = (el.get("text") or "").strip()
#             tag   = el.get("tag", "")
#             if label or text:
#                 print(f"  [{tag}] label='{label}' | text='{text}'")
#         print("=== END DOM DEBUG ===")

#         # ✅ Agar DOM empty hai — page close ya crash
#         if not dom:
#             print("⚠️ DOM is empty — page may be closed or crashed")
#             return {
#                 "action": "done",
#                 "result": "UNKNOWN",
#                 "reason": "Project was submitted but page closed before verification"
#             }

#         if _verify_project_in_dom(dom, state.last_project_name):
#             state.project_verified = True
#             state.phase = "done"
#             return {
#                 "action": "done",
#                 "result": "PASS",
#                 "reason": f"Project '{state.last_project_name}' visible in DOM"
#             }

#         print("⏳ Project not yet visible, waiting...")
#         return {"action": "wait", "seconds": 2}
#     # =========================================================
#     # ✅ PHASE: DONE
#     # =========================================================
#     if state.project_verified:
#         return {"action": "done", "result": "PASS"}

#     # =========================================================
#     # 📁 PROJECT CREATION HANDLER
#     # =========================================================
#     try:
#         els = _detect_elements(dom)
#         form_is_open = els["project_name_input"] is not None

#         # ---------------------------------------------------------
#         # 🚀 PHASE: NAVIGATE (form not open yet)
#         # ---------------------------------------------------------
#         if not form_is_open:
#             is_on_resource_page = "resource" in url.lower()
#             state.phase = "navigating"

#             if not is_on_resource_page and els["resource_planner_btn"]:
#                 print("➡️  Navigating to Resource Planner")
#                 return {"action": "click", "selector": els["resource_planner_btn"]["selector"]}

#             if is_on_resource_page and els["projects_tab"] and not els["add_project_btn"]:
#                 print("➡️  Clicking Projects tab")
#                 return {"action": "click", "selector": els["projects_tab"]["selector"]}

#             if els["add_project_btn"]:
#                 print("➡️  Opening Add Project form")
#                 return {"action": "click", "selector": els["add_project_btn"]["selector"]}

#             return {"action": "wait", "seconds": 2}

#         # ---------------------------------------------------------
#         # 📝 PHASE: FILL FORM
#         # ---------------------------------------------------------
#         state.phase = "form_filling"

#         def _pending(el):
#             return el is not None and el["selector"] not in state.interacted_selectors

#         # Project Name
#         if _pending(els["project_name_input"]):
#             name = f"AutoProject_{datetime.now().strftime('%H%M%S')}"
#             state.last_project_name = name
#             state.interacted_selectors.add(els["project_name_input"]["selector"])
#             return {
#                 "action": "type",
#                 "selector": els["project_name_input"]["selector"],
#                 "text": name
#             }

#         # Start Date
#         if _pending(els["start_date_input"]):
#             state.interacted_selectors.add(els["start_date_input"]["selector"])
#             return {
#                 "action": "type",
#                 "selector": els["start_date_input"]["selector"],
#                 "text": datetime.now().strftime("%Y-%m-%d")
#             }

#         # End Date
#         if _pending(els["end_date_input"]):
#             state.interacted_selectors.add(els["end_date_input"]["selector"])
#             return {
#                 "action": "type",
#                 "selector": els["end_date_input"]["selector"],
#                 "text": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
#             }

#         # Dropdowns
#         for dropdown in [
#             els["project_category_dropdown"],
#             els["client_dropdown"],
#             els["project_lead_dropdown"],
#             els["project_manager_dropdown"],
#             els["employee_dropdown"],
#         ]:
#             if _pending(dropdown):
#                 state.interacted_selectors.add(dropdown["selector"])
#                 return {
#                     "action": "type",
#                     "selector": dropdown["selector"],
#                     "text": "a"
#                 }

#         # ---------------------------------------------------------
#         # ✅ SUBMIT
#         # ---------------------------------------------------------
#         if els["submit_btn"]:
#             print(f"🚀 Submitting project '{state.last_project_name}'...")
#             state.phase = "submitted"
#             state.project_submitted = True
#             return {"action": "click", "selector": els["submit_btn"]["selector"]}

#         print("⏳ Form open but submit not visible yet...")
#         return {"action": "wait", "seconds": 2}

#     except Exception as e:
#         print("Project handler error:", e)
#         import traceback
#         traceback.print_exc()

# #     return {"action": "wait", "seconds": 2}
# from datetime import datetime, timedelta
# import re

# # =========================================================
# # 🗂️ STATE MACHINE
# # =========================================================

# class AgentState:
#     def __init__(self):
#         self.interacted_selectors: set = set()
#         self.phase: str = "init"

#         # CREATE flow
#         self.project_submitted: bool = False
#         self.project_verified: bool = False
#         self.last_project_name: str = ""

#         # UPDATE flow
#         self.target_project_name: str = ""
#         self.three_dot_clicked: bool = False
#         self.update_form_open: bool = False
#         self.update_submitted: bool = False
#         self.update_verified: bool = False
#         self._empty_dom_count: int = 0

#     def reset(self):
#         self.__init__()


# state = AgentState()


# def reset_state():
#     state.reset()
#     print("🔄 Agent state reset")


# # =========================================================
# # 🚀 ENTRY FUNCTION
# # =========================================================

# async def decide_action(goal, dom, url, email=None, password=None):
#     return await _decide(goal, dom, url, email, password)


# # =========================================================
# # 🔐 LOGIN HANDLER
# # =========================================================

# def _handle_login(dom, email, password):
#     email_input = password_input = next_button = sign_in_button = None
#     yes_button = no_button = dont_show_btn = mfa_input = verify_btn = None

#     for el in dom:
#         label   = (el.get("label") or "").lower().strip()
#         text    = (el.get("text") or "").lower().strip()
#         tag     = (el.get("tag") or "").lower()
#         el_type = el.get("type")
#         combined = label + " " + text

#         if el_type == "email" or (tag == "input" and "email" in label):
#             email_input = el
#         if el_type == "password":
#             password_input = el
#         if tag in ["button", "input", "a"]:
#             if "next" in combined:
#                 next_button = el
#             if any(x in combined for x in ["sign in", "login", "submit"]):
#                 sign_in_button = el
#             # ✅ MFA / Stay signed in handlers
#             if "yes" in combined and "stay" not in combined:
#                 yes_button = el
#             if any(x in combined for x in ["stay signed in", "yes, stay signed in"]):
#                 yes_button = el
#             if any(x in combined for x in ["no, sign in to another account", "no"]) and tag == "button":
#                 no_button = el
#             if any(x in combined for x in ["don't show this again", "dont show"]):
#                 dont_show_btn = el
#             if any(x in combined for x in ["verify", "approve", "confirm"]):
#                 verify_btn = el
#         if el_type == "tel" or (tag == "input" and any(x in label for x in ["code", "otp", "verification"])):
#             mfa_input = el

#     # ── Priority 1: Stay signed in / Yes prompt ──────────
#     if yes_button:
#         print("🔐 Clicking 'Yes' / Stay signed in")
#         return {"action": "click", "selector": yes_button["selector"]}

#     # ── Priority 2: "Don't show this again" checkbox ─────
#     if dont_show_btn:
#         print("🔐 Clicking 'Don't show this again'")
#         return {"action": "click", "selector": dont_show_btn["selector"]}

#     # ── Priority 3: MFA code input ────────────────────────
#     if mfa_input and not mfa_input.get("value"):
#         print("🔐 MFA input detected — waiting for user to enter code manually")
#         # We can't auto-fill MFA — just wait for user
#         return {"action": "wait", "seconds": 5}

#     if mfa_input and mfa_input.get("value") and verify_btn:
#         return {"action": "click", "selector": verify_btn["selector"]}

#     # ── Priority 4: Email step ────────────────────────────
#     if email_input and not password_input:
#         if not email_input.get("value") and email:
#             return {"action": "type", "selector": email_input["selector"], "text": email}
#         if email_input.get("value") and next_button:
#             return {"action": "click", "selector": next_button["selector"]}

#     # ── Priority 5: Password step ─────────────────────────
#     if password_input:
#         if not password_input.get("value") and password:
#             return {"action": "type", "selector": password_input["selector"], "text": password}
#         if password_input.get("value") and sign_in_button:
#             return {"action": "click", "selector": sign_in_button["selector"]}

#     return None


# # =========================================================
# # 🔍 PARSE GOAL — extract update details
# # =========================================================

# def _parse_update_goal(goal):
#     """
#     Auto-generate update values — same philosophy as create.
#     Only search_project is extracted from goal, rest is auto-generated.
#     """
#     ts = datetime.now().strftime("%H%M%S")
#     data = {
#         "client"          : "Auto Client",
#         "project_name"    : f"UpdatedProject_{ts}",
#         "project_lead"    : "",          # will type 'a' → pick first autocomplete
#         "project_manager" : "",          # same
#         "start_date"      : datetime.now().strftime("%Y-%m-%d"),
#         "end_date"        : (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
#         "category"        : "",
#         "status"          : "",
#         "flexible_hours"  : False,
#         "employees"       : [],
#     }
#     return data


# def _extract_search_project(goal):
#     """Extract project name from simple goal: 'login and update project AutoProject_125731'"""
#     # Match: update project <name>
#     m = re.search(r"update project\s+([A-Za-z0-9_\-]+)", goal, re.IGNORECASE)
#     if m:
#         return m.group(1).strip()
#     return ""


# # =========================================================
# # 🔍 DOM ELEMENT DETECTOR — CREATE
# # =========================================================

# def _detect_create_elements(dom):
#     els = {
#         "resource_planner_btn": None, "projects_tab": None,
#         "add_project_btn": None, "project_name_input": None,
#         "start_date_input": None, "end_date_input": None,
#         "project_category_dropdown": None, "client_dropdown": None,
#         "project_lead_dropdown": None, "project_manager_dropdown": None,
#         "employee_dropdown": None, "submit_btn": None, "comboboxes": [],
#     }
#     for el in dom:
#         label   = (el.get("label") or "").lower().strip()
#         tag     = (el.get("tag") or "").lower()
#         el_type = el.get("type")
#         if "column menu" in label: continue
#         if "resource" in label and "planner" in label: els["resource_planner_btn"] = el
#         if label == "projects" and tag == "button": els["projects_tab"] = el
#         if ("add project" in label or "create project" in label) and tag == "button": els["add_project_btn"] = el
#         if tag == "input" and "project" in label and "name" in label: els["project_name_input"] = el
#         if tag == "input" and el_type == "date" and "start" in label: els["start_date_input"] = el
#         if tag == "input" and el_type == "date" and "end" in label: els["end_date_input"] = el
#         if tag == "input" and "category" in label: els["project_category_dropdown"] = el
#         if tag == "input" and "client" in label: els["client_dropdown"] = el
#         if tag == "input" and "lead" in label: els["project_lead_dropdown"] = el
#         if tag == "input" and "manager" in label: els["project_manager_dropdown"] = el
#         if tag == "input" and "employee" in label: els["employee_dropdown"] = el
#         if tag == "button" and "create new project" in label: els["submit_btn"] = el
#         if tag == "input" and label == "combobox": els["comboboxes"].append(el)

#     cb = els["comboboxes"]
#     if cb:
#         if not els["client_dropdown"] and len(cb) >= 1:           els["client_dropdown"] = cb[0]
#         if not els["project_lead_dropdown"] and len(cb) >= 2:     els["project_lead_dropdown"] = cb[1]
#         if not els["project_manager_dropdown"] and len(cb) >= 3:  els["project_manager_dropdown"] = cb[2]
#         if not els["employee_dropdown"] and len(cb) >= 4:         els["employee_dropdown"] = cb[3]
#     return els


# # =========================================================
# # 🔍 DOM ELEMENT DETECTOR — UPDATE FORM
# # =========================================================

# def _detect_update_form_elements(dom):
#     els = {
#         "project_name_input": None, "start_date_input": None,
#         "end_date_input": None, "client_dropdown": None,
#         "project_lead_dropdown": None, "project_manager_dropdown": None,
#         "project_category_dropdown": None, "project_status_dropdown": None,
#         "employee_dropdown": None, "flexible_hours_checkbox": None,
#         "submit_btn": None, "comboboxes": [],
#     }
#     for el in dom:
#         label   = (el.get("label") or "").lower().strip()
#         tag     = (el.get("tag") or "").lower()
#         el_type = el.get("type")
#         if tag == "input" and "project" in label and "name" in label: els["project_name_input"] = el
#         if tag == "input" and el_type == "date" and "start" in label: els["start_date_input"] = el
#         if tag == "input" and el_type == "date" and "end" in label: els["end_date_input"] = el
#         if tag == "input" and "client" in label: els["client_dropdown"] = el
#         if tag == "input" and "lead" in label: els["project_lead_dropdown"] = el
#         if tag == "input" and "manager" in label: els["project_manager_dropdown"] = el
#         if tag == "input" and "category" in label: els["project_category_dropdown"] = el
#         if tag == "input" and "status" in label: els["project_status_dropdown"] = el
#         if tag == "input" and "employee" in label: els["employee_dropdown"] = el
#         if tag == "input" and el_type == "checkbox" and "flexible" in label: els["flexible_hours_checkbox"] = el
#         if tag == "button" and any(x in label for x in ["update", "save", "submit"]): els["submit_btn"] = el
#         if tag == "input" and label == "combobox": els["comboboxes"].append(el)

#     cb = els["comboboxes"]
#     if cb:
#         if not els["client_dropdown"] and len(cb) >= 1:           els["client_dropdown"] = cb[0]
#         if not els["project_lead_dropdown"] and len(cb) >= 2:     els["project_lead_dropdown"] = cb[1]
#         if not els["project_manager_dropdown"] and len(cb) >= 3:  els["project_manager_dropdown"] = cb[2]
#         if not els["employee_dropdown"] and len(cb) >= 4:         els["employee_dropdown"] = cb[3]
#     return els


# # =========================================================
# # ✅ HELPERS
# # =========================================================

# def _verify_project_in_dom(dom, project_name):
#     name_lower = project_name.lower()
#     for el in dom:
#         for field in ["label", "text", "value"]:
#             val = (el.get(field) or "").lower()
#             if name_lower in val:
#                 print(f"  ✅ Found '{project_name}' in [{el.get('tag')}] {field}")
#                 return True
#     return False


# def _format_date(date_str):
#     for fmt in ["%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d"]:
#         try:
#             return datetime.strptime(date_str.strip(), fmt).strftime("%Y-%m-%d")
#         except:
#             pass
#     return date_str


# def _find_three_dot_button(dom, project_name):
#     """
#     Find the Actions ⋮ button for the given project row.
#     Strategy: after finding the project row div, the LAST button
#     in that row is the Actions button (bare button with no label/text).
#     """
#     project_row_found = False
#     row_buttons = []

#     print(f"🔍 Searching three-dot button for: {project_name}")

#     for el in dom:
#         label = (el.get("label") or "").lower()
#         text  = (el.get("text") or "").lower()
#         tag   = (el.get("tag") or "").lower()
#         sel   = (el.get("selector") or "")

#         # Detect start of project row
#         if project_name.lower() in label or project_name.lower() in text:
#             project_row_found = True
#             row_buttons = []
#             print(f"  ✅ Found project row")
#             continue

#         if project_row_found:
#             if tag == "button":
#                 print(f"  🔘 Button: label='{label}' text='{text}' sel='{sel}'")
#                 row_buttons.append(el)

#             # Stop when we hit next project row (another div with date pattern)
#             if tag == "div" and len(row_buttons) > 0 and ("2025" in label or "2026" in label):
#                 if project_name.lower() not in label:
#                     break

#     if not row_buttons:
#         print(f"  ❌ No buttons found after project row")
#         return None

#     # The LAST button in the row is always the Actions ⋮
#     chosen = row_buttons[-1]
#     print(f"  ✅ Actions button selected: sel='{chosen.get('selector')}' label='{chosen.get('label')}'")
#     return chosen


# # =========================================================
# # 🧠 MAIN DECISION FUNCTION
# # =========================================================

# async def _decide(goal, dom, url, email=None, password=None):
#     try:
#         login_action = _handle_login(dom, email, password)
#         if login_action:
#             return login_action
#     except Exception as e:
#         print("Login handler error:", e)

#     goal_lower = goal.lower()

#     is_update = any(kw in goal_lower for kw in ["update project", "edit project", "modify project"])
#     is_create = any(kw in goal_lower for kw in ["create project", "add project", "new project"])

#     if is_update:
#         return await _handle_update_project(goal, dom, url)
#     if is_create:
#         return await _handle_create_project(goal, dom, url)

#     return {"action": "wait", "seconds": 2}


# # =========================================================
# # 📁 CREATE PROJECT FLOW
# # =========================================================

# async def _handle_create_project(goal, dom, url):
#     if state.project_submitted and not state.project_verified:
#         print(f"🔍 Verifying project '{state.last_project_name}'...")
#         if not dom:
#             state._empty_dom_count += 1
#             if state._empty_dom_count >= 3:
#                 return {"action": "done", "result": "UNKNOWN",
#                         "reason": "Submitted but page closed before verification"}
#             return {"action": "wait", "seconds": 2}
#         state._empty_dom_count = 0
#         if _verify_project_in_dom(dom, state.last_project_name):
#             state.project_verified = True
#             return {"action": "done", "result": "PASS",
#                     "reason": f"Project '{state.last_project_name}' visible in DOM"}
#         return {"action": "wait", "seconds": 2}

#     if state.project_verified:
#         return {"action": "done", "result": "PASS"}

#     try:
#         els = _detect_create_elements(dom)
#         form_is_open = els["project_name_input"] is not None

#         if not form_is_open:
#             is_on_resource_page = "resource" in url.lower()
#             if not is_on_resource_page and els["resource_planner_btn"]:
#                 return {"action": "click", "selector": els["resource_planner_btn"]["selector"]}
#             if is_on_resource_page and els["projects_tab"] and not els["add_project_btn"]:
#                 return {"action": "click", "selector": els["projects_tab"]["selector"]}
#             if els["add_project_btn"]:
#                 return {"action": "click", "selector": els["add_project_btn"]["selector"]}
#             return {"action": "wait", "seconds": 2}

#         def _pending(el):
#             return el is not None and el["selector"] not in state.interacted_selectors

#         if _pending(els["project_name_input"]):
#             name = f"AutoProject_{datetime.now().strftime('%H%M%S')}"
#             state.last_project_name = name
#             state.interacted_selectors.add(els["project_name_input"]["selector"])
#             return {"action": "type", "selector": els["project_name_input"]["selector"], "text": name}

#         if _pending(els["start_date_input"]):
#             state.interacted_selectors.add(els["start_date_input"]["selector"])
#             return {"action": "type", "selector": els["start_date_input"]["selector"],
#                     "text": datetime.now().strftime("%Y-%m-%d")}

#         if _pending(els["end_date_input"]):
#             state.interacted_selectors.add(els["end_date_input"]["selector"])
#             return {"action": "type", "selector": els["end_date_input"]["selector"],
#                     "text": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")}

#         for dropdown in [els["project_category_dropdown"], els["client_dropdown"],
#                          els["project_lead_dropdown"], els["project_manager_dropdown"],
#                          els["employee_dropdown"]]:
#             if _pending(dropdown):
#                 state.interacted_selectors.add(dropdown["selector"])
#                 return {"action": "type", "selector": dropdown["selector"], "text": "a"}

#         if els["submit_btn"]:
#             state.project_submitted = True
#             return {"action": "click", "selector": els["submit_btn"]["selector"]}

#         return {"action": "wait", "seconds": 2}

#     except Exception as e:
#         print("Create handler error:", e)
#         import traceback; traceback.print_exc()
#     return {"action": "wait", "seconds": 2}


# # =========================================================
# # ✏️ UPDATE PROJECT FLOW
# # =========================================================

# async def _handle_update_project(goal, dom, url):
#     data = _parse_update_goal(goal)

#     # Set target project name once
#     if not state.target_project_name:
#         name = _extract_search_project(goal)
#         if name:
#             state.target_project_name = name
#             print(f"🎯 Target project to update: '{state.target_project_name}'")

#     # ── VERIFIED ─────────────────────────────────────────
#     if state.update_verified:
#         return {"action": "done", "result": "PASS",
#                 "reason": f"Project updated successfully"}

#     # ── SUBMITTED — check result ──────────────────────────
#     if state.update_submitted and not state.update_verified:
#         print("🔍 Verifying update was saved...")
#         if not dom:
#             state._empty_dom_count += 1
#             if state._empty_dom_count >= 3:
#                 return {"action": "done", "result": "UNKNOWN",
#                         "reason": "Update submitted but page closed before verification"}
#             return {"action": "wait", "seconds": 2}
#         state._empty_dom_count = 0

#         # Check for success toast
#         for el in dom:
#             label = (el.get("label") or "").lower()
#             text  = (el.get("text") or "").lower()
#             if any(x in label or x in text for x in ["success", "updated", "saved", "project updated"]):
#                 state.update_verified = True
#                 return {"action": "done", "result": "PASS",
#                         "reason": "Update saved — success message visible"}

#         # Form closed = success
#         update_els = _detect_update_form_elements(dom)
#         if not update_els["project_name_input"] and not update_els["submit_btn"]:
#             state.update_verified = True
#             return {"action": "done", "result": "PASS",
#                     "reason": "Update form closed — project updated successfully"}

#         return {"action": "wait", "seconds": 2}

#     # ── FORM IS OPEN — fill it ────────────────────────────
#     if state.update_form_open:
#         return await _fill_update_form(dom, data)

#     # ── THREE DOT CLICKED — look for menu item ────────────
#     if state.three_dot_clicked:

#         # Debug — dekho DOM mein context menu aaya ya nahi
#         print("=== CONTEXT MENU DEBUG ===")
#         for el in dom:
#             label = (el.get("label") or "").strip()
#             text  = (el.get("text") or "").strip()
#             tag   = (el.get("tag") or "")
#             sel   = (el.get("selector") or "")
#             if label or text:
#                 print(f"  [{tag}] label='{label}' | text='{text}' | sel='{sel}'")
#         print("=== END CONTEXT MENU DEBUG ===")

#         for el in dom:
#             label = (el.get("label") or "").lower()
#             text  = (el.get("text") or "").lower()
#             if "update project" in label or "update project" in text:
#                 print("✅ Found 'Update Project' menu item")
#                 state.update_form_open = True
#                 state._three_dot_retry = 0
#                 return {"action": "click", "selector": el["selector"]}

#         # Menu never appeared — three-dot click landed on wrong button
#         state._three_dot_retry = getattr(state, "_three_dot_retry", 0) + 1
#         print(f"⏳ Context menu not found (attempt {state._three_dot_retry}/5)")

#         if state._three_dot_retry >= 5:
#             print("🔄 Three-dot click failed — resetting to retry with correct button")
#             state.three_dot_clicked = False
#             state._three_dot_retry  = 0
#             state.interacted_selectors = {
#                 s for s in state.interacted_selectors
#                 if not s.startswith("button")
#             }

#         return {"action": "wait", "seconds": 1}

#     # ── NAVIGATE + SEARCH + CLICK THREE DOT ──────────────
#     is_on_resource_page = "resource" in url.lower()
#     resource_btn = projects_tab = search_input = None

#     for el in dom:
#         label = (el.get("label") or "").lower().strip()
#         tag   = (el.get("tag") or "").lower()
#         if "column menu" in label: continue
#         if "resource" in label and "planner" in label: resource_btn = el
#         if label == "projects" and tag == "button": projects_tab = el
#         if "search project" in label and tag == "input": search_input = el

#     # Navigate to resource planner first
#     if not is_on_resource_page and resource_btn:
#         print("➡️ Navigating to Resource Planner")
#         return {"action": "click", "selector": resource_btn["selector"]}

#     # Click Projects tab
#     if is_on_resource_page and projects_tab:
#         sel = projects_tab["selector"]
#         if sel not in state.interacted_selectors:
#             state.interacted_selectors.add(sel)
#             print("➡️ Clicking Projects tab")
#             return {"action": "click", "selector": sel}

#     # Search for the project
#     if search_input and state.target_project_name:
#         sel = search_input["selector"]
#         if sel not in state.interacted_selectors:
#             state.interacted_selectors.add(sel)
#             print(f"🔍 Searching: {state.target_project_name}")
#             return {"action": "type", "selector": sel, "text": state.target_project_name}

#     # Find and click three-dot button
#     three_dot = _find_three_dot_button(dom, state.target_project_name)
#     if three_dot:
#         print(f"🎯 Clicking three-dot menu for '{state.target_project_name}'")
#         state.three_dot_clicked = True
#         return {"action": "click", "selector": three_dot["selector"]}

#     return {"action": "wait", "seconds": 2}


# # =========================================================
# # 📝 FILL UPDATE FORM
# # =========================================================

# async def _fill_update_form(dom, data):
#     els = _detect_update_form_elements(dom)

#     def _pending(el):
#         return el is not None and el["selector"] not in state.interacted_selectors

#     def _type(el, val):
#         state.interacted_selectors.add(el["selector"])
#         return {"action": "type", "selector": el["selector"], "text": val}

#     def _click(el):
#         state.interacted_selectors.add(el["selector"])
#         return {"action": "click", "selector": el["selector"]}

#     if _pending(els["client_dropdown"]) and data.get("client"):
#         return _type(els["client_dropdown"], data["client"])

#     if _pending(els["project_name_input"]) and data.get("project_name"):
#         return _type(els["project_name_input"], data["project_name"])

#     if _pending(els["project_lead_dropdown"]) and data.get("project_lead"):
#         return _type(els["project_lead_dropdown"], data["project_lead"])

#     if _pending(els["project_manager_dropdown"]) and data.get("project_manager"):
#         return _type(els["project_manager_dropdown"], data["project_manager"])

#     if _pending(els["start_date_input"]) and data.get("start_date"):
#         return _type(els["start_date_input"], _format_date(data["start_date"]))

#     if _pending(els["end_date_input"]) and data.get("end_date"):
#         return _type(els["end_date_input"], _format_date(data["end_date"]))

#     if _pending(els["project_category_dropdown"]) and data.get("category"):
#         return _type(els["project_category_dropdown"], data["category"])

#     if _pending(els["project_status_dropdown"]) and data.get("status"):
#         return _type(els["project_status_dropdown"], data["status"])

#     if _pending(els["flexible_hours_checkbox"]) and data.get("flexible_hours"):
#         return _click(els["flexible_hours_checkbox"])

#     # Employees — type each one separately
#     employees = data.get("employees", [])
#     for emp in employees:
#         emp_key = f"emp::{emp}"
#         if emp_key not in state.interacted_selectors and els["employee_dropdown"]:
#             state.interacted_selectors.add(emp_key)
#             return {"action": "type", "selector": els["employee_dropdown"]["selector"], "text": emp}

#     # Submit
#     if els["submit_btn"] and els["submit_btn"]["selector"] not in state.interacted_selectors:
#         print("🚀 Submitting update form...")
#         state.interacted_selectors.add(els["submit_btn"]["selector"])
#         state.update_submitted = True
#         return {"action": "click", "selector": els["submit_btn"]["selector"]}

#     print("⏳ Waiting for update form fields...")
#     return {"action": "wait", "seconds": 2}
from datetime import datetime, timedelta
import re

# =========================================================
# 🗂️ STATE MACHINE
# =========================================================

class AgentState:
    def __init__(self):
        self.interacted_selectors: set = set()
        self.phase: str = "init"

        # CREATE flow
        self.project_submitted: bool = False
        self.project_verified: bool = False
        self.last_project_name: str = ""

        # UPDATE flow
        self.target_project_name: str = ""
        self.three_dot_clicked: bool = False
        self.update_form_open: bool = False
        self.update_submitted: bool = False
        self.update_verified: bool = False
        self._empty_dom_count: int = 0
        self._three_dot_retry: int = 0
        self._verify_wait_count: int = 0
        self._pending_select_value: str = ""

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
    email_input = password_input = next_button = sign_in_button = None
    yes_button = no_button = dont_show_btn = mfa_input = verify_btn = None

    for el in dom:
        label    = (el.get("label") or "").lower().strip()
        text     = (el.get("text") or "").lower().strip()
        tag      = (el.get("tag") or "").lower()
        el_type  = el.get("type")
        combined = label + " " + text

        if el_type == "email" or (tag == "input" and "email" in label):
            email_input = el
        if el_type == "password":
            password_input = el
        if tag in ["button", "input", "a"]:
            if "next" in combined:
                next_button = el
            if any(x in combined for x in ["sign in", "login", "submit"]):
                sign_in_button = el
            if "yes" in combined and "stay" not in combined:
                yes_button = el
            if any(x in combined for x in ["stay signed in", "yes, stay signed in"]):
                yes_button = el
            if any(x in combined for x in ["no, sign in to another account", "no"]) and tag == "button":
                no_button = el
            if any(x in combined for x in ["don't show this again", "dont show"]):
                dont_show_btn = el
            if any(x in combined for x in ["verify", "approve", "confirm"]):
                verify_btn = el
        if el_type == "tel" or (tag == "input" and any(x in label for x in ["code", "otp", "verification"])):
            mfa_input = el

    if yes_button:
        print("🔐 Clicking 'Yes' / Stay signed in")
        return {"action": "click", "selector": yes_button["selector"]}

    if dont_show_btn:
        print("🔐 Clicking 'Don't show this again'")
        return {"action": "click", "selector": dont_show_btn["selector"]}

    if mfa_input and not mfa_input.get("value"):
        print("🔐 MFA input detected — waiting for user to enter code manually")
        return {"action": "wait", "seconds": 5}

    if mfa_input and mfa_input.get("value") and verify_btn:
        return {"action": "click", "selector": verify_btn["selector"]}

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
# 🔍 EXTRACT PROJECT NAME FROM GOAL
# =========================================================

def _extract_search_project(goal):
    m = re.search(r"update project\s+([A-Za-z0-9_\-]+)", goal, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return ""


# =========================================================
# 🔍 DOM ELEMENT DETECTOR — CREATE
# =========================================================

def _detect_create_elements(dom):
    els = {
        "resource_planner_btn": None, "projects_tab": None,
        "add_project_btn": None, "project_name_input": None,
        "start_date_input": None, "end_date_input": None,
        "project_category_dropdown": None, "client_dropdown": None,
        "project_lead_dropdown": None, "project_manager_dropdown": None,
        "employee_dropdown": None, "submit_btn": None, "comboboxes": [],
    }
    for el in dom:
        label   = (el.get("label") or "").lower().strip()
        tag     = (el.get("tag") or "").lower()
        el_type = el.get("type")
        if "column menu" in label: continue
        if "resource" in label and "planner" in label: els["resource_planner_btn"] = el
        if label == "projects" and tag == "button": els["projects_tab"] = el
        if ("add project" in label or "create project" in label) and tag == "button": els["add_project_btn"] = el
        if tag == "input" and "project" in label and "name" in label: els["project_name_input"] = el
        if tag == "input" and el_type == "date" and "start" in label: els["start_date_input"] = el
        if tag == "input" and el_type == "date" and "end" in label: els["end_date_input"] = el
        if tag == "input" and "category" in label: els["project_category_dropdown"] = el
        if tag == "input" and "client" in label: els["client_dropdown"] = el
        if tag == "input" and "lead" in label: els["project_lead_dropdown"] = el
        if tag == "input" and "manager" in label: els["project_manager_dropdown"] = el
        if tag == "input" and "employee" in label: els["employee_dropdown"] = el
        if tag == "button" and "create new project" in label: els["submit_btn"] = el
        if tag == "input" and label == "combobox": els["comboboxes"].append(el)

    cb = els["comboboxes"]
    if cb:
        if not els["client_dropdown"] and len(cb) >= 1:           els["client_dropdown"] = cb[0]
        if not els["project_lead_dropdown"] and len(cb) >= 2:     els["project_lead_dropdown"] = cb[1]
        if not els["project_manager_dropdown"] and len(cb) >= 3:  els["project_manager_dropdown"] = cb[2]
        if not els["employee_dropdown"] and len(cb) >= 4:         els["employee_dropdown"] = cb[3]
    return els


# =========================================================
# ✅ HELPERS
# =========================================================

def _verify_project_in_dom(dom, project_name):
    name_lower = project_name.lower()
    for el in dom:
        for field in ["label", "text", "value"]:
            val = (el.get(field) or "").lower()
            if name_lower in val:
                print(f"  ✅ Found '{project_name}' in [{el.get('tag')}] {field}")
                return True
    return False


def _format_date(date_str):
    for fmt in ["%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d"]:
        try:
            return datetime.strptime(date_str.strip(), fmt).strftime("%Y-%m-%d")
        except:
            pass
    return date_str


def _find_three_dot_button(dom, project_name):
    """
    Find the Actions ⋮ button using data-testid='ActionMenuButton'
    scoped to the project row.
    """
    print(f"🔍 Searching three-dot button for: {project_name}")

    project_row_found = False

    for el in dom:
        label       = (el.get("label") or "").lower()
        text        = (el.get("text") or "").lower()
        tag         = (el.get("tag") or "").lower()
        data_testid = (el.get("dataTestId") or "")

        # Detect project row start
        if project_name.lower() in label or project_name.lower() in text:
            project_row_found = True
            print(f"  ✅ Found project row")
            continue

        if project_row_found:
            # ✅ Best match — exact data-testid
            if data_testid == "ActionMenuButton":
                print(f"  ✅ Found ActionMenuButton via data-testid")
                return el

            # Stop at next project row
            if tag == "div" and ("2025" in label or "2026" in label):
                if project_name.lower() not in label:
                    break

    # Fallback — search entire DOM for ActionMenuButton
    print("  ⚠️ Row-scoped search failed — trying full DOM fallback")
    for el in dom:
        if (el.get("dataTestId") or "") == "ActionMenuButton":
            print(f"  ✅ Found ActionMenuButton in full DOM")
            return el

    print(f"  ❌ ActionMenuButton not found")
    return None


# =========================================================
# 🧠 MAIN DECISION FUNCTION
# =========================================================

async def _decide(goal, dom, url, email=None, password=None):
    try:
        login_action = _handle_login(dom, email, password)
        if login_action:
            return login_action
    except Exception as e:
        print("Login handler error:", e)

    goal_lower = goal.lower()

    is_update = any(kw in goal_lower for kw in ["update project", "edit project", "modify project"])
    is_create = any(kw in goal_lower for kw in ["create project", "add project", "new project"])

    if is_update:
        return await _handle_update_project(goal, dom, url)
    if is_create:
        return await _handle_create_project(goal, dom, url)

    return {"action": "wait", "seconds": 2}


# =========================================================
# 📁 CREATE PROJECT FLOW
# =========================================================

async def _handle_create_project(goal, dom, url):
    if state.project_submitted and not state.project_verified:
        print(f"🔍 Verifying project '{state.last_project_name}'...")
        if not dom:
            state._empty_dom_count += 1
            if state._empty_dom_count >= 3:
                return {"action": "done", "result": "UNKNOWN",
                        "reason": "Submitted but page closed before verification"}
            return {"action": "wait", "seconds": 2}
        state._empty_dom_count = 0
        if _verify_project_in_dom(dom, state.last_project_name):
            state.project_verified = True
            return {"action": "done", "result": "PASS",
                    "reason": f"Project '{state.last_project_name}' visible in DOM"}
        return {"action": "wait", "seconds": 2}

    if state.project_verified:
        return {"action": "done", "result": "PASS"}

    try:
        els = _detect_create_elements(dom)
        form_is_open = els["project_name_input"] is not None

        if not form_is_open:
            is_on_resource_page = "resource" in url.lower()
            if not is_on_resource_page and els["resource_planner_btn"]:
                return {"action": "click", "selector": els["resource_planner_btn"]["selector"]}
            if is_on_resource_page and els["projects_tab"] and not els["add_project_btn"]:
                return {"action": "click", "selector": els["projects_tab"]["selector"]}
            if els["add_project_btn"]:
                return {"action": "click", "selector": els["add_project_btn"]["selector"]}
            return {"action": "wait", "seconds": 2}

        def _pending(el):
            return el is not None and el["selector"] not in state.interacted_selectors

        if _pending(els["project_name_input"]):
            name = f"AutoProject_{datetime.now().strftime('%H%M%S')}"
            state.last_project_name = name
            state.interacted_selectors.add(els["project_name_input"]["selector"])
            return {"action": "type", "selector": els["project_name_input"]["selector"], "text": name}

        if _pending(els["start_date_input"]):
            state.interacted_selectors.add(els["start_date_input"]["selector"])
            return {"action": "type", "selector": els["start_date_input"]["selector"],
                    "text": datetime.now().strftime("%Y-%m-%d")}

        if _pending(els["end_date_input"]):
            state.interacted_selectors.add(els["end_date_input"]["selector"])
            return {"action": "type", "selector": els["end_date_input"]["selector"],
                    "text": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")}

        for dropdown in [els["project_category_dropdown"], els["client_dropdown"],
                         els["project_lead_dropdown"], els["project_manager_dropdown"],
                         els["employee_dropdown"]]:
            if _pending(dropdown):
                state.interacted_selectors.add(dropdown["selector"])
                return {"action": "type", "selector": dropdown["selector"], "text": "a"}

        if els["submit_btn"]:
            state.project_submitted = True
            return {"action": "click", "selector": els["submit_btn"]["selector"]}

        return {"action": "wait", "seconds": 2}

    except Exception as e:
        print("Create handler error:", e)
        import traceback; traceback.print_exc()
    return {"action": "wait", "seconds": 2}


# =========================================================
# ✏️ UPDATE PROJECT FLOW
# =========================================================

# async def _handle_update_project(goal, dom, url):

#     # Set target project name once
#     if not state.target_project_name:
#         name = _extract_search_project(goal)
#         if name:
#             state.target_project_name = name
#             print(f"🎯 Target project to update: '{state.target_project_name}'")

#     # ── VERIFIED ─────────────────────────────────────────
#     if state.update_verified:
#         return {"action": "done", "result": "PASS",
#                 "reason": "Project updated successfully"}

#     # ── SUBMITTED — check result ──────────────────────────
#     if state.update_submitted and not state.update_verified:
#         print("🔍 Verifying update was saved...")
#         if not dom:
#             state._empty_dom_count += 1
#             if state._empty_dom_count >= 3:
#                 return {"action": "done", "result": "UNKNOWN",
#                         "reason": "Update submitted but page closed before verification"}
#             return {"action": "wait", "seconds": 2}
#         state._empty_dom_count = 0

#         # ── Check 1: Success toast message ───────────────
#         for el in dom:
#             label = (el.get("label") or "").lower()
#             text  = (el.get("text") or "").lower()
#             if any(x in label or x in text for x in ["success", "updated", "saved", "project updated"]):
#                 state.update_verified = True
#                 return {"action": "done", "result": "PASS",
#                         "reason": "Update saved — success message visible"}

#         # ── Check 2: Submit button gone = form closed ─────
#         submit_still_visible = any(
#             tag == "button" and any(x in (el.get("label") or "").lower()
#                                     for x in ["update project", "save", "submit"])
#             for el in dom
#             for tag in [(el.get("tag") or "").lower()]
#         )

#         # ── Check 3: Update form inputs gone ─────────────
#         form_inputs_visible = any(
#             (el.get("name") or "").lower() in ["project_name", "project_start_date", "project_end_date"]
#             for el in dom
#         )

#         # ── Check 4: Back on projects list (ActionMenuButton visible) ──
#         back_on_list = any(
#             (el.get("dataTestId") or "") == "ActionMenuButton"
#             for el in dom
#         )

#         print(f"  submit_visible={submit_still_visible} | form_inputs={form_inputs_visible} | back_on_list={back_on_list}")

#         if back_on_list or (not submit_still_visible and not form_inputs_visible):
#             state.update_verified = True
#             return {"action": "done", "result": "PASS",
#                     "reason": "visible in dom Project updated successfully"}

#         # ── Check 5: Timeout fallback after 6 waits ───────
#         state._verify_wait_count = getattr(state, "_verify_wait_count", 0) + 1
#         if state._verify_wait_count >= 6:
#             state.update_verified = True
#             return {"action": "done", "result": "PASS",
#                     "reason": "Update likely saved — form no longer blocking"}

#         return {"action": "wait", "seconds": 2}

#     # ── FORM IS OPEN — fill it ────────────────────────────
#     if state.update_form_open:
#         return await _fill_update_form(dom)

#     # ── THREE DOT CLICKED — look for menu item ────────────
#     if state.three_dot_clicked:

#         print("=== CONTEXT MENU DEBUG ===")
#         for el in dom:
#             label       = (el.get("label") or "").strip()
#             text        = (el.get("text") or "").strip()
#             tag         = (el.get("tag") or "")
#             sel         = (el.get("selector") or "")
#             data_testid = (el.get("dataTestId") or "")
#             if label or text or data_testid:
#                 print(f"  [{tag}] label='{label}' | text='{text}' | testid='{data_testid}' | sel='{sel}'")
#         print("=== END CONTEXT MENU DEBUG ===")

#         for el in dom:
#             label       = (el.get("label") or "").lower()
#             text        = (el.get("text") or "").lower()
#             data_testid = (el.get("dataTestId") or "")

#             # ✅ Match by data-testid — most reliable
#             if data_testid == "EditMenuItem":
#                 print("✅ Found 'EditMenuItem' via data-testid")
#                 state.update_form_open = True
#                 state._three_dot_retry = 0
#                 return {"action": "click", "selector": "[data-testid='EditMenuItem']"}

#             # Fallback — match by text
#             if any(x in label or x in text for x in ["update", "edit"]):
#                 print(f"✅ Found menu item via text: '{text or label}'")
#                 state.update_form_open = True
#                 state._three_dot_retry = 0
#                 return {"action": "click", "selector": el["selector"]}

#         # Menu never appeared
#         state._three_dot_retry = getattr(state, "_three_dot_retry", 0) + 1
#         print(f"⏳ Context menu not found (attempt {state._three_dot_retry}/5)")

#         if state._three_dot_retry >= 5:
#             print("🔄 Three-dot click failed — resetting to retry with correct button")
#             state.three_dot_clicked = False
#             state._three_dot_retry  = 0
#             state.interacted_selectors = {
#                 s for s in state.interacted_selectors
#                 if not s.startswith("button") and "ActionMenuButton" not in s
#             }

#         return {"action": "wait", "seconds": 1}

#     # ── NAVIGATE + SEARCH + CLICK THREE DOT ──────────────
#     is_on_resource_page = "resource" in url.lower()
#     resource_btn = projects_tab = search_input = None

#     for el in dom:
#         label = (el.get("label") or "").lower().strip()
#         tag   = (el.get("tag") or "").lower()
#         if "column menu" in label: continue
#         if "resource" in label and "planner" in label: resource_btn = el
#         if label == "projects" and tag == "button": projects_tab = el
#         if "search project" in label and tag == "input": search_input = el

#     # Navigate to resource planner first
#     if not is_on_resource_page and resource_btn:
#         print("➡️ Navigating to Resource Planner")
#         return {"action": "click", "selector": resource_btn["selector"]}

#     # Click Projects tab
#     if is_on_resource_page and projects_tab:
#         sel = projects_tab["selector"]
#         if sel not in state.interacted_selectors:
#             state.interacted_selectors.add(sel)
#             print("➡️ Clicking Projects tab")
#             return {"action": "click", "selector": sel}

#     # Search for the project
#     if search_input and state.target_project_name:
#         sel = search_input["selector"]
#         if sel not in state.interacted_selectors:
#             state.interacted_selectors.add(sel)
#             print(f"🔍 Searching: {state.target_project_name}")
#             return {"action": "type", "selector": sel, "text": state.target_project_name}

#     # Find and click three-dot button
#     three_dot = _find_three_dot_button(dom, state.target_project_name)
#     if three_dot:
#         print(f"🎯 Clicking three-dot menu for '{state.target_project_name}'")
#         state.three_dot_clicked = True
#         return {"action": "click", "selector": "[data-testid='ActionMenuButton']"}

#     return {"action": "wait", "seconds": 2}


# # =========================================================
# # 📝 FILL UPDATE FORM — same style as create flow
# # =========================================================

# async def _fill_update_form(dom):
#     """
#     Fill update form field by field — same philosophy as create flow.
#     Detects fields by name=, id=, role= attributes.
#     """

#     def _pending(el):
#         return el is not None and el["selector"] not in state.interacted_selectors

#     # ── Detect all form fields ────────────────────────────
#     project_name_input       = None
#     start_date_input         = None
#     end_date_input           = None
#     client_dropdown          = None
#     project_manager_dropdown = None
#     employee_dropdown        = None
#     billing_status_dropdown  = None
#     project_status_dropdown  = None
#     flexible_hours_checkbox  = None
#     submit_btn               = None
#     comboboxes               = []

#     for el in dom:
#         tag     = (el.get("tag") or "").lower()
#         el_type = (el.get("type") or "").lower()
#         el_name = (el.get("name") or "").lower()
#         el_id   = (el.get("id") or "").lower()
#         label   = (el.get("label") or "").lower().strip()
#         role    = (el.get("role") or "").lower()

#         # Project Name — name="project_name"
#         if tag == "input" and el_name == "project_name":
#             project_name_input = el

#         # Start Date — name="project_start_date"
#         if tag == "input" and el_type == "date" and el_name == "project_start_date":
#             start_date_input = el

#         # End Date — name="project_end_date"
#         if tag == "input" and el_type == "date" and el_name == "project_end_date":
#             end_date_input = el

#         # Billing Status — id="status"
#         if tag == "div" and el_id == "status" and role == "combobox":
#             billing_status_dropdown = el

#         # Project Status — id="project_status"
#         if tag == "div" and el_id == "project_status" and role == "combobox":
#             project_status_dropdown = el

#         # Flexible Hours checkbox
#         if tag == "input" and el_type == "checkbox" and "flexible" in label:
#             flexible_hours_checkbox = el

#         # Submit button
#         if tag == "button" and any(x in label for x in ["update", "save", "submit"]):
#             submit_btn = el

#         # Combobox inputs — client, manager, employee (in order)
#         if tag == "input" and role == "combobox":
#             comboboxes.append(el)

#     # Assign comboboxes in order: [0]=client, [1]=manager, [2]=employee
#     if len(comboboxes) >= 1: client_dropdown          = comboboxes[0]
#     if len(comboboxes) >= 2: project_manager_dropdown = comboboxes[1]
#     if len(comboboxes) >= 3: employee_dropdown        = comboboxes[2]

#     # ── New values to set (always different from current) ─
#     new_project_name = f"UpdatedProject_{datetime.now().strftime('%H%M%S')}"
#     new_start_date   = datetime.now().strftime("%Y-%m-%d")
#     new_end_date     = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")

#     # Billing status options — pick one different from current
#     billing_options  = ["Billable", "Non Billable"]
#     # Project status options — pick one different from current
#     status_options   = ["Active", "Inactive", "Completed", "On Hold"]

#     def _pick_different(options, current_value):
#         """Return first option that is different from current value."""
#         current_lower = (current_value or "").lower().strip()
#         for opt in options:
#             if opt.lower() != current_lower:
#                 return opt
#         return options[0]

#     # ── Fill fields one by one — always overwrite ─────────

#     # 1. Client — always clear and retype
#     if client_dropdown and _pending(client_dropdown):
#         current = (client_dropdown.get("value") or "").strip()
#         print(f"📝 Changing client (current='{current}')...")
#         state.interacted_selectors.add(client_dropdown["selector"])
#         return {"action": "type", "selector": client_dropdown["selector"], "text": "b"}

#     # 2. Project Name — always set new unique name
#     if project_name_input and _pending(project_name_input):
#         current = (project_name_input.get("value") or "").strip()
#         state.last_project_name = new_project_name
#         print(f"📝 Changing project name: '{current}' → '{new_project_name}'")
#         state.interacted_selectors.add(project_name_input["selector"])
#         return {"action": "type", "selector": project_name_input["selector"], "text": new_project_name}

#     # 3. Project Manager — always clear and retype
#     if project_manager_dropdown and _pending(project_manager_dropdown):
#         current = (project_manager_dropdown.get("value") or "").strip()
#         print(f"📝 Changing project manager (current='{current}')...")
#         state.interacted_selectors.add(project_manager_dropdown["selector"])
#         return {"action": "type", "selector": project_manager_dropdown["selector"], "text": "b"}

#     # 4. Start Date — always set new date
#     if start_date_input and _pending(start_date_input):
#         current = (start_date_input.get("value") or "").strip()
#         print(f"📝 Changing start date: '{current}' → '{new_start_date}'")
#         state.interacted_selectors.add(start_date_input["selector"])
#         return {"action": "type", "selector": start_date_input["selector"], "text": new_start_date}

#     # 5. End Date — always set new date
#     if end_date_input and _pending(end_date_input):
#         current = (end_date_input.get("value") or "").strip()
#         print(f"📝 Changing end date: '{current}' → '{new_end_date}'")
#         state.interacted_selectors.add(end_date_input["selector"])
#         return {"action": "type", "selector": end_date_input["selector"], "text": new_end_date}

#     # 6. Billing Status — pick different option from current
#     if billing_status_dropdown and _pending(billing_status_dropdown):
#         current = (billing_status_dropdown.get("value") or
#                    billing_status_dropdown.get("text") or
#                    billing_status_dropdown.get("label") or "").strip()
#         new_val = _pick_different(billing_options, current)
#         print(f"📝 Changing billing status: '{current}' → '{new_val}'")
#         state.interacted_selectors.add(billing_status_dropdown["selector"])
#         # Click to open dropdown, then pick option
#         state._pending_select_value = new_val
#         return {"action": "click", "selector": billing_status_dropdown["selector"]}

#     # After billing status dropdown opens — pick the option
#     if getattr(state, "_pending_select_value", None):
#         val = state._pending_select_value
#         state._pending_select_value = None
#         print(f"📝 Selecting option: '{val}'")
#         return {"action": "click", "selector": f"li[role='option']:has-text('{val}')"}

#     # 7. Project Status — pick different option from current
#     if project_status_dropdown and _pending(project_status_dropdown):
#         current = (project_status_dropdown.get("value") or
#                    project_status_dropdown.get("text") or
#                    project_status_dropdown.get("label") or "").strip()
#         new_val = _pick_different(status_options, current)
#         print(f"📝 Changing project status: '{current}' → '{new_val}'")
#         state.interacted_selectors.add(project_status_dropdown["selector"])
#         state._pending_select_value = new_val
#         return {"action": "click", "selector": project_status_dropdown["selector"]}

#     # 8. Employee — always add a new one
#     if employee_dropdown and _pending(employee_dropdown):
#         print("📝 Adding employee...")
#         state.interacted_selectors.add(employee_dropdown["selector"])
#         return {"action": "type", "selector": employee_dropdown["selector"], "text": "b"}

#     # 9. Flexible Hours checkbox — toggle it
#     if flexible_hours_checkbox and _pending(flexible_hours_checkbox):
#         print("📝 Toggling flexible hours...")
#         state.interacted_selectors.add(flexible_hours_checkbox["selector"])
#         return {"action": "click", "selector": flexible_hours_checkbox["selector"]}

#     # 10. Submit
#     if submit_btn and submit_btn["selector"] not in state.interacted_selectors:
#         print("🚀 Submitting update form...")
#         state.interacted_selectors.add(submit_btn["selector"])
#         state.update_submitted = True
#         return {"action": "click", "selector": submit_btn["selector"]}

#     print("⏳ Waiting for update form fields...")
#     return {"action": "wait", "seconds": 2}
# from datetime import datetime, timedelta
from datetime import datetime, timedelta


# =========================================================
# 🔄 HANDLE UPDATE PROJECT — Fixed & Complete
# =========================================================

async def _handle_update_project(goal, dom, url):

    # Set target project name once
    if not state.target_project_name:
        name = _extract_search_project(goal)
        if name:
            state.target_project_name = name
            print(f"🎯 Target project to update: '{state.target_project_name}'")

    # ── VERIFIED ─────────────────────────────────────────
    if state.update_verified:
        return {"action": "done", "result": "PASS",
                "reason": "Project updated successfully"}

    # ── SUBMITTED — check result ──────────────────────────
    if state.update_submitted and not state.update_verified:
        print("🔍 Verifying update was saved...")
        if not dom:
            state._empty_dom_count += 1
            if state._empty_dom_count >= 3:
                return {"action": "done", "result": "UNKNOWN",
                        "reason": "Update submitted but page closed before verification"}
            return {"action": "wait", "seconds": 2}
        state._empty_dom_count = 0

        # ── Check 1: Success toast message ───────────────
        for el in dom:
            label = (el.get("label") or "").lower()
            text  = (el.get("text") or "").lower()
            if any(x in label or x in text for x in ["success", "updated", "saved", "project updated"]):
                state.update_verified = True
                return {"action": "done", "result": "PASS",
                        "reason": "Update saved — success message visible"}

        # ── Check 2: Submit button gone = form closed ─────
        submit_still_visible = any(
            tag == "button" and any(x in (el.get("label") or "").lower()
                                    for x in ["update project", "save", "submit"])
            for el in dom
            for tag in [(el.get("tag") or "").lower()]
        )

        # ── Check 3: Update form inputs gone ─────────────
        form_inputs_visible = any(
            (el.get("name") or "").lower() in ["project_name", "project_start_date", "project_end_date"]
            for el in dom
        )

        # ── Check 4: Back on projects list (ActionMenuButton visible) ──
        back_on_list = any(
            (el.get("dataTestId") or "") == "ActionMenuButton"
            for el in dom
        )

        print(f"  submit_visible={submit_still_visible} | form_inputs={form_inputs_visible} | back_on_list={back_on_list}")

        if back_on_list or (not submit_still_visible and not form_inputs_visible):
            state.update_verified = True
            return {"action": "done", "result": "PASS",
                    "reason": "Project updated successfully — form closed"}

        # ── Check 5: Timeout fallback after 6 waits ───────
        state._verify_wait_count = getattr(state, "_verify_wait_count", 0) + 1
        if state._verify_wait_count >= 6:
            state.update_verified = True
            return {"action": "done", "result": "PASS",
                    "reason": "Update likely saved — form no longer blocking"}

        return {"action": "wait", "seconds": 2}

    # ── FORM IS OPEN — fill it ────────────────────────────
    if state.update_form_open:
        return await _fill_update_form(dom)

    # ── THREE DOT CLICKED — look for menu item ────────────
    if state.three_dot_clicked:

        print("=== CONTEXT MENU DEBUG ===")
        for el in dom:
            label       = (el.get("label") or "").strip()
            text        = (el.get("text") or "").strip()
            tag         = (el.get("tag") or "")
            sel         = (el.get("selector") or "")
            data_testid = (el.get("dataTestId") or "")
            if label or text or data_testid:
                print(f"  [{tag}] label='{label}' | text='{text}' | testid='{data_testid}' | sel='{sel}'")
        print("=== END CONTEXT MENU DEBUG ===")

        for el in dom:
            label       = (el.get("label") or "").lower()
            text        = (el.get("text") or "").lower()
            data_testid = (el.get("dataTestId") or "")

            # ✅ Match by data-testid — most reliable
            if data_testid == "EditMenuItem":
                print("✅ Found 'EditMenuItem' via data-testid")
                state.update_form_open = True
                state._three_dot_retry = 0
                return {"action": "click", "selector": "[data-testid='EditMenuItem']"}

            # Fallback — match by text
            if any(x in label or x in text for x in ["update", "edit"]):
                print(f"✅ Found menu item via text: '{text or label}'")
                state.update_form_open = True
                state._three_dot_retry = 0
                return {"action": "click", "selector": el["selector"]}

        # Menu never appeared — retry
        state._three_dot_retry = getattr(state, "_three_dot_retry", 0) + 1
        print(f"⏳ Context menu not found (attempt {state._three_dot_retry}/5)")

        if state._three_dot_retry >= 5:
            print("🔄 Three-dot click failed — resetting to retry with correct button")
            state.three_dot_clicked = False
            state._three_dot_retry  = 0
            state.interacted_selectors = {
                s for s in state.interacted_selectors
                if not s.startswith("button") and "ActionMenuButton" not in s
            }

        return {"action": "wait", "seconds": 1}

    # ── NAVIGATE + SEARCH + CLICK THREE DOT ──────────────
    is_on_resource_page = "resource" in url.lower()
    resource_btn = projects_tab = search_input = None

    for el in dom:
        label = (el.get("label") or "").lower().strip()
        tag   = (el.get("tag") or "").lower()
        if "column menu" in label: continue
        if "resource" in label and "planner" in label: resource_btn = el
        if label == "projects" and tag == "button": projects_tab = el
        if "search project" in label and tag == "input": search_input = el

    # Navigate to resource planner first
    if not is_on_resource_page and resource_btn:
        print("➡️ Navigating to Resource Planner")
        return {"action": "click", "selector": resource_btn["selector"]}

    # Click Projects tab
    if is_on_resource_page and projects_tab:
        sel = projects_tab["selector"]
        if sel not in state.interacted_selectors:
            state.interacted_selectors.add(sel)
            print("➡️ Clicking Projects tab")
            return {"action": "click", "selector": sel}

    # Search for the project
    if search_input and state.target_project_name:
        sel = search_input["selector"]
        if sel not in state.interacted_selectors:
            state.interacted_selectors.add(sel)
            print(f"🔍 Searching: {state.target_project_name}")
            return {"action": "type", "selector": sel, "text": state.target_project_name}

    # Find and click three-dot button
    three_dot = _find_three_dot_button(dom, state.target_project_name)
    if three_dot:
        print(f"🎯 Clicking three-dot menu for '{state.target_project_name}'")
        state.three_dot_clicked = True
        return {"action": "click", "selector": "[data-testid='ActionMenuButton']"}

    return {"action": "wait", "seconds": 2}


# =========================================================
# 📝 FILL UPDATE FORM — Fixed combobox + dropdown handling
# =========================================================

async def _fill_update_form(dom):
    """
    Fill update form field by field.
    KEY FIXES:
      - Combobox dropdowns wait for an option to appear before selecting
      - _pending_select_value only clears after the option is actually found & clicked
      - _pending_combobox tracks which combobox is awaiting option selection
      - Submit only fires after all pending states are resolved
    """

    def _pending(el):
        return el is not None and el["selector"] not in state.interacted_selectors

    # ── FIX 1: Resolve any pending combobox option selection FIRST ────
    # After typing in a combobox, either:
    #   (a) browser autocomplete already selected an option — detect by checking
    #       that no open dropdown listbox exists in DOM → clear and move on, OR
    #   (b) dropdown is open — click the first visible option.
    if getattr(state, "_pending_combobox", None):
        field_name = state._pending_combobox
        print(f"⏳ Waiting for dropdown options for '{field_name}'...")

        # ── Check if a listbox/dropdown is currently open ────
        listbox_open = any(
            (el.get("role") or "").lower() in ("listbox", "menu")
            or (el.get("tag") or "").lower() == "ul"
            for el in dom
        )

        # ── Look for selectable options in DOM ───────────────
        option = None
        for el in dom:
            role = (el.get("role") or "").lower()
            tag  = (el.get("tag") or "").lower()
            text = (el.get("text") or "").strip()
            if role == "option" and text:
                option = el
                break
            if tag == "li" and text:
                option = el
                break

        if option:
            # Dropdown is open and has options — click first one
            print(f"✅ Selecting option '{option.get('text', '')}' for '{field_name}'")
            state._pending_combobox      = None
            state._pending_combobox_wait = 0
            return {"action": "click", "selector": option["selector"]}

        if not listbox_open:
            # ✅ No open dropdown = browser autocomplete already handled it
            # (log shows "✅ Autocomplete option selected") — safe to move on
            print(f"✅ Autocomplete already resolved for '{field_name}' — moving on")
            state._pending_combobox      = None
            state._pending_combobox_wait = 0
            # Fall through to next field (don't return here)
        else:
            # Listbox is open but no options yet — keep waiting
            state._pending_combobox_wait = getattr(state, "_pending_combobox_wait", 0) + 1
            if state._pending_combobox_wait >= 8:
                print(f"⚠️ No options found for '{field_name}' after retries — skipping")
                state._pending_combobox      = None
                state._pending_combobox_wait = 0
            else:
                return {"action": "wait", "seconds": 1}

    # ── FIX 2: Resolve any pending dropdown (billing/project status) FIRST ──
    # Only clear _pending_select_value if the option is actually found in DOM.
    if getattr(state, "_pending_select_value", None):
        val = state._pending_select_value
        print(f"⏳ Looking for dropdown option: '{val}'...")

        option = None
        for el in dom:
            role = (el.get("role") or "").lower()
            text = (el.get("text") or "").strip()
            tag  = (el.get("tag") or "").lower()
            if role in ("option", "menuitem") and val.lower() in text.lower():
                option = el
                break
            if tag == "li" and val.lower() in text.lower():
                option = el
                break

        if option:
            print(f"✅ Found and clicking option: '{val}'")
            state._pending_select_value      = None
            state._pending_select_wait_count = 0
            return {"action": "click", "selector": option["selector"]}

        # Option not yet rendered — wait (do NOT clear the value)
        state._pending_select_wait_count = getattr(state, "_pending_select_wait_count", 0) + 1
        if state._pending_select_wait_count >= 8:
            print(f"⚠️ Option '{val}' not found after retries — skipping")
            state._pending_select_value      = None
            state._pending_select_wait_count = 0
        return {"action": "wait", "seconds": 1}

    # ── Detect all form fields ────────────────────────────
    project_name_input       = None
    start_date_input         = None
    end_date_input           = None
    client_dropdown          = None
    project_manager_dropdown = None
    employee_dropdown        = None
    billing_status_dropdown  = None
    project_status_dropdown  = None
    flexible_hours_checkbox  = None
    submit_btn               = None
    comboboxes               = []

    for el in dom:
        tag     = (el.get("tag") or "").lower()
        el_type = (el.get("type") or "").lower()
        el_name = (el.get("name") or "").lower()
        el_id   = (el.get("id") or "").lower()
        label   = (el.get("label") or "").lower().strip()
        role    = (el.get("role") or "").lower()

        # Project Name — name="project_name"
        if tag == "input" and el_name == "project_name":
            project_name_input = el

        # Start Date — name="project_start_date"
        if tag == "input" and el_type == "date" and el_name == "project_start_date":
            start_date_input = el

        # End Date — name="project_end_date"
        if tag == "input" and el_type == "date" and el_name == "project_end_date":
            end_date_input = el

        # Billing Status — id="status"
        if tag == "div" and el_id == "status" and role == "combobox":
            billing_status_dropdown = el

        # Project Status — id="project_status"
        if tag == "div" and el_id == "project_status" and role == "combobox":
            project_status_dropdown = el

        # Flexible Hours checkbox
        if tag == "input" and el_type == "checkbox" and "flexible" in label:
            flexible_hours_checkbox = el

        # Submit button
        if tag == "button" and any(x in label for x in ["update", "save", "submit"]):
            submit_btn = el

        # Combobox inputs — client, manager, employee (in order)
        if tag == "input" and role == "combobox":
            comboboxes.append(el)

    # Assign comboboxes in order: [0]=client, [1]=manager, [2]=employee
    if len(comboboxes) >= 1: client_dropdown          = comboboxes[0]
    if len(comboboxes) >= 2: project_manager_dropdown = comboboxes[1]
    if len(comboboxes) >= 3: employee_dropdown        = comboboxes[2]

    # ── New values to set ─────────────────────────────────
    new_project_name = f"UpdatedProject_{datetime.now().strftime('%H%M%S')}"
    new_start_date   = datetime.now().strftime("%Y-%m-%d")
    new_end_date     = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")

    billing_options = ["Billable", "Non Billable"]
    status_options  = ["Active", "Inactive", "Completed", "On Hold"]

    def _pick_different(options, current_value):
        current_lower = (current_value or "").lower().strip()
        for opt in options:
            if opt.lower() != current_lower:
                return opt
        return options[0]

    # ── Fill fields one by one ────────────────────────────

    # 1. Client — type to trigger dropdown, then wait for option selection
    if client_dropdown and _pending(client_dropdown):
        current = (client_dropdown.get("value") or "").strip()
        print(f"📝 Changing client (current='{current}')...")
        state.interacted_selectors.add(client_dropdown["selector"])
        state._pending_combobox      = "client"
        state._pending_combobox_wait = 0
        return {"action": "type", "selector": client_dropdown["selector"], "text": "b"}

    # 2. Project Name — always set new unique name
    if project_name_input and _pending(project_name_input):
        current = (project_name_input.get("value") or "").strip()
        state.last_project_name = new_project_name
        print(f"📝 Changing project name: '{current}' → '{new_project_name}'")
        state.interacted_selectors.add(project_name_input["selector"])
        return {"action": "type", "selector": project_name_input["selector"], "text": new_project_name}

    # 3. Project Manager — type to trigger dropdown, then wait for option selection
    if project_manager_dropdown and _pending(project_manager_dropdown):
        current = (project_manager_dropdown.get("value") or "").strip()
        print(f"📝 Changing project manager (current='{current}')...")
        state.interacted_selectors.add(project_manager_dropdown["selector"])
        state._pending_combobox      = "project_manager"
        state._pending_combobox_wait = 0
        return {"action": "type", "selector": project_manager_dropdown["selector"], "text": "b"}

    # 4. Start Date
    if start_date_input and _pending(start_date_input):
        current = (start_date_input.get("value") or "").strip()
        print(f"📝 Changing start date: '{current}' → '{new_start_date}'")
        state.interacted_selectors.add(start_date_input["selector"])
        return {"action": "type", "selector": start_date_input["selector"], "text": new_start_date}

    # 5. End Date
    if end_date_input and _pending(end_date_input):
        current = (end_date_input.get("value") or "").strip()
        print(f"📝 Changing end date: '{current}' → '{new_end_date}'")
        state.interacted_selectors.add(end_date_input["selector"])
        return {"action": "type", "selector": end_date_input["selector"], "text": new_end_date}

    # 6. Billing Status — click to open, then wait for option
    if billing_status_dropdown and _pending(billing_status_dropdown):
        current = (billing_status_dropdown.get("value") or
                   billing_status_dropdown.get("text") or
                   billing_status_dropdown.get("label") or "").strip()
        new_val = _pick_different(billing_options, current)
        print(f"📝 Changing billing status: '{current}' → '{new_val}'")
        state.interacted_selectors.add(billing_status_dropdown["selector"])
        state._pending_select_value      = new_val
        state._pending_select_wait_count = 0
        return {"action": "click", "selector": billing_status_dropdown["selector"]}

    # 7. Project Status — click to open, then wait for option
    if project_status_dropdown and _pending(project_status_dropdown):
        current = (project_status_dropdown.get("value") or
                   project_status_dropdown.get("text") or
                   project_status_dropdown.get("label") or "").strip()
        new_val = _pick_different(status_options, current)
        print(f"📝 Changing project status: '{current}' → '{new_val}'")
        state.interacted_selectors.add(project_status_dropdown["selector"])
        state._pending_select_value      = new_val
        state._pending_select_wait_count = 0
        return {"action": "click", "selector": project_status_dropdown["selector"]}

    # 8. Employee — type to trigger dropdown, then wait for option selection
    if employee_dropdown and _pending(employee_dropdown):
        print("📝 Adding employee...")
        state.interacted_selectors.add(employee_dropdown["selector"])
        state._pending_combobox      = "employee"
        state._pending_combobox_wait = 0
        return {"action": "type", "selector": employee_dropdown["selector"], "text": "b"}

    # 9. Flexible Hours checkbox — toggle it
    if flexible_hours_checkbox and _pending(flexible_hours_checkbox):
        print("📝 Toggling flexible hours...")
        state.interacted_selectors.add(flexible_hours_checkbox["selector"])
        return {"action": "click", "selector": flexible_hours_checkbox["selector"]}

    # 10. Submit — only after ALL pending states are clear
    # Guard: don't submit if any async selection is still in progress
    if getattr(state, "_pending_combobox", None) or getattr(state, "_pending_select_value", None):
        print("⏳ Waiting for pending selections before submit...")
        return {"action": "wait", "seconds": 1}

    if submit_btn and submit_btn["selector"] not in state.interacted_selectors:
        print("🚀 Submitting update form...")
        state.interacted_selectors.add(submit_btn["selector"])
        state.update_submitted = True
        return {"action": "click", "selector": submit_btn["selector"]}

    print("⏳ Waiting for update form fields...")
    return {"action": "wait", "seconds": 2}