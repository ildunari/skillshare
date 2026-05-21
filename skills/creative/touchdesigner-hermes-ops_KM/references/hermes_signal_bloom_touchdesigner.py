# Paste into TouchDesigner Textport or run via td_execute_python once twozero MCP is ready.
# Builds a simple Hermes-colored procedural network using built-in TOPs.

root = op('/project1')
for child in list(root.children):
    if child.name.startswith('hermes_') and child.valid:
        child.destroy()

noise = root.create(noiseTOP, 'hermes_noise')
noise.par.outputresolution = 'custom'
noise.par.resolutionw = 1280
noise.par.resolutionh = 720
noise.par.type = 'sparse'
noise.par.period = 5
noise.par.harmon = 6
noise.par.mono = False
noise.par.level = 0.75
noise.par.offsetx.expr = 'absTime.seconds * 0.045'
noise.par.offsety.expr = 'absTime.seconds * 0.025'

level = root.create(levelTOP, 'hermes_bloom_level')
noise.outputConnectors[0].connect(level.inputConnectors[0])
level.par.blacklevel = 0.18
level.par.brightness1 = 1.25
level.par.gamma1 = 0.72

blur = root.create(blurTOP, 'hermes_soft_bloom')
level.outputConnectors[0].connect(blur.inputConnectors[0])
blur.par.filter = 'gaussian'
blur.par.size = 12

comp = root.create(compositeTOP, 'hermes_composite')
level.outputConnectors[0].connect(comp.inputConnectors[0])
blur.outputConnectors[0].connect(comp.inputConnectors[1])
comp.par.operand = 'screen'

out = root.create(nullTOP, 'hermes_out')
comp.outputConnectors[0].connect(out.inputConnectors[0])
out.viewer = True
out.display = True

for i, node in enumerate([noise, level, blur, comp, out]):
    node.nodeX = i * 220
    node.nodeY = 0

result = {'created': [n.path for n in [noise, level, blur, comp, out]], 'output': out.path}
