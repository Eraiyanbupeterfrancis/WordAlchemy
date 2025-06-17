import tkinter as tk
from tkinter import scrolledtext, messagebox
import openai
from openai import OpenAI

token = "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"

endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)


def generate_story():
    # Get user input from entry fields and split by commas
    nouns = entry_nouns.get().split(",")
    verbs = entry_verbs.get().split(",")
    adjectives = entry_adjectives.get().split(",")
    adverbs = entry_adverbs.get().split(",")
    genre = genre_var.get()

    # Remove whitespace and empty strings from lists
    nouns = [word.strip() for word in nouns if word.strip()]
    verbs = [word.strip() for word in verbs if word.strip()]
    adjectives = [word.strip() for word in adjectives if word.strip()]
    adverbs = [word.strip() for word in adverbs if word.strip()]

    # Check if all fields have at least one word
    if not nouns or not verbs or not adjectives or not adverbs:
        messagebox.showwarning("Input Error", "Please provide words in all fields.")
        return

    # Create the prompt for the OpenAI API
    prompt = f"""
    Write a short, creative story (5-7 sentences) in the {genre} genre.
    The story should include these words:
    Nouns: {', '.join(nouns)}
    Verbs: {', '.join(verbs)}
    Adjectives: {', '.join(adjectives)}
    Adverbs: {', '.join(adverbs)}.
    Make it imaginative and fun!and in simple terms.
    """

    try:
        # Call OpenAI API to generate the story
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=1.0,
            top_p=1.0,
            model=model
        )
        # Extract the generated story from the response
        story = response.choices[0].message.content

        # Display the story in the scrolled text box
        story_box.delete(1.0, tk.END)
        story_box.insert(tk.END, story)

    except Exception as e:
        # Show error message if API call fails
        messagebox.showerror("Error", f"Failed to generate story: {e}")

# Create the main application window
root = tk.Tk()
root.title("WordAlchemy - Vocabulary Story Generator")

# Nouns input
tk.Label(root, text="Enter Nouns (comma-separated):").grid(row=0, column=0, sticky="w")
entry_nouns = tk.Entry(root, width=60)
entry_nouns.grid(row=0, column=1, padx=5, pady=5)

# Verbs input
tk.Label(root, text="Enter Verbs (comma-separated):").grid(row=1, column=0, sticky="w")
entry_verbs = tk.Entry(root, width=60)
entry_verbs.grid(row=1, column=1, padx=5, pady=5)

# Adjectives input
tk.Label(root, text="Enter Adjectives (comma-separated):").grid(row=2, column=0, sticky="w")
entry_adjectives = tk.Entry(root, width=60)
entry_adjectives.grid(row=2, column=1, padx=5, pady=5)

# Adverbs input
tk.Label(root, text="Enter Adverbs (comma-separated):").grid(row=3, column=0, sticky="w")
entry_adverbs = tk.Entry(root, width=60)
entry_adverbs.grid(row=3, column=1, padx=5, pady=5)

# Genre selection
tk.Label(root, text="Select Genre:").grid(row=4, column=0, sticky="w")
genre_var = tk.StringVar(value="sci-fi")
genres = ["sci-fi", "fantasy", "comedy", "horror", "romance"]
genre_menu = tk.OptionMenu(root, genre_var, *genres)
genre_menu.grid(row=4, column=1, sticky="w", padx=5, pady=5)

# Generate story button
generate_btn = tk.Button(root, text="Generate Story", command=generate_story)
generate_btn.grid(row=5, column=0, columnspan=2, pady=10)

# Scrolled text box to display the generated story
story_box = scrolledtext.ScrolledText(root, width=80, height=15, wrap=tk.WORD)
story_box.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()
