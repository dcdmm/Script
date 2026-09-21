```mermaid
flowchart TD
    subgraph TEAM["同一个组织 · dmmandtom"]
        direction TD
        U1["dcdmm · 仓库 admin<br/>负责 xx 分支<br/>本次两个 PR 均由其合并"]
        U2["dcdmmgo · 仓库 write<br/>负责 yy 分支<br/>提交改动并解决 yy 的冲突"]
        REPO["共同的 GitHub 仓库<br/>dmmandtom/test<br/>共享 main、xx、yy 分支"]

        U1 -->|"组织成员"| REPO
        U2 -->|"组织成员"| REPO
    end

    subgraph HISTORY["蓝色 main / 橙色 dcdmm 的 xx / 紫色 dcdmmgo 的 yy"]
        direction TD

        O["① 共同起点 · 492289e<br/>初始提交 a0<br/>README.md：a0"]
        A1["main 新增第二行 · 7399dd9<br/>提交 a1<br/>README.md：a0、a1"]
        X1["dcdmm 在 xx 提交 · e2a2a04<br/>从共同起点新增第二行 A1<br/>README.md：a0、A1"]
        Y1["dcdmmgo 在 yy 提交 · cc6ffbf<br/>从共同起点新增第二行 b1<br/>README.md：a0、b1"]
        XPR["② dcdmm 提交 PR #1<br/>xx → main<br/>源分支提交 e2a2a04"]
        XC{{"③ 将 main 合并进 xx<br/>同一位置的 A1 与 a1 冲突<br/>处理结果：保留 A1"}}
        XM["xx 的合并提交 · ab40fab<br/>dcdmm 解决冲突，由 GitHub 生成合并提交<br/>README.md：a0、A1"]
        P1["④ dcdmm 合并 PR #1 · xx → main<br/>生成合并提交 53afa9d<br/>README.md：a0、A1"]
        YPR["⑤ dcdmmgo 提交 PR #2<br/>yy → main<br/>源分支提交 cc6ffbf"]
        FM["⑥ yy 获取更新后的主分支<br/>本地可用 git fetch origin<br/>将 origin/main 更新至 53afa9d"]
        YC{{"在 yy 合并 origin/main<br/>同一位置的 b1 与 A1 冲突<br/>处理结果：先 A1，后 b1"}}
        YM["⑦ dcdmmgo 完成 yy 合并 · 37518a0<br/>保留双方内容，形成三行<br/>README.md：a0、A1、b1"]
        P2["⑧ dcdmm 合并 PR #2 · yy → main<br/>生成合并提交 ba761ef<br/>README.md：a0、A1、b1"]

        O -->|"main 继续提交"| A1
        O -->|"xx 从 492289e 分叉"| X1
        O -->|"yy 从 492289e 分叉"| Y1
        X1 -->|"推送 xx，创建 PR"| XPR
        XPR -->|"PR #1 存在冲突"| XC
        A1 -->|"引入 main 的 a1"| XC
        XC -->|"完成冲突处理"| XM
        A1 -->|"main 原有历史"| P1
        XM -->|"PR #1 已更新，可合并"| P1
        P1 --> FM
        Y1 -->|"推送 yy，创建 PR"| YPR
        YPR -->|"PR #2 存在冲突"| YC
        FM -->|"引入 main 的 A1"| YC
        YC -->|"整理内容并提交"| YM
        P1 -->|"main 原有历史"| P2
        YM -->|"推送 yy，更新 PR #2"| P2
    end

    subgraph FINISH["当前工作区的完成状态"]
        direction TD
        S["本地 HEAD → main，与 origin/main 一致<br/>均指向 ba761ef<br/>README.md 共三行：a0、A1、b1"]
    end

    REPO -->|"共享仓库中的提交历史"| O
    P2 -->|"当前工作区已同步"| S

    classDef mainNode fill:#eff6ff,stroke:#2563eb,color:#172554,stroke-width:2px;
    classDef xxNode fill:#fff7ed,stroke:#c2410c,color:#7c2d12,stroke-width:2px;
    classDef yyNode fill:#f5f3ff,stroke:#7c3aed,color:#4c1d95,stroke-width:2px;
    classDef actionNode fill:#f8fafc,stroke:#64748b,color:#0f172a,stroke-width:1.5px;

    class O,A1,P1,FM,P2 mainNode;
    class U1,X1,XPR,XC,XM xxNode;
    class U2,Y1,YPR,YC,YM yyNode;
    class REPO,S actionNode;

    linkStyle 0,3,5,6,8,10 stroke:#c2410c,stroke-width:3px;
    linkStyle 1,4,12,13,15,17 stroke:#7c3aed,stroke-width:3px;
    linkStyle 2,7,9,11,14,16 stroke:#2563eb,stroke-width:3px;
    linkStyle 18,19 stroke:#64748b,stroke-width:2px;
```

