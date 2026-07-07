<img width="480" height="600" alt="image" src="https://github.com/user-attachments/assets/5390fee8-7c5e-48fa-b441-6aa5b5f2b8a5" />
<img width="325" height="650" alt="image" src="https://github.com/user-attachments/assets/c330da59-625c-45df-a4e8-b216c8807209" />


# FolderCheck (Folder Blueprint & Checklist Mapper)
[English](#english) | [中文](#中文)
---
## English
FolderCheck is a lightweight, translucent desktop widget for Windows designed to act as both a project checklist and a **Folder Blueprint Mapper**. It bridges the gap between task management and your actual physical file system. You can plan out a file structure first, then materialize it on disk, or drag an existing folder to automatically audit your project structure.
### Key Features
*   **📂 Infinite Tree-Based Blueprint**: Built using PySide6's recursive tree architecture. Folders and files are visually distinguished, showing progress bars and completion percentages on parent nodes.
*   **🎯 Smart Disk Sensing (Smart Path Resolution)**: Monitors your disk in real-time. If a planned file is created on your disk, the task automatically lights up blue. If you rename a task, FolderCheck offers to rename the actual file on disk.
*   **✨ Batch Generation & Materialization**: Right-click any blueprinted folder/file structure and select "Generate Placeholder" to instantly create the physical directories and empty files on your hard drive.
*   **🖱️ Advanced Drag & Drop**:
    *   *Internal*: Drag-and-drop tasks to nest them under parents or reorder them.
    *   *External*: Drag any physical folder from Windows Explorer directly into the window to reverse-engineer its layout into a blueprint up to 3 levels deep.
*   **⚡ Multi-Select & Batch Edit**: Select multiple nodes (`Ctrl` or `Shift`) to batch-toggle checkboxes, batch-color background tints (8 presets available), batch-generate files, or batch-delete (`Delete` key).
*   **📋 Export to Markdown**: A single click copies the entire blueprint hierarchy into a Markdown checklist, indicating the disk status of each item (`Exists` vs `Missing`).
*   **⚙️ Windows Context Menu Integration**: Run with the `--setup` flag to request admin privilege and automatically add FolderCheck to the Windows "New" context menu (`Right Click -> New -> FolderCheck Checklist`).
---
### Installation & Run
1. **Install Dependencies**:
   Ensure you have Python 3.10+ installed.
   ```bash
   pip install -r requirements.txt
   ```
   *(Requires: `PySide6`)*
2. **Run FolderCheck**:
   ```bash
   python foldercheck.py [your_file.check]
   ```
   If run without arguments, it loads a default `test.check` file in the workspace.
3. **Install to Windows Right-Click Menu**:
   ```bash
   python foldercheck.py --setup
   ```
   This will prompt for Administrator privileges to configure registry keys.
---
## 中文
FolderCheck 是一款为 Windows 设计的半透明极简桌面挂件，既是任务清单，又是**文件夹蓝图映射器**。它打破了“项目管理”与“物理文件系统”的壁垒。你可以先在软件内规划目录结构再一键生成物理文件，也可以直接拖入已有文件夹进行结构审计。
### 核心特性
*   **📂 无限层级树状蓝图**：基于 PySide6 构建的递归树状架构。清晰区分文件夹与文件，父节点实时计算子任务进度并支持半透明进度条填充。
*   **🎯 硬盘状态智能感知**：实时监控硬盘文件。当蓝图文件存在于硬盘上时，任务文字会亮起蓝色；在软件中重命名任务时，支持同步重命名硬盘真实文件。
*   **✨ 物理一键实体化**：在蓝图节点上右键选择 `✨ Generate Placeholder`，即可直接在硬盘上批量建立对应的真实文件夹及空白占位文件。
*   **🖱️ 内外部双向拖拽**：
    *   *内部拖拽*：自由上下排序，或直接将节点拖入另一个节点使其升级为子任务。
    *   *外部拖拽*：将 Windows 资源管理器中的任意文件夹拖入窗口，即可瞬间自动扫描并反向生成最多 3 层深的蓝图树。
*   **⚡ 批量多选与联动编辑**：支持 `Ctrl` 和 `Shift` 多选。可批量打勾、批量调整 8 种马卡龙背景色、批量生成文件以及批量删除（支持 `Delete` 键）。
*   **📋 导出 Markdown 报告**：点击顶部 `📄` 按钮，一键将蓝图树复制为 Markdown 代办列表，并自动标注每个文件的硬盘状态（`Exists` 或 `Missing`）。
*   **⚙️ Windows 右键菜单集成**：使用 `python foldercheck.py --setup` 运行，会自动申请管理员权限并将软件注册到 Windows 右键菜单中（`右键 -> 新建 -> FolderCheck Checklist`）。
---
### 快速开始
1. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```
   *(核心依赖：`PySide6`)*
2. **启动程序**：
   ```bash
   python foldercheck.py [your_file.check]
   ```
   如果不带任何参数启动，程序默认会加载或创建同目录下的 `test.check`。
3. **注册右键菜单新建项**：
   ```bash
   python foldercheck.py --setup
   ```
