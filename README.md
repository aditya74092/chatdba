# ChatDBA - PostgreSQL Natural Language Query Chatbot

## High-Level Overview

ChatDBA is a conversational AI chatbot that allows users to interact with PostgreSQL databases using natural language. Instead of writing SQL queries, users can simply ask questions in plain English, and ChatDBA will understand their intent, generate the appropriate SQL, and return the results in a conversational format.

### Key Features

- **Conversational Interface**: Natural language interaction with your database
- **Complex Query Understanding**: Handles multi-table joins and complex conditions
- **Context Awareness**: Maintains conversation context for follow-up questions
- **PostgreSQL Integration**: Seamless connection to your PostgreSQL database
- **Natural Results Presentation**: Results are presented in a conversational format
- **LLM-Powered**: Uses advanced language models to understand and generate queries

### Use Cases

- Data analysts who want to query data without writing SQL
- Business users who need to extract information from databases
- Developers who want to quickly prototype database queries
- Anyone who needs to extract complex information from PostgreSQL without SQL knowledge

## Low-Level Implementation

### Architecture

ChatDBA consists of several key components:

1. **Chat Interface**: Handles user input and displays results
2. **Query Generator**: Converts natural language to SQL
3. **Database Executor**: Safely executes queries and returns results
4. **Context Manager**: Maintains conversation history
5. **Language Model**: Powers natural language understanding

### Technical Components

- **QueryGenerator**: Core class that orchestrates the query generation process
- **SafePostgresClient**: Handles database connections and query execution
- **ChatDBA**: Textual-based TUI application for user interaction
- **LangChain**: Powers the natural language to SQL conversion
- **OllamaLLM**: Local language model for query generation

## Code Structure

```
chatdba/
├── query_generator.py  # Core query generation logic
├── db_client.py       # Database connection and safety
├── tui_app.py         # Terminal user interface
├── test_query.py      # Query generation tests
├── test_safety.py     # Safety feature tests
└── requirements.txt   # Project dependencies
```

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL database
- Ollama with llama3:8b model

### Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your `.env` file with database credentials
4. Run the application: `python tui_app.py`

### Configuration

Create a `.env` file with:

```
PG_USER=your_username
PG_PASSWORD=your_password
```

## Usage

```python
from query_generator import QueryGenerator

# Initialize the generator
generator = QueryGenerator()

# Generate a query from natural language
result = await generator.generate_query("Show me all active users from New York")
print(result)
```

## License

MIT

## Technical Details

### Technology Stack

1. **Core Technologies**:
   - Python 3.13
   - PostgreSQL
   - Ollama (llama3:8b model)
   - LangChain
   - Textual (TUI framework)

2. **Key Packages**:
   - `langchain`: Natural language processing and SQL generation
   - `langchain_ollama`: Integration with Ollama LLM
   - `asyncpg`: Async PostgreSQL client
   - `textual`: Terminal user interface framework
   - `python-dotenv`: Environment variable management

### End-to-End Workflow

1. **Application Startup**:
   - `tui_app.py` is executed
   - `ChatDBA` class is instantiated
   - `QueryGenerator` is created and passed to `ChatDBA`
   - `on_mount()` is called to initialize the database connection

2. **User Input Processing**:
   - User enters a natural language query in the input field
   - `on_input_submitted()` or `on_button_pressed()` is triggered
   - The query is passed to `QueryGenerator.generate_query()`

3. **Query Generation**:
   - `QueryGenerator.generate_query()` is called with the user's question
   - `create_sql_query_chain()` from LangChain is used to generate SQL
   - The LLM (Ollama) processes the natural language and generates SQL
   - The generated SQL is returned to the `generate_query()` method

4. **Query Execution**:
   - The SQL query is passed to `SafePostgresClient.safe_execute()`
   - `_is_destructive()` checks if the query is safe to execute
   - `_explain_query()` estimates the number of rows to be scanned
   - If safe, the query is executed using `asyncpg`
   - Results are returned as a list of dictionaries

5. **Result Display**:
   - The results are formatted and displayed in the TUI
   - The `Static` widget is updated with the formatted results
   - User can see the results and enter a new query

### Detailed Function Call Sequence

Below is a detailed breakdown of the exact function call sequence when a user submits a query:

#### 1. Application Initialization
```
main.py
└── ChatDBA.__init__()
    └── QueryGenerator.__init__()
        ├── SafePostgresClient.__init__()
        └── OllamaLLM.__init__()
```

#### 2. Database Connection
```
ChatDBA.on_mount()
└── QueryGenerator.setup()
    └── SafePostgresClient.connect()
        └── asyncpg.connect()
```

#### 3. User Query Processing
```
ChatDBA.on_input_submitted() or ChatDBA.on_button_pressed()
└── QueryGenerator.generate_query()
    ├── create_sql_query_chain()
    │   └── LangChain processes the query
    │       └── OllamaLLM.generate()
    └── SafePostgresClient.safe_execute()
        ├── SafePostgresClient._is_destructive()
        ├── SafePostgresClient._explain_query()
        │   └── asyncpg.fetchrow("EXPLAIN...")
        └── asyncpg.fetch()
```

#### 4. Result Processing
```
SafePostgresClient.safe_execute()
└── Returns (query, results) to QueryGenerator.generate_query()
    └── Returns results to ChatDBA.on_input_submitted()
        └── Static.update()
```

### Function Details

#### QueryGenerator Class
- `__init__()`: Initializes the LLM and database client
- `setup()`: Establishes the database connection
- `generate_query(question)`: Main entry point for query generation
  - Creates a SQL query chain
  - Invokes the chain with the user's question
  - Executes the generated SQL safely
  - Returns the results

