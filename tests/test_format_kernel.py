from format_kaggle_kernel import format_kernel


def test_format_kernel():
    format_kernel("harupy/format-kaggle-kernel")


def test_format_kernel_with_black_options():
    format_kernel("harupy/format-kaggle-kernel", ["--line-length", "100"])
