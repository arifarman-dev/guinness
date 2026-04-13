import requests
import json

TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

def top_stories(limit=30):
    response = requests.get(TOP_STORIES_URL)
    story_ids = response.json()[:limit]

    stories = []

    for story_id in story_ids:
        story_response = requests.get(ITEM_URL.format(story_id))
        story = story_response.json()

        comments = []
        for comment_id in story.get("kids", [])[:10]:
            comment_response = requests.get(ITEM_URL.format(comment_id))
            comment = comment_response.json()
            comments.append(comment)
        
        story["comments"] = comments
        stories.append(story)

    return stories

if __name__ == "__main__":
    stories = top_stories()

    with open("./data/stories.json", "w") as f:
        json.dump(stories, f, indent=2)

    print(f"Saved {len(stories)} stories to data/stories.json")