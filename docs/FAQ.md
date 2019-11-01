# FAQ

## Where can I get your training data?
I can't say what my data sources are because too many people downloading from them could cause them to block scraping.
[Danbooru2018](https://www.gwern.net/Danbooru2018) is a good starting point.

## Where can I get your training code?
My training code is is modified from Forty-lock's project [PEPSI](https://github.com/Forty-lock/PEPSI), which is the official implementation of the paper [PEPSI : Fast Image Inpainting With Parallel Decoding Network](http://openaccess.thecvf.com/content_CVPR_2019/html/Sagong_PEPSI__Fast_Image_Inpainting_With_Parallel_Decoding_Network_CVPR_2019_paper.html). [PEPSI](https://github.com/Forty-lock/PEPSI) is licensed under the MIT license.

## Why aren't black and white images supported? Black and white images seem easier to decensor than color images.
Black and white images contain screentone patterns which are difficult for neural networks to replicate.

## Some censor bars are transparent, but DeepCreamPy ignores the partially visible art. Could you train a neural network that doesn't?
It's on my to-do list, but it's not a high priority.

## Does this work with real life porn?
DeepCreamPy is not trained on real life porn, so it will not work with real life porn.
