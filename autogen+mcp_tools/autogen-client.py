import asyncio
from autogen_ext.tools.mcp import McpWorkbench, StdioServerParams,mcp_server_tools 
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ModelInfo
from autogen_core import CancellationToken

async def main() -> None:
    params = StdioServerParams(
        command="python",
        args=["autogen+mcp_tools/server.py"],
        read_timeout_seconds=60,
    )

    
    tools = await mcp_server_tools(params)
    print(tools)

    model_client = OllamaChatCompletionClient(
    model="qwen3:latest",
    base_url = "http://localhost:11434",
    model_info=ModelInfo(vision=True,function_calling=True,json_output=False)
    )

    agent = AssistantAgent(
        name="Email_Sender",
        model_client=model_client,
        system_message="You are an expert email sender. You will be given an email address, subject, and body. You need to send the email using the tools provided.",
        tools=tools
    )
    
    await agent.run(task="write a mail sick leave mail for tomorrow to rishabhrawat526@gmail.com ", cancellation_token=CancellationToken())
    
if __name__ == "__main__":
    asyncio.run(main())
