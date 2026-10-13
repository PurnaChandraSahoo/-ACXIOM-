# AcxiomCRM — Django MVP

A fast starter project for demonstrating the AcxiomCRM assignment using Python, Django templates, HTML, CSS, JavaScript, and SQLite.

## 1. Setup (Windows)
Open Command Prompt/PowerShell in this folder:

```bash
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
py manage.py makemigrations crm
py manage.py migrate
py manage.py createsuperuser
py manage.py runserver
```

Open http://127.0.0.1:8000/ and sign in with the superuser you created.
Admin data management: http://127.0.0.1:8000/admin/

If `py` is unavailable, use `python` instead.

## Included
- Django session authentication (login/logout); Django password hashing and CSRF protection
- Dashboard KPI cards and Chart.js charts
- Customer, Lead, Opportunity, Follow-up, Activity, and Audit Log models
- Add/list/search for core CRM records
- Server-side model/form validation, including email, phone, opportunity amount/probability/date, follow-up date
- Customer/Lead/Opportunity JSON GET APIs, protected by login
- Django admin for full CRUD and quick demo data entry

## Demo workflow
1. Create a superuser and log in.
2. Use the top navigation to add customers, leads, opportunities and follow-ups.
3. Visit Django Admin to edit/delete records and inspect audit events.
4. Visit `/api/customers/`, `/api/leads/`, `/api/opportunities/` while logged in.

## Important scope note
This is a 2-hour MVP, not a production-complete implementation of every requirement in the supplied specification. In particular, granular Admin/Manager/Sales Executive permissions, robust account lockout, full update/delete screens, API write endpoints, CSV exports, and comprehensive audit coverage still need development. Use the Django admin for complete CRUD during the demo. For production, configure HTTPS, secure cookies, environment-based secrets, rate limiting, and database credentials securely.

## MySQL (optional)
Install a compatible driver such as `mysqlclient`, create a database, then update `DATABASES` in `acxiomcrm/settings.py`. SQLite is the quickest choice for the 2-hour deadline.
