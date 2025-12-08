import os
os.environ["USE_TF"] = "0"

from langchain_community.document_loaders import WebBaseLoader
import bs4


class WebTransfer:
    def __init__(self):
        pass

    def transfer(self, link):

        # Real browser user-agent (VERY IMPORTANT)
        headers = {
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
        }

        # DO NOT ADD "features" HERE - WebBaseLoader already adds it
        bs_args = {
            "parse_only": bs4.SoupStrainer(["main", "article", "div"])
        }

        loader = WebBaseLoader(
            web_paths=(link,),
            header_template=headers,
            bs_kwargs=bs_args
        )

        return loader.load()


if __name__ == "__main__":
    obj = WebTransfer()
    docs = obj.transfer("https://www.w3schools.com/java/java_intro.asp")

    print(docs)