#### SafePostgresClient Class
- `__init__()`: Sets up the client with safety parameters
- `connect(dsn)`: Establishes the database connection
- `_is_destructive(query)`: Checks if a query is destructive
- `_explain_query(query)`: Estimates the number of rows to be scanned
- `safe_execute(query)`: Safely executes a query and returns results
- `close()`: Closes the database connection

#### ChatDBA Class (TUI)
- `__init__()`: Initializes the TUI application
- `on_mount()`: Called when the application starts
- `compose()`: Defines the UI layout
- `on_input_submitted()`: Handles Enter key in the input field
- `on_button_pressed()`: Handles button clicks

### Safety Features

1. **Query Validation**:
   - Destructive queries (INSERT, UPDATE, DELETE, etc.) are blocked
   - Large scans (>10,000 rows) require confirmation
   - SQL injection prevention through parameterized queries

2. **Error Handling**:
   - Database connection errors are caught and displayed
   - Query execution errors are handled gracefully
   - Natural language processing errors are caught and explained

### Database Interaction

1. **Connection Management**:
   - Async connection pool using `asyncpg`
   - Connection parameters from environment variables
   - Automatic connection cleanup

2. **Query Execution**:
   - Prepared statements for efficiency
   - Transaction management for data consistency
   - Result set streaming for large queries

### **1. Overview: What We're Building**  
We're creating **ChatDBA** – a **local-first AI agent** that:  
- Lets users **chat with PostgreSQL** using natural language  
- Runs entirely on a Mac (with optional cloud fallback)  
- Auto-generates complex SQL (joins, procedures, etc.)  
- Validates queries for safety before execution  
- Packages as a **single executable** for easy sharing  

---

### **2. Technology Stack**  

#### **Core Packages**  
| Package               | Purpose                                                                 | Version  |
|-----------------------|-------------------------------------------------------------------------|----------|
| `Ollama`              | Runs local LLMs (Llama 3)                                               | Latest   |
| `LangChain`           | Connects LLM to PostgreSQL + query generation logic                     | 0.2.1   |
| `asyncpg`             | Async PostgreSQL client (faster than psycopg2)                          | 3.2.0   |
| `Textual`             | Terminal UI framework                                                   | 0.54.2  |
| `PyInstaller`         | Bundles app into a single executable                                    | 6.7.0   |

#### **Supporting Packages**  
| Package               | Purpose                                                                 |
|-----------------------|-------------------------------------------------------------------------|
| `python-dotenv`       | Manages database credentials in `.env`                                  |
| `questionary`         | Interactive configuration wizard                                       |
| `langchain-community` | Ollama integration (deprecated but functional)                         |




---

















1. Overview: What We're Building

We're creating ChatDBA – a local-first AI agent that:

Lets users chat with PostgreSQL using natural language
Runs entirely on a Mac (with optional cloud fallback)
Auto-generates complex SQL (joins, procedures, etc.)
Validates queries for safety before execution
Packages as a single executable for easy sharing
2. Technology Stack

Core Packages

Package	Purpose	Version
Ollama	Runs local LLMs (Llama 3)	Latest
LangChain	Connects LLM to PostgreSQL + query generation logic	0.2.1
asyncpg	Async PostgreSQL client (faster than psycopg2)	3.2.0
Textual	Terminal UI framework	0.54.2
PyInstaller	Bundles app into a single executable	6.7.0
Supporting Packages

Package	Purpose
python-dotenv	Manages database credentials in .env
questionary	Interactive configuration wizard
langchain-community	Ollama integration (deprecated but functional)


```
The flow of what happens.



-Read file: app.py

-Read file: tui_app.py

-Read file: query_generator.py

-Read file: db_client.py



--------



Let me break down the complete flow when a user enters a query:

1. **User Interface (tui_app.py)**:
   - User types a question in the input field and clicks "Execute"
   - The `on_button_pressed` event handler in `ChatDBA` class is triggered
   - It gets the input value and calls `generator.generate_query(input.value)`

2. **Query Generation (query_generator.py)**:
   - The `generate_query` method in `QueryGenerator` class is called
   - It uses the local Ollama LLM (llama3:8b) to convert the natural language to SQL
   - The conversion happens through `create_sql_query_chain` from langchain
   - The LLM generates a SQL query based on the question

3. **Database Execution (db_client.py)**:
   - The generated SQL query is passed to `SafePostgresClient.safe_execute`
   - Before execution, several safety checks are performed:
     - `_is_destructive`: Checks if query contains dangerous operations (INSERT, UPDATE, DELETE, etc.)
     - `_explain_query`: Estimates how many rows the query will scan
     - If estimated rows > max_read_rows (10000), raises a warning
   - If all checks pass, the query is executed using `asyncpg`:
     ```python
     result = await self.conn.fetch(query)
     ```
   - Results are converted to a list of dictionaries and returned

4. **Result Display (tui_app.py)**:
   - The results are displayed in the UI's results section
   - If any errors occur, they are shown to the user

Specific PostgreSQL interactions happen in these places:
1. Initial connection in `QueryGenerator.__init__`:
   ```python
   self.db_uri = f"postgresql://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}@localhost/postgres"
   ```

2. Database execution in `SafePostgresClient.safe_execute`:
   ```python
   result = await self.conn.fetch(query)
   ```

The flow ensures:
- Safe query execution (no destructive operations without confirmation)
- Row limit protection (prevents large queries)
- Error handling at each step
- Clean result formatting

Would you like me to explain any specific part of this flow in more detail?
