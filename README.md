
# Subsea Research Station — AI Escape Room

An interactive underwater research-station escape room built with Python, Streamlit and an optional Gemini API integration.

Players must investigate the station, solve puzzles, collect items, restore the oxygen system and unlock the emergency escape hatch.

## Project Overview

This project contains two implementations:

- **Version 1:** LLM-led Game Master using conversation context to guide the player.
- **Version 2:** Python-controlled game engine with structured state, inventory management, puzzle prerequisites and action validation.

Version 2 separates game rules and state transitions from the LLM narration layer.

## Technologies

- Python
- Streamlit
- Google Gemini API (optional)
- python-dotenv
- unittest
- Playwright (optional, for browser screenshot automation)

## Repository Structure

```text
Subsea-Escape-Room/
├── version1/
│   └── app.py
├── version2/
│   ├── app.py
│   ├── game_engine.py
│   └── __init__.py
├── tests/
│   ├── test_game_engine.py
│   └── __init__.py
├── figures/
│   ├── architecture_v1.png
│   └── architecture_v2.png
├── data/
│   └── test_matrix.csv
├── docs/
│   ├── technical_summary.docx
│   └── technical_summary.md
├── README.md
├── requirements.txt
├── .env.example
└── .gitignore
```

## Installation — Windows

### 1. Clone the repository

```powershell
git clone https://github.com/YOUR_USERNAME/Subsea-Escape-Room.git
cd Subsea-Escape-Room
```

### 2. Create a virtual environment

```powershell
py -3.14 -m venv .venv
```

### 3. Activate the environment

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure environment variables

```powershell
Copy-Item .env.example .env
```

The Gemini API integration is optional. Version 2 can be played without an API key.

## Run Version 2

```powershell
streamlit run version2/app.py
```

Open:

http://localhost:8501

## Run Version 1

Open another PowerShell terminal, activate the virtual environment and run:

```powershell
streamlit run version1/app.py --server.port 8502
```

Open:

http://localhost:8502

## Optional Gemini API Configuration

Add your own API key to the local `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY_HERE
GEMINI_MODEL=gemini-2.0-flash
```

Never upload `.env` or expose API credentials in the repository.

## Game Scenario

The player is trapped inside an underwater research station.

Five interactive objects are available:

1. Sonar panel
2. Specimen cabinet
3. Control console
4. Oxygen valve
5. Emergency escape hatch

## Puzzle Sequence

| Stage | Player action | Result |
|---|---|---|
| 1 | Inspect sonar panel | Reveals code 2741 |
| 2 | Enter 2741 at specimen cabinet | Receives magnetic key and calibration card |
| 3 | Use calibration card at control console | Reveals code 6308 |
| 4 | Set oxygen valve to SAFE | Oxygen system secured |
| 5 | Use magnetic key on escape hatch | Hatch unlocked |
| 6 | Enter 6308 | Escape completed |

## Automated Testing

Run the test suite from the repository root:

```powershell
python -m unittest discover -s tests -v
```

The test suite covers:

- Sonar clue discovery
- Specimen cabinet prerequisites
- Correct and incorrect access codes
- Inventory collection
- Control console prerequisites
- Escape hatch requirements
- Prompt-injection rejection
- Restart and state reset

## Architecture Diagrams

The architecture diagrams are available in:

- `figures/architecture_v1.png`
- `figures/architecture_v2.png`

## Technical Documentation

The project report is available in:

- `docs/technical_summary.docx`
- `docs/technical_summary.md`

## Implementation Limitations

Version 2 uses a defined set of supported action phrases and aliases. It does not provide unrestricted natural-language understanding.

The Python game engine is authoritative for puzzle validation and game-state changes. Optional LLM narration does not override validated game rules.

## Security and Repository Hygiene

The following files and directories must not be committed:

- `.env`
- `.venv/`
- `__pycache__/`
- `*.pyc`

Refer to `.gitignore` for the exclusion rules.

## Author

**Sayan Kr. Dutta**

University of Europe for Applied Sciences

Project: AI Escape Room
