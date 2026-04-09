import re
import nbformat
from nbformat.v4 import new_markdown_cell
from pathlib import Path
from uuid import uuid4

import os
import re
import yaml
import nbformat
from nbformat.v4 import new_markdown_cell
from pathlib import Path
from uuid import uuid4
import subprocess

# =========================================================
# Determine base repo URL for JupyterLite
# =========================================================
github_repository = os.environ.get('GITHUB_REPOSITORY', '')


PY_BLOCK_RE = re.compile(r"```python_code_block\s*\n(.*?)```", re.DOTALL)

# Global loader cell with all necessary CSS, JS, and initialization
GLOBAL_LOADER_SOURCE = (
    "<!-- ==================== GLOBAL LOADER: PYODIDE + CODEMIRROR ==================== -->\n"
    "<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/codemirror@5.65.16/lib/codemirror.min.css'>\n"
    "<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/codemirror@5.65.16/theme/eclipse.min.css'>\n"
    "<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/codemirror@5.65.16/theme/material.min.css'>\n"
    "<script src='https://cdn.jsdelivr.net/npm/codemirror@5.65.16/lib/codemirror.min.js'></script>\n"
    "<script src='https://cdn.jsdelivr.net/npm/codemirror@5.65.16/mode/python/python.min.js'></script>\n"
    "\n"
    "<style>\n"
    ".py-cell {border:1px solid var(--pst-color-border,#ccc);border-radius:6px;margin:16px 0;background:var(--pst-color-surface,#fff);box-shadow:0 1px 3px rgba(0,0,0,0.08);overflow:hidden;}\n"
    ".CodeMirror {border-radius:4px;font-family:monospace;font-size:14px;line-height:1.5;height:auto;background:var(--pst-color-background,#f9f9f9);overflow-y:auto;}\n"
    ".CodeMirror-scroll {max-height:432px;}\n"
    "[data-theme='dark'] .CodeMirror,html[data-mode='dark'] .CodeMirror {background:#1e1e1e!important;color:#d4d4d4!important;}\n"
    "[data-theme='dark'] .CodeMirror-gutters,html[data-mode='dark'] .CodeMirror-gutters {background:#1e1e1e!important;border-right:1px solid #3e3e3e!important;}\n"
    "[data-theme='dark'] .CodeMirror-linenumber,html[data-mode='dark'] .CodeMirror-linenumber {color:#858585!important;}\n"
    ".py-run,.py-clear{padding:6px 12px;background:var(--pst-color-surface,#fff);color:var(--pst-color-text,#000);border:1px solid var(--pst-color-border,#ccc);border-radius:4px;cursor:pointer;font-size:13px;margin-right:8px;transition:all .3s;}\n"
    ".py-run:hover,.py-clear:hover{background:var(--pst-color-primary,#2196f3);color:#fff;border-color:var(--pst-color-primary,#2196f3);}\n"
    ".py-out{white-space:pre-wrap;word-wrap:break-word;font-family:monospace;font-size:13px;line-height:1.6;overflow-y:auto;padding:8px;background:var(--pst-color-background,#f5f5f5);border-radius:4px;margin:8px 0;color:var(--pst-color-text,#000);}\n"
    "[data-theme='dark'] .py-out,html[data-mode='dark'] .py-out,[data-theme='dark'] .py-cell .py-out,html[data-mode='dark'] .py-cell .py-out{background:#1e1e1e !important;color:#d4d4d4 !important;}\n"
    "[data-theme='dark'] .py-cell,html[data-mode='dark'] .py-cell,[data-theme='dark'] .py-cell,html[data-mode='dark'] .py-cell{background:#252525 !important;border-color:#3e3e3e !important;}\n"
    "[data-theme='dark'] .py-run,html[data-mode='dark'] .py-run,[data-theme='dark'] .py-clear,html[data-mode='dark'] .py-clear,[data-theme='dark'] .py-cell .py-run,html[data-mode='dark'] .py-cell .py-run,[data-theme='dark'] .py-cell .py-clear,html[data-mode='dark'] .py-cell .py-clear{background:#252525 !important;color:#d4d4d4 !important;border-color:#3e3e3e !important;}\n"
    ".resize-handle{height:14px;background:repeating-linear-gradient(90deg,var(--pst-color-border,#aaa),var(--pst-color-border,#aaa) 2px,transparent 2px,transparent 5px);cursor:ns-resize;border-radius:4px;margin:4px 0;touch-action:none;}\n"
    ".resize-handle.dragging{background:var(--pst-color-primary,#2196f3);}\n"
    "</style>\n"
    "\n"
    "<div style='margin-bottom:10px;padding:10px;background:var(--pst-color-background,#f7f7f7);border-left:3px solid var(--pst-color-primary,#2196f3);border-radius:4px;'>\n"
    "  <button id='restart-pyodide' style='padding:6px 14px;background:#d32f2f;color:white;border:none;border-radius:3px;cursor:pointer;font-size:13px;'>🔄 Restart Kernel</button>\n"
    "  <span id='kernel-status' style='margin-left:12px;font-size:13px;'>⏳ Loading Pyodide…</span>\n"
    "</div>\n"
    "\n"
    "<script>\n"
    "(function(){\n"
    "  if(window.pyodideLoaderInitialized)return;\n"
    "  window.pyodideLoaderInitialized=true;\n"
    "\n"
    "  // ---------- Load Pyodide ----------\n"
    "  window.loadPyodideOnce=async function(){\n"
    "    if(window.pyodideReadyPromise)return window.pyodideReadyPromise;\n"
    "    window.pyodideReadyPromise=(async()=>{\n"
    "      const s=document.createElement('script');s.src='https://cdn.jsdelivr.net/pyodide/v0.23.4/full/pyodide.js';document.head.appendChild(s);\n"
    "      await new Promise(r=>s.onload=r);\n"
    "      const py=await loadPyodide({indexURL:'https://cdn.jsdelivr.net/pyodide/v0.23.4/full/'});\n"
    "      window.pyodide=py;const st=document.getElementById('kernel-status');if(st){st.textContent='✅ Pyodide ready';st.style.color='var(--pst-color-primary,#2196f3)';}\n"
    "      return py;\n"
    "    })();return window.pyodideReadyPromise;};window.loadPyodideOnce();\n"
    "\n"
    "  // ---------- Restart Kernel ----------\n"
    "  document.addEventListener('DOMContentLoaded',()=>{\n"
    "    const b=document.getElementById('restart-pyodide');const s=document.getElementById('kernel-status');\n"
    "    if(!b||!s)return;\n"
    "    b.addEventListener('click',async()=>{s.textContent='🔄 Restarting kernel...';s.style.color='orange';b.disabled=true;delete window.pyodide;window.pyodideReadyPromise=null;await window.loadPyodideOnce();s.textContent='✅ Kernel restarted';s.style.color='var(--pst-color-primary,#2196f3)';b.disabled=false;});\n"
    "  });\n"
    "\n"
    "  // ---------- Resize Handler ----------\n"
    "  window.initResizeHandle=function(h,el,minH=80){if(!h||!el)return;let y0,h0;const sd=y=>{y0=y;h0=el.offsetHeight;h.classList.add('dragging');document.body.style.userSelect='none';};const mv=y=>{el.style.height=Math.max(minH,h0+(y-y0))+'px';};const sp=()=>{h.classList.remove('dragging');document.body.style.userSelect='';};h.addEventListener('mousedown',e=>{sd(e.clientY);document.onmousemove=e=>mv(e.clientY);document.onmouseup=()=>{document.onmousemove=null;sp();};});h.addEventListener('touchstart',e=>{const t=e.touches[0];sd(t.clientY);document.ontouchmove=e=>mv(e.touches[0].clientY);document.ontouchend=()=>{document.ontouchmove=null;sp();};});};\n"
    "\n"
    "  // ---------- Initialize CodeMirror ----------\n"
    "  const getTheme=()=>{const el=document.documentElement;return (el.getAttribute('data-theme')||el.dataset.mode||'light')==='dark'?'material':'eclipse';};\n"
    "  window.enableCodeMirrorEditors=function(){\n"
    "    document.querySelectorAll('.py-cell').forEach(cell=>{\n"
    "      const t=cell.querySelector('.py-code');\n"
    "      if(!t||t._cm)return;\n"
    "      const encodedCode=cell.getAttribute('data-code');\n"
    "      if(encodedCode){try{const binary=atob(encodedCode);const bytes=Uint8Array.from(binary,c=>c.charCodeAt(0));t.value=new TextDecoder('utf-8').decode(bytes);}catch(e){console.error('Failed to decode code:',e);}}\n"
    "      const ed=CodeMirror.fromTextArea(t,{mode:'python',theme:getTheme(),lineNumbers:true,indentUnit:4,smartIndent:true,lineWrapping:true,viewportMargin:Infinity});t._cm=ed;\n"
    "      const setHeight=()=>{const lines=ed.lineCount();const maxH=Math.min(lines,12)*24;ed.setSize(null,maxH);};\n"
    "      setHeight();ed.on('change',setHeight);\n"
    "    });\n"
    "  };\n"
    "  // Watch for theme changes and update CodeMirror instances\n"
    "  const observer=new MutationObserver(()=>{const theme=getTheme();document.querySelectorAll('.CodeMirror').forEach(cm=>{if(cm.CodeMirror)cm.CodeMirror.setOption('theme',theme);});});\n"
    "  observer.observe(document.documentElement,{attributes:true,attributeFilter:['data-theme','data-mode']});\n"
    "})();\n"
    "</script>"
)

