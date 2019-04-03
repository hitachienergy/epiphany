import os
import yaml


def generate_terraform_file(infrastructure, template_generator, template_generator_config, terraform_build_directory):
    for idx, document in enumerate(infrastructure):
        yaml_document = yaml.load(str(document), Loader=yaml.FullLoader)

        content = template_generator.generate_terraform_file_content(document=yaml_document,
                                                                     templates_paths=
                                                                     template_generator_config.
                                                                     templates_paths)

        if yaml_document["kind"] != "epiphany-cluster":
            terraform_file_name = "{:03d}".format(idx + 1) + "_" + yaml_document["specification"]["name"] + ".tf"
        else:
            terraform_file_name = "000_" + yaml_document["specification"]["name"] + ".tf"

        terraform_output_file_path = os.path.join(terraform_build_directory, terraform_file_name)

        with open(terraform_output_file_path, 'w') as terraform_output_file:
            terraform_output_file.write(content)


def create_terraform_output_dir(terraform_build_directory):
    if not os.path.exists(terraform_build_directory):
        os.makedirs(terraform_build_directory)
