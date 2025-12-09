# TPEE: Event-Structured LLM Planning for Continuous-Parameter Industrial Workflows
✨This repository contains the implementation of TPEE framework and details of the dataset LEIA-Plan in **"TPEE: Event-Structured LLM Planning for Continuous-Parameter Industrial Workflows"** (*Submitted to ICAPS 2026*).
 <img src="fig/method.png" style="display:block;margin:0 auto;max-width:90%;height:auto;">

 ## 📝 LEIA-Plan
[LEIA-Plan](./LEIA-Plan/) is a laser-etching industrial dataset of atomic events and multi-step workflows, constructed from real operational scenarios involving five-axis CNC machines, dynamic-focusing galvanometers, and pulsed fiber lasers.

⏳*Details will be updated soon.*

## 💬 Prompt
[task-decomposition-prompt](prompts/task-decomposition-prompt) is used in Prompt Composition Module and Plan Sampling Module in TPEE for sampling candidate atomic-event sequences.

[task-decomposition-prompt-no-exp](prompts/task-decomposition-prompt-no-exp) is task-decomposition prompt based on task-decomposition-prompt without *Explanations Inclusion* for ablation study in this work.

[plan-select-prompt](prompts/plan-select-prompt) is prompt for selecting initial atomic-event sequence from candidate atomic-event sequences in Plan Sampling Module. And [plan-select-prompt-no-exp](prompts/plan-select-prompt-no-exp) is the one without *Explanations Inclusion*.

[plan-rewrite-prompt](prompts/plan-rewrite-prompt) is the sequence-revision prompt for *rewriting process* in Plan Rewrite Module. [plan-rewrite-prompt-no-exp](prompts/plan-rewrite-prompt-no-exp) is the one without *Explanations Inclusion*.


 ## 💻 Code
🚧 *Work in progress — updates will be added soon.*


