# N8N Workflows

This project contains n8n workflows and utilities for automating various tasks using n8n.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your n8n instance credentials:
```
N8N_URL=http://localhost:5678
N8N_TOKEN=your_n8n_token
```

## Project Structure

- `workflows/`: Contains n8n workflow JSON files
- `scripts/`: Python scripts for workflow management
- `utils/`: Helper functions and classes

## Usage

To run Python scripts:
```bash
python scripts/your_script.py
```

## Contributing

1. Create a new workflow in n8n
2. Export the workflow JSON
3. Place it in the `workflows` directory
4. Add any necessary Python scripts in the `scripts` directory
