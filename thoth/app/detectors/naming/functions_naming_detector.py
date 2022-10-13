import re
from thoth.app.detectors.abstract_detector import AbstractDetector, DetectorClassification


class DetectFunctionNaming(AbstractDetector):
    """
    Detect function names that are not in snake case
    """

    NAME = "Function naming"
    ARGUMENT = "function_naming"
    HELP = "Detects function names that are not in snake case"
    IMPACT = DetectorClassification.INFORMATIONAL

    def _detect(self) -> None:
        snake_case_regexp = r"^([a-z0-9]*_*[a-z0-9]*)*$"

        contract_functions = self.disassembler.functions

        for function in contract_functions:
            function_name = function.name.split(".")[-1]
            is_snake_case = bool(re.match(snake_case_regexp, function_name))
            if not is_snake_case:
                self.detected = True
                self.result.append("%s function name needs to be in snake case" % function_name)
