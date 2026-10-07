# F-01/R-01: retrieval stays off by default and can be re-enabled explicitly.
import sys
import unittest
from unittest.mock import patch

from code_sentinel.agents.nodes import retrieve_context_node


class RetrievalSwitchTests(unittest.TestCase):
    def test_disabled_skips_retrieval_even_for_function_diff(self):
        state = {"diff_content": "+def changed_function(): pass", "language": "Python"}
        with patch("code_sentinel.agents.nodes.config.CODE_RETRIEVAL_ENABLED", False):
            with patch.dict(sys.modules, {"code_sentinel.core.knowledge_base": None}):
                with patch("code_sentinel.agents.nodes.retrieve_related_code") as tool:
                    self.assertEqual(retrieve_context_node(state), {"repo_context": ""})
                    tool.invoke.assert_not_called()

    def test_enabled_calls_retrieval(self):
        state = {"diff_content": "+def changed_function(): pass", "language": "Python"}
        with patch("code_sentinel.agents.nodes.config.CODE_RETRIEVAL_ENABLED", True):
            with patch(
                "code_sentinel.agents.nodes.retrieve_related_code"
            ) as tool:
                tool.invoke.return_value = "related code"
                self.assertEqual(
                    retrieve_context_node(state), {"repo_context": "related code"}
                )
                tool.invoke.assert_called_once_with(
                    {"query": "changed_function(): pass"}
                )


if __name__ == "__main__":
    unittest.main()
