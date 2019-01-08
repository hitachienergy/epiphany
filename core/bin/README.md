# Bin Folder

This folder holds all of the binaries and scripts that are maintained outside of Epiphany but used by Epiphany. This folder does *NOT* hold output from the /build folder. The /build folder is used for holding the output of any generated code or rendered output from the build process. 

## template_engine

The `template_engine` is a Python app that takes 3 parameters:

- Input template
- Output file
- Data file

```bash
./template_engine \
    -i /data/terraform/pipeline/main.tf.j2 \
    -o /build/terraform/pipeline/main.tf \
    -d /data/terraform/pipeline/pipeline.yaml
```

It uses `Jinja2` templating syntax so you can have templates embedded in templates for complex needs or just simple code/data generation. The data is in a `yaml` format. The input template should have a `.j2` file extension but it's not required.
