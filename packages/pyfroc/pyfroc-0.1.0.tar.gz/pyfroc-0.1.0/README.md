# pyfroc

Python framework for FROC analysis

## About

### What pyfroc does

- Improve FROC analysis procedure.
- Manage responses of raters.
- The responses can be made using segmentation function of [3D Slicer](https://www.slicer.org/).
- Evaluate responses and devide them into true positive or false positive automatically.
- Build a xlsx file for the [RJafroc](https://github.com/dpc10ster/RJafroc), a R library which runs statistical tests of AFROC (alternative Free-response receiver operating characteristic) analysis.
- Write images of responses with paired lesions (if exists).

### What pyfroc doesn't

- Statistical analysis of JAFROC. This is out of scope of pyfroc. Use [RJafroc](https://github.com/dpc10ster/RJafroc) for statistical analysis.
- FROC analysis including multi-modality references because pyfroc doesn't implement an algorithm to match intermodality lesions.

## Table of contents

## Use case

pyfroc is designed for specific scenarios of FROC analysis. pyfroc supports only one modality for reference lesions.

### Example scenario #1

- Compare diagnostic performance between radiologists and AI.
- Using a specific series to record responses.

### Example scenario #2

- Compare a standard MRI protocol with an abbreviated protocol.
- Using same series to record responses.

### Example scenario #3

- Compare images reconstructed using an advanced method with images reconstructed using conventional method.
- Using either series to record responses.

## Instalation

```bash
pip install pyfroc
```

## Tutorial

Use pyfroc with 3D Slicer


## License

GPLv3