# Cell initialization script (placed after all cells)
CELL_INIT_SOURCE = (
    "\n<script>\n"
    "if(!window.pyodideCellsInitialized){\n"
    "window.pyodideCellsInitialized=true;\n"
    "setTimeout(()=>{\n"
    "  document.querySelectorAll('.py-out').forEach(out=>{out.style.cssText+='white-space:pre-wrap !important;word-wrap:break-word !important;';});\n"
    "  if(typeof window.enableCodeMirrorEditors==='function')window.enableCodeMirrorEditors();\n"
    "  document.querySelectorAll('.py-cell').forEach(cell=>{\n"
    "    if(cell.dataset.init)return;cell.dataset.init='1';\n"
    "    const ta=cell.querySelector('.py-code');const cm=ta._cm;const out=cell.querySelector('.py-out');const run=cell.querySelector('.py-run');const clr=cell.querySelector('.py-clear');const wrap=cell.querySelector('.output-wrapper');\n"
    "    if(!run||!out)return;\n"
    "    out.style.cssText += 'white-space:pre-wrap !important;word-wrap:break-word !important;font-family:monospace !important;font-size:13px !important;line-height:1.6 !important;';\n"
    "    run.addEventListener('click',async()=>{\n"
    "      run.disabled=true;out.textContent='';out.style.color='';wrap.style.display='block';\n"
    "      const debugEnabled = typeof window !== 'undefined' && window.location && window.location.search && window.location.search.indexOf('pydebug=1')!==-1;\n"
    "      let debugEl=null; if(debugEnabled){debugEl=document.createElement('pre');debugEl.style.background='#111';debugEl.style.color='#ddd';debugEl.style.padding='8px';debugEl.style.marginTop='8px';debugEl.style.fontSize='12px';out.parentNode.appendChild(debugEl);}\n"
    "      try{\n"
    "        const py=await window.loadPyodideOnce();let output='';\n"
    "        const addOutput=(s)=>{\n"
    "          try{\n"
    "            // Decode incoming chunk robustly (handles Uint8Array / ArrayBuffer)\n"
    "            let chunk = '';\n"
    "            if(s instanceof Uint8Array || s instanceof ArrayBuffer){\n"
    "              const bytes = s instanceof Uint8Array ? s : new Uint8Array(s);\n"
    "              chunk = new TextDecoder('utf-8').decode(bytes);\n"
    "            } else if(typeof s === 'object' && s !== null){\n"
    "              chunk = String(s);\n"
    "            } else {\n"
    "              chunk = String(s);\n"
    "            }\n"
    "\n"
    "            // Insert a newline between chunks when the previous chunk did not\n"
    "            // end with one and the current one does not start with one. This\n"
    "            // prevents multiple print() calls from being concatenated on a\n"
    "            // single line (e.g. \"28102442810244\").\n"
    "            if(typeof addOutput._lastEnded === 'undefined') addOutput._lastEnded = true;\n"
    "            if(!addOutput._lastEnded && chunk.length > 0 && !chunk.startsWith('\\n')){\n"
    "              output += '\\n';\n"
    "            }\n"
    "\n"
    "            output += chunk;\n"
    "            addOutput._lastEnded = chunk.endsWith('\\n');\n"
    "          }catch(e){\n"
    "            output += String(s);\n"
    "          }\n"
    "          out.textContent = output;\n"
    "          if(typeof debugEl!=='undefined' && debugEl){try{debugEl.textContent += JSON.stringify(s)+'\\n';}catch(e){} }\n"
    "          console.debug('pyodide-output-chunk', s);\n"
    "        };\n"
    "        // Register both write and batched handlers to be robust across pyodide versions\n"
    "        py.setStdout({write:addOutput, batched:addOutput, flush:()=>{}});\n"
    "        py.setStderr({write:(s)=>{addOutput(s);out.style.color='#c62828';}, batched:(s)=>{addOutput(s);out.style.color='#c62828';}, flush:()=>{}});\n"
    "        await py.runPythonAsync(cm?cm.getValue():ta.value);\n"
    "        if(output.trim() === ''){ out.textContent = '(no stdout captured — check browser console)'; out.style.color = '#777'; }\n"
    "        if(out.style.color!=='#c62828')out.style.color='';\n"
    "      }catch(e){\n"
    "        out.textContent = e.toString();out.style.color='#c62828';console.error('pyodide-exec-error', e);\n"
    "      }\n"
    "      run.disabled=false;\n"
    "    });\n"
    "    clr.addEventListener('click',()=>{out.textContent='';wrap.style.display='none';});\n"
    "    const r1=cell.querySelector('.cell-resize');const r2=cell.querySelector('.output-resize');if(window.initResizeHandle){if(r1)window.initResizeHandle(r1,cell.querySelector('.CodeMirror'));if(r2)window.initResizeHandle(r2,out);}\n"
    "  });\n"
    "},800);\n"
    "}\n"
    "</script>"
)


