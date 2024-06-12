from jinja2 import Environment, FileSystemLoader
import os

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

# Example usage
# replacements = {
#     "function_name": "my_function",
#     "parameters": "x, y",
#     "body": "return x + y",
#     "main_code": "print(my_function(5, 3))"
# }

# template_dir = '.'
# template_file = 'template.temp'
# output_file = 'generated_script.py'

# script_generator = ScriptGenerator(template_dir, template_file, replacements)
# script_generator.generate_script(output_file)
