import pathlib
import os
import base64
import openai

SCREENSHOTS_DIR = "/home/rjouhameau/Pictures/Screenshots/"


def get_latest_created_screenshot(dir_path: str) -> pathlib.Path | None:
    screenshots_dir = pathlib.Path(dir_path)

    if not screenshots_dir.exists():
        raise FileNotFoundError(f"Directory {dir_path} does not exist.")
    return max(
        screenshots_dir.glob("*.png"), key=lambda x: x.stat().st_ctime, default=None
    )


get_latest_created_screenshot(SCREENSHOTS_DIR)


client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def encode_image(image_path: str | pathlib.Path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


last_screenshot = get_latest_created_screenshot(SCREENSHOTS_DIR)
base64_image = encode_image(last_screenshot)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": [
                # {"type": "text", "text": "Describe the image given to you"},
                {
                    "type": "text",
                    "text": "Extract the table from the image, and output a markdown table. However, I want to perform some modifications. For the first column, create a 'standard' column which would take either as value 'luxury' or  'premium'. And the second column, 'type',  with value of either 'properties' or 'rooms'. For the third column, put the 'hostel_name'. For the rest, stick to what the table display",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}",
                    },
                },
            ],
        },
    ],
)


print(response.choices[0].message.content)
