"""Freeze the persistent product identity values used by existing installs."""

from __future__ import annotations

import importlib
import os

import pytest

import jarvis.core.branding as branding

_CURRENT_IDENTITY = {
    "PRODUCT_NAME": "AETHER",
    "PRODUCT_COMPACT_NAME": "AETHER",
    "PRODUCT_SLUG": "aether",
    "CONFIG_FILE_NAME": "jarvis.toml",
    "KEYRING_SERVICE_NAME": "aether",
    "CONTROL_KEY_PREFIX": "jctl_",
    "SESSION_COOKIE_NAME": "jarvis_session",
    "MANAGED_INSTALL_MARKER": ".jarvis-managed-install",
    "DEFAULT_INSTALL_DIR_NAME": ".aether",
    "WINDOWS_USER_DATA_DIR_NAME": "Jarvis",
    "FALLBACK_USER_DATA_DIR_NAME": ".jarvis",
    "DESKTOP_OUTPUT_MIRROR_DIR_NAME": "Jarvis-Output",
    "WINDOWS_MUTEX_NAME": r"Global\AETHER_v1",
    "WINDOWS_APP_USER_MODEL_ID": "AETHER.AETHER",
    "WINDOWS_UNINSTALL_REGISTRY_SUBKEY": (
        r"Software\Microsoft\Windows\CurrentVersion\Uninstall\AETHER"
    ),
    "WINDOWS_AUTOSTART_TASK_NAME": "AETHER Autostart",
    "WINDOWS_SHORTCUT_FILE_NAME": "AETHER.lnk",
    "WINDOWS_AUTOSTART_DESCRIPTION": "AETHER (Autostart)",
    "WINDOWS_BRANDED_LAUNCHER_FILE_NAME": "AETHER.exe",
    "WINDOWS_BRANDED_LAUNCHER_DIR_NAME": "AETHER",
    "WINDOWS_BRANDED_LAUNCH_ENV_VAR": "JARVIS_BRANDED_LAUNCH",
    "MACOS_APP_NAME": "AETHER",
    "MACOS_APP_DIR_NAME": "AETHER.app",
    "MACOS_EXECUTABLE_NAME": "AETHER",
    "MACOS_BUNDLE_ID": "com.aether.desktop",
    "MACOS_AUTOSTART_LABEL": "com.aether.autostart",
    "LINUX_APP_NAME": "AETHER",
    "LINUX_DESKTOP_ENTRY_FILE_NAME": "aether.desktop",
    "LINUX_WM_CLASS": "aether",
    "DEFAULT_OFFICIAL_REPO_SLUG": "agastyatomar/AETHER",
    "OFFICIAL_REPO_SLUG_ENV_VAR": "JARVIS_OFFICIAL_REPO_SLUG",
    "OFFICIAL_REPO_SLUG": "agastyatomar/AETHER",
    "OFFICIAL_REPO_URL": "https://github.com/agastyatomar/AETHER",
    "OFFICIAL_REPO_GIT_URL": "https://github.com/agastyatomar/AETHER.git",
    "OFFICIAL_RELEASES_LATEST_API_URL": (
        "https://api.github.com/repos/agastyatomar/AETHER/releases/latest"
    ),
    "UPDATER_USER_AGENT": "AETHER-Updater",
}


def test_default_exported_identity_values_are_frozen() -> None:
    previous = os.environ.pop(branding.OFFICIAL_REPO_SLUG_ENV_VAR, None)
    try:
        module = importlib.reload(branding)
        actual = {name: getattr(module, name) for name in _CURRENT_IDENTITY}
        assert actual == _CURRENT_IDENTITY
    finally:
        if previous is not None:
            os.environ[branding.OFFICIAL_REPO_SLUG_ENV_VAR] = previous
        importlib.reload(branding)


def test_official_repo_slug_override_is_exact() -> None:
    assert (
        branding.resolve_official_repo_slug(
            {"JARVIS_OFFICIAL_REPO_SLUG": "RenamedOrg/RenamedRepo"}
        )
        == "RenamedOrg/RenamedRepo"
    )


@pytest.mark.parametrize(
    "value",
    [
        "owner",
        "owner/repo/extra",
        "/repo",
        "owner/",
        "owner/repo evil",
        " owner/repo",
        "owner/repo ",
    ],
)
def test_official_repo_slug_override_rejects_non_exact_values(value: str) -> None:
    with pytest.raises(ValueError, match="exact owner/repository slug"):
        branding.resolve_official_repo_slug({"JARVIS_OFFICIAL_REPO_SLUG": value})
