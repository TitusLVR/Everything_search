# 🧭 Everything Search — Blender Addon

A powerful **live search sidebar** addon for Blender that integrates with the *Everything* search engine on Windows. It allows users to instantly locate and open files directly within Blender using a searchable sidebar panel.

---

## ✨ Features

- 🔍 **Instant file search** from the 3D View sidebar using Everything Search (via DLL)
- 📂 Open files or reveal containing folders directly from the results
- 📄 Filter results by file type (e.g., `.blend`, `.png`, `.fbx`, etc.)
- 🧠 Smart paging support to browse through results
- 🛠️ Customizable settings for maximum results, visible entries, and DLL path
- ⌨️ Configurable hotkey (`F9`) to open the sidebar panel

---

## 🛠 Installation

1. **Install Everything** search engine from [https://www.voidtools.com](https://www.voidtools.com)
2. Copy `Everything64.dll` file to the `Everything` folder  
   _(e.g., `C:\Program Files\Everything`)_
3. In Blender:
    - Go to `Edit > Preferences > Add-ons`
    - Click `Install`, then select this addon's `.zip` or source folder
    - Enable **Everything Search**

---

## ⚙️ Preferences Panel

- **Everything DLL Path**: Set manually to point to `Everything64.dll`
- **Max Results**: Cap the number of search results
- **Results Shown in Panel**: Control how many results appear per page
- **Shortcut Key**: Shows active shortcut configuration (`F9` by default)

---

## 🧩 Usage

1. Press `F9` to open the **Everything Search** panel
2. Type your query (e.g., "character_walk")
3. Select file type from the dropdown (e.g., `.blend`, `.png`, or `All`)
4. Click result to:
    - 🔄 Load the file into Blender
    - 📁 Reveal the file’s folder (CTRL+Click)
    - 🆕 Open file in a **new Blender instance** (ALT+Click)

---

## 🔐 Requirements

- **Windows OS only** (requires Everything64.dll)
- **Everything Search must be installed** with IPC enabled

---

## 🧑‍💻 Author

**Titus**  
📧 titus.mailbox@gmail.com  
🌐 GitHub: [@titus.mailbox](https://github.com/titus.mailbox)

---

## 📝 License

This project is licensed under the terms of the following file:

[View LICENSE](license)
