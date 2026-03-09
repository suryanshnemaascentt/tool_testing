# async def execute_step(page, dom, step):

#     index = step.get("index")
#     action = step.get("action")
#     value = step.get("text") or step.get("value")

#     if index is None or index >= len(dom):
#         return False

#     element = dom[index]

#     try:
#         # Get all matching elements on the page
#         locator = page.locator(
#             "input, button, select, textarea, a, [role='button'], [role='link']"
#         )

#         # Use the playwright_index to select the correct element
#         playwright_index = element.get("playwright_index", index)
#         target_locator = locator.nth(playwright_index)

#         if action == "click":
#             await target_locator.click()

#         elif action == "type":
#             await target_locator.fill(value or "")
#             await target_locator.press("Tab")   # 🔥 trigger blur
#             await page.wait_for_timeout(500)    # 🔥 allow DOM update


#         elif action == "wait":
#             await page.wait_for_timeout(step.get("seconds", 2) * 1000)

#         elif action == "done":
#             return True

#         else:
#             return False

#         await page.wait_for_timeout(500)
#         return True

#     except Exception as e:
#         print("Executor error:", e)
#         return False


# async def execute_step(page, dom, step):

#     index = step.get("index")
#     action = step.get("action")
#     value = step.get("text") or step.get("value")

#     if index is None or index >= len(dom):
#         return False

#     element = dom[index]

#     try:
#         locator = page.locator(
#             "input, button, select, textarea, a, [role='button'], [role='link']"
#         )

#         playwright_index = element.get("playwright_index", index)
#         target_locator = locator.nth(playwright_index)

#         if action == "click":
#             await target_locator.click()

#         elif action == "type":
#             await target_locator.fill(value or "")
#             await target_locator.press("Tab")
#             await page.wait_for_timeout(300)

#         elif action == "wait":
#             await page.wait_for_timeout(step.get("seconds", 2) * 1000)

#         elif action == "done":
#             return True

#         else:
#             return False

#         return True

#     except Exception as e:
#         print("Executor error:", e)
#         return False
# async def execute_step(page, dom, step):

#     action = step.get("action")
#     selector = step.get("selector")
#     value = step.get("text") or step.get("value")

#     if not action:
#         return False

#     try:
#         # WAIT ACTION
#         if action == "wait":
#             await page.wait_for_timeout(step.get("seconds", 2) * 1000)
#             return True

#         # DONE ACTION
#         if action == "done":
#             return True

#         # For click & type, selector is required
#         if not selector:
#             print("❌ No selector provided")
#             return False

#         target_locator = page.locator(selector)

#         # Ensure element exists
#         await target_locator.wait_for(state="visible", timeout=5000)

#         if action == "click":
#             await target_locator.click()

#         elif action == "type":
#             await target_locator.fill(value or "")
#             await page.wait_for_timeout(300)

#         else:
#             return False

#         return True

#     except Exception as e:
#         print("Executor error:", e)
#         return False

# -------------------------------------------first solution--------------------------------------------
# executor.py
# async def execute_step(page, dom, step):

#     action = step.get("action")
#     selector = step.get("selector")
#     value = step.get("text") or step.get("value")

#     try:
#         if action == "wait":
#             seconds = step.get("seconds", 2)
#             print(f"⏳ Waiting {seconds} seconds...")
#             await page.wait_for_timeout(seconds * 1000)
#             return True

#         if action == "done":
#             print("✅ Goal completed!")
#             return True

#         if not selector:
#             print("❌ No selector provided")
#             return False

#         print(f"\n🔍 Executing action: {action}")
#         print(f"   Selector: {selector}")

#         locator = page.locator(selector)

#         count = await locator.count()
#         print(f"   Found {count} matching element(s)")
#         if count == 0:
#             print("❌ Element not found")
#             return False

#         element = locator.first

#         await element.scroll_into_view_if_needed()
#         await page.wait_for_timeout(200)

#         # =========================================================
#         # CLICK
#         # =========================================================
#         if action == "click":
#             try:
#                 await element.click(timeout=4000)
#                 print("   ✅ Click successful!")
#                 await page.wait_for_timeout(500)
#                 return True
#             except Exception as e:
#                 print(f"❌ Click failed: {e}")
#                 try:
#                     await element.click(force=True)
#                     print("   🔥 Force click successful!")
#                     await page.wait_for_timeout(500)
#                     return True
#                 except Exception as e2:
#                     print(f"❌ Force click failed: {e2}")
#                     return False

