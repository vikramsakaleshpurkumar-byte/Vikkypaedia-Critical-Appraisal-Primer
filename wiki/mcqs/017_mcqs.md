## q-017-1 · Best of five

An AI model performs well retrospectively at its development hospital. A clinic with different patients and a different care pathway wants to use it for triage. Which evidence most directly addresses the clinic's adoption question?

A. A higher average score across unrelated prediction tasks
B. A benchmark against a different algorithm using the original dataset
C. Evaluation of the system with the intended patients, users and workflow
D. A more detailed description of the model's architecture alone
E. A larger retrospective sample from the original hospital

<details><summary>Answer and reasoning</summary>

Best response: C. Evaluation of the system with the intended patients, users and workflow

Retrospective development performance does not establish clinical usefulness in the new setting.

**A.** Cross-task performance does not establish usefulness for this specific triage decision. (PDF 277)

**B.** This compares models within the same setting rather than evaluating transfer. (PDF 277)

**C.** Retrospective development performance does not establish clinical usefulness in the new setting. (PDF 277)

**D.** Architecture can aid understanding but does not demonstrate the intended clinical performance. (PDF 277)

**E.** This may refine development performance without testing the clinic's context. (PDF 277)

Source: PDF 277, printed 258. Model editorial check; independent specialist review outstanding.

</details>

## q-017-2 · Best of five

A model paper reports a high aggregate performance score but omits data sources, preprocessing and treatment of missing values. Which first request best supports an appraisal of how the result was produced?

A. A second headline metric without data-processing details
B. The same performance score calculated to more decimal places
C. A list of the authors' previous model publications
D. A different graphical presentation of the aggregate score
E. A reproducible account of input acquisition and processing

<details><summary>Answer and reasoning</summary>

Best response: E. A reproducible account of input acquisition and processing

The missing pipeline details affect interpretation and whether the evaluated task matches use in practice.

**A.** More result summaries do not resolve the methodological gap. (PDF 281)

**B.** Precision of reporting does not supply missing methods. (PDF 281)

**C.** Prior work does not replace reporting of this system's data pipeline. (PDF 281)

**D.** Replotting does not disclose how inputs were handled. (PDF 281)

**E.** The missing pipeline details affect interpretation and whether the evaluated task matches use in practice. (PDF 281)

Source: PDF 281, printed 262. Model editorial check; independent specialist review outstanding.

</details>

## q-017-3 · Best of five

A clinical AI system is modified after deployment. Early evaluation recorded no safety incidents. Which response most appropriately follows from the change and initial evidence?

A. Use the original benchmark score as the sole safety indicator
B. Apply the early safety conclusion unchanged to the modified system
C. Wait for a statistically significant harm signal before recording incidents
D. Treat every performance update as evidence of improved patient safety
E. Reassess risks and monitor observed harms as the system is used

<details><summary>Answer and reasoning</summary>

Best response: E. Reassess risks and monitor observed harms as the system is used

Safety assessment continues as new contexts and changes expose risks not seen initially.

**A.** A benchmark does not encompass all implementation-related harms. (PDF 282)

**B.** The modified system and its use may create different risks. (PDF 282)

**C.** Recording and investigating risk should not depend on first crossing a significance threshold. (PDF 282)

**D.** Prediction improvement and safety are distinct outcomes. (PDF 282)

**E.** Safety assessment continues as new contexts and changes expose risks not seen initially. (PDF 282)

Source: PDF 282, printed 263. Model editorial check; independent specialist review outstanding.

</details>

## q-017-4 · Assertion–reason

Assertion (A): A fluent clinical answer establishes that the underlying claims are accurate.

Reason (R): A conversational system can produce plausible statements that are unsupported or incorrect.

Judge the truth of each statement and whether R explains A.

A. Both A and R are true, and R correctly explains A.
B. Both A and R are true, but R does not correctly explain A.
C. A is true, but R is false.
D. A is false, but R is true.
E. Both A and R are false.

<details><summary>Answer and reasoning</summary>

Best response: D. A is false, but R is true.

A is false and R is true. Conversational fluency is compatible with factual error and is not a substitute for checking the claims.

**A.** This combination misclassifies at least one statement. A is false and R is true. Conversational fluency is compatible with factual error and is not a substitute for checking the claims. (PDF 274)

**B.** This combination misclassifies at least one statement. A is false and R is true. Conversational fluency is compatible with factual error and is not a substitute for checking the claims. (PDF 274)

**C.** This combination misclassifies at least one statement. A is false and R is true. Conversational fluency is compatible with factual error and is not a substitute for checking the claims. (PDF 274)

**D.** A is false and R is true. Conversational fluency is compatible with factual error and is not a substitute for checking the claims. (PDF 274)

**E.** This combination misclassifies at least one statement. A is false and R is true. Conversational fluency is compatible with factual error and is not a substitute for checking the claims. (PDF 274)

Source: PDF 274, printed 255. Model editorial check; independent specialist review outstanding.

</details>

## q-017-5 · Data interpretation

An AI paper reports excellent image-classification performance but does not specify the clinical decision, intended users or care pathway. The clinic must decide whether to adopt it. Which missing comparison is the priority for that adoption decision?

A. Average computation time on two generations of the same hardware
B. Parameter counts across the new and previous versions of the architecture
C. Classification accuracy against another model on the same image collection
D. Clinical consequences with the AI system versus current practice in its intended role
E. Performance scores on alternative partitions of the development dataset

<details><summary>Answer and reasoning</summary>

Best response: D. Clinical consequences with the AI system versus current practice in its intended role

Utility depends on the decision, users and pathway; classification performance alone does not establish better care.

**A.** Processing time can matter operationally but does not establish the clinical consequences of adoption. (PDF 279)

**B.** Architecture size does not directly establish the improvement or harms in the intended care decision. (PDF 279)

**C.** An algorithm comparison is useful technically but does not determine the clinical decision and consequences. (PDF 279)

**D.** Utility depends on the decision, users and pathway; classification performance alone does not establish better care. (PDF 279)

**E.** Internal comparisons cannot by themselves specify or establish clinical usefulness in the intended role. (PDF 279)

Source: PDF 279, printed 260. Model editorial check; independent specialist review outstanding.

</details>