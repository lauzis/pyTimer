#!/usr/bin/python
class activeColab:
    def __init__(self):
        return None
    
    def ac_api_get_projects():
        project_list_url= self.time_api_url + "?path_info=projects&format=json&auth_api_token="+self.settings.api_key;
        request = requests.get(project_list_url)
        projects = json.loads(request.content)
        print(projects)