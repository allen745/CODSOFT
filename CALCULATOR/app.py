import streamlit as st
import math
import json
from datetime import datetime

st.set_page_config(
    page_title="CalcPro | Calculator",
    page_icon="🧮",
    layout="centered"
)

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .calc-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 1.5rem;
        color: white;
    }
    .calc-header h1 { font-size: 2rem; margin: 0; color: white; }
    .calc-header p  { margin: 0.3rem 0 0; opacity: 0.7; color: white; font-size: 0.9rem; }

    .display-box {
        background: #1a1a2e;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid #0f3460;
    }
    .display-expr {
        font-size: 0.85rem;
        color: #888;
        min-height: 20px;
        font-family: monospace;
        text-align: right;
    }
    .display-result {
        font-size: 2.5rem;
        font-weight: 700;
        color: #e94560;
        text-align: right;
        font-family: monospace;
        word-break: break-all;
    }
    .history-item {
        background: #1a1a2e;
        border-radius: 8px;
        padding: 8px 12px;
        margin-bottom: 6px;
        border-left: 3px solid #e94560;
        font-family: monospace;
        font-size: 0.85rem;
        color: #ccc;
    }
    .history-item span { color: #e94560; font-weight: 600; float: right; }
    .mode-info {
        background: #0f3460;
        border-radius: 8px;
        padding: 8px 12px;
        margin-bottom: 12px;
        font-size: 0.8rem;
        color: #aaa;
        text-align: center;
    }
    div[data-testid="stButton"] > button {
        width: 100%;
        border-radius: 10px;
        font-size: 1rem;
        font-weight: 600;
        padding: 0.6rem;
        transition: all 0.15s;
    }
</style>
""", unsafe_allow_html=True)

# ─── Session State ────────────────────────────────────────────────────────────
if "display"  not in st.session_state: st.session_state.display  = "0"
if "expr"     not in st.session_state: st.session_state.expr     = ""
if "history"  not in st.session_state: st.session_state.history  = []
if "new_num"  not in st.session_state: st.session_state.new_num  = True
if "mode"     not in st.session_state: st.session_state.mode     = "Basic"
if "memory"   not in st.session_state: st.session_state.memory   = 0.0
if "last_ans" not in st.session_state: st.session_state.last_ans = 0.0

# ─── Helper Functions ─────────────────────────────────────────────────────────
def press_num(n):
    if st.session_state.new_num:
        st.session_state.display = str(n)
        st.session_state.new_num = False
    else:
        if st.session_state.display == "0":
            st.session_state.display = str(n)
        else:
            st.session_state.display += str(n)

def press_dot():
    if st.session_state.new_num:
        st.session_state.display = "0."
        st.session_state.new_num = False
    elif "." not in st.session_state.display:
        st.session_state.display += "."

def press_op(op):
    st.session_state.expr += st.session_state.display + f" {op} "
    st.session_state.new_num = True

def press_equals():
    try:
        full_expr = st.session_state.expr + st.session_state.display
        result = eval(full_expr, {"__builtins__": {}}, {})
        result = round(float(result), 10)
        if result == int(result):
            result_str = str(int(result))
        else:
            result_str = str(result)
        st.session_state.history.insert(0, {
            "expr": full_expr,
            "result": result_str,
            "time": datetime.now().strftime("%H:%M:%S")
        })
        if len(st.session_state.history) > 10:
            st.session_state.history = st.session_state.history[:10]
        st.session_state.last_ans = float(result)
        st.session_state.display = result_str
        st.session_state.expr = ""
        st.session_state.new_num = True
    except:
        st.session_state.display = "Error"
        st.session_state.expr = ""
        st.session_state.new_num = True

def press_clear():
    st.session_state.display = "0"
    st.session_state.expr    = ""
    st.session_state.new_num = True

def press_backspace():
    if len(st.session_state.display) > 1:
        st.session_state.display = st.session_state.display[:-1]
    else:
        st.session_state.display = "0"

def press_sign():
    try:
        val = float(st.session_state.display)
        st.session_state.display = str(-val) if val != 0 else "0"
    except:
        pass

def press_percent():
    try:
        val = float(st.session_state.display)
        st.session_state.display = str(val / 100)
    except:
        pass

def sci_func(fn):
    try:
        val = float(st.session_state.display)
        if   fn == "sin":   result = math.sin(math.radians(val))
        elif fn == "cos":   result = math.cos(math.radians(val))
        elif fn == "tan":   result = math.tan(math.radians(val))
        elif fn == "log":   result = math.log10(val)
        elif fn == "ln":    result = math.log(val)
        elif fn == "sqrt":  result = math.sqrt(val)
        elif fn == "sq":    result = val ** 2
        elif fn == "cube":  result = val ** 3
        elif fn == "inv":   result = 1 / val
        elif fn == "exp":   result = math.exp(val)
        elif fn == "abs":   result = abs(val)
        elif fn == "floor": result = math.floor(val)
        elif fn == "ceil":  result = math.ceil(val)
        elif fn == "pi":
            st.session_state.display = str(round(math.pi, 10))
            st.session_state.new_num = True
            return
        elif fn == "e":
            st.session_state.display = str(round(math.e, 10))
            st.session_state.new_num = True
            return
        result = round(float(result), 10)
        expr_label = f"{fn}({val})"
        if result == int(result): result_str = str(int(result))
        else: result_str = str(result)
        st.session_state.history.insert(0, {
            "expr": expr_label, "result": result_str,
            "time": datetime.now().strftime("%H:%M:%S")
        })
        if len(st.session_state.history) > 10:
            st.session_state.history = st.session_state.history[:10]
        st.session_state.last_ans = float(result)
        st.session_state.display = result_str
        st.session_state.new_num = True
    except Exception as ex:
        st.session_state.display = "Error"
        st.session_state.new_num = True

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="calc-header">
    <h1>🧮 CalcPro</h1>
    <p>Advanced Python Calculator — Basic & Scientific</p>
</div>
""", unsafe_allow_html=True)

