import streamlit as st
import json
import os
from datetime import datetime, date
import uuid

st.set_page_config(
    page_title="TaskFlow | To-Do List",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = "tasks.json"
PRIORITIES = {"🔴 High": "high", "🟡 Medium": "medium", "🟢 Low": "low"}
PRIORITY_COLORS = {"high": "#ff4b4b", "medium": "#ffa500", "low": "#21c354"}
CATEGORIES = ["Personal", "Work", "Study", "Health", "Finance", "Other"]

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2, default=str)

def add_task(title, description, priority, category, due_date):
    tasks = load_tasks()
    task = {
        "id": str(uuid.uuid4()),
        "title": title.strip(),
        "description": description.strip(),
        "priority": priority,
        "category": category,
        "due_date": str(due_date),
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    tasks.append(task)
    save_tasks(tasks)
    return task

def update_task(task_id, updates):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task.update(updates)
    save_tasks(tasks)

def delete_task(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)

def toggle_complete(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if task["completed"] else None
    save_tasks(tasks)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
    }
    .main-header h1 { font-size: 2.5rem; margin: 0; color: white; }
    .main-header p  { font-size: 1rem; margin: 0.5rem 0 0; opacity: 0.85; color: white; }
    .stat-card {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        border-left: 4px solid;
    }
    .stat-card h2 { font-size: 2rem; margin: 0; }
    .stat-card p  { margin: 0; color: #666; font-size: 0.85rem; }
    .task-card {
        background: white;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        border-left: 5px solid;
    }
    .task-title { font-size: 1.05rem; font-weight: 600; margin: 0 0 6px 0; }
    .task-meta  { font-size: 0.82rem; color: #777; margin-top: 4px; }
    .badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 6px;
    }
    .completed-task { opacity: 0.55; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## ➕ Add New Task")
    with st.form("add_task_form", clear_on_submit=True):
        title       = st.text_input("Task Title *", placeholder="e.g. Complete Python project")
        description = st.text_area("Description", placeholder="Optional details...", height=80)
        priority    = st.selectbox("Priority", list(PRIORITIES.keys()))
        category    = st.selectbox("Category", CATEGORIES)
        due_date    = st.date_input("Due Date", value=date.today())
        submitted   = st.form_submit_button("Add Task ✅", use_container_width=True)
        if submitted:
            if not title.strip():
                st.error("Task title is required!")
            else:
                add_task(title, description, PRIORITIES[priority], category, due_date)
                st.success("Task added!")
                st.rerun()

    st.markdown("---")
    st.markdown("## 🔍 Filter & Search")
    search_query    = st.text_input("Search tasks", placeholder="Type to search...")
    filter_status   = st.selectbox("Status", ["All", "Active", "Completed"])
    filter_priority = st.selectbox("Priority", ["All", "🔴 High", "🟡 Medium", "🟢 Low"])
    filter_category = st.selectbox("Category", ["All"] + CATEGORIES)
    sort_by         = st.selectbox("Sort by", ["Created (Newest)", "Created (Oldest)", "Due Date", "Priority"])

st.markdown("""
<div class="main-header">
    <h1>✅ TaskFlow</h1>
    <p>Your personal productivity manager — stay focused, stay ahead.</p>
</div>
""", unsafe_allow_html=True)

tasks     = load_tasks()
total     = len(tasks)
completed = sum(1 for t in tasks if t["completed"])
active    = total - completed
overdue   = sum(1 for t in tasks if not t["completed"] and t.get("due_date") and t["due_date"] < str(date.today()))

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="stat-card" style="border-color:#667eea"><h2 style="color:#667eea">{total}</h2><p>Total Tasks</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="stat-card" style="border-color:#21c354"><h2 style="color:#21c354">{active}</h2><p>Active</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="stat-card" style="border-color:#a0a0a0"><h2 style="color:#a0a0a0">{completed}</h2><p>Completed</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="stat-card" style="border-color:#ff4b4b"><h2 style="color:#ff4b4b">{overdue}</h2><p>Overdue</p></div>', unsafe_allow_html=True)

if total > 0:
    st.markdown("<br>", unsafe_allow_html=True)
    progress = completed / total
    st.progress(progress, text=f"Overall Progress — {completed}/{total} tasks completed ({int(progress*100)}%)")

st.markdown("<br>", unsafe_allow_html=True)

def apply_filters(tasks):
    if search_query:
        tasks = [t for t in tasks if search_query.lower() in t["title"].lower()
                 or search_query.lower() in t.get("description","").lower()]
    if filter_status == "Active":
        tasks = [t for t in tasks if not t["completed"]]
    elif filter_status == "Completed":
        tasks = [t for t in tasks if t["completed"]]
    if filter_priority != "All":
        tasks = [t for t in tasks if t["priority"] == PRIORITIES[filter_priority]]
    if filter_category != "All":
        tasks = [t for t in tasks if t["category"] == filter_category]
    priority_order = {"high": 0, "medium": 1, "low": 2}
    if sort_by == "Created (Newest)":
        tasks.sort(key=lambda x: x["created_at"], reverse=True)
    elif sort_by == "Created (Oldest)":
        tasks.sort(key=lambda x: x["created_at"])
    elif sort_by == "Due Date":
        tasks.sort(key=lambda x: x.get("due_date","9999"))
    elif sort_by == "Priority":
        tasks.sort(key=lambda x: priority_order.get(x["priority"], 2))
    return tasks

filtered_tasks = apply_filters(tasks)

if not filtered_tasks:
    st.info("No tasks found. Add one from the sidebar! 👈")
else:
    st.markdown(f"### 📋 Tasks ({len(filtered_tasks)} shown)")
    for task in filtered_tasks:
        p_color    = PRIORITY_COLORS.get(task["priority"], "#ccc")
        is_done    = task["completed"]
        due        = task.get("due_date","")
        is_overdue = not is_done and due and due < str(date.today())
        card_class = "task-card completed-task" if is_done else "task-card"
        strike     = "text-decoration:line-through;color:#aaa;" if is_done else ""
        done_icon  = "✅ " if is_done else ""
        overdue_badge = '<span class="badge" style="background:#fff0f0;color:#ff4b4b">⚠️ OVERDUE</span>' if is_overdue else ""
        desc_text  = f" | 📝 {task['description']}" if task.get('description') else ""

        card_html = (
            f'<div class="{card_class}" style="border-color:{p_color}">'
            f'<p class="task-title" style="{strike}">{done_icon}{task["title"]}</p>'
            f'<div class="task-meta">'
            f'<span class="badge" style="background:{p_color}22;color:{p_color}">{task["priority"].upper()}</span>'
            f'<span class="badge" style="background:#f0f0ff;color:#667eea">{task["category"]}</span>'
            f'{overdue_badge}'
            f'📅 Due: {due} | 🕐 Created: {task["created_at"][:10]}{desc_text}'
            f'</div>'
            f'</div>'
        )
        st.markdown(card_html, unsafe_allow_html=True)

        c1, c2, c3, _ = st.columns([1.2, 1, 1, 4])
        with c1:
            label = "↩️ Undo" if is_done else "✅ Done"
            if st.button(label, key=f"toggle_{task['id']}"):
                toggle_complete(task["id"])
                st.rerun()
        with c2:
            if st.button("🗑️ Delete", key=f"del_{task['id']}"):
                delete_task(task["id"])
                st.rerun()
        with c3:
            if st.button("✏️ Edit", key=f"edit_{task['id']}"):
                st.session_state[f"editing_{task['id']}"] = True

        if st.session_state.get(f"editing_{task['id']}", False):
            with st.form(key=f"edit_form_{task['id']}"):
                st.markdown("**✏️ Edit Task**")
                new_title = st.text_input("Title", value=task["title"])
                new_desc  = st.text_area("Description", value=task.get("description",""), height=60)
                new_pri   = st.selectbox("Priority", list(PRIORITIES.keys()),
                                         index=list(PRIORITIES.values()).index(task["priority"]))
                new_cat   = st.selectbox("Category", CATEGORIES,
                                         index=CATEGORIES.index(task["category"]) if task["category"] in CATEGORIES else 0)
                new_due   = st.date_input("Due Date", value=date.fromisoformat(task["due_date"]) if task.get("due_date") else date.today())
                s1, s2 = st.columns(2)
                with s1:
                    if st.form_submit_button("💾 Save", use_container_width=True):
                        update_task(task["id"], {
                            "title": new_title, "description": new_desc,
                            "priority": PRIORITIES[new_pri], "category": new_cat,
                            "due_date": str(new_due)
                        })
                        st.session_state[f"editing_{task['id']}"] = False
                        st.rerun()
                with s2:
                    if st.form_submit_button("❌ Cancel", use_container_width=True):
                        st.session_state[f"editing_{task['id']}"] = False
                        st.rerun()
        st.markdown("---")

st.markdown("""
<div style='text-align:center;color:#aaa;font-size:0.8rem;margin-top:2rem'>
    Built with ❤️ using Python & Streamlit | CodSoft Python Internship | Allen Stivanson Christian
</div>
""", unsafe_allow_html=True)
