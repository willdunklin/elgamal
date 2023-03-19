========
pf_sim_2
========

Port of ps-simulation-modeler to trame 2


* Free software: Apache Software License


Installing
----------
Build and install the Vue components

.. code-block:: console

    cd vue-components
    npm i
    npm run build
    cd -

Install the application

.. code-block:: console

    pip install -e .


Run the application

.. code-block:: console

    pf_sim_2

Features
--------

* TODO


File Structure
--------------
.. code-block:: console
  - pf_sim_2/
      - app/
          - engine/ # Trame logic
              - model/    # Simput model/UI definitions
              - snippets/ # logic for page code snippets
              - engine.py # Main logic handler
              - ...       # Logic components (generally specific to pages)

          - ui/ # Trame UI
              - ui.py # Main UI handler
              - ...   # UI components (pages)

          - main.py # Entry point

      - module/  # Serve the compiled Vue components
      - widgets/ # Python wrapper around the Vue components

  - vue-components/src/components # Custom Vue components
      - FileDatabase/ # FileDatabase Vue component
          - index.vue     # Vue component
          - script.js     # JS logic
          - template.html # HTML template

      - ... # Other Vue components

  - data/ # Data files (specified by cli args)
      - database/ # FileDatabase data
      - output/   # Project Output data
      - share/    # Shared data

