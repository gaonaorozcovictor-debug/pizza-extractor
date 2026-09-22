from langchain.chat_models import init_chat_model
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import os
import getpass

load_dotenv()

if "ANTHROPIC_API_KEY" not in os.environ:
    os.environ["ANTHROPIC_API_KEY"] = getpass.getpass("Introduce tu  AWS Key: ")


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ORDERS_PATH = PROJECT_ROOT / "data" / "example_orders"


#################################################################
# Define the schema
#################################################################
from typing import List
from pydantic import BaseModel, Field


class Pizza(BaseModel):
    """Transcription of the pizza order."""

    pizza_order: str = Field(
        ..., description="The pizza order transcription."
    )

class Pizza_order_list(BaseModel):
    """ Generated Pizza orders"""
    # Creates a model so that we can extract multiple entities.
    order_list: List[Pizza]


#####################################################################################
# Generate examples
#####################################################################################
def generate_structured_example_orders(model_name, prompt, provider=None, temperature = 0.7):
    model = init_chat_model(
        model_name,
        model_provider=provider,
        temperature = temperature
    )
    structured_llm = model.with_structured_output(schema=Pizza_order_list)
    response = structured_llm.invoke(prompt)
    return response

#####################################################################################
# Save examples
#####################################################################################

def save_orders_to_file(content) -> Path:
    ORDERS_PATH.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = ORDERS_PATH / f"pedidos_pizza_{timestamp}.json"

    output_file.write_text(
        content.model_dump_json(indent=2),
        encoding="utf-8",
    )

    return output_file

#####################################################################################
# Load examples
#####################################################################################
def load_orders_as_list(filename: str) -> list[str]:
    """Lädt eine JSON-Datei aus data/example_orders und gibt die Orders als Liste zurück."""
    data_path = Path.cwd().parent / "data" / "example_orders"
    path = ORDERS_PATH / filename
    data = json.loads(path.read_text(encoding="utf-8"))

    return [order["pizza_order"] for order in data["order_list"]]


if __name__ == "__main__":
    result = generate_structured_example_orders()
    print(result)