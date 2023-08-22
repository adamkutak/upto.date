ARTICLE_SUMMARIZER = """
Your job is to provide a succinct news update on the topic of {topic}.
Use the contents of the raw articles below. They have been scraped from the internet, so there may be formatting issues.
Each article includes the link where it was retrieved, and the contents.
Do not make anything up. All information should come from the articles.
There could be multiple stories on this topic. Make sure to cover each story.
Multiple articles may talk about the same story, make sure to summarize each story, not each article. Don't repeat yourself.
You can decide which stories are more/less important, and correspondingly give them more/less words in your output.
However, it is important to at least touch on each story surrounding this topic.
The word count should be around {word_count} words.

The raw articles are below:
{article_string}
"""

ARTICLE_SUMMARIZER_ERROR = """
The output you gave me returned this error: {error}.
Your output is supposed to be parsed into a json, then the "content" and "links" objects are extracted directly.
Can you try again but make sure it is valid json, with the "content" and "links" objects at the top level?
Do not write an apology message or anything else. You should only return valid json.
"""

ARTICLE_EXTRAS = """
Below is a newsletter that gives updates on various topics. Create an introduction and title.
It should flow well with the entire newsletter. It is also crucial that the introduction and title work together, and don't repeat themselves.

The title should be no more than {title_word_count} words. It doesn't have to touch on every topic.
The introduction should be no more than {introduction_word_count} words. It should reference at least most of the topics in the newsletter.

The newsletter:
{newsletter}
"""

ARTICLE_EXTRAS_ERROR = """
The output you gave me returned this error: {error}.
Your output is supposed to be parsed into a json, then the "introduction" and "title" objects are extracted directly.
Can you try again but make sure it is valid json, with the "introduction" and "title" objects at the top level?
Do not write an apology message or anything else. You should only return valid json.
"""
