# # async def extract_live_dom(page):
# #     """Optimized DOM extraction with reduced waiting and better performance."""
# #     # Minimal wait for DOM content
# #     try:
# #         await page.wait_for_load_state("domcontentloaded", timeout=5000)
# #     except:
# #         pass  # Continue even if wait fails
    
# #     # Optimized JavaScript evaluation with early filtering
# #     elements = await page.evaluate("""
# #     () => {
# #         // Early exit if no elements found
# #         const selector = "button, a, input, select, textarea, [role='button'], [role='link']";
# #         const nodes = document.querySelectorAll(selector);
        
# #         if (nodes.length === 0) return [];
        
# #         const results = [];
# #         let index = 0;
        
# #         // Process nodes with early filtering
# #         for (let i = 0; i < nodes.length && results.length < 30; i++) {
# #             const el = nodes[i];
            
# #             // Skip invisible or disabled elements early
# #             if (el.disabled || el.offsetParent === null) continue;
            
# #             const tag = el.tagName.toLowerCase();
# #             const role = el.getAttribute("role");
# #             const type = el.getAttribute("type");
# #             const value = el.value || el.getAttribute("value");
# #             const placeholder = el.getAttribute("placeholder");
# #             const name = el.getAttribute("name");
# #             const text = el.innerText || "";
            
# #             // Create label with priority order
# #             const label = text.trim() || placeholder || value || name || role || "";
            
# #             results.push({
# #                 index: index++,
# #                 playwright_index: i,
# #                 tag: tag,
# #                 type: type,
# #                 role: role,
# #                 label: label,
# #                 value: value
# #             });
# #         }
        
# #         return results;
# #     }
# #     """)
    
# #     if elements:
# #         print(f"✅ Extracted {len(elements)} DOM elements")
# #     else:
# #         print("⚠️ No DOM elements found")
    
# #     return elements



# async def extract_live_dom(page):
#     try:
#         await page.wait_for_load_state("domcontentloaded", timeout=5000)
#     except:
#         pass

#     elements = await page.evaluate("""
#     () => {
#         const selector = "button, a, input, select, textarea, [role='button'], [role='link']";
#         const nodes = document.querySelectorAll(selector);

#         if (nodes.length === 0) return [];

#         const results = [];

#         for (let i = 0; i < nodes.length && results.length < 40; i++) {
#             const el = nodes[i];

#             if (el.disabled || el.offsetParent === null) continue;

#             const tag = el.tagName.toLowerCase();
#             const id = el.id || "";
#             const role = el.getAttribute("role") || "";
#             const type = el.getAttribute("type") || "";
#             const value = el.value || "";
#             const placeholder = el.getAttribute("placeholder") || "";
#             const name = el.getAttribute("name") || "";
#             const ariaLabel = el.getAttribute("aria-label") || "";
#             const text = el.innerText || "";

#             const label =
#                 text.trim() ||
#                 placeholder ||
#                 ariaLabel ||
#                 name ||
#                 value ||
#                 role ||
#                 "";

#             // Build stable selector
#             let selectorPath = "";
#             if (id) {
#                 selectorPath = "#" + id;
#             } else if (name) {
#                 selectorPath = tag + "[name='" + name + "']";
#             } else {
#                 selectorPath = tag + ":nth-of-type(" + (i + 1) + ")";
#             }

#             results.push({
#                 tag: tag,
#                 id: id,
#                 role: role,
#                 type: type,
#                 label: label,
#                 selector: selectorPath
#             });
#         }

#         return results;
#     }
#     """)

#     if elements:
#         print(f"✅ Extracted {len(elements)} DOM elements")
#     else:
#         print("⚠️ No DOM elements found")

#     return elements
# dom_builder.py
async def extract_live_dom(page):
    try:
        await page.wait_for_load_state("networkidle", timeout=7000)
    except:
        pass

    # 🔥 VERY IMPORTANT — force render hidden/drawer fields
    try:
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(500)
    except:
        pass

    for attempt in range(3):
        try:
            elements = await page.evaluate("""
            () => {
                const selector = "button, a, input, select, textarea, [role='button'], [role='link']";
                const nodes = document.querySelectorAll(selector);

                const results = [];

                for (let i = 0; i < nodes.length && results.length < 200; i++) {

                    const el = nodes[i];

                    if (
                        el.disabled ||
                        el.getAttribute("aria-hidden") === "true"
                    ) continue;

                    const tag = el.tagName.toLowerCase();
                    const id = el.id || "";
                    const role = el.getAttribute("role") || "";
                    const type = el.getAttribute("type") || "";
                    const value = el.value || el.getAttribute("value") || el.defaultValue || "";
                    const placeholder = el.getAttribute("placeholder") || "";
                    const name = el.getAttribute("name") || "";
                    const ariaLabel = el.getAttribute("aria-label") || "";
                    const text = (el.innerText || "").trim();

                    // 🔥 Better label priority
                    const label =
                        ariaLabel ||
                        placeholder ||
                        name ||
                        text ||
                        role ||
                        value ||
                        "";

                    let selectorPath = "";

                    if (id) {
                        selectorPath = "#" + CSS.escape(id);
                    }
                    else if (ariaLabel) {
                        selectorPath = tag + "[aria-label='" + CSS.escape(ariaLabel) + "']";
                    }
                    else if (name) {
                        selectorPath = tag + "[name='" + CSS.escape(name) + "']";
                    }
                    else if (text && text.length < 50) {
                        const safeText = text.replace(/'/g, "\\'");
                        selectorPath = tag + ":has-text('" + safeText + "')";
                    }
                    else {
                        selectorPath = tag;
                    }

                    results.push({
                        tag: tag,
                        id: id,
                        type: type,
                        label: label,
                        selector: selectorPath,
                        value: value,
                        class: el.className
                    });
                }

                return results;
            }
            """)

            print("DOM CONTENT:", elements)
            print(f"✅ Extracted {len(elements)} DOM elements")
            return elements

        except Exception as e:
            print(f"⚠️ DOM extraction failed (attempt {attempt+1}):", e)
            try:
                await page.wait_for_load_state("load", timeout=5000)
            except:
                pass

    print("❌ DOM extraction failed after 3 attempts.")
    return []
