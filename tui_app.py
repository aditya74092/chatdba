import asyncio
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Input, Button, Static
from query_generator import QueryGenerator
import json

class ChatDBA(App):
    CSS = """
    Container {
        layout: vertical;
        padding: 1;
    }
    Input {
        width: 100%;
    }
    #results {
        height: 70%;
        border: solid #666;
        padding: 1;
        overflow-y: auto;
    }
    """

    def __init__(self, generator: QueryGenerator):
        super().__init__()
        self.generator = generator
        self._is_setup = False

    async def on_mount(self) -> None:
        """Called when app is mounted (started)."""
        try:
            if not self._is_setup:
                await self.generator.setup()
                self._is_setup = True
                # Update UI to show connection status
                results = self.query_one("#results", Static)
                results.update("Database connected successfully. You can now enter queries.")
        except Exception as e:
            results = self.query_one("#results", Static)
            results.update(f"Error connecting to database: {str(e)}")

    async def on_unmount(self) -> None:
        """Called when app is unmounted (closed)."""
        if self._is_setup:
            await self.generator.client.close()
            self._is_setup = False

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Input(placeholder="Ask a question (e.g. 'Count active users')", id="query_input"),
            Button("Execute", id="execute_btn"),
            Static(id="results"),
        )

    def format_result(self, result):
        """Format the query result into a readable string."""
        if isinstance(result, str):
            return result
        try:
            # If it's a list of dictionaries
            if isinstance(result, list):
                if not result:
                    return "No results found."
                # Get headers from first row
                headers = list(result[0].keys())
                # Create a table-like format
                output = []
                # Add headers
                header_row = " | ".join(str(h) for h in headers)
                output.append(header_row)
                output.append("-" * len(header_row))
                # Add data rows
                for row in result:
                    row_str = " | ".join(str(row.get(h, '')) for h in headers)
                    output.append(row_str)
                return "\n".join(output)
            # If it's a single dictionary
            elif isinstance(result, dict):
                return "\n".join(f"{k}: {v}" for k, v in result.items())
            # If it's a number or other simple type
            else:
                return str(result)
        except Exception as e:
            return f"Error formatting result: {str(e)}\nRaw result: {str(result)}"

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "execute_btn":
            if not self._is_setup:
                results = self.query_one("#results", Static)
                results.update("Database not connected. Please wait...")
                await self.on_mount()
                if not self._is_setup:
                    return

            input = self.query_one("#query_input", Input)
            results = self.query_one("#results", Static)
            
            try:
                query_result = await self.generator.generate_query(input.value)
                formatted_result = self.format_result(query_result)
                results.update(f"Result:\n{formatted_result}")
            except Exception as e:
                results.update(f"Error: {str(e)}")

if __name__ == "__main__":
    generator = QueryGenerator()
    app = ChatDBA(generator)
    app.run() 