# Software Requirements Specification (SRS) for Tinky

## 1. Introduction

### 1.1 Purpose
This Software Requirements Specification (SRS) documents the complete requirements, architecture, and behavior of the **Tinky** application. It serves as a comprehensive guide for developers, stakeholders, and maintainers to understand the system's capabilities, constraints, and design.

### 1.2 Scope
**Tinky** is a background-running, omnipresent AI companion for Microsoft Windows. It allows users to harness the power of Large Language Models (LLMs) directly inside any application (e.g., MS Word, browsers, code editors) without copy-pasting or switching context. By typing specific text triggers (e.g., ` .g` for grammar correction), Tinky captures the preceding text, processes it via an AI provider, and replaces the original text in-place using keyboard automation.

### 1.3 Definitions and Acronyms
*   **SRS:** Software Requirements Specification
*   **LLM:** Large Language Model
*   **Trigger:** A specific sequence of characters (usually ending with a space and dot, e.g., ` .g`) that initiates an AI action.
*   **In-place Replacement:** The process of automatically deleting the user's typed text and pasting the AI-generated response in the active window.
*   **VFS:** Virtual File System (relevant to Windows Store Python environments).

---

## 2. Overall Description

### 2.1 Product Perspective
Tinky is a standalone Windows desktop application built using Python. It operates primarily in the system tray and relies on low-level OS hooks (keyboard monitoring, clipboard manipulation, and UI automation) to function seamlessly across the entire operating system. It interfaces with external cloud-based AI providers (such as OpenRouter, OpenAI) via REST APIs.

### 2.2 User Characteristics
The target audience ranges from casual users wanting quick grammar fixes to power users and professionals needing rapid translation, code generation, or tone adjustments without disrupting their workflow. Users are expected to have basic knowledge of obtaining an API key from an AI provider.

### 2.3 Operating Environment
*   **OS:** Microsoft Windows 10 and Windows 11 (64-bit).
*   **Hardware:** Standard modern PC (minimum 4GB RAM, active internet connection).
*   **Dependencies (Runtime):** Bundled Visual C++ 2022 x64 Redistributable.

### 2.4 Design and Implementation Constraints
*   **Security:** API keys must be securely encrypted at rest. The application must not trigger anti-virus heuristics maliciously.
*   **Performance:** Trigger detection must be instantaneous (under 50ms latency for keypresses) so it does not interfere with normal typing.
*   **OS Limitations:** Certain secured windows (e.g., UAC prompts, password fields, some remote desktop sessions) block global keyboard hooks or programmatic pasting. The app must handle these gracefully.

---

## 3. System Features

### 3.1 Global Keyboard Monitoring and Trigger Engine
*   **Description:** The system continually monitors keystrokes in the background using a rolling buffer to detect specific command patterns.
*   **Requirements:**
    *   Must maintain a lightweight ring buffer (e.g., last 2000 characters).
    *   Must detect predefined triggers (e.g., ` .g`, ` .tr`) and custom user-defined triggers.
    *   Must support dynamic instruction triggers using the triple-dot syntax (e.g., `make this a bulleted list ...ask...`).
    *   Must automatically pause monitoring when a password field is focused (heuristic detection).

### 3.2 In-Place Text Replacement
*   **Description:** Once a trigger is detected and AI processing completes, the app replaces the text in the active window.
*   **Requirements:**
    *   Must calculate the exact number of backspaces needed to delete the original text and the trigger.
    *   Must execute backspaces at a safe, configurable speed to prevent application freezing.
    *   Must paste the AI result using the system clipboard (`Ctrl+V`).
    *   Must restore the user's previous clipboard contents after pasting.

### 3.3 AI Provider Integration
*   **Description:** Handles the communication with LLM APIs.
*   **Requirements:**
    *   Primary support for **OpenRouter** (which routes to OpenAI, Anthropic, Gemini, etc.).
    *   Must handle network timeouts, rate limits, and API errors gracefully, showing a non-intrusive notification to the user.
    *   Must allow users to select specific models dynamically.

### 3.4 Custom Triggers
*   **Description:** Users can define their own shorthand triggers mapped to specific system prompts.
*   **Requirements:**
    *   Users can specify a trigger string (e.g., `.code`) and the underlying AI instruction ("Format this as a Python script").
    *   Changes must be applied to the trigger engine immediately without restarting the app.

