# DeepCreamPy
*Plausibly Reconstruct Anime-style Artworks with Deep Neural Networks.*

[![GitHub release](https://img.shields.io/github/release/Deepshift/DeepCreamPy.svg)](https://github.com/Deepshift/DeepCreamPy/releases/latest)
[![GitHub downloads](https://img.shields.io/github/downloads/Deepshift/DeepCreamPy/latest/total.svg)](https://github.com/Deepshift/DeepCreamPy/releases/latest)
[![GitHub downloads](https://img.shields.io/github/downloads/Deepshift/DeepCreamPy/total.svg)](https://github.com/Deepshift/DeepCreamPy/releases)
[![GitHub issues](https://img.shields.io/github/issues/Deepshift/DeepCreamPy.svg)](https://github.com/Deepshift/DeepCreamPy/issues)

A deep learning-based tool to automatically replace parts of artworks with plausible reconstructions.

Before using DeepCreamPy, the user must mark regions in the artwork using green color with an image editing program (e.g., GIMP, Photoshop). DeepCreamPy takes the images with green colored regions as input, and a neural network automatically fills in the highlighted regions.

You can download the latest release for Windows 64-bit [here](https://github.com/Deepshift/DeepCreamPy/releases/latest).

For users interested in compiling DeepCreamPy themselves, DeepCreamPy can run on Windows, Mac, and Linux.

Before opening a new issue, please check [closed issues](https://github.com/Deepshift/DeepCreamPy/issues?q=is%3Aissue+is%3Aclosed) and refer to the [table of contents](https://github.com/Deepshift/DeepCreamPy#table-of-contents).

<p align="center">
	<img src="https://github.com/Deepshift/DeepCreamPy/blob/master/readme_images/mermaid_collage.png" width="800">
</p>

## Features
- Reconstructing images of any size
- Reconstruction of ANY shaped censor (e.g. black lines, pink hearts, etc.)
- Decensoring of mosaic censors
- Limited support for black-and-white/monochrome images
- Generate multiple variations of reconstructions from the same image

## Limitations
The reconstruction is mainly for anime-style human-like figures that have minor to moderate redactions. If an organ (e.g. arms, legs) is completely deleted, reconstruction will fail.

It does NOT work with:
- Screentones (e.g. printed material)
- Real life photos
- Animated gifs and videos

## Table of Contents
Setup:
* [Running latest Window 64-bit release](docs/INSTALLATION_BINARY.md)
* [Running code yourself](docs/INSTALLATION.md)

Usage:
* [Tutorial](docs/USAGE.md)
* [Troubleshooting for installing](docs/TROUBLESHOOTING.md)
* [Troubleshooting for poor quality outputs](docs/TROUBLESHOOTING_DECENSORS.md)

Miscellaneous:
* [FAQ](docs/FAQ.md)

## To do
- Moving to PyTorch or newer versions of TensorFlow
- Improving UI
- Error logging

## Contributions
We welcome contributions as long as they comply with the [GNU Affero General Public License v3.0](LICENSE.md). Be advised of GitHub's [inbound=outbound](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service#6-contributions-under-repository-license) rule.

Previously, contributors had to sign a [Contributor License Agreement](https://github.com/deeppomf/contributing/blob/master/sign-cla.md#sign-the-cla) (the "CLA"). This requirement is currently no longer in place.

This project was initially created by **deeppomf** and all credit goes to them. Special thanks to ccppoo, IAmTheRedSpy, 0xb8, deniszh, Smethan, harjitmoe, itsVale, StartleStars, SoftArmpit and everyone else for their contributions!

## License
Source code and official releases/binaries are distributed under the [GNU Affero General Public License v3.0](LICENSE.md).

## Acknowledgements
Example mermaid image by Shurajo & AVALANCHE Game Studio under [CC BY 3.0 License](https://creativecommons.org/licenses/by/3.0/). The example image is modified from the original, which can be found [here](https://opengameart.org/content/mermaid).

Neural network code is modified from Forty-lock's project [PEPSI](https://github.com/Forty-lock/PEPSI), which is the official implementation of the paper [PEPSI : Fast Image Inpainting With Parallel Decoding Network](http://openaccess.thecvf.com/content_CVPR_2019/html/Sagong_PEPSI__Fast_Image_Inpainting_With_Parallel_Decoding_Network_CVPR_2019_paper.html). [PEPSI](https://github.com/Forty-lock/PEPSI) is licensed under the MIT license.

Training data is modified from gwern's project [Danbooru2017: A Large-Scale Crowdsourced and Tagged Anime Illustration Dataset](https://www.gwern.net/Danbooru2017) and other sources.

See [ACKNOWLEDGEMENTS.md](docs/ACKNOWLEDGEMENTS.md) for full license text of these projects.
