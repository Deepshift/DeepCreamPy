# DeepCreamPy
*Decensoring Hentai with Deep Neural Networks.*

## DeepCreamPy 2.0--a major upgrade over DeepCreamPy 1.3--is under construction.

## DeepCreamPy 2.0 can be used by running the code yourself.

## No binary is available for DeepCreamPy 2.0 yet. Wait for the next release.

[![GitHub release](https://img.shields.io/github/release/deeppomf/DeepCreamPy.svg)](https://github.com/deeppomf/DeepCreamPy/releases/latest)
[![GitHub downloads](https://img.shields.io/github/downloads/deeppomf/DeepCreamPy/latest/total.svg)](https://github.com/deeppomf/DeepCreamPy/releases/latest)
[![GitHub downloads](https://img.shields.io/github/downloads/deeppomf/DeepCreamPy/total.svg)](https://github.com/deeppomf/DeepCreamPy/releases)
[![GitHub issues](https://img.shields.io/github/issues/deeppomf/DeepCreamPy.svg)](https://github.com/deeppomf/DeepCreamPy/issues)
[![Donate with PayPal](https://img.shields.io/badge/paypal-donate-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=SAM6C6DQRDBAE)
[![Project license](https://img.shields.io/github/license/deeppomf/DeepCreamPy.svg)](https://raw.githubusercontent.com/deeppomf/DeepCreamPy/master/LICENSE.txt)
[![Twitter Follow](https://img.shields.io/twitter/follow/deeppomf.svg?label=Follow&style=social)](https://twitter.com/deeppomf/)

A deep learning-based tool to automatically replace censored artwork in hentai with plausible reconstructions.

Before DeepCreamPy can be used, the user must color censored regions in their hentai green in an image editing program like GIMP or Photoshop. DeepCreamPy takes the green colored images as input, and a neural network autommatically fills in the censored regions.

DeepCreamPy has a pre-built binary for Windows 64-bit available [here](https://github.com/deeppomf/DeepCreamPy/releases/latest). DeepCreamPy's code works on Windows, Mac, and Linux.

Please before you open a new issue check [closed issues](https://github.com/deeppomf/DeepCreamPy/issues?q=is%3Aissue+is%3Aclosed) and check the [table of contents](https://github.com/deeppomf/DeepCreamPy#table-of-contents).

<p align="center">
	<img src="https://github.com/deeppomf/DeepCreamPy/blob/master/readme_images/mermaid_collage.png" width="800">
</p>

## Features
- Decensoring images of ANY size
- Decensoring of ANY shaped censor (e.g. black lines, pink hearts, etc.)
- Decensoring of mosaic decensors

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
* [UNDER CONSTRUCTION: Running latest Window 64-bit release](docs/INSTALLATION_BINARY.md)
* [Running code yourself](docs/INSTALLATION.md)

Usage:
* [Decensoring tutorial](docs/USAGE.md)
* [Troubleshooting for installing](docs/TROUBLESHOOTING.md)
* [Troubleshooting for poor quality decensors](docs/TROUBLESHOOTING_DECENSORS.md)

Miscellaneous:
* [FAQ](docs/FAQ.md)

## To do
- Resolve all Tensorflow compatibility problems
- Finish the user interface
- Add error log

Follow me on Twitter [@deeppomf](https://twitter.com/deeppomf) (NSFW Tweets) for project updates.

## Contributions
Contributions are closed for the near future.

Special thanks to ccppoo, IAmTheRedSpy, 0xb8, deniszh, Smethan, mrmajik45, harjitmoe, itsVale, StartleStars, and SoftArmpit for their contributions!

## License
Please see the [EULA](EULA.txt) for license details.

## Acknowledgements
Example mermaid image by Shurajo & AVALANCHE Game Studio under [CC BY 3.0 License](https://creativecommons.org/licenses/by/3.0/). The example image is modified from the original, which can be found [here](https://opengameart.org/content/mermaid).

Neural network code is modified from Forty-lock's project [PEPSI](https://github.com/Forty-lock/PEPSI), which is the official implementation of the paper [PEPSI : Fast Image Inpainting With Parallel Decoding Network](http://openaccess.thecvf.com/content_CVPR_2019/html/Sagong_PEPSI__Fast_Image_Inpainting_With_Parallel_Decoding_Network_CVPR_2019_paper.html). [PEPSI](https://github.com/Forty-lock/PEPSI) is licensed under the MIT license.

Training data is modified from gwern's project [Danbooru2017: A Large-Scale Crowdsourced and Tagged Anime Illustration Dataset](https://www.gwern.net/Danbooru2017) and other sources.

See [ACKNOWLEDGEMENTS.md](docs/ACKNOWLEDGEMENTS.md) for full license text of these projects.

## Donations
If you like the work I do, you can donate to me via Paypal. The funds will go towards keeping me alive. [![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=SAM6C6DQRDBAE)