def has_loader(cell):
    """Check if cell contains the Pyodide loader"""
    if cell.cell_type != "markdown":
        return False
    source = cell.source if isinstance(cell.source, str) else "".join(cell.source)
    return "GLOBAL LOADER: PYODIDE" in source or "pyodideLoaderInitialized" in source


def has_init_script(cell):
    """Check if cell contains the init script"""
    if cell.cell_type != "markdown":
        return False
    source = cell.source if isinstance(cell.source, str) else "".join(cell.source)
    return "pyodideCellsInitialized" in source


def has_py_cell(cell):
    """Check if cell contains a py-cell div"""
    if cell.cell_type != "markdown":
        return False
    source = cell.source if isinstance(cell.source, str) else "".join(cell.source)
    return "class='py-cell'" in source or 'class="py-cell"' in source


def notebook_has_python_code_block(nb):
    """Return True if the notebook contains at least one python_code_block markdown fenced block."""
    return any(
        PY_BLOCK_RE.search(cell.source if isinstance(cell.source, str) else "".join(cell.source))
        for cell in nb.cells
        if cell.cell_type == "markdown"
    )


def build_py_cell(code: str, idx: int):
    """Build an interactive Python cell with proper escaping"""
    import html
    import base64
    
    # Use base64 encoding to completely bypass markdown rendering
    # This ensures the code is never touched by the markdown processor
    code_bytes = code.rstrip().encode('utf-8')
    encoded_code = base64.b64encode(code_bytes).decode('ascii')
    
    cell = new_markdown_cell(
        f"<div class='py-cell' data-code='{encoded_code}'>\n"
        f"  <textarea class='py-code'></textarea>\n"
        f"  <div class='resize-handle cell-resize'></div>\n"
        f"  <div>\n"
        f"    <button class='py-run'>▶ Run</button>\n"
        f"    <button class='py-clear'>Clear</button>\n"
        f"    <span class='run-status'></span>\n"
        f"  </div>\n"
        f"  <div class='output-wrapper' style='display:none;'>\n"
        f"    <pre class='py-out' style='height:100px;overflow-y:auto;'></pre>\n"
        f"    <div class='resize-handle output-resize'></div>\n"
        f"  </div>\n"
        f"</div>"
    )
    cell["id"] = f"pycell-{uuid4().hex[:8]}"
    cell["metadata"] = {}
    return cell


