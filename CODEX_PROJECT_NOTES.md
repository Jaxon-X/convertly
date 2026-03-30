# Convertly Project Notes

## Overview
- Convertly is a Django + Celery file conversion project with a static frontend in `front/`.
- Backend runs best through Docker Compose with `web`, `celery`, `redis`, and `db` services.
- Frontend currently uses a single-entry architecture:
  - `front/index.html`
  - `front/styles/main.css`
  - `front/scripts/converters.js`
  - `front/scripts/main.js`

## Backend State
- File uploads are written to the shared Docker volume path and deleted after 10 minutes.
- Converted files are deleted after 15 minutes.
- Downloads are protected by:
  - JWT authentication
  - a signed download token returned by the conversion response

## Auth State
- V1 auth is email + password + username/display name.
- Register and login currently return JWT tokens immediately so the user can continue the pending download.
- User model now includes `is_email_verified` and `email_verification_sent_at` to prepare for future email verification.
- Email verification is not enforced yet.

## Frontend UX State
- Users can convert as guests.
- When they try to download, the frontend opens an auth modal if they are not signed in.
- After registration, the modal switches to the login tab and asks the user to click `Login and download`.
- After successful login, the frontend resumes the pending download automatically.
- Tool cards and selected-file badges use per-format visual tones.

## Important Files
- Backend auth:
  - `user/models.py`
  - `user/serializers.py`
  - `user/views.py`
- Conversion and secure download:
  - `convertor/views.py`
  - `convertor/tasks.py`
  - `convertor/tests.py`
- Frontend auth/workspace:
  - `front/index.html`
  - `front/styles/main.css`
  - `front/scripts/converters.js`
  - `front/scripts/main.js`

## Recent Changes
- Dockerized local development flow and shared storage between `web` and `celery`.
- Rebuilt frontend into a single animated conversion workspace.
- Removed old legacy frontend pages and assets.
- Lightened frontend palette and highlighted the workspace section.
- Added signed-download + auth gating for downloads.
- Added V1 login/register modal flow in the frontend.
- Added `user.0003_customuser_email_verification_fields` to prepare the auth model for future email verification.
- Verified the current auth + download implementation with Django tests for `user` and `convertor`.
- Fixed the auth modal visibility bug so the dialog stays hidden on first page load and only appears when the download action triggers it.
- Replaced the old generic logo asset with a lighter custom SVG brand mark and refined the header logo frame so the product branding feels cleaner and more intentional.
- Switched the frontend favicon from the old PNG asset to the new SVG logo and added a version query so browsers are more likely to refresh the cached tab icon.
