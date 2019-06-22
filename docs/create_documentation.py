import shutil
import os

from md_autogen import to_md_file
from md_autogen import MarkdownAPIGenerator

from model_server import core
from model_server.utils import tensor_utils
from model_server.utils import prediction_utils
from model_server.utils import model_info_utils


def generate_api_docs():
    modules = [
        core,
        tensor_utils,
        prediction_utils,
        model_info_utils
    ]

    md_gen = MarkdownAPIGenerator("model_server", "https://github.com/Abhijit-2592/model-server/tree/master")
    for m in modules:
        md_string = md_gen.module2md(m)
        to_md_file(md_string, m.__name__, "sources")


def remove_sources():
    shutil.rmtree("sources", ignore_errors=True)


def update_index_md():
    os.mkdir("sources")
    shutil.copyfile('../README.md', 'sources/index.md')


if __name__ == "__main__":
    remove_sources()
    update_index_md()
    generate_api_docs()
