# VS-Code-Workspace-Creator
python app with a gui to make vscode workspace files super quick either one by one or for all folders inside another folder

## why use this?

* saves u time clickin around in vscode to make workspaces
* good if u gotta make lotsa workspace files for many projects
* u can make em for specific folders u pick or batch create for all folders inside a parent folder

## gettin started

1.  **need python:** make sure u got python installed (like python 3.8 or newer probably works)
2.  **install the fancy gui stuff:** this app uses customtkinter so u gotta install it
    ```bash
    pip install customtkinter
    ```
3.  **get the code:** download the python script (`.py` file) from this repo

## how to run it

just open ur terminal or command prompt go to the folder where u saved the script and run:

```bash
python your_script_name.py
(replace your_script_name.py with whatever u called the file like ws_maker_app.py or somethin)how to use the appits pretty simple:Add Folder to List: click this pick a folder adds it to the white box listRemove Selected: click a folder in the list then click this removes itClear List: removes everything from the listCreate in Subfolders...: click this pick a parent folder itll find all folders directly inside that parent and make a workspace file in each of themCreate Workspaces for Folders in List: click this big button at the bottom itll make a workspace file inside each folder u added to the listLog Box: the box at the bottom shows u whats happenin successes
```
