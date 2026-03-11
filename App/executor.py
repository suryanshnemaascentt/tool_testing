
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










































