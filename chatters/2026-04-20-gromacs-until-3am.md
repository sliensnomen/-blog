---
title: 调试 GROMACS 到凌晨 3 点
date: '2026-04-20 03:12:00'
tags:
- GROMACS
- 日常
- 夜猫子
mood: 疲惫
cover: https://bu.dusays.com/2026/03/24/69c1e38b346cb.jpg
description: ''
---

报错：

```
Fatal error:
There is no domain decomposition for 8 ranks ...
```

盯着看了二十分钟，发现是自己把 `-ntmpi` 和 `-ntomp` 搞反了。

现在模拟倒是跑了，但我睡不着了。冲杯咖啡看日出吧。
