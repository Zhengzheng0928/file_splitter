# file_splitter
file_splitter
File Splitter / 文件分割合并器
English | 中文说明
English
📖 Introduction
File Splitter is a lightweight, efficient, and easy-to-use desktop utility designed to handle large files. Whether you need to transfer large files via email/USB or manage storage space, this tool helps you split files into smaller chunks and merge them back seamlessly without data loss.
✨ Features
Smart Splitting: Split files by specific size (KB, MB, GB) or by a specific number of parts.
Seamless Merging: One-click merging to restore the original file perfectly.
User-Friendly UI: Clean interface with drag-and-drop support.
Safety First: Checks disk space and verifies file integrity during the process.
Portable: No installation required (if using the .exe version), just run and go.
🚀 How to Use
1. Split File
Click "Select File" or drag a file into the window.
Choose your split mode:
By Size: Enter the size of each chunk (e.g., 10 MB).
By Count: Enter how many parts you want to split the file into.
Select the output directory.
Click "Start Split".
2. Merge File
Switch to the "Merge" tab.
Select the first part of the split files (e.g., filename.part1).
Ensure all parts are in the same folder.
Click "Start Merge" to restore the original file.
🛠️ Tech Stack
Language: Python 3.x
GUI Framework: Tkinter / CustomTkinter
Packaging: PyInstaller
📄 License
This project is licensed under the Apache License 2.0. See the LICENSE file for details.
中文说明
📖 项目简介
File Splitter（文件分割合并器） 是一款轻量、高效且易于使用的桌面工具，专为处理大文件设计。无论您是因为邮箱附件限制、U盘容量不足，还是为了更方便地存储和传输数据，本工具都能帮助您将大文件无损切割成小块，并能完美地将其还原。
✨ 主要功能
智能分割：支持按指定大小（KB/MB/GB）或按指定份数进行切割。
无缝合并：一键合并功能，确保还原后的文件与原件完全一致，无数据丢失。
极简界面：界面清爽直观，支持拖拽操作，上手即用。
安全校验：内置磁盘空间检测与文件完整性校验机制。
绿色便携：打包后的版本无需安装，双击即可运行。
🚀 使用说明
1. 分割文件
点击 "选择文件" 按钮或将文件直接拖入窗口。
选择分割模式：
按大小分割：输入每一块的大小（例如：10 MB）。
按份数分割：输入想要将文件切分成几块。
选择输出目录（保存位置）。
点击 "开始分割" 即可。
2. 合并文件
切换到 "合并" 选项卡。
选中分割后的 第一个文件（通常后缀为 .part1）。
确保所有分割后的文件都在同一个文件夹内。
点击 "开始合并"，等待进度条完成即可还原原文件。
🛠️ 技术栈
开发语言: Python 3.x
图形界面: Tkinter / CustomTkinter
打包工具: PyInstaller
📄 开源协议
本项目遵循 Apache License 2.0 开源协议。详情请参阅 LICENSE
更新日志 / Changelog
●       v1.0.0
●       首次发布：支持文件按大小/份数分割。 Initial release: Support file splitting by size or by count.
●       首次发布：支持多文件无缝合并。 Initial release: Support seamless merging of multiple split files.
●       界面优化：采用中英双语界面，支持拖拽操作。 UI improvement: Bilingual interface with drag-and-drop support.
●       ️ 性能提升：优化大文件读写速度，减少内存占用。 Performance improvement: Optimized read/write speed and reduced memory usage.

常见问题 / FAQ
Q: 合并后的文件打不开怎么办？ What if the merged file cannot be opened?
A: 请确保所有分割后的分片文件（如 .part1, .part2…）都在同一个文件夹内，且文件名未被修改。尝试重新点击“合并”按钮。 Please ensure all split files (e.g., .part1, .part2…) are in the same folder and filenames are unchanged. Try clicking “Merge” again.

Q: 分割后的文件可以删除原文件吗？ Can I delete the original file after splitting?
A: 可以。但在您确认合并成功且原文件内容无误之前，建议暂时保留原文件以防万一。 Yes. But it is recommended to keep the original file until you confirm the merge is successful.

Q: 支持多大的文件？ What is the maximum file size supported?
A: 理论上支持任意大小的文件（TB级别也可以），只要您的硬盘空间足够存放分割后的文件即可。 Theoretically supports files of any size (even TB-level), as long as your disk has enough space.

Q: 软件是免费的吗？ Is this software free?
A: 是的，本项目完全免费开源，您可以自由使用。 Yes, this project is completely free and open-source. Feel free to use it.
