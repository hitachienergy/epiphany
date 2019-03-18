import logging
import sys

import jinja2
from jinja2 import Template


class TemplateGenerator:

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def generate_terraform_file_content(self, document, templates_paths):
        self.logger.info("Running template generator.")

        template_path = self.get_template_path(document, templates_paths)

        rendered_template = self.render_template(document, template_path)
        self.logger.info("Finished running template generator.")

        return rendered_template

    def get_template_path(self, document, templates_paths):

        self.logger.info("Getting template path.")
        template_path = templates_paths[document["provider"]][document["kind"]]
        self.logger.info("Template path: " + template_path)

        return template_path

    def render_template(self, document, template_path):
        self.logger.info("Start to render template.")

        try:

            with open(template_path) as template_file:
                self.logger.info("Reading template.")
                template = Template(template_file.read(), undefined=jinja2.StrictUndefined)

                self.logger.info("Rendering template.")
                output = template.render(document)

            return output

        except Exception as e:
            self.logger.error("TemplateGenerator has failed to render template file from " + template_path + "===> ", e)
            sys.exit(1)
