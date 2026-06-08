# Latex使用手册

**Overleaf**：在线协作平台（推荐新手）[https://www\.overleaf\.com](https://www.overleaf.com)

## **基础语法与文档结构**

1. **最小工作示例（MWE）**

```XML
\\documentclass{article}     % 文档类
\\usepackage{ctex}            % 中文支持
\\title{我的第一篇 \\LaTeX 文档}
\\author{张三}
\\date{\\today}
\\begin{document}
\\maketitle                  % 生成标题
\\section{引言}
这是一个简单的 \\LaTeX 示例文档。
\\end{document}
```

2. **常用文档类**

## **文本与段落格式**

3. **特殊字符转义**

```XML
\\% \\$ \\& \\# \\_ \\{ \\} \\~{} \\textbackslash{}  % 特殊符号
```

4. **字体样式**

```XML
\\textbf{加粗} \\textit{斜体} \\underline{下划线}
\\texttt{等宽字体} \\textsf{无衬线} \\textrm{衬线体}
```

5. **段落控制**

```XML
\\section{章节标题}          % 一级标题
\\subsection{子标题}         % 二级标题
\\paragraph{段落标题}       % 不编号
\\subparagraph{子段落标题}  % 不编号
\\indent 首行缩进           % 默认已启用
\\noindent 取消首行缩进
\\linebreak\\\\ 或 \\newline    % 换行
\\clearpage                  % 强制分页
```

## **数学公式**

6. **行内公式与显示公式**

```XML
% 行内公式
欧拉公式：$e^{i\\pi} + 1 = 0$
% 显示公式（自动编号）
$$\\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}$$
% 不编号公式
\\begin{equation*}
\\forall x \\in \\mathbb{R},\\ \\exists y \\in \\mathbb{R} \\text{ s.t. } y > x
\\end{equation*}
```

7. **常用数学符号**

## **图表与浮动体**

8. **插入图片（需 ****`graphicx`**** 宏包）**

```XML
\\usepackage{graphicx}
\\begin{figure}[htbp]
\\centering
\\includegraphics[width=0.5\\textwidth]{example-image}  % 图片路径
\\caption{示例图片}  % 标题
\\label{fig:example}  % 标签
\\end{figure}
```

9. **表格（****`tabular`**** 环境）**

```XML
\\begin{table}[htbp]
\\centering
\\begin{tabular}{|l|c|r|}
\\hline
左对齐 & 居中 & 右对齐 \\\\
\\hline
A & 1 & X \\\\
B & 2 & Y \\\\
\\hline
\\end{tabular}
\\caption{简单表格}
\\label{tab:example}
\\end{table}
```

## **列表与表格**

10. **无序列表**

```XML
\\begin{itemize}
\\item 第一项
\\item 第二项
\\end{itemize}
```

11. **有序列表**

```XML
\\begin{enumerate}
\\item 第一步
\\item 第二步
\\end{enumerate}
```

12. **自定义列表间距**

```XML
\\usepackage{enumitem}
\\begin{itemize}[noitemsep]
\\item 紧凑列表
\\end{itemize}
```

## **交叉引用与超链接**

13. **标签与引用**

```XML
\\section{引言}\\label{sec:intro}
参考章节 \\ref{sec:intro} 和图表 \\ref{fig:example}
```

14. **超链接（****`hyperref`**** 宏包）**

```XML
\\usepackage{hyperref}
\\href{<https://example.com>}{链接文本}
\\url{<https://example.com>}
```

## **参考文献管理**

15. **使用 BibTeX**

```XML
% 在 .bib 文件中定义文献
@article{einstein,
  author = "Albert Einstein",
  title = "Relativity: The Special and General Theory",
  year = "1920"
}
% 在主文档中引用
\\cite{einstein}
% 选择样式
\\bibliographystyle{plain}
\\bibliography{references}  % references.bib
```

16. **编译流程**

17. `pdflatex main.tex`

18. `bibtex main`

19. `pdflatex main.tex`

20. `pdflatex main.tex`

## **高级功能**

21. **自定义命令**

```XML
\\newcommand{\\R}{\\mathbb{R}}  % 快捷命令
\\R^n  % 使用示例
\\newenvironment{proof}{\\textbf{证明：}}{\\qed}  % 自定义环境
```

22. **代码高亮（****`listings`****）**

```Plain Text
\\usepackage{listings}
\\lstset{language=Python, basicstyle=\\ttfamily}
\\begin{lstlisting}
print("Hello, World!")
\\end{lstlisting}
```

23. **多图并排**

```Plain Text
\\usepackage{subcaption}
\\begin{figure}
\\begin{subfigure}{0.45\\textwidth}
\\includegraphics{img1}
\\caption{子图1}
\\end{subfigure}
\\hfill
\\begin{subfigure}{0.45\\textwidth}
\\includegraphics{img2}
\\caption{子图2}
\\end{subfigure}
\\end{figure}
```

## **实战案例**

24. **学术论文模板（IEEE）**

```XML
\\documentclass[10pt, conference]{IEEEtran}
\\usepackage{amsmath}
\\title{论文标题}
\\author{\\IEEEauthorblockN{作者姓名}\\IEEEauthorblockA{单位}}
\\begin{document}
\\maketitle
\\section{摘要}
这是摘要内容。
\\bibliographystyle{ieeetr}
\\bibliography{refs}
\\end{document}
```

25. **Beamer 幻灯片**

```XML
\\documentclass{beamer}
\\title{演示文稿标题}
\\author{张三}
\\begin{document}
\\frame{\\titlepage}
\\frame{\\frametitle{目录}\\tableofcontents}
\\section{章节1}
\\frame{\\frametitle{标题} 内容}
\\end{document}
```

## **注意事项**

- **编译错误处理**：

    - `Missing $ inserted`：数学模式缺失

    - `Undefined control sequence`：宏包未加载或拼写错误

    - `Overfull/Underfull \\hbox`：排版警告（可忽略但建议优化）

- **中文支持**：

```Plain Text
\\usepackage[UTF8]{ctex}  % 支持中文
\\usepackage{fontspec}    % XeLaTeX 字体支持
```

**版本控制**：

- 使用 Git 时忽略 `.aux`, `.log`, `.pdf` 等临时文件

- `.gitignore` 示例：

```Plain Text
*.aux
*.log
*.pdf
```

1. **性能优化**： 

    - 大文档使用 `\\includeonly` 选择性编译

    - 图片格式优先使用 PDF/SVG（矢量图）

2. **调试技巧**： 

    - 使用 `%` 注释逐段排除错误

    - 使用 `\\listfiles` 查看宏包版本

---

**进一步学习**:

- [Overleaf 文档](https://www.overleaf.com/learn)

- [LaTeX Wikibook](https://en.wikibooks.org/wiki/LaTeX)

- 推荐书籍：《LaTeX 入门》（刘海洋）、《The LaTeX Companion》