def inject(input_nb: Path, output_nb: Path):
    """Convert markdown Python code blocks to interactive Pyodide cells"""
    nb = nbformat.read(input_nb, as_version=4)
    
    # Check if notebook already has loader/cells
    already_has_loader = any(has_loader(cell) for cell in nb.cells)
    already_has_py_cells = any(has_py_cell(cell) for cell in nb.cells)
    already_has_init = any(has_init_script(cell) for cell in nb.cells)
    
    if already_has_loader and already_has_py_cells:
        print(f"⚠️  Notebook already has Pyodide cells - skipping conversion")
        print(f"   Loader: {'✓' if already_has_loader else '✗'}")
        print(f"   Py-cells: {'✓' if already_has_py_cells else '✗'}")
        print(f"   Init script: {'✓' if already_has_init else '✗'}")
        
        # Just clean up duplicate loaders and ensure proper structure
        new_cells = []
        loader_added = False
        init_added = False
        
        for cell in nb.cells:
            # Skip duplicate loaders
            if has_loader(cell):
                if not loader_added:
                    # Keep only the first loader
                    cell["id"] = f"pyodide-loader-{uuid4().hex[:8]}"
                    new_cells.append(cell)
                    loader_added = True
                continue
            
            # Skip duplicate init scripts
            if has_init_script(cell):
                if not init_added:
                    cell["id"] = f"pyodide-init-{uuid4().hex[:8]}"
                    init_added = True
                # Move to end
                continue
            
            new_cells.append(cell)
        
        # Add init script at end if we have py-cells
        if already_has_py_cells and not init_added:
            init_cell = new_markdown_cell(CELL_INIT_SOURCE)
            init_cell["id"] = f"pyodide-init-{uuid4().hex[:8]}"
            init_cell["metadata"] = {}
            new_cells.append(init_cell)
        
        nb.cells = new_cells
        nbformat.write(nb, output_nb)
        print(f"✅ Cleaned up {input_nb} -> {output_nb}")
        return
    
    # Convert Python code blocks
    new_cells = []
    loader_inserted = False
    cell_counter = 1
    converted_cells = 0

    for cell in nb.cells:
        # Skip existing loader cells
        if has_loader(cell) or has_init_script(cell):
            continue
            
        # Insert GLOBAL LOADER after first heading
        if (
            not loader_inserted
            and cell.cell_type == "markdown"
            and cell.source.lstrip().startswith("#")
        ):
            new_cells.append(cell)
            loader_cell = new_markdown_cell(GLOBAL_LOADER_SOURCE)
            loader_cell["id"] = f"pyodide-loader-{uuid4().hex[:8]}"
            loader_cell["metadata"] = {}
            new_cells.append(loader_cell)
            loader_inserted = True
            continue

        if cell.cell_type != "markdown":
            new_cells.append(cell)
            continue

        text = cell.source if isinstance(cell.source, str) else "".join(cell.source)
        matches = list(PY_BLOCK_RE.finditer(text))

        if not matches:
            new_cells.append(cell)
            continue

        # Found Python code blocks
        last = 0
        for m in matches:
            before = text[last:m.start()]
            code = m.group(1)

            if before.strip():
                preserved = new_markdown_cell(before)
                preserved["id"] = f"md-{uuid4().hex[:8]}"
                preserved["metadata"] = {}
                new_cells.append(preserved)

            new_cells.append(build_py_cell(code, cell_counter))
            converted_cells += 1
            cell_counter += 1
            last = m.end()

        after = text[last:]
        if after.strip():
            tail = new_markdown_cell(after)
            tail["id"] = f"md-{uuid4().hex[:8]}"
            tail["metadata"] = {}
            new_cells.append(tail)

    # Add cell initialization script at the end if we converted any cells
    if converted_cells > 0:
        init_cell = new_markdown_cell(CELL_INIT_SOURCE)
        init_cell["id"] = f"pyodide-init-{uuid4().hex[:8]}"
        init_cell["metadata"] = {}
        new_cells.append(init_cell)

    # Only update if we made changes
    if converted_cells > 0 or len(new_cells) != len(nb.cells):
        nb.cells = new_cells
        
        # Clean up notebook metadata
        nb.metadata = {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.11"
            }
        }
        
        nbformat.write(nb, output_nb)
        print(f"✅ Converted {input_nb} -> {output_nb}")
        print(f"   Generated {converted_cells} interactive Python cells")
    else:
        print(f"ℹ️  No Python code blocks found in {input_nb}")



