from format_kaggle_kernel import format_kernel


# https://www.kaggle.com/harupy/format-kaggle-kernel
TEST_KERNEL = "harupy/format-kaggle-kernel"


def test_format_kernel():
    format_kernel(TEST_KERNEL)


def test_format_kernel_with_black_options():
    format_kernel(TEST_KERNEL, ["--line-length", "100"])
