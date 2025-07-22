# Advanced XSS Payload Generator

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/github/license/TheOSuite/paygen)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen)

An intuitive GUI tool built with Python's Tkinter that helps security researchers and developers craft various Cross-Site Scripting (XSS) payloads efficiently. It offers customizable payload templates, multiple encoding options, and real-time previews to streamline testing and exploitation workflows.

---

## Features

- **Customizable Payloads:** Choose from predefined HTML tags or create your own templates with a `{payload}` placeholder.
- **JavaScript Injection:** Input custom JavaScript code to embed within payloads.
- **Encoding Options:** Apply different encoding schemes such as HTML entities, URL encoding, or Base64 to suit different contexts.
- **Preview:** Visualize the final payload in real-time before copying.
- **Copy to Clipboard:** Easily copy generated payloads for use in testing.

---

## Installation

1. Ensure you have Python 3.x installed on your system.
2. Save the provided script as `paygen.py`.
3. Run the script using Python:

```bash
python paygen.py
```

---

## Usage

1. Launch the application:

```bash
python paygen.py
```

2. Use the GUI to configure your payload:

   - Enter your JavaScript code in the "JavaScript Code" section.
   - Select or define a custom HTML template.
   - Choose an encoding type.
   - Click **Generate Payload** to produce the payload.
   - View the payload in the output box or use the **Preview** button to see how it looks.

---

## Customization

- **Adding More Templates:** Modify the `create_payload_config_frame()` method in `paygen.py` to include more predefined tags.
- **Encoding Types:** Extend the `apply_encoding()` method to support additional encoding schemes if needed.

---

## License

This project is provided **as-is**. Use responsibly and ensure you have permission to test payloads in target environments.

---

## Notes

- This tool is intended for educational and authorized security testing purposes.
- Always test in controlled environments to avoid unintended security issues.

---

## Contact

For questions or contributions, please open an issue or submit a pull request.

---
