import project
import os

app = project.app
app.debug = False

app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
