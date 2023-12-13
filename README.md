# green-benchmark

## Sources

- List any sources...
- WattHours Per Kilometer for Electric Vehicles: https://ev-database.org/cheatsheet/energy-consumption-electric-car
- Estimated battery-electric vehicle sales in the United States in 2022, by brand: https://www.statista.com/statistics/698414/sales-of-all-electric-vehicles-in-the-us-by-brand/
- We also need to address for hybrid vehicles -- the EV dataset does not contain information about hybrids
  - https://www.kaggle.com/datasets/iottech/electric-vehicle-data-1997-2024-update-version
  - https://www.kaggle.com/datasets/utkarshx27/electric-vehicle-population-data
  - https://datadryad.org/stash/dataset/doi:10.5061/dryad.2bvq83bnj
  - https://datadryad.org/stash/dataset/doi:10.5061/dryad.2bvq83bnj
  - Great source: End to End ML for cars: https://www.kaggle.com/datasets/vivovinco/monitoring-of-co2-emissions-from-passenger-cars
  - US government publishes an EIO-LCA database which provides the kgCO2𝑒 per dollar estimate for aggregated NAICS codes:
        Wesley W Ingwersen, Mo Li, Ben Young, Jorge Vendries, and Catherine Birney.
        2022. USEEIO v2. 0, The US Environmentally-Extended Input-Output Model v2.
        0. Scientific Data 9, 1 (2022), 1–24.
  - https://www.energy.gov/eere/vehicles/articles/fotw-1223-january-31-2022-average-carbon-dioxide-emissions-2021-model-year - Data on emissions based on model year.
  - Lithium Ion batteries https://www.energimyndigheten.se/globalassets/forskning--innovation/transporter/c243-the-life-cycle-energy-consumption-and-co2-emissions-from-lithium-ion-batteries-.pdf numbers
      - Other estimates https://www.sciencedirect.com/science/article/pii/S0959652621039731
  - https://pdf.sciencedirectassets.com/271737/1-s2.0-S1361920917X00060/1-s2.0-S1361920916301742/am.pdf?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEEEaCXVzLWVhc3QtMSJIMEYCIQDOnjsYbXpgrhIwKPyekv5eFfYL1pJ1grMirSoN2NnF9AIhAKP0TBDAVvT4f2Npy%2B2uuPtSdh3S1KoPlUgr7T4vBas1KrwFCKr%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQBRoMMDU5MDAzNTQ2ODY1IgyIaDCZg%2FwEx36H%2F0YqkAWf3FETvcSxr4YVl3%2BWLywf%2B5Qbdx4XRNnpS%2F2U0mydJ1JR3%2FlQ%2B7%2BmWVaPjD4OSvdcTRGgz1sKGmDORmlCZ206PZeS%2FkUfFfj9Iqnpe%2BDzAd0iQj21dx%2BT%2F9QN70BZoqS9KSwHC37UwC50PE2upuUZIDh4%2BfnEHlD7hF4pW5%2Frv8RO55C6Nmd5YzcA5G8%2BuW8cwEZ3aG76fRnv4mH6GFm3RWzdPA2lM5zKAyDq60dkWosGAWcyfMUzebtS38gpfaeMlunEINskfKOedrBxOwWu65gKsjd%2BONJG2q8vBLTRfCQu53kW1lOTeQiVm%2Buwl1PcuXEpnWxGah1%2Fs%2FFRSq9kdsJQrYrsxJADw6D4%2B%2BLv03z3L6%2Bf8r%2FIx3jcH3Lfg%2BG374ouJ5zpDa37M%2F6jWm9pRaO1PSn926%2B13VCyo6rat2b8RbeZCtJ1uOVXf9DWicgbGeop5%2BI7pXWKSiN00r6FmF4gp4p2%2FhIQfs7lpfh%2Bo0%2FWDTglwgCP8Tg1gBkqBiYvbpH1Yqwiwr90e1C%2BfwtTLtmrIjEzKUqVkmkmMNyzJH0X%2BynKMT%2BSfZcNwd5gFXQuU3FsdgEP8PIomCuXi3xnbmVuEWj%2FU90Ktuj0Q00%2F7zk8MgpBMn5%2FF5F0gKLTI0h1D%2FBaFFUELdKWd%2FrrpJxLRgUEtt3PuGnUj9sZfcgAic%2FHKkXBE9WxBetW%2BM14R1S34A6D6tdumkX0CIwoDlgYnFVCYR9lMOUAM%2FbgFVHkEGpcOX4JIfURAaRl26XSX29yjt6g2Je3wmUuRUqN4BSyTDJCscHiUk%2BV05QYg1buGkF4cZydXkRmtzG%2BjudLhudBgq%2BPGCjFHgPKpZe2YM%2B8hrKU4nV8FrtV8u3bi8LEnzCR8cerBjqwAS1%2BS55cf9FMv6oIltbd%2B9dEOd3mNMgQBzjxXetipO33nUr8znlhI7sGpkmXa7VHLkVglE449ZCjgvbiNLXeN6WNFzWezN45tNhUgnd2eWB8YGOrnxM0LmSXWn9XAk0aEPMn483m1LqzPGXUoyHL4V3ECV3oRivsPmTJ%2BciTOfwa7aC4bUohgBxT0RXET9dYtCiIBnAlwHI0F%2F7K6OMTctg3af0Grdr5wlfFb9%2Fgliob&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20231207T183324Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAQ3PHCVTYUTPMRIOG%2F20231207%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=4b8cebd07d263bcd4fe61d1f473663dc5ba4f4efa8257c13cf02feb33b1d1f81&hash=cd9a47cb60e0ad593594e3494eca8baa80e0c819b1c22c53c8d1d7739ff2666b&host=68042c943591013ac2b2430a89b270f6af2c76d8dfd086a07176afe7c76c2c61&pii=S1361920916301742&tid=pdf-0f0f261a-14dd-45cd-bc8e-54e561c0d81d&sid=571131c271e24348c35952e589bbaed00016gxrqa&type=client : Degradation information! (Sorry the Link is Long)

  
  
