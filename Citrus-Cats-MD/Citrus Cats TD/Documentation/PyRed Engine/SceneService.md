Here is an example of what a scene would look like 

``` python
class ExampleScene(SceneService.Scene):
    def __init__(self, scene_name, app):
        super().__init__(scene_name, app)

    def on_enter(self):
        return super().on_enter()

    def update(self):
        pass

    def draw(self):
        self.app.get_screen().fill((0, 255, 0))
        
```
