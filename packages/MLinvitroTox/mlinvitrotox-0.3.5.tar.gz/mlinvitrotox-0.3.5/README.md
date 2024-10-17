# MLinvitroTox

MLinvitroTox performs high-throughput hazard-based prioritization of high-resolution mass spectrometry data.


## A. Project description

MLinvitroTox is an open-source Python package developed to provide a fully automated high-throughput pipeline for hazard-driven prioritization of toxicologically relevant signals among tens of thousands of signals commonly detected in complex environmental samples through nontarget high-resolution mass spectrometry (NTS HRMS/MS). It is a machine learning (ML) framework comprising 490 independent XGBoost classifiers trained on molecular fingerprints from chemical structures and target specific endpoints from the ToxCast/Tox21 [invitroDBv4.1 database](https://www.epa.gov/comptox-tools/exploring-toxcast-data). MLinvitroTox predicts a bioactivity fingerprint for each unidentified HRMS feature (a distinct m/z ion) based on the molecular fingerprints derived from MS2 fragmentation spectra. The 490-bit binary bioactivity fingerprints are used as the basis for prioritizing the HRMS features towards further elucidation and analytical confirmation. This approach adds toxicological relevance to environmental analysis by focusing the time-consuming molecular identification efforts on features most likely to cause adverse effects. 

The package contains 
- scripts that were used to build the models
- input data to build the models (in `data/input`) and processed data (in `data/processed`)
- modeling results and the models
- a streamlit app to view the results
- scripts for users to run the models on their data


## B. Getting started

Currently, the package is only available on PyPI and can be installed as follows. 

```
pip install mlinvitrotox
```


## C. Example / Usage

Have a look at the [tutorial](https://renkulab.io/projects/expectmine/mlinvitrotox-tutorial). 

MLinvitroTox will work with SIRIUS output up to [v5.8.6](https://github.com/bright-giant/sirius/releases/tag/v5.8.6), but not the latest release v6.0.4 (work in progress).


## D. Development

If you are interested in the project and the package, please reach out to <lilian.gasser@sdsc.ethz.ch>.


## References
- Arturi et al. (2024) "MLinvitroTox reloaded for high-throughput hazard-based prioritization of HRMS data." (In preparation).
- Arturi, Katarzyna, and Juliane Hollender. "Machine learning-based hazard-driven prioritization of features in nontarget screening of environmental high-resolution mass spectrometry data." Environmental Science & Technology 57, no. 46 (2023): 18067-18079.
- Dührkop, Kai, Markus Fleischauer, Marcus Ludwig, Alexander A. Aksenov, Alexey V. Melnik, Marvin Meusel, Pieter C. Dorrestein, Juho Rousu, and Sebastian Böcker. "SIRIUS 4: a rapid tool for turning tandem mass spectra into metabolite structure information." Nature methods 16, no. 4 (2019): 299-302.
- Abedini, Jaleh, Bethany Cook, Shannon Bell, Xiaoqing Chang, Neepa Choksi, Amber B. Daniel, David Hines et al. "Application of new approach methodologies: ICE tools to support chemical evaluations." Computational Toxicology 20 (2021): 100184.
- Richard, Ann M., Richard S. Judson, Keith A. Houck, Christopher M. Grulke, Patra Volarath, Inthirany Thillainadarajah, Chihae Yang et al. "ToxCast chemical landscape: paving the road to 21st century toxicology." Chemical research in toxicology 29, no. 8 (2016): 1225-1251.