if github_repository:
    username, repo_name = github_repository.split('/')
    base_url = f"https://{username.lower()}.github.io/{repo_name}"
    print(f"📦 Repository: {github_repository}")
else:
    try:
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'],
                                capture_output=True, text=True, check=True)
        remote_url = result.stdout.strip()
        if 'github.com' in remote_url:
            if remote_url.startswith('git@'):
                repo_part = remote_url.split(':')[1].replace('.git', '')
            else:
                repo_part = remote_url.split('github.com/')[1].replace('.git', '')
            username, repo_name = repo_part.split('/')
            base_url = f"https://{username.lower()}.github.io/{repo_name}"
        else:
            raise Exception("Not a GitHub repository")
    except Exception:
        print("❌ Could not determine repository URL. Please set GITHUB_REPOSITORY environment variable.")
        exit(1)

jupyterlite_url = f"{base_url}/jupyterlite/lab/index.html"
print(f"🌐 Base URL: {base_url}")
print(f"🚀 JupyterLite URL: {jupyterlite_url}")

# =========================================================
# TOC and notebooks path setup
# =========================================================
toc_path = "notebooks/_toc.yml"
notebooks_dir = "notebooks"

with open(toc_path, "r", encoding="utf-8") as f:
    toc_data = yaml.safe_load(f)

