# Cursor AI: Supercharging Your Code (Beyond Copilot) - 15-Minute Lecture Guide

This README provides a guide for a 15-minute lecture introducing Cursor AI to developers familiar with IntelliJ IDEA and GitHub Copilot. The lecture focuses on practical, hands-on aspects and integration with both external and local LLMs.

**Target Audience:** Developers using IntelliJ IDEA and GitHub Copilot.

**Time:** 15 minutes (This is tight, so we'll focus on the most impactful features)

**Goal:** Show developers how Cursor can enhance their existing workflow, particularly with its advanced features and local model capabilities.

## Lecture Outline & Script

**(0:00 - 0:30) Introduction - The "Why" of Cursor**

*   **Slide 1: Title Slide (Cursor AI: Supercharging Your Code)**
    *   "You're already using Copilot, which is great. But what if you could have a coding assistant that understands your *entire* codebase, debugs with context, and even runs locally? That's Cursor."
    *   "We're going to cover setup, key features, and how to integrate it with your existing workflow, including both cloud and *local* LLMs."
    *   "This is all about practical, hands-on tips."

**(0:30 - 2:00) Setup and Installation - Getting Started Quickly**

*   **Slide 2: Installation (Visual - Cursor download page)**
    *   "First, download Cursor from [cursor.sh](https://cursor.sh/). It's a separate editor, built on VS Code, so the interface will feel familiar."
    *   **(Live Demo - 1 minute):**
        *   Quickly show the download and installation process (have it pre-installed to save time).
        *   Open Cursor and show the familiar VS Code-like interface.
        *   Open a small, pre-existing project (e.g., a simple Node.js or Python project) – *ideally* one they might recognize (or a simplified version of a common project type).
        *   Point out that extensions are compatible.  "You can install your favorite VS Code extensions, including the ones you use for your specific language."
        *   Briefly mention that keyboard shortcuts are very close to VS Code / IntelliJ.

*   **Slide 3: Connecting to External LLMs (API Keys)**
    *   "By default, Cursor uses OpenAI models (GPT-4, GPT-3.5-turbo). You'll need an OpenAI API key for the best experience."
    *   "Go to Settings (Cmd/Ctrl + ,), search for 'Cursor: API Key', and paste your key."
    *   "There are also options for other providers like Anthropic (Claude) if you have access."
    *   Show a screenshot of the settings page where the API key is entered.  *Don't* show your actual key!

**(2:00 - 4:00) Basic Usage - Familiar Territory (But Better)**

*   **Slide 4: Code Completion (Side-by-side with Copilot)**
    *   "Cursor has excellent code completion, similar to Copilot. But it often provides more context-aware suggestions."
    *   **(Live Demo - 1 minute):**
        *   Start typing a function in your demo project.
        *   Show Cursor's completion suggestions, highlighting how they might be more relevant or complete than what you'd expect from Copilot alone.  *Prepare a specific example beforehand where the difference is clear.*
        *   Emphasize: "Notice how Cursor is using not just the current file, but potentially the *whole project* to understand what I'm trying to do."
        * Use `@` to reference files, folders and docs.

*   **Slide 5: Chat with Your Codebase (The Real Power)**
    *   "Here's where Cursor really shines: the chat interface (Cmd/Ctrl + K). This isn't just chat – it's chat *with context*."
    *   **(Live Demo - 1 minute):**
        *   Open the chat panel (Cmd/Ctrl + K).
        *   Ask a question about the *project*, not just the current file. For example:
            *   "What are the main functions in this project?"
            *   "How is data validated in the user input form?" (if applicable)
            *   "Where is the database connection configured?"
            *   "@file explain this file"
            *   "@docs explain how this library works"
        *   Show how Cursor answers, referencing specific files and lines of code.
        *   *Prepare a question beforehand that demonstrates this project-level understanding.*

**(4:00 - 7:00) Advanced Features - Beyond Basic Chat**

*   **Slide 6: Edit in Chat (Cmd/Ctrl + L) - Describe the Change**
    *   "You can *edit* your code directly within the chat. Describe the change you want, and Cursor will generate the code modification."
    *   **(Live Demo - 1.5 minutes):**
        *   Select a block of code (e.g., a function).
        *   Press Cmd/Ctrl + L.
        *   In the chat, give a clear instruction: "Refactor this function to use async/await." or "Add error handling to this function, logging any exceptions."
        *   Show Cursor's suggested changes. *Choose an example where the refactoring is non-trivial but also easily understandable.*
        *   Accept the changes (or parts of them).
        *   Emphasize: "This is HUGE for refactoring and adding features quickly. You describe the *intent*, and Cursor handles the details."

*   **Slide 7: Debugging with Context**
    *   "Cursor can help you debug. When you encounter an error, copy the error message and paste it into the chat."
    *   **(Live Demo - 1.5 minutes):**
        *   Introduce a *simple, deliberate error* into your code (e.g., a typo in a variable name, or a missing import). *Make sure this error is easily reproducible.*
        *   Run the code (show the error in the terminal).
        *   Copy the error message.
        *   Paste the error message into the Cursor chat (Cmd/Ctrl + K).
        *   Show how Cursor not only identifies the error but also suggests a fix, *with context* from your codebase.
        *   Apply the fix (or manually correct the code based on Cursor's suggestion).
        *   Emphasize: "Cursor doesn't just tell you *what's* wrong, it helps you understand *why* it's wrong and how to fix it within the context of *your* code."

**(7:00 - 9:00) Local LLMs with Ollama - Offline and Private**

*   **Slide 8: Why Local LLMs? (Privacy, Cost, Customization)**
    *   "Using cloud-based LLMs is convenient, but sometimes you need more control."
    *   "Local LLMs offer:  Privacy (your code never leaves your machine), Cost savings (no API fees), and Customization (you can choose the model)."
    *   "We'll use Ollama, a popular tool for running LLMs locally."

*   **Slide 9: Ollama Setup (Brief Overview)**
    *   "First, install Ollama from [ollama.ai](https://ollama.ai/). It's a simple installer."
    *   "Then, you need to 'pull' a model. For example: `ollama pull codellama:7b-code` (This pulls a 7 billion parameter Code Llama model)."
    *   **(No Live Demo for Ollama installation - too time-consuming. Assume they can follow the instructions.)**
    *   *Have Ollama pre-installed and a model (e.g., `codellama:7b-code`) pre-pulled.*
    *   Mention that larger models (e.g., 34B) require more powerful hardware.

*   **Slide 10: Connecting Cursor to Ollama**
    *   "In Cursor's settings, search for 'Cursor: Models: Chat' and 'Cursor: Models: Edit'."
    *   "You can specify a custom model. For Ollama, the format is `ollama/<model_name>` (e.g., `ollama/codellama:7b-code`)."
    *   **(Live Demo - 1 minute)**
        *   Show the settings in Cursor.
        *   Change the model to the Ollama model.
        *   Go back to the chat and ask a simple question to demonstrate that it's using the local model. ("What language is this project written in?")
        *   Emphasize: "Now, all my code interactions are happening *locally*, powered by the model I chose."

**(9:00 - 11:00) Getting the Best Out of Cursor - Tips and Tricks**

*   **Slide 11: Pro Tips**
    *   "Use clear, concise prompts. The better you describe what you want, the better the results."
    *   "Iterate! Don't be afraid to refine your prompts or ask follow-up questions."
    *   "Use `@` to reference files, folders, or even documentation within your project. This gives Cursor more context."
    *   "Explore the 'Generate Docs' feature (right-click on a function/class)."
    *   "Check out the Cursor changelog regularly ([cursor.sh/changelog](https://cursor.sh/changelog)) – they're constantly adding new features."
    *   "Use keyboard shortcuts!" (Show a quick reminder of Cmd/Ctrl + K and Cmd/Ctrl + L)

**(11:00 - 12:00) Cursor vs. Copilot - When to Use Which**

*   **Slide 12: Comparison Table**

    | Feature        | GitHub Copilot     | Cursor AI                 |
    |----------------|--------------------|---------------------------|
    | Code Completion | Excellent          | Excellent (often better)  |
    | Chat           | Basic              | Advanced (codebase context) |
    | Code Editing   | Limited            | Powerful (describe edits) |
    | Debugging      | Limited            | Context-aware suggestions  |
    | Local LLMs    | No                 | Yes (with Ollama)          |
    | Project Scope  | File-level         | Project-level             |
    | Price          | Paid               | Free tier, Pro Paid      |

    *   "Copilot is still great for quick completions, but Cursor excels at tasks requiring deeper understanding of your project."
    *   "Cursor's local LLM option is a game-changer for privacy and offline work."

**(12:00 - 14:00) Q&A and Wrap-up**

*   **Slide 13: Q&A**
    *   Open the floor for questions. Anticipate questions about:
        *   Specific language support.
        *   Performance differences between cloud and local LLMs.
        *   Integration with specific IntelliJ features.
        *   Privacy policies.
        *   Cost of the pro version.
        *   Can I use it to help me learn a new codebase?
*   **Slide 14:  Thank You and Resources**
        * "Cursor is evolving rapidly. The best way to learn is to try it!"
        * Links to
            * Cursor website: [cursor.sh](https://cursor.sh)
            * Ollama website: [ollama.ai](https://ollama.ai)
            * Cursor Changelog

**(14:00 - 15:00) Buffer for Overflow/Demos**

*   Have additional, pre-prepared demo examples ready to go if time allows, or to answer specific questions. These could include:
    *   Generating unit tests with Cursor.
    *   Creating documentation with Cursor.
    *   More complex refactoring examples.

## Key Considerations:

*   **Fast Pace:** 15 minutes is very short. Speak quickly and clearly, and prioritize the most impactful features.
*   **Visuals:** Use plenty of screenshots and keep the live demos concise.
*   **Hands-On:** Encourage the audience to download Cursor and try it out during the lecture (if possible).
*   **Relevance:** Connect everything back to their existing IntelliJ/Copilot experience. Show how Cursor *complements* and *enhances* their current tools.
*   **Enthusiasm:** Show your own excitement about Cursor's capabilities!
*   **Prepare, prepare, prepare!**: Practice the demos multiple times. Have fallback plans if something goes wrong (e.g., internet issues).

## Preparation Checklist:

*   [ ] Install Cursor.
*   [ ] Install Ollama and pull a model (e.g., `codellama:7b-code`).
*   [ ] Obtain an OpenAI API key (or other LLM provider key).
*   [ ] Prepare a small, representative demo project.
*   [ ] Prepare specific examples for code completion, chat, editing, and debugging.
*   [ ] Create slides (or use this README as a visual guide).
*   [ ] Practice the lecture and demos multiple times.
*  [ ] Have backup plans in the demos (in case something does not work as planned)

Good luck with your lecture!