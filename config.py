import argparse

def str2floatarr(v):
    if type(v) == str:
        try:
            return [float(v) for v in v.split(',')]
        except:
            raise argparse.ArgumentTypeError('Integers seperated by commas expected.')
    else:
        raise argparse.ArgumentTypeError('Integers seperated by commas expected.')

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1', True):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0', False):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def get_args():
	parser = argparse.ArgumentParser(description='')

	#Input output folders settings
	parser.add_argument('--decensor_input_path', dest='decensor_input_path', default='./decensor_input/', help='input images with censored regions colored green to be decensored by decensor.py path')
	parser.add_argument('--decensor_input_original_path', dest='decensor_input_original_path', default='./decensor_input_original/', help='input images with no modifications to be decensored by decensor.py path')
	parser.add_argument('--decensor_output_path', dest='decensor_output_path', default='./decensor_output/', help='output images generated from running decensor.py path')

	#Decensor settings
	parser.add_argument('--mask_color', dest='mask_color', default=[0,255,0], type=str2floatarr, help='rgb color of the mask, comma seperated.')
	parser.add_argument('--is_mosaic', dest='is_mosaic', default='False', type=str2bool, help='true if image has mosaic censoring, false otherwise')

	args = parser.parse_args()
	return args

if __name__ == '__main__':
	get_args()