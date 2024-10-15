# LLM Task Agents

LLM Task Agents is a Python package for creating and managing different agents that can handle tasks like image and text classification, SQL query generation, and JSON structure management. The agents are built on top of large language models (LLMs) and are designed to be modular and easy to integrate.

## Features

- **Text Classification Agent**: Classifies text into predefined categories using LLM-based prompts.
- **SQL Agent**: Runs SQL queries on databases and returns structured results.
- **JSON Agent**: Handles JSON validation and generation based on predefined schemas.
- **Image Classification Agent**: Classifies images into predefined categories using LLM models.

## Installation

### From PyPI

You can install the package via pip once it is uploaded to PyPI:

```bash
pip install llm-task-agents
```

### From Source

Alternatively, you can clone the repository and install the package manually:

```bash
git clone https://github.com/yourusername/llm_task_agents.git
cd llm_task_agents
pip install .
```

## Usage

Below are examples of how to use the different agents provided by the package.

### Text Classification Agent

```python
from llm_task_agents.agent_factory import AgentFactory
import os
from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax

# Initialize the console
console = Console()

# Text classification agent
text = "Je vois la vie en rose."

labels = ["Positive", "Negative"]

agent = AgentFactory.get_agent(
	 agent_type="text", 
	 llm_api_url=os.getenv("OLLAMA_API_BASE"), 
	 model="llama3.2:3b"
)

# Run the agent to classify text
result = agent.run(text=text, labels=labels)

# Display results
console.print("TEXT CLASSIFICATION AGENT")
console.print(f"[bold]Text:[/bold]\n{text}")
console.print(f"[bold]Labels:[/bold]\n{labels}")
console.print(f"[bold]Result:[/bold]\n{result}")
```

### SQL Agent

```python
from llm_task_agents.agent_factory import AgentFactory
import os
from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax

# Initialize the console
console = Console()

# SQL Agent
user_request = "Show total sales per month"

agent = AgentFactory.get_agent(
    agent_type="sql",
    llm_api_url=os.getenv("OLLAMA_API_BASE"),
    model="llama3.2:3b",
    database_driver="mysql",
    database_username=os.getenv("MYSQL_USER", "root"),
    database_password=os.getenv("MYSQL_PASSWORD", "password"),
    database_host=os.getenv("MYSQL_HOST", "localhost"),
    database_port="3306",
    database_name="chinook",
    # debug=True,
)

# Get the list of tables
tables = agent.list_tables()

# Generate the SQL query
sql_query = agent.run(
    user_request=user_request,
    tables=tables,
    allowed_statements=["SELECT"]
)

# Function to display tables using rich Table
def display_tables(tables):
    table = Table(title="Database Tables")
    table.add_column("Table Name", justify="left", style="cyan", no_wrap=True)

    for table_name in tables:
        table.add_row(table_name)

    console.print(table)

# Display results
console.print("SQL AGENT")
display_tables(tables)
console.print(f"[bold]User Request:[/bold] {user_request}")

if sql_query:
    console.print("[bold green]Valid SQL Query:[/bold green]")
    syntax = Syntax(sql_query, "sql", theme="monokai", line_numbers=True)
    console.print(syntax)
else:
    console.print("[red]Failed to generate a valid SQL query.[/red]")
```

### JSON Agent

```python
from llm_task_agents.agent_factory import AgentFactory

# Create a JSON agent
json_agent = AgentFactory.get_agent(
	agent_type="json",
	llm_api_url="http://your-llm-api.com",
	model="your-model"
)

# Define a JSON schema
schema = {
	"person": {
		"first_name": "string",
		"last_name": "string",
		"age": "int"
	}
}

# Generate JSON based on the schema
result = json_agent.run(task="Generate persona", structure=schema)
print(result)
```

## Development

If you'd like to contribute to this project, follow these steps to set up your local environment:

### Clone the Repository

```bash
git clone https://github.com/yourusername/llm_task_agents.git
cd llm_task_agents
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built using the `ollama` LLM API.
- SQL query management with SQLAlchemy.
