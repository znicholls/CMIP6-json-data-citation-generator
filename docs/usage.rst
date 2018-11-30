.. _usage-reference:

Usage
-----

Generating json files
=====================

Having cloned this repository, an example, marked up, yaml file is given in ``tests/test_data/valid_input.yaml``. Assuming that your working directory is the root of this repository, json files can then be generated as shown below. Running this command will produce output in the path ``./example-outputs`` along with output like the block below (note: any warning about Iris not being installed can be safely ignored).
Each example json file is based off the template file ``tests/test_data/valid_input.yaml`` but fills in the missing text with information taken from the filepath of each data file.

.. code-block:: console

    # check current working directory
    $ pwd
    .../CMIP6-json-data-citation-generator
    $ generate-cmip6-citation-files tests/test_data/input4MIPs_like tests/test_data/valid_input.yaml ./example-outputs --drs CMIP6input4MIPs --regexp ".*\.nc" --keep
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

Further help can be accessed with

.. code-block:: console

    $ generate-cmip6-citation-files -h

Uploading json files
====================

json files can be upload to the CMIP6 data citation server using the command line.

To make this run, two vital steps must be taken:

#. Produce valid json files to upload (see `Generating json files`_)
#. Meet the preconditions specified in Section 2.1 of the `CMIP6 Citation Userguide <https://cera-www.dkrz.de/docs/pdf/CMIP6_Citation_Userguide.pdf>`_

When installed, the upload client can be run with

.. code-block:: console

    $ upload-cmip6-citation-files input

where ``input`` is either a single file or a folder of files to upload. Further help can be accessed with

.. code-block:: console

    $ upload-cmip6-citation-files -h
