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

## 3. Knowledge Library

After the Business Logic determines **what** should be communicated, the next challenge is deciding **how** it should be communicated.

Raw classifications such as `High`, `Average`, or `Low` are not meaningful enough to be presented directly to parents, teachers, or students.

Instead, every business outcome is translated into human-readable narratives through a Knowledge Library.

```text
Raw Data
↓
Business Logic
↓
Knowledge Library
↓
Personalized Narrative
```

Rather than hardcoding sentences throughout the codebase, all explanations are centralized into reusable knowledge components.

This separation makes the report easier to maintain, extend, and improve without modifying the underlying business logic.

---

### Knowledge Components

The prototype organizes the library into several categories, each serving a different purpose within the report.

- Executive Summary
- Positive Indicators
- Focus Areas
- Learning Plans
- Growth Opportunities
- Learning Observations

Each component contains domain-specific explanations that correspond to the business rules defined in the previous layer.

---

### Narrative Mapping

Instead of displaying classifications directly, each result is translated into a narrative.

For example,

```text
Attendance = High
```

does not appear in the report as

> Attendance: High

Instead, it becomes a more meaningful explanation describing the student's learning behavior.

Likewise,

```text
Class Participation = Low
```

is transformed into an observation explaining why classroom engagement may deserve additional attention.

This approach shifts the report from simply presenting data to communicating understanding.

---

### Why a Knowledge Library?

Separating knowledge from business logic provides several advantages.

Business Logic only determines **what** should be shown.

The Knowledge Library determines **how** that information should be explained.

Because of this separation:

- narratives can be improved without changing the decision rules,
- different writing styles can be introduced,
- multiple languages can be supported,
- and explanations remain consistent throughout the report.

---

### Building the Library

The initial knowledge library was written manually based on the intended interpretation of each business rule.

This process involved translating educational concepts into clear and concise narratives that would be meaningful to parents and teachers.

Although manually creating these explanations requires more effort initially, it produces a stable and reusable knowledge base that can be refined over time.

---

### LLM as a Knowledge Enhancement Layer

Large Language Models (LLMs) can significantly improve the quality of the knowledge library.

Rather than replacing the decision engine, an LLM can be used to enhance the narrative itself.

Possible applications include:

- improving wording and readability,
- generating alternative sentence variations,
- adapting the writing style for different audiences,
- translating reports into multiple languages,
- expanding concise explanations,
- helping draft the initial knowledge library.

In this architecture, the LLM acts as a **knowledge enhancement layer**, not as the primary decision maker.

---

### Future Direction: Dynamic Narrative Generation

A future version of the engine could combine Business Logic with dynamic LLM generation.

Instead of selecting a predefined explanation from the library, the system could generate personalized narratives using both the business outcomes and contextual information.

The architecture would become:

```text
Business Logic
↓
Knowledge Library
↓
LLM Enhancement
↓
Dynamic Narrative
```

or, for fully dynamic generation,

```text
Business Logic
↓
Context + Knowledge
↓
LLM
↓
Personalized Narrative
```

This would allow every report to become more natural, unique, and context-aware while still remaining grounded in the predefined business rules.

---

### Why Dynamic LLM Was Not Used

The current prototype intentionally relies on a rule-based knowledge library.

Although dynamic LLM generation offers greater flexibility, it also introduces practical considerations such as:

- API costs,
- response time,
- consistency,
- reproducibility,
- prompt engineering,
- output validation.

For a report automation engine, maintaining predictable and repeatable outputs is currently more important than maximizing linguistic variation.

The modular architecture keeps the Knowledge Library independent, allowing dynamic LLM generation to be integrated in future iterations without redesigning the Business Logic.

## 4. Presentation

After determining **what** should be communicated (Business Logic) and **how** it should be explained (Knowledge Library), the final challenge is deciding **how the information should be presented**.

The Presentation layer focuses on readability rather than aesthetics.

The goal is to ensure that readers can understand the report quickly, identify the most important findings, and naturally progress toward the recommended actions.

---

### Information Hierarchy

The report follows a deliberate reading sequence.

```text
Student Profile + Overall Grade
        ↓
Executive Summary
        ↓
Learning Habits
        ↓
Subject Performance
        ↓
Positive Indicators
        ↓
Focus Areas
        ↓
Learning Plan
        ↓
Growth Opportunities
        ↓
Learning Observations
```

This order mirrors how people typically process information.

The report begins with context, continues with supporting evidence, highlights strengths before weaknesses, and concludes with recommendations and observations.

---

### Progressive Disclosure

Not every piece of information should be presented at once.

Instead, the report gradually reveals information.

The reader first understands:

> Who is the student?

↓

How is the student's overall performance?

↓

What evidence supports that conclusion?

↓

Which areas deserve attention?

↓

What actions should be taken?

By progressively revealing information, the report becomes easier to follow and less cognitively demanding.

---

### Positive Before Improvement

The report intentionally presents strengths before improvement areas.

```text
Positive Indicators
        ↓
Focus Areas
        ↓
Learning Plan
```

Starting with achievements creates a more balanced reading experience and provides context before discussing opportunities for improvement.

