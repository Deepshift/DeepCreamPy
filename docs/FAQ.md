# FAQ

## Where can I get your training data?
I can't say what my data sources are because too many people downloading from them could cause them to block scraping.

## Where can I get your training code?
My training code is mostly unchanged from MathiasGruber's project [Partial Convolutions for Image Inpainting using Keras](https://github.com/MathiasGruber/PConv-Keras), which is an unofficial implementation of the paper [Image Inpainting for Irregular Holes Using Partial Convolutions](https://arxiv.org/abs/1804.07723).

## Why aren't black and white images supported? Black and white images seem easier to decensor than color images.
Black and white images contain screentone patterns which are difficult for neural networks to replicate.

## Some censor bars are transparent, but DeepCreamPy ignores the partially visible art. Could you train a neural network that doesn't?
It's on my to-do list, but it's not a high priority.

## Does this work with real life porn?
It's not meant to, but you might get OK results anyways.