### 3.5 History and Undo System
*   **Description:** Tracks recent AI generations and allows users to revert unwanted changes.
*   **Requirements:**
    *   Maintain a local SQLite database of past generations.
    *   Typing the undo trigger (e.g., ` .undo`) must fetch the most recent original text and replace the AI output.
    *   Must implement a periodic purge mechanism to delete history older than a user-defined threshold (e.g., 5 minutes) for privacy.

### 3.6 Settings and Dashboard Interface
*   **Description:** A graphical user interface for configuring the application.
*   **Requirements:**
    *   Built using PySide6 (Qt) featuring a modern, premium "glassmorphic" aesthetic.
    *   Provides sections for: General settings (Startup, API key), Triggers (Predefined & Custom), History viewer, and App info.
    *   Must encrypt the API key before saving it to the configuration file (`config.toml`).

---

## 4. Non-Functional Requirements

### 4.1 Performance Requirements
*   **Memory Footprint:** The application should consume less than 150MB of RAM while idling in the background.
*   **CPU Usage:** Keyboard listening must consume near 0% CPU under normal typing conditions.
*   **AI Latency:** The system must begin the replacement process immediately upon receiving the full response from the API.

### 4.2 Security Requirements
*   **Data Privacy:** All typed text not matching a trigger is immediately discarded from RAM. No keystrokes are ever logged to disk or sent to a server.
*   **API Key Protection:** Uses Fernet symmetric encryption. The encryption key is derived using PBKDF2HMAC tied to the local machine profile, meaning the `config.toml` cannot simply be copied to another machine to steal the API key.

### 4.3 Reliability and Robustness
*   **Single Instance Guard:** A local Windows Mutex (`Local\tinky_SingleInstance_Mutex_v1`) ensures only one instance of Tinky runs at a time. If a user tries to launch a second instance, the existing dashboard is brought to the foreground.
*   **Fallback Capture:** If the rolling keyboard buffer doesn't contain the full text, the app will attempt a fallback `Ctrl+A` -> `Ctrl+C` capture method via COM automation or clipboard interaction.

---

## 5. System Architecture

### 5.1 Component Overview
1.  **Core Engine:** `keyboard_listener.py`, `trigger_parser.py`, `replacer.py`. Handles OS-level hooks and string manipulation.
2.  **AI Layer:** `provider_factory.py`. Manages asynchronous HTTP requests to OpenRouter.
3.  **Storage Layer:** `config.py`, `database.py`. Manages TOML configuration and aiosqlite history persistence.
4.  **Security Layer:** `encryption.py`. Manages local machine-bound Fernet encryption.
5.  **UI Layer:** PySide6 windows (`dashboard.py`, `settings_window.py`). Bound to the core engine using `qasync` for asyncio event loop integration.

### 5.2 Data Flow (Trigger Execution)
1.  User types "Hello world .g".
2.  `KeyboardListener` captures characters into the deque buffer.
3.  Upon spacebar or trigger completion, `TriggerParser` evaluates the buffer.
4.  Match found! `TriggerParser` extracts original text ("Hello world") and instruction ("Fix grammar").
5.  App core locks the keyboard/buffer.
6.  `ProviderFactory` sends the request to the LLM asynchronously.
7.  Response received ("Hello, world.").
8.  `TextReplacer` sends 14 backspaces (length of "Hello world .g").
9.  `TextReplacer` copies "Hello, world." to the clipboard.
10. `TextReplacer` sends `Ctrl+V`.
11. Clipboard is restored to its previous state.

---

## 6. Deployment and Distribution

*   **Compilation:** The Python source is compiled into a single executable (`Tinky.exe`) using **Nuitka**, avoiding the extraction overhead of PyInstaller and obfuscating the source code.
*   **Bundling:** VC++ 2022 runtime DLLs (`msvcp140.dll`, etc.) are bundled directly inside the executable to ensure compatibility on raw Windows installations.
*   **Installer:** An **Inno Setup 6** script (`setup.iss`) compiles a standard Windows installer (`Tinky-Setup-1.0.0.exe`).
*   **Privileges:** The installer and application are configured for a **per-user** installation (`%LocalAppData%`), requiring zero administrative privileges (No UAC prompts).
*   **Startup:** Configured via `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` registry keys to launch automatically upon user login.
