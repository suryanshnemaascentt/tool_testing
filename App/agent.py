

import asyncio
from playwright.async_api import async_playwright
from dom_builder import extract_live_dom
from llm_planner import decide_action, reset_state
from executor import execute_step
from test_reporter import TestReporter

MAX_STEPS = 60


# =========================================================
# 🔍 Page alive checker
# =========================================================
async def is_page_alive(page):
    try:
        await page.title()
        return True
    except:
        return False


async def run(url, goal, email=None, password=None, test_mode=False):
    reporter = TestReporter(goal=goal, url=url) if test_mode else None
    reset_state()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto(url)

        if reporter:
            reporter.start()

        for step_num in range(MAX_STEPS):
            print(f"\n===== STEP {step_num + 1} =====")

            if not await is_page_alive(page):
                print("❌ Browser/page was closed. Stopping agent.")
                if reporter:
                    reporter.finish(result="FAIL", reason="Browser was closed unexpectedly")
                    reporter.save_report()
                    reporter.print_summary()
                break

            print("Current URL:", page.url)

            try:
                await page.wait_for_load_state("domcontentloaded", timeout=5000)
            except:
                pass

            dom = await extract_live_dom(page)
            action = await decide_action(goal, dom, page.url, email, password)
            print("🤖 ACTION:", action)

            if reporter:
                reporter.log_step(step_num + 1, action, page.url)

            if action.get("action") == "done":
                result = action.get("result", "UNKNOWN")
                reason = action.get("reason", "")
                icon = "✅" if result == "PASS" else ("⚠️" if result == "UNKNOWN" else "❌")
                print(f"\n{icon} Goal completed — {result}")
                if reason:
                    print(f"   Reason: {reason}")
                if reporter:
                    reporter.finish(result=result, reason=reason)
                    reporter.save_report()
                    reporter.print_summary()
                break

            success = await execute_step(page, dom, action)

            if reporter:
                reporter.update_last_step(success=success)

        else:
            print("\n❌ Max steps reached without completing goal")
            if reporter:
                reporter.finish(result="FAIL", reason="Max steps reached")
                reporter.save_report()
                reporter.print_summary()

        try:
            await browser.close()
        except:
            pass


# =========================================================
# 💬 CLI Input — User se lo
# =========================================================

def get_inputs():
    print("\n" + "=" * 55)
    print("   🤖  Automation Tool")
    print("=" * 55)

    # Credentials
    print("\n📌 Login Details")
    url      = "https://grid.ds.ascentt.ai/login"
    if not url:
        url = "https://grid.ds.ascentt.ai/login"
    email    = "suryansh.nema@ascentt.com"
    password = "**************"

    # Task
    print("\n📌 Task")
    print("   1 → Create Project  (auto name + dates)")
    print("   2 → Update Project  (give project name)")
    choice = input("   Choose (1/2) : ").strip()

    if choice == "2":
        task           = "update"
        search_project = input("   Project Name to Update : ").strip()
        goal           = f"login and update project {search_project}"
    else:
        task           = "create"
        search_project = ""
        goal           = "login and create project"

    # Summary
    print("\n" + "=" * 55)
    print(f"  Task    : {task.upper()}")
    print(f"  URL     : {url}")
    print(f"  Email   : {email}")
    if task == "update":
        print(f"  Project : {search_project}")
    print("=" * 55 + "\n")

    return url, email, password, goal


if __name__ == "__main__":
    url, email, password, goal = get_inputs()
    asyncio.run(run(url, goal, email=email, password=password, test_mode=True))