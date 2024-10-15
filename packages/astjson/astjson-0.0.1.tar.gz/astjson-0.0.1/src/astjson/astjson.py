
from typing import Any, Dict, Optional, Union

import ast

TYPE_TAG = '_type'

NodeValue = Union[int, float, bool, str, complex, bytearray, bytes]
ReturnValue = Union[NodeValue, Dict[str, str]]


def get_json_value(node: NodeValue) -> ReturnValue:
    if isinstance(node, (int, float, bool, str,)):
        return node
    if isinstance(node, (complex, bytearray, bytes)):
        return {TYPE_TAG: node.__class__.__name__, 'value': repr(node)}


def ast_to_json(node: ast.AST) -> dict[str, Any]:
    result = _ast_to_json(node)
    if not isinstance(result, dict):
        raise ValueError(f"Failed to convert {node}")
    return result


def _ast_to_json(node:  Any) -> Any:
    if isinstance(node, ast.AST):
        fields: Dict[str, Any] = {
            field: _ast_to_json(getattr(node, field))
            for field in node._fields
        }
        return {
            TYPE_TAG: node.__class__.__name__,
            **fields
        }
    if node is None:
        return None
    if isinstance(node, (int, float, bool, str, complex, bytearray, bytes)):
        return get_json_value(node)
    if isinstance(node, list):
        return [_ast_to_json(item) for item in node]
    if isinstance(node, tuple):
        return tuple(_ast_to_json(item) for item in node)
    if isinstance(node, type(Ellipsis)):
        return {TYPE_TAG: 'Ellipsis', 'value': 'Ellipsis'}
    raise ValueError(f"Unsupported node {type(node)}: {node}")