# ─── Mode Selector ────────────────────────────────────────────────────────────
col_m1, col_m2 = st.columns(2)
with col_m1:
    if st.button("🔢 Basic Mode", use_container_width=True,
                 type="primary" if st.session_state.mode == "Basic" else "secondary"):
        st.session_state.mode = "Basic"
        st.rerun()
with col_m2:
    if st.button("🔬 Scientific Mode", use_container_width=True,
                 type="primary" if st.session_state.mode == "Scientific" else "secondary"):
        st.session_state.mode = "Scientific"
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ─── Display ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="display-box">
    <div class="display-expr">{st.session_state.expr if st.session_state.expr else "&nbsp;"}</div>
    <div class="display-result">{st.session_state.display}</div>
</div>
""", unsafe_allow_html=True)

# ─── Memory & Utility Row ────────────────────────────────────────────────────
u1, u2, u3, u4, u5 = st.columns(5)
with u1:
    if st.button("MC", use_container_width=True):
        st.session_state.memory = 0.0; st.rerun()
with u2:
    if st.button("MR", use_container_width=True):
        st.session_state.display = str(st.session_state.memory)
        st.session_state.new_num = True; st.rerun()
with u3:
    if st.button("M+", use_container_width=True):
        try: st.session_state.memory += float(st.session_state.display)
        except: pass
        st.rerun()
with u4:
    if st.button("M-", use_container_width=True):
        try: st.session_state.memory -= float(st.session_state.display)
        except: pass
        st.rerun()
with u5:
    if st.button("ANS", use_container_width=True):
        st.session_state.display = str(st.session_state.last_ans)
        st.session_state.new_num = True; st.rerun()

st.markdown(f"""<div class="mode-info">Memory: {st.session_state.memory} &nbsp;|&nbsp; Last Answer: {st.session_state.last_ans}</div>""", unsafe_allow_html=True)

# ─── Scientific Functions ─────────────────────────────────────────────────────
if st.session_state.mode == "Scientific":
    st.markdown("**Scientific Functions**")
    sr1 = st.columns(5)
    sci_row1 = [("sin", "sin"), ("cos", "cos"), ("tan", "tan"), ("log", "log₁₀"), ("ln", "ln")]
    for col, (fn, label) in zip(sr1, sci_row1):
        with col:
            if st.button(label, key=f"sci_{fn}", use_container_width=True):
                sci_func(fn); st.rerun()

    sr2 = st.columns(5)
    sci_row2 = [("sqrt", "√x"), ("sq", "x²"), ("cube", "x³"), ("inv", "1/x"), ("exp", "eˣ")]
    for col, (fn, label) in zip(sr2, sci_row2):
        with col:
            if st.button(label, key=f"sci2_{fn}", use_container_width=True):
                sci_func(fn); st.rerun()

    sr3 = st.columns(5)
    sci_row3 = [("abs", "|x|"), ("floor", "⌊x⌋"), ("ceil", "⌈x⌉"), ("pi", "π"), ("e", "e")]
    for col, (fn, label) in zip(sr3, sci_row3):
        with col:
            if st.button(label, key=f"sci3_{fn}", use_container_width=True):
                sci_func(fn); st.rerun()

    st.markdown("---")

# ─── Basic Keypad ─────────────────────────────────────────────────────────────
r0 = st.columns(4)
with r0[0]:
    if st.button("AC", use_container_width=True, type="primary"):
        press_clear(); st.rerun()
with r0[1]:
    if st.button("+/-", use_container_width=True):
        press_sign(); st.rerun()
with r0[2]:
    if st.button("%", use_container_width=True):
        press_percent(); st.rerun()
with r0[3]:
    if st.button("⌫", use_container_width=True):
        press_backspace(); st.rerun()

r1 = st.columns(4)
nums_ops = [("7","num"),("8","num"),("9","num"),("÷","op")]
for col,(val,typ) in zip(r1,nums_ops):
    with col:
        if st.button(val, key=f"b_{val}", use_container_width=True):
            if typ=="num": press_num(val)
            else: press_op("/")
            st.rerun()

r2 = st.columns(4)
nums_ops2 = [("4","num"),("5","num"),("6","num"),("×","op")]
for col,(val,typ) in zip(r2,nums_ops2):
    with col:
        if st.button(val, key=f"b_{val}", use_container_width=True):
            if typ=="num": press_num(val)
            else: press_op("*")
            st.rerun()

r3 = st.columns(4)
nums_ops3 = [("1","num"),("2","num"),("3","num"),("−","op")]
for col,(val,typ) in zip(r3,nums_ops3):
    with col:
        if st.button(val, key=f"b_{val}", use_container_width=True):
            if typ=="num": press_num(val)
            else: press_op("-")
            st.rerun()

r4 = st.columns(4)
with r4[0]:
    if st.button("0", key="b_0", use_container_width=True):
        press_num("0"); st.rerun()
with r4[1]:
    if st.button(".", key="b_dot", use_container_width=True):
        press_dot(); st.rerun()
with r4[2]:
    if st.button("=", key="b_eq", use_container_width=True, type="primary"):
        press_equals(); st.rerun()
with r4[3]:
    if st.button("+", key="b_plus", use_container_width=True):
        press_op("+"); st.rerun()

# ─── Power button ─────────────────────────────────────────────────────────────
if st.button("xʸ (Power)", use_container_width=True):
    press_op("**"); st.rerun()

# ─── History ─────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📜 Calculation History")

if not st.session_state.history:
    st.info("No calculations yet — start calculating!")
else:
    hc1, hc2 = st.columns([3,1])
    with hc2:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.history = []
            st.rerun()
    for item in st.session_state.history:
        st.markdown(f"""
        <div class="history-item">
            🕐 {item['time']} &nbsp;|&nbsp; {item['expr']} = <span>{item['result']}</span>
        </div>
        """, unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center;color:#aaa;font-size:0.8rem;margin-top:2rem'>
    Built with ❤️ using Python & Streamlit | CodSoft Python Internship | Allen Stivanson Christian
</div>
""", unsafe_allow_html=True)