The objective is not to avoid weaknesses, but to present them in a constructive sequence.

---

### Visual Prioritization

Business Logic is also reflected visually.

Each category is represented using consistent labels and colors.

```text
High
        ↓
Positive Label

Average
        ↓
Suggested Label

Low
        ↓
Needs Attention Label
```

These visual cues allow readers to identify important information without reading every paragraph in detail.

---

### Conditional Presentation

The report avoids displaying unnecessary information.

Sections such as:

- Positive Indicators
- Focus Areas
- Learning Plan
- Growth Opportunities
- Learning Observations

are generated only when relevant.

Instead of displaying empty placeholders or generic statements, the report simply omits sections that do not provide value.

This keeps every generated report concise and focused on meaningful insights.

---

### Dynamic Pagination

Because every student's report contains different amounts of content, page length cannot be predetermined.

The layout therefore applies pagination rules rather than relying on fixed page designs.

Before rendering a new section, the engine checks whether sufficient space remains on the current page.

```text
Enough Space
        ↓
Continue Rendering

Insufficient Space
        ↓
Move Section to Next Page
```

This prevents sections from being split awkwardly across pages and maintains a more natural reading experience.

---

### HTML-First Rendering

The report is rendered in HTML before being exported to PDF.

The HTML layout intentionally follows an A4 page structure so that the visual appearance remains consistent during PDF conversion.

Designing in HTML also provides greater flexibility for styling, debugging, and future enhancements compared to generating PDF layouts directly.

---

### Design Philosophy

The Presentation layer is not responsible for deciding **what** appears in the report.

Instead, it determines **how readers experience the information**.

A well-designed report is not defined by visual appearance alone, but by how effectively it communicates insights and supports decision-making.

# Architecture Evolution: The Role of LLM

The current prototype intentionally relies on a rule-based Knowledge Library to ensure that every generated report remains deterministic, consistent, and easy to validate.

However, the architecture was designed to be modular from the beginning, allowing Large Language Models (LLMs) to be introduced without changing the overall reporting pipeline.

Instead of acting as a single "report generator", an LLM can contribute at different layers depending on the desired objective.

---

## Stage 1 — Knowledge Generation

The first opportunity is during the creation of the Knowledge Library itself.

Rather than manually writing every explanation, recommendation, or observation pattern from scratch, an LLM can assist in generating the initial knowledge base.

For example,

```text
Business Rule

Attendance = High
```

↓

LLM generates multiple narrative candidates

↓

Human review and refinement

↓

Knowledge Library

This approach significantly accelerates library development while keeping the final knowledge base under human supervision.

The resulting library becomes a reusable organizational asset instead of repeatedly generating the same explanations.

---

## Stage 2 — Knowledge Enhancement

Once a Knowledge Library has been established, an LLM can further improve the quality of existing narratives.

Rather than changing the Business Logic, the LLM focuses on improving how the information is communicated.

Possible enhancements include:

- improving readability,
- generating alternative phrasings,
- adapting writing tone,
- simplifying explanations,
- translating into multiple languages,
- generating audience-specific versions (parents, teachers, school administrators),
- standardizing writing consistency across the entire report.

At this stage, the LLM functions as a language enhancement layer rather than a decision-making component.

---

## Stage 3 — Dynamic Narrative Generation

The most advanced implementation is using an LLM to generate personalized narratives dynamically.

Instead of retrieving predefined explanations from the Knowledge Library, the system provides structured context such as:

- student profile,
- overall performance,
- business rule outcomes,
- strengths,
- focus areas,
- learning plans,
- learning observations.

The LLM then synthesizes this information into a unique narrative while remaining grounded in the predefined Business Logic.

```text
Business Logic
        │
        ▼
Student Context
        │
        ▼
LLM
        │
        ▼
Personalized Narrative
```

Unlike a fully prompt-driven system, the Business Logic continues to determine **what** should be communicated, while the LLM determines **how** that information is expressed.

This separation helps preserve consistency, interpretability, and controllability.

---

## Why Rule-Based Logic Remains the Foundation

Although dynamic LLM generation offers greater flexibility, the current prototype intentionally prioritizes a rule-based approach.

A predefined Knowledge Library provides:

- deterministic outputs,
- consistent interpretations,
- easier validation,
- lower operational cost,
- faster report generation,
- predictable behavior across all reports.

These characteristics are particularly important for reporting systems where consistency is often more valuable than linguistic variation.

---

## Long-Term Vision

Rather than replacing existing components, the long-term direction is to progressively extend the architecture.

```text
Current Prototype

Data Processing
        │
Business Logic
        │
Knowledge Library
        │
Presentation
        │
Automation
```

↓

```text
Future Architecture

Data Processing
        │
Business Logic
        │
Knowledge Library
        │
LLM Layer
        │
Presentation
        │
Automation
```

The objective is not to build an "AI-generated report."

The objective is to build a reporting engine where Business Logic provides consistency, Knowledge Library provides domain knowledge, and LLM enhances the quality and personalization of the final narrative.

This layered architecture allows AI capabilities to evolve independently without requiring fundamental changes to the reporting pipeline.