#         # =========================================================
#         # TYPE
#         # =========================================================
#         elif action == "type":
#             try:
#                 print(f"   ⌨️ Typing value: {value}")

#                 # Clear existing value
#                 await element.fill("")
#                 await page.wait_for_timeout(200)

#                 # Fill new value (works for text + date)
#                 await element.fill(value or "")
#                 print("   ✅ Value filled")

#                 await page.wait_for_timeout(500)

#                 # 🔥 Handle MUI autocomplete dropdown
#                 try:
#                     await page.wait_for_selector("ul[role='listbox']", timeout=1500)

#                     option = page.locator("li[role='option']").first
#                     if await option.count() > 0:
#                         await option.click()
#                         print("   ✅ Clicked first dropdown option")

#                 except:
#                     pass

#                 await page.wait_for_timeout(500)
#                 return True

#             except Exception as e:
#                 print(f"❌ Type failed: {e}")
#                 return False

#         # =========================================================
#         # SELECT (for real <select>)
#         # =========================================================
#         elif action == "select":
#             try:
#                 await element.select_option(value)
#                 print("   ✅ Select successful!")
#                 await page.wait_for_timeout(500)
#                 return True
#             except Exception as e:
#                 print(f"❌ Select failed: {e}")
#                 return False

#         else:
#             print(f"❌ Unknown action: {action}")
#             return False

#     except Exception as e:
#         print(f"❌ Executor error: {e}")
#         import traceback
#         traceback.print_exc()
#         return False



async def execute_step(page, dom, step):
    action   = step.get("action")
    selector = step.get("selector")
    value    = step.get("text") or step.get("value")

    try:
        # ── WAIT ──────────────────────────────────────────────────
        if action == "wait":
            seconds = step.get("seconds", 2)
            print(f"⏳ Waiting {seconds}s...")
            await page.wait_for_timeout(seconds * 1000)
            return True

        # ── DONE ──────────────────────────────────────────────────
        if action == "done":
            return True

        if not selector:
            print("❌ No selector provided")
            return False

        print(f"\n🔍 Action : {action}")
        print(f"   Selector: {selector}")

        locator = page.locator(selector)
        count   = await locator.count()
        print(f"   Found {count} element(s)")

        if count == 0:
            print("❌ Element not found")
            return False

        element = locator.first
        await element.scroll_into_view_if_needed()
        await page.wait_for_timeout(200)

        # ── CLICK ─────────────────────────────────────────────────
        if action == "click":
            try:
                await element.click(timeout=4000)
                print("   ✅ Click OK")
                await page.wait_for_timeout(500)
                return True
            except Exception as e:
                print(f"   ⚠️  Normal click failed: {e} — trying force click")
                try:
                    await element.click(force=True)
                    print("   ✅ Force click OK")
                    await page.wait_for_timeout(500)
                    return True
                except Exception as e2:
                    print(f"   ❌ Force click failed: {e2}")
                    return False

        # ── TYPE ──────────────────────────────────────────────────
        elif action == "type":
            try:
                print(f"   ⌨️  Typing: {value!r}")
                await element.fill("")
                await page.wait_for_timeout(200)
                await element.fill(value or "")
                print("   ✅ Fill OK")
                await page.wait_for_timeout(500)

                # Handle MUI / autocomplete dropdown
                try:
                    await page.wait_for_selector("ul[role='listbox']", timeout=1500)
                    option = page.locator("li[role='option']").first
                    if await option.count() > 0:
                        await option.click()
                        print("   ✅ Autocomplete option selected")
                except:
                    pass

                await page.wait_for_timeout(500)
                return True

            except Exception as e:
                print(f"   ❌ Type failed: {e}")
                return False

        # ── SELECT ────────────────────────────────────────────────
        elif action == "select":
            try:
                await element.select_option(value)
                print("   ✅ Select OK")
                await page.wait_for_timeout(500)
                return True
            except Exception as e:
                print(f"   ❌ Select failed: {e}")
                return False

        else:
            print(f"   ❌ Unknown action: {action}")
            return False

    except Exception as e:
        print(f"❌ Executor error: {e}")
        import traceback
        traceback.print_exc()
        return False