toc_files = []

def extract_files(entries):
    for item in entries:
        if isinstance(item, dict):
            if "file" in item:
                toc_files.append(os.path.basename(item["file"]))
            if "sections" in item:
                extract_files(item["sections"])
        elif isinstance(item, list):
            extract_files(item)

if "chapters" in toc_data:
    extract_files(toc_data["chapters"])
elif "parts" in toc_data:
    for part in toc_data["parts"]:
        if "chapters" in part:
            extract_files(part["chapters"])

valid_notebooks = []
for name in toc_files:
    no_ext, _ = os.path.splitext(name)
    ipynb_path = os.path.join(notebooks_dir, no_ext + ".ipynb")
    if os.path.exists(ipynb_path):
        valid_notebooks.append(no_ext)

print(f"📚 Valid notebooks from TOC: {valid_notebooks}")
# =========================================================
# Run injection for all valid notebooks from TOC
# =========================================================
print("\n🚀 Starting Pyodide conversion for TOC notebooks...")
for nb_name in valid_notebooks:
    nb_path = Path(notebooks_dir) / f"{nb_name}.ipynb"
    nb = nbformat.read(nb_path, as_version=4)
    if not notebook_has_python_code_block(nb):
        print(f"⏭ Skipping {nb_path}: no python_code_block markdown tag found.")
        continue
    inject(nb_path, nb_path)

print("\n✅ All TOC notebooks processed successfully.")