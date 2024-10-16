# SPDX-FileCopyrightText: 2024-present Mark Hall <mark.hall@open.ac.uk>
#
# SPDX-License-Identifier: MIT
"""Block 2 commands."""

import os
import shutil
import signal
import subprocess
from enum import Enum
from urllib.parse import urlparse

from rich import print as console
from typer import Exit, Typer

app = Typer()


class ExpoVersion(str, Enum):
    """Expo versions enumeration."""

    live = "live"
    sdk51 = "sdk51"


@app.command()
def run(part: int, activity: int, expo_version: ExpoVersion = ExpoVersion.live, clean_existing: bool = False) -> None:
    """Run a Block 2 activity."""
    dest_dir = os.path.join("work", f"Part{part}Activity{activity}")
    source_dir = os.path.join("resources", f"Part{part}Activity{activity}")
    if os.path.exists(os.path.join(source_dir, "App.jsx")) or os.path.exists(os.path.join(source_dir, "App.tsx")):
        run_expo_app(source_dir, dest_dir, expo_version, clean_existing)
    elif os.path.exists(os.path.join(source_dir, "app.js")) or os.path.exists(os.path.join(source_dir, "app.ts")):
        run_express_app(source_dir, dest_dir, clean_existing)
    else:
        run_webserver(source_dir, dest_dir, clean_existing)


def run_expo_app(source_dir: str, dest_dir: str, expo_version: ExpoVersion, clean_existing: bool) -> None:
    """Deploy and run an Expo app."""
    if clean_existing and os.path.exists(dest_dir):
        console(f":litter_in_bin_sign: Removing existing files in [cyan bold]{dest_dir}[/cyan bold]")
        shutil.rmtree(dest_dir)
    if os.path.exists(dest_dir):
        console(f":white_check_mark: Using existing files in [cyan bold]{dest_dir}[/cyan bold]")
    else:
        console(":hammer: Copying the Expo skeleton")
        if expo_version == ExpoVersion.live:
            shutil.copytree(os.path.join("skeletons", "reactnative"), dest_dir)
        elif expo_version == ExpoVersion.sdk51:
            shutil.copytree(os.path.join("skeletons", "sdk51dev"), dest_dir)
        console(":hammer: Copying the Project skeleton")
        if expo_version == ExpoVersion.sdk51 and os.path.exists(f"{source_dir}sdk51"):
            shutil.copytree(f"{source_dir}sdk51", dest_dir, dirs_exist_ok=True)
        else:
            shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)
    console(":hammer: Installing dependencies")
    result = subprocess.run(  # noqa: S603
        ["npm", "ci"],  # noqa: S607
        cwd=dest_dir,
        check=False,
    )
    if result.returncode == 0:
        console(":white_check_mark: Dependencies installed")
    else:
        console("[red bold]Error:[/red bold] Failed to correctly install the dependencies")
        raise Exit(code=1)
    if expo_version == ExpoVersion.live:
        console(":hammer: Installing dependencies")
        result = subprocess.run(  # noqa: S603
            ["npm", "ci"],  # noqa: S607
            cwd=os.path.join(dest_dir, "web"),
            check=False,
        )
        if result.returncode == 0:
            console(":white_check_mark: Dependencies installed")
        else:
            console("[red bold]Error:[/red bold] Failed to correctly install the dependencies")
            raise Exit(code=1)
        result = subprocess.run(  # noqa: S603
            ["npm", "run", "dev"],  # noqa: S607
            cwd=os.path.join(dest_dir, "web"),
            check=False,
        )
    elif expo_version == ExpoVersion.sdk51:
        console(":hammer: Exporting application")
        shutil.move(os.path.join(dest_dir, "App.jsx"), os.path.join(dest_dir, "App.js"))
        result = subprocess.run(  # noqa: S603
            ["npx", "expo", "export", "-p", "web"],  # noqa: S607
            cwd=dest_dir,
            check=False,
        )
        if result.returncode == 0:
            console(":white_check_mark: Exported")
        else:
            console("[red bold]Error:[/red bold] Export failed")
            raise Exit(code=1)
        console(":hammer: Installing local web server")
        result = subprocess.run(  # noqa: S603
            ["npm", "install", "local-web-server"],  # noqa: S607
            cwd=os.path.join(dest_dir, "dist"),
            check=False,
        )
        if result.returncode == 0:
            console(":white_check_mark: Local web server installeed")
        else:
            console("[red bold]Error:[/red bold] Local web server installation failed")
            raise Exit(code=1)
        app_base = os.environ["JUPYTERHUB_SERVICE_PREFIX"] if "JUPYTERHUB_SERVICE_PREFIX" in os.environ else "/"
        app_path = "http://localhost:5173"
        rewrite_path = ""
        if "VSCODE_PROXY_URI" in os.environ:
            url = urlparse(os.environ["VSCODE_PROXY_URI"])
            app_path = f"{url.scheme}://{url.netloc}"
            app_base = app_base + "proxy/absolute/5173"
            rewrite_path = f"{app_base}proxy/absolute/5173"
        app_path = app_path + app_base
        console(f"""Files shown in a directory listing are not hyperlinked correctly. Access files by modifying the URL.
press ctrl-c to quit
{app_path}""")

        if rewrite_path:
            process = subprocess.Popen(  # noqa: S603
                ["npx", "ws", "-p", "5173", "--rewrite", rewrite_path],  # noqa: S607
                cwd=os.path.join(dest_dir, "dist"),
                start_new_session=True,
            )
        else:
            process = subprocess.Popen(  # noqa: S603
                ["npx", "ws", "-p", "5173"],  # noqa: S607
                cwd=os.path.join(dest_dir, "dist"),
                start_new_session=True,
            )

        def cleanup(sig, frame) -> None:  # noqa:ARG001, ANN001
            """Local cleanup code."""
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            console(":hammer: Cleaning up")
            shutil.move(os.path.join(dest_dir, "App.js"), os.path.join(dest_dir, "App.jsx"))
            raise Exit()

        signal.signal(signal.SIGINT, cleanup)

        input()

        cleanup(None, None)


