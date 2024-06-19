from jinja2 import Environment, FileSystemLoader

class ScriptGenerator:
    def __init__(self, template_dir, template_file, replacements):
        self.template_dir = template_dir
        self.template_file = template_file
        self.replacements = replacements
        self.env = Environment(loader=FileSystemLoader(self.template_dir))

    def generate_script(self, output_file):
        template = self.env.get_template(self.template_file)
        script_content = template.render(self.replacements)
        
        with open(output_file, 'w') as file:
            file.write(script_content)
        
        print(f"Script generated: {output_file}")
        
    def get_generated_script(self):
        template = self.env.get_template(self.template_file)
        return template.render(self.replacements)