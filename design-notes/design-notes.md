# System Design Notes

This document explains how I translated report observations into system rules before writing the automation code.

The main idea of this prototype is not only to generate PDF reports, but to convert raw student data into structured, meaningful, and personalized learning reports.

## Core Framework

I used four layers to design the report automation engine:

```text
Data Processing
↓
Business Logic
↓
Knowledge Library
↓
Presentation
```

## 1. Data Processing

The first step was identifying what information is meaningful in the context of a student learning report.

Rather than starting from the available dataset, I first defined what information should be communicated to the reader. This ensures that every piece of data included in the report serves a clear purpose.

For a learning report, the information can generally be grouped into several categories:

- Student identity
- Overall learning performance
- Learning habits
- Subject-level achievement

### Available Dataset

The Kaggle dataset already provides several useful variables, including:

- Student ID
- Overall Grade
- Attendance
- Weekly Study Hours
- Class Participation

These variables represent the core indicators of a student's academic performance and learning behavior.

### Data Enrichment

To make the prototype closer to a real-world report, several additional fields were introduced.

First, dummy student names were generated so each report could represent an individual student rather than anonymous records.

Second, subject-level scores were added as synthetic data. While these values are not part of the original dataset, they allow the report to demonstrate how subject-specific achievements can be interpreted and transformed into personalized insights such as Growth Opportunities and Subject Performance.

### Data Transformation

Instead of exposing every variable directly in the report, related data is transformed into higher-level business concepts.

For example,

```text
Attendance
Weekly Study Hours
Class Participation
↓
Learning Habits
```

Similarly,

```text
Mathematics
Science
English
Other Subject Scores
↓
Subject Performance
```

This transformation is important because readers think in terms of concepts—not individual database columns.

By processing the data into meaningful business entities first, the following layers (Business Logic, Knowledge Library, and Presentation) become significantly easier to design and maintain.

## 2. Business Logic

Once the data has been transformed into meaningful business entities, the next challenge is determining how those entities should be interpreted.

At this stage, the objective is no longer to process data, but to answer a more important question:

> **"What should this report communicate to the reader?"**

A learning report should not simply display numbers. Instead, it should help readers understand the student's strengths, areas for improvement, and possible next steps.

To achieve this, the report uses a collection of business rules that determine:

- how data is categorized,
- which sections should be generated,
- what information should be prioritized,
- and when certain insights should or should not appear.

The report structure itself remains fixed, but the content inside each section is generated dynamically based on these rules.

---

### Learning Habits

Rather than displaying Attendance, Weekly Study Hours, and Class Participation separately, these metrics are grouped into a single business entity called **Learning Habits**.

```text
Attendance
Weekly Study Hours
Class Participation
↓
Learning Habits
```

Each metric is evaluated independently and classified into one of three categories.

```text
High
Average
Low
```

The category is later used by multiple sections throughout the report, making it one of the core building blocks of the decision engine.

Instead of recalculating the same interpretation repeatedly, every downstream section simply references these classifications.

---

### Subject Performance

Subject scores follow the same design principle.

Instead of treating every subject independently, all subject scores are processed using a common classification rule.

```text
Subject Score
↓
High
Average
Low
```

Using a shared classification model keeps the report consistent and makes future maintenance significantly easier.

---

### Positive Indicators

The purpose of this section is to reinforce what the student is already doing well.

Rather than manually writing strengths for every report, the system automatically searches for metrics classified as **High**.

```text
Learning Habit = High
OR
Subject Performance = High
↓
Positive Indicators
```

Each matching metric contributes a corresponding positive explanation.

If no High category exists, the section is omitted entirely.

This prevents the report from generating generic compliments that are not supported by the data.

---

### Focus Areas

Focus Areas identify aspects of the student's learning that deserve additional attention.

The section collects every metric classified as:

```text
Average
Low
```

Unlike Positive Indicators, the goal here is not to criticize performance, but to identify opportunities for improvement.

If every metric is already classified as High, this section is skipped.

---

### Learning Plan

Learning Plan transforms findings into actionable recommendations.

Instead of treating every improvement equally, the report assigns different priorities.

```text
Low
↓
Needs Attention
```

```text
Average
↓
Suggested
```

The output is then sorted so that the most urgent recommendations appear first.

```text
Needs Attention
↓
Suggested
```

This ordering encourages readers to focus on the highest-priority actions before reviewing lower-priority suggestions.

---

### Growth Opportunities

Growth Opportunities are intentionally separated from Positive Indicators.

While Positive Indicators acknowledge current strengths, Growth Opportunities identify areas with exceptional potential.

The prototype currently uses the following rule:

```text
Subject Score ≥ 95
↓
Growth Opportunity
```

A score at this level may indicate that the student has developed a particularly strong aptitude or interest in a specific subject.

Rather than simply celebrating the achievement, the report encourages readers to consider how these strengths might be further developed.

If no subject reaches the defined threshold, the section is omitted.

---

### Learning Observations

Learning Observations is designed to identify meaningful contrasts between academic performance and learning habits.

Unlike other sections that evaluate individual metrics, this section looks for specific combinations across multiple indicators to uncover learning patterns that may not be immediately visible.

The current prototype focuses only on **High-Low** combinations involving:

- Overall Grade
- Attendance
- Weekly Study Hours
- Class Participation

For example,

```text
High Overall Grade
+
Low Class Participation
↓
Generate Learning Observation
```

or

```text
High Overall Grade
+
Low Weekly Study Hours
↓
Generate Learning Observation
```

These combinations may suggest that a student performs well academically despite showing relatively weak learning habits. Rather than treating this as a positive or negative outcome, the report presents it as an observation that may help parents or teachers better understand the student's learning characteristics.

Likewise, the opposite pattern is also considered.

```text
Low Overall Grade
+
High Attendance
↓
Generate Learning Observation
```

or

```text
Low Overall Grade
+
High Weekly Study Hours
↓
Generate Learning Observation
```

This may indicate that the student demonstrates strong learning discipline, but that these efforts have not yet translated into academic achievement. Such observations can encourage further discussion about learning strategies or additional support.

Only High-Low combinations are used in the current design.

Average-related combinations (such as High-Average or Average-Low) are intentionally excluded because they tend to produce less distinctive interpretations and often do not provide sufficiently meaningful insights for the reader.

If none of the predefined High-Low patterns are detected, the Learning Observations section is omitted.

This section demonstrates that the report is designed to interpret relationships between data rather than evaluate each metric in isolation.

---

### Conditional Rendering

Not every student requires every section.

Each report is generated dynamically based on the available findings.

The following sections are only created when at least one corresponding rule is satisfied:

- Positive Indicators
- Focus Areas
- Learning Plan
- Growth Opportunities
- Learning Observations

If no relevant condition exists, the section is omitted.

This keeps the report concise while ensuring that every generated section contributes meaningful information.

---

### Design Philosophy

The Business Logic layer is the core intelligence of the report.

Instead of asking,

> "How do I generate this report?"

the design process starts with a different question:

> **"What decisions should this report help the reader make?"**

Only after those decision rules were clearly defined was the automation logic implemented in code.
