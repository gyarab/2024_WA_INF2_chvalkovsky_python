import os
import subprocess
import re
import argparse
from pathlib import Path


class SVSException(Exception):
    pass
class SystemdException(SVSException):
    pass

class SVS():
    SVS_STATIC_ROOT = Path("/var/caddy.root.d/")
    SVS_CONFIG_FILE = Path(".svs")
    VENV_DIR = Path(".venv")
    REQUIREMENTS_TXT = Path("requirements.txt")
    MANAGE_PY = Path("manage.py")
    PGPASS = Path("~/.pgpass").expanduser()
    SYSTEMD_DIR = Path("~/.config/systemd/user/").expanduser()
    LOGS_DIR = Path("logs")


    def __init__(self):
        self.dir = Path.cwd()
        self.domain = None

    def load(self):
        self.load_config()
        self.project_name = self.django_get_project()
        self.settings_file = Path(self.project_name) / "settings.py"
        self.settings_file_svs =  Path(self.project_name) / "settings_svs.py"
        self.pg_username = self.pg_get_username()
        
    def load_config(self):
        """Load the svs configuration file."""
        if not self.SVS_CONFIG_FILE.exists():
            print(f"🟨 Config file '{self.SVS_CONFIG_FILE}' not found.")
            return
        
        with self.SVS_CONFIG_FILE.open("r") as f:
            for line in f:
                key, value = line.strip().split("=", 1)
                if key == "domain":
                    self.domain = value
    
    def save_config(self):
        """Save the svs configuration file."""
        with self.SVS_CONFIG_FILE.open("w") as f:
            if self.domain:
                f.write(f"domain={self.domain}\n")

    def command(self, command, env=None, check=True):
        """Run a shell command and return the output."""
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=check, env=env)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            cmd = " ".join([str(c) for c in command])
            if command[0]=="systemctl":
                raise SystemdException(f"Error executing '{cmd}'")
            else:
                raise SVSException(f"Error executing '{cmd}':\nstdout:{e.stdout}\nstderr:{e.stderr}")

    def is_valid_svs_domain(self, domain):
        """Validate domain format."""
        if not domain:
            return False
        pattern = r"^[a-z0-9]+\.svs\.gyarab\.cz$"
        match = re.match(pattern, domain)
        return match is not None

    def is_valid_domain(self, domain):
        """Check if the domain is a valid domain name."""
        if not domain:
            return False
        pattern = r"^((?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+(?!-)[A-Za-z0-9-]{1,63}(?<!-)$"
        match = re.match(pattern, domain)
        return match is not None

    # avava-web

    def avava_web_list(self):
        """List all registered domains."""
        lines = self.command(["sudo", "avava-web", "list"]).splitlines()
        domains = {}
        for line in lines:
            match = re.match(r'\s*- "(?P<domain>[^"]+)": port=(?P<port>\d+)', line)
            if match:
                domain = match.group("domain")
                port = int(match.group("port"))
                domains[domain] = port
                print(f"🟦 Registered '{domain}' at port {port}")
        if not domains:
            print("🟦 No registered domains found")
        return domains

    def avava_web_register(self, domain):
        """Register a domain with avava."""
        domains = self.avava_web_list()
        if domain in domains:
            return domains[domain]
        else:
            if self.is_valid_svs_domain(domain) or self.is_valid_domain(domain):
                output = self.command(["sudo", "avava-web", "register", domain]).strip() 
                if "Domena" in output and "zaregistrovana" in output:
                    match = re.search(r"portu (\d+)", output)
                    if match:
                        port = match.group(1)
                        print(f"🟩 Domain {domain} registered successfully on port {port}")
                        return port
                    else:
                        raise SVSException(f"Error parsing domain port '{domain}': unrecognized '{output}'")
                else:
                    raise SVSException(f"Error registering domain '{domain}': unrecognized '{output}'")

    def avava_web_unregister(self, domain):
        """Unregister a domain with avava."""
        if self.is_valid_svs_domain(domain) or self.is_valid_domain(domain):
            domains = self.avava_web_list()
            if domain not in domains:
                print(f"🟨 Domain {domain} not registered")

            
            self.command(["sudo", "avava-web", "--script", "unregister", domain]).strip().splitlines()
            print(f"🟩 Domain {domain} unregistered successfully")

    # venv

    def create_venv(self, domain):
        """Create or update virtual environment for the given domain."""
        if not self.REQUIREMENTS_TXT.exists():
            raise SVSException(f"File '{self.REQUIREMENTS_TXT}' not found.")

        if self.VENV_DIR.exists():
            print(f"🟩 Virtual '{self.VENV_DIR}' environment exists. Updating packages...")
            self.command([self.VENV_DIR / "bin" / "pip", "install", "--upgrade", "-r", self.REQUIREMENTS_TXT])
        else:
            print(f"🟩 Creating virtual environment '{self.VENV_DIR}' ...")
            self.command(["python3", "-m", "venv", self.VENV_DIR])
            print(f"🟩 Installing packages from '{self.REQUIREMENTS_TXT}'...")
            self.command([self.VENV_DIR / "bin" / "pip", "install", "-r", self.REQUIREMENTS_TXT])
            print(f"🟩 Installing gunicorn server...")
            self.command([self.VENV_DIR / "bin" / "pip", "install", "gunicorn"])
            print(f"🟩 Installing psycopg...")
            self.command([self.VENV_DIR / "bin" / "pip", "install", "psycopg"])
    
    # pg

    def pg_get_username(self):
        """Get the PostgreSQL username from the PGPASS file."""
        if not self.PGPASS.exists():
            raise SVSException(f"File '{self.PGPASS}' not found.")
        
        with self.PGPASS.open("r") as f:
            for line in f:
                parts = line.split(":")
                if len(parts) >= 4:
                    username = parts[3]
                    print(f"🟩 Detected PostgreSQL username '{username}'")
                    return username
        
        raise SVSException(f"Could not find username in '{self.PGPASS}' file.")

    # django

    def django_get_project(self):
        """Get the Django project name from manage.py file."""
        if not self.MANAGE_PY.exists():
            raise SVSException(f"File '{self.MANAGE_PY}' not found.")
        
        with self.MANAGE_PY.open("r") as f:
            content = f.read()
        
        match = re.search(r"os\.environ\.setdefault\(['\"]DJANGO_SETTINGS_MODULE['\"], ['\"]([\w\.]+)['\"]\)", content)
        if match:
            project_name = match.group(1).split(".")[0]

            print(f"🟩 Detected Django project '{project_name}'")
            return project_name
        else:
            raise SVSException(f"Could not detect Django project name from '{self.MANAGE_PY}' file.")

    def django_collect_static(self):
        """Collect static files for the Django project."""
        print("🟩 Collecting static files...")
        self.command([self.VENV_DIR / "bin" / "python", self.MANAGE_PY, "collectstatic", "--noinput"], env={"DJANGO_SETTINGS_MODULE": f"{self.project_name}.settings_svs"})

    def django_create_settings_svs(self):
        if not self.settings_file.exists():
            raise SVSException(f"Error: {self.settings_file} not found.")

        static_root_domain = self.SVS_STATIC_ROOT / self.domain
        if not static_root_domain.exists():
            raise SVSException(f"Static web root directory '{static_root_domain}' not found.")

        index_html = static_root_domain / "index.html"
        backup_index_html = static_root_domain / "index.html.backup"
        
        if index_html.exists():
            print(f"🟩 Moving `{index_html}` to `{backup_index_html}`...")
            index_html.rename(backup_index_html)

        if self.settings_file_svs.exists():
            print(f"🟨 Alternate settings file '{self.settings_file_svs}' exists, not touching it.")
        else:
            print(f"🟩 Creating alternate settings file '{self.settings_file_svs}'...")
            static_dir = static_root_domain / "static"
            svs_config={
                "DEBUG" : "False",
                "ALLOWED_HOSTS": f"['{self.domain}']",
                "STATIC_ROOT": f"'{static_dir}'",
                "DATABASES": f"""{{
        'default': {{
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': '{self.pg_username}',
            'USER': '{self.pg_username}',
            'PASSWORD': '',
        }}
    }}
    """
            }
            
            with self.settings_file.open("r") as f:
                content = f.read()

            with self.settings_file_svs.open("w") as f:
                f.write("from .settings import *\n\n")
                for key, value in svs_config.items():
                    f.write(f"{key} = {value}\n\n")

    def django_migrate(self):
        """Run Django migrations."""
        print("🟩 Running Django migrations...")
        self.command([self.VENV_DIR / "bin" / "python", self.MANAGE_PY, "migrate"], env={"DJANGO_SETTINGS_MODULE": f"{self.project_name}.settings_svs"})

    def django_loaddata(self, fixture):
        """Load Django fixtures."""
        print(f"🟩 Load Django fixtures '{fixture}'...")
        self.command([self.VENV_DIR / "bin" / "python", self.MANAGE_PY, "loaddata", fixture], env={"DJANGO_SETTINGS_MODULE": f"{self.project_name}.settings_svs"})
        
    def django_setup(self, domain, port):
        """Set up Django project with Gunicorn and systemd."""

        print(f"🟩 Setting up Django project on domain '{self.domain}'")
        self.create_venv(self.domain)

        self.django_create_settings_svs()
        self.django_migrate()
        self.django_collect_static()

        self.systemd_setup(port)

    def django_clean(self):
        """Clean Django project setup (remove systemd service, virtual environment, and .svs file)."""
        #if self.VENV_DIR.exists():
        #    print(f"🟩 Removing virtual environment {self.VENV_DIR} ...")
        #    self.VENV_DIR.rmdir()

        if self.settings_file_svs.exists():
            print(f"🟩 Removing alternate settings file {self.settings_file_svs} ...")
            self.settings_file_svs.unlink()

    # systemd

    def systemd_exists(self):
        units = self.command(["systemctl", "--user", "list-unit-files", "--type=service", "--no-pager"]).splitlines()
        for line in units:
            if line.startswith(f"{self.domain}.service"):
                return True
        raise SystemdException(f"Service '{self.domain}' not found in systemd unit files")

    def systemd_daemon_reload(self):
        print("🟩 Reload systemd daemon config...")
        self.command(["systemctl", "--user", "daemon-reload"])

    def systemd_enable(self):
        print("🟩 Enable systemd daemon...")
        self.command(["systemctl", "--user", "enable", f"{self.domain}.service"])

    def systemd_status(self):
        lines = self.command(["systemctl", "--user", "status", f"{self.domain}.service", "--no-pager"], check=False).splitlines()
        for line in lines:
            line=line.strip()
            if line.startswith("Active:"):
                key, value = line.split(":", 1)
                status = value.strip().split(" ", 1)[0].strip()
                return status
        raise SystemdException(f"Error parsing service systemd '{self.domain}.service' status")

    def systemd_is_active(self):
        status = self.systemd_status()
        return status=="active"

    def systemd_start(self):
        self.systemd_exists()
        if not self.systemd_is_active():
            print("🟩 Starting gunicorn service...")
            self.command(["systemctl", "--user", "start", f"{self.domain}.service"])
            if not self.systemd_is_active():
                raise SystemdException(f"Failed to start service '{self.domain}'")

    def systemd_stop(self):
        self.systemd_exists()
        if self.systemd_is_active():
            print("🟩 Stopping gunicorn service...")
            self.command(["systemctl", "--user", "stop", f"{self.domain}.service"])
            if self.systemd_is_active():
                raise SystemdException(f"Failed to stop service '{self.domain}'")

    def systemd_restart(self):
        self.systemd_exists()
        print("🟩 Restarting gunicorn service...")
        self.command(["systemctl", "--user", "restart", f"{self.domain}.service"])
        if not self.systemd_is_active():
            raise SystemdException(f"Failed to restart service '{self.domain}'")

    def systemd_setup(self, port):
        """Set up systemd service for the Django project."""

        systemd_service_file = self.SYSTEMD_DIR / f"{self.domain}.service"
        systemd_env_file = self.SYSTEMD_DIR / f"{self.domain}.service.env"

        if not self.SYSTEMD_DIR.exists():
            print(f"🟩 Creating systemd directory {self.SYSTEMD_DIR} ...")
            self.SYSTEMD_DIR.mkdir(parents=True, exist_ok=True)

        if not self.LOGS_DIR.exists():
            print(f"🟩 Creating logs directory {self.LOGS_DIR} ...")
            self.LOGS_DIR.mkdir(parents=True, exist_ok=True)

        print("🟩 Creating systemd env file '{systemd_env_file}'...")
        with systemd_env_file.open("w") as f:
            f.write(f"DJANGO_SETTINGS_MODULE={self.project_name}.settings_svs\n")

        print("🟩 Creating systemd service file '{systemd_service_file}'...")
        gunicorn_exec= (self.VENV_DIR / "bin" / "gunicorn").absolute()
        executable = f"{gunicorn_exec} --workers 2 --bind :{port} --access-logfile {self.LOGS_DIR}/access.log --error-logfile {self.LOGS_DIR}/error.log --capture-output {self.project_name}.wsgi:application"

        service_content = f"""[Unit]
Description=Gunicorn instance to serve {self.project_name} at {self.domain}
After=network.target

[Service]
Type=simple
WorkingDirectory={self.dir.absolute()}
EnvironmentFile={systemd_env_file.absolute()}
ExecStart={executable}

[Install]
WantedBy=default.target
"""
        with systemd_service_file.open("w") as f:
            f.write(service_content)

        media_symlink = self.SVS_STATIC_ROOT / self.domain / "media"
        media_dir = self.dir / "media"
        if not media_symlink.exists():
            if not media_dir.exists():
                print(f"🟨 Media directory {media_dir} not found, creating (might cause problems if included in git repo in the future)")
                media_dir.mkdir(parents=True, exist_ok=True)
            
            print(f"🟩 Creating symlink from '{media_symlink}' to '{media_dir}' ...")
            media_symlink.symlink_to(media_dir)
      
        if self.systemd_is_active(): # might be active from previous setup
            self.systemd_stop()

        self.systemd_daemon_reload()
        self.systemd_enable()
        self.systemd_start()
        self.command(["loginctl", "enable-linger"])
        
    def systemd_clean(self):
        systemd_service_file = self.SYSTEMD_DIR / f"{self.domain}.service"
        systemd_env_file = self.SYSTEMD_DIR / f"{self.domain}.env"
        
        try:
            self.systemd_stop()
        except SystemdException as e:
            print(f"🟨 Exception while stopping service: {e}")

        if systemd_service_file.exists():
            print(f"🟩 Removing systemd service file {systemd_service_file} ...")
            systemd_service_file.unlink()
        
        if systemd_env_file.exists():
            print(f"🟩 Removing systemd env file {systemd_env_file} ...")
            systemd_env_file.unlink()

        self.command(["systemctl", "--user", "daemon-reload"])

    # journalctl

    def journalctl_messages(self):
        print("🟩 Displaying journalctl messages:")
        messages=self.command(["journalctl", "--user-unit", f"{self.domain}.service", "-n", "20"]).splitlines()
        for message in messages:
            print(message)

    # utility

    def setup(self):
        """Setup Django project for svs.gyarab.cz."""
        if not self.domain:
            while True:
                domain = input("❓ Enter domain name (in form *.svs.gyarab.cz or other valid domain naime): ")
                if not self.is_valid_svs_domain(domain) and not self.is_valid_domain(domain):
                    print(f"🟨 Domain {domain} is invalid domain name.")
                else:
                    self.domain=domain
                    self.save_config()
                    break

        port = self.avava_web_register(self.domain)
        self.django_setup(self.domain, port)
        print(f"🟩 Setup complete. Your Django project is now running on https://{self.domain}/")

    def update(self):
        if not self.domain:
            raise SVSException(f"Domain name not found in configuration file. Run setup first.")
        
        print("🟩 Update git repository...")
        self.command(["git", "pull"])
        
        self.django_migrate()
        self.django_collect_static()
        self.systemd_restart()
        print("🟩 Update complete.")

    def info(self):
        domains = self.avava_web_list()
        if self.domain:
            print(f"🟩 Project domain '{self.domain}'")
            self.systemd_exists()
            status = self.systemd_status()
            if "active" in status:
                print(f"🟩 Service '{self.domain}' running")
            else:
                print(f"🟨 Service '{self.domain}' not running ('{status}')")
            self.journalctl_messages()
        else:
            print("🟨 Project domain not set.")

    def clean(self):
        if not self.domain:
            raise SVSException(f"Domain name not found in configuration file. Run setup first.")
        self.systemd_clean()
        self.django_clean()
        self.avava_web_unregister(self.domain)
        self.SVS_CONFIG_FILE.unlink()
        print("🟩 Cleanup complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage Django project for svs.gyarab.cz. Script must be run from the Django project directory, where manage.py is located.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    setup_parser = subparsers.add_parser("setup", help="Setup Django project for svs.gyarab.cz")
    info_parser = subparsers.add_parser("info", help="Show information about the Django project setup")
    update_parser = subparsers.add_parser("update", help="Update Django project (run git pull, migrations, reload static files and restart service)")
    clean_parser = subparsers.add_parser("clean", help="Clean up Django project setup (delete created config files and stop systemd service)")
    loaddata_parser = subparsers.add_parser("loaddata", help="Load Django fixtures")
    loaddata_parser.add_argument("fixture", help="Fixture file to load")
    help_parser = subparsers.add_parser("help", help="Show this help message")

    args = parser.parse_args()

    if args.command == "help" or args.command is None:
        parser.print_help()
    else:
        svs = SVS()
        try:
            svs.load()
            if args.command == "setup":
                svs.setup()
            elif args.command == "info":
                svs.info()
            elif args.command == "update":
                svs.update()
            elif args.command == "clean":
                svs.clean()
            elif args.command == "loaddata":
                svs.django_loaddata(args.fixture)
        except SystemdException as e:
            print(f"🟥 {e.__class__.__name__}: {e}")
            svs.journalctl_messages()
        except SVSException as e:
            print(f"🟥 {e.__class__.__name__}: {e}")
