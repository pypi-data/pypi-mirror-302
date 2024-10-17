import os


class use_proxy:
    def __enter__(self):
        os.environ["http_proxy"] = os.getenv("OPENAI_HTTP_PROXY")
        os.environ["https_proxy"] = os.getenv("OPENAI_HTTP_PROXY")
        return self

    def __exit__(self, *args):
        os.environ.pop("http_proxy")
        os.environ.pop("https_proxy")
