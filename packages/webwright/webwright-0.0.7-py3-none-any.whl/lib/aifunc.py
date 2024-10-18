import json
import os
import asyncio

from halo import Halo
from datetime import datetime

from lib.util import get_logger
from lib.util import setup_function_logging

# Import helper functions and decorators
from lib.function_wrapper import tools, callable_registry

from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit import print_formatted_text

from lib.llm import llm_wrapper
from lib.omnilog import OmniLogVectorStore

import traceback
import inspect

# Ensure the .webwright directory exists
webwright_dir = os.path.expanduser('~/.webwright')
os.makedirs(webwright_dir, exist_ok=True)

# Configure logging
logger = get_logger()

async def execute_function_by_name(function_name, f_llm, olog_history, **kwargs):
    logger.info(f"Calling {function_name} with arguments {kwargs}")
    logger.info(f"{f_llm} and {olog_history}")
    
    if function_name not in callable_registry:
        logger.error(f"Function {function_name} not found in registry")
        return json.dumps({"error": f"Function {function_name} not found in registry"})
    
    try:
        func_logger = setup_function_logging(function_name)
        func_logger.info(f"Function {function_name} called with arguments: {kwargs}")
        function_to_call = callable_registry[function_name]
        
        # Check if the function accepts 'olog' as a parameter
        function_params = inspect.signature(function_to_call).parameters
        if 'olog' in function_params:
            kwargs['olog'] = olog_history

        if 'llm' in function_params:
            kwargs['llm'] = f_llm

        if asyncio.iscoroutinefunction(function_to_call):
            # If it's a coroutine function, await it
            result = await function_to_call(**kwargs)
        else:
            # If it's a regular function, run it in a thread to avoid blocking
            result = await asyncio.to_thread(function_to_call, **kwargs)
        
        func_logger.info(f"Function {function_name} executed successfully with result: {result}")
        return json.dumps(result) if not isinstance(result, str) else result
    
    except Exception as e:
        func_logger.error(f"Function {function_name} failed with error: {e}")
        return json.dumps({"error": str(e)})

def function_calls_to_text(function_calls):
    text_descriptions = []
    for call in function_calls:
        args_text = ", ".join(f"{k}={v}" for k, v in call['arguments'].items())
        text_descriptions.append(f"Function '{call['name']}' called with arguments: {args_text}")
    return "\n".join(text_descriptions)

async def ai(username="anonymous", config=None, olog: OmniLogVectorStore = None):
    llm = llm_wrapper(config=config)

    async def call_llm_with_spinner(messages, system_prompt=None, use_tools=True):
        spinner = Halo(text='Calling LLM...', spinner='dots')
        spinner.start()
        try:
            return await llm.call_llm_api(
                messages=messages,
                system_prompt=system_prompt,
                tools=tools if use_tools else None
            )
        except Exception as e:
            raise Exception(f"Failed to get a response from LLM: {str(e)}")
        finally:
            spinner.stop()

    # Get message history (olog) and then call the LLM
    messages = olog.get_recent_entries(10)
    llm_response = await call_llm_with_spinner(messages)
    logger.info(f"LLM response: {llm_response}")

    if llm_response.get("function_calls"):
        content = llm_response.get("content") or function_calls_to_text(llm_response["function_calls"])
        olog.add_entry({
            'content': [
                {"type": "text", "text": content},
                *[{
                    "type": "tool_use",
                    "id": call['id'],
                    "name": call['name'],
                    "input": call['arguments']
                } for call in llm_response["function_calls"]]
            ],
            'type': 'llm_response',
            'timestamp': datetime.now().isoformat(),
        })
    else:
        olog.add_entry({
            'content': llm_response["content"],
            'type': 'llm_response',
            'timestamp': datetime.now().isoformat()
        })
        if llm_response.get("formatted_response"):
            print_formatted_text(llm_response["formatted_response"])
        return True

    for func_call in llm_response["function_calls"]:
        logger.info(f"Processing function call: {func_call}")
        try:
            print_formatted_text(FormattedText([('class:bold', f"Executing function: {func_call['name']}")]))
            
            if func_call["name"] == "set_api_config_dialog":
                func_call["arguments"]["spinner"] = Halo(text='Configuring API...', spinner='dots')
            
            result = await execute_function_by_name(func_call["name"], llm, olog, **func_call["arguments"])
            logger.info(f"Function {func_call['name']} executed with result: {result}")
    
            log_entry = {
                'content': [{
                    "type": "tool_result",
                    "tool_call_id": func_call['id'],
                    "name": func_call["name"],
                    "output": result
                }],
                'type': 'tool_call',
                'timestamp': datetime.now().isoformat()
            }
            logger.info(f"Logging function result: {log_entry}")
            olog.add_entry(log_entry)

            messages = olog.get_recent_entries(10)
            system_prompt = "Using the last tool response, summarize the results."
            summary_response = await call_llm_with_spinner(messages, system_prompt=system_prompt, use_tools=False)
            
            if not summary_response:
                raise Exception("Empty response from LLM during summarization")
            
            if summary_response.get("formatted_response"):
                print_formatted_text(summary_response["formatted_response"])
        
        except json.JSONDecodeError as e:
            error_message = f"Failed to parse function arguments for {func_call['name']}: {str(e)}"
            print_formatted_text(FormattedText([('class:error', error_message)]))
            logger.error(error_message)
        except Exception as e:
            error_message = f"Error executing function {func_call['name']}: {str(e)}"
            print_formatted_text(FormattedText([('class:error', error_message)]))
            print_formatted_text(FormattedText([('class:error', traceback.format_exc())]))
            logger.error(error_message, exc_info=True)

    return True
