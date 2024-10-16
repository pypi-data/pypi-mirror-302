from functools import wraps
from typing import Any, Callable, Optional, Union
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool, StructuredTool, tool

# Global variable to control mocking behavior
GLOBAL_MOCK_MODE = False

class EnhancedStructuredTool(StructuredTool):
    mock_output: Optional[Any] = None
    update_func: Optional[Callable] = None
    human_escalation: bool = False

    def run(self, *args: Any, **kwargs: Any) -> Any:
        if GLOBAL_MOCK_MODE:
            return self.get_mock_output(*args, **kwargs)

        result = super().run(*args, **kwargs)

        if self.update_func is not None:
            result = self.update_func(result)

        if self.human_escalation:
            human_input = input(f"Tool output: {result}\nDo you want to modify this? (y/n): ")
            if human_input.lower() == 'y':
                result = input("Enter new output: ")

        return result

    def get_mock_output(self, *args: Any, **kwargs: Any) -> Any:
        if self.mock_output is not None:
            return self.mock_output
        return input(f"Enter mock output for {self.name} (args: {args}, kwargs: {kwargs}): ")

def el_tool_wrapper(
    name: Optional[str] = None,
    description: Optional[str] = None,
    return_direct: bool = False,
    args_schema: Optional[type[BaseModel]] = None,
    infer_schema: bool = True,
    mock_output: Optional[Any] = None,
    update_func: Optional[Callable] = None,
    human_escalation: bool = False
):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        structured_tool = StructuredTool.from_function(
            func=wrapper,
            name=name or func.__name__,
            description=description or func.__doc__,
            return_direct=return_direct,
            args_schema=args_schema,
            infer_schema=infer_schema
        )

        enhanced_tool = EnhancedStructuredTool(
            **structured_tool.dict(),
            mock_output=mock_output,
            update_func=update_func,
            human_escalation=human_escalation
        )

        return enhanced_tool

    return decorator

def set_global_mock_mode(mode: bool):
    global GLOBAL_MOCK_MODE
    GLOBAL_MOCK_MODE = mode

# Example usage
class WikipediaInput(BaseModel):
    query: str = Field(description="The search query for Wikipedia")

@el_tool_wrapper(
    name="EnhancedWikipedia",
    description="Search Wikipedia and enhance the results",
    args_schema=WikipediaInput,
    update_func=lambda x: f"EL enhanced: {x}"
)
def enhanced_wikipedia_tool(query: str) -> str:
    """Search Wikipedia for a given query and return enhanced results."""
    # Placeholder for actual Wikipedia search logic
    return f"Wikipedia result for: {query}"

@el_tool_wrapper(
    name="DuckDuckGoSearch",
    description="Search the web using DuckDuckGo with human oversight",
    human_escalation=True
)
def wrapped_duckduckgo_tool(query: str) -> str:
    """Search the web using DuckDuckGo."""
    # Placeholder for actual DuckDuckGo search logic
    return f"DuckDuckGo search result for: {query}"

@el_tool_wrapper(
    update_func=lambda x: x.upper(),
    infer_schema=True
)
def custom_tool(input_text: str) -> str:
    """A custom tool that processes text."""
    return f"Processed: {input_text}"
