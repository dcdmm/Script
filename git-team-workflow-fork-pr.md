```mermaid
flowchart TD
    subgraph MAIN["主仓库 dcdmm/Script · 蓝色 master"]
        direction TD
        O["① 本次记录起点 · 6e95e33<br/>test.txt 为空"]
        A0["master 提交 a0 · 734215c<br/>文件内容：a0<br/>这是 master 与 xx 的共同祖先"]
        A1["master 提交 a1 · a894076<br/>文件内容：a0、a1"]
        A2["master 提交 a2 · eecee1f<br/>文件内容：a0、a1、a2"]
    end

    subgraph FORK["另一个账号 dcdmmgo · 紫色 Fork 工作分支 xx"]
        direction TD
        F["② Fork 到 dcdmmgo/Script<br/>xx 的开发历史从 734215c 分出<br/>继承已有的 a0"]
        B0["xx 提交 b0 · 3953e61<br/>文件内容：a0、b0"]
        B1["xx 提交 b1 · 926027a<br/>文件内容：a0、b0、b1"]
        PUSH["③ 将 xx 的提交推送到自己的 Fork<br/>dcdmmgo/Script:xx 到达 926027a"]
    end

    subgraph PR["跨仓库 PR #19 · 先整合主分支，再合并 PR"]
        direction TD
        OPEN["④ dcdmmgo 创建 PR #19<br/>来源：dcdmmgo/Script:xx<br/>目标：dcdmm/Script:master<br/>创建 PR 时，主仓库尚未接收 b0、b1"]
        X{{"xx 与主仓库 master 有冲突<br/>双方都在 a0 后追加内容<br/>xx 是 b0、b1；master 是 a1、a2"}}
        M["⑤ 把 master 合入 xx，解决冲突<br/>合并提交 a6ca320<br/>第一父提交：926027a；第二父提交：eecee1f<br/>文件内容：a0、b0、b1、a1、a2"]
        UPDATE["Fork 的远程 xx 更新到 a6ca320<br/>原 PR #19 随来源分支更新<br/>主仓库 master 此时仍在 eecee1f"]
        MERGE["⑥ dcdmm 合并 PR #19<br/>主仓库 master 更新到 7f10e1d<br/>第一父提交：eecee1f；第二父提交：a6ca320<br/>文件内容：a0、b0、b1、a1、a2"]
    end

    subgraph FINISH["主仓库本地副本同步，完成流程"]
        direction TD
        SYNC["⑦ 本地 master 拉取主仓库更新<br/>git pull --tags origin master，快进完成<br/>本地 master 与 origin/master 均到达 7f10e1d"]
    end

    O --> A0
    A0 --> A1
    A1 --> A2
    A0 -->|"Fork 协作，xx 从此处分出"| F
    F --> B0
    B0 --> B1
    B1 --> PUSH
    PUSH --> OPEN
    OPEN --> X
    A2 -->|"目标分支已有 a1、a2"| X
    X -->|"保留双方内容，完成合并提交"| M
    B1 -->|"xx 原有历史"| M
    A2 -->|"master 的历史合入 xx"| M
    M --> UPDATE
    UPDATE -->|"合并原 PR #19"| MERGE
    A2 -->|"master 接收 PR 的整合结果"| MERGE
    MERGE --> SYNC

    classDef mainNode fill:#eff6ff,stroke:#2563eb,color:#172554,stroke-width:2px;
    classDef forkNode fill:#f5f3ff,stroke:#7c3aed,color:#4c1d95,stroke-width:2px;
    classDef actionNode fill:#f8fafc,stroke:#64748b,color:#0f172a,stroke-width:1.5px;

    class O,A0,A1,A2,MERGE mainNode;
    class F,B0,B1,PUSH,X,M,UPDATE forkNode;
    class OPEN,SYNC actionNode;

    linkStyle 0,1,2,9,12,15 stroke:#2563eb,stroke-width:3px;
    linkStyle 3,4,5,6,10,11,13,14 stroke:#7c3aed,stroke-width:3px;
    linkStyle 7,8,16 stroke:#64748b,stroke-width:2px;
```

| 步骤 | 在哪里操作 | 做了什么 | 完成后的状态 |
| --- | --- | --- | --- |
| ① 主仓库开发 | `dcdmm/Script:master` | 从 `6e95e33` 的空文件开始，依次提交 a0、a1、a2 | 主分支到达 `eecee1f`，文件内容为 a0、a1、a2 |
| ② 另一个账号 Fork 并开发 | `dcdmmgo/Script` 的 `xx` 分支 | Fork 项目；xx 的历史从 `734215c` 分出，依次提交 b0、b1 | xx 到达 `926027a`，文件内容为 a0、b0、b1；分叉点是 a0 提交，而不是空文件起点 `6e95e33` |
| ③ 推送到 Fork | 贡献者本地 → `dcdmmgo/Script:xx` | 将工作分支推送到自己账号下的仓库 | Fork 的 xx 包含 b0、b1，主仓库 master 尚未接收这些改动 |
| ④ 创建跨仓库 PR | 主仓库的 GitHub PR 页面 | `dcdmmgo` 创建 [PR #19](https://github.com/dcdmm/Script/pull/19)，来源选自己的 `xx`，目标选主仓库的 `master` | PR 建立两个仓库分支之间的合并请求；两边在 a0 后的追加内容有冲突 |
| ⑤ 先在 xx 整合主分支 | 贡献者的 `xx` 分支 | 将 `eecee1f` 合入 `926027a`，解决冲突，生成 `a6ca320`，并使 Fork 远程 xx 接收结果 | xx 内容变成 a0、b0、b1、a1、a2；原 PR 随之更新；主仓库 master 仍是 `eecee1f` |
| ⑥ 再把 PR 合回主仓库 | GitHub，`dcdmm/Script:master` | `dcdmm` 合并 PR #19，生成 `7f10e1d` | 主仓库正式包含 b0、b1；PR 合并时的来源分支头为 `a6ca320`，不会因目标分支的合并操作自动变成 `7f10e1d` |
| ⑦ 同步主仓库本地副本 | 当前本地仓库的 `master` | reflog 记录为 `pull --tags origin master: Fast-forward` | 本地 master、origin/master 和核对时的主仓库远程 master 均为 `7f10e1d` |
