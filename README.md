![test_render](https://user-images.githubusercontent.com/11904770/190935213-25c15ff1-8b44-483e-8ab0-8991016fda66.png)

# 3D Scatterplots for Blender

This package takes in a tab-separated file (tsv) with the following format, and automatically generates a 3D render and blender file.

TSV files should be header-less, and tab-separated with the following layout.

Cluster | cellID | X | Y | Z | cluster_color_hexvalue |
:--:|:--:|:--: | :--:|:--:|:--: | 
String, of cluster grouping | String, unique cell identifier| float of x coordinate | float of y coordinate | float of z coordinate | Hex value of fill color | 

Here's an example lines used for the render at the top of the page.

```bash
Astrocytes    TAGGTCCGACGTACTAGGGCCTCGGTCTATGGCCTA    4.24424248742567    -1.74691044949975    -6.48374510684418    #1C7D54
Astrocytes    ATTCAGAAGCATCGCGCAGCCAGACTCTATGGCCTA    3.60301401455387    -1.96493138894082    -6.47136162049336    #1C7D54
Astrocytes    TCAACGAGTTCGCGATGGTCAGAGCCCGCCGATATC    5.51775913941571    -1.87741656898663    -6.76243310557264    #1C7D54
```

## Installation
To install perform the following steps.

1. Download and install the latest blender release [here.](https://www.blender.org/download/)
2. Download this repository as a zip file.

https://user-images.githubusercontent.com/11904770/190935113-fcad07f4-8312-4bfb-a8e6-3e18f172a639.mp4

3. Open blender. On the top left go to Edit > Preferences > Add-ons > Install.. and select the zip file. Then click the checkbox to activate the module.

https://user-images.githubusercontent.com/11904770/190935130-e06b1a6b-14d6-4f6d-9156-0bf297fa0b39.mp4

4. To access the 3D Scatterplot menu, in the 3D viewport open the panel.
5. Use the file path navigator for the input file to select your TSV, or leave the field unaltered to try the test data set.
6. Set up the output directory and prefix name using the filepath selector and the text box.
7. Press the button "Generate 3D Plot" on the panel to run and wait for the data to be loaded in.

https://user-images.githubusercontent.com/11904770/190935141-ff82d086-4db8-4507-bbf2-5ad421b4bc68.mp4

8. The file will automatically save as a .blend file in your [output_dir]/[prefix_name].blend. To render just press F12, make sure you save the image once rendering is complete.


