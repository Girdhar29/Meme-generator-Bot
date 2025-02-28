# import os
# import logging
# import requests
# from datetime import datetime
# from dotenv import load_dotenv
# from openai import OpenAI
# from textblob import TextBlob
# from .models import Meme
#
# # Load environment variables
# load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
#
# # Initialize OpenAI client
# client = OpenAI(api_key=OPENAI_API_KEY)
#
#
# def correct_spelling(text):
#     """Corrects spelling in the given text."""
#     return str(TextBlob(text).correct())
#
#
# def generate_meme_text(comment_text):
#     """Generate a witty meme caption and tweet-style text without spelling mistakes."""
#     try:
#         response = client.chat.completions.create(
#             model="gpt-4-turbo",
#             messages=[
#                 {"role": "system", "content": """You are a Twitter/X meme bot that responds to user comments with viral meme captions.
#                 - Make it **humorous, sarcastic, or absurdly relatable**.
#                 - Ensure **perfect grammar and spelling** (No mistakes).
#                 - Fit **current meme trends and Twitter culture**.
#                 - Your response should include:
#                   1. A **short text overlay** for the meme image.
#                   2. A **tweet-style caption** (under 280 characters) for engagement.
#                 - Ensure the meme aligns with the comment's sentiment and topic."""},
#                 {"role": "user", "content": f"Generate a funny meme caption for this comment: '{comment_text}'"}
#             ]
#         )
#
#         meme_text = response.choices[0].message.content.strip()
#         return meme_text
#
#     except Exception as e:
#         logging.error(f"Error generating meme text: {e}")
#         return "When life gives you lemons, make memes!"
#
#
# def generate_meme_image(comment_text):
#     """Generate a meme image using OpenAI DALL·E and return the image URL."""
#     try:
#         response = client.images.generate(
#             model="dall-e-3",
#             prompt=f"""Create a viral meme responding to this comment: '{comment_text}' do not do speling mistake in image text.
#             Use a popular meme format with bold, legible text (e.g., Impact font) placed at the top and/or bottom to avoid covering key image elements.
#             Ensure proper grammar, spacing, and alignment for a polished look.
#             If needed, add a contrasting background for readability.
#             The meme should be optimized for social media sharing (X/Twitter, Instagram, etc.) to maximize engagement.""",
#             n=1,
#             size="1024x1024"
#         )
#         return response.data[0].url
#     except Exception as e:
#         logging.error(f"Error generating meme image: {e}")
#         return None
#
#
# def download_and_save_image(image_url):
#     """Download and save the meme image locally with improved quality."""
#     try:
#         media_dir = "media"
#         os.makedirs(media_dir, exist_ok=True)
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         save_path = os.path.join(media_dir, f"meme_{timestamp}.png")
#
#         response = requests.get(image_url, stream=True)
#         if response.status_code == 200:
#             with open(save_path, 'wb') as file:
#                 for chunk in response.iter_content(1024):
#                     file.write(chunk)
#             return save_path
#         else:
#             logging.error(f"Failed to download image. HTTP Status: {response.status_code}")
#             return None
#     except Exception as e:
#         logging.error(f"Error downloading image: {e}")
#         return None
#
#
# # def save_meme_to_db(user_prompt, caption, image_url, saved_image_path):
# #     """Save the meme details to the database."""
# #     try:
# #         Meme.objects.create(
# #             user_prompt=user_prompt,
# #             caption=caption,
# #             image_url=image_url,
# #             local_image_path=saved_image_path
# #
# #         )
# #     except Exception as e:
# #         logging.error(f"Error saving meme to DB: {e}")
#
# def respond_to_comment(comment_text):
#     """Generate a meme and save it in response to a comment."""
#     meme_text = generate_meme_text(comment_text)  # Generate caption
#     image_url = generate_meme_image(comment_text)  # Get meme image URL
#
#     if not image_url:
#         logging.error("Failed to generate meme image.")
#         return None, None, None
#
#     saved_image_path = download_and_save_image(image_url)  # Save image locally
#
#     if not saved_image_path:
#         logging.error("Failed to download and save image.")
#         return None, None, None
#
#     #  Ensure `image_url`, `meme_text`, and `saved_image_path` are all returned
#     logging.info(f"Meme generated for comment: '{comment_text}'")
#     return image_url, meme_text, saved_image_path
#
#
#



import os
import logging
import aiohttp
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from textblob import TextBlob
from .models import Meme

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

async def correct_spelling(text):
    """Correct spelling asynchronously."""
    return str(TextBlob(text).correct())

