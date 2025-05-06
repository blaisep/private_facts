import json
import os
import sys
from pathlib import Path
from .config import Config


APP_NAME = "Gridsync"

if sys.platform in ("win32", "darwin"):
    import certifi

    # Workaround for broken-by-default certificate verification on Windows.
    # See https://github.com/twisted/treq/issues/94#issuecomment-116226820
    # TLS certificate verification was also observed to be broken on macOS
    # 10.16 <https://github.com/gridsync/gridsync/issues/459> -- and using
    # `certifi`'s CA bundle reportedly fixed it.
    os.environ["SSL_CERT_FILE"] = certifi.where()


if getattr(sys, "frozen", False):
    pkgdir = os.path.dirname(os.path.realpath(sys.executable))
    if sys.platform == "darwin":
        pkgdir_resources = str(
            Path(Path(pkgdir).parent, "Resources", "resources")
        )
    else:
        pkgdir_resources = str(Path(pkgdir, "_internal", "resources"))
    os.environ["PATH"] += os.pathsep + pkgdir
    os.environ["PATH"] += os.pathsep + os.path.join(pkgdir, "Tahoe-LAFS")
    os.environ["PATH"] += os.pathsep + os.path.join(pkgdir, "magic-folder")
    if sys.platform == "win32":
        # Workaround for PyInstaller being unable to find Qt5Core.dll on PATH.
        # See https://github.com/pyinstaller/pyinstaller/issues/4293
        _meipass = getattr(sys, "_MEIPASS", "")
        if _meipass:
            os.environ["PATH"] = _meipass + os.pathsep + os.environ["PATH"]
    try:
        del sys.modules["twisted.internet.reactor"]  # PyInstaller workaround
    except KeyError:
        pass
    if sys.platform not in ("win32", "darwin"):
        # PyInstaller's bootloader sets the 'LD_LIBRARY_PATH' environment
        # variable to the root of the executable's directory which causes
        # `xdg-open` -- and, by extension, QDesktopServices.openUrl() -- to
        # fail to properly locate/launch applications by MIME-type/URI-handler.
        # Unsetting it globally here fixes this issue.
        os.environ.pop("LD_LIBRARY_PATH", None)
else:
    pkgdir = os.path.dirname(os.path.realpath(__file__))
    pkgdir_resources = os.path.join(pkgdir, "resources")


settings = Config(os.path.join(pkgdir_resources, "config.txt")).load()

def _load_grid_settings() -> dict[str, dict]:
    results: dict[str, dict] = {}
    for p in Path(pkgdir_resources, "providers").glob("*-*.json"):
        try:
            s = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.decoder.JSONDecodeError):
            continue
        n = s.get("nickname")
        if n:
            results[n] = s
    return results

grid_settings = _load_grid_settings()

for envvar, value in os.environ.items():
    if envvar.startswith("GRIDSYNC_"):
        words = envvar.split("_")
        if len(words) >= 3:
            section = words[1].lower()
            option = "_".join(words[2:]).lower()
            try:
                settings[section][option] = value
            except KeyError:
                settings[section] = {option: value}

#Define config_dir
if sys.platform == "win32":
    appdata = str(os.getenv("APPDATA"))
    config_dir = os.path.join(appdata, APP_NAME)
    autostart_file_path = os.path.join(
        appdata,
        "Microsoft",
        "Windows",
        "Start Menu",
        "Programs",
        "Startup",
        APP_NAME + ".lnk",
    )
elif sys.platform == "darwin":
    config_dir = os.path.join(
        os.path.expanduser("~"), "Library", "Application Support", APP_NAME
    )
    autostart_file_path = os.path.join(
        os.path.expanduser("~"), "Library", "LaunchAgents", APP_NAME + ".plist"
    )
    # Required for macOS 11 ("Big Sur") compatibility.
    # See https://github.com/gridsync/gridsync/issues/319
    os.environ["QT_MAC_WANTS_LAYER"] = "1"
else:
    config_home = os.environ.get(
        "XDG_CONFIG_HOME", os.path.join(os.path.expanduser("~"), ".config")
    )
    config_dir = os.path.join(config_home, APP_NAME.lower())
    autostart_file_path = os.path.join(
        config_home, "autostart", APP_NAME + ".desktop"
    )