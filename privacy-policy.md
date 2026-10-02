# Privacy Policy for Tinky

**Last Updated:** July 22, 2026

Thank you for choosing Tinky ("we," "us," or "our"). We are committed to protecting your privacy and ensuring you have full control over your data. Because Tinky is a locally-installed productivity application that processes text via AI, transparency about how your data is handled is our highest priority.

This Privacy Policy explains how Tinky collects, uses, processes, and protects your information.

## 1. Core Philosophy: Local-First & Bring-Your-Own-Key
Tinky operates on a **"Local-First"** and **"Bring-Your-Own-Key" (BYOK)** architecture. 
- We do not run our own backend servers. 
- We do not collect telemetry, analytics, or usage data.
- We do not have access to your API keys, the text you write, or the AI responses you generate. 

## 2. Information Processing and Keyboard Hooks
To function as a universal text assistant, Tinky uses local operating system APIs (such as `SetWindowsHookEx`) to listen for specific keystrokes across different applications. 

**How the keyboard hook works:**
- **Volatile Memory Only:** Tinky maintains a small, rolling buffer of your recent keystrokes entirely in volatile system memory (RAM).
- **Trigger Detection:** This buffer is continuously scanned *locally* for your configured trigger patterns (e.g., `.g`, `.tr`, `.ta`).
- **No Keylogging:** The keystroke buffer is **never** saved to disk, logged to a file, or transmitted over the internet. When you close Tinky or turn off your computer, the buffer is permanently erased.

## 3. Interaction with Third-Party AI Providers
Tinky acts as a direct bridge between your computer and the AI provider of your choice (e.g., Google Gemini, OpenAI, Anthropic, OpenRouter, Groq).

- **API Keys:** Your API keys are encrypted locally on your machine using a machine-specific key and stored in your local `%APPDATA%` folder. They are never transmitted to us or any third party (other than the respective API provider when making a request).
- **Data Transmission:** When you activate a trigger, Tinky securely transmits *only* the specific text immediately preceding the trigger, along with your system prompt, directly to your configured AI provider via a secure HTTPS connection.
- **Third-Party Policies:** Because Tinky connects directly to these third-party providers using your API key, the processing of that specific text is governed by the Privacy Policy of the AI provider you selected. We encourage you to review their data retention and privacy policies (e.g., many providers do not use API data to train their models).

## 4. Local Data Storage
Tinky stores certain operational data locally on your device in the `%APPDATA%\OmniType` directory:
- **Configuration:** Your preferences, custom triggers, and encrypted API keys.
- **Local History:** A temporary database of recent AI interactions (e.g., original text length, result length, and duration). 
  - **Auto-Purging:** By default, Tinky automatically permanently deletes this history every 5 minutes. You can adjust this duration in the Settings menu.

## 5. Information We Collect (None)
Because Tinky does not connect to our servers, we do not collect:
- Personal identifiable information (PII)
- Account details (Tinky does not require an account)
- Telemetry, crash reports, or usage analytics
- Your prompts, text, or AI outputs

## 6. Children's Privacy
Tinky is not directed to individuals under the age of 13. Since we do not collect any personal information, we do not knowingly collect personal information from children under 13.

## 7. Changes to this Privacy Policy
We may update this Privacy Policy periodically to reflect changes in our practices or for other operational, legal, or regulatory reasons. If we make significant changes, we will update the "Last Updated" date at the top of this policy.

## 8. Contact Us
If you have any questions, concerns, or requests regarding this Privacy Policy, please contact us via the project's official repository or support channels.