| 步骤 | 成员与操作位置 | 做了什么 | 完成后的状态 |
| --- | --- | --- | --- |
| 协作背景 | 两人同属 `dmmandtom` 组织，共用仓库 `dmmandtom/test`；`dcdmm` 为 admin（管理员），负责 xx；`dcdmmgo` 为 write（写入权限），负责 yy | main 的规则已启用：限制更新、限制删除、阻止强推；绕过列表中的 Repository admin 设为 Always allow（始终允许绕过） | 各自在分支开发，由 dcdmm 合并 PR 到 main |
| ① 从同一起点分别开发 | `main`；`dcdmm / xx`；`dcdmmgo / yy` | 初始提交 `492289e` 只有 a0；main 的 `7399dd9` 添加 a1，xx 的 `e2a2a04` 添加 A1，yy 的 `cc6ffbf` 添加 b1 | 三个普通提交的父提交都是 `492289e`；xx 和 yy 都没有以 `7399dd9` 为起点 |
| ② xx 推送并提交 PR #1 | `dcdmm / xx`；GitHub | 推送 xx 的 `e2a2a04`，于 2026-09-21 11:07:04（UTC+8）创建 [PR #1](https://github.com/dmmandtom/test/pull/1)：xx → main | PR 已创建，尚未合并；xx 的 A1 与 main 的 a1 冲突，main 仍在 `7399dd9` |
| ③ main 合入 xx，处理第一次冲突 | `dcdmm / xx`；合并提交的提交者为 GitHub | 将 main 的 `7399dd9` 合入 xx 的 `e2a2a04`，同一位置的 A1 与 a1 冲突；结果选择 A1，形成 `ab40fab` | xx 为 a0、A1，PR #1 随源分支更新；main 尚未改变 |
| ④ 管理员合并 PR #1 | `dcdmm` 在 GitHub 合并 [PR #1](https://github.com/dmmandtom/test/pull/1) | 将 xx 的 `ab40fab` 合入 main，生成 `53afa9d` | main 为 a0、A1；`53afa9d` 与 `ab40fab` 的文件树相同；yy 原有提交仍只有 a0、b1 |
| ⑤ yy 推送并提交 PR #2 | `dcdmmgo / yy`；GitHub | 推送 yy 的 `cc6ffbf`，于 2026-09-21 11:11:04（UTC+8）创建 [PR #2](https://github.com/dmmandtom/test/pull/2)：yy → main | PR 已创建，尚未合并；yy 的 b1 与 main 的 A1 冲突，main 仍在 `53afa9d` |
| ⑥ yy 获取主分支并开始合并 | `dcdmmgo / 本地 yy` | `git switch yy` → `git fetch origin` → `git merge origin/main`，目标为 `53afa9d` | fetch 更新本地远程跟踪引用 origin/main；合并时 A1 与 b1 冲突，等待解决 |
| ⑦ yy 解决冲突并更新 PR #2 | `dcdmmgo / yy` | 将 README 整理为 a0、A1、b1，形成合并提交 `37518a0`；执行 `git push origin yy`，更新已有的 PR #2 | yy 为 a0、A1、b1，PR #2 随源分支更新；main 仍在 `53afa9d` |
| ⑧ 管理员合并 PR #2 | `dcdmm` 在 GitHub 合并 [PR #2](https://github.com/dmmandtom/test/pull/2) | 将 yy 的 `37518a0` 合入 main，生成 `ba761ef`；PR 描述为“第二行修改为 b1”，实际是在 A1 后新增第三行 b1 | main 为 a0、A1、b1；`ba761ef` 与 `37518a0` 的文件树相同 |
