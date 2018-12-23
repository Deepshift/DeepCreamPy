# Troubleshooting Install

## Running Binary

Remember the binary is only for 64-bit Windows systems.

## Running Code

### I'm running a Linux OS, and I get the error message "Using TensorFlow backend. Illegal instruction" when running decensor.py

Unfortunately, you can't run DCP on your machine because your CPU doesn't support AVX instructions. Newer versions of tensorflow can't run on these CPUs. This problem doesn't exist for Windows with non-AVX CPUs because there are custom Windows Tensorflow wheels, you can find it [here](https://github.com/fo40225/tensorflow-windows-wheel/tree/master/1.10.0/py36/CPU/sse2).

Upgrading your CPU to a newer CPU will probably fix this issue.

See issue #74 for a discussion.
