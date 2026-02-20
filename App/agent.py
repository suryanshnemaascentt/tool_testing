# # agent.py

# import asyncio
# from playwright.async_api import async_playwright
# from dom_builder import extract_live_dom
# from llm_planner import decide_action
# from executor import execute_step


# async def run(url, goal):

#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=False)
#         page = await browser.new_page()

#         await page.goto(url)

#         for step_num in range(20):

#             print(f"\n===== STEP {step_num+1} =====")
#             print("Current URL:", page.url)

#             dom = await extract_live_dom(page)

#             action = await decide_action(goal, dom, page.url)
#             print("🤖 ACTION:", action)

#             if action.get("action") == "done":
#                 print("✅ Goal completed")
#                 break

#             await execute_step(page, dom, action)

#         await browser.close()


# # agent.py

# import asyncio
# from playwright.async_api import async_playwright
# from dom_builder import extract_live_dom
# from llm_planner import decide_action
# from executor import execute_step


# async def run(url, goal):

#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=False)
#         page = await browser.new_page()

#         await page.goto(url)

#         for step_num in range(20):

#             print(f"\n===== STEP {step_num+1} =====")
#             print("Current URL:", page.url)

#             dom = await extract_live_dom(page)

#             action = await decide_action(goal, dom, page.url)
#             print("🤖 ACTION:", action)

#             if action.get("action") == "done":
#                 print("✅ Goal completed")
#                 break

#             await execute_step(page, dom, action)

#         await browser.close()


# if __name__ == "__main__":
#     url = "https://grid.ds.ascentt.ai/login"
#     goal = "Login using email suryansh.nema@ascentt.com and password Sn94948988@"

#     asyncio.run(run(url, goal))
# agent.py

import asyncio
from playwright.async_api import async_playwright
from dom_builder import extract_live_dom
from llm_planner import decide_action
from executor import execute_step


async def run(url, goal, email=None, password=None):

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto(url)

        for step_num in range(30):

            print(f"\n===== STEP {step_num+1} =====")
            print("Current URL:", page.url)
            try:
                await page.wait_for_load_state("domcontentloaded", timeout=5000)
            except:
                pass

            dom = await extract_live_dom(page)

            # 🔥 Pass email and password to decision maker
            action = await decide_action(goal, dom, page.url, email, password)
            print("🤖 ACTION:", action)

            if action.get("action") == "done":
                print("✅ Goal completed")
                break

            await execute_step(page, dom, action)

        await browser.close()


if __name__ == "__main__":
    # 🔥 Take input dynamically
    url ="https://grid.ds.ascentt.ai/login"
    goal = "login and create project"
    email = "suryansh.nema@ascentt.com"
    password = "Sn94948988@"

    asyncio.run(run(url, goal, email, password))

