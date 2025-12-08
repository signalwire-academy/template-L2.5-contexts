# Lab 2.5: Contexts & Workflows

**Duration:** 60 minutes
**Level:** 2

## Objectives

Complete this lab to demonstrate your understanding of the concepts covered.

## Prerequisites

- Completed previous labs
- Python 3.10+ with signalwire-agents installed
- Virtual environment activated

## Instructions

### 1. Set Up Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Implement Your Solution

Edit `solution/agent.py` according to the lab requirements.

### 3. Test Locally

```bash
# List available functions
swaig-test solution/agent.py --list-tools

# Check SWML output
swaig-test solution/agent.py --dump-swml
```

### 4. Submit

```bash
git add solution/agent.py
git commit -m "Complete Lab 2.5: Contexts & Workflows"
git push
```

## Grading

| Check | Points |
|-------|--------|
| Agent Instantiation | 10 |
| SWML Generation | 10 |
| start_order function | 15 |
| add_pizza function | 15 |
| complete_order function | 15 |
| Contexts Configured | 15 |
| Test: Add pizza | 20 |
| **Total** | **100** |

**Passing Score:** 70%

## Reference

See `reference/starter.py` for a boilerplate template.

---

## Next Assignment

Ready to continue? [**Start Lab 2.6: State Management**](https://classroom.github.com/a/IbVS78JP)

---

*SignalWire AI Agents Certification*
