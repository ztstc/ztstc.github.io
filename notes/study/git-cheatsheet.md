# Git 速查

> 高频命令的备忘单，详细参数请查 `git <command> --help`。

## 配置

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
```

## 初始化与克隆

```bash
git init
git clone https://github.com/user/repo.git
git clone --depth 1 url   # 浅克隆，省时间
```

## 提交与撤销

```bash
git status
git add <file>
git add -p                # 交互式选择 hunks
git commit -m "msg"
git commit --amend        # 改最近一次提交（未推送时）
git restore <file>        # 丢弃工作区修改
git restore --staged <file>  # 取消暂存
```

## 分支

```bash
git branch                # 列出本地分支
git branch -a             # 包含远程
git switch -c feat-x      # 新建并切换
git switch main           # 切回 main
git branch -d feat-x      # 删除已合并分支
git branch -D feat-x      # 强制删除
```

## 远程

```bash
git remote -v
git remote add origin <url>
git push -u origin main
git pull --rebase         # 拉取并 rebase（更线性）
```

## 改写历史（危险，慎用）

```bash
git rebase -i HEAD~3      # 交互式 rebase 最近 3 次
git rebase main           # 把当前分支 rebase 到 main
git cherry-pick <sha>     # 拣选单个提交
```

## 找回丢失的提交

```bash
git reflog                # 看到所有 HEAD 移动记录
git reset --hard <sha>    # 回到某个状态
```

> **黄金法则**：已推送到公共分支的提交不要 `rebase`。
