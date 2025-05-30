from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
import os,asyncio
from autogen_core import CancellationToken
from autogen_core import Image as AGImage
from PIL import Image
from autogen_agentchat.messages import MultiModalMessage
from  autogen_core.models import ModelInfo
async def main() -> None:  
    image = Image.open('imagesummarizer/pic1.jpg')
    
    img = AGImage(image)

    model_client = OllamaChatCompletionClient(
    model="qwen3:latest",
    base_url = "http://localhost:11434",
    model_info=ModelInfo(vision=True,function_calling=True,json_output=False)
    )
    multiModalMessage = MultiModalMessage(content=["Summarize what this picture depicts in detail",img],source='user')

    describer = AssistantAgent(
        name="Image_Describer",
        model_client=model_client,
        system_message="You are an expert image describer. You will be given an image and you need to describe it in detail.",
    )

    res=await describer.on_messages([multiModalMessage],cancellation_token=CancellationToken())
    print(res.chat_message.content)
if __name__ == "__main__":
    asyncio.run(main())