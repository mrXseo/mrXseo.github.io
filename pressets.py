class html_file():

    def __init__(self, path, lang = "en"):
        self.lang : str = lang
        self.content : list[str] = []
        self.head : list[str] = []
        self.body : list[str] = []
        self.path : str = path
        self.html_objects : list = []
    
    def load(self):
        f = open("index.html", "w")
        for st in self.content:
            f.writelines(st + "\n")

    def add_html_obj(self, obj):
        self.html_objects.append(obj)
    
    def build_html(self):
        self.content.clear()
        self.content.append("<!DOCTYPE html>")
        self.content.append('<html lang="'+self.lang+'">')

        self.head.append('<head>')
        self.head.append('\t<style>')
        for html_obj in self.html_objects:
            self.head += html_obj.get_style()
        self.head.append('\t</style>')
        self.head.append('</head>')

        self.body.append('<body>')
        for html_obj in self.html_objects:
            self.body += html_obj.get_body()
        self.body.append('</body>')


        self.content += self.head
        self.content += self.body
        self.content.append('</html>')

class HtmlObj:
    pass

class HtmlObj:

    objs_last_id = {
        "obj":0,
    }

    def __init__(self, style_name = "obj", **kwargs):
        self.style_name = style_name
        if style_name in HtmlObj.objs_last_id.keys():
            self.name = style_name + str(HtmlObj.objs_last_id[self.style_name])
        else:
            HtmlObj.objs_last_id[style_name] = 0
            self.name = style_name + str(HtmlObj.objs_last_id[self.style_name])
        HtmlObj.objs_last_id[style_name] += 1
        self.content : list[str] = []
        self.child_html_objs : list[HtmlObj] = []
        self.params : dict[str, str] = {}
        for arg_key in kwargs:
            self.params[arg_key] = kwargs[arg_key]

    def get_style(self) -> list[str]:
        string_list = []
        string_list.append("\t\t."+self.name+" {")
        for param_name in self.params:
            string_list.append("\t\t\t"+param_name+": "+self.params[param_name] + " ;")
        string_list.append("\t\t}")
        
        for obj in self.child_html_objs:
            string_list += obj.get_style()

        return string_list

    def set_content(self, content : list[str] = []):
        self.content = content

    def get_body(self, deep = 1) -> list[str]:
        string_list : list[str] = []
        string_list.append("\t"*deep + '<div class="'+self.name+'">')
        string_list += self.content
        for html_obj in self.child_html_objs:
            string_list += html_obj.get_body(deep+1)
        string_list.append("\t"*deep + '</div>')
        return string_list

    def add_obj(self, obj : HtmlObj):
        self.child_html_objs.append(obj)