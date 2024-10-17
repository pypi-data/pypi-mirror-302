# 限制参数值范围
def value_range(
    val: float,
    min: float = float("-inf"),
    max: float = float("-inf"),
):
    if val < min:
        val = min
    elif val > max:
        val = max
    return val

