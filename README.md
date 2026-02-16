![Python](https://img.shields.io/badge/python-3.9+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Windows](https://img.shields.io/badge/platform-Windows-blue)
![GitHub release](https://img.shields.io/github/v/release/Guilherme-A-Garcia/PassGen)

# PassGen 🔒
PassGen is a neat Python GUI for my password generation logic made with CustomTkinter.<br>
It uses the following libraries: CustomTkitner, CTkMessagebox, secrets, string, os and sys.<br>
The [binaries](https://github.com/Guilherme-A-Garcia/PassGen/releases) are currently compiled with [Nuitka](https://nuitka.net/).

## Table of Contents
- [Preview](#preview)
- [Current Features](#current-features)
- [Requirements](#requirements)
- [Using the Source Code](#using-the-source-code)
- [How to Use](#how-to-use)
- [Roadmap](#roadmap)
- [Contributing](#contributing)

## Preview
![Main Interface](assets/images/previews/preview.png)

## Current Features
- Intuitive and modern interface
- ~~-Basic password generation-~~
- Proper password generation with the secrets module
- Password exportation
- Error handling with message boxes

## Requirements
If you wish to use the source code version you will need to install [Python](https://www.python.org/downloads/).🐍<br>

Otherwise, if you're planning on using the binary, you won't need to install any third-party application or interpreter.<br>
While this works for Windows, you will still need the [Wine compatibility layer](https://www.winehq.org/) for Linux. 🍷

## Using the Source Code

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Guilherme-A-Garcia/PassGen/
    cd PassGen
    ```

2.  **Create and activate a virtual environment** (recommended):

    *   **Linux/macOS:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    *   **Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Install the required packages** using the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

## How to Use
1. Download the latest release of this project (Or download the latest version of the repository);
2. Execute the .exe binary (or activate your virtual environment and run `python main.py` within the project directory);
3. Input the amount of characters your password will have;
4. Click "Enter" to generate the password.

If you wish to clear, copy or export the generated password into a .txt file, click the respective button.

## Roadmap
- ✅ Refactor from procedural to OOP;
- ✅ Migrate to CustomTkinter;
- ✅ Themes;
- ❌ Proper Linux support;
- ❌ The main dish: Add cryptography to the mix!
- ❌ Turn this whole thing into PySide6;

## Contributing
✨ Contributions are always welcome! ✨<br><br>

### How to Contribute:
*   **Report Bugs**: Open an issue with detailed steps to reproduce.
*   **Suggest Features**: Open an issue to discuss your idea.
*   **Contribute Directly to the Code**:<br>
    I. Fork the repository;<br>
    II. Create a new branch;<br>
    III. Make your changes and commit;<br>
    IV. Push to the branch;<br>
    V. Open a Pull Request;<br>
    VI. Kindly wait for approval. ;)<br>
<br>
Thank you for reading!
