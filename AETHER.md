# AETHER

AETHER is Agastya Tomar (Aadi)'s customized personal AI assistant built from the uploaded PersonalJarvis codebase.

## Identity
- **Product:** AETHER
- **Assistant voice name:** ATHER
- **Owner/developer:** Agastya Tomar (Aadi)
- **Repository target:** `agastyatomar/AETHER`
- **Wake phrases:** `Hey ATHER` and `ATHER`

## Voice behavior
- Say `Hey ATHER` or `ATHER` to activate voice listening.
- After activation, AETHER accepts the spoken command through the existing speech pipeline.
- Existing push-to-talk/hotkey fallbacks remain available where wake-word support is unavailable.
- Wake configuration remains user-editable; the ATHER aliases are the shipped default.

## Compatibility
Internal Python module names such as `jarvis` are retained where renaming them would risk breaking the existing architecture. User-facing product branding, package metadata, desktop identity, repository links, and the default voice identity are AETHER/ATHER.

## Upstream attribution
The repository retains the applicable upstream license and attribution notices. This customization does not remove upstream legal notices.
