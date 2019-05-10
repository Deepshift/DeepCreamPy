# DeepCreamPy
*Decensoring Hentai with Deep Neural Networks.*

*DeepCreamPyV2 coming in Summer 2019*

[![GitHub release](https://img.shields.io/github/release/deeppomf/DeepCreamPy.svg)](https://github.com/deeppomf/DeepCreamPy/releases/latest)
[![GitHub downloads](https://img.shields.io/github/downloads/deeppomf/DeepCreamPy/latest/total.svg)](https://github.com/deeppomf/DeepCreamPy/releases/latest)
[![GitHub downloads](https://img.shields.io/github/downloads/deeppomf/DeepCreamPy/total.svg)](https://github.com/deeppomf/DeepCreamPy/releases)
[![GitHub issues](https://img.shields.io/github/issues/deeppomf/DeepCreamPy.svg)](https://github.com/deeppomf/DeepCreamPy/issues)
[![Donate with PayPal](https://img.shields.io/badge/paypal-donate-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=SAM6C6DQRDBAE)
[![Project license](https://img.shields.io/github/license/deeppomf/DeepCreamPy.svg)](https://raw.githubusercontent.com/deeppomf/DeepCreamPy/master/LICENSE.txt)
[![Twitter Follow](https://img.shields.io/twitter/follow/deeppomf.svg?label=Follow&style=social)](https://twitter.com/deeppomf/)

A deep learning-based tool to automatically replace censored artwork in hentai with plausible reconstructions.

The user colors censored regions green in an image editing program like GIMP or Photoshop. A neural network fills in the censored regions.

DeepCreamPy has a pre-built binary for Windows 64-bit available [here](https://github.com/deeppomf/DeepCreamPy/releases/latest). DeepCreamPy's code works on Windows, Mac, and Linux.

Please before you open a new issue check [closed issues](https://github.com/deeppomf/DeepCreamPy/issues?q=is%3Aissue+is%3Aclosed) and check the [table of contents](https://github.com/deeppomf/DeepCreamPy#table-of-contents).

<p align="center">
	<img src="https://github.com/deeppomf/DeepCreamPy/blob/master/readme_images/mermaid_collage.png" width="800">
</p>

## Features
- Decensoring images of ANY size
- Decensoring of ANY shaped censor (e.g. black lines, pink hearts, etc.)
- Higher quality decensors
- Support for mosaic decensors (WIP)

## Limitations
The decensorship is for color hentai images that have minor to moderate censorship of the penis or vagina. If a vagina or penis is completely censored out, decensoring will be ineffective.

It does NOT work with:
- Black and white/Monochrome image
- Hentai with screentones (e.g. printed hentai)
- Real life porn
- Censorship of nipples
- Censorship of anus
- Animated gifs/videos

## Table of Contents
Setup:
* [Running latest Window 64-bit release](docs/INSTALLATION_BINARY.md)
* [Running code yourself](docs/INSTALLATION.md)

Usage:
* [Decensoring tutorial](docs/USAGE.md)
* [Troubleshooting for installing](docs/TROUBLESHOOTING.md)
* [Troubleshooting for poor quality decensors](docs/TROUBLESHOOTING_DECENSORS.md)

Miscellaneous:
* [FAQ](docs/FAQ.md)

## To do
- Switch to Deepfillv2 model
- Enhance data collection and extraction
- Use new training techniques
- Resolve all Tensorflow compatibility problems
- Finish the user interface
- Add support for black and white images
- Add error log

Follow me on Twitter [@deeppomf](https://twitter.com/deeppomf) (NSFW Tweets) for project updates.

Contributions are welcome! Special thanks to ccppoo, IAmTheRedSpy, 0xb8, deniszh, Smethan, mrmajik45, harjitmoe, itsVale, StartleStars, and SoftArmpit!

## License
This project is licensed under GNU Affero General Public License v3.0.

See [LICENSE.txt](LICENSE.txt) for more information about the license.

## Acknowledgements
Example mermaid image by Shurajo & AVALANCHE Game Studio under [CC BY 3.0 License](https://creativecommons.org/licenses/by/3.0/). The example image is modified from the original, which can be found [here](https://opengameart.org/content/mermaid).

Neural network code is modified from MathiasGruber's project [Partial Convolutions for Image Inpainting using Keras](https://github.com/MathiasGruber/PConv-Keras), which is an unofficial implementation of the paper [Image Inpainting for Irregular Holes Using Partial Convolutions](https://arxiv.org/abs/1804.07723). [Partial Convolutions for Image Inpainting using Keras](https://github.com/MathiasGruber/PConv-Keras) is licensed under the MIT license.

User interface code is modified from Packt's project [Tkinter GUI Application Development Blueprints - Second Edition](https://github.com/PacktPublishing/Tkinter-GUI-Application-Development-Blueprints-Second-Edition). [Tkinter GUI Application Development Blueprints - Second Edition](https://github.com/PacktPublishing/Tkinter-GUI-Application-Development-Blueprints-Second-Edition) is licensed under the MIT license.

Data is modified from gwern's project [Danbooru2017: A Large-Scale Crowdsourced and Tagged Anime Illustration Dataset](https://www.gwern.net/Danbooru2017) and other sources.

See [ACKNOWLEDGEMENTS.md](docs/ACKNOWLEDGEMENTS.md) for full license text of these projects.

## Donations
If you like the work I do, you can donate to me via Paypal. The funds will mainly go towards purchasing better GPUs to accelerate training. [![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=SAM6C6DQRDBAE)
