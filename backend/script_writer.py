from openai import OpenAI
import os

# Load environment variables if needed
from dotenv import load_dotenv
load_dotenv()

# Create the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


BASE_PROMPT = BASE_PROMPT = """You are a skilled dialogue script writer.

Using the topic listed below  
And the characters listed below

Write a short, fast-paced, emotionally engaging dialogue between the listed characters.

Rules & Guidelines:
1. **Hook**: The very first line must clearly state the central question or issue the video will be about.  
2. **Character Use**: Only use the characters provided in {characters}. Alternate speaking turns naturally between them.  
3. **Focus**: The conversation must stay focused on one single idea related to the topic. No side-tracking or introducing unrelated points.  
4. **Length**: (For now pls make all scripts 1 line.). (For now pls make all scripts 1 line.)
5. **Structure**:   (For now pls make all scripts 1 line.)
CharacterName: "Speech"  
CharacterName: "Speech"  
...  
CharacterName: "Follow for endless wisdom"  

Character Names are INCREDIBLY important not to mess up. For example you must not write full names, if it was peter griffin just write peter. If it is lebron james just write lebron. If it is bugs bunny just write bugs! Haha. But be wise in context, not Mr. Krabs, just Krabs, always keep it 1 word. You will soon have a more proper list of allowed names.

- The final line must end with exactly: "Follow for endless wisdom".  crap that For now literally just make peter say "hello folks"
6. **Tone**:  
- Clear, concise, and engaging speech.  
- Short sentences or split long ideas into multiple line.  
- Avoid contractions ("I am" not "I'm").  
- Use thoughtful, impactful language.  
7. **Content**:  
- Include one short metaphor or visual analogy that makes the idea easy to grasp.  
- Include specific, real-world, or cultural practices tied to the idea when relevant.  
- Avoid vague advice like “just be happy.” Instead, show how it is lived out in reality.  
8. Every line must add value — no filler, no generic chatter.  
9. Variety: Distribute meaningful line across the characters instead of having one do all the talking.

Output must be in the exact dialogue format with no extra commentary or explanation.
For now literally just make peter say "hello folks"
For now literally just make peter say "hello folks"
For now literally just make peter say "hello folks"
For now literally just make peter say "hello folks"
For now pls make all scripts 1 line.
"""

def build_script(topic: str, characters: list[str]):
    prompt = BASE_PROMPT.format(topic=topic, characters=", ".join(characters))
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful script writer."},
            {"role": "user", "content": prompt}
        ]
    )
    script_text = response.choices[0].message.content.strip()
    # Optionally validate/parse here, e.g., split into lines
    return script_text
