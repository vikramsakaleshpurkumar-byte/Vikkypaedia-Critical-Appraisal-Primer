# Human + AI: a practical paper-reading guide

Checked 6 November 2026. Authored educational workflow informed by the sources below; not a validated method or a replacement for comprehensive review methods.

## 1. Catch the confident leap

Outcome: Identify a population, design or time-horizon claim that exceeds a supplied source.

Begin with your own one-sentence question and first impression. Then use AI for a second view. This course workflow keeps something independent to compare with the generated answer.

Read the output beside the source. Check who was studied, the design, comparator, outcome and follow-up. Mark each claim as supported, unsupported or not assessable from the material supplied. A helpful simplification must preserve the limits that change meaning.

Ask for a brief explanation of unfamiliar terms, then explain the idea back without the output. An analogy is a teaching aid; check where it stops fitting.

Reusable prompt:

> Use only the supplied paper or excerpt. First state what material you can actually access. Map population, design, comparator, outcomes, follow-up and limitations to exact page, section or table locations. Separate what the authors report from your interpretation. Preserve qualifiers. Write “not reported in the supplied material” rather than infer missing details. Finish with three claims I should verify in the original. Do not give a clinical recommendation.

Human checks:

- Match each summary claim to a source location.
- Circle any switch from associated with to caused or prevents.
- Restore missing population and follow-up limits.

