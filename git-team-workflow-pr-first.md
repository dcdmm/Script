```mermaid
flowchart TD
    subgraph WORK["先创建两个 PR，再解决 bb 冲突"]
        direction TD

        O["① 共同起点 · 7a96d1d<br/>本地 master 与 origin/master 已同步<br/>从这里分别创建 aa、bb"]
        A0["本地 aa 提交 · b9ea1c9<br/>提交说明：a"]
        A1["本地 aa 提交 · abeab63<br/>提交说明：a1"]
        PA["② 推送 aa，创建 PR #12<br/>远程 aa → master<br/>aa、origin/aa、远程 aa 均在 abeab63"]
        B0["本地 bb 提交 · fddb8b3<br/>提交说明：b0"]
        B1["本地 bb 提交 · 0cb2d33<br/>提交说明：b1"]
        PB["③ 推送 bb，创建 PR #13<br/>远程 bb → master<br/>bb、origin/bb、远程 bb 均在 0cb2d33"]
        READY["两个 PR 都已创建，尚未合并<br/>此时远程 master 仍在 7a96d1d"]
        P12["④ 先合并 aa 的 PR #12<br/>远程 master 更新到 c25f6a4<br/>本地 master 和 origin/master 不会自动更新"]
        X{{"bb 原有的 PR #13 现在有冲突<br/>主分支已加入 aa 的改动<br/>需要解决冲突后才能合并"}}
        FETCH["⑤ 获取主分支更新<br/>git fetch origin master<br/>origin/master 更新到 c25f6a4"]
        M["⑥ 在本地 bb 合入 c25f6a4，解决冲突并提交<br/>生成合并提交 e5bfff3<br/>此时只更新本地 bb，远程 bb 尚未更新"]
        UPDATE["⑦ 推送 bb，原 PR #13 自动更新<br/>bb、origin/bb、远程 bb 均在 e5bfff3<br/>无需重新创建 PR"]
        P13["⑧ 合并原来的 PR #13<br/>远程 master 更新到 f87dde7<br/>本地 origin/master 仍需获取最新状态"]
    end

    subgraph FINISH["同步本地 master，完成流程"]
        direction TD
        SYNC["⑨ 切回 master，拉取远程更新并完成快进同步<br/>本地 master 与 origin/master 均指向 f87dde7<br/>流程完成"]
    end

    O -->|"创建 aa"| A0
    A0 --> A1
    A1 -->|"git push origin aa，然后创建 PR"| PA
    O -->|"创建 bb"| B0
    B0 --> B1
    B1 -->|"git push origin bb，然后创建 PR"| PB
    PA --> READY
    PB --> READY
    READY -->|"先合并 PR #12"| P12
    PB -->|"原 PR #13 继续等待合并"| X
    P12 -->|"目标主分支变化，与 bb 产生冲突"| X
    X -->|"回到本地处理"| FETCH
    FETCH -->|"将获取的主分支提交合入 bb"| M
    B1 -->|"bb 原有提交也参与这次合并"| M
    M -->|"git push origin bb"| UPDATE
    UPDATE -->|"冲突已解决，合并 PR #13"| P13
    P12 -->|"主分支从 c25f6a4 继续更新"| P13
    P13 -->|"同步远程结果到本地"| SYNC

    classDef mainNode fill:#eff6ff,stroke:#2563eb,color:#172554,stroke-width:2px;
    classDef aaNode fill:#fff7ed,stroke:#c2410c,color:#7c2d12,stroke-width:2px;
    classDef bbNode fill:#f5f3ff,stroke:#7c3aed,color:#4c1d95,stroke-width:2px;
    classDef actionNode fill:#f8fafc,stroke:#64748b,color:#0f172a,stroke-width:1.5px;

    class O,P12,FETCH,P13 mainNode;
    class A0,A1,PA aaNode;
    class B0,B1,PB,X,M,UPDATE bbNode;
    class READY,SYNC actionNode;

    linkStyle 0,1,2,6 stroke:#c2410c,stroke-width:3px;
    linkStyle 3,4,5,7,9,13,14,15 stroke:#7c3aed,stroke-width:3px;
    linkStyle 8,10,12,16 stroke:#2563eb,stroke-width:3px;
    linkStyle 11,17 stroke:#64748b,stroke-width:2px;
```

| 步骤 | 在哪里操作 | 做了什么 | 结果与分支状态 |
| --- | --- | --- | --- |
| ① 共同起点，分别开发 | 本地 aa、bb | 从 `7a96d1dee55a8c711000873247550d1421318fd7` 创建 aa、bb，各提交两次 | aa 到 `abeab63`，bb 到 `0cb2d33`；两边尚未互相合并 |
| ② 创建 aa 的 PR | 本地推送；GitHub 创建 PR | 推送 aa，创建 [PR #12](https://github.com/dcdmm/Script/pull/12)：远程 aa → master | aa、origin/aa 与远程 aa 均在 `abeab63`；创建 PR 不会修改主分支 |
| ③ 创建 bb 的 PR | 本地推送；GitHub 创建 PR | 推送 bb，创建 [PR #13](https://github.com/dcdmm/Script/pull/13)：远程 bb → master | bb、origin/bb 与远程 bb 均在 `0cb2d33`；此时 PR #12 也尚未合并，目标主分支仍在 `7a96d1d` |
| ④ 合并 aa | GitHub | 合并 PR #12，生成 `c25f6a4` | 远程 master 已包含 aa 的改动；原 PR #13 与更新后的主分支有冲突；本地引用不会自动更新 |
| ⑤ 获取最新主分支 | 本地 | 获取记录显示执行过 `git fetch origin master` | origin/master 更新到 `c25f6a4`；本地 master 仍在 `7a96d1d`，工作分支尚未因此合并 |
| ⑥ 解决冲突并提交 | 本地 bb | 将获取的主分支提交 `c25f6a4` 合入 bb，处理冲突并完成提交 | 生成 `e5bfff3`；两个父提交是 bb 原来的 `0cb2d33` 和主分支的 `c25f6a4`；此时远程 bb 和 origin/bb 尚未接收新提交 |
| ⑦ 更新已有 PR | 本地推送；GitHub 自动更新 PR | 推送 bb 的合并提交 | bb、origin/bb 与远程 bb 均在 `e5bfff3`；原 PR #13 自动包含新提交，无需再建 PR |
| ⑧ 合并 bb | GitHub | 合并原 PR #13，生成 `f87dde7` | 远程 master 接收 bb 的整合结果；远程 aa 仍在 `abeab63`，远程 bb 仍在 `e5bfff3` |
| ⑨ 同步本地主分支，完成流程 | 本地 master | 切回 master，拉取远程更新，完成快进同步 | 本地 master 与 origin/master 都指向 `f87dde7`，不产生新提交 |
