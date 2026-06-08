# 特性演示笔记

> 这是一篇**自动生成的演示笔记**，用来验证三件新功能：
> 1. **KaTeX** 数学公式（行内 $E=mc^2$ 与块级公式）
> 2. **highlight.js** 代码高亮（Python / C / bash / Verilog）
> 3. **标签 / 分类 / 搜索**（见侧栏 metadata）

## 1. 数学公式（KaTeX）

行内公式示例：能量守恒 $E = mc^2$，欧拉恒等式 $e^{i\pi} + 1 = 0$，二次方程求根公式 $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$。

块级公式示例（二次型）：

$$
f(x) = \frac{1}{\sigma\sqrt{2\pi}} \exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)
$$

矩阵：

$$
\mathbf{R} = \begin{pmatrix}
\cos\theta & -\sin\theta \\
\sin\theta &  \cos\theta
\end{pmatrix}
$$

## 2. 代码高亮（highlight.js）

Python（带行号）：

```python
def fibonacci(n: int) -> int:
    """递归求斐波那契数列第 n 项。"""
    if n < 2:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

if __name__ == "__main__":
    print([fibonacci(i) for i in range(10)])
```

C 语言：

```c
#include <stdio.h>

int main(void) {
    for (int i = 0; i < 5; i++) {
        printf("Hello, FPGA %d\n", i);
    }
    return 0;
}
```

Verilog（FPGA 触发器）：

```verilog
module dflipflop (
    input  wire clk,
    input  wire rst_n,
    input  wire d,
    output reg  q
);
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            q <= 1'b0;
        else
            q <= d;
    end
endmodule
```

Bash：

```bash
git add -A
git commit -m "feat: add demo-features note"
git push
```

## 3. 标签 / 分类（侧栏 metadata）

> 该笔记在 `assets/data/notes-index.json` 里登记的 tags：
>
> `tags: ["demo", "katex", "highlight", "test"]`
>
> `category: "study"`
>
> 在侧栏输入"katex"或"verilog"试试搜索过滤。

## 4. 结论

如果上面的数学公式渲染成了漂亮的排版（不是源码），代码块有彩色关键字（不是黑白），侧栏有搜索框 + 标签显示，则三件新功能**全部跑通**。
