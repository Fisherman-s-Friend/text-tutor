import subprocess
import os
import sys
import platform


def activate_venv():
    if platform.system() == "Windows":
        return os.path.join("flask-server", "venv", "Scripts", "activate")
    else:
        return os.path.join("flask-server", "venv", "bin", "activate")


def install_flask_dependencies():
    activate_script = activate_venv()
    requirements_file = os.path.join("flask-server", "requirements.txt")

    if platform.system() == "Windows":
        subprocess.run(
            f"{activate_script} && pip install -r {requirements_file}", shell=True
        )
    else:
        subprocess.run(
            f"source {activate_script} && pip install -r {requirements_file}",
            shell=True,
            executable="/bin/bash",
        )


def install_react_dependencies():
    client_dir = os.path.join("client")
    subprocess.run("npm install", cwd=client_dir, shell=True)


def create_and_activate_venv():
    venv_dir = os.path.join("flask-server", "venv")
    if not os.path.exists(venv_dir):
        subprocess.run([sys.executable, "-m", "venv", venv_dir])
    activate_script = activate_venv()

    if platform.system() == "Windows":
        return f"{activate_script} &&"
    else:
        return f"source {activate_script} &&"


def start_flask_server():
    activate_script = activate_venv()
    server_script = os.path.join("flask-server", "server.py")

    if platform.system() == "Windows":
        subprocess.run(f"{activate_script} && python {server_script}", shell=True)
    else:
        subprocess.run(
            f"source {activate_script} && python {server_script}",
            shell=True,
            executable="/bin/bash",
        )


def start_react_client():
    client_dir = os.path.join("client")
    subprocess.run("npm start", cwd=client_dir, shell=True)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "install_flask_dependencies":
            install_flask_dependencies()
        elif sys.argv[1] == "install_react_dependencies":
            install_react_dependencies()
        elif sys.argv[1] == "start_flask_server":
            start_flask_server()
        elif sys.argv[1] == "start_react_client":
            start_react_client()
    else:
        # Create and activate virtual environment for Flask server
        venv_activation_cmd = create_and_activate_venv()

        # Install dependencies for Flask and React
        subprocess.run([sys.executable, __file__, "install_flask_dependencies"])
        subprocess.run([sys.executable, __file__, "install_react_dependencies"])

        # Start the Flask server in a new process
        flask_process = subprocess.Popen(
            [sys.executable, __file__, "start_flask_server"]
        )

        # Start the React client in a new process
        react_process = subprocess.Popen(
            [sys.executable, __file__, "start_react_client"]
        )

        # Wait for both processes to complete
        flask_process.wait()
        react_process.wait()
