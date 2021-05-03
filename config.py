""" Arguments and variables for creating histograms of images.
"h" represents hue, "s" represents saturation
"""
h_bins = 50
s_bins = 60
histSize = [h_bins, s_bins]
h_ranges = [0, 180]
s_ranges = [0, 256]
ranges = h_ranges + s_ranges  
channels = [0, 1]  
blur_threshold = 6.0