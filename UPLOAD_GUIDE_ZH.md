# 三人分工及上传说明

## 对照最初分工

| 队员 | 部分 | 代码与测试 |
|---|---|---|
| Jiakai Chen | Part 1：文件读取与棋盘表示 | board.py、parser.py、blocks.py、tests/test_jiakai_chen.py |
| Tingting Li | Part 2：激光物理与模拟 | laser.py、simulation.py、tests/test_tingting_li.py |
| Junying Yu | Part 3：求解算法与输出 | solver.py、main.py、output.py、lazor.py、tests/test_junying_yu.py |

Jiakai Chen 兼顾 README、上传说明和仓库整理。Tingting Li 负责模拟测试，
并与 Jiakai Chen 确认 blocks.py 中的 interact 规则。Junying Yu 负责搜索
优化、整体集成、tests/support.py 和 tests/__init__.py。

## 压缩包结构

- lazor_team：完整可运行代码。
- upload_by_person/Jiakai_Chen：Jiakai Chen 的上传文件集合。
- upload_by_person/Tingting_Li：Tingting Li 的上传文件集合。
- upload_by_person/Junying_Yu：Junying Yu 的上传文件集合。

上传集合不是独立可运行程序。姓名文件夹仅用于分发，不应保留在最终仓库路径中。
程序的 board.py、parser.py 等仍用功能命名，保持导入清楚、运行正常。

## 上传步骤

1. 仓库所有者邀请另两位队员为 Collaborators，两位接受邀请。
2. 三人使用自己的账号，进入同一个仓库。建议按 Jiakai Chen、Tingting Li、
   Junying Yu 的顺序完成首次上传。
3. 在本地进入自己姓名文件夹，例如 upload_by_person/Tingting_Li。
4. GitHub Code 页面 -> Add file -> Upload files。
5. 拖入姓名文件夹里的内容，而不是姓名文件夹本身。
6. 检查路径应为 simulation.py、tests/test_tingting_li.py 等，不能带 Tingting_Li/ 前缀。
7. 填写准确的提交说明，再 Commit changes；若要求通过分支提交，创建自己的分支并发 PR。
8. 三人的 tests 子目录应合并到同一 tests 中，保留已有其他队员的文件。
9. Jiakai Chen 上传 README 时可更新仓库自动创建的 README，但保留需要的课程信息。
   macOS 用 Command+Shift+. 显示 .gitignore，只上传需要的文件。

建议提交说明：
- Jiakai Chen: Add BFF parser, board representation and block classes
- Tingting Li: Add laser geometry, tracing and reachability analysis
- Junying Yu: Add DFS solver, output and command-line integration

所有人都应实际理解、修改、测试自己负责部分，真实记录贡献。

## 本地验证

三部分合并后，在包含 lazor.py 的文件夹运行：

```bash
python3 -m pip install Pillow
python3 -m unittest discover -v
python3 lazor.py boards/mad_1.bff --outdir solutions
```

课程其他关卡放入 boards 后：

```bash
python3 lazor.py boards/*.bff --outdir solutions
```

测试按三位队员的模块职责组织。代码注释及 README 为英文，本上传说明为中文。

## 最终提交

确认 README 姓名与分工、全部课程关卡结果。创建最终 tag 和 Release，
在指定表单与 Canvas 提交仓库 URL，并完成 peer review。
作业截止：2026 年 11 月 10 日下午 3:00，截止后不要继续修改提交版本。

GitHub 官方参考：
https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository
https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository
