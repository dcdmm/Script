```mermaid
%%{init: {"flowchart": {"wrappingWidth": 360}}}%%
flowchart TD
    subgraph HISTORY["蓝色 master 目标分支 / 橙色 ss 来源分支 / 紫色冲突处理"]
        direction TD

        O["① 共同起点 · e8b8408<br/>进度：0 / 甲：原始 / 乙：原始"]
        SS["② 从起点创建 ss，依次提交七步<br/>第一步 1e9bcb6 → 第二步 0720d39<br/>→ 第三步 4680e99 → 第四步 02a3cf7<br/>→ 第五步 9040820 → 第六步 0b23af0<br/>→ 第七步 95e0863<br/>ss 最终内容：进度 7 / 甲、乙均为分支"]
        M["③ 切回 master，设置冲突 · 5ae2882<br/>进度：0 / 甲：主线 / 乙：主线"]
        PICK["④ 在目标分支启动 cherry-pick<br/>git cherry-pick e8b8408..95e0863<br/>选取 ss 的第一步至第七步"]
        C1["第一步自动成功 · a4f229f<br/>进度：1 / 甲：主线 / 乙：主线"]
        X2{{"⑤ 应用第二步 0720d39 时冲突<br/>当前甲：主线 / 待应用甲：分支<br/>HEAD 仍停在第一步 a4f229f"}}
        C2["将甲改为分支，保留乙为主线<br/>git add test.txt<br/>git cherry-pick --continue<br/>生成第二步 · 8bf128e"]
        C34["⑥ 继续自动应用第三、四步<br/>第三步 1adf011：进度改为 3<br/>第四步 6289f00：进度改为 4<br/>甲：分支 / 乙：主线"]
        X5{{"⑦ 应用第五步 9040820 时冲突<br/>当前乙：主线 / 待应用乙：分支<br/>HEAD 仍停在第四步 6289f00"}}
        C5["将乙改为分支，保留甲为分支<br/>git add test.txt<br/>git cherry-pick --continue<br/>生成第五步 · 93f4861"]
        C67["⑧ 继续自动应用第六、七步<br/>第六步 72ce9ae：进度改为 6<br/>第七步 7460e99：进度改为 7"]

        O -->|"git switch -c ss"| SS
        O -->|"master 从共同起点继续"| M
        M --> PICK
        SS -.->|"选取七个提交的改动"| PICK
        PICK --> C1
        C1 --> X2
        X2 -->|"手动编辑并去掉冲突标记"| C2
        C2 -->|"继续剩余队列"| C34
        C34 --> X5
        X5 -->|"手动编辑并去掉冲突标记"| C5
        C5 -->|"继续剩余队列"| C67
    end

    subgraph FINISH["完成练习"]
        direction TD
        DONE["⑨ master 到达 7460e99<br/>test.txt：进度 7 / 甲、乙均为分支<br/>ss 仍指向原来的 95e0863<br/>两边最终内容相同，提交历史不同"]
    end

    C67 --> DONE

    classDef mainNode fill:#eff6ff,stroke:#2563eb,color:#172554,stroke-width:2px;
    classDef sourceNode fill:#fff7ed,stroke:#c2410c,color:#7c2d12,stroke-width:2px;
    classDef conflictNode fill:#f5f3ff,stroke:#7c3aed,color:#4c1d95,stroke-width:2px;
    classDef actionNode fill:#f8fafc,stroke:#64748b,color:#0f172a,stroke-width:1.5px;

    class O,M,C1,C34,C67 mainNode;
    class SS sourceNode;
    class X2,C2,X5,C5 conflictNode;
    class PICK,DONE actionNode;

    linkStyle 0,3 stroke:#c2410c,stroke-width:3px;
    linkStyle 1,2,4,7,10 stroke:#2563eb,stroke-width:3px;
    linkStyle 5,6,8,9 stroke:#7c3aed,stroke-width:3px;
    linkStyle 11 stroke:#64748b,stroke-width:2px;
```

| 提交说明 | ss 原提交 | master 新提交 | 这一步的改动 | 主线应用后的内容：进度 / 甲 / 乙 |
| --- | --- | --- | --- | --- |
| 第一步 | `1e9bcb6` | `a4f229f` | 进度 0 → 1，自动成功 | 1 / 主线 / 主线 |
| 第二步 | `0720d39` | `8bf128e` | 来源改动是甲「原始 → 分支」；主线已是「主线」，冲突后选择「分支」 | 1 / 分支 / 主线 |
| 第三步 | `4680e99` | `1adf011` | 进度 1 → 3，自动成功 | 3 / 分支 / 主线 |
| 第四步 | `02a3cf7` | `6289f00` | 进度 3 → 4，自动成功 | 4 / 分支 / 主线 |
| 第五步 | `9040820` | `93f4861` | 来源改动是乙「原始 → 分支」；主线已是「主线」，冲突后选择「分支」 | 4 / 分支 / 分支 |
| 第六步 | `0b23af0` | `72ce9ae` | 进度 4 → 6，自动成功 | 6 / 分支 / 分支 |
| 第七步 | `95e0863` | `7460e99` | 进度 6 → 7，自动成功 | 7 / 分支 / 分支 |
