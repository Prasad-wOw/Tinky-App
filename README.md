# OmniType

> **AI-powered inline text enhancement for Windows** — fix grammar, translate, change tone, or ask AI questions without leaving your keyboard.

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/UI-PySide6-41CD52.svg)](https://doc.qt.io/qtforpython/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows-0078D4.svg)](https://www.microsoft.com/windows)

---

## ✨ Features

OmniType listens to what you type in **any** Windows application and acts on short trigger suffixes you append to your text. No copy-paste, no switching apps — just type and trigger.

| Trigger | Action |
|---|---|
| `.g` | Fix grammar & spelling |
| `.ta` | Ask the AI a question (answer replaces text) |
| `.tr` | Translate to your configured target language |
| `.polite` | Rewrite in a polite tone |
| `.professional` | Rewrite in a professional tone |
| `.friendly` | Rewrite in a friendly tone |
| `.casual` | Rewrite in a casual tone |
| `.formal` | Rewrite in a formal tone |
| `...instruction...` | Custom rewrite with your own instruction |
| `.undo` | Undo the last AI replacement |

**Key highlights**

- 🔒 **Privacy-first** — API keys are AES-encrypted at rest; raw text is never logged
- 🪶 **Lightweight** — lives in the system tray, < 60 MB RAM at idle
- ⚡ **Fast** — median latency ≈ 800 ms (Gemini Flash)
- 🔌 **Multi-provider** — Gemini, OpenAI, Cloudflare Workers AI, Ollama (local)
- 🛠 **Fully configurable** — all triggers, timeouts, and history retention are adjustable
- 🖥 **Single `.exe`** — distribute as one file with PyInstaller

---

## 🚀 Installation

### Prerequisites

- Windows 10 / 11 (64-bit)
- Python 3.11 or newer (for running from source)
- An API key for at least one supported AI provider

### From source

```bash
git clone https://github.com/your-org/OmniType.git
cd OmniType
pip install -r requirements.txt
python -m omnitype.main
```

### From the pre-built `.exe`

Download `OmniType.exe` from the [Releases](https://github.com/your-org/OmniType/releases) page and double-click it. No Python installation required.

---

## ⚡ Quick Start

1. **Launch** OmniType (source: `python -m omnitype.main` | exe: double-click).
2. The **OmniType tray icon** (⌨) appears in the system tray.
3. Right-click the icon → **Settings** → enter your API key.
4. Open **any** text field (Notepad, Word, browser address bar, chat, email …).
5. Type some text followed by a trigger:

   ```
   i goed to the market yesterday .g
   ```

6. OmniType erases the trigger buffer and types the corrected text **in place**.

That's it. No clipboard gymnastics required.

---

## ⚙️ Configuration

OmniType stores its configuration at:

```
%APPDATA%\OmniType\config.toml
```

The first run copies `config.default.toml` there if no file exists.

### Full `config.toml` reference

```toml
[ai]
# Provider: "gemini" | "openai" | "cloudflare" | "ollama"
ai_provider          = "gemini"
# API key stored AES-encrypted — edit via Settings UI, not by hand
api_key_encrypted    = ""
# Model name (provider-specific)
model                = "gemini-1.5-flash"
# Base URL — for OpenAI-compatible endpoints or Cloudflare
base_url             = ""
# Cloudflare account ID (only used when ai_provider = "cloudflare")
cloudflare_account_id = ""
# Sampling temperature 0.0–1.0 (lower = more deterministic)
temperature          = 0.7
# Default target language for .tr translate trigger
translation_target_language = "English"
# Master on/off switch (also toggled from tray menu)
enabled              = true

[triggers]
trigger_grammar      = ".g"
trigger_ask          = ".ta"
trigger_translate    = ".tr"
trigger_polite       = ".polite"
trigger_professional = ".professional"
trigger_friendly     = ".friendly"
trigger_casual       = ".casual"
trigger_formal       = ".formal"
trigger_undo         = ".undo"

[ui]
# "dark" or "light"
theme                      = "dark"
show_notifications         = true
start_with_windows         = false
# How long overlay notifications stay on screen (ms); 0 = sticky
notification_duration_ms   = 2000

[privacy]
# History entries older than this are auto-purged (minutes)
history_duration_minutes   = 5
# Maximum entries kept in history table
max_history_entries        = 50
# Wipe clipboard contents after pasting AI result
clear_clipboard_after_paste = true
```

---

## 🤖 AI Provider Setup

### Gemini (default, recommended)

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey) and create a free API key.
2. Open OmniType → Settings → **AI Provider** → select **Gemini**.
3. Paste the key in the **API Key** field.
4. Recommended model: `gemini-1.5-flash` (fast & cheap) or `gemini-1.5-pro`.

### OpenAI

1. Visit [platform.openai.com/api-keys](https://platform.openai.com/api-keys) and generate a key.
2. Settings → **AI Provider** → **OpenAI**.
3. Model: `gpt-4o-mini` (cheapest), `gpt-4o`, or any other chat model.

### Cloudflare Workers AI

1. Log in to the [Cloudflare Dashboard](https://dash.cloudflare.com/).
2. Workers & Pages → **Workers AI** → create an API token.
3. Settings → **AI Provider** → **Cloudflare**.
4. Fill **API Key**, **Account ID**, and choose a model (e.g. `@cf/meta/llama-3-8b-instruct`).

### Ollama (local / offline)

1. Install [Ollama](https://ollama.ai) and pull a model: `ollama pull llama3`.
2. Ensure Ollama is running (`ollama serve`).
3. Settings → **AI Provider** → **Ollama**.
4. **Base URL**: `http://localhost:11434` (default).
5. **Model**: `llama3`, `mistral`, `phi3`, etc.

> **Tip:** Ollama is the only provider that works fully offline — no API key needed.

---

## 🔑 Trigger Reference

### Built-in triggers

| Trigger suffix | Type | Description |
|---|---|---|
| `.g` | `grammar` | Correct grammar, spelling, and punctuation |
| `.ta` | `ask_ai` | Ask a question; the AI's answer replaces your text |
| `.tr` | `translate` | Translate to `translation_target_language` |
| `.polite` | `tone` | Rewrite in a polite, courteous tone |
| `.professional` | `tone` | Rewrite in a professional business tone |
| `.friendly` | `tone` | Rewrite in a warm, friendly tone |
| `.casual` | `tone` | Rewrite in a relaxed, casual tone |
| `.formal` | `tone` | Rewrite in a formal academic/legal tone |
| `.undo` | `undo` | Restore the text from before the last AI replacement |

### Custom rewrite trigger

Surround an instruction with triple-dots:

```
meeting at 3pm tmrw ...translate to bullet points...
```

OmniType will apply `translate to bullet points` as a custom instruction.

### Changing trigger strings

All triggers are configurable in `config.toml` or via **Settings → Triggers**. For example, to use `.fix` instead of `.g`:

```toml
[triggers]
trigger_grammar = ".fix"
```

---

## 🏗 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         OmniType Process                            │
│                                                                     │
│  ┌──────────────┐     ┌──────────────────┐     ┌────────────────┐  │
│  │  Keyboard    │────▶│  TriggerParser   │────▶│  OmniTypeApp   │  │
│  │  Listener   │     │  (pattern match) │     │  (Qt main thd) │  │
│  │  (bg thread)│     └──────────────────┘     └───────┬────────┘  │
│  └──────────────┘                                      │           │
│                                                        ▼           │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                     Pipeline (_process_trigger)             │   │
│  │  1. Validate text   2. Build prompt   3. AI call (async)    │   │
│  │  4. Replace text    5. Undo stack     6. History DB         │   │
│  └──────────────────────────────┬──────────────────────────────┘   │
│                                 │                                   │
│          ┌──────────────────────┼──────────────────────┐           │
│          ▼                      ▼                      ▼           │
│  ┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐  │
│  │ AI Provider  │    │  TextReplacer    │    │  History/Undo    │  │
│  │ (aiohttp)    │    │  (keyboard+clip) │    │  (aiosqlite)     │  │
│  └──────────────┘    └──────────────────┘    └──────────────────┘  │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │   UI Layer: SystemTray | SettingsWindow | NotificationWidget│   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

**Package layout**

```
omnitype/
├── main.py                  # Entry point (single-instance, qasync loop)
├── app.py                   # OmniTypeApp orchestrator
├── core/
│   ├── keyboard_listener.py # Background keyboard hook (pynput)
│   ├── trigger_parser.py    # Pattern matching → TriggerMatch
│   ├── replacer.py          # Backspace + clipboard paste
│   ├── undo_manager.py      # In-memory undo stack
│   └── history_manager.py   # Async DB history recorder
├── ai/
│   ├── base_provider.py     # ABC for all AI providers
│   ├── gemini_provider.py   # Google Gemini via REST
│   ├── openai_provider.py   # OpenAI / compatible via REST
│   ├── cloudflare_provider.py
│   ├── ollama_provider.py   # Local Ollama
│   └── provider_factory.py  # ProviderFactory + PromptBuilder
├── ui/
│   ├── tray.py              # QSystemTrayIcon
│   ├── settings_window.py   # Settings dialog (PySide6)
│   ├── history_window.py    # History viewer
│   └── notification_widget.py  # Overlay toast
├── storage/
│   ├── config.py            # AppConfig dataclass + TOML I/O
│   └── database.py          # aiosqlite DatabaseManager
├── security/
│   └── encryption.py        # Fernet AES key encryption
└── utils/
    ├── logger.py            # Structured logging setup
    └── helpers.py           # Misc utilities
```

---

## 🛠 Development Guide

### Set up the development environment

```bash
# Clone the repository
git clone https://github.com/your-org/OmniType.git
cd OmniType

# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate   # Windows

# Install all dependencies including dev tools
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### `requirements.txt` (runtime)

```
PySide6>=6.6.0
qasync>=0.27.0
aiohttp>=3.9.0
aiosqlite>=0.19.0
keyboard>=0.13.5
pyperclip>=1.8.2
pyautogui>=0.9.54
pynput>=1.7.6
cryptography>=42.0.0
pywin32>=306
psutil>=5.9.0
tomli>=2.0.0 ; python_version < "3.11"
tomli-w>=1.0.0
```

### `requirements-dev.txt` (development only)

```
pytest>=8.0.0
pytest-asyncio>=0.23.0
pytest-qt>=4.4.0
pytest-mock>=3.14.0
pyinstaller>=6.5.0
ruff>=0.4.0
mypy>=1.10.0
```

### Running the app from source

```bash
python -m omnitype.main
```

Or using the module entry point defined in `pyproject.toml`:

```bash
omnitype
```

### Running tests

```bash
# Run all tests
pytest omnitype/tests/ -v

# Run a specific test file
pytest omnitype/tests/test_trigger_parser.py -v

# Run with coverage
pytest omnitype/tests/ --cov=omnitype --cov-report=html
```

### Code style

OmniType uses **Ruff** for linting and formatting:

```bash
ruff check omnitype/
ruff format omnitype/
```

Type checking with mypy:

```bash
mypy omnitype/ --ignore-missing-imports
```

---

## 📦 Building the `.exe`

### Requirements

```bash
pip install pyinstaller>=6.5.0
```

### Build command

```bash
pyinstaller OmniType.spec
```

The output will be at `dist/OmniType.exe` — a single self-contained executable (~80–120 MB depending on Qt modules included).

### Customising the build

- **Icon**: replace `assets/icon.ico` with your own 256×256 `.ico` file.
- **Version info**: edit the `version` field in `OmniType.spec` or add a `version.rc` resource file.
- **One-directory mode**: remove `a.binaries`, `a.zipfiles`, `a.datas` from the `EXE()` call and add a `COLLECT()` step to produce a folder instead.

---

## 🔒 Privacy & Security

| Concern | How OmniType handles it |
|---|---|
| **API keys** | Encrypted with AES-256 (Fernet) before writing to `config.toml`; key derived from machine-specific entropy |
| **Text content** | Never logged — only character counts are written to the log file |
| **History** | Stored locally in `%APPDATA%\OmniType\omnitype.db`; auto-purged after `history_duration_minutes` |
| **Clipboard** | Optionally wiped after paste (`clear_clipboard_after_paste = true`) |
| **Network** | Only outbound HTTPS to the configured AI provider; no telemetry |
| **Single instance** | Enforced via Windows named mutex — no inter-process RPC |

> **Note:** When using cloud AI providers (Gemini, OpenAI, Cloudflare), your text is sent to their servers subject to their privacy policies. Use **Ollama** for fully local, offline processing.

---

## 🔧 Troubleshooting

### OmniType doesn't detect my typing

- **Run as Administrator** — `keyboard` and `pynput` require elevated privileges in some Windows configurations.
- Check that OmniType is enabled: right-click tray icon → **Enable OmniType**.
- Some applications (e.g. UAC dialogs, full-screen games) block global keyboard hooks by design.

### The text replacement types in the wrong window

- OmniType targets the **foreground window at the time the trigger fires**. Avoid switching focus between typing and the trigger suffix.

### The AI response is slow

- For cloud providers: check your network connection and API quota.
- Switch to a faster model (e.g. `gemini-1.5-flash` instead of `gemini-1.5-pro`).
- For Ollama: ensure the model is fully loaded (`ollama run <model>` in a terminal).

### I see "Nothing to undo"

- The undo stack only holds the **most recent** replacement from the current session. Restarting OmniType clears the undo history.

### Settings window won't open

- If the settings window is minimised to the taskbar, it may not come to focus. Look for it in the Windows taskbar.

### API key validation fails

- Double-check the key has no leading/trailing spaces.
- Ensure the selected provider matches the key type (e.g. an OpenAI key won't work with Gemini).

### Log file location

```
%APPDATA%\OmniType\omnitype.log
```

Enable `DEBUG` level logging by setting the environment variable `OMNITYPE_LOG_LEVEL=DEBUG` before launching.

---

## 🤝 Contributing

Pull requests and issues are welcome! Please follow these guidelines:

1. **Fork** the repo and create a feature branch: `git checkout -b feat/my-feature`.
2. Write tests for any new functionality.
3. Run the full test suite: `pytest omnitype/tests/ -v`.
4. Run linting: `ruff check omnitype/ && ruff format omnitype/`.
5. Open a pull request with a clear description of your changes.

### Commit message convention

```
type(scope): short description

feat(triggers): add .summarize trigger
fix(replacer): handle zero total_chars edge case
docs(readme): update Ollama setup instructions
test(history): add concurrent record test
```

### Areas we'd love help with

- macOS / Linux port (replace `pywin32` hooks with cross-platform equivalents)
- Additional AI provider adapters (Anthropic Claude, Cohere, etc.)
- UI polish and accessibility improvements
- End-to-end integration tests

---

## 📄 License

OmniType is released under the **MIT License**. See [LICENSE](LICENSE) for the full text.

---

## 🙏 Acknowledgements

- [PySide6](https://doc.qt.io/qtforpython/) — Qt for Python
- [qasync](https://github.com/CabbageDevelopment/qasync) — asyncio integration for Qt
- [keyboard](https://github.com/boppreh/keyboard) — Global keyboard hooks
- [pynput](https://github.com/moses-palmer/pynput) — Input device monitoring
- [aiohttp](https://docs.aiohttp.org/) — Async HTTP client
- [cryptography](https://cryptography.io/) — Fernet AES encryption
- [aiosqlite](https://github.com/omnilib/aiosqlite) — Async SQLite

---

*Built with ❤️ as a Capstone project at VIT University.*
