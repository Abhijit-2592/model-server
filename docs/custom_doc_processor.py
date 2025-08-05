import re
from functools import partial

from pydoc_markdown.contrib.processors.pydocmd import PydocmdProcessor

sub = partial(re.sub, flags=re.M)


class DocProcessor(PydocmdProcessor):
    def _process(self, node):
        if not getattr(node, "docstring", None):
            return

        # join long lines ending in escape (\)
        c = sub(r"\\\n\s*", "", node.docstring.content)
        # escape literal `*`
        c = sub(r"^(\w+\s{2,}:.*?)\*(.*?)$", r"\1\\*\2", c)
        # convert parameter lists to markdown list
        c = sub(r"^(\w+)\s{2,}(:.*?)$", r"* __\1__*\2*  ", c)
        # convert REPL code blocks to code
        c = sub(r"^(>>>|\.\.\.)(.*?)$", r"```\n\1\2\n```", c)
        c = sub(r"^(>>>|\.\.\.)(.*?)\n```\n```\n(>>>|\.\.\.)", r"\1\2\n\3", c)
        c = sub(r"^(>>>|\.\.\.)(.*?)\n```\n```\n(>>>|\.\.\.)", r"\1\2\n\3", c)
        c = sub(r"^(```)(\n>>>)", r"\1python\2", c)
        # hide <h2> from `nav`
        node.docstring.content = sub(r"^(.+?)\n[-]{4,}$", r"__\1__\n", c)

        return super()._process(node)
