from utils import search, extract_article
import json
from prompts import (
    ARTICLE_SUMMARIZER,
    ARTICLE_EXTRAS,
    ARTICLE_SUMMARIZER_ERROR,
    ARTICLE_EXTRAS_ERROR,
)
import openai

MAX_ARTICLES = 3


# TODO: add style option (silly, serious, witty, etc)


def create_initial_article(
    topic_list: list[str],
    word_count: int,
    title_word_count: int = None,
    introduction_word_count: int = None,
    article_count: int = MAX_ARTICLES,
):
    newsletter = ""
    links = []
    for topic in topic_list:
        article_list = []
        title_url_collection = search(topic, article_count)
        for title_url in title_url_collection:
            article_contents = extract_article(title_url["link"])
            article_contents = article_contents.replace("\n\n\n", "")
            extracted_text = {
                "link": title_url["link"],
                "contents": article_contents,
            }

            article_list.append(str(extracted_text))

        string_article_list = "\n\n".join(article_list)

        prompt = ARTICLE_SUMMARIZER.format(
            topic=topic,
            word_count=word_count,
            article_string=string_article_list,
        )
        system_message = """
        You are an expert journalist.
        Return a json object with two elements. These two elements should be the top level elements.
        The first, content, is the body of your summary article.
        The second, links, is a list of links from which you gathered your information.
        You don't have to use information from each link you are given.
        If you don't use some sources, then do not put their corresponding links in the 'links' return object.
        """

        messages = openai_chat_response(
            prompt=prompt,
            system_message=system_message,
        )
        topic_summary = messages[-1]

        print("starting new topic")

        encoutering_errors = True
        attempts = 1
        while encoutering_errors and attempts >= 0:
            print("entering/reentering loop")
            encoutering_errors = False
            attempts -= 1
            try:
                topic_summary_dict = json.loads(topic_summary.content)
                newsletter += topic_summary_dict["content"]
                newsletter += "\n\n"
                links.extend(topic_summary_dict["links"])
            except Exception as e:
                encoutering_errors = True
                messages = openai_chat_response(
                    prompt=ARTICLE_SUMMARIZER_ERROR.format(error=e),
                    existing_messages=messages,
                )
                topic_summary = messages[-1]

    introduction, title = create_newsletter_extras(
        newsletter,
        title_word_count,
        introduction_word_count,
    )

    newsletter = introduction + "\n\n" + newsletter

    return newsletter, title


# create an introduction from the final article
def create_newsletter_extras(
    newsletter, title_word_count=20, introduction_word_count=60
):
    prompt = ARTICLE_EXTRAS.format(
        title_word_count=title_word_count,
        introduction_word_count=introduction_word_count,
        newsletter=newsletter,
    )
    system_message = """
    You are an expert journalist.
    You need to write an introduction and title for the newsletter.
    Return a json object with two items: introduction and title.
    These two elements should be the top level elements.
    """
    messages = openai_chat_response(
        prompt=prompt,
        system_message=system_message,
    )
    extras = messages[-1]

    encoutering_errors = True
    attempts = 1
    while encoutering_errors and attempts >= 0:
        encoutering_errors = False
        attempts -= 1
        try:
            extras_dict = json.loads(extras.content)
            introduction = extras_dict["introduction"]
            title = extras_dict["title"]
        except Exception as e:
            messages = openai_chat_response(
                prompt=ARTICLE_EXTRAS_ERROR.format(error=e),
                existing_messages=messages,
            )
            extras = messages[-1]

    return introduction, title


# create a langchain agent that takes in the article summary
# it should then go out on its own, and update the summary with regular google search results
def execute_search_agent():
    pass


# FUTURE: checker agent that takes in the article, then analyzes if it is true using search and scrape tools
def execute_checker_agent():
    pass


# FUTURE: delta agent that looks at the difference between the previous newsletter and this one. It ensures that news isn't repeated.
def execute_delta_agent():
    pass


def openai_chat_response(
    prompt,
    model="gpt-3.5-turbo-16k",
    system_message=None,
    existing_messages=None,
):
    messages = []
    if system_message:
        messages.append(
            {
                "role": "system",
                "content": system_message,
            }
        )
    elif existing_messages:
        messages.extend(existing_messages)

    messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )

    messages.append(response.choices[0].message)
    return messages


def run():
    my_topic_list = [
        "China real estate",
        "Superconductors",
        "SpaceX Starship rocket",
    ]
    article, title = create_initial_article(
        topic_list=my_topic_list,
        word_count=150,
        title_word_count=30,
        introduction_word_count=100,
        article_count=4,
    )

    print(title)
    print()
    print(article)


run()
