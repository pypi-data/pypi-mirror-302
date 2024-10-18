from typing import Any, Dict, List, Union, Optional

from scale_gp import BaseModel


class TranslationTestCaseSchema(BaseModel):
    origin_text: List[str]
    language: Optional[str] = None
    expected_translation: Optional[str] = None
    other_inputs: Optional[Union[str, float, Dict[str, Any]]] = None
    other_expected: Optional[Union[str, float, Dict[str, Any]]] = None
