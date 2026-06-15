# MESA Validate

A Streamlit application for human-in-the-loop validation of LLM-extracted structured outputs against Pydantic schemas within the MESA (Medical-concept Extraction with Schema Alignment) framework.

## Repo Structure

```
presto-validate/
├── Home.py                   # Entry point
├── pages/
│   ├── 1_Sessions.py         # Session management
│   ├── 2_Validate.py         # Validation interface
│   └── 3_Analysis.py         # View results and metrics
├── utils/
│   ├── models.py             # Defining data models
│   ├── session_manager.py    # 'CRUD' functions
│   ├── schema_loader.py      # Schema config loading
│   ├── schema_inspector.py   # Schema introspection
│   ├── predictions_loader.py # File handling
│   ├── validation_ui.py      # UI generation
│   ├── metrics.py            # Calculating metrics
│   └── styles.py             # CSS styles
├── sessions/                 # Session data
├── predictions/              # JSON files in subfolders
├── schemas.yaml              # configuration schemas here
```

## Installation

1. Create authentication 
   ```shell
   cp auth.template.yaml auth.yaml
   # now edit auth.yaml username and password
   ```

2. **Configure schemas** in `schemas.yaml`:
   ```yaml
   schemas:
     - module: your_schema_module_name
       root_class: YourRootClassName
   ```

3. **Add prediction files** to subdirectory in `predictions/`

## Launch

```bash
docker compose up -d --build
```

Default URL: http://localhost:8501

## Prediction File Format

Each JSON prediction file must contain two required fields:

```json
{
  "content": "The original document text...",
  "output": {
    "field1": "value1",
    "field2": { ... },
    "list_field": [ ... ]
  }
}
```

- **`content`**: Original document text (string)
- **`output`**: LLM extraction result (object matching your Pydantic schema)
