import writer as wf



def _run_model(model,content):
    import os
    from dotenv import load_dotenv
    from openai import OpenAI
    import instructor
    import logfire
    from pydantic import BaseModel, Field
    from typing import Iterable, List

    load_dotenv()

    logfire.configure(token=os.getenv("LOGFIRE_API_KEY"))

    client = instructor.patch(
        OpenAI(
        )
    )
    logfire.instrument_openai(client)

    class PostGeneration(BaseModel):
        title: str = Field(..., description = "Title of the post")
        uid: str = Field(..., description = "Unique id for the post")
        post: str = Field(..., description = "The content of the post, this should be only the content of the topic and emojis")
        tags: List[str] = Field(..., description = "Five main relevant hashtags given for the post and #")

    return client.chat.completions.create(
        messages = [
        {
            "role": "system",
            "content": "You are a social media expert, your task is to generate engaging social\
                media posts",
        },
        {"role": "user", "content": f"""
         
        # Your task is to generate 5 social media posts content for the following topic: {content}

        ## You will generate two main part as your task, the post and the hashtags, the post should include emojis and no hashtags.

        ## Make Sure to follow the below guideline to generate them.

        ### Steps
        1. **Understand customer needs**: Start by asking for the intended use, target audience, tone, word count, style, and content format if not provided.

        2. **Create outlines**: Based on the needs, create detailed outlines for the content, dividing it into sections with summaries and word count allocations.

        3. **Manage word count**: Keep track of the word count while writing, ensuring adherence to specifications and smoothly transitioning between sections.

        4. **Creative expansion**: Use strategies such as expanding discussions, incorporating bullet points, and adding interesting facts to enrich the content while maintaining relevance and quality.

        5. **Sequential writing and delivery**: Write and deliver content section by section, updating on progress and planning the subsequent parts.

        6. **Content quality**: Integrate SEO strategies and focus on making the content engaging and suitable for the intended audience and platform.

        7. **Content formatting**: The default format is markdown, but you can structure it in any required format.

        8. **Extended interaction**: For complex topics or longer word counts, inform the user of the need for multiple responses to ensure consistency throughout the content.

        9. **The post should not include hashtags.
        
        """},
    ], 
        model=model,
        stream=True, response_model = Iterable[PostGeneration]
    )

def handle_button_click(state):
    state["message"] = "% Loading up expert social media posts..."
    posts = []
    hashtags = []
    titles = []
    for post in _run_model("gpt-3.5-turbo", state["topic"]):
        print(post)
        titles.append(post.model_dump()["title"])
        posts.append(post.model_dump()["post"])
        hashtags.append(post.model_dump()["tags"])
    state["posts"] = {title: post for title, post in zip(titles, posts)}
    print(hashtags)
    # Ensure hashtags is a list of strings
     #state["tags"] = {tags: tags for tags in hashtags}
    
    state["message"] = ""

    print(titles)
    print(state["tags"])


wf.init_state({
    "my_app": {
        "title": "SOCIAL POST GENERATOR"
    },
    "posts":"", 
    "topic":"",
    "message":"",
})




