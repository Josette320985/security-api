import os
import time
import secrets
import re

# Paths to the shared files (mounted from the frontend HTML folder)
JS_PATH = "/shared-html/app.js"           # Frontend app.js
LOGIN_JS_PATH = "/shared-html/login.js"   # Frontend login.js
BACKEND_SECRET_FILE = "/app/.secret"      # Secret del backend
LDAP_SECRET_FILE = "/app/.ldap-secret"    # Secret del LDAP
FRONTEND_LDAP_SECRET = "/shared-html/.ldap-secret"  # Para que el frontend lo lea
FRONTEND_BACKEND_SECRET = "/shared-html/.backend-secret"  # Para que el frontend lo lea


def update_frontend_backend_secret(new_secret):
    """Actualiza el API_KEY del backend en app.js del frontend."""
    try:
        with open(JS_PATH, "r") as f:
            content = f.read()
        # Reemplaza: const API_KEY = "...";
        pattern = r'(const\s+API_KEY\s*=\s*")[^"]*(";)'
        new_content = re.sub(pattern, f'\\g<1>{new_secret}\\g<2>', content)
        with open(JS_PATH, "w") as f:
            f.write(new_content)
        print(f"[rotate] Updated frontend app.js API_KEY")
    except Exception as e:
        print(f"[rotate] Error updating frontend app.js: {e}")


def update_frontend_ldap_secret(new_secret):
    """Actualiza el LDAP_API_KEY en login.js del frontend."""
    try:
        with open(LOGIN_JS_PATH, "r") as f:
            content = f.read()
        # Reemplaza: const LDAP_API_KEY = "...";
        pattern = r'(const\s+LDAP_API_KEY\s*=\s*")[^"]*(";)'
        new_content = re.sub(pattern, f'\\g<1>{new_secret}\\g<2>', content)
        with open(LOGIN_JS_PATH, "w") as f:
            f.write(new_content)
        print(f"[rotate] Updated frontend login.js LDAP_API_KEY")
    except Exception as e:
        print(f"[rotate] Error updating frontend login.js: {e}")


def rotate_secrets():
    """Rota los 3 secrets simultáneamente."""
    # Generate new random secrets
    new_backend_secret = secrets.token_urlsafe(32)
    new_ldap_secret = secrets.token_urlsafe(32)

    # Write secrets to the backend's internal files
    with open(BACKEND_SECRET_FILE, "w") as f:
        f.write(new_backend_secret)
    with open(LDAP_SECRET_FILE, "w") as f:
        f.write(new_ldap_secret)

    # Write secrets to the shared volume (visible to ldap-api and frontend)
    with open(FRONTEND_BACKEND_SECRET, "w") as f:
        f.write(new_backend_secret)
    with open(FRONTEND_LDAP_SECRET, "w") as f:
        f.write(new_ldap_secret)

    # Update the JS files served by the frontend
    update_frontend_backend_secret(new_backend_secret)
    update_frontend_ldap_secret(new_ldap_secret)

    # Update environment variables in memory
    os.environ["API_SECRET"] = new_backend_secret
    os.environ["LDAP_API_KEY"] = new_ldap_secret

    print(f"[rotate] New BACKEND_API_SECRET: {new_backend_secret}")
    print(f"[rotate] New LDAP_API_KEY: {new_ldap_secret}")


if __name__ == "__main__":
    print("[rotate] Starting secret rotation every 2 minutes...")
    while True:
        rotate_secrets()
        time.sleep(120)   # 2 minutos