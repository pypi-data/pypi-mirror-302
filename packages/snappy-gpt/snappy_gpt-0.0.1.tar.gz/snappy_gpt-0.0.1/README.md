# SnappyGPT

Python Module that creates and applies graph processing functions for ESAs SNAP graph processing tool (GPT)

## Requirements

* SNAP must be installed and snappy configured for your python enviroment
* numpy is requiered for utils.py

## Example

```python
from SnappyGPT import utils, GPT

product=utils.read('filename.zip')

preProcessGraph = GPT.Graph()
preProcessGraph.add_calibration(outputImageScaleInDb=True, outputSigmaBand=True)
preProcessGraph.add_thermal_noise_removal()
preProcessGraph.add_topsar_deburst()

processedProduct=preProcessGraph.create_product(product)
```