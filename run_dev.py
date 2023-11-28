import signal
import subprocess
import time

if __name__ == "__main__":
    tailwind = subprocess.Popen(
        "npx tailwindcss -i ./readverse/css/main.css -o ./readverse/static/style.css --watch",
        shell=True,
    )
    print("Waiting 5 seconds until tailwind boots up...")
    time.sleep(5)

    server = subprocess.Popen(
        "flask run --debug",
        shell=True,
    )

    def kill_servers_exit(_, __):
        server.kill()
        tailwind.kill()
        exit()

    signal.signal(signal.SIGINT, kill_servers_exit)
    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            kill_servers_exit(None, None)
