# profile.py

import geni.portal as portal
import geni.rspec.pg as rspec

# Create a Request object to start building the RSpec.
request = portal.context.makeRequestRSpec()

# Node webserver
webserver = request.RawPC("webserver")
webserver.hardware_type = "pc3000"  # Specify hardware type if needed
webserver.routable_control_ip = True

# Node observer
observer = request.RawPC("observer")
observer.hardware_type = "pc3000"  # Specify hardware type if needed

# Link between the nodes
link = request.Link(members = [webserver, observer])

# Print the generated RSpec
portal.context.printRequestRSpec()

