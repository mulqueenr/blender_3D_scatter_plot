# blender_3D_scatter_plot

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

Blender Module for 3D scatter plots.

