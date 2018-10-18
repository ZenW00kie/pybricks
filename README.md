# PyBricks

PyBricks is the Databricks SDK for Python, which allows Python developers to write software that uses the Databricks platform, including Clusters and DBFS.

- [Setup](##setup)
- [Clusters](##clusters)
- [DBFS](##dbfs)
- [Jobs](##jobs)
- [Stacks](##stacks)

This app uses the following open-source libraries:
[Databricks CLI](https://github.com/databricks/databricks-cli)
[License](https://github.com/databricks/databricks-cli/blob/master/LICENSE.txt)


## Setup

### Automatic authentication
In order to make use of the automatic authentication you currently need a .databrickscfg file in your home directory (we're working on having the ability to create this config on the fly). The config file should look like the following:
```
[DEFAULT]
host = HOST
username = USERNAME
password = PASSWORD
token = DATABRICKS TOKEN
```
You can use you username and password and/or create an API token.

## Clusters

## DBFS

## Jobs

## Stacks
