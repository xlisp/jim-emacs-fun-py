# https://microsoft.github.io/autogen/docs/topics/non-openai-models/local-litellm-ollama/#example-with-function-calling

from typing import Literal
from typing_extensions import Annotated
import autogen
from langfuse import Langfuse
#from langfuse.decorators import trace
#https://langfuse.com/docs/sdk/python/decorators
from langfuse.decorators import observe
import os 

# Langfuse initialization
langfuse = Langfuse(
    public_key=os.environ['LANGFUSE_PUBLIC_KEY'],
    secret_key=os.environ['LANGFUSE_SECRET_KEY'],
    host="https://us.cloud.langfuse.com"
)

local_llm_config = {
    "config_list": [
        {
            "model": "ollama/llama3.1",
            "api_key": "NULL",
            "api_type": "open_ai",
            "base_url": "http://0.0.0.0:4000",
            "price": [0, 0],
        }
    ],
    "cache_seed": None,
}

chatbot = autogen.AssistantAgent(
    name="chatbot",
    system_message="""For currency exchange tasks,
        only use the functions you have been provided with.
        If the function has been called previously,
        return only the word 'TERMINATE'.""",
    llm_config=local_llm_config,
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and "TERMINATE" in x.get("content", ""),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=1,
    code_execution_config={"work_dir": "code", "use_docker": False},
)

CurrencySymbol = Literal["USD", "EUR"]

def exchange_rate(base_currency: CurrencySymbol, quote_currency: CurrencySymbol) -> float:
    if base_currency == quote_currency:
        return 1.0
    elif base_currency == "USD" and quote_currency == "EUR":
        return 1 / 1.1
    elif base_currency == "EUR" and quote_currency == "USD":
        return 1.1
    else:
        raise ValueError(f"Unknown currencies {base_currency}, {quote_currency}")

@user_proxy.register_for_execution()
@chatbot.register_for_llm(description="Currency exchange calculator.")
@observe()
def currency_calculator(
    base_amount: Annotated[float, "Amount of currency in base_currency"],
    base_currency: Annotated[CurrencySymbol, "Base currency"] = "USD",
    quote_currency: Annotated[CurrencySymbol, "Quote currency"] = "EUR",
) -> str:
    quote_amount = exchange_rate(base_currency, quote_currency) * base_amount
    langfuse.event("currency_conversion_completed")
    return f"{format(quote_amount, '.2f')} {quote_currency}"

@observe()
def main():
    res = user_proxy.initiate_chat(
        chatbot,
        message="How much is 123.45 EUR in USD?",
        summary_method="reflection_with_llm",
    )
    langfuse.score("conversation_completed", 1.0)
    return res

if __name__ == "__main__":
    main()
    langfuse.flush()

