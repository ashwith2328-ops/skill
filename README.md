# Placement-Oriented Skill Gap Analyzer

A web app built with **HTML**, **CSS**, and **Django** that helps users compare their skills against placement and job role requirements and see where the gaps are.

## Features

- **Analyze** — Select a placement role and your profile to see which required skills you meet and which you need to build.
- **Roles** — Browse placement roles and their required skills (with proficiency levels).
- **Profiles** — Create profiles and attach your skills with self-assessed proficiency.
- **Skills catalog** — View all skills grouped by category.

## Tech stack

- **Backend:** Django 5
- **Frontend:** HTML5, CSS3 (no JavaScript required for core flow)
- **Database:** SQLite (default)

## Setup

1. **Create and activate a virtual environment** (recommended):

   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   # source venv/bin/activate  # macOS/Linux
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations:**

   ```bash
   python manage.py migrate
   ```

4. **Create a superuser** (to add roles, skills, and manage data via admin):

   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

6. Open **http://127.0.0.1:8000/** in your browser.

## Initial data

- Go to **http://127.0.0.1:8000/admin/** and log in with your superuser account.
- Add **Skill categories** and **Skills**.
- Add **Placement roles** and link required skills via **Role skill requirements** (with proficiency: basic / intermediate / advanced / expert).
- Create **User profiles** and add **User skills** for each profile.

Then use **Analyze** to pick a role and a profile and view the gap report.

## Project structure

```
Placement-Oriented Skill Gap Analyzer/
├── manage.py
├── requirements.txt
├── README.md
├── skill_gap_analyzer/       # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── skill_gap/                # Main app
    ├── models.py             # SkillCategory, Skill, PlacementRole, UserProfile, etc.
    ├── views.py
    ├── urls.py
    ├── forms.py
    ├── admin.py
    ├── templates/skill_gap/  # HTML templates
    └── static/skill_gap/css/ # CSS
```

## License

MIT.
