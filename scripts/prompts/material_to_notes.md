你是一个资深开源维护者 + 技术写作者。请在当前 git 仓库中，把我提供的学习材料整理成一个“专业的纯 Markdown + Jupyter”学习笔记条目，并融入现有工程结构。

约束：
- 保持仓库风格：NOTES/ 放 Markdown 笔记，LABS/notebooks/ 放可复现 notebook，LABS/src/ 放可复用代码（如需要）。
- 不引入新框架/静态站点；不做过度重构；改动尽量小但专业。
- 所有内容必须可在 GitHub 直接阅读；Notebook 可运行且输出合理（建议 Run All 后清理冗余输出）。
- 只在必要时更新 requirements.txt（仅添加最少依赖）。
- 每一步都要确保文件路径和链接正确。

输入材料：
- 源文件：/mnt/data/1_numpy.md （可能包含 YAML frontmatter）

任务：
1) 创建目录 NOTES/topics/numpy/ （如不存在）。
2) 将 1_numpy.md 迁移为 NOTES/topics/numpy/01_numpy_basics.md，并做适配：
   - 移除 YAML frontmatter，替换为统一头部：
     标题、Last updated、Tags、TL;DR（3条）；
   - 修复明显的 Markdown/代码块格式问题（如注释粘连、缺少换行等），但不要改写核心内容。
3) 创建可复现 notebook：LABS/notebooks/R_010_numpy_basics.ipynb
   - 覆盖：array 创建、dtype/shape、索引切片、reshape/transpose、broadcasting、一个简单 plot
   - notebook 顶部包含 Purpose/Outputs 元信息（Markdown cell）
4) 更新 NOTES/00_index.md：在 Topics 中加入 NumPy 的链接条目。
5) 更新 NOTES/00_roadmap.md：新增一个可勾选任务，指向该 NumPy 笔记/或 notebook。
6) 更新 README.md：增加 “Demos” 列表，加入 R_010 notebook 链接（保留原有内容）。
7) 确认 .gitignore 对 __pycache__/.ipynb_checkpoints 生效；如 DATA 忽略策略存在，保持不破坏 README.md。
8) 给出本次变更的建议 commit message（不需要实际 git commit），并输出变更文件清单（paths）。

输出要求：
- 给出每个文件的最终内容（或对大文件给出清晰 patch/差异）。
- 最后输出：Checklist（我需要手动确认的点，比如“在 VSCode 选择 .venv kernel 并 Run All”）。

