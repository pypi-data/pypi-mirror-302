from abc import ABC, abstractmethod
from typing import List, Union, AbstractSet, Collection, Literal


class Tokenizer(ABC):
    """抽象基类,定义了本地分词器的接口。"""

    @abstractmethod
    def encode(
        self,
        text: str,
        allowed_special: Union[AbstractSet[str], Literal["all"]] = "all",
        disallowed_special: Union[Collection[str], str] = (),
    ) -> List[int]:
        """将输入文本字符串编码为token id列表。

        Args:
            text (str): 要编码的字符串。

        Returns:
            List[int]: token id列表。
        """
        pass

    @abstractmethod
    def decode(self, token_ids: List[int], **kwargs) -> str:
        """将token id列表解码为字符串。

        Args:
            token_ids (List[int]): 输入的token id列表。

        Returns:
            str: 解码后的字符串。
        """
        pass
