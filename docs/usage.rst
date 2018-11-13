.. _usage-reference:

Usage
-----

Having cloned this repository, an example, marked up, yaml file is given in ``tests/test_data/valid_input.yaml``.

An example of of how to use the generator is given in ``scripts/example-generation.py``.
Running this script will produce output in the path ``./example-outputs`` along with output like the block below (note: any warning about Iris not being installed can be safely ignored).
Each example json file is based off the template file ``tests/test_data/valid_input.yaml`` but fills in the missing text with information taken from the filepath of each data file.

.. code-block:: console

    ./example-outputs does not exist, making it now

    Writing citation file for input4MIPs.CMIP6.AerChemMIP.UoM.UoM-AIM-ssp370-lowNTCF-1-2-0 to ./example-outputs/input4MIPs.CMIP6.AerChemMIP.UoM.UoM-AIM-ssp370-lowNTCF-1-2-0.json
    Writing citation file for input4MIPs.CMIP6.CMIP.UoM.UoM-CMIP-1-2-0 to ./example-outputs/input4MIPs.CMIP6.CMIP.UoM.UoM-CMIP-1-2-0.json
    Writing citation file for input4MIPs.CMIP6.ScenarioMIP.UoM.UoM-AIM-ssp370-1-2-0 to ./example-outputs/input4MIPs.CMIP6.ScenarioMIP.UoM.UoM-AIM-ssp370-1-2-0.json
    Writing citation file for input4MIPs.CMIP6.ScenarioMIP.UoM.UoM-GCAM4-ssp434-1-2-0 to ./example-outputs/input4MIPs.CMIP6.ScenarioMIP.UoM.UoM-GCAM4-ssp434-1-2-0.json
    Writing citation file for input4MIPs.CMIP6.ScenarioMIP.UoM.UoM-GCAM4-ssp460-1-2-0 to ./example-outputs/input4MIPs.CMIP6.ScenarioMIP.UoM.UoM-GCAM4-ssp460-1-2-0.json
    Writing citation file for input4MIPs.CMIP6.ScenarioMIP.UoM.UoM-IMAGE-ssp119-1-2-0 to ./example-outputs/input4MIPs.CMIP6.ScenarioMIP.UoM.UoM-IMAGE-ssp119-1-2-0.json
    Writing citation file for input4MIPs.CMIP6.ScenarioMIP.UoM.UoM-IMAGE-ssp126-1-2-0 to ./example-outputs/input4MIPs.CMIP6.ScenarioMIP.UoM.UoM-IMAGE-ssp126-1-2-0.json
    Writing citation file for input4MIPs.CMIP6.ScenarioMIP.UoM.UoM-MESSAGE-GLOBIOM-ssp245-1-2-0 to ./example-outputs/input4MIPs.CMIP6.ScenarioMIP.UoM.UoM-MESSAGE-GLOBIOM-ssp245-1-2-0.json
    Writing citation file for input4MIPs.CMIP6.ScenarioMIP.UoM.UoM-REMIND-MAGPIE-ssp534-over-1-2-0 to ./example-outputs/input4MIPs.CMIP6.ScenarioMIP.UoM.UoM-REMIND-MAGPIE-ssp534-over-1-2-0.json
    Writing citation file for input4MIPs.CMIP6.ScenarioMIP.UoM.UoM-REMIND-MAGPIE-ssp585-1-2-0 to ./example-outputs/input4MIPs.CMIP6.ScenarioMIP.UoM.UoM-REMIND-MAGPIE-ssp585-1-2-0.json