async def generate_meme_text(comment_text):
    """Generate a witty meme caption asynchronously."""
    try:
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a Twitter/X meme bot..."},
                {"role": "user", "content": f"Generate a funny meme caption: '{comment_text}'"}
            ]
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        logging.error(f"Error generating meme text: {e}")
        return "When life gives you lemons, make memes!"

async def generate_meme_image(comment_text):
    """Generate a meme image asynchronously using OpenAI DALL·E."""
    try:
        response = await asyncio.to_thread(
            client.images.generate,
            model="dall-e-3",
            prompt=f"Create a viral meme responding to '{comment_text}'...",
            n=1,
            size="1024x1024"
        )
        return response.data[0].url
    except Exception as e:
        logging.error(f"Error generating meme image: {e}")
        return None

async def download_and_save_image(image_url):
    """Download meme image asynchronously."""
    try:
        media_dir = "media"
        os.makedirs(media_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = os.path.join(media_dir, f"meme_{timestamp}.png")

        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                if response.status == 200:
                    with open(save_path, 'wb') as file:
                        file.write(await response.read())
                    return save_path
                else:
                    logging.error(f"Failed to download image. HTTP Status: {response.status}")
                    return None
    except Exception as e:
        logging.error(f"Error downloading image: {e}")
        return None

async def respond_to_comment(comment_text):
    """Generate a meme asynchronously."""
    meme_text = await generate_meme_text(comment_text)
    image_url = await generate_meme_image(comment_text)

    if not image_url:
        logging.error("Failed to generate meme image.")
        return None, None, None

    saved_image_path = await download_and_save_image(image_url)

    if not saved_image_path:
        logging.error("Failed to download and save image.")
        return None, None, None

    logging.info(f"Meme generated for comment: '{comment_text}'")
    return image_url, meme_text, saved_image_path











#
# # for integration with X(Twitter)
#
# import os
# import logging
# import requests
# import tweepy
# from datetime import datetime
# from dotenv import load_dotenv
# from openai import OpenAI
# from textblob import TextBlob
# from .models import Meme
#
# # Load environment variables
# load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
#
# # Initialize OpenAI client
# client = OpenAI(api_key=OPENAI_API_KEY)
#
# # Twitter API authentication
# TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
# TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
# TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
# TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
#
# auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
# auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
# twitter_api = tweepy.API(auth)
#
#
# def generate_meme_text(comment_text):
#     """Generate a witty meme caption and tweet-style text without spelling mistakes."""
#     try:
#         response = client.chat.completions.create(
#             model="gpt-4-turbo",
#             messages=[
#                 {"role": "system", "content": """You are a Twitter/X meme bot that responds to user comments with viral meme captions.
#                     - Make it **humorous, sarcastic, or absurdly relatable**.
#                     - Ensure **perfect grammar and spelling** (No mistakes).
#                     - Fit **current meme trends and Twitter culture**.
#                     - Your response should include:
#                       1. A **short text overlay** for the meme image.
#                       2. A **tweet-style caption** (under 280 characters) for engagement.
#                     - Ensure the meme aligns with the comment's sentiment and topic."""},
#                 {"role": "user", "content": f"Generate a funny meme caption for this comment: '{comment_text}'"}
#             ]
#         )
#
#         meme_text = response.choices[0].message.content.strip()
#         return meme_text
#
#     except Exception as e:
#         logging.error(f"Error generating meme text: {e}")
#         return "When life gives you lemons, make memes!"
#
#
# def generate_meme_image(comment_text):
#     """Generate a meme image using OpenAI DALL·E and return the image URL."""
#     try:
#         response = client.images.generate(
#             model="dall-e-3",
#             prompt=f"""Create a viral meme responding to this comment: '{comment_text}'.
#                 Use a popular meme format with bold, legible text (e.g., Impact font) placed at the top and/or bottom to avoid covering key image elements.
#                 Ensure proper grammar, spacing, and alignment for a polished look.
#                 If needed, add a contrasting background for readability.
#                 The meme should be optimized for social media sharing (X/Twitter, Instagram, etc.) to maximize engagement.""",
#             n=1,
#             size="1024x1024"
#         )
#         return response.data[0].url
#     except Exception as e:
#         logging.error(f"Error generating meme image: {e}")
#         return None
#
#
# def download_and_save_image(image_url):
#     """Download and save the meme image locally with improved quality."""
#     try:
#         media_dir = "media"
#         os.makedirs(media_dir, exist_ok=True)  # Ensure directory exists
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         save_path = os.path.join(media_dir, f"meme_{timestamp}.png")  # PNG for better quality
#
#         response = requests.get(image_url, stream=True)
#         if response.status_code == 200:
#             with open(save_path, 'wb') as file:
#                 for chunk in response.iter_content(1024):
#                     file.write(chunk)
#             return save_path
#         else:
#             logging.error(f"Failed to download image. HTTP Status: {response.status_code}")
#             return None
#     except Exception as e:
#         logging.error(f"Error downloading image: {e}")
#         return None
#
#
# def post_meme_on_twitter(comment_id, caption, image_path):
#     """Post a meme as a reply to a specific Twitter comment."""
#     try:
#         media = twitter_api.media_upload(image_path)  # Upload the image
#         tweet = twitter_api.update_status(status=caption, media_ids=[media.media_id_string],
#                                           in_reply_to_status_id=comment_id, auto_populate_reply_metadata=True)
#         return f"https://twitter.com/user/status/{tweet.id}"
#     except Exception as e:
#         logging.error(f"Error posting meme on Twitter: {e}")
#         return None
#
#
# def respond_to_comment(comment_text, comment_id):
#     """Generate a meme, save it, and post it on Twitter."""
#     meme_text = generate_meme_text(comment_text)  # Generate caption
#     image_url = generate_meme_image(comment_text)  # Get meme image URL
#
#     if not image_url:
#         logging.error("Failed to generate meme image.")
#         return None, None, None
#
#     saved_image_path = download_and_save_image(image_url)  # Save image locally
#
#     if not saved_image_path:
#         logging.error("Failed to download and save image.")
#         return None, None, None
#
#     # Post meme as a reply to the comment on Twitter
#     tweet_url = post_meme_on_twitter(comment_id, meme_text, saved_image_path)
#
#     if not tweet_url:
#         logging.error("Failed to post meme on Twitter.")
#         return None, None, None
#
#     logging.info(f"Meme generated and posted for comment: '{comment_text}'")
#     return image_url, meme_text, tweet_url





## direct for post

# def post_direct_meme(caption, image_path):
#     """Post a meme directly on Twitter (not a reply)."""
#     try:
#         media = twitter_api.media_upload(image_path)  # Upload the image
#         tweet = twitter_api.update_status(status=caption, media_ids=[media.media_id_string])  # Direct tweet
#
#         return f"https://twitter.com/user/status/{tweet.id}"  # Return tweet link
#     except Exception as e:
#         logging.error(f"Error posting meme directly on Twitter: {e}")
#         return None
#
#
# def post_direct_meme_flow(meme_topic):
#     """Generate a meme, save it, and post it directly on Twitter."""
#     meme_text = generate_meme_text(meme_topic)  # Generate caption
#     image_url = generate_meme_image(meme_topic)  # Generate meme image
#
#     if not image_url:
#         logging.error("Failed to generate meme image.")
#         return None, None, None
#
#     saved_image_path = download_and_save_image(image_url)  # Save image locally
#
#     if not saved_image_path:
#         logging.error("Failed to download and save image.")
#         return None, None, None
#
#     # Post meme as a new tweet (not a reply)
#     tweet_url = post_direct_meme(meme_text, saved_image_path)
#
#     if not tweet_url:
#         logging.error("Failed to post meme on Twitter.")
#         return None, None, None
#
#     logging.info(f"Meme generated and posted: '{meme_topic}'")
#     return image_url, meme_text, tweet_url



## prompt for text
# def generate_meme_text(meme_topic):
#     """Generate a meme caption based on a given topic for a direct Twitter post."""
#     prompt = f"""
#     You are a funny meme generator. Create a short and witty tweet-style caption
#     related to '{meme_topic}'. Keep it engaging, humorous, and relevant.
#     Avoid hashtags, and keep it concise within Twitter's character limit.
#     """
#
#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         messages=[{"role": "system", "content": prompt}]
#     )
#
#     return response["choices"][0]["message"]["content"].strip()

## for image
# def generate_meme_image(meme_topic):
#     """Generate a meme image using OpenAI DALL·E for direct Twitter posting."""
#     prompt = f"""
#     Create a viral meme on '{meme_topic}'.
#     - Use a popular meme format that is instantly recognizable.
#     - Add bold, legible text (like Impact font) at the top and/or bottom.
#     - Ensure proper grammar, spacing, and alignment.
#     - The meme should be relatable, funny, and perfect for Twitter/X.
#     - Optimize for social media engagement and virality.
#     """
#
#     response = client.images.generate(
#         model="dall-e-3",
#         prompt=prompt,
#         n=1,
#         size="1024x1024"
#     )
#
#     return response.data[0].url
