import click
import json
from spreadsheet.download import download_xml
from config_upload.uploader import upload_cfg
@click.group()
def cmd_entry():
    '''
    cli for Universal Farm System
    '''
    pass

@cmd_entry.command()
@click.option("--cfg", "config", type=click.Path(file_okay=True), required=True, help="the query constrain of download file")
def download(config:str):
    download_xml(file=config)

@cmd_entry.command()
@click.option("--node_id", "node_id", type=str, required=True, help="the node token of target node")
@click.option("--cfg", "config", type=click.Path(file_okay=True), required=True, help="the configuration file of node")
def upload_node_cfg(node_id:str, config:str):
    upload_cfg(node_id=node_id, cfg=json.loads(open(config).read()))

if __name__ == "__main__":
    cmd_entry.add_command(download)
    cmd_entry.add_command(upload_node_cfg)
    cmd_entry()