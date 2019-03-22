from cli.helpers.list_helpers import select_all


class AWSInventoryCreator:
    def create(self, files):
        autoscaling_groups = select_all(files, lambda x: x.kind == 'infrastructure/virtual-machine')
        if autoscaling_groups is not None:
            for autoscaling_group in autoscaling_groups:
                print(autoscaling_group.specification['name'])
