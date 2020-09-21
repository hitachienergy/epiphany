resource "aws_resourcegroups_group" "eks_resource_group" {
  name = "resource-group-${random_string.random.result}"

  resource_query {
    query = <<JSON
{
  "ResourceTypeFilters": [
    "AWS::EC2::Instance"
  ],
  "TagFilters": [
    {
      "Key": "Environment",
      "Values": ["${var.environment}"]
    }
  ]
}
JSON
  }
}