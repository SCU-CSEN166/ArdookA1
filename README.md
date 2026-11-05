
# CSEN 166 — Term Team Project for Social Impact (TTP4SI)

**Team:** A1

**Challenge:** Ardook

**Members:** Emily Ramos, Flora Li, Avner Chen

**Link:** https://github.com/SCU-CSEN166/ArdookA1

**Last updated:** 11/4/2026

> **How to use this README:** Maintain this single file throughout the project. Complete the Week 5 project plan first, then update the appropriate weekly section before each milestone. Be specific and honest: describe what you attempted, what worked, what did not work, and what evidence supports your conclusions. For every week, document each member's actual contribution. If a task was not completed, explain the blocker and next step. Do not include private or sensitive data in this public README.

## Remember - Best Practices

### Data access and privacy
[Explain where authorized data can be accessed. Do not commit personal information, private WhatsApp exports, API keys, credentials, or restricted grant/application records. Use synthetic or anonymized examples in the README.]

### Known limitations
[Keep a current list of what the system cannot reliably do.]

## Week 5 — Scope: Project Plan

**Deliverable during Week 6 Lab:** A project plan (write in this README file) describing your problem formulation, proposed approach, each team member's responsibilities, proposed baseline models with Hugging Face links, proposed evaluation metrics, proposed data with links, and goals for each week.

### 1. Problem formulation and social impact
- **Problem:** Ardook is an Armenian-based organization. Nonprofits such as Ardook apply for various types of grants, and our problem is to determine which ones are well-fit for Ardook.
- **Intended users:** Intended users are the members of the Ardook organization who are going to apply for grants. 
- **Inputs and outputs:** The system will recieve a grant that Ardook can apply to and will output a recommendation score indicating how well-fit it is for the organization, as well as recommended actions.
- **Success criteria:** Our success criteria would be solid reasoning behind whether the provided grant is a good fit, able to be nuanced in judgement, and provides actionable steps for organizers. 
- **Constraints and risks:** Hallucination of recommendations (providing invalid/inaccurate info). There may not be enough data currently to parse through.

### 2. Proposed technical approach
- **Pipeline:** Our pipeline consists of inputting data and then immediately doing text preprocessing. After doing the text preprocessing, we will be doing some feature extraction where we use like TF-IDF and keyword matching. After doing the feature extraction, we will do a model comparison, which can help us decide on the ranking and evaluation of those models that we would be able to use to get a final output.
- **Baseline(s):** We can train a logistic regression model to be able to handle our grants and identify certain keywords that might be helpful for determining grant eligibility. We use TF-IDF to identify keywords in the descriptions of the grants in the database. Then we could calculate the similarity score using cosine similarity. Then, for the logistic regression model, we would classify the grants into different categories, such as women-focused, disability focused, children/family-focused, or general funding. We will then compare the predictions against the semantic similarity models. 
- **Proposed models/tools:** [Name, purpose, and link to each Hugging Face model or other resource.]
  - [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) - [It creates sentence embeddings for semantic search and similarity, which we will look at keywords like Women, Female, Small Business]
  - [bge-m3](https://huggingface.co/BAAI/bge-m3) - [Highly capable of cross-lingual alignment, so it is good for Armenian, Georgian, or other foreign languages that aren't English]
  - [Logistic Regression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression) - [It is the primary supervised baseline that we will use, where it can sort and classify grants into categories, which is especially useful in TF-IDF score calculation]
  - [BART-Large-MNLI](https://huggingface.co/facebook/bart-large-mnli) - [It is a zero-shot classifier that classifies grants into predefined categories without a huge labeled dataset. It is useful for limited data of examples of each grant category.]
  - [DistilBERT](https://huggingface.co/distilbert/distilbert-base-uncased) - [This is a smaller transformer model that can be fine tuned to our grant dataset, as it is useful in the comparison of classification performance and logistic regression.]
- **Alternative approach:** [If the baseline underperforms, we will use a hybrid search where we can combine keyword matching with semantic similarity, which can be helpful in keyword matching and concepts that may have different wording. If we then collected more labeled grant examples, we can then fine-tune the models such as DistilBERT to categorize grants more accurately. Then we will look at ranking the grants to see which ones have a stronger relationship. Then if we have time, we look at extraction of other data such as demographics, ownership, organization type and/or their funding purposes.]

### 3. Proposed data
| Dataset/source | Link or access instructions | Purpose | Size / languages | Privacy or usage considerations |
|---|---|---|---|---|
|---|---|---|---|---|
|---|---|---|---|---|
| Synthetic Data  | [URL](https://docs.google.com/spreadsheets/d/1vEmw_SD_ZDxQbQ-pE6rCKqWJaf-RASZWW6QTLTP5HtI/edit?gid=823558156#gid=823558156) | Training/Evaluation | Synthetic Data Created to Train/Test the Model| --- |
|Ardook All Grant Recommendations | [URL](https://drive.google.com/file/d/10EcaXrXUItPKAJwdqx6BTepwhGWMQIUn/view) | |---|

- **Data preparation:** Removing duplicate rows, making sure numerical features are on a scale that[Cleaning, anonymization, annotation, splitting, deduplication, etc.]
- **Data limitations:** Our provided dataset is currently small, so we need more data to train our model on.

### 4. Proposed evaluation
| Metric / test | What it measures | How it will be calculated | Target / success criterion |
|---|---|---|---|
| [Metric - e.g Accuracy, F1, AoC] | [Quality dimension] | [Method/ Formula] | [Target] | 
| Accuracy | accuracy | number of correct predictions/number of total predictions | aim for 1.0 | 
| Precision | precision | number of recommended grants are revelant | Aim to be above 0.7| 
| Recall | recall | number of relevant grants the model sucessfully identified| Aim to be above 0.7| 
 
- **Evaluation examples:** We will look at the direct wording of Women, Female, and Small Business in particular, and from there we will look at related examples of like Female/Women-Owned Enterprises or Entrepreneurship as well as Business Ownership. Further along, we will look at Disability inclusion, underserved communities, and family-oriented. 
- **Human verification:** At least two team members will check for baseline eligibility throughout all the grants, whether it is US-based or elsewhere.  
- **Failure cases to watch:** Two cases that we will watch for are early misclassification that are way larger than we expected, or any wrong classification that we need to either relabel the data or input more data to train. 

### 5. Team responsibilities
| Member | Primary responsibility (Data / models / evaluation / integration / etc.) | Specific Weekly contribution (work completed) | Planned next task |
|---|---|---|---|
|Emily |---|Repository setup and preliminary plan| Find suitable data to supplement the current data|
|Flora|Data and models|Creating Fake/Synthetic Data plan, and wrote the Evaluation examples, Human Verification, and failure cases to watch. I also found the models that we will use in training of our datasets. Introduced more metrics that we could use to evaluate our models. |Find real data that aren't aligned with Ardook just to test the model more to make sure it is accurate or precise|
| Avner |---|---|---|
---

## Week 6 — Build: Working Baseline

**Deliverable during Week 7 Lab:** A runnable baseline, setup/run instructions, and 1–2 example inputs and outputs. Update this section with what worked, what failed, and individual contributions.

### Implementation status
- **What runs end-to-end now?** [Describe exactly.]
- **How to run it:** [Commands, dependencies, configuration; refer to Setup below.]
- **Model(s) and data actually used:** [Names, versions, links, and any changes from the plan.]
- **Example 1:** Input: [non-sensitive example] → Output: [result]
- **Example 2:** Input: [non-sensitive example] → Output: [result]

### Attempts and outcomes
| Attempt / change | Worked? (Yes / Partly / No) | Evidence (output, metric, link) | What we learned / next step |
|---|---|---|---|
| [Attempt] | [Status] | [Evidence] | [Learning] |

### Individual contributions during that week
| Member | What I personally implemented/tested | Result (worked / partly / failed) | Evidence (commit, PR, experiment) | Blocker / next step |
|---|---|---|---|---|
| [Name] | [Specific contribution] | [Status] | [Link] | [Next step] |

---

## Week 7 — Evaluate: Results Checkpoint

**Deliverable during Week 8 Lab:** Preliminary evaluation results, metrics, development-set details, and 2–3 representative successes or failures. Include what you will improve next.

### Evaluation setup
- **Development data:** [Source, size, selection, annotations, link or access instructions]
- **Metrics and rationale:** [Why these metrics reflect the intended use]
- **Comparison:** [Baseline versus current approach, if different]

| System / version | Metric 1 | Metric 2 | Notes |
|---|---:|---:|---|
| Baseline | [Value] | [Value] | [Notes] |
| Current | [Value] | [Value] | [Notes] |

### Successes, failures, and interpretation
| Example / category | Expected behavior | Actual behavior | Success or failure? | Likely reason |
|---|---|---|---|---|
| [Case] | [Expected] | [Observed] | [Status] | [Hypothesis] |

- **What improved?** [Evidence]
- **What did not improve?** [Evidence]
- **Next experiment:** [Specific change and how you will measure it]

### Individual contributions during that week
| Member | Work completed | Result (worked / partly / failed) | Evidence | Next step |
|---|---|---|---|---|
| [Name] | [Specific work] | [Status] | [Link] | [Next step] |

---

## Week 8 — Stress-Test: Reliability on Hidden Data

**Deliverable during Week 9 Lab:** Hidden-test results (as provided by the TA), analysis of at least three important failure cases, and a prioritized improvement plan.

- **Submitted system version / commit:** [Commit hash]
- **Hidden-test metrics and leaderboard result:** [Results, when available]
- **Difference from development results:** [Compare; do not assume the hidden set is identical]

| Failure case / category | What went wrong | Possible cause | Severity / user impact | Proposed fix |
|---|---|---|---|---|
| [Case 1] | [Observation] | [Hypothesis] | [Impact] | [Fix] |
| [Case 2] | [Observation] | [Hypothesis] | [Impact] | [Fix] |
| [Case 3] | [Observation] | [Hypothesis] | [Impact] | [Fix] |

### Changes attempted after stress-testing
| Change | Worked? (Yes / Partly / No) | Evidence | Keep, revise, or revert? |
|---|---|---|---|
| [Change] | [Status] | [Result] | [Decision] |

### Individual contributions during that week
| Member | Work completed | Result (worked / partly / failed) | Evidence | Next step |
|---|---|---|---|---|
| [Name] | [Specific work] | [Status] | [Link] | [Next step] |

---

## Week 9 — Responsible AI, Peer Testing, and Final Delivery

**Deliverable during Week 10 Lab:** Document peer-testing feedback, Responsible AI concerns, changes made in response, and the final runnable system. Submit the final project report as instructed.

### Peer testing
- **Team evaluated:** [Team ID]
- **One thing that worked well:** [Evidence]
- **One meaningful failure:** [Reproduction steps or example]
- **One actionable recommendation:** [Specific fix]
- **Feedback received from another team:** [Summary]

### Responsible AI assessment
- **Potential harms or affected users:** [Who could be affected and how?]
- **Privacy and data handling:** [How sensitive information is protected]
- **Reliability and unsupported claims:** [How outputs are verified or uncertainty is communicated]
- **Fairness, accessibility, and usability:** [Relevant concerns and tests]
- **Human oversight:** [Where a human should review or correct outputs]
- **Remaining limitations:** [What should not be trusted or deployed yet]

### Final improvements and outcomes
| Feedback / issue | Change made | Worked? (Yes / Partly / No) | Evidence | Remaining limitation |
|---|---|---|---|---|
| [Issue] | [Change] | [Status] | [Link or metric] | [Limitation] |

### Individual contributions during that week
| Member | Final implementation / evaluation / documentation contribution | Result (worked / partly / failed) | Evidence | Reflection / remaining work |
|---|---|---|---|---|
| [Name] | [Specific work] | [Status] | [Link] | [Reflection] |



### Final submission checklist
- [ ] Code and final system/prototype are in the repository
- [ ] Setup and run instructions are complete and tested
- [ ] Data sources, model versions, and dependencies are documented
- [ ] Evaluation results are reported and compared with the baseline
- [ ] Important failures and limitations are explained
- [ ] Hidden-test and peer-feedback findings are addressed
- [ ] Responsible AI considerations and human oversight are discussed
- [ ] Every team member's contributions are documented for every week

**Final commit / release:** [Commit hash or tag]

---

## Setup and Reproducibility (keep updated)

### Requirements
[Python version, libraries, compute requirements, model access]

### Installation
```bash
# Add installation commands here
```

### Run the system
```bash
# Add an example command here
```

### Run evaluation
```bash
# Add an example evaluation command here
```

### Repository structure
```text
project/
├── README.md
├── requirements.txt
├── src/
├── tests/
├── evaluation/
└── examples/
```



