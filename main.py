import generation.grid_generator, generation.person_generator
import render.Renderer

theGrid = generation.grid_generator.generate(100)
# theGrid.render()

persons = generation.person_generator.generate(theGrid, 10000)

# for thePerson in persons:
#     print(thePerson.home.x, thePerson.home.y)


render.Renderer.run(theGrid)