def run_express_app(source_dir: str, dest_dir: str, clean_existing: bool) -> None:
    """Deploy and run an express app."""
    if clean_existing and os.path.exists(dest_dir):
        console(f":litter_in_bin_sign: Removing existing files in [cyan bold]{dest_dir}[/cyan bold]")
        shutil.rmtree(dest_dir)
    if os.path.exists(dest_dir):
        console(f":white_check_mark: Using existing files in [cyan bold]{dest_dir}[/cyan bold]")
    else:
        console(":hammer: Copying the application skeleton")
        shutil.copytree(source_dir, dest_dir)
    console(":hammer: Installing express")
    result = subprocess.run(  # noqa: S603
        ["npm", "install", "express", "cors"],  # noqa: S607
        cwd=dest_dir,
        check=False,
    )
    if result.returncode == 0:
        console(":white_check_mark: Installed")
    else:
        console("[red bold]Error:[/red bold] Install failed")
        raise Exit(code=1)
    console("""Running the web service
Note: it is only accessible locally""")
    if os.path.exists(os.path.join(source_dir, "app.js")):
        result = subprocess.run(  # noqa: S603
            ["node", "app.js"],  # noqa: S607
            cwd=dest_dir,
            check=False,
        )
    elif os.path.exists(os.path.join(source_dir, "app.ts")):
        result = subprocess.run(  # noqa: S603
            ["npx", "tsc"],  # noqa: S607
            cwd=dest_dir,
            check=False,
        )
        result = subprocess.run(  # noqa: S603
            ["node", "app.js"],  # noqa: S607
            cwd=dest_dir,
            check=False,
        )


def run_webserver(source_dir: str, dest_dir: str, clean_existing: bool) -> None:
    """Run a webserver in the dest_dir."""
    if clean_existing and os.path.exists(dest_dir):
        console(f":litter_in_bin_sign: Removing existing files in [cyan bold]{dest_dir}[/cyan bold]")
        shutil.rmtree(dest_dir)
    if os.path.exists(dest_dir):
        console(f":white_check_mark: Using existing files in [cyan bold]{dest_dir}[/cyan bold]")
    else:
        console(":hammer: Copying the application skeleton")
        shutil.copytree(source_dir, dest_dir)
    console(":hammer: Installing the local web-server")
    result = subprocess.run(  # noqa: S603
        ["npm", "install", "local-web-server"],  # noqa: S607
        cwd=dest_dir,
        check=False,
    )
    if result.returncode == 0:
        console(":white_check_mark: Installed")
    else:
        console("[red bold]Error:[/red bold] Install failed")
        raise Exit(code=1)
    if os.path.exists(os.path.join(dest_dir, "build.sh")):
        console(":hammer: Running build script")
        result = subprocess.run(  # noqa: S603
            ["bash", "build.sh"],  # noqa: S607
            cwd=dest_dir,
            check=False,
        )
        if result.returncode == 0:
            console(":white_check_mark: Build script completed")
        else:
            console("[red bold]Error:[/red bold] Build script failed")
            raise Exit(code=1)

        app_base = os.environ["JUPYTERHUB_SERVICE_PREFIX"] if "JUPYTERHUB_SERVICE_PREFIX" in os.environ else "/"
        app_path = "http://localhost:5173"
        rewrite_path = ""
        if "VSCODE_PROXY_URI" in os.environ:
            url = urlparse(os.environ["VSCODE_PROXY_URI"])
            app_path = f"{url.scheme}://{url.netloc}"
            app_base = app_base + "proxy/absolute/5173"
            rewrite_path = f"{app_base}proxy/absolute/5173"
        app_path = app_path + app_base
        console(f"""Files shown in a directory listing are not hyperlinked correctly. Access files by modifying the URL.
press ctrl-c to quit
{app_path}""")

        if rewrite_path:
            subprocess.run(  # noqa: S603
                ["npx", "ws", "-p", "5173", "--rewrite", rewrite_path],  # noqa: S607
                cwd=dest_dir,
                check=False,
            )
        else:
            subprocess.run(  # noqa: S603
                ["npx", "ws", "-p", "5173"],  # noqa: S607
                cwd=dest_dir,
                check=False,
            )
