import numpy as np
import flowutils


class LogicleTransform():
    def __init__(
        self, top_of_scale, m_positive_decades, width_of_linear, addition_negative
    ):
        self.top_of_scale = top_of_scale
        self.m_positive_decades = m_positive_decades
        self.width_of_linear = width_of_linear
        self.addition_negative = addition_negative

    def __call__(self, data):
        return flowutils.transforms.logicle(
            data, None,
            t=self.top_of_scale, m=self.m_positive_decades,
            w=self.width_of_linear, a=self.addition_negative
        )

    def inverse(self, data):
        return flowutils.transforms.logicle_inverse(
            data, None,
            t=self.top_of_scale, m=self.m_positive_decades,
            w=self.width_of_linear, a=self.addition_negative
        )

    def get_params(self):
        return (
            self.top_of_scale, self.m_positive_decades,
            self.width_of_linear, self.addition_negative
        )

    def __repr__(self) -> str:
        return (
            f"LogicleTransform <"
            f"t={self.top_of_scale:.5f}, m={self.m_positive_decades:.5f}, "
            f"w={self.width_of_linear:.5f}, a={self.addition_negative:.2f}>"
        )


def logicle_transform(data, return_transform=False):
    if data.max() > 1:
        top_decade = np.round(np.log10(data.max()), 1) + 0.1
    else:
        top_decade = 0.1
    top_of_scale = 10 ** top_decade
    assert top_of_scale > 1

    m_positive_decades = top_decade - 0.2 if top_decade > 1 else top_decade - 0.01
    assert m_positive_decades > 0

    addition_negative = 0.05
    r = np.quantile(data, 0.05)
    if abs(r) > 1:
        width_of_linear = (m_positive_decades - np.log10(top_of_scale / abs(r))) / 2
        width_of_linear = max(0.05, width_of_linear)
        addition_negative = 0.25
    else:
        width_of_linear = 0.05
    assert width_of_linear > 0, f"{top_of_scale}, {m_positive_decades}, r={r}"

    # transform
    logicle = LogicleTransform(
        top_of_scale, m_positive_decades,
        width_of_linear, addition_negative
    )

    if return_transform:
        return logicle(data), logicle

    return logicle(data)
