import subprocess
import json
import argparse
import shutil
import os
import zipfile

plugin_id_list = [
    10102, # Ok, Gradle!
    7793, # Markdown
    6351, # Dart
    9212, # Flutter
]

parser = argparse.ArgumentParser(description="Download and install personal plugin list for Intellij kind IDE")
parser.add_argument("plugin_path", metavar="plugin_path", help="Path to install the plugin")

def retrieve_last(array):
    return array[len(array) - 1]

if __name__ == '__main__':
    args = parser.parse_args()

    for plugin_id in plugin_id_list:
        response = subprocess.run(['curl', "https://plugins.jetbrains.com/api/plugins/{plugin_id}/updates".format(plugin_id = plugin_id)], capture_output=True)
        #("https://plugins.jetbrains.com/files/" + json.loads(response.stdout)[0]['file'])
        json_res = json.loads(response.stdout)[0]
        file_path = "https://plugins.jetbrains.com/files/" + json_res['file'] + "?updatedId=" + str(json_res["id"]) + "&pluginId=" + str(plugin_id) + "&family=INTELLIJ"
        file_name = retrieve_last(json.loads(response.stdout)[0]['file'].split("/"))
        subprocess.run(['curl', file_path, '-o', file_name])
        with zipfile.ZipFile(file_name) as zipped:
            zipped.extractall(args.plugin_path)
        os.remove(file_name)