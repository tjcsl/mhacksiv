import project
import os

app = project.app
app.debug = False

app.run(port=os.getenv('PORT', 5000))
