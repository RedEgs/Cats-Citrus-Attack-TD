
# RedEngine

RedEngine is a game engine designed on top of [pygame-ce](https://github.com/pygame-community/pygame-ce) and [PyQT6](https://pypi.org/project/PyQt6/). RedEngine was originally a framework for pygame, but now its a full app and has many useful features

# Background (You can skip)

PyRedEngine was originally a framework I had written for pygame when I was first learning it. As I improved, I started getting irritated by all the flaws of the engine and it honestly proved to be more cumbersome than just writing for the components that I needed at the time. 

The framework also became a huge time sink as I spent far more hours making the framework than the game itself, I'm sure if you've tried making any tools for yourself, you'd find thats also the case. 

Anyway, the game I was making with the engine was for my A-Level computer science coursework, called "citrus cats tower defense", heavily inspired by Bloons TD 6 at the time. Like I said, the framework became a huge time sink and I actually enjoyed making that more than the game. 

Shortly after I realised this, I pivoted the direction of my coursework to be the engine itself and so I spent a lot of time converting the engine into something that was more aligned to a an application rather than a framework. 

After many, many rewrites, the engine became completely different to what it was originally and so I made it into it's own thing which is now the RedEngine.  

Lots of the code in the engine is from older versions of the engine where I wasn't nearly as proficient at programming as I am now and lots of it is sloppy code when I realised I actually had a deadline to meet, that being my A-Level hand in date which caught me massively off guard aha.

If you really want to look at how far the whole project has come, every single interation, change, decision, file etc is available to look at on the commit timeline. You can check out an older version of the engine when I was just a framework at this git repo, it SHOULD be usable right away but i've archived the repo now.

# 📦 Technologies

This project is made using the following technologies:

- [Python 3.9+](https://www.python.org/) The programming language I used to build with
- [pygame-ce](https://github.com/pygame-community/pygame-ce) for the game part of the game engine
- [PyQT6](https://pypi.org/project/PyQt6/) for the engine's main app UI 
- [Qscintilla](https://qscintilla.com/) a PyQT5/6 integrated code editor
- [PyInstaller](https://pyinstaller.org/en/stable/) a tool for compiling python to a single binary/executable

# ⭐ Features

*You can scroll down to see more videos and images of the project actually working, you don't just have to take my word for it.* 

This is everything you can do with RedEngine:

-  **Project Manager/Launcher:** You can save, load and share projects. Projects contain all the code, assets and libraries necessary for a project, this makes them fully self contained (*other than the python installation*) and git compatible. 

- **Resource Manager:** Within the engine's UI is a panel which can be used to create, load, edit, rename files along with displaying their file sizes and types and their role within the project. 

- **Integrated Code Editor:** There's a simple code editor you can use to edit files completely within the engine, it also features syntax highlighting for python files. 

- **Integrated Viewport:** Once you select a python file as the "main" one, you can run the pygame code within the engine and it'll display it on the viewport just like other game engines like Unity, Godot etc. The game can be paused, started, stopped or even save state. 

- **Hot-loading/Live code editing:** One of the engines most compelling features is that you can edit the game's code while it runs. This means you can change features and iterate quicker. There's a little bit more to it than that, but it works REALLY well.

- **Properties Inspector:** Another big feature of the engine, is that it has a properties inspector which is capable of editing and viewing the attributes of any object and displaying it within interface. This also makes iteration very quick.

- **Debug Information:** The engine also has a panel for obtaining the debug information and performance info. It lets you see the FPS average, 1% high and 1% low, general resource usage by the process. It even has a draw call counter which see's is able to count how many function's are drawing to the screen within a single frame, making optimisation easier to improve.

- **Command Prompt:** The engine has a command prompt for running python code during runtime, it can be useful for running code during runtime or general debugging.

- **Integrated compiler:** The engine features a build tool which allows you to compile your entire project into a single executable removing the headache of having to use PyInstaller yourself. It also features a few quality of life options allowing you transpile your project to a RedEngine agnostic file so you can use it as if it weren't even made using the engine.

# ⚙️ The Process

Disclaimer: *This project took a lot of time to make it into what it was now, and i'd even say about 70% of the time i spent on this project, was working on sub-projects which I then merged into the main product. A lot of the process was quite non-linear and so it's quite hard to describe it like it was, so don't take it too seriously.*

### Product Analysis
When I first locked in the idea of creating the engine, I started
by doing a product analysis of similar game engines. The game engine's which I analysed were: [Unity](https://unity.com/), [Unreal Engine](https://www.unrealengine.com/en-US), [Roblox Studio](https://create.roblox.com/) and [Godot](https://godotengine.org/). I analysed them against 4 topics using their strengths and weaknesses of those topics to weigh them. Those 4 topics being the following:
- User Interface within the engine, 
- Integration of features 
- Integration of extra features (Quality of life etc)
- Community support & documentation 
Then I closed the evaluation of each with closing thoughts and anything else i'd like to say about it. The reason I did this was so I could any features I liked and avoid any features I didn't like for my product. This gave me a feature list to work towards.

### Success Criteria
After doing product analysis, I defined the limitations of my approach to the solution, such as being limited to CPU rendering, language speed etc. To conclude this stage of my project, I created a success criteria to work towards which would serve as an evaluator of my success when I reach the end of my project as well as a goal.

### Programming 
At this point I started actually programming the engine, but to be 100% honest, I was quite eager to get coding so I had already tested some features on their own at this point. For some of the systems I was able to create them quite quickly, but other like the hot-loader, it required a lot of revision and planning. 

### Revision and Cleanup
By the time I had all the features in the engine, I still had a little bit of time, so I spent a lot of it rewriting components to fit better with the other systems in the engine, so that also took a lot of time. 

Around the time of my deadline, the engine was pretty complete but just lacked a little bit of polish and robustness but overall I'm quite happy with how the process went but a lot was learned and I know what i'd now do going further.

# 📈 What I've learned

Since this was my first project where I actually had a criteria and deadline to meet, I learned a lot about managing a project generally and allocating my time. 

### Planning saves A LOT of time    

I don't ever plan my projects, to be honest. Before this one, I couldn't see the value of planning a project because I always thought I'd "just figure it out" or "i'd manage" and I think part of this was because I'm very eager to code before I think which costs me a lot of time later down the line. 

Despite the fact I still spent countless hours refactoring, I'm 1000% certain that I would've spent a lot more If I didnt. It also really, really helped keep my thoughts aligned and preventing me from feature creeping too hard, which I am very prone to. 

Ultimately, I think its thanks to planning that I loved the project so much and that it turned out the way it did. Not only this but it really helped me from feature creeping and was one of the only projects that I didn't burn out from.

### Documenting is worth the time

Like I said previously, I've never taken on a formal project like this one and so I was required to document my features and ideas for this project. I always thought it'd be a waste of time since i'd understand it all anyway, or so I thought.

Lots of the time spent on this project was documenting my ideas and such, which allowed me to spot flaws in my ideas while explaining them. It also helped me understand my code better weirdly? 

Since I spent so much time writing up my ideas, plans, code etc. I found I spent a fair amount of time away from my code which becomes a hassle because then I normally have to re-learn it again, but I didn't feel that way despite the size of the codebase at this point. So, all in all, going forward, i'm definetly going to document my projects much more.


Anyway, If I kept going this page would be massive, so those were just a couple points. On the other hand, here's what I'd change about the project itself. 

# 🔧 What I'd change/improve.

- **Making the engine portable:** What I mean by this is, I wish I made the engine its own application maybe even in another language like C++ or Java, so I could properly install this on a system. As it stands right now, its just some python scripts and not very usable as a product.

- **Using virtual environments:** One of the issues with the engine is that it relies on using your systems installation of python, which if you've ever used python on any other OS than Windows, that very quickly becomes a problem with package managers and such. Some developers also prefer not to install or modify packages system wide as it messes with version dependencies etc. So if I could go back in time, i'd definelty orient the whole project manager to rely on Venvs which also would make projects even more portable than they are now.

# ▶️ Running the engine

To run the engine, follow these steps:

- Clone the repo onto your machine

- Install all the packages in `requirements.txt`

- Navigate to `ApplicationEngine/redengine`

- Run `engine_main.py` 

To test the engine you can create a new project and it'll generate a minimal example so you can test the engine right away. 
*You can try running some of the test projects in the test folder, absolutely no gaurantee that any of them work though.*

# 🎥 Videos/Demos

https://github.com/user-attachments/assets/adcf296d-5a6d-402b-a56d-8306a38b4aac

https://github.com/user-attachments/assets/41d1b91c-92f8-4224-bcc9-79a71d08092a

https://github.com/user-attachments/assets/5adb7543-479d-4fee-a554-ab05ee1b09a1

https://github.com/user-attachments/assets/16f67cf4-f8a4-4a40-8a23-06bf4ed6e7c4






