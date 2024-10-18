import pathlib
import os
import base64
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

SCREENSHOTS_DIR = "/home/rjouhameau/Pictures/Screenshots/"


def get_latest_created_screenshot(dir_path: str) -> pathlib.Path | None:
    screenshots_dir = pathlib.Path(dir_path)

    if not screenshots_dir.exists():
        raise FileNotFoundError(f"Directory {dir_path} does not exist.")
    return max(
        screenshots_dir.glob("*.png"), key=lambda x: x.stat().st_ctime, default=None
    )


def encode_image(image_path: str | pathlib.Path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


llm = ChatOpenAI(model="gpt-4o", api_key=os.environ.get("OPENAI_API_KEY"))


last_screenshot = get_latest_created_screenshot(SCREENSHOTS_DIR)
base64_image = encode_image(last_screenshot)


res = llm.invoke(
    [
        HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": "From this image, extract the diagrams using mermaid so that I can add them to my markdown document",
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                },
            ]
        )
    ]
)

print(res)

print(res.content)
