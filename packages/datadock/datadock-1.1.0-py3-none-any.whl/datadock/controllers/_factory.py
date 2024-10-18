from abc import ABC, abstractmethod
from typing import Type, Union

from datadock.controllers._base_controllers import FormBaseController
from datadock.controllers._controller_8k import Clean8KController
from datadock.controllers._controller_10k import Clean10KController


# Abstract Factory for creating Form Controllers
class FormControllerFactory(ABC):
    @abstractmethod
    def create_controller(
        self, form_type: str, amendments: bool
    ) -> "FormBaseController":
        pass


# class ConcreteFormControllerFactory(FormControllerFactory):
#     def create_controller(
#         self, form_type: str, amendments: bool
#     ) -> Type[FormBaseController]:
#         if form_type == "8-K" or amendments:
#             return Clean8KController
#         elif form_type == "10-K" or amendments:
#             return Clean10KController
#         else:
#             raise ValueError(f"Unsupported form type: {form_type}")


class ConcreteFormControllerFactory(FormControllerFactory):
    def create_controller(
        self, form_type: str, amendments: bool
    ) -> Type[FormBaseController]:
        if form_type == "8-K" or amendments:
            return Clean8KController  # Return the class itself (callable)
        elif form_type == "10-K" or amendments:
            return Clean10KController  # Return the class itself (callable)
        else:
            raise ValueError(f"Unsupported form type: {form_type}")
