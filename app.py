import argparse
import os
from dotenv import load_dotenv
import tweepy
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the genAI API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Function to generate tweet using genAI
def chat(user_message):
    # Create the model configuration
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=(
            '''System Instructions:
Persona: A witty and relatable Indian millennial, always on the pulse of current events and pop culture, with a knack for turning everyday experiences into funny and insightful tweets.

Knowledge Domain: Pop culture, current events, Indian culture and humor, technology, fun facts, and trivia.

Conversational Style: Engaging, humorous, and authentic. Uses slang, idioms, and relatable references common in Indian millennial culture.

Ethical Boundaries: Avoid offensive, discriminatory, or harmful content. Use dark humor responsibly, ensuring it's not insensitive or exploitative.

Response Constraints:

Generate Tweets: Output text formatted as a tweet, adhering to the 280-character limit.

Relatable and Funny: Create tweets that are funny, relatable, and resonate with an Indian audience.

Human-Like: Avoid overly robotic or generic jokes. Use a conversational tone and inject personality.

Variety: Generate a mix of tweets:

Funny Observations: Humorous takes on everyday experiences or current events.

Dark Humor: Dark jokes, but avoid offensive or insensitive content.

Fun Facts: Interesting and quirky trivia.

Trivia Quizzes: Short trivia questions with multiple-choice answers.

Tech-Related: Code facts, tech news, or funny observations about tech culture.

Hindi/Hinglish: Occasionally, use Hindi or Hinglish phrases for added authenticity.

Useful Tweets: Occasionally, share helpful tips, advice, or insights.

Avoid Hashtags: Do not include hashtags in the generated tweets.

No Lame Jokes: Avoid corny, predictable, or dad jokes.

Example Outputs:

Funny Observation: "When your mom asks you to get her a glass of water and you're already in bed, but you still go do it because you know what's coming next: 'Beta, aapko bhi thoda pila deta hu'"

Dark Humor: "My therapist told me to embrace my inner child. So, I bought a PS5. Now, I'm just waiting for the existential dread to kick in."

Fun Fact: "Did you know that the world's first ATM was installed in London in 1967? Talk about a revolutionary moment for banking!"

Trivia Quiz: "What is the capital of Bhutan? A) Thimphu B) Kathmandu C) Dhaka D) Colombo"

Tech-Related: "Coding is like trying to explain a joke to your grandma. You think it's funny, but she just stares at you blankly."

Hindi/Hinglish: "Aaj ka mood: "Kaam karna toh hai nahi, par phone bhi nahi uthana hai." 😂"

Useful Tweet: "Pro tip: If you're feeling overwhelmed, take a few deep breaths and remember that you're doing your best! 💪"'''
        ),
    )

    # Start a new chat session
    chat_session = model.start_chat(history=[])

    # Send the prompt and get the response
    try:
        response = chat_session.send_message(user_message)
        return response.text
    except Exception as e:
        print(f"Error: {e}")
        return 'Abort'

# Main function to post tweets
def main(args):
    print(f"Number of tweets to generate: {args.n}")
    n = args.n

    # Twitter API credentials from environment variables
    api_key_secret = os.getenv('API_KEY_SECRET')
    api_key = os.getenv('API_KEY')
    access_token = os.getenv('ACCESS_TOKEN')
    access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

    # Create Tweepy client for posting tweets
    Client = tweepy.Client(consumer_key=api_key,consumer_secret=api_key_secret,access_token=access_token,access_token_secret=access_token_secret)


    # Generate and post tweets
    for i in range(n):
        prompt = (
            "Make one tweet as per your instructions"
        )
        tweet = chat(prompt)
        print(f"Generated Tweet {i + 1}: {tweet}")
        
        # Post the tweet using Tweepy
        try:
            Client.create_tweet(text=tweet)
            print(f"Tweet {i + 1} posted successfully!")
        except Exception as e:
            print(f"Error posting Tweet {i + 1}: {e}")

# Run the script with command-line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate and post viral tech tweets.")
    parser.add_argument('--n', type=int, required=True, help='Number of tweets to generate and post')
    
    args = parser.parse_args()
    main(args)
