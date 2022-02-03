from cli.helpers.data_loader import load_all_schema_objs, types
from cli.helpers.objdict_helpers import merge_objdict, replace_yesno_with_booleans
from cli.helpers.doc_list_helpers import select_first
from cli.helpers.Step import Step
from cli.version import VERSION


class DefaultMerger(Step):
    def __init__(self, docs):
        super().__init__(__name__)
        self.docs = docs

    def run(self):
        merged_docs = []

        for doc in self.docs:
            replace_yesno_with_booleans(doc)
            files_with_defaults = load_all_schema_objs(types.DEFAULT, doc.provider, doc.kind)
            self.logger.info('Merging: ' + doc.kind+' name: '+doc.name)
            merged = self.merge_parent(files_with_defaults, doc)
            merged_docs.append(merged)

        return merged_docs

    def merge_parent(self, files, doc):
        if hasattr(doc, 'based_on'):
            self.logger.info(doc.name + ' is based on: '+doc.based_on)
            parent = select_first(files, lambda x: x.name == doc.based_on)
            merged_parent = self.merge_parent(files, parent)
            merged_parent['version'] = VERSION
            merge_objdict(merged_parent, doc)
            return merged_parent
        default_config = select_first(self.docs, lambda x: x.name == 'default' and x.kind == doc.kind)
        default_doc = select_first(files, lambda x: x.name == 'default')
        if default_config is not None:
            merge_objdict(default_doc, default_config)
        default_doc['version'] = VERSION
        merge_objdict(default_doc, doc)
        return default_doc
