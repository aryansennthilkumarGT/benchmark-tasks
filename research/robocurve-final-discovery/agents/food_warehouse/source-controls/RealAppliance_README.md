<p align="center">
  <img src="assets/teaser.png" alt="RealAppliance teaser" width="100%"/>
</p>

# Appliance Manuals Dataset
A comprehensive multi-task dataset for appliance manual understanding, featuring 100 appliances across 13 appliance categories with multiple tasks

## 🔗 Links

[<img src="https://img.shields.io/badge/arXiv-2512.00287-red.svg" alt="arXiv"/>](https://arxiv.org/abs/2512.00287)
[<img src="https://img.shields.io/badge/Project%20Page-View%20Details-blue.svg" alt="Project Page"/>](https://realappliance.github.io/)

## 📊 Dataset Overview

This dataset contains appliance manuals in multiple languages (Chinese, English, French, Spanish, German, etc.) covering various home appliances including:

- **Air Fryers**
- **Blenders** 
- **Coffee Machines**
- **Microwaves**
- **Ovens**
- **Rice Cookers**
- **Toasters**
- **Washing Machines**
- **Mixers**
- **Kettles**
- **Bread Makers**
- **Deep Fryers**
- **Slow Cookers**

### Dataset Statistics
- **Total Manuals**: 100 real appliance manuals
- **Task 1**: key page identification tasks
- **Task 2**: open planning tasks
- **Task 3**: part alignment tasks
- **Languages**: Chinese (CH), English (EN), French (FR), Spanish (SP), German (DE), etc.

## 🎯 Tasks

### Task 1: Key Page Finding
**Objective**: Identify which pages in an appliance manual contain part introductions with component names, functions, and diagrams.

**Input**: Images from appliance manual pages
**Output**: Page indices that contain part introduction content
**Samples**: 100 annotated examples

### Task 2: Open Planning
**Objective**: Generate robotic manipulation sequences based on manual instructions using predefined atomic actions.

**Input**: Manual images + task description
**Output**: Sequence of atomic actions
**Samples**: ~980 planning examples

### Task 3: Part Alignment
**Objective**: Locate appliance parts in images by providing bounding box coordinates.

**Input**: Camera images of appliances + reference manual
**Output**: `[x1,y1,x2,y2]` bounding box coordinates

### Task 4: Closeloop Adjustment
**Objective**: Choose the next corrective or continuation atomic action given a partially-executed plan and the current appliance status. This task evaluates the model's ability to reason about execution history, detect deviations or incomplete steps, and output a single safe atomic action that advances the appliance toward the ground-truth plan.

**Input**: A JSON record that includes:
- `history`: steps already performed (may contain errors)
- `conduct`: steps conducted by the IsaacSim
- `gt_planning`: full ground-truth plan
- an image of the current appliance state

**Output**: One and only one atomic action (string). The model must select a single next-step from the allowed atomic actions, using the image and the provided history/conduct to decide.

## 📁 Data Structure

```
dataset/
├── image/                    # PDF manuals organized by appliance
│   ├── open_planning/        # Observation for openloop planning
│   ├── part_alignment/       # Images for part alignment from different angles
├── manuals_pdfs/                    # PDF manuals organized by appliance
│   ├── 001_airfryer_ch/
│   │   ├── 001_CH.pdf              # manual pdf with index and language as title
│   │   └── __pycache__/            # Processing cache
│   ├── 002_breadmachine_ch/
│   │   └── 002_CH.pdf
│   └── ... (100 appliance folders)
├── model/                    # PDF manuals organized by appliance
│   ├── 001/
│   │   ├── ...
│   │   ├── Aligned.usd             # USD appliance asset 
│   │   └── gt_part.json            # Part name and idx link
│   │   └── screen.json             # Configuration for screen display mechanism
│   │   └── utils,py                # Mechanisms' code for this appliance
│   └── ...
│   └── mech_utils_class.py   # Mechanisms' code used by all appliances
├── task_1_keypage.json             # Key page finding task
├── task_2_open_planning.json       # Open planning task
├── task_3_part_alignment.json      # Part alignment task
├── task_4_closeloop.json           # Closeloop Adjustment task
├── benchmark_task1.py              # Benchmark script for task 1
├── benchmark_task2.py              # Benchmark script for task 2
├── benchmark_task3.py              # Benchmark script for task 3
└── benchmark_task4_example.py      # Example code for running task 4
```

## 🚀 Usage

### Installation

```bash
git clone https://github.com/gaoyz1235/RealAppliance.git
pip install -r requirements.txt
```

Set your LLM API credentials before running benchmarks:

```bash
export OPENAI_API_KEY=your_api_key
export OPENAI_BASE_URL=https://your-api-endpoint/v1   # optional, for OpenAI-compatible APIs
```

### Benchmark Task 1–3

Task 1–3 benchmarks load annotated samples from JSON, convert manual PDFs to images, send them to a vision-language model, parse the model response, and report evaluation metrics.

Run on a specific appliance (e.g. manual `001`):
```bash
python benchmark_task1.py --llm gpt-4o-mini --manual_id 001
python benchmark_task2.py --llm gpt-4o-mini --manual_id 001
python benchmark_task3.py --llm gpt-4o-mini --manual_id 001
```
Omit `--manual_id` to evaluate all samples in the corresponding task JSON file.

Results are saved to:
- `result/{llm}_taskN/{manual_id}/detailed_results.json` — per-sample predictions
- `result/{llm}_taskN/{manual_id}/summary.json` — aggregated metrics
- `benchmark_taskN_{llm}.json` — summary at project root

### Benchmark Task 4: Closeloop Adjustment

Task 4 requires [Isaac Sim](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/download.html). Please install ISAAC SIM 4.5.0 from the official NVIDIA documentation before running the benchmark.

Task 4 is evaluated with `benchmark_task4_example.py`:

```bash
python benchmark_task4_example.py --manual_id 001 --llm_model gpt-4o-mini
```


## 📄 Citation

If you use this dataset in your research, please cite:

```bibtex
@misc{gao2025realappliancelethighfidelityappliance,
      title={RealAppliance: Let High-fidelity Appliance Assets Controllable and Workable as Aligned Real Manuals}, 
      author={Yuzheng Gao and Yuxing Long and Lei Kang and Yuchong Guo and Ziyan Yu and Shangqing Mao and Jiyao Zhang and Ruihai Wu and Dongjiang Li and Hui Shen and Hao Dong},
      year={2025},
      eprint={2512.00287},
      archivePrefix={arXiv},
      primaryClass={cs.RO},
      url={https://arxiv.org/abs/2512.00287}, 
}
```
