

async def extract_live_dom(page):
    try:
        await page.wait_for_load_state("networkidle", timeout=7000)
    except:
        pass

    # Force render hidden/drawer fields
    try:
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(500)
    except:
        pass

    for attempt in range(3):
        try:
            elements = await page.evaluate("""
            () => {
                const selector = "button, a, input, select, textarea, [role='button'], [role='link'], [role='option'], [role='row'], [role='cell'], [role='gridcell'], [role='menuitem'], td, th, span[data-id]";
                const nodes = document.querySelectorAll(selector);
                const results = [];

                for (let i = 0; i < nodes.length && results.length < 300; i++) {
                    const el = nodes[i];

                    if (
                        el.disabled ||
                        el.getAttribute("aria-hidden") === "true"
                    ) continue;

                    const tag         = el.tagName.toLowerCase();
                    const elId        = el.id || "";
                    const roleAttr    = el.getAttribute("role") || "";
                    const type        = el.getAttribute("type") || "";
                    const value       = el.value || el.getAttribute("value") || el.defaultValue || "";
                    const placeholder = el.getAttribute("placeholder") || "";
                    const nameAttr    = el.getAttribute("name") || "";
                    const ariaLabel   = el.getAttribute("aria-label") || "";
                    const text        = (el.innerText || "").trim().slice(0, 200);
                    const dataId      = el.getAttribute("data-id") || "";
                    const dataTestId  = el.getAttribute("data-testid") || "";

                    const label =
                        ariaLabel ||
                        placeholder ||
                        nameAttr ||
                        text ||
                        roleAttr ||
                        value ||
                        "";

                    // ── Build selector ──────────────────────────────
                    let selectorPath = "";

                    if (dataTestId) {
                        // ✅ Most reliable — use data-testid
                        selectorPath = `[data-testid='${dataTestId}']`;
                    } else if (elId) {
                        selectorPath = "#" + CSS.escape(elId);
                    } else if (ariaLabel) {
                        selectorPath = `${tag}[aria-label='${CSS.escape(ariaLabel)}']`;
                    } else if (nameAttr) {
                        selectorPath = `${tag}[name='${CSS.escape(nameAttr)}']`;
                    } else if (text && text.length < 50) {
                        const safeText = text.replace(/'/g, "\\'");
                        selectorPath = `${tag}:has-text('${safeText}')`;
                    } else {
                        selectorPath = tag;
                    }

                    results.push({
                        tag,
                        id:          elId,
                        type,
                        label,
                        text,
                        selector:    selectorPath,
                        value,
                        dataId,
                        dataTestId,
                        name:        nameAttr,
                        role:        roleAttr,
                        class:       el.className
                    });
                }

                return results;
            }
            """)

            print(f"✅ Extracted {len(elements)} DOM elements")
            return elements

        except Exception as e:
            print(f"⚠️ DOM extraction failed (attempt {attempt + 1}):", e)
            try:
                await page.wait_for_load_state("load", timeout=5000)
            except:
                pass

    print("❌ DOM extraction failed after 3 attempts.")
    return []