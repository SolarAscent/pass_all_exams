# Prompt Patterns

Load this file when a session needs reusable wording.

## Evidence Header

```text
资料依据:
- ...

合理推断:
- ...

待确认:
- ...
```

Rules:

- Empty sections may be omitted except `待确认` when a claim matters for exam prediction.
- Never present inferred exam scope as teacher-confirmed.
- If materials conflict, quote the labels the student supplied, then ask which source is authoritative.
- When files were ingested through MarkItDown, cite the converted material filename and section heading when possible.

## Compact Teaching Pattern

```text
这一点的考法核心是: <one sentence>.

<concrete example first>

拆成三块:
1. <chunk>
2. <chunk>
3. <chunk>

最容易丢分的是: <trap>.

你先别看标准表述: 用一句话/一个公式条件/三步框架复述它。
```

## Scoreable Answer Pattern

```text
可拿分答案:
1. 点名: <term/theory/formula>
2. 机制: <why it applies>
3. 结合材料: <case-specific evidence>
4. 结论/建议: <exam-style close>
```

## Quantitative Course Pattern

```text
先判断题型: <pattern>.
能用这个方法的条件: <conditions>.
最短解题路:
1. <step>
2. <step>
3. <step>
检查点: <unit/sign/domain/common mistake>.
```

## Programming Course Pattern

```text
先看输入输出和状态变化。
核心机制: <concept>.
最小例子:
<code or trace>
常见坑: <bug pattern>.
现在你手动 trace 一遍: <small input>.
```

## Remediation Pattern

```text
根因判断: <confusion|missing-term|logic-reversal|transfer-failure|calculation|expression>
换一种讲法: <new representation>
重测: <new angle question>
记录: corrected/stubborn and next review date
```
