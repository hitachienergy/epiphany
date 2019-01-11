# Azure Data

This folder contains all of the different clusters that need to be generated. This root folder contains all templates `*.tf.j2` in Jinja2 template format.

Each sub-folder represents the classification of the cluster:

```text
infrastructure
  \chef
  \epiphany
  \<whatever>
```

Within the given sub-folder you place the `data.yaml` file that is used to hold all of the data required for the given cluster. It contains data, options, etc. You can use a helper script called `gen_helper.sh` in the root of this folder. It calls the `gen_terraform_template.sh` script in the `/bin` folder. It's a helper script that makes it a little easier to use.

```text
infrastructure
  \chef
    data.yaml
  \epiphany
    data.yaml
  \<whatever>
```

## Call EPIPHANY_UP

This script is a helper script that calls helper scripts based on values passed.

```text
# Assumes EPIPHANY_UP is in your path but it is most likely in the REPO_ROOT/bin

infrastructure
  \epiphany
    ./EPIPHANY_UP $(pwd) ${PWD##*/}
```

The above command line only show 2 parameters because the third one is optional. The third parameter is the name of the data file which defaults to `data.yaml`. However, you can override the default for more flexibility. The data and output *.tf *must* reside in the same folder.

Also, `$pwd` means to pass in the current folder path; `${PWD##*/}` means to pass only the name of the current folder; `empty` but could contain the name of the data file.
