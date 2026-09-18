# Groups

A Django web app that connects students and teachers within a school for
tutoring and group study. Sign-in is restricted to Google accounts on a single
configured email domain, users are automatically sorted into student and
teacher roles, and teachers can open study rooms with real-time chat.

## What the site does

**Domain-restricted Google sign-in.** Authentication runs entirely through
Google OAuth (django-allauth). A custom social adapter (`groups/adapters.py`)
rejects any account whose email is not on the domain named by the
`ALLOWED_EMAIL_DOMAIN` environment variable, showing `templates/error.html`
instead of logging them in. There is no self-serve password registration.

**Automatic student/teacher roles.** On first sign-in the adapter reads the
email local part: addresses beginning with three digits (student ID numbers)
are added to the `student` group, everything else to the `teacher` group. Role
gates the rest of the UI — for example, only teachers see and can use the
"create room" action, enforced by the `allowed_users` decorator in
`base/decorators.py`.

**Study rooms with live chat.** Teachers create named rooms, which get a unique
URL slug. A room is private to its participant list: the HTTP view and the
WebSocket consumer both refuse anyone who is not a participant. Messages are
delivered over Django Channels (WebSocket, Redis-backed channel layer) and
persisted, so history reloads with the page.

**Tutoring connections.** Every user gets a `Profile` automatically via a
`post_save` signal. Users can browse and search a directory of profiles, send
connection invitations, and accept, decline, or remove them. Accepting a
`Relationship` wires up the friendship on both sides through signals in
`tutor/signals.py`.

**Home feed.** The landing page lists only the rooms the signed-in user
participates in, newest first, with a name search.

## Layout

| Path | Purpose |
| --- | --- |
| `groups/` | Project settings, URL root, ASGI entrypoint, allauth social adapter |
| `users/` | `CustomUser` (unique email, `AbstractUser`), login/logout views |
| `base/` | Home feed, room creation, auth/role decorators |
| `chat/` | `Room` and `Message` models, room view, WebSocket consumer and routing |
| `tutor/` | `Profile` and `Relationship` models, invitations, profile directory |
| `templates/`, `static/` | Shared base templates, navbar, CSS and vanilla JS |

## Stack

Django 4.x · Django Channels + Daphne (ASGI) · Redis (channel layer) ·
PostgreSQL · django-allauth (Google OAuth) · plain HTML/CSS/JS front end

## Running locally

Requires Python 3.9+, PostgreSQL, and Redis.

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Configure the environment. Every secret is read from the environment, so nothing
sensitive lives in the repo:

```bash
cp .env.example .env
# then fill in DJANGO_SECRET_KEY, POSTGRES_PASSWORD and ALLOWED_EMAIL_DOMAIN
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Start Redis and PostgreSQL, create the database named in `POSTGRES_DB`, then:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Because `ASGI_APPLICATION` is set, `runserver` is served by Daphne, so
WebSockets work in development without a separate process.

### One-time Google OAuth setup

1. In the Google Cloud console create an **OAuth 2.0 Client ID** of type *Web
   application*, with `http://127.0.0.1:8000/accounts/google/login/callback/`
   as an authorized redirect URI.
2. `settings.py` uses `SITE_ID = 4`, so in Django admin make sure a **Site**
   row with that ID exists and its domain is `127.0.0.1:8000`.
3. In Django admin add a **Social application**: provider `Google`, your client
   ID and secret, associated with that site.

Do not commit the downloaded `client_secret*.json` — it is gitignored.

## Configuration reference

All settings come from environment variables (see `.env.example`):

| Variable | Default | Notes |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | random per process in debug | **Required** when `DJANGO_DEBUG=False` |
| `DJANGO_DEBUG` | `True` | Set `False` in production |
| `DJANGO_ALLOWED_HOSTS` | `127.0.0.1,localhost` | Comma-separated |
| `ALLOWED_EMAIL_DOMAIN` | _empty_ | **Required.** Email domain allowed to sign in; empty refuses everyone |
| `POSTGRES_DB` / `POSTGRES_USER` / `POSTGRES_PASSWORD` / `POSTGRES_HOST` / `POSTGRES_PORT` | `pgdb` / `postgres` / _empty_ / `localhost` / `5432` | |
| `REDIS_HOST` / `REDIS_PORT` | `127.0.0.1` / `6379` | Channels layer |
| `CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS`, `SECURE_SSL_REDIRECT` | _empty_ | Production only |

With `DJANGO_DEBUG=False`, `settings.py` additionally turns on HSTS, secure
session and CSRF cookies, SSL redirect, `X-Frame-Options: DENY`, and refuses to
start without a real secret key.

## Known gaps

- The login page still renders a username/password form, but the credential
  logic in `users/views.py` is commented out and the `register/` route is
  disabled — Google SSO is the only working path.
- `base.views.userProfile` renders `base/profile.html`, which does not exist;
  the live profile page is `tutor:user-profile`.
- `SOCIALACCOUNT_LOGIN_ON_GET = True` is needed because the login template
  links to the provider with a plain `<a href>`. Switching to a POST form would
  let this be turned off.
- `data.json` is a fixture of permissions and content types only, not seed
  content.
- The `tests.py` files are all still empty.
