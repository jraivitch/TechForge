# TechForge

TechForge is an interactive learning platform for mastering software engineering, DevOps, mobile security, and technical sales skills. It covers 19 topics and 63 lessons organized around real-world workflows, with built-in progress tracking, quizzes, and full-text search — all running locally in your browser.

---

## What TechForge Covers

TechForge is organized into 19 topics, each broken into 3–4 hands-on lessons. Every lesson includes:

- **Explanation** — a clear conceptual breakdown of the topic
- **Real-world context** — how the concept applies in day-to-day engineering work
- **Commands** — the exact terminal commands used
- **Code example** — runnable snippets or annotated walkthroughs
- **Quiz** — a question and answer to test retention

### Topics

| # | Topic | Description |
|---|-------|-------------|
| 1 | Git | Version control — staging, committing, branching, pushing |
| 2 | GitHub | Pull requests, code review, cloning, forking |
| 3 | Bash | Terminal navigation, file management, grep, pipes |
| 4 | Python | Variables, functions, loops, file I/O |
| 5 | Linux | Kernel basics, file system layout, permissions |
| 6 | Docker | Containers, images, Dockerfile, builds |
| 7 | Networking | IP, DNS, TCP/UDP, ports, HTTP |
| 8 | REST APIs | HTTP methods, JSON, authentication, headers |
| 9 | SQL | SELECT, WHERE, INSERT/UPDATE/DELETE, JOINs |
| 10 | Appium | Mobile UI automation, locators, Corellium integration |
| 11 | ADB | Android Debug Bridge — shell, logcat, file transfer, port forwarding |
| 12 | Android | Architecture, APK format, file system, logcat security |
| 13 | iOS | Architecture, IPA format, dynamic analysis, objection |
| 14 | Frida | Dynamic instrumentation, Java hooking, iOS workflow, cert pinning bypass |
| 15 | Vim | Modal editing, navigation, search-replace, saving files |
| 16 | Corellium | Virtual iOS/Android devices, snapshots, networking, ADB/Appium integration |
| 17 | Reverse Engineering | Static analysis, dynamic analysis, jadx, APK inspection |
| 18 | Solutions Engineering | Discovery, demos, proof of concept, the SE sales cycle |
| 19 | Demo Engineering | Repeatable demos, storytelling, demo environments |

---

## App Features

### Dashboard
The home page shows your overall progress across all 19 topics — total lessons, completed lessons, and completion percentage. It surfaces topics you are currently working through and suggests what to continue next.

### Topic Browser
Browse all topics in a grid view with per-topic progress bars showing how many lessons you have completed. Click any topic to see its full lesson list.

### Lesson View
Each lesson page shows:
- The full explanation and real-world context
- A formatted commands block with the key terminal commands
- A syntax-highlighted code example
- The quiz question and answer
- Estimated read time, difficulty level, and tags
- A "Mark Complete" button to record your progress
- Previous / Next lesson navigation within the topic

### Progress Tracking
Marking a lesson complete records the completion timestamp in a local SQLite database. Progress persists across sessions and is reflected everywhere — dashboard stats, topic progress bars, and individual lesson status indicators.

### Search
The search bar at the top of every page performs a full-text search across topic names, topic descriptions, lesson titles, lesson explanations, lesson real-world sections, and tags. Results are grouped by topics and lessons.

### Sidebar Navigation
Every page has a persistent sidebar listing all 19 topics with their icons, so you can jump to any topic instantly from anywhere in the app.

---

## Tech Stack

- **Backend**: Python 3 + Flask
- **Database**: SQLite (via Python's built-in `sqlite3` module — no ORM)
- **Templates**: Jinja2 (Flask's built-in templating engine)
- **Frontend**: Vanilla HTML/CSS/JS — no external frameworks
- **Content**: Seeded via `data/seed.py` — all 19 topics and 63 lessons defined in Python

---

## Installation

### Prerequisites

- Python 3.10 or later
- `pip` (comes with Python)

### Steps

**1. Clone the repository**

```bash
git clone https://github.com/your-username/TechForge.git
cd TechForge
```

**2. Create and activate a virtual environment** (recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Initialize the database**

```bash
flask --app run init-db
```

This creates `instance/techforge.db` with the schema (topics, lessons, lesson_progress tables).

**5. Seed the content**

```bash
python data/seed.py
```

This populates the database with all 19 topics and 63 lessons.

---

## Running the App

```bash
python run.py
```

Open your browser and go to:

```
http://localhost:5000
```

The app runs in debug mode by default. Any code changes you make will automatically reload the server.

---

## Project Structure

```
TechForge/
├── run.py                  # Entry point — creates and runs the Flask app
├── config.py               # Development and production config classes
├── requirements.txt        # Python dependencies (Flask)
├── data/
│   └── seed.py             # Seeds all 19 topics and 63 lessons into the database
├── instance/
│   └── techforge.db        # SQLite database (created by init-db, not committed)
└── app/
    ├── __init__.py         # App factory (create_app), blueprint registration
    ├── database.py         # DB connection, schema init, get_topic_progress helper
    ├── routes/
    │   ├── dashboard.py    # GET /  — dashboard with overall stats
    │   ├── topics.py       # GET /topics, GET /topics/<id>
    │   ├── lessons.py      # GET /lessons/<id>, POST /lessons/<id>/complete
    │   └── search.py       # GET /search?q=<query>
    ├── templates/
    │   ├── base.html       # Shared layout with sidebar and nav
    │   ├── dashboard.html  # Home page
    │   ├── topics.html     # Topic grid
    │   ├── topic_detail.html  # Topic lesson list
    │   ├── lesson.html     # Individual lesson view
    │   └── search.html     # Search results
    └── static/
        ├── css/main.css    # All styles
        └── js/main.js      # Client-side behavior
```

---

## Resetting Progress

To clear all progress and start fresh without losing content:

```bash
sqlite3 instance/techforge.db "DELETE FROM lesson_progress;"
```

To re-seed all content from scratch (wipes topics, lessons, and progress):

```bash
python data/seed.py
```

---

## Database Schema

```sql
topics (
    id, name, description, difficulty, icon, order_index
)

lessons (
    id, topic_id, title, explanation, real_world,
    commands, code_example, quiz_question, quiz_answer,
    difficulty, estimated_minutes, tags, order_index
)

lesson_progress (
    id, lesson_id, completed, completed_at
)
```

You can inspect the live database directly:

```bash
sqlite3 instance/techforge.db
sqlite> SELECT name, icon FROM topics ORDER BY order_index;
sqlite> SELECT COUNT(*) FROM lesson_progress WHERE completed = 1;
```
