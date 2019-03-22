import os
import yaml


def generate_terraform_file(infrastructure, template_generator, template_generator_config, terraform_build_directory):
    for idx, document in enumerate(infrastructure):
        yaml_document = yaml.load(str(document))

        if yaml_document["kind"] != "epiphany-cluster":
            content = template_generator.generate_terraform_file_content(document=yaml_document,
                                                                         templates_paths=
                                                                         template_generator_config.
                                                                         templates_paths)

            terraform_output_file_path = os.path.join(terraform_build_directory, "{:03d}".format(idx) + "_" +
                                                      yaml_document["specification"]["name"] + ".tf")

            with open(terraform_output_file_path, 'w') as terraform_output_file:
                terraform_output_file.write(content)


def create_terraform_output_dir(terraform_build_directory):
    if not os.path.exists(terraform_build_directory):
        os.makedirs(terraform_build_directory)
