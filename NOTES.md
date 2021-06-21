# Image Formats

`matplotlib` supports certain image formats.  I tried each one and report the results here: 
* `eps`: very nice; text can be highlighted ✔️  
* `jpeg`: just an image; text is blurry & cannot be highlighted❌  
* `jpg`: just an image; text is blurry & cannot be highlighted❌  
* `pdf`: text can be highlighted; however, the marks look distorted when zoomed out❌  
* `pgf`: returned non-zero exit status 43❌  
* `png`: just an image; text is blurry & cannot be highlighted❌  
* `ps`: it ran, the but the chart position is botched in the pdf file❌  
* `raw`: hit an infinite loop❌  
* `rgba`: hit an infinite loop❌  
* `svg`: got an exception `could not convert image`❌  
* `svgz`: got an exception `could not convert image`❌  
* `tif`: just an image; text is blurry & cannot be highlighted❌  
* `tiff`: just an image; text is blurry & cannot be highlighted❌  
