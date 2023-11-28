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

    server.wait()
    tailwind.kill()
