# llm_planner.py
# Fully Deterministic Planner (No LLM)

from datetime import datetime, timedelta

INTERACTED_SELECTORS = set()



# =========================================================
# 🚀 ENTRY FUNCTION
# =========================================================

async def decide_action(goal, dom, url, email=None, password=None):
    return await decide_action_with_failed_indices(
        goal, dom, url, email, password
    )


# =========================================================
# 🧠 MAIN DECISION FUNCTION
# =========================================================

async def decide_action_with_failed_indices(
    goal,
    dom,
    url,
    email=None,
    password=None
):

    # =========================================================
    # 🔐 LOGIN HANDLER
    # =========================================================
    try:
        email_input = None
        password_input = None
        next_button = None
        sign_in_button = None
        yes_button = None

        for el in dom:
            print(f"this is el: {el}")
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

    except Exception as e:
        print("Login handler error:", e)

    # =========================================================
    # 📁 PROJECT CREATION HANDLER
    # =========================================================

    is_create_project = any(
        keyword in goal.lower()
        for keyword in ["create project", "add project", "new project"]
    )

    if not is_create_project:
        return {"action": "wait", "seconds": 2}

    try:
        # -----------------------------------------------------
        # 🔍 Detect Elements
        # -----------------------------------------------------

        resource_planner_btn = None
        projects_tab = None
        add_project_btn = None

        project_name_input = None
        start_date_input = None
        end_date_input = None
        project_category_dropdown = None
        client_dropdown = None
        project_lead_dropdown = None
        project_manager_dropdown = None
        employee_dropdown = None
        submit_btn = None

        for el in dom:
            label = (el.get("label") or "").lower()
            tag = (el.get("tag") or "").lower()
            el_type = el.get("type")

            if "column menu" in label:
                continue

            # Navigation
            
            if "resource" in label and "planner" in label:
                resource_planner_btn = el

            if label == "projects" and tag == "button":
                projects_tab = el

            if ("add project" in label or "create project" in label) and tag == "button":
                add_project_btn = el

            # Form Fields
            if tag == "input" and "project" in label and "name" in label:
                project_name_input = el

            if tag == "input" and el_type == "date" and "start" in label:
                start_date_input = el

            if tag == "input" and el_type == "date" and "end" in label:
                end_date_input = el

            if tag == "input" and "category" in label:
                project_category_dropdown = el

            if tag == "input" and "client" in label:
                client_dropdown = el

            if tag == "input" and "lead" in label:
                project_lead_dropdown = el

            if tag == "input" and "manager" in label:
                project_manager_dropdown = el

            if tag == "input" and "employee" in label:
                employee_dropdown = el

            if tag == "button" and "create new project" in label:
                submit_btn = el

        # -----------------------------------------------------
        # 🔥 Combobox Fallback Mapping
        # -----------------------------------------------------

        comboboxes = [
            el for el in dom
            if el.get("tag") == "input"
            and (el.get("label") or "").lower() == "combobox"
        ]

        if comboboxes:
            if not client_dropdown and len(comboboxes) >= 1:
                client_dropdown = comboboxes[0]
            if not project_lead_dropdown and len(comboboxes) >= 2:
                project_lead_dropdown = comboboxes[1]
            if not project_manager_dropdown and len(comboboxes) >= 3:
                project_manager_dropdown = comboboxes[2]
            if not employee_dropdown and len(comboboxes) >= 4:
                employee_dropdown = comboboxes[3]

        # -----------------------------------------------------
        # 🚀 Navigation Flow
        # ----------------------------------------------------
        is_on_resource_page = "resource" in url.lower()
        

            # If form not opened yet, open it
        if add_project_btn and not project_name_input:
                return {"action": "click", "selector": add_project_btn["selector"]}

    
        if resource_planner_btn and not is_on_resource_page:
            return {"action": "click", "selector": resource_planner_btn["selector"]}

        if projects_tab and is_on_resource_page and not add_project_btn:
            return {"action": "click", "selector": projects_tab["selector"]}

        if add_project_btn and not project_name_input:
            {"action": "click", "selector": add_project_btn["selector"]}
    

        # -----------------------------------------------------
        # 📝 Fill Form
        # -----------------------------------------------------

        if project_name_input and project_name_input["selector"] not in INTERACTED_SELECTORS:
            INTERACTED_SELECTORS.add(project_name_input["selector"])
            return {
                "action": "type",
                "selector": project_name_input["selector"],
                "text": f"AutoProject_{datetime.now().strftime('%H%M%S')}"
            }

        if start_date_input and start_date_input["selector"] not in INTERACTED_SELECTORS:
            INTERACTED_SELECTORS.add(start_date_input["selector"])
            return {
                "action": "type",
                "selector": start_date_input["selector"],
                "text": datetime.now().strftime("%Y-%m-%d")
            }

        if end_date_input and end_date_input["selector"] not in INTERACTED_SELECTORS:
            INTERACTED_SELECTORS.add(end_date_input["selector"])
            return {
                "action": "type",
                "selector": end_date_input["selector"],
                "text": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
            }

        # Dropdowns (single interaction each)
        for dropdown in [
            project_category_dropdown,
            client_dropdown,
            project_lead_dropdown,
            project_manager_dropdown,
        ]:
            if dropdown and dropdown["selector"] not in INTERACTED_SELECTORS:
                INTERACTED_SELECTORS.add(dropdown["selector"])
                return {
                    "action": "type",
                    "selector": dropdown["selector"],
                    "text": "a"
                }

        # -----------------------------------------------------
        # 👥 EMPLOYEE MULTI SELECT (ONLY 1)
        # -----------------------------------------------------

        # -----------------------------------------------------
# 👥 EMPLOYEE MULTI SELECT (Fixed)
# -----------------------------------------------------

        if employee_dropdown and employee_dropdown["selector"] not in INTERACTED_SELECTORS:
            INTERACTED_SELECTORS.add(employee_dropdown["selector"])
            return {
                "action": "type",
                "selector": employee_dropdown["selector"],
                "text": "a"
            }


        # -----------------------------------------------------
        # ✅ Submit
        # -----------------------------------------------------

        if submit_btn:
            return {"action": "click", "selector": submit_btn["selector"]}
        print(submit_btn, add_project_btn)
  
    except Exception as e:
        print("Project handler error:", e)

    return {"action": "wait", "seconds": 2}