Evidence context: [Peters & Chin-Yee — Generalization bias in LLM summarization of scientific research](https://doi.org/10.1098/rsos.241776)

## 2. Make the answer traceable

Outcome: Distinguish finding a reference from verifying that it supports the specific claim.

Give the tool a defined task and a clear source boundary. State whether it has the full paper, an abstract or a selected excerpt. Label conclusions about missing material as unresolved.

Use a claim ledger: claim → source location → your check → uncertainty. Open the reference, confirm its identity and inspect the cited passage. If access fails, record that the claim is unverified rather than asking the same system to reassure you.

For discovery, check whether a system retrieves documents or generates from its existing model alone. Treat the results as candidates to inspect. This distinction does not establish search completeness.

Reusable prompt:

> Build a claim ledger from the material I supply. Columns: exact claim; source title or identifier; exact page/section/table; supporting text or numbers; stated limitation; what I must check manually. Label direct findings, author interpretation and your inference separately. If you cannot access a source, mark it unverified. Do not invent references or fill unavailable cells from memory.

Human checks:

- Open the source rather than only the citation link.
- Check whether the outcome and study population match the claim.
- Keep unresolved access gaps visible.

Evidence context: [Asai et al. — Synthesizing scientific literature with retrieval-augmented language models](https://pmc.ncbi.nlm.nih.gov/articles/PMC12935541/)

## 3. Rebuild the numbers

Outcome: Recalculate absolute and relative effects from provided event counts and identify what cannot be inferred.

Ask AI to organise the numerator, denominator, event definition, comparison and follow-up before calculating. Then calculate independently with a calculator or reproducible code. Generated arithmetic is a draft to check.

For an undesirable binary event, compare experimental and control risks. Absolute risk reduction is control risk minus experimental risk; relative risk divides experimental risk by control risk. With a positive ARR, NNT is its reciprocal when risks are expressed as proportions. Retain the time period and relevant uncertainty.

For continuous outcomes or adjusted models, do not force a two-by-two calculation. Preserve the reported measure and interval, and ask what additional information would be needed.

To decipher a figure, start with the axes, units, scale, comparison and uncertainty markers. Check them against the caption and results text. Ask for an explanation tied to visible labels; when the tool cannot inspect an image or a number is unreadable, leave it unresolved rather than guessing.

Reusable prompt:

> Extract the event definition, follow-up, numerator and denominator for each group exactly as reported. Cite the table or page. State whether values are adjusted, unadjusted, imputed or incomplete. Show formulas and substitute the values step by step. Do not infer missing denominators or invent confidence intervals. For a figure, identify visible axes, units, scale and uncertainty markers; state when you cannot inspect the image. Explain the result in natural frequencies where appropriate and list calculations requiring manual verification.

Human checks:

- Check counts directly in the original table.
- Recalculate before reading the AI’s final number.
- Preserve outcome, units, follow-up and missing-data limitations.

Evidence context: Supplied textbook appendix 2, PDF page 335; original formulas and credits retained in source.pdf.

## 4. Question the methods

Outcome: Separate an explicitly reported method from an inference and a missing detail.

Read the question and design before requesting appraisal. Ask for a methods map, then one plausible threat to interpretation at a time. Require a source location for every judgement; leave missing methods as unknown.

Use a challenge pass: what else could explain this finding, which group is missing, and what would change your conclusion? Write your judgement before comparing it with the generated critique. More confident prose is not stronger methodological evidence.

When screening or extracting for a formal synthesis, define the criteria, test the tool on relevant material and document how you check its output. Follow the applicable review method; a convenient reading workflow is not a validated systematic-review process.

Reusable prompt:

> I have made an initial appraisal. Help me challenge it using only the supplied methods and protocol. For each concern, give: reported fact and location; possible bias mechanism; likely consequence if that mechanism operated; alternative explanation; information needed to judge it. Do not mark an unreported method as performed. Do not assign an overall evidence-certainty label from one paper alone.

Human checks:

- Separate absent reporting from demonstrated poor conduct.
- Check protocol and supplements where available.
- Retain a reasoned human judgement and a list of unknowns.

Evidence context: [Gartlehner et al. — Responsible Integration of AI in Rapid Reviews](https://pmc.ncbi.nlm.nih.gov/articles/PMC12644243/)

## 5. Choose the right assistant

Outcome: Match a reading or review task to a tool category and specify the human verification needed.

Use a document-grounded reader when your task is to interrogate a known paper; use a literature-retrieval system to discover candidate sources; use a synthesis workflow only when its methods and verification suit the review. A general chatbot can explain terminology, but its answer alone does not establish source coverage.

Before choosing a tool, test a known paper and a known missing detail. Can you inspect original passages? Does it distinguish unavailable content? Can you export records and reproduce the task? What material may be uploaded under your institution’s rules?

Record tool and version, date, task, inputs, prompt, retrieval scope and your checks. These are course workflow suggestions. They do not validate a product or replace a librarian or methodological reviewer when comprehensive searching is needed.

Reusable prompt:

> Help draft, not certify, a search plan for this review question. Identify concepts, synonyms and candidate controlled vocabulary; propose database-specific syntax for a human information specialist to check. List databases and dates actually searched separately from suggestions. Do not claim exhaustive coverage. Record limitations, inaccessible sources and how search strings and results can be exported for review.

Human checks:

- Match tool type to the actual task.
- Inspect retrieval scope and exportability.
- Never equate a persuasive shortlist with a comprehensive search.

Evidence context: [Asai et al. — Synthesizing scientific literature with retrieval-augmented language models](https://pmc.ncbi.nlm.nih.gov/articles/PMC12935541/); [Cochrane launches independent study of AI tools for evidence synthesis](https://www.cochrane.org/about-us/news/cochrane-launches-innovative-study-assess-ai-tools-evidence-synthesis)

## 6. Keep the human signature

Outcome: Produce an auditable appraisal note and decide whether material may be shared with an external AI service.

Finish with a short human-authored judgement: the question, what the study supports, what it does not support, important uncertainty and relevance to the decision. Keep the claim ledger and any corrections you made.

Check confidentiality, consent, licensing and institutional or journal policy before moving material into an external service. A published abstract, a licensed full text, a private patient record and a confidential peer-review manuscript have different constraints. A tool’s availability is not permission to upload.

For work you submit, follow the relevant disclosure requirements and retain human responsibility for accuracy, attribution and interpretation. This lab records no patient information, calls no AI service and sends no learner content anywhere. You choose whether to copy a prompt into an approved tool.

Reusable prompt:

> Help format my verified appraisal note without adding facts. Use these headings: decision question; study design and population; checked findings with source locations; limitations and unresolved questions; applicability; my judgement; AI assistance and human checks. Preserve uncertainty and flag any unsupported sentence. Use placeholders where I have not supplied information. Do not create citations or claim that you validated the paper.

Human checks:

- Keep the final judgement and source trail.
- Check permission before sharing any document externally.
- Disclose relevant AI assistance under the applicable policy.

Evidence context: [ICMJE — Use of AI by Authors](https://www.icmje.org/recommendations/browse/artificial-intelligence/ai-use-by-authors.html); [ICMJE — Editors’ Role in Ensuring Responsible Use of AI](https://www.icmje.org/recommendations/browse/artificial-intelligence/ai-use-by-editors.html); [WHO — Artificial intelligence-related health research: ethics review and oversight](https://www.who.int/publications/i/item/9789240124073)

## Source notes

[Peters & Chin-Yee — Generalization bias in LLM summarization of scientific research](https://doi.org/10.1098/rsos.241776) — 2025-04. The tested models sometimes broadened conclusions by dropping qualifiers. Results concern the models, prompts and material studied; they are not a current ranking of every AI system.

[Asai et al. — Synthesizing scientific literature with retrieval-augmented language models](https://pmc.ncbi.nlm.nih.gov/articles/PMC12935541/) — 2026-02-04. Retrieval-supported synthesis improved benchmark performance, yet retrieval could miss relevant papers and answers could contain unsupported information. Evaluation preferences also had limitations. This does not establish a replacement for a systematic review.

[Gartlehner et al. — Responsible Integration of AI in Rapid Reviews](https://pmc.ncbi.nlm.nih.gov/articles/PMC12644243/) — 2025-11-24. For Cochrane rapid reviews, AI should assist under human oversight, with justified use, verified outputs and transparent reporting of tools, model versions and prompts. This is methodological guidance, not an accuracy trial.

[ICMJE — Use of AI by Authors](https://www.icmje.org/recommendations/browse/artificial-intelligence/ai-use-by-authors.html) — Current page checked 2026-11-06. Humans retain responsibility for submitted content. Authors should disclose relevant AI use, check accuracy and attribution, and cite original sources rather than treating generated text as primary evidence.

[ICMJE — Editors’ Role in Ensuring Responsible Use of AI](https://www.icmje.org/recommendations/browse/artificial-intelligence/ai-use-by-editors.html) — Current page checked 2026-11-06. Submitted manuscripts are confidential. Editors and reviewers should not upload them to AI systems where confidentiality cannot be assured without explicit author permission; journal policies also apply.

[WHO — Artificial intelligence-related health research: ethics review and oversight](https://www.who.int/publications/i/item/9789240124073) — 2026-07-21. The report examines oversight of research using AI, research about AI, and AI-related health data science, including fairness and power imbalances. Only the public overview was used here; no claim of full-report appraisal.

[Cochrane launches independent study of AI tools for evidence synthesis](https://www.cochrane.org/about-us/news/cochrane-launches-innovative-study-assess-ai-tools-evidence-synthesis) — 2026-02-19. Cochrane described plans for independent, prospective evaluation because existing assessments have limitations. An announced evaluation is not a result or endorsement of a specific product.

Read the updated course guide and build/ai_update_sources.md for provenance and review limits. Original source permissions remain unchanged.